# NHẬT KÝ HỌC TẬP & LỘ TRÌNH CHUYỂN HƯỚNG MOBILE + AI

## 1. Mục tiêu cá nhân
- **Hồ sơ:** Mobile Developer (Android / Kotlin) kinh nghiệm 3-5 năm, nghiệp vụ Fintech / Ngân hàng.
- **Mục tiêu:** Chuyển hướng sang Mobile + AI Engineer / Backend AI (Target lương: 28 - 33 triệu).
- **Chiến lược:** Vừa học vừa xây dựng project thực chiến (Backend AI + App Android Automation ô tô `DriveSafeAI`), có test tự động, sổ tay phỏng vấn và sync qua Git để học liền mạch giữa máy công ty và máy ở nhà.

---

## 2. Tiến độ hiện tại (Cập nhật: 20/11/2026)

### ✅ Đã hoàn thành
- **Bài 1 – 12:** Python cơ bản, JSON, Pydantic, HTTP Client, FastAPI CRUD + `pytest` (`main.py`, `test_main.py` — 8/8 pass).
- **Bài 13 – 14:** Pandas phân tích, làm sạch dữ liệu, `pd.merge` và `groupby().agg()` (`lesson13.py`, `lesson14.py`).
- **Bài 15:** Nối Pandas vào FastAPI & đóng gói JSON Prompt (`lesson15.py`).
- **Bài 16:** Gọi Google Gemini API (`google-genai`, `gemini-flash-lite-latest`) + bảo mật `.env` (`lesson16.py`).
- **Bài 17:** Structured Output (`response_schema` + Pydantic `CarCommandPlan`) cho Android Car Co-Pilot (`lesson17.py`).
- **Bài 18:** Streaming Server-Sent Events (`text/event-stream`) & `AsyncIterator` + `yield` (`lesson18.py`).
- **Bài 19:** Function Calling / Tool Use (`client.chats.create` + Pandas tools `add_car_expense`, `get_expense_summary`) (`lesson19.py`).
- **Bài 20:** Embeddings (`gemini-embedding-001`, 3072 chiều) & Semantic Search bằng Cosine Similarity (`lesson20.py`).
- **Dự án thực chiến `DriveSafeAI` (`~/AndroidStudioProjects/DriveSafeAI` + `backend/`):**
  - **Module 1 (Backend AI):** Hoàn thiện `backend/` (`triage` & `compose-reply`) + `pytest` mock Gemini (5/5 pass).
  - **Module 2 (Android Notification Collector):** `CarNotificationListenerService` + `NotificationBatchDebouncer` (4s, `Mutex`, test bằng VirtualTime) + MVI Dashboard.
  - **Module 3 (Silent Reply & Audio Ducking):** `CarSpeechSpeaker` (`AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK`), `CarVoiceRecognizer` (`vi-VN`), `SilentReplySender` (`RemoteInput` + `PendingIntent` IPC).
  - Tài liệu phỏng vấn chi tiết: [docs/INTERVIEW_PLAYBOOK.md](docs/INTERVIEW_PLAYBOOK.md).

---

### ⏳ Đang làm (Bài 21: Chunking & Full RAG Pipeline)
- **File đang mở:** `lesson21.py` (khung sẵn 3 `# TODO`):
  1. `chunk_text(text, chunk_size=260, overlap=50)`: Cắt văn bản sổ tay xe có phần gối đầu.
  2. `retrieve_relevant_chunks(...)`: Tìm top-k đoạn liên quan nhất và lọc ngưỡng `min_score = 0.55` chống bịa đặt.
  3. `ask_rag(...)`: Ghép context `[Đoạn #...]` và gọi Gemini trả lời kèm trích dẫn nguồn.
- **Kế tiếp sau Bài 21:**
  - **Bài 22–23:** Vector DB + Đánh giá & Guardrails cho RAG.
  - **Bài 24–25 / Module 4–5:** Dockerize Backend + nối Retrofit từ App `DriveSafeAI` vào Backend thật + `BluetoothCarReceiver` tự động bật khi lên xe.

---

## 3. Bản đồ đối chiếu kiến thức (Android Kotlin vs Python AI)

| Android (Kotlin) | FastAPI / Python AI | Ghi chú |
| :--- | :--- | :--- |
| `data class User(...)` | `class User(BaseModel):` (Pydantic) | Validate & ép JSON Schema cho Structured Output |
| `suspend fun` + `Flow<String>` + `emit` | `async def` + `AsyncIterator` + `yield` | Stream SSE từng chunk theo thời gian thực |
| `users.filter { ... }` / `groupBy` | `df[df["age"] > 25]` / `df.groupby(...)` | Xử lý & tổng hợp dữ liệu bằng Pandas |
| `MockWebServer` / Fake Repo | `app.dependency_overrides` + Mock | Test API LLM nhanh không tốn tiền quota |
| `NotificationListenerService` | `CarNotificationListenerService` | System-bound service bắt thông báo Zalo/SMS |
| `RemoteInput` + `PendingIntent` | `SilentReplySender` | Trả lời ngầm qua Binder IPC không che bản đồ |

---

## 4. Cách bật lại ở máy tính khác (Về nhà mở Antigravity)
1. Chạy `git pull` (hoặc `git clone`) repo `learn-llm`, chạy `uv sync` và copy `.env` chứa `GEMINI_API_KEY`.
2. Mở thư mục `learn-llm` bằng **Antigravity** (Workspace Skill `.agents/skills/daily-study-tutor/SKILL.md` tự động được nhận diện).
3. Chỉ cần nhắn **"ôn bài"** hoặc **"học tiếp"** — Antigravity sẽ tự đọc file này và bật widget bài tập tương tác + hướng dẫn tiếp từ `lesson21.py`!
