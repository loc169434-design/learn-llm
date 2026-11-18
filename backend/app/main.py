from __future__ import annotations

from fastapi import FastAPI

from backend.app.api.drive_routes import router as drive_router

app = FastAPI(
    title="DriveSafe AI Backend",
    version="0.1.0",
    description="Backend AI phân loại, tóm tắt thông báo Zalo/Messenger và chuẩn hóa câu trả lời giọng nói khi lái xe.",
)

app.include_router(drive_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
