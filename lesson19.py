import os
from datetime import date

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Lesson 19: Function Calling / Tool Use (AI Agent)")

MODEL_NAME = "gemini-flash-lite-latest"

# Giả lập database lưu chi phí xe ô tô (làm thật sẽ lưu SQLite/PostgreSQL)
EXPENSES_DB: list[dict] = [
    {"date": "2026-11-02", "category": "xang", "amount_vnd": 850000, "note": "Đổ đầy bình A95 Petrolimex"},
    {"date": "2026-11-10", "category": "phi_duong", "amount_vnd": 140000, "note": "Phí cao tốc Long Thành"},
    {"date": "2026-11-12", "category": "bao_duong", "amount_vnd": 1200000, "note": "Thay nhớt mốc 20.000 km"},
    {"date": "2026-11-15", "category": "xang", "amount_vnd": 700000, "note": "Đổ xăng ở Quận 7"},
]


# --- 2 HÀM PYTHON (TOOLS) ĐỂ GEMINI TỰ GỌI KHI CẦN ---
# Lưu ý: Gemini đọc tên hàm, type hints và docstring để biết cách truyền tham số!
def add_car_expense(category: str, amount_vnd: int, note: str) -> dict:
    """
    Ghi nhận một khoản chi phí xe hơi mới vào cơ sở dữ liệu.

    Args:
        category: Loại chi phí, chỉ chọn 1 trong 3 giá trị: 'xang', 'bao_duong', hoặc 'phi_duong'.
        amount_vnd: Số tiền chi tính bằng VNĐ (ví dụ 500000 cho 500 ngàn).
        note: Ghi chú ngắn về khoản chi (ví dụ: 'Đổ xăng ở Nguyễn Văn Linh').
    """
    record = {
        "date": date.today().isoformat(),
        "category": category,
        "amount_vnd": amount_vnd,
        "note": note,
    }
    EXPENSES_DB.append(record)
    return {"status": "saved", "record": record}


def get_expense_summary(category: str = "ALL") -> dict:
    """
    Thống kê tổng tiền và số lần chi tiêu cho xe hơi bằng Pandas.

    Args:
        category: Loại chi phí cần lọc ('xang', 'bao_duong', 'phi_duong'),
                  hoặc 'ALL' để thống kê toàn bộ các loại.
    """
    df = pd.DataFrame(EXPENSES_DB)
    if df.empty:
        return {"category": category, "count": 0, "total_vnd": 0}

    if category != "ALL":
        df = df[df["category"] == category]

    return {
        "category": category,
        "count": int(len(df)),
        "total_vnd": int(df["amount_vnd"].sum()) if not df.empty else 0,
        "items": df.to_dict(orient="records"),
    }


SYSTEM_PROMPT = """
Bạn là AI Agent quản lý chi phí xe hơi cho tài xế.
- Khi tài xế báo mới chi tiền (đổ xăng, thay nhớt, phí cầu đường...), hãy gọi tool `add_car_expense`.
- Khi tài xế hỏi tổng tiền hoặc lịch sử chi tiêu, hãy gọi tool `get_expense_summary`.
- Luôn trả lời ngắn gọn bằng tiếng Việt dựa trên kết quả tool trả về, không tự tính nhẩm sai.
"""


class AgentRequest(BaseModel):
    question: str


class AgentResponse(BaseModel):
    question: str
    answer: str
    total_records: int


def ask_car_agent(question: str) -> str:
    """
    TODO 1: Dùng `client.chats.create` với `tools=[add_car_expense, get_expense_summary]`
    để Gemini tự động chọn và gọi hàm Python khi cần.

    Gợi ý:
    1. Kiểm tra os.getenv("GEMINI_API_KEY"), thiếu -> raise ValueError(...)
    2. client = genai.Client()
    3. chat = client.chats.create(
           model=MODEL_NAME,
           config=types.GenerateContentConfig(
               system_instruction=SYSTEM_PROMPT,
               tools=[add_car_expense, get_expense_summary],
               temperature=0.0,
           ),
       )
    4. response = chat.send_message(question)
    5. return response.text or ""
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise NotImplementedError("Chưa cấu hình GEMINI_API_KEY trong file .env")
    client = genai.Client()
    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[add_car_expense, get_expense_summary],
            temperature=0.0,
        )
    )
    response = chat.send_message(question)
    return response.text or ""


@app.post("/agent/ask", response_model=AgentResponse)
def agent_ask(req: AgentRequest) -> AgentResponse:
    """
    TODO 2: Gọi ask_car_agent(req.question), bắt lỗi 500/502 và trả về AgentResponse.
    """
    try:
        answer = ask_car_agent(req.question)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=500, detail=f"Lỗi gọi gemini ")
    return AgentResponse(question=req.question, answer=answer, total_records=len(EXPENSES_DB), )
