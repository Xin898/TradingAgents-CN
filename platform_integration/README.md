# Platform Integration Boundary

This package is the explicit integration boundary between TradingAgents-CN and the downstream Trader SCSs.

## Rule

TradingAgents produces decision-support signals, never broker/exchange orders.

TradingAgents workflow -> AnalysisSignal -> StockTrader/CrypTrader -> Strategy -> Risk -> OMS -> Execution

## Contract goals

- versioned schema
- explicit freshness through dataTimestamp and validUntil
- idempotency via analysisId
- no leakage of TradingAgents internal persistence models
- backward-compatible evolution
- no dependency on Alpaca/Binance concepts

The initial router is a foundation endpoint only. The next epic should replace the placeholder with an asynchronous analysis job, persisted result and versioned event publication.
