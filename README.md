# Learn LLM & Python Backend for Mobile Developers

Repository lưu trữ lộ trình học tập và thực hành chuyển hướng từ **Mobile Developer (Android / Kotlin)** sang **Mobile + AI & Backend Engineer**.

## 📁 Cấu trúc dự án
- `main.py`: REST API xây dựng bằng FastAPI (CRUD User, lọc query param, tính stats, validate lỗi 422/404).
- `test_main.py`: Bộ kiểm thử tự động toàn diện sử dụng `TestClient` và `pytest` (8/8 test cases pass).
- `lesson13.py`: Thực hành xử lý và phân tích dữ liệu với `pandas` (DataFrame, Series, lọc điều kiện, đếm `value_counts`, gom nhóm `groupby`, xuất CSV, xử lý `NaN`).
- `lesson14.py`: Làm sạch dữ liệu & ghép bảng (`drop_duplicates`, chuẩn hóa chuỗi, `pd.merge`, `groupby().agg()`).
- `lesson15.py`: Kết nối dữ liệu Pandas vào FastAPI và xây dựng Prompt chuẩn bị gọi LLM.
- `lesson16.py`: Gọi Google Gemini API (`google-genai`) từ FastAPI và đọc cấu hình qua `.env`.
- `STUDY_LOG.md`: Nhật ký học tập chi tiết, bản đồ đối chiếu kiến thức giữa Kotlin/Android và Python/FastAPI/AI.
- `users.json`, `users_cli.py`, `test_users.py`: CLI xử lý dữ liệu và unit test cơ bản.
- `pyproject.toml`, `uv.lock`: Quản lý thư viện và khóa phiên bản với `uv`.
- `.env.example`: File mẫu cấu hình biến môi trường (`GEMINI_API_KEY`).

## 🛠️ Cài đặt môi trường (Setup)

Yêu cầu: **Python >= 3.10** và **[uv](https://docs.astral.sh/uv/)**.

### 1. Cài đặt các thư viện phụ thuộc
```bash
uv sync
```
*(Nếu dùng IDE như PyCharm/VS Code, chọn Python Interpreter là `.venv/bin/python` trong thư mục dự án.)*

### 2. Cấu hình API Key (từ Bài 16 trở đi)
Copy file mẫu thành `.env` rồi điền API Key của bạn vào:
```bash
cp .env.example .env
```
Mở `.env` và cập nhật:
```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```
> **Bảo mật:** File `.env` đã được khai báo trong `.gitignore` để không bao giờ bị đẩy nhầm lên GitHub.

## 🚀 Hướng dẫn chạy

### 1. Chạy các bài thực hành dữ liệu
```bash
uv run python lesson13.py
uv run python lesson14.py
```

### 2. Khởi động FastAPI Server
```bash
# Bài 12 (CRUD Users)
uv run uvicorn main:app --reload

# Bài 16 (Fintech Analytics + Gemini API)
uv run uvicorn lesson16:app --reload
```
Truy cập tài liệu Swagger UI tự động tại: `http://127.0.0.1:8000/docs`

### 3. Chạy kiểm thử tự động
```bash
uv run pytest test_main.py
```
