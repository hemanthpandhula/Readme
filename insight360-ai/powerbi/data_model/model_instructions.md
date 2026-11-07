# Power BI Data Model Instructions

## Recommended star schema
- Dimensions: dim_date, dim_customer, dim_product, dim_region, dim_department, dim_supplier
- Facts: fact_sales, fact_expenses, fact_inventory

## Relationships
- fact_sales.date_key -> dim_date.date_key (many-to-one)
- fact_sales.customer_key -> dim_customer.customer_key
- fact_sales.product_key -> dim_product.product_key
- fact_sales.region_key -> dim_region.region_key
- fact_sales.department_key -> dim_department.department_key
- fact_expenses.date_key -> dim_date.date_key
- fact_expenses.region_key -> dim_region.region_key
- fact_expenses.department_key -> dim_department.department_key
- fact_inventory.date_key -> dim_date.date_key
- fact_inventory.product_key -> dim_product.product_key
- fact_inventory.region_key -> dim_region.region_key

Mark `dim_date[full_date]` as date table column.
