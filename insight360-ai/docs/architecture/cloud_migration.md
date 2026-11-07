# Azure + Fabric Migration Architecture

## Local to cloud mapping
- Local CSV inputs -> ADLS Gen2 landing zone
- Python ETL -> Azure Data Factory + Fabric Dataflows
- PostgreSQL warehouse -> Fabric Warehouse / Azure SQL
- ML scripts -> Azure ML / Fabric notebooks
- FastAPI service -> Azure Container Apps / App Service
- React frontend -> Azure Static Web Apps
- Secrets -> Azure Key Vault
- Monitoring -> Azure Monitor + Application Insights

## Governance and security
- Managed identities for service-to-service auth.
- Data access policies by domain and sensitivity.
- Lineage tracking via Fabric and Purview integration.
