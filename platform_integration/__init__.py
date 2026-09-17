"""Stable integration boundary between TradingAgents and downstream Trader SCSs.

Keep package import lightweight: importing contracts/mappers must not initialize the
FastAPI router or the full application dependency graph.
"""

__all__ = []
