from app.repositories.analytics_repository import AnalyticsRepository


class DashboardService:
    def __init__(self, repo: AnalyticsRepository):
        self.repo = repo

    def summary(self) -> dict:
        return self.repo.fetch_one("SELECT * FROM vw_dashboard_summary")

    def trends(self) -> list[dict]:
        return self.repo.fetch_all("SELECT * FROM vw_monthly_revenue ORDER BY year, month")

    def sales(self, limit: int = 100, offset: int = 0) -> list[dict]:
        return self.repo.fetch_all(
            """
            SELECT fs.transaction_id, dd.full_date, dc.customer_name, dp.product_name, dr.region_name,
                   fs.quantity, fs.revenue, fs.cost, fs.profit
            FROM fact_sales fs
            JOIN dim_date dd ON fs.date_key = dd.date_key
            JOIN dim_customer dc ON fs.customer_key = dc.customer_key
            JOIN dim_product dp ON fs.product_key = dp.product_key
            JOIN dim_region dr ON fs.region_key = dr.region_key
            ORDER BY fs.transaction_id DESC
            LIMIT :limit OFFSET :offset
            """,
            {"limit": limit, "offset": offset},
        )

    def customers(self) -> list[dict]:
        return self.repo.fetch_all("SELECT * FROM vw_top_customers ORDER BY revenue DESC LIMIT 100")

    def products(self) -> list[dict]:
        return self.repo.fetch_all(
            """
            SELECT dp.product_name, dp.category, SUM(fs.revenue) AS revenue, SUM(fs.profit) AS profit
            FROM fact_sales fs
            JOIN dim_product dp ON fs.product_key = dp.product_key
            GROUP BY dp.product_name, dp.category
            ORDER BY revenue DESC
            LIMIT 100
            """
        )

    def regions(self) -> list[dict]:
        return self.repo.fetch_all("SELECT * FROM vw_region_performance ORDER BY revenue DESC")

    def finance(self) -> list[dict]:
        return self.repo.fetch_all(
            """
            SELECT ddp.department_name, SUM(fe.amount) AS total_expense
            FROM fact_expenses fe
            JOIN dim_department ddp ON fe.department_key = ddp.department_key
            GROUP BY ddp.department_name
            ORDER BY total_expense DESC
            """
        )

    def data_quality(self) -> dict:
        return self.repo.fetch_one("SELECT * FROM vw_data_quality_latest")
