from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class IncomingNotificationBatch(BaseModel):
    app_package: str = Field(
        description="Package name của ứng dụng gửi thông báo, VD: com.zing.zalo, com.facebook.orca",
        examples=["com.zing.zalo"],
    )
    sender_name: str = Field(
        min_length=1,
        description="Tên người gửi hoặc tên nhóm/Official Account trên thông báo",
        examples=["Vợ"],
    )
    messages: list[str] = Field(
        min_length=1,
        description="Danh sách các tin nhắn gom được trong cửa sổ debounce (VD 4 giây)",
        examples=[["Anh ơi", "Đang ở đâu thế", "Về ghé mua sữa ít đường cho con nha"]],
    )


class TriageDecision(BaseModel):
    priority: Literal["IMPORTANT", "NORMAL", "IGNORE_SPAM"] = Field(
        description="Mức độ ưu tiên: IGNORE_SPAM cho quảng cáo/khuyến mãi/OTP/hệ thống"
    )
    should_read_aloud: bool = Field(
        description="True nếu cần đọc lên loa xe cho tài xế nghe, False nếu là quảng cáo/rác"
    )
    summary_tts: Optional[str] = Field(
        default=None,
        description="Câu tóm tắt tự nhiên bằng tiếng Việt (tối đa 30 từ) để đọc qua TTS khi đang lái xe",
    )
    can_quick_reply: bool = Field(
        description="True nếu tin nhắn mang tính hội thoại/câu hỏi cần hỏi tài xế có muốn trả lời không"
    )


class ComposeReplyRequest(BaseModel):
    sender_name: str = Field(min_length=1, examples=["Vợ"])
    incoming_messages: list[str] = Field(min_length=1)
    raw_voice_transcript: str = Field(
        min_length=1,
        description="Văn bản thô thu từ SpeechRecognizer trên xe (có thể lủng củng, thiếu dấu chấm phẩy)",
        examples=["nhắn lại là anh đang chạy ngoài nguyễn văn linh tầm 15 phút nữa về nhớ mua sữa rồi"],
    )


class ComposeReplyResponse(BaseModel):
    polished_reply: str = Field(
        description="Nội dung tin nhắn hoàn chỉnh, lịch sự, tự nhiên để gửi thẳng vào Zalo/Messenger"
    )
    confirm_tts: str = Field(
        description="Câu thông báo ngắn gọn để đọc xác nhận qua loa xe sau khi gửi"
    )
