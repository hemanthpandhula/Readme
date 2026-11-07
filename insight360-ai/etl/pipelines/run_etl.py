from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from etl.validation.rules import REQUIRED_COLUMNS, missing_columns, split_valid_invalid_sales

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "datasets" / "generated"
REPORT_DIR = ROOT / "etl" / "reports"
SCHEMA_SQL = ROOT / "sql" / "schema" / "001_create_schema.sql"
VIEW_SQL = ROOT / "sql" / "views" / "analytics_views.sql"


def get_engine():
    import os

    database_url = os.getenv("DATABASE_URL", "******localhost:5432/insight360")
    return create_engine(database_url, future=True)


def read_table(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")
    if path.suffix == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)


def validate_inputs() -> dict[str, pd.DataFrame]:
    frames = {}
    for table in REQUIRED_COLUMNS:
        frame = read_table(table)
        missing = missing_columns(frame, table)
        if missing:
            raise ValueError(f"{table}: missing columns {missing}")
        if frame.empty:
            raise ValueError(f"{table}: empty file")
        frames[table] = frame
    return frames


def execute_sql_file(conn, path: Path):
    sql_text = path.read_text()
    for statement in [s.strip() for s in sql_text.split(';') if s.strip()]:
        conn.execute(text(statement))


def load_tables(conn, frames: dict[str, pd.DataFrame], execution_id: int):
    mapping = {
        "regions": "ops_regions",
        "departments": "ops_departments",
        "suppliers": "ops_suppliers",
        "products": "ops_products",
        "customers": "ops_customers",
        "expenses": "ops_expenses",
        "inventory": "ops_inventory",
    }

    for src, table in mapping.items():
        frames[src].to_sql(table, conn, if_exists="append", index=False, method="multi")

    sales_valid, sales_invalid = split_valid_invalid_sales(frames["sales_transactions"])
    sales_valid.to_sql("ops_sales_transactions", conn, if_exists="append", index=False, method="multi")

    for _, row in sales_invalid.head(5000).iterrows():
        conn.execute(
            text(
                """
                INSERT INTO rejected_records(execution_id, source_table, reason, payload)
                VALUES (:execution_id, 'ops_sales_transactions', :reason, CAST(:payload AS JSONB))
                """
            ),
            {
                "execution_id": execution_id,
                "reason": "validation failure",
                "payload": row.to_json(date_format="iso"),
            },
        )

    date_frame = frames["dates"].copy()
    date_frame["date"] = pd.to_datetime(date_frame["date"]).dt.date
    date_frame["date_key"] = pd.to_datetime(date_frame["date"]).dt.strftime("%Y%m%d").astype(int)
    date_frame = date_frame.rename(columns={"date": "full_date"})
    date_frame[["date_key", "full_date", "year", "month", "day", "month_name", "quarter", "week_of_year", "is_weekend"]].to_sql(
        "dim_date", conn, if_exists="append", index=False, method="multi"
    )

    conn.execute(text("""
        INSERT INTO dim_region(region_code, region_name, country, manager_name)
        SELECT region_code, region_name, country, manager_name FROM ops_regions
        ON CONFLICT(region_code) DO NOTHING
    """))
    conn.execute(text("""
        INSERT INTO dim_department(department_code, department_name)
        SELECT department_code, department_name FROM ops_departments
        ON CONFLICT(department_code) DO NOTHING
    """))
    conn.execute(text("""
        INSERT INTO dim_supplier(supplier_id, supplier_name, region_code, rating)
        SELECT supplier_id, supplier_name, region_code, rating FROM ops_suppliers
        ON CONFLICT(supplier_id) DO NOTHING
    """))
    conn.execute(text("""
        INSERT INTO dim_product(product_id, product_name, category, supplier_key, standard_cost, list_price)
        SELECT p.product_id, p.product_name, p.category, ds.supplier_key, p.standard_cost, p.list_price
        FROM ops_products p
        LEFT JOIN dim_supplier ds ON p.supplier_id = ds.supplier_id
        ON CONFLICT(product_id) DO NOTHING
    """))
    conn.execute(text("""
        INSERT INTO dim_customer(customer_id, customer_name, segment, region_key, city, email, signup_date)
        SELECT c.customer_id, c.customer_name, c.segment, dr.region_key, c.city, c.email, c.signup_date
        FROM ops_customers c
        LEFT JOIN dim_region dr ON c.region_code = dr.region_code
        ON CONFLICT(customer_id) DO NOTHING
    """))

    conn.execute(text("""
        INSERT INTO fact_sales(transaction_id, date_key, customer_key, product_key, region_key, department_key, quantity, unit_price, discount_pct, discount_amount, revenue, cost, profit, execution_id)
        SELECT
          s.transaction_id,
          TO_CHAR(DATE(s.transaction_ts), 'YYYYMMDD')::INT,
          dc.customer_key,
          dp.product_key,
          dr.region_key,
          dd.department_key,
          s.quantity,
          s.unit_price,
          s.discount_pct,
          s.discount_amount,
          s.revenue,
          s.cost,
          s.profit,
          :execution_id
        FROM ops_sales_transactions s
        JOIN dim_customer dc ON s.customer_id = dc.customer_id
        JOIN dim_product dp ON s.product_id = dp.product_id
        JOIN dim_region dr ON s.region_code = dr.region_code
        JOIN dim_department dd ON s.department_code = dd.department_code
        ON CONFLICT(transaction_id) DO NOTHING
    """), {"execution_id": execution_id})

    conn.execute(text("""
        INSERT INTO fact_expenses(expense_id, date_key, region_key, department_key, expense_type, amount, execution_id)
        SELECT
          e.expense_id,
          TO_CHAR(e.expense_date, 'YYYYMMDD')::INT,
          dr.region_key,
          dd.department_key,
          e.expense_type,
          e.amount,
          :execution_id
        FROM ops_expenses e
        JOIN dim_region dr ON e.region_code = dr.region_code
        JOIN dim_department dd ON e.department_code = dd.department_code
        ON CONFLICT(expense_id) DO NOTHING
    """), {"execution_id": execution_id})

    conn.execute(text("""
        INSERT INTO fact_inventory(inventory_id, date_key, product_key, region_key, opening_qty, received_qty, issued_qty, closing_qty, execution_id)
        SELECT
          i.inventory_id,
          TO_CHAR(i.inventory_date, 'YYYYMMDD')::INT,
          dp.product_key,
          dr.region_key,
          i.opening_qty,
          i.received_qty,
          i.issued_qty,
          i.closing_qty,
          :execution_id
        FROM ops_inventory i
        JOIN dim_product dp ON i.product_id = dp.product_id
        JOIN dim_region dr ON i.region_code = dr.region_code
        ON CONFLICT(inventory_id) DO NOTHING
    """), {"execution_id": execution_id})

    return len(sales_valid), len(sales_invalid)


def run(mode: str = "full"):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    frames = validate_inputs()
    engine = get_engine()

    with engine.begin() as conn:
        execute_sql_file(conn, SCHEMA_SQL)
        execution_id = conn.execute(
            text(
                """
                INSERT INTO etl_execution(execution_mode, status, source_path, notes)
                VALUES (:mode, 'running', :source_path, 'Insight360 ETL execution')
                RETURNING execution_id
                """
            ),
            {"mode": mode, "source_path": str(DATA_DIR)},
        ).scalar_one()

        if mode == "full":
            for t in [
                "fact_sales",
                "fact_expenses",
                "fact_inventory",
                "dim_customer",
                "dim_product",
                "dim_supplier",
                "dim_department",
                "dim_region",
                "dim_date",
                "ops_sales_transactions",
                "ops_expenses",
                "ops_inventory",
                "ops_customers",
                "ops_products",
                "ops_suppliers",
                "ops_departments",
                "ops_regions",
            ]:
                conn.execute(text(f"TRUNCATE TABLE {t} RESTART IDENTITY CASCADE"))

        valid_sales, invalid_sales = load_tables(conn, frames, execution_id)
        execute_sql_file(conn, VIEW_SQL)

        total_records = sum(len(df) for df in frames.values())
        rejected_records = invalid_sales
        valid_records = total_records - rejected_records
        quality_score = round((valid_records / total_records) * 100, 2)

        conn.execute(
            text(
                """
                UPDATE etl_execution
                SET status = 'success', ended_at = NOW(), total_records = :total_records,
                    valid_records = :valid_records, rejected_records = :rejected_records,
                    quality_score = :quality_score
                WHERE execution_id = :execution_id
                """
            ),
            {
                "execution_id": execution_id,
                "total_records": total_records,
                "valid_records": valid_records,
                "rejected_records": rejected_records,
                "quality_score": quality_score,
            },
        )

    report = {
        "execution_id": execution_id,
        "mode": mode,
        "total_records": total_records,
        "valid_records": valid_records,
        "rejected_records": rejected_records,
        "quality_score": quality_score,
    }
    report_file = REPORT_DIR / f"etl_execution_{execution_id}.json"
    report_file.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insight360 ETL pipeline")
    parser.add_argument("--mode", choices=["full", "incremental"], default="full")
    args = parser.parse_args()
    run(mode=args.mode)
