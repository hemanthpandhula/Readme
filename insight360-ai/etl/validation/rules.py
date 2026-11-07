from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "sales_transactions": [
        "transaction_id",
        "transaction_ts",
        "customer_id",
        "product_id",
        "region_code",
        "department_code",
        "quantity",
        "unit_price",
        "discount_pct",
        "discount_amount",
        "revenue",
        "cost",
        "profit",
    ],
    "customers": ["customer_id", "customer_name", "segment", "region_code", "city", "email", "signup_date"],
    "products": ["product_id", "product_name", "category", "supplier_id", "standard_cost", "list_price"],
    "regions": ["region_code", "region_name", "country", "manager_name"],
    "departments": ["department_code", "department_name"],
    "suppliers": ["supplier_id", "supplier_name", "region_code", "rating"],
    "expenses": ["expense_id", "expense_date", "department_code", "region_code", "expense_type", "amount"],
    "inventory": ["inventory_id", "inventory_date", "product_id", "region_code", "opening_qty", "received_qty", "issued_qty", "closing_qty"],
    "dates": ["date", "year", "month", "day", "month_name", "quarter", "week_of_year", "is_weekend"],
}


def missing_columns(df: pd.DataFrame, table: str) -> list[str]:
    expected = set(REQUIRED_COLUMNS[table])
    return sorted(expected - set(df.columns))


def split_valid_invalid_sales(df: pd.DataFrame):
    work = df.copy()
    work["transaction_ts"] = pd.to_datetime(work["transaction_ts"], errors="coerce")
    rules = (
        work["transaction_ts"].notna()
        & (work["quantity"] > 0)
        & (work["revenue"] >= 0)
        & work["customer_id"].notna()
        & work["product_id"].notna()
    )
    valid = work[rules].drop_duplicates(subset=["transaction_id"])
    invalid = work[~rules | work.duplicated(subset=["transaction_id"], keep=False)]
    return valid, invalid
