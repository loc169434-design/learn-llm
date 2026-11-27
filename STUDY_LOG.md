# NHẬT KÝ HỌC TẬP & LỘ TRÌNH CHUYỂN HƯỚNG MOBILE + AI

## 1. Mục tiêu cá nhân
- **Hồ sơ:** Mobile Developer (Android / Kotlin) kinh nghiệm 3-5 năm, nghiệp vụ Fintech / Ngân hàng.
- **Mục tiêu:** Chuyển hướng sang Mobile + AI Engineer / Backend AI (Target lương: 28 - 33 triệu).
- **Chiến lược:** Vừa học vừa xây dựng project thực chiến (Backend AI + App Android Automation ô tô `DriveSafeAI`), có test tự động, sổ tay phỏng vấn và sync qua Git để học liền mạch giữa máy công ty và máy ở nhà.

---

## 2. Tiến độ hiện tại (Cập nhật: 27/11/2026)

### ✅ Đã hoàn thành
- **Bài 1 – 12:** Python cơ bản, JSON, Pydantic, HTTP Client, FastAPI CRUD + `pytest` (`main.py`, `test_main.py` — 8/8 pass).
- **Bài 13 – 14:** Pandas phân tích, làm sạch dữ liệu, `pd.merge` và `groupby().agg()` (`lesson13.py`, `lesson14.py`).
- **Bài 15:** Nối Pandas vào FastAPI & đóng gói JSON Prompt (`lesson15.py`).
- **Bài 16:** Gọi Google Gemini API (`google-genai`, `gemini-flash-lite-latest`) + bảo mật `.env` (`lesson16.py`).
- **Bài 17:** Structured Output (`response_schema` + Pydantic `CarCommandPlan`) cho Android Car Co-Pilot (`lesson17.py`).
- **Bài 18:** Streaming Server-Sent Events (`text/event-stream`) & `AsyncIterator` + `yield` (`lesson18.py`).
- **Bài 19:** Function Calling / Tool Use (`client.chats.create` + Pandas tools `add_car_expense`, `get_expense_summary`) (`lesson19.py`).
- **Bài 20:** Embeddings (`gemini-embedding-001`, 3072 chiều) & Semantic Search bằng Cosine Similarity (`lesson20.py`).
- **Bài 21:** Chunking có gối đầu (`overlap`) & Full RAG Pipeline (`lesson21.py` — lọc ngưỡng `min_score=0.55`, trích dẫn `[Đoạn #...]`, chặn đứng câu hỏi ngoài lề `NGUỒN: []`).
- **Bài 22:** Local Vector Store (`.json` + `.npy` nhị phân, nạp lại `0 API calls`) & RAG Evaluation tự động (`lesson22.py` — đạt `4/5 (80%)`, phát hiện thực nghiệm ngưỡng `min_score=0.55` để lọt câu *"Giá Bitcoin"* qua tầng Retrieval nhưng bị lớp Guardrail thứ 2 ở Gemini Prompt chặn lại thành công!).
- **Dự án thực chiến `DriveSafeAI` (`~/AndroidStudioProjects/DriveSafeAI` + `backend/`):**
  - **Module 1 (Backend AI):** Hoàn thiện `backend/` (`triage` & `compose-reply`) + `pytest` mock Gemini (5/5 pass).
  - **Module 2 (Android Notification Collector):** `CarNotificationListenerService` + `NotificationBatchDebouncer` (4s, `Mutex`, test bằng VirtualTime) + MVI Dashboard.
  - **Module 3 (Silent Reply & Audio Ducking):** `CarSpeechSpeaker` (`AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK`), `CarVoiceRecognizer` (`vi-VN`), `SilentReplySender` (`RemoteInput` + `PendingIntent` IPC).
  - Tài liệu phỏng vấn chi tiết: [docs/INTERVIEW_PLAYBOOK.md](docs/INTERVIEW_PLAYBOOK.md).

---

### ⏳ Đang làm (Cập nhật: 27/11/2026)
1. **Phòng thí nghiệm Tự Train AI & Nghiên cứu trình TS. Bùi Thanh Hùng (`ai_research_lab/` + `research_thay_hung/`):**
   - Đã tổng hợp toàn bộ công trình nghiên cứu của thầy trong [research_thay_hung/README.md](research_thay_hung/README.md).
   - **Lộ trình 14 ngày hiểu bản chất lý thuyết & tự train model:** Theo dõi tại [ai_research_lab/PROGRESS_TRACKER.md](ai_research_lab/PROGRESS_TRACKER.md).
   - **✅ Đã hoàn thành Ngày 01 (`day01_tfidf_and_vn_text`):** Pass 100% `lab01_tfidf_from_scratch.py` (ma trận TF-IDF `48 x 484`, Twin Search câu không dấu khớp Top-3 `[URGENT]`, Top-1 `score=0.709`).
   - **✅ Đã hoàn thành Ngày 02 (`day02_ml_classifiers_and_metrics`):** Pass 100% `lab02_ml_classifiers.py` — **Linear SVM vô địch** (`Test Acc=83.3%`, `Macro-F1=0.831`, `URGENT Recall=100%`), Logistic Regression (`Macro-F1=0.757`), Random Forest Overfitting (`Train 100% / Test 33.3%`).
   - **⏳ Đang làm bài tập Ngày 03 (`day03_loss_and_gradient_descent`):** Đã xong toàn bộ Lý thuyết Tiết 1 (*Cross-Entropy Loss*) + Tiết 2 (*Gradient Descent*, *Learning Rate*, *3 bước 1 Epoch*, *Softmax Numerical Stability*) & 2 bài Trắc nghiệm. Đang code dở 3 `# TODO` trong `lab03_gradient_descent_from_scratch.py` (đã giải thích chi tiết `axis=1, keepdims=True` cho `TODO 1`, kế tiếp hoàn thiện `TODO 1 -> TODO 3`).
2. **Kế tiếp lộ trình GenAI & `DriveSafeAI`:**
   - **Bài 23–25 / Module 4:** Tinh chỉnh ngưỡng `min_score` RAG đạt `5/5`, nối Retrofit từ App `DriveSafeAI` vào Backend thật + `BluetoothCarReceiver` + Dockerize Backend.

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
3. Chỉ cần nhắn **"ôn bài"** hoặc **"học tiếp"** — Antigravity sẽ tự đọc file này và bật widget bài tập tương tác + hướng dẫn tiếp đúng điểm đang dừng gần nhất!
