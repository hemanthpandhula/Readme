from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.analytics_repository import AnalyticsRepository, RepositoryError
from app.schemas.api import (
    AIChatRequest,
    AIChatResponse,
    DashboardSummaryResponse,
    DataQualityResponse,
    HealthResponse,
    MonthlyTrendPoint,
    RunResponse,
)
from app.services.ai_service import AIService
from app.services.dashboard_service import DashboardService
from app.services.etl_service import ETLService
from app.services.ml_service import MLService

router = APIRouter()


def _svc(db: Session) -> DashboardService:
    return DashboardService(AnalyticsRepository(db))


@router.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status='ok', service='insight360-backend', timestamp=datetime.utcnow())


@router.get('/dashboard/summary', response_model=DashboardSummaryResponse)
def dashboard_summary(db: Session = Depends(get_db)):
    try:
        return _svc(db).summary()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/dashboard/trends', response_model=list[MonthlyTrendPoint])
def dashboard_trends(db: Session = Depends(get_db)):
    try:
        return _svc(db).trends()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/sales')
def sales(limit: int = Query(default=100, ge=1, le=1000), offset: int = Query(default=0, ge=0), db: Session = Depends(get_db)):
    try:
        return _svc(db).sales(limit=limit, offset=offset)
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/customers')
def customers(db: Session = Depends(get_db)):
    try:
        return _svc(db).customers()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/products')
def products(db: Session = Depends(get_db)):
    try:
        return _svc(db).products()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/regions')
def regions(db: Session = Depends(get_db)):
    try:
        return _svc(db).regions()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/finance')
def finance(db: Session = Depends(get_db)):
    try:
        return _svc(db).finance()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.post('/data/upload', response_model=RunResponse)
async def upload_data(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in {'.csv', '.xlsx', '.xls'}:
        raise HTTPException(status_code=400, detail='Only CSV and Excel files are allowed')

    target_dir = Path(__file__).resolve().parents[3] / 'datasets' / 'raw'
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / file.filename
    content = await file.read()
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail='File exceeds 15MB limit')
    target.write_bytes(content)
    return RunResponse(status='success', detail=f'Uploaded to {target}')


@router.post('/etl/run', response_model=RunResponse)
def run_etl(mode: str = Query(default='full', pattern='^(full|incremental)$')):
    try:
        detail = ETLService().run(mode=mode)
        return RunResponse(status='success', detail=detail)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get('/etl/status', response_model=DataQualityResponse)
def etl_status(db: Session = Depends(get_db)):
    try:
        return _svc(db).data_quality()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/data-quality', response_model=DataQualityResponse)
def data_quality(db: Session = Depends(get_db)):
    try:
        return _svc(db).data_quality()
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get('/anomalies')
def anomalies(db: Session = Depends(get_db)):
    repo = AnalyticsRepository(db)
    try:
        return repo.fetch_all('SELECT * FROM anomaly_results ORDER BY anomaly_score DESC LIMIT 200')
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.post('/anomalies/run', response_model=RunResponse)
def run_anomalies():
    try:
        detail = MLService().run_anomaly()
        return RunResponse(status='success', detail=detail)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get('/forecasts')
def forecasts(db: Session = Depends(get_db)):
    repo = AnalyticsRepository(db)
    try:
        return repo.fetch_all('SELECT * FROM forecast_results ORDER BY forecast_period DESC LIMIT 60')
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.post('/forecasts/run', response_model=RunResponse)
def run_forecasts():
    try:
        detail = MLService().run_forecast()
        return RunResponse(status='success', detail=detail)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post('/ai/chat', response_model=AIChatResponse)
def ai_chat(request: AIChatRequest, db: Session = Depends(get_db)):
    try:
        result = AIService(AnalyticsRepository(db)).handle(request.question)
        return AIChatResponse(
            intent=result.intent,
            answer=result.answer,
            evidence=result.evidence,
            deterministic_fallback=result.deterministic_fallback,
        )
    except RepositoryError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
