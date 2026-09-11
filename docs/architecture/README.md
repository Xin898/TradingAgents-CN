# Trading Platform Integration Architecture

This document describes the **target integration role** of TradingAgents-CN in the wider portfolio architecture. It does not replace the upstream project's original licensing or product documentation.

## SCS role

TradingAgents-CN acts as an **AI Market Intelligence / Decision Support SCS**.

It produces analysis; it does not own deterministic trading risk, OMS state or execution.

## Integration NFRs

| ID | Requirement | Architecture consequence |
|---|---|---|
| NFR-A01 | Loose coupling | Downstream Traders consume explicit/versioned Analysis API or AnalysisSignal contracts, not internal TradingAgents storage. |
| NFR-A02 | Independent data ownership | TradingAgents owns its MongoDB/Redis data; Trader systems never query these stores directly. |
| NFR-A03 | Independent deployment | TradingAgents can evolve/deploy independently from StockTrader/CrypTrader. |
| NFR-A04 | Time-bounded signals | Analysis includes data timestamp/validity metadata so downstream Traders can reject stale analysis. |
| NFR-A05 | Failure isolation | TradingAgents/LLM failure must not directly corrupt Trader order/portfolio state. Traders decide how to degrade when intelligence is unavailable. |
| NFR-A06 | Contract compatibility | Analysis contracts are versioned and designed for backward-compatible evolution. |

## Platform boundary

```text
Market Data / News / Fundamentals
              ↓
       TradingAgents-CN
        own DB / Redis
              ↓
       AnalysisSignal/API
        ┌─────┴─────┐
        ↓           ↓
   StockTrader   CrypTrader
    own DB        own DB
        │           │
      Alpaca      Binance
        └─────┬─────┘
              ↓
         TradeMonitor
           own DB
```

### No shared database

Every SCS owns its data. Cross-SCS integration uses APIs/events only.

### Signal contract

A target AnalysisSignal carries at least:

```text
analysisId
instrument
direction / market view
confidence / score
risk factors
dataTimestamp
validUntil
modelVersion
schemaVersion
```

Downstream Traders own freshness validation, idempotency and the final deterministic trading decision.
