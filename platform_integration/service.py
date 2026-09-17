from typing import Any, Dict, Optional

from app.core.database import get_mongo_db

from .contracts import AnalysisJobStatus, AnalysisStatusResponse
from .mapper import to_analysis_signal


_STATUS_MAP = {
    "pending": AnalysisJobStatus.PENDING,
    "queued": AnalysisJobStatus.PENDING,
    "processing": AnalysisJobStatus.PROCESSING,
    "running": AnalysisJobStatus.PROCESSING,
    "completed": AnalysisJobStatus.COMPLETED,
    "failed": AnalysisJobStatus.FAILED,
    "cancelled": AnalysisJobStatus.CANCELLED,
}


class PlatformIntegrationService:
    """Anti-corruption layer over TradingAgents' internal persistence model."""

    async def find_task(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        db = get_mongo_db()
        return await db.analysis_tasks.find_one({"task_id": analysis_id})

    async def status(self, analysis_id: str) -> Optional[AnalysisStatusResponse]:
        task = await self.find_task(analysis_id)
        if not task:
            return None
        raw_status = str(task.get("status", "pending")).lower()
        return AnalysisStatusResponse(
            analysisId=analysis_id,
            status=_STATUS_MAP.get(raw_status, AnalysisJobStatus.PROCESSING),
            progress=int(task.get("progress", 0) or 0),
            instrument=task.get("symbol") or task.get("stock_code"),
            createdAt=task.get("created_at"),
            completedAt=task.get("completed_at"),
            error=task.get("last_error"),
            schemaVersion=1,
        )

    async def result(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        db = get_mongo_db()
        report = await db.analysis_reports.find_one({"task_id": analysis_id})
        if report:
            return report

        task = await self.find_task(analysis_id)
        if not task:
            return None

        internal_analysis_id = (task.get("result") or {}).get("analysis_id")
        if internal_analysis_id:
            report = await db.analysis_reports.find_one({"analysis_id": internal_analysis_id})
            if report:
                return report

        result = task.get("result")
        if result:
            merged = dict(result)
            merged.setdefault("stock_symbol", task.get("symbol") or task.get("stock_code"))
            merged.setdefault("created_at", task.get("created_at"))
            merged.setdefault("updated_at", task.get("completed_at"))
            return merged
        return None

    async def signal(self, analysis_id: str):
        result = await self.result(analysis_id)
        if result is None:
            return None
        return to_analysis_signal(analysis_id, result)


platform_integration_service = PlatformIntegrationService()
