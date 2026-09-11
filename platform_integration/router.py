from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .contracts import AnalysisSignal, Direction


router = APIRouter(prefix="/api/v1/platform", tags=["platform-integration"])


class AnalysisRequest(BaseModel):
    instrument: str
    horizon: str = "1D"


@router.post("/analysis", response_model=AnalysisSignal, status_code=202)
async def request_analysis(request: AnalysisRequest) -> AnalysisSignal:
    """
    Foundation endpoint for the downstream trading platform.

    TODO next epic:
      1. create asynchronous analysis job
      2. execute TradingAgents workflow
      3. persist result
      4. publish versioned AnalysisSignal event
    """
    now = datetime.now(timezone.utc)

    # Placeholder result: this is intentionally NOT a trading order.
    # It proves the platform contract while keeping execution responsibilities
    # inside StockTrader/CrypTrader.
    if not request.instrument.strip():
        raise HTTPException(status_code=400, detail="instrument is required")

    return AnalysisSignal(
        analysisId=f"analysis-{uuid4()}",
        instrument=request.instrument.upper(),
        direction=Direction.NEUTRAL,
        confidence=0.0,
        riskFactors=["analysis-workflow-not-yet-connected"],
        dataTimestamp=now,
        validUntil=now,
        modelVersion="foundation-placeholder",
        schemaVersion=1,
    )
