# Business Requirements

## Departments
- Sales
- Finance
- Operations
- Customer Management
- Product Management
- Regional Management

## Core business questions
1. Total revenue
2. Net profit
3. Profit margin
4. Profit decrease drivers
5. Top revenue products
6. Poor-performing regions
7. Top customers
8. Rising expenses
9. Unusual transactions
10. Next month revenue forecast
11. Recommended actions

## Personas
- Executive sponsor
- Sales manager
- Finance controller
- Operations lead
- Data analyst

## KPIs
- Total Revenue
- Total Cost
- Total Profit
- Profit Margin
- Total Expenses
- Sales Growth (MoM/YoY)
- Average Order Value
- Anomaly Count
- Data Quality Score

## Assumptions
- Data is synthetic and generated with fixed seeds.
- KPI values are queried from warehouse facts/views.
- Invalid records are quarantined.

## Acceptance criteria
- End-to-end local execution works from generated data to dashboard/API.
- Required API endpoints respond with warehouse-backed data.
- ETL outputs quality score and rejected records.
- AI assistant returns evidence-backed answers from approved function queries.
