from __future__ import annotations

import json
import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel

# Đọc các biến môi trường từ file .env (nếu có)
load_dotenv()

app = FastAPI(title="Lesson 16: FastAPI + Gemini API")

MODEL_NAME = "gemini-flash-lite-latest"

USERS_RAW = [
    {"user_id": 1, "name": "An", "city": " hcm "},
    {"user_id": 2, "name": "Binh", "city": "Hn"},
    {"user_id": 3, "name": "Chi", "city": "HCM"},
    {"user_id": 1, "name": "An", "city": " hcm "},
]

TX_RAW = [
    {"tx_id": "T01", "user_id": 1, "amount": 150000, "status": "SUCCESS"},
    {"tx_id": "T02", "user_id": 1, "amount": 200000, "status": "FAILED"},
    {"tx_id": "T03", "user_id": 2, "amount": 500000, "status": "SUCCESS"},
    {"tx_id": "T04", "user_id": 3, "amount": None, "status": "SUCCESS"},
    {"tx_id": "T05", "user_id": 99, "amount": 100000, "status": "SUCCESS"},
]


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    answer: str
    data_used: dict


def build_revenue_summary() -> dict:
    """Làm sạch và tổng hợp doanh thu bằng Pandas (từ Bài 14-15)."""
    df_users = pd.DataFrame(USERS_RAW).drop_duplicates().copy()
    df_users["city"] = df_users["city"].str.strip().str.upper()

    df_tx = pd.DataFrame(TX_RAW).copy()
    df_tx["amount"] = df_tx["amount"].fillna(0)
    df_tx = df_tx[df_tx["status"] == "SUCCESS"]

    df_merged = pd.merge(df_tx, df_users, on="user_id", how="inner")
    summary = (
        df_merged.groupby("city")["amount"]
        .agg(tx_count="count", total_amount="sum", avg_amount="mean")
        .sort_values("total_amount", ascending=False)
        .reset_index()
    )
    cities = summary.to_dict(orient="records")
    return {
        "total_revenue": sum(item["total_amount"] for item in cities),
        "cities": cities,
    }


def ask_gemini(system_prompt: str, user_prompt: str) -> str:
    """
    TODO 1: Gọi Gemini API bằng SDK mới `google-genai`.

    Gợi ý:
    1. Kiểm tra os.getenv("GEMINI_API_KEY"), nếu rỗng thì raise ValueError(...)
    2. client = genai.Client()  # Tự động lấy GEMINI_API_KEY từ biến môi trường
    3. response = client.models.generate_content(
           model=MODEL_NAME,
           contents=user_prompt,
           config=types.GenerateContentConfig(
               system_instruction=system_prompt,
               temperature=0.2,
           ),
       )
    4. return response.text or ""
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Chưa cấu hình GEMINI_API_KEY trong file .env")
    client = genai.Client()  # SDK tự đọc GEMINI_API_KEY từ biến môi trường
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2,
        ),
    )
    return response.text or ""


@app.post("/analytics/ask", response_model=AskResponse)
def ask_analytics(req: AskRequest) -> AskResponse:
    """
    TODO 2: Kết nối Pandas summary + Prompt + Gemini API.

    Gợi ý:
    1. summary = build_revenue_summary()
    2. Tạo system_prompt và user_prompt (nhúng json.dumps(summary, ensure_ascii=False, indent=2) + req.question)
    3. Gọi ask_gemini(system_prompt, user_prompt):
       - Bắt ValueError -> raise HTTPException(status_code=500, detail=str(e))
       - Bắt Exception -> raise HTTPException(status_code=502, detail=f"Lỗi gọi Gemini: {e}")
    4. Trả về AskResponse(question=req.question, answer=answer, data_used=summary)
    """

    summary = build_revenue_summary()
    system_prompt = (
        "Bạn là chuyên gia phân tích dữ liệu Fintech. "
        "Chỉ trả lời dựa trên số liệu JSON được cung cấp, trả lời ngắn gọn bằng tiếng Việt."
    )
    summary_json = json.dumps(summary, ensure_ascii=False, indent=2)
    user_prompt = f"Dữ liệu doanh thu:\n{summary_json}\n\nCâu hỏi: {req.question}"
    try:
        answer = ask_gemini(system_prompt, user_prompt)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Lỗi gọi Gemini: {e}")
    return AskResponse(question=req.question, answer=answer, data_used=summary)
