from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
BASE = Path(__file__).resolve().parent / "generated"
BASE.mkdir(parents=True, exist_ok=True)


def _save(df: pd.DataFrame, name: str) -> None:
    df.to_csv(BASE / name, index=False)


def build_regions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "region_code": ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"],
            "region_name": ["North", "South", "East", "West", "Central"],
            "country": ["India"] * 5,
            "manager_name": [f"Manager {i}" for i in range(1, 6)],
        }
    )


def build_departments() -> pd.DataFrame:
    names = ["Sales", "Finance", "Operations", "Customer Management"]
    return pd.DataFrame({"department_code": [f"D{i:02d}" for i in range(1, 5)], "department_name": names})


def build_suppliers(n: int = 20) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "supplier_id": np.arange(1, n + 1),
            "supplier_name": [f"Supplier {i}" for i in range(1, n + 1)],
            "region_code": rng.choice(["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"], n),
            "rating": rng.integers(2, 6, n),
        }
    )


def build_products(n: int = 120) -> pd.DataFrame:
    categories = ["Beverages", "Snacks", "Personal Care", "Household", "Stationery"]
    return pd.DataFrame(
        {
            "product_id": np.arange(1, n + 1),
            "product_name": [f"Product {i}" for i in range(1, n + 1)],
            "category": rng.choice(categories, n),
            "supplier_id": rng.integers(1, 21, n),
            "standard_cost": np.round(rng.uniform(5, 800, n), 2),
            "list_price": np.round(rng.uniform(10, 1200, n), 2),
        }
    )


def build_customers(n: int = 1200) -> pd.DataFrame:
    segments = ["Enterprise", "SMB", "Retail", "Online"]
    return pd.DataFrame(
        {
            "customer_id": np.arange(1, n + 1),
            "customer_name": [f"Customer {i}" for i in range(1, n + 1)],
            "segment": rng.choice(segments, n),
            "region_code": rng.choice(["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"], n),
            "city": rng.choice(["Hyderabad", "Bengaluru", "Delhi", "Mumbai", "Chennai"], n),
            "email": [f"customer{i}@example.com" for i in range(1, n + 1)],
            "signup_date": pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 700, n), unit="D"),
        }
    )


def build_dates(start: str = "2024-01-01", end: str = "2025-12-31") -> pd.DataFrame:
    dates = pd.date_range(start=start, end=end, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "year": dates.year,
            "month": dates.month,
            "day": dates.day,
            "month_name": dates.strftime("%B"),
            "quarter": dates.quarter,
            "week_of_year": dates.isocalendar().week.astype(int),
            "is_weekend": dates.dayofweek >= 5,
        }
    )


def build_sales(rows: int = 14000) -> pd.DataFrame:
    tx_dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 730, rows), unit="D")
    quantity = rng.integers(1, 30, rows)
    unit_price = rng.uniform(20, 1500, rows)
    discount_pct = rng.choice([0, 0.02, 0.05, 0.1, 0.15], rows, p=[0.35, 0.2, 0.2, 0.2, 0.05])
    gross = quantity * unit_price
    discount_amount = gross * discount_pct
    revenue = gross - discount_amount
    cost = revenue * rng.uniform(0.55, 0.9, rows)
    profit = revenue - cost

    return pd.DataFrame(
        {
            "transaction_id": np.arange(1, rows + 1),
            "transaction_ts": tx_dates + pd.to_timedelta(rng.integers(0, 86400, rows), unit="s"),
            "customer_id": rng.integers(1, 1201, rows),
            "product_id": rng.integers(1, 121, rows),
            "region_code": rng.choice(["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"], rows),
            "department_code": rng.choice(["D01", "D02", "D03", "D04"], rows),
            "quantity": quantity,
            "unit_price": np.round(unit_price, 2),
            "discount_pct": np.round(discount_pct, 4),
            "discount_amount": np.round(discount_amount, 2),
            "revenue": np.round(revenue, 2),
            "cost": np.round(cost, 2),
            "profit": np.round(profit, 2),
        }
    )


def build_expenses(rows: int = 1500) -> pd.DataFrame:
    dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 730, rows), unit="D")
    return pd.DataFrame(
        {
            "expense_id": np.arange(1, rows + 1),
            "expense_date": dates,
            "department_code": rng.choice(["D01", "D02", "D03", "D04"], rows),
            "region_code": rng.choice(["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"], rows),
            "expense_type": rng.choice(["Logistics", "Payroll", "Marketing", "Rent", "Utilities"], rows),
            "amount": np.round(rng.uniform(2000, 150000, rows), 2),
        }
    )


def build_inventory(rows: int = 4000) -> pd.DataFrame:
    dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 730, rows), unit="D")
    opening = rng.integers(0, 500, rows)
    received = rng.integers(0, 300, rows)
    issued = rng.integers(0, 300, rows)
    closing = opening + received - issued
    return pd.DataFrame(
        {
            "inventory_id": np.arange(1, rows + 1),
            "inventory_date": dates,
            "product_id": rng.integers(1, 121, rows),
            "region_code": rng.choice(["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"], rows),
            "opening_qty": opening,
            "received_qty": received,
            "issued_qty": issued,
            "closing_qty": closing,
        }
    )


def build_quality_issues(sales: pd.DataFrame) -> pd.DataFrame:
    bad = sales.sample(120, random_state=SEED).copy()
    bad.loc[bad.index[:20], "quantity"] = -5
    bad.loc[bad.index[20:40], "transaction_ts"] = "2035-15-99"
    bad.loc[bad.index[40:60], "revenue"] = -100
    bad.loc[bad.index[60:80], "customer_id"] = 999999
    bad.loc[bad.index[80:100], "product_id"] = np.nan
    bad = pd.concat([bad, bad.head(20)], ignore_index=True)
    return bad


def main() -> None:
    regions = build_regions()
    departments = build_departments()
    suppliers = build_suppliers()
    products = build_products()
    customers = build_customers()
    dates = build_dates()
    sales = build_sales()
    expenses = build_expenses()
    inventory = build_inventory()
    issues = build_quality_issues(sales)

    for name, df in {
        "regions.csv": regions,
        "departments.csv": departments,
        "suppliers.csv": suppliers,
        "products.csv": products,
        "customers.csv": customers,
        "dates.csv": dates,
        "sales_transactions.csv": sales,
        "sales_transactions_with_issues.csv": issues,
        "expenses.csv": expenses,
        "inventory.csv": inventory,
    }.items():
        _save(df, name)

    print("Generated synthetic datasets in", BASE)


if __name__ == "__main__":
    main()
