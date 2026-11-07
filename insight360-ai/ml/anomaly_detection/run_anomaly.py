from __future__ import annotations

from pathlib import Path
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "ml" / "reports" / "anomaly_results.csv"


def load_sales() -> pd.DataFrame:
    db = os.getenv("DATABASE_URL", "******localhost:5432/insight360")
    engine = create_engine(db, future=True)
    query = """
    SELECT fs.transaction_id, fs.quantity, fs.discount_pct, fs.revenue, fs.cost, fs.profit,
           dr.region_name, dp.category
    FROM fact_sales fs
    JOIN dim_region dr ON fs.region_key = dr.region_key
    JOIN dim_product dp ON fs.product_key = dp.product_key
    """
    return pd.read_sql_query(query, engine)


def run() -> pd.DataFrame:
    df = load_sales()
    X = df[["quantity", "discount_pct", "revenue", "cost", "profit"]].astype(float)

    model = IsolationForest(contamination=0.02, random_state=42)
    labels = model.fit_predict(X)
    scores = -model.score_samples(X)

    z = np.abs((X["revenue"] - X["revenue"].mean()) / X["revenue"].std(ddof=0))
    baseline_flag = z > 3

    out = df.copy()
    out["anomaly_score"] = scores
    out["is_unusual_transaction"] = labels == -1
    out["baseline_high_zscore"] = baseline_flag
    out["reason"] = np.where(
        out["is_unusual_transaction"],
        "IsolationForest flagged this transaction as unusual based on multi-feature pattern.",
        "No unusual behavior detected by model.",
    )

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(REPORT, index=False)
    db = os.getenv("DATABASE_URL", "******localhost:5432/insight360")
    engine = create_engine(db, future=True)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS anomaly_results (
                  result_id BIGSERIAL PRIMARY KEY,
                  transaction_id BIGINT,
                  quantity NUMERIC,
                  discount_pct NUMERIC,
                  revenue NUMERIC,
                  cost NUMERIC,
                  profit NUMERIC,
                  region_name VARCHAR(80),
                  category VARCHAR(80),
                  anomaly_score NUMERIC,
                  is_unusual_transaction BOOLEAN,
                  baseline_high_zscore BOOLEAN,
                  reason TEXT,
                  execution_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )
        conn.execute(text("TRUNCATE TABLE anomaly_results"))
    out.to_sql("anomaly_results", engine, if_exists="append", index=False, method="multi")
    return out


if __name__ == "__main__":
    data = run()
    print(f"Generated anomaly results: {len(data)} rows -> {REPORT}")
