from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable

from .contracts import AnalysisSignal, MarketView


_BULLISH = {"buy", "strong_buy", "long", "bullish", "买入", "看多"}
_BEARISH = {"sell", "strong_sell", "short", "bearish", "卖出", "看空"}


def _utc(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str) and value:
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            dt = datetime.now(timezone.utc)
    else:
        dt = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _confidence(value: Any) -> float:
    try:
        score = float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0
    if score > 1.0 and score <= 100.0:
        score /= 100.0
    return max(0.0, min(1.0, score))


def _market_view(result: Dict[str, Any]) -> MarketView:
    decision = result.get("decision") or {}
    action = str(decision.get("action") or "").strip().lower().replace(" ", "_")
    if action in _BULLISH:
        return MarketView.BULLISH
    if action in _BEARISH:
        return MarketView.BEARISH
    return MarketView.NEUTRAL


def _risk_factors(result: Dict[str, Any]) -> Iterable[str]:
    factors = []
    risk_level = result.get("risk_level")
    if risk_level:
        factors.append(f"risk-level:{risk_level}")
    decision = result.get("decision") or {}
    raw = decision.get("risk_factors") or result.get("risk_factors") or []
    if isinstance(raw, str):
        raw = [raw]
    factors.extend(str(item).strip() for item in raw if str(item).strip())
    return list(dict.fromkeys(factors))


def to_analysis_signal(analysis_id: str, result: Dict[str, Any], ttl_minutes: int = 60) -> AnalysisSignal:
    instrument = result.get("stock_symbol") or result.get("stock_code")
    if not instrument:
        raise ValueError("analysis result has no instrument")

    decision = result.get("decision") or {}
    confidence = decision.get("confidence", result.get("confidence_score", 0.0))
    timestamp = _utc(result.get("updated_at") or result.get("analysis_date") or result.get("created_at"))
    model_version = result.get("model_info") or decision.get("model_version") or "tradingagents-current"

    return AnalysisSignal(
        analysisId=analysis_id,
        instrument=str(instrument).upper(),
        marketView=_market_view(result),
        confidence=_confidence(confidence),
        riskFactors=list(_risk_factors(result)),
        dataTimestamp=timestamp,
        validUntil=timestamp + timedelta(minutes=ttl_minutes),
        modelVersion=str(model_version),
        schemaVersion=1,
    )
