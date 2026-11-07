import pandas as pd

from etl.validation.rules import missing_columns, split_valid_invalid_sales


def test_missing_columns():
    df = pd.DataFrame({"transaction_id": [1]})
    missing = missing_columns(df, "sales_transactions")
    assert "quantity" in missing


def test_sales_validation_split():
    df = pd.DataFrame(
        {
            "transaction_id": [1, 2, 2],
            "transaction_ts": ["2024-01-01", "bad-date", "2024-02-01"],
            "customer_id": [1, 1, 1],
            "product_id": [1, 1, 1],
            "region_code": ["NORTH", "NORTH", "NORTH"],
            "department_code": ["D01", "D01", "D01"],
            "quantity": [5, 0, 3],
            "unit_price": [10, 10, 10],
            "discount_pct": [0.1, 0.1, 0.1],
            "discount_amount": [5, 1, 1],
            "revenue": [45, 9, 9],
            "cost": [30, 5, 5],
            "profit": [15, 4, 4],
        }
    )
    valid, invalid = split_valid_invalid_sales(df)
    assert len(valid) == 1
    assert len(invalid) >= 1
