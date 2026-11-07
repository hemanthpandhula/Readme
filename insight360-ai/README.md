# Insight360 AI

Enterprise business intelligence, predictive analytics, and AI-powered decision support platform (synthetic consulting case for retail/distribution).

## Business Problem
Leadership needs reliable visibility into revenue, profit, expenses, customer/product performance, unusual transactions, and short-term forecasts from one governed analytics platform.

## Objectives
- Ingest and validate raw business data
- Build normalized + star-schema warehouse in PostgreSQL
- Expose KPI and analytics APIs
- Detect unusual transactions and forecast revenue
- Provide grounded AI analytics assistant with deterministic fallback

## Key Features
- Reproducible synthetic data generation (10k+ sales records)
- Data-quality checks with quarantine and ETL execution reporting
- 30+ business SQL queries and analytical views
- FastAPI backend with service/repository layers
- React + Vite + TypeScript dashboard frontend
- Isolation Forest anomaly detection + baseline
- Revenue forecasting with baseline comparison and metrics
- Power BI implementation guide and DAX library

## Project Structure
See folder layout under `insight360-ai/`:
- `backend/`: FastAPI API
- `frontend/`: React web app
- `etl/`: extraction, validation, transformation, load pipeline
- `sql/`: schema, views, query library
- `ml/`: anomaly and forecasting pipelines
- `ai/`: provider abstraction and safety rules
- `datasets/`: generated data and samples
- `powerbi/`: DAX and report guidance
- `docs/`: architecture, API, database, interview assets

## Personas and KPIs
- Executive: revenue, profit, margin, growth
- Sales manager: top products/customers, regional performance
- Finance manager: expenses, profitability by department
- Operations manager: inventory and unusual transactions
- Data team: ETL status, quality score, data freshness

## Assumptions
- Data is synthetic and labeled as simulated.
- Local PostgreSQL is available using Docker compose.
- Power BI PBIX is manually created from documented model; no generated PBIX file is included.

## Acceptance Criteria (MVP)
- End-to-end flow from generated data -> ETL -> warehouse -> API -> frontend works locally.
- KPI values are sourced from warehouse queries only.
- Invalid records are quarantined, not loaded into clean warehouse facts.
- AI endpoint uses approved analytics functions and evidence-backed responses.

## Setup
### 1) Environment
```bash
cd /home/runner/work/Readme/Readme/insight360-ai
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 2) Start database
```bash
docker compose up -d postgres
```

### 3) Generate data + run ETL
```bash
python datasets/generate_data.py
python etl/pipelines/run_etl.py --mode full
```

### 4) Run backend
```bash
uvicorn backend.app.main:app --reload --port 8000
```

### 5) Run frontend
```bash
cd frontend
npm install
npm run dev
```

## Testing
```bash
cd /home/runner/work/Readme/Readme/insight360-ai
pytest backend/tests -q
```

## API Documentation
- OpenAPI: `http://localhost:8000/docs`
- Endpoint list: `docs/api/endpoints.md`

## Data Quality Reports
ETL execution reports are written to `etl/reports/` with quality score and rejected record counts.

## Security Controls (Local MVP)
- Environment-variable configuration
- Upload type/size validation
- Parameterized SQL for repository queries
- AI routed through approved function registry (no write SQL)
- Deterministic fallback if external provider is unavailable

## Production-Hardening Gaps
- Authentication and role-based authorization
- Strong SQL AST parser for any dynamic query path
- Caching, rate limiting, WAF, and full observability stack
- CI/CD and infrastructure-as-code deployment automation

## Screenshots Checklist
- [ ] Executive overview
- [ ] Sales/customer/product analytics
- [ ] ETL monitor and data quality
- [ ] Anomaly and forecasting pages
- [ ] AI assistant response with evidence

## Future Scope
- Incremental CDC ingestion
- Rich semantic layer and metric store
- Fabric-native orchestration
- MLOps model registry and drift detection
