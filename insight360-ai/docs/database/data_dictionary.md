# Data Dictionary (Synthetic)

All datasets are synthetic and reproducible from `datasets/generate_data.py` with random seed `42`.

## Core files
- `sales_transactions.csv`: transactional sales facts.
- `customers.csv`: customer master.
- `products.csv`: product master.
- `regions.csv`: region master.
- `departments.csv`: department master.
- `expenses.csv`: operational expense events.
- `inventory.csv`: inventory movements.
- `suppliers.csv`: supplier master.
- `dates.csv`: date dimension source.

## Column summaries

### sales_transactions.csv
- transaction_id: unique transaction number.
- transaction_ts: transaction timestamp.
- customer_id: customer reference.
- product_id: product reference.
- region_code: region reference.
- department_code: department reference.
- quantity: sold units.
- unit_price: pre-discount selling price.
- discount_pct: discount rate.
- discount_amount: total discount amount.
- revenue: net revenue.
- cost: cost of goods sold.
- profit: revenue minus cost.

### customers.csv
- customer_id, customer_name, segment, region_code, city, email, signup_date.

### products.csv
- product_id, product_name, category, supplier_id, standard_cost, list_price.

### regions.csv
- region_code, region_name, country, manager_name.

### departments.csv
- department_code, department_name.

### expenses.csv
- expense_id, expense_date, department_code, region_code, expense_type, amount.

### inventory.csv
- inventory_id, inventory_date, product_id, region_code, opening_qty, received_qty, issued_qty, closing_qty.

### suppliers.csv
- supplier_id, supplier_name, region_code, rating.
