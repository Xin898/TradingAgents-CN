from datetime import datetime, timedelta, timezone

from platform_integration.contracts import AnalysisSignal, Direction


def test_analysis_signal_freshness():
    now = datetime.now(timezone.utc)
    signal = AnalysisSignal(
        analysisId="a-1",
        instrument="AAPL",
        direction=Direction.LONG,
        confidence=0.8,
        riskFactors=[],
        dataTimestamp=now,
        validUntil=now + timedelta(minutes=5),
        modelVersion="test",
        schemaVersion=1,
    )

    assert signal.is_stale(now) is False
    assert signal.is_stale(now + timedelta(minutes=6)) is True
