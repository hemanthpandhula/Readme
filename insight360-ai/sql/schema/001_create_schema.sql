CREATE TABLE IF NOT EXISTS etl_execution (
  execution_id BIGSERIAL PRIMARY KEY,
  execution_mode VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  source_path TEXT,
  total_records INT DEFAULT 0,
  valid_records INT DEFAULT 0,
  rejected_records INT DEFAULT 0,
  quality_score NUMERIC(5,2),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS rejected_records (
  reject_id BIGSERIAL PRIMARY KEY,
  execution_id BIGINT REFERENCES etl_execution(execution_id),
  source_table VARCHAR(100) NOT NULL,
  reason TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_regions (
  region_code VARCHAR(20) PRIMARY KEY,
  region_name VARCHAR(80) NOT NULL,
  country VARCHAR(80) NOT NULL,
  manager_name VARCHAR(120) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_departments (
  department_code VARCHAR(20) PRIMARY KEY,
  department_name VARCHAR(80) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_suppliers (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(120) NOT NULL,
  region_code VARCHAR(20) REFERENCES ops_regions(region_code),
  rating INT CHECK (rating BETWEEN 1 AND 5),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(120) NOT NULL,
  category VARCHAR(80) NOT NULL,
  supplier_id INT REFERENCES ops_suppliers(supplier_id),
  standard_cost NUMERIC(12,2) NOT NULL CHECK (standard_cost >= 0),
  list_price NUMERIC(12,2) NOT NULL CHECK (list_price >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_customers (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(120) NOT NULL,
  segment VARCHAR(80) NOT NULL,
  region_code VARCHAR(20) REFERENCES ops_regions(region_code),
  city VARCHAR(80),
  email VARCHAR(150),
  signup_date DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_sales_transactions (
  transaction_id BIGINT PRIMARY KEY,
  transaction_ts TIMESTAMPTZ NOT NULL,
  customer_id INT REFERENCES ops_customers(customer_id),
  product_id INT REFERENCES ops_products(product_id),
  region_code VARCHAR(20) REFERENCES ops_regions(region_code),
  department_code VARCHAR(20) REFERENCES ops_departments(department_code),
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
  discount_pct NUMERIC(7,4) NOT NULL CHECK (discount_pct BETWEEN 0 AND 1),
  discount_amount NUMERIC(12,2) NOT NULL,
  revenue NUMERIC(14,2) NOT NULL,
  cost NUMERIC(14,2) NOT NULL,
  profit NUMERIC(14,2) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_expenses (
  expense_id BIGINT PRIMARY KEY,
  expense_date DATE NOT NULL,
  department_code VARCHAR(20) REFERENCES ops_departments(department_code),
  region_code VARCHAR(20) REFERENCES ops_regions(region_code),
  expense_type VARCHAR(80) NOT NULL,
  amount NUMERIC(14,2) NOT NULL CHECK (amount > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ops_inventory (
  inventory_id BIGINT PRIMARY KEY,
  inventory_date DATE NOT NULL,
  product_id INT REFERENCES ops_products(product_id),
  region_code VARCHAR(20) REFERENCES ops_regions(region_code),
  opening_qty INT NOT NULL,
  received_qty INT NOT NULL,
  issued_qty INT NOT NULL,
  closing_qty INT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dim_date (
  date_key INT PRIMARY KEY,
  full_date DATE NOT NULL UNIQUE,
  year INT NOT NULL,
  month INT NOT NULL,
  day INT NOT NULL,
  month_name VARCHAR(20) NOT NULL,
  quarter INT NOT NULL,
  week_of_year INT NOT NULL,
  is_weekend BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_region (
  region_key BIGSERIAL PRIMARY KEY,
  region_code VARCHAR(20) NOT NULL UNIQUE,
  region_name VARCHAR(80) NOT NULL,
  country VARCHAR(80) NOT NULL,
  manager_name VARCHAR(120) NOT NULL,
  effective_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
  effective_end_date DATE,
  is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS dim_department (
  department_key BIGSERIAL PRIMARY KEY,
  department_code VARCHAR(20) NOT NULL UNIQUE,
  department_name VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_supplier (
  supplier_key BIGSERIAL PRIMARY KEY,
  supplier_id INT NOT NULL UNIQUE,
  supplier_name VARCHAR(120) NOT NULL,
  region_code VARCHAR(20),
  rating INT
);

CREATE TABLE IF NOT EXISTS dim_product (
  product_key BIGSERIAL PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  product_name VARCHAR(120) NOT NULL,
  category VARCHAR(80) NOT NULL,
  supplier_key BIGINT REFERENCES dim_supplier(supplier_key),
  standard_cost NUMERIC(12,2) NOT NULL,
  list_price NUMERIC(12,2) NOT NULL,
  effective_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
  effective_end_date DATE,
  is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS dim_customer (
  customer_key BIGSERIAL PRIMARY KEY,
  customer_id INT NOT NULL UNIQUE,
  customer_name VARCHAR(120) NOT NULL,
  segment VARCHAR(80) NOT NULL,
  region_key BIGINT REFERENCES dim_region(region_key),
  city VARCHAR(80),
  email VARCHAR(150),
  signup_date DATE,
  effective_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
  effective_end_date DATE,
  is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS fact_sales (
  sales_key BIGSERIAL PRIMARY KEY,
  transaction_id BIGINT NOT NULL UNIQUE,
  date_key INT NOT NULL REFERENCES dim_date(date_key),
  customer_key BIGINT NOT NULL REFERENCES dim_customer(customer_key),
  product_key BIGINT NOT NULL REFERENCES dim_product(product_key),
  region_key BIGINT NOT NULL REFERENCES dim_region(region_key),
  department_key BIGINT NOT NULL REFERENCES dim_department(department_key),
  quantity INT NOT NULL,
  unit_price NUMERIC(12,2) NOT NULL,
  discount_pct NUMERIC(7,4) NOT NULL,
  discount_amount NUMERIC(12,2) NOT NULL,
  revenue NUMERIC(14,2) NOT NULL,
  cost NUMERIC(14,2) NOT NULL,
  profit NUMERIC(14,2) NOT NULL,
  execution_id BIGINT REFERENCES etl_execution(execution_id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fact_expenses (
  expense_key BIGSERIAL PRIMARY KEY,
  expense_id BIGINT NOT NULL UNIQUE,
  date_key INT NOT NULL REFERENCES dim_date(date_key),
  region_key BIGINT NOT NULL REFERENCES dim_region(region_key),
  department_key BIGINT NOT NULL REFERENCES dim_department(department_key),
  expense_type VARCHAR(80) NOT NULL,
  amount NUMERIC(14,2) NOT NULL,
  execution_id BIGINT REFERENCES etl_execution(execution_id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fact_inventory (
  inventory_key BIGSERIAL PRIMARY KEY,
  inventory_id BIGINT NOT NULL UNIQUE,
  date_key INT NOT NULL REFERENCES dim_date(date_key),
  product_key BIGINT NOT NULL REFERENCES dim_product(product_key),
  region_key BIGINT NOT NULL REFERENCES dim_region(region_key),
  opening_qty INT NOT NULL,
  received_qty INT NOT NULL,
  issued_qty INT NOT NULL,
  closing_qty INT NOT NULL,
  execution_id BIGINT REFERENCES etl_execution(execution_id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_region ON fact_sales(region_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_expenses_date ON fact_expenses(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_inventory_date ON fact_inventory(date_key);
