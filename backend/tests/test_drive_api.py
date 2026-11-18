from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.api.drive_routes import _provide_service
from backend.app.main import app
from backend.app.schemas.drive import (
    ComposeReplyRequest,
    ComposeReplyResponse,
    IncomingNotificationBatch,
    TriageDecision,
)


class MockDriveAiService:
    """Mock service dùng trong Unit Test để test nhanh 0.01s, không tốn tiền/quota Gemini API."""

    def triage_notifications(self, batch: IncomingNotificationBatch) -> TriageDecision:
        if "khuyến mãi" in " ".join(batch.messages).lower():
            return TriageDecision(
                priority="IGNORE_SPAM",
                should_read_aloud=False,
                summary_tts=None,
                can_quick_reply=False,
            )
        return TriageDecision(
            priority="IMPORTANT",
            should_read_aloud=True,
            summary_tts=f"{batch.sender_name} vừa nhắn {len(batch.messages)} tin trên Zalo.",
            can_quick_reply=True,
        )

    def compose_reply(self, req: ComposeReplyRequest) -> ComposeReplyResponse:
        return ComposeReplyResponse(
            polished_reply="Anh đang lái xe, khoảng 15 phút nữa anh về tới nha.",
            confirm_tts=f"Đã gửi tin nhắn trả lời cho {req.sender_name}.",
        )


def setup_function() -> None:
    app.dependency_overrides[_provide_service] = lambda: MockDriveAiService()


def teardown_function() -> None:
    app.dependency_overrides.clear()


client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_triage_important_zalo_batch_returns_summary() -> None:
    payload = {
        "app_package": "com.zing.zalo",
        "sender_name": "Vợ",
        "messages": ["Anh ơi", "Về nhớ ghé mua sữa nha"],
    }
    response = client.post("/api/v1/drive/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "IMPORTANT"
    assert data["should_read_aloud"] is True
    assert "Vợ" in data["summary_tts"]
    assert data["can_quick_reply"] is True


def test_triage_spam_notification_is_ignored() -> None:
    payload = {
        "app_package": "com.zing.zalo",
        "sender_name": "ZaloPay",
        "messages": ["Khuyến mãi hoàn tiền 50% hôm nay!"],
    }
    response = client.post("/api/v1/drive/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "IGNORE_SPAM"
    assert data["should_read_aloud"] is False
    assert data["summary_tts"] is None


def test_triage_empty_messages_returns_422_validation_error() -> None:
    payload = {
        "app_package": "com.zing.zalo",
        "sender_name": "Vợ",
        "messages": [],
    }
    response = client.post("/api/v1/drive/triage", json=payload)
    assert response.status_code == 422


def test_compose_reply_polishes_driver_voice_transcript() -> None:
    payload = {
        "sender_name": "Vợ",
        "incoming_messages": ["Mấy giờ anh về?"],
        "raw_voice_transcript": "nhắn lại là anh đang lái xe 15p nữa về",
    }
    response = client.post("/api/v1/drive/compose-reply", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "15 phút" in data["polished_reply"]
    assert "Vợ" in data["confirm_tts"]
