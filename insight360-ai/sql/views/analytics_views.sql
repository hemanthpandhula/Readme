CREATE OR REPLACE VIEW vw_dashboard_summary AS
SELECT
  COALESCE(SUM(fs.revenue),0) AS total_revenue,
  COALESCE(SUM(fs.cost),0) AS total_cost,
  COALESCE(SUM(fs.profit),0) AS total_profit,
  COALESCE(SUM(fe.amount),0) AS total_expenses,
  CASE WHEN SUM(fs.revenue) = 0 THEN 0 ELSE (SUM(fs.profit) / SUM(fs.revenue)) * 100 END AS profit_margin_pct,
  COUNT(DISTINCT fs.transaction_id) AS transaction_count
FROM fact_sales fs
LEFT JOIN fact_expenses fe ON fs.date_key = fe.date_key;

CREATE OR REPLACE VIEW vw_monthly_revenue AS
SELECT
  dd.year,
  dd.month,
  MIN(dd.full_date) AS period_start,
  SUM(fs.revenue) AS revenue,
  SUM(fs.profit) AS profit,
  SUM(fs.quantity) AS quantity
FROM fact_sales fs
JOIN dim_date dd ON fs.date_key = dd.date_key
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;

CREATE OR REPLACE VIEW vw_region_performance AS
SELECT
  dr.region_name,
  SUM(fs.revenue) AS revenue,
  SUM(fs.profit) AS profit,
  CASE WHEN SUM(fs.revenue)=0 THEN 0 ELSE SUM(fs.profit)/SUM(fs.revenue) END AS margin
FROM fact_sales fs
JOIN dim_region dr ON fs.region_key = dr.region_key
GROUP BY dr.region_name;

CREATE OR REPLACE VIEW vw_top_customers AS
SELECT
  dc.customer_name,
  dc.segment,
  SUM(fs.revenue) AS revenue,
  SUM(fs.profit) AS profit,
  COUNT(*) AS orders
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
GROUP BY dc.customer_name, dc.segment;

CREATE OR REPLACE VIEW vw_data_quality_latest AS
SELECT
  execution_id,
  status,
  started_at,
  ended_at,
  total_records,
  valid_records,
  rejected_records,
  quality_score,
  notes
FROM etl_execution
ORDER BY execution_id DESC
LIMIT 1;
