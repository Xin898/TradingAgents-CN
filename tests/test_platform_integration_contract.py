from datetime import datetime, timezone

from platform_integration.contracts import MarketView
from platform_integration.mapper import to_analysis_signal


def test_maps_buy_decision_to_bullish_signal():
    signal = to_analysis_signal(
        "task-123",
        {
            "stock_symbol": "AAPL",
            "decision": {"action": "BUY", "confidence": 82},
            "risk_level": "medium",
            "updated_at": datetime(2026, 9, 17, 10, 0, tzinfo=timezone.utc),
            "model_info": "qwen-max",
        },
    )

    assert signal.analysis_id == "task-123"
    assert signal.instrument == "AAPL"
    assert signal.market_view == MarketView.BULLISH
    assert signal.confidence == 0.82
    assert signal.schema_version == 1
    assert "risk-level:medium" in signal.risk_factors
    assert signal.valid_until > signal.data_timestamp


def test_unknown_action_is_neutral_not_order_instruction():
    signal = to_analysis_signal(
        "task-456",
        {
            "stock_symbol": "MSFT",
            "decision": {"action": "WAIT", "confidence": 0.6},
            "analysis_date": "2026-09-17T10:00:00Z",
        },
    )

    assert signal.market_view == MarketView.NEUTRAL
    assert signal.confidence == 0.6


def test_confidence_is_clamped():
    signal = to_analysis_signal(
        "task-789",
        {"stock_symbol": "NVDA", "confidence_score": 150, "decision": {}},
    )
    assert signal.confidence == 1.0
