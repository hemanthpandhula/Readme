from __future__ import annotations

from pathlib import Path
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "ml" / "reports" / "forecast_results.csv"
METRICS = ROOT / "ml" / "reports" / "forecast_metrics.json"


def load_monthly_revenue() -> pd.DataFrame:
    db = os.getenv("DATABASE_URL", "******localhost:5432/insight360")
    engine = create_engine(db, future=True)
    q = "SELECT year, month, period_start, revenue FROM vw_monthly_revenue ORDER BY year, month"
    df = pd.read_sql_query(q, engine)
    df["period_start"] = pd.to_datetime(df["period_start"])
    return df


def run() -> pd.DataFrame:
    df = load_monthly_revenue()
    df["lag1"] = df["revenue"].shift(1)
    df["lag2"] = df["revenue"].shift(2)
    df = df.dropna().reset_index(drop=True)

    train_size = int(len(df) * 0.8)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    X_train = train[["year", "month", "lag1", "lag2"]]
    y_train = train["revenue"]
    X_test = test[["year", "month", "lag1", "lag2"]]
    y_test = test["revenue"]

    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    naive = test["lag1"].values

    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, preds))),
        "mape": float(mean_absolute_percentage_error(y_test, preds)),
        "naive_mae": float(mean_absolute_error(y_test, naive)),
    }

    result = test[["period_start", "revenue"]].copy()
    result["predicted_revenue"] = preds
    result["naive_baseline"] = naive

    last = df.iloc[-1]
    next_month = (pd.Timestamp(last["period_start"]) + pd.offsets.MonthBegin(1)).normalize()
    next_features = pd.DataFrame(
        [{
            "year": next_month.year,
            "month": next_month.month,
            "lag1": float(last["revenue"]),
            "lag2": float(df.iloc[-2]["revenue"]),
        }]
    )
    next_pred = float(model.predict(next_features)[0])

    forecast_row = pd.DataFrame(
        [{"period_start": next_month, "revenue": np.nan, "predicted_revenue": next_pred, "naive_baseline": float(last["revenue"])}]
    )
    result = pd.concat([result, forecast_row], ignore_index=True)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(REPORT, index=False)
    METRICS.write_text(str(metrics))
    db = os.getenv("DATABASE_URL", "******localhost:5432/insight360")
    engine = create_engine(db, future=True)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS forecast_results (
                  result_id BIGSERIAL PRIMARY KEY,
                  forecast_period DATE,
                  actual_revenue NUMERIC,
                  predicted_revenue NUMERIC,
                  naive_baseline NUMERIC,
                  execution_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )
        conn.execute(text("TRUNCATE TABLE forecast_results"))
    write = result.rename(columns={"period_start": "forecast_period", "revenue": "actual_revenue"})
    write.to_sql("forecast_results", engine, if_exists="append", index=False, method="multi")
    return result


if __name__ == "__main__":
    out = run()
    print(f"Generated forecast results: {len(out)} rows -> {REPORT}")
