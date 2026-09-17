import asyncio

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.analysis import SingleAnalysisRequest
from app.routers.auth_db import get_current_user
from app.services.simple_analysis_service import get_simple_analysis_service

from .contracts import AnalysisAccepted, AnalysisJobStatus, AnalysisRequest, AnalysisSignal, AnalysisStatusResponse
from .service import platform_integration_service


router = APIRouter(prefix="/api/v1/platform", tags=["platform-integration"])


@router.post("/analyses", response_model=AnalysisAccepted, status_code=status.HTTP_202_ACCEPTED)
async def create_analysis(request: AnalysisRequest, user: dict = Depends(get_current_user)) -> AnalysisAccepted:
    """Start TradingAgents analysis and return a stable platform analysis ID."""
    symbol = request.instrument.strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="instrument is required")

    internal_request = SingleAnalysisRequest(symbol=symbol)
    analysis_service = get_simple_analysis_service()
    created = await analysis_service.create_analysis_task(user["id"], internal_request)
    analysis_id = created["task_id"]

    async def execute() -> None:
        service = get_simple_analysis_service()
        await service.execute_analysis_background(analysis_id, user["id"], internal_request)

    # V1 reuses the current TradingAgents execution model. A durable queue/worker
    # can replace this without changing the public integration contract.
    asyncio.create_task(execute())

    return AnalysisAccepted(analysisId=analysis_id, status=AnalysisJobStatus.PENDING, schemaVersion=1)


@router.get("/analyses/{analysis_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(analysis_id: str, _: dict = Depends(get_current_user)) -> AnalysisStatusResponse:
    result = await platform_integration_service.status(analysis_id)
    if result is None:
        raise HTTPException(status_code=404, detail="analysis not found")
    return result


@router.get("/analyses/{analysis_id}/signal", response_model=AnalysisSignal)
async def get_analysis_signal(analysis_id: str, _: dict = Depends(get_current_user)) -> AnalysisSignal:
    current_status = await platform_integration_service.status(analysis_id)
    if current_status is None:
        raise HTTPException(status_code=404, detail="analysis not found")
    if current_status.status == AnalysisJobStatus.FAILED:
        raise HTTPException(status_code=409, detail="analysis failed")
    if current_status.status != AnalysisJobStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="analysis is not completed")

    signal = await platform_integration_service.signal(analysis_id)
    if signal is None:
        raise HTTPException(status_code=404, detail="completed analysis has no result")
    return signal
