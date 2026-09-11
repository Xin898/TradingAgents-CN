from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Direction(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"


class AnalysisSignal(BaseModel):
    """Versioned decision-support contract exposed to downstream Trader SCSs."""

    analysis_id: str = Field(alias="analysisId")
    instrument: str
    direction: Direction
    confidence: float = Field(ge=0.0, le=1.0)
    risk_factors: List[str] = Field(default_factory=list, alias="riskFactors")
    data_timestamp: datetime = Field(alias="dataTimestamp")
    valid_until: datetime = Field(alias="validUntil")
    model_version: str = Field(alias="modelVersion")
    schema_version: int = Field(default=1, alias="schemaVersion")

    model_config = {"populate_by_name": True}

    def is_stale(self, now: datetime) -> bool:
        return now >= self.valid_until
