-- Q01 total revenue
SELECT SUM(revenue) AS total_revenue FROM fact_sales;
-- Q02 total net profit
SELECT SUM(profit) AS total_profit FROM fact_sales;
-- Q03 profit margin
SELECT CASE WHEN SUM(revenue)=0 THEN 0 ELSE SUM(profit)/SUM(revenue) END AS margin FROM fact_sales;
-- Q04 monthly revenue trend
SELECT dd.year, dd.month, SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_date dd ON fs.date_key=dd.date_key GROUP BY dd.year,dd.month ORDER BY dd.year,dd.month;
-- Q05 monthly profit trend
SELECT dd.year, dd.month, SUM(fs.profit) profit FROM fact_sales fs JOIN dim_date dd ON fs.date_key=dd.date_key GROUP BY dd.year,dd.month ORDER BY dd.year,dd.month;
-- Q06 revenue by product
SELECT dp.product_name,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_product dp ON fs.product_key=dp.product_key GROUP BY dp.product_name ORDER BY revenue DESC;
-- Q07 top 10 products
SELECT dp.product_name,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_product dp ON fs.product_key=dp.product_key GROUP BY dp.product_name ORDER BY revenue DESC LIMIT 10;
-- Q08 bottom regions
SELECT dr.region_name,SUM(fs.profit) profit FROM fact_sales fs JOIN dim_region dr ON fs.region_key=dr.region_key GROUP BY dr.region_name ORDER BY profit ASC LIMIT 5;
-- Q09 top customers
SELECT dc.customer_name,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_customer dc ON fs.customer_key=dc.customer_key GROUP BY dc.customer_name ORDER BY revenue DESC LIMIT 10;
-- Q10 expenses by department
SELECT ddp.department_name,SUM(fe.amount) amount FROM fact_expenses fe JOIN dim_department ddp ON fe.department_key=ddp.department_key GROUP BY ddp.department_name ORDER BY amount DESC;
-- Q11 expense trend
SELECT d.year,d.month,SUM(fe.amount) amount FROM fact_expenses fe JOIN dim_date d ON fe.date_key=d.date_key GROUP BY d.year,d.month ORDER BY d.year,d.month;
-- Q12 duplicate transaction ids in ops
SELECT transaction_id,COUNT(*) c FROM ops_sales_transactions GROUP BY transaction_id HAVING COUNT(*)>1;
-- Q13 invalid quantities in ops
SELECT * FROM ops_sales_transactions WHERE quantity<=0;
-- Q14 missing customer reference
SELECT ost.transaction_id FROM ops_sales_transactions ost LEFT JOIN ops_customers oc ON ost.customer_id=oc.customer_id WHERE oc.customer_id IS NULL;
-- Q15 sales rank by revenue
SELECT dp.category, SUM(fs.revenue) revenue, RANK() OVER (ORDER BY SUM(fs.revenue) DESC) revenue_rank FROM fact_sales fs JOIN dim_product dp ON fs.product_key=dp.product_key GROUP BY dp.category;
-- Q16 running total
SELECT d.full_date, SUM(fs.revenue) revenue, SUM(SUM(fs.revenue)) OVER (ORDER BY d.full_date) running_revenue FROM fact_sales fs JOIN dim_date d ON fs.date_key=d.date_key GROUP BY d.full_date ORDER BY d.full_date;
-- Q17 mom growth
WITH m AS (SELECT d.year,d.month,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_date d ON fs.date_key=d.date_key GROUP BY d.year,d.month) SELECT year,month,revenue, LAG(revenue) OVER (ORDER BY year,month) prev_revenue, CASE WHEN LAG(revenue) OVER (ORDER BY year,month)=0 THEN NULL ELSE (revenue-LAG(revenue) OVER (ORDER BY year,month))/LAG(revenue) OVER (ORDER BY year,month) END mom_growth FROM m;
-- Q18 yoy growth
WITH y AS (SELECT d.year,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_date d ON fs.date_key=d.date_key GROUP BY d.year) SELECT year,revenue, LAG(revenue) OVER (ORDER BY year) prev_revenue, CASE WHEN LAG(revenue) OVER (ORDER BY year)=0 THEN NULL ELSE (revenue-LAG(revenue) OVER (ORDER BY year))/LAG(revenue) OVER (ORDER BY year) END yoy_growth FROM y;
-- Q19 avg order value
SELECT AVG(revenue) AS avg_order_value FROM fact_sales;
-- Q20 region margin
SELECT dr.region_name,CASE WHEN SUM(fs.revenue)=0 THEN 0 ELSE SUM(fs.profit)/SUM(fs.revenue) END margin FROM fact_sales fs JOIN dim_region dr ON fs.region_key=dr.region_key GROUP BY dr.region_name;
-- Q21 customer lifetime proxy
SELECT dc.customer_name, SUM(fs.revenue) lifetime_revenue FROM fact_sales fs JOIN dim_customer dc ON fs.customer_key=dc.customer_key GROUP BY dc.customer_name ORDER BY lifetime_revenue DESC;
-- Q22 product contribution
SELECT dp.category, SUM(fs.revenue) revenue, SUM(fs.revenue)/SUM(SUM(fs.revenue)) OVER () contribution FROM fact_sales fs JOIN dim_product dp ON fs.product_key=dp.product_key GROUP BY dp.category;
-- Q23 monthly anomaly candidates high discounts
SELECT d.year,d.month,COUNT(*) AS suspicious_discount_orders FROM fact_sales fs JOIN dim_date d ON fs.date_key=d.date_key WHERE fs.discount_pct>0.12 GROUP BY d.year,d.month ORDER BY d.year,d.month;
-- Q24 inventory stockouts
SELECT COUNT(*) stockout_events FROM fact_inventory WHERE closing_qty<0;
-- Q25 latest etl status
SELECT * FROM vw_data_quality_latest;
-- Q26 rejected records by table
SELECT source_table,COUNT(*) rejects FROM rejected_records GROUP BY source_table;
-- Q27 top expense region
SELECT dr.region_name,SUM(fe.amount) amount FROM fact_expenses fe JOIN dim_region dr ON fe.region_key=dr.region_key GROUP BY dr.region_name ORDER BY amount DESC LIMIT 1;
-- Q28 product and region matrix
SELECT dp.category,dr.region_name,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_product dp ON fs.product_key=dp.product_key JOIN dim_region dr ON fs.region_key=dr.region_key GROUP BY dp.category,dr.region_name;
-- Q29 finance ratio
SELECT SUM(fs.profit) / NULLIF(SUM(fe.amount),0) AS profit_to_expense_ratio FROM fact_sales fs CROSS JOIN fact_expenses fe;
-- Q30 stale data check
SELECT MAX(d.full_date) AS latest_date, CURRENT_DATE - MAX(d.full_date) AS days_stale FROM fact_sales fs JOIN dim_date d ON fs.date_key=d.date_key;
-- Q31 top supplier contribution
SELECT ds.supplier_name,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_product dp ON fs.product_key=dp.product_key JOIN dim_supplier ds ON dp.supplier_key=ds.supplier_key GROUP BY ds.supplier_name ORDER BY revenue DESC LIMIT 10;
-- Q32 department performance
SELECT dd.department_name,SUM(fs.revenue) revenue,SUM(fs.profit) profit FROM fact_sales fs JOIN dim_department dd ON fs.department_key=dd.department_key GROUP BY dd.department_name;
-- Q33 expense growth by type
WITH e AS (SELECT d.year,d.month,expense_type,SUM(amount) amount FROM fact_expenses fe JOIN dim_date d ON fe.date_key=d.date_key GROUP BY d.year,d.month,expense_type) SELECT *, amount - LAG(amount) OVER (PARTITION BY expense_type ORDER BY year,month) delta FROM e;
-- Q34 customer segment margin
SELECT dc.segment, SUM(fs.profit)/NULLIF(SUM(fs.revenue),0) AS margin FROM fact_sales fs JOIN dim_customer dc ON fs.customer_key=dc.customer_key GROUP BY dc.segment;
-- Q35 contribution by month and region
SELECT d.year,d.month,dr.region_name,SUM(fs.revenue) revenue FROM fact_sales fs JOIN dim_date d ON fs.date_key=d.date_key JOIN dim_region dr ON fs.region_key=dr.region_key GROUP BY d.year,d.month,dr.region_name ORDER BY d.year,d.month,revenue DESC;