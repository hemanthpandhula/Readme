from __future__ import annotations


def approved_functions() -> dict[str, str]:
    return {
        "summary": "SELECT * FROM vw_dashboard_summary",
        "top_customers": "SELECT customer_name, revenue FROM vw_top_customers ORDER BY revenue DESC LIMIT 10",
        "highest_revenue_region": "SELECT region_name, revenue FROM vw_region_performance ORDER BY revenue DESC LIMIT 1",
        "profit_drop_reason": """
            WITH monthly AS (
              SELECT year, month, revenue, profit
              FROM vw_monthly_revenue
            )
            SELECT m.*, 
                   (m.profit - LAG(m.profit) OVER (ORDER BY year, month)) AS profit_delta,
                   (m.revenue - LAG(m.revenue) OVER (ORDER BY year, month)) AS revenue_delta
            FROM monthly m
            ORDER BY year DESC, month DESC
            LIMIT 3
        """,
        "anomalies": "SELECT * FROM anomaly_results ORDER BY anomaly_score DESC LIMIT 20",
        "forecast": "SELECT * FROM forecast_results ORDER BY forecast_period DESC LIMIT 12",
    }
