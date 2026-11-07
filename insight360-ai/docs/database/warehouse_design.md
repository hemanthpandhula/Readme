# Warehouse Design

## Layers
1. Operational ingestion tables (`ops_*`)
2. Analytical star schema (`dim_*`, `fact_*`)

## SCD Strategy
- `dim_customer`, `dim_product`, and `dim_region` include SCD Type 2 fields:
  - `effective_start_date`
  - `effective_end_date`
  - `is_current`
- Current ETL MVP performs upsert-on-natural-key and preserves SCD fields for extension.

## Audit and governance
- `etl_execution` logs execution mode, status, quality score, and row counts.
- `rejected_records` stores quarantined invalid rows with reasons.
