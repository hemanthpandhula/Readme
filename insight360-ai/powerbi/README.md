# Power BI Implementation Guide

## Dashboards
1. Executive Overview
2. Sales and Customer Analytics
3. Finance and Operations
4. Data Quality and ETL

## Data source
Use PostgreSQL `insight360` database and analytical views:
- `vw_dashboard_summary`
- `vw_monthly_revenue`
- `vw_region_performance`
- `vw_top_customers`
- `vw_data_quality_latest`
- `fact_sales`, `fact_expenses`, `fact_inventory`

## Required DAX measures
Stored in `powerbi/dax/measures.dax`.

## Build steps
1. Open Power BI Desktop.
2. Get Data -> PostgreSQL -> local connection.
3. Import listed views and dimensions.
4. Mark `dim_date` as Date table.
5. Create measures from `powerbi/dax/measures.dax`.
6. Add slicers for date, region, category.
7. Configure drill-through pages for region and customer.
