from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MarketView(str, Enum):
    """Market opinion only. It is deliberately not an executable order side."""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class AnalysisJobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class AnalysisRequest(BaseModel):
    instrument: str = Field(min_length=1)
    horizon: str = Field(default="1D", min_length=1)


class AnalysisAccepted(BaseModel):
    analysis_id: str = Field(alias="analysisId")
    status: AnalysisJobStatus
    schema_version: int = Field(default=1, alias="schemaVersion")

    model_config = {"populate_by_name": True}


class AnalysisStatusResponse(BaseModel):
    analysis_id: str = Field(alias="analysisId")
    status: AnalysisJobStatus
    progress: int = Field(default=0, ge=0, le=100)
    instrument: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    completed_at: Optional[datetime] = Field(default=None, alias="completedAt")
    error: Optional[str] = None
    schema_version: int = Field(default=1, alias="schemaVersion")

    model_config = {"populate_by_name": True}


class AnalysisSignal(BaseModel):
    """Versioned decision-support contract consumed by StockTrader/CrypTrader.

    This contract expresses a market opinion. It MUST NOT be interpreted as an
    order and intentionally contains no quantity, account or execution fields.
    """

    analysis_id: str = Field(alias="analysisId")
    instrument: str
    market_view: MarketView = Field(alias="marketView")
    confidence: float = Field(ge=0.0, le=1.0)
    risk_factors: List[str] = Field(default_factory=list, alias="riskFactors")
    data_timestamp: datetime = Field(alias="dataTimestamp")
    valid_until: datetime = Field(alias="validUntil")
    model_version: str = Field(alias="modelVersion")
    schema_version: int = Field(default=1, alias="schemaVersion")

    model_config = {"populate_by_name": True}

    def is_stale(self, now: datetime) -> bool:
        return now >= self.valid_until
