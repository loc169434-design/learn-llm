from __future__ import annotations

import json
from typing import Protocol

from google import genai
from google.genai import types

from backend.app.core.config import Settings, get_settings
from backend.app.schemas.drive import (
    ComposeReplyRequest,
    ComposeReplyResponse,
    IncomingNotificationBatch,
    TriageDecision,
)

TRIAGE_SYSTEM_PROMPT = """
Bạn là trợ lý AI lọc và đọc tin nhắn an toàn cho tài xế đang lái ô tô tại Việt Nam.
Quy tắc:
1. Nếu tin nhắn là quảng cáo, khuyến mãi (Zalo OA, Shopee, ngân hàng quảng cáo), mã OTP, hoặc thông báo hệ thống không cần phản hồi:
   - Đặt `priority = "IGNORE_SPAM"`, `should_read_aloud = false`, `summary_tts = null`, `can_quick_reply = false`.
2. Nếu là tin nhắn của người thật (gia đình, đồng nghiệp, bạn bè, khách hàng, tài xế giao hàng):
   - Đặt `should_read_aloud = true`, `priority = "IMPORTANT"` (nếu gấp/hỏi han trực tiếp) hoặc `"NORMAL"`.
   - Gom tất cả các tin nhắn rời rạc trong danh sách thành ĐÚNG 1 câu tiếng Việt tự nhiên, ngắn gọn (dưới 30 từ) trong `summary_tts` để đọc qua loa xe (ví dụ: "Vợ nhắn trên Zalo hỏi anh đang ở đâu và dặn về nhớ mua sữa ít đường cho con.").
   - Đặt `can_quick_reply = true` nếu người gửi đang chờ câu trả lời.
"""

COMPOSE_REPLY_SYSTEM_PROMPT = """
Bạn là trợ lý soạn tin nhắn trả lời rảnh tay khi tài xế đang lái ô tô.
Nhiệm vụ:
1. Chuyển lời nói thô của tài xế (`raw_voice_transcript`) thành câu trả lời hoàn chỉnh trong `polished_reply`:
   - Bỏ các từ thừa mở đầu như "nhắn lại là", "trả lời là", "bảo với cổ là"...
   - Giữ đúng xưng hô thân mật/lịch sự phù hợp với ngữ cảnh tin nhắn đến và tên người gửi.
   - Sửa lỗi chính tả/viết hoa chuẩn tiếng Việt, ngắn gọn, tự nhiên như người thật gõ.
2. Tạo `confirm_tts` ngắn gọn dưới 20 từ để báo cho tài xế biết đã gửi (VD: "Đã gửi tin nhắn trả lời cho Vợ.").
"""


class DriveAiService(Protocol):
    def triage_notifications(self, batch: IncomingNotificationBatch) -> TriageDecision: ...

    def compose_reply(self, req: ComposeReplyRequest) -> ComposeReplyResponse: ...


class GeminiDriveAiService:
    def __init__(self, settings: Settings) -> None:
        if not settings.gemini_api_key:
            raise ValueError("Chưa cấu hình GEMINI_API_KEY trong môi trường hoặc file .env")
        self._model = settings.gemini_model
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def triage_notifications(self, batch: IncomingNotificationBatch) -> TriageDecision:
        payload = json.dumps(batch.model_dump(), ensure_ascii=False, indent=2)
        response = self._client.models.generate_content(
            model=self._model,
            contents=f"Thông báo mới nhận được:\n{payload}",
            config=types.GenerateContentConfig(
                system_instruction=TRIAGE_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=TriageDecision,
                temperature=0.0,
            ),
        )
        if isinstance(response.parsed, TriageDecision):
            return response.parsed
        return TriageDecision.model_validate_json(response.text or "{}")

    def compose_reply(self, req: ComposeReplyRequest) -> ComposeReplyResponse:
        payload = json.dumps(req.model_dump(), ensure_ascii=False, indent=2)
        response = self._client.models.generate_content(
            model=self._model,
            contents=f"Ngữ cảnh và lời nói của tài xế:\n{payload}",
            config=types.GenerateContentConfig(
                system_instruction=COMPOSE_REPLY_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ComposeReplyResponse,
                temperature=0.1,
            ),
        )
        if isinstance(response.parsed, ComposeReplyResponse):
            return response.parsed
        return ComposeReplyResponse.model_validate_json(response.text or "{}")


def get_drive_ai_service() -> DriveAiService:
    return GeminiDriveAiService(settings=get_settings())
