from __future__ import annotations

import os
from typing import Literal, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Lesson 17: Structured Output - Android Car AI Co-Pilot")

MODEL_NAME = "gemini-flash-lite-latest"


class CarAction(BaseModel):
    action_type: Literal["NAVIGATE", "PLAY_MUSIC", "SEND_MESSAGE", "CAR_SETTING", "UNKNOWN"]
    app: Optional[str] = Field(
        default=None,
        description="Tên app thực thi trên Android nếu có (vietmap, google_maps, youtube_music, zalo...)",
    )
    target: str = Field(description="Đối tượng chính: địa điểm, tên bài hát, người nhận, hoặc tên cài đặt")
    detail: Optional[str] = Field(
        default=None,
        description="Thông tin bổ sung: nội dung tin nhắn hoặc giá trị cài đặt (VD: '80%', 'ON')",
    )


class CarCommandPlan(BaseModel):
    reply_speech: str = Field(description="Câu phản hồi ngắn gọn, tự nhiên bằng tiếng Việt để Android TTS đọc lại")
    actions: list[CarAction]


class VoiceRequest(BaseModel):
    voice_text: str


SYSTEM_PROMPT = """
Bạn là AI Co-Pilot điều khiển tự động hóa trên màn hình Android ô tô ở Việt Nam.
Nhiệm vụ: phân tích câu nói tự nhiên của tài xế thành danh sách các hành động tuần tự.
Quy tắc:
- Một câu nói có thể chứa nhiều hành động (tách thành từng phần tử trong `actions` theo đúng thứ tự).
- Nếu tài xế không nói rõ tên app: chỉ đường mặc định `vietmap`, nghe nhạc mặc định `youtube_music`, nhắn tin mặc định `zalo`.
- Nếu câu nói không phải lệnh điều khiển xe/điện thoại, trả về 1 action có `action_type="UNKNOWN"`.
- `reply_speech` phải cực kỳ ngắn gọn (dưới 20 từ) để đọc bằng loa xe khi đang lái.
"""


def parse_car_command(voice_text: str) -> CarCommandPlan:
    """
    TODO 1: Dùng Structured Output của Gemini để ép trả về đúng schema `CarCommandPlan`.

    Gợi ý:
    1. Kiểm tra os.getenv("GEMINI_API_KEY"), nếu thiếu -> raise ValueError(...)
    2. client = genai.Client()
    3. response = client.models.generate_content(
           model=MODEL_NAME,
           contents=voice_text,
           config=types.GenerateContentConfig(
               system_instruction=SYSTEM_PROMPT,
               response_mime_type="application/json",
               response_schema=CarCommandPlan,
               temperature=0.0,
           ),
       )
    4. Nếu response.parsed là CarCommandPlan thì return response.parsed,
       ngược lại return CarCommandPlan.model_validate_json(response.text)
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Chưa cấu hình GEMINI_API_KEY trong file .env")
    client = genai.Client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=voice_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=CarCommandPlan,
            temperature=0.0,
        )
    )
    if isinstance(response.parsed, CarCommandPlan):
        return response.parsed
    return CarCommandPlan.model_validate_json(response.text or "{}")


@app.post("/car/command", response_model=CarCommandPlan)
def handle_car_voice_command(req: VoiceRequest) -> CarCommandPlan:
    """
    TODO 2: Nhận voice_text từ App Android, gọi parse_car_command(), bắt lỗi 500/502 và trả về CarCommandPlan.
    """
    try:
        return parse_car_command(req.voice_text)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Lỗi gọi Gemini: {e}")
