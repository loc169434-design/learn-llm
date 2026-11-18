from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from backend.app.schemas.drive import (
    ComposeReplyRequest,
    ComposeReplyResponse,
    IncomingNotificationBatch,
    TriageDecision,
)
from backend.app.services.gemini_service import DriveAiService, get_drive_ai_service

router = APIRouter(prefix="/api/v1/drive", tags=["DriveSafe AI"])


def _provide_service() -> DriveAiService:
    try:
        return get_drive_ai_service()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/triage", response_model=TriageDecision)
def triage_notifications(
    batch: IncomingNotificationBatch,
    service: DriveAiService = Depends(_provide_service),
) -> TriageDecision:
    try:
        return service.triage_notifications(batch)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Lỗi xử lý AI Triage: {exc}") from exc


@router.post("/compose-reply", response_model=ComposeReplyResponse)
def compose_reply(
    req: ComposeReplyRequest,
    service: DriveAiService = Depends(_provide_service),
) -> ComposeReplyResponse:
    try:
        return service.compose_reply(req)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Lỗi xử lý AI Compose Reply: {exc}") from exc
