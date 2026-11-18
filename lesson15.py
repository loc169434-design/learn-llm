from __future__ import annotations

import json
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from lesson14 import df_merged

app = FastAPI(title="Fintech Analytics + LLM Prompt Prep")

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


class CityRevenue(BaseModel):
    city: str
    tx_count: int
    total_amount: float
    avg_amount: float


class AnalyticsReport(BaseModel):
    total_revenue: float
    cities: list[CityRevenue]


class AskRequest(BaseModel):
    question: str


class PromptPreviewResponse(BaseModel):
    system_prompt: str
    user_prompt: str
    report: AnalyticsReport


def build_city_report() -> AnalyticsReport:
    """
    TODO 1: Dùng Pandas làm sạch & tổng hợp dữ liệu (giống Bài 14),
    sau đó chuyển thành AnalyticsReport (Pydantic model) để FastAPI trả JSON.

    Gợi ý các bước:
    1. Làm sạch df_users (drop_duplicates + strip().upper())
    2. Làm sạch df_tx (fillna(0) + lọc status == "SUCCESS")
    3. pd.merge(..., on="user_id", how="inner")
    4. groupby("city")["amount"].agg(tx_count="count", total_amount="sum", avg_amount="mean")
       -> .sort_values("total_amount", ascending=False).reset_index()
    5. Chuyển từng dòng thành CityRevenue(**row) và tính total_revenue = sum(...)
    """

    summary = (
        df_merged.groupby("city")["amount"]
        .agg(tx_count="count", total_amount="sum", avg_amount="mean")
        .sort_values("total_amount", ascending=False)
        .reset_index()
    )
    cities = [CityRevenue(**row) for row in summary.to_dict("records")]
    total_revenue = sum(c.total_amount for c in cities)
    return AnalyticsReport(total_revenue=total_revenue, cities=cities)
    raise NotImplementedError("Hãy hoàn thiện TODO 1")


@app.get("/analytics/revenue", response_model=AnalyticsReport)
def get_revenue_report() -> AnalyticsReport:
    """
    TODO 2: Gọi build_city_report() và trả về kết quả.
    """
    try:
        return build_city_report()
    except NotImplementedError:
        print("Hãy hoàn thiện TODO 2")
        raise NotImplementedError()


@app.post("/analytics/build-prompt", response_model=PromptPreviewResponse)
def build_llm_prompt(req: AskRequest) -> PromptPreviewResponse:
    """
    TODO 3: Chuẩn bị Prompt chuẩn để gửi cho LLM (chống LLM tự bịa số liệu).
    - Gọi build_city_report() để lấy số liệu thật
    - Tạo system_prompt: dặn LLM đóng vai chuyên gia Fintech, chỉ dùng số liệu được cung cấp
    - Tạo user_prompt: nhúng report.model_dump() (dạng JSON string) + req.question
    - Trả về PromptPreviewResponse(...)
    """
    report = build_city_report()
    system_prompt = (
        "Bạn là chuyên gia phân tích dữ liệu Fintech. "
        "Chỉ được trả lời dựa trên số liệu JSON được cung cấp, không tự bịa thêm số."
    )
    report_json = json.dumps(report.model_dump(),ensure_ascii=False, indent=2)
    user_prompt = f"Dữ liệu doanh thu:\n{report_json}\n\nCâu hỏi: {req.question}"
    return PromptPreviewResponse(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        report=report,
    )
