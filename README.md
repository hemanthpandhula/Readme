# Insight360 AI Workspace

This repository contains the **Insight360 AI** project scaffold and implementation under `/home/runner/work/Readme/Readme/insight360-ai`.

## Quick start

```bash
cd /home/runner/work/Readme/Readme/insight360-ai
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python datasets/generate_data.py
docker compose up -d postgres
python etl/pipelines/run_etl.py --mode full
uvicorn backend.app.main:app --reload --port 8000
```

Frontend:

```bash
cd /home/runner/work/Readme/Readme/insight360-ai/frontend
npm install
npm run dev
```
