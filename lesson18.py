from __future__ import annotations

import json
import os
from collections.abc import AsyncIterator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Lesson 18: Streaming SSE & Async FastAPI")

MODEL_NAME = "gemini-flash-lite-latest"

SYSTEM_PROMPT = (
    "Bạn là trợ lý AI chuyên về Android và ô tô. không trả lời bất cứ gì không liên quan chủ đề trên "
    "Trả lời rõ ràng, tự nhiên bằng tiếng Việt."
)


class ChatRequest(BaseModel):
    question: str


async def stream_gemini_answer(question: str) -> AsyncIterator[str]:
    """
    TODO 1: Viết Async Generator (`async def` + `yield`) stream từng đoạn text từ Gemini theo chuẩn SSE.

    Tương đương Kotlin Flow<String> { emit(...) }:
    1. client = genai.Client()
    2. stream = await client.aio.models.generate_content_stream(
           model=MODEL_NAME,
           contents=question,
           config=types.GenerateContentConfig(
               system_instruction=SYSTEM_PROMPT,
               temperature=0.5,
           ),
       )
    3. async for chunk in stream:
           if chunk.text:
               payload = json.dumps({"text": chunk.text}, ensure_ascii=False)
               yield f"data: {payload}\n\n"
    4. Kết thúc stream: yield "data: [DONE]\n\n"
    """
    client = genai.Client()
    stream = await client.aio.models.generate_content_stream(
        model=MODEL_NAME,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.0,
        )
    )
    async for chunk in stream:
        if chunk.text:
            payload = json.dumps({"text": chunk.text}, ensure_ascii=False)
            yield f"data: {payload}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    """
    TODO 2: Trả về StreamingResponse chuẩn Server-Sent Events (`text/event-stream`).

    Gợi ý:
    1. Kiểm tra nếu chưa có os.getenv("GEMINI_API_KEY") -> raise HTTPException(500, detail=...)
    2. Trả về:
       StreamingResponse(
           stream_gemini_answer(req.question),
           media_type="text/event-stream",
       )
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="Chưa cấu hình GEMINI_API_KEY trong file .env")
    return StreamingResponse(
        stream_gemini_answer(req.question),
        media_type="text/event-stream",
    )


@app.get("/", response_class=HTMLResponse)
def demo_ui() -> str:
    """Trang test nhỏ để bạn thấy chữ chạy từng nhịp (Swagger UI thường đợi xong mới hiện)."""
    return """
    <!doctype html>
    <html lang="vi">
    <body style="font-family: sans-serif; max-width: 700px; margin: 40px auto;">
      <h2>Demo Streaming SSE (Bài 18)</h2>
      <input id="q" style="width: 75%; padding: 8px;" value="Giải thích ngắn gọn Kotlin Coroutines cho người mới học" />
      <button onclick="ask()" style="padding: 8px 16px;">Hỏi AI</button>
      <pre id="out" style="white-space: pre-wrap; background: #f4f4f4; padding: 16px; margin-top: 16px; min-height: 120px;"></pre>
      <script>
        async function ask() {
          const out = document.getElementById('out');
          out.textContent = '';
          const res = await fetch('/chat/stream', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question: document.getElementById('q').value})
          });
          const reader = res.body.getReader();
          const decoder = new TextDecoder();
          while (true) {
            const {value, done} = await reader.read();
            if (done) break;
            for (const line of decoder.decode(value).split('\\n')) {
              if (line.startsWith('data: ') && !line.includes('[DONE]')) {
                out.textContent += JSON.parse(line.slice(6)).text;
              }
            }
          }
        }
      </script>
    </body>
    </html>
    """
