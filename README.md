# Learn LLM & Python Backend for Mobile Developers

Repository lưu trữ lộ trình học tập và thực hành chuyển hướng từ **Mobile Developer (Android / Kotlin)** sang **Mobile + AI & Backend Engineer**.

## 📁 Cấu trúc dự án
- `main.py`: REST API xây dựng bằng FastAPI (CRUD User, lọc query param, tính stats, validate lỗi 422/404).
- `test_main.py`: Bộ kiểm thử tự động toàn diện sử dụng `TestClient` và `pytest` (7/7 test cases pass).
- `lesson13.py`: Thực hành xử lý và phân tích dữ liệu với `pandas` (DataFrame, Series, lọc điều kiện, đếm `value_counts`, gom nhóm `groupby`).
- `STUDY_LOG.md`: Nhật ký học tập chi tiết, bản đồ đối chiếu kiến thức giữa Kotlin/Android và Python/FastAPI/AI.
- `users.json`, `users_cli.py`, `test_users.py`: CLI xử lý dữ liệu và unit test cơ bản.

## 🚀 Hướng dẫn chạy

### 1. Khởi động API Server
```bash
uvicorn main:app --reload
```
Truy cập tài liệu API tự động tại: `http://127.0.0.1:8000/docs`

### 2. Chạy kiểm thử tự động
```bash
pytest test_main.py
```
