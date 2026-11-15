# NHẬT KÝ HỌC TẬP & LỘ TRÌNH CHUYỂN HƯỚNG MOBILE + AI

## 1. Mục tiêu cá nhân
- **Hồ sơ:** Mobile Developer (Android / Kotlin) kinh nghiệm 3-5 năm, nghiệp vụ Fintech / Ngân hàng.
- **Mục tiêu:** Chuyển hướng sang Mobile + AI Engineer / Backend AI (Target lương: 28 - 33 triệu).
- **Chiến lược:** Vừa học vừa xây dựng project GitHub có source code chạy được, có test tự động và README chuẩn chỉ làm bằng chứng năng lực.

---

## 2. Tiến độ hiện tại

### ✅ Đã hoàn thành (Tuần 1 - Tuần 2)
- **Bài 1 - 4:** Python cơ bản, biến, hàm, vòng lặp, tính tuổi trung bình, gom nhóm theo city, viết test logic.
- **Bài 5 - 8:** Xử lý file JSON (`users.json`), type hints, Pydantic `BaseModel`.
- **Bài 9 - 11:** HTTP client (`requests`, `httpx`), gọi API bên thứ ba.
- **Bài 12: REST API đầu tiên với FastAPI**
  - Đã xong file `main.py`:
    - `GET /users` (hỗ trợ query param `city: Optional[str]`).
    - `GET /users/{user_id}` (path param, ném `HTTPException(404)`).
    - `POST /users` (nhận body Pydantic model, status 201, tự động validate lỗi 422).
    - `GET /stats` (thống kê tổng user, tuổi trung bình, gom nhóm `cities`).
    - `DELETE /users/{user_id}` (xóa user khỏi list bằng `.pop()`, xử lý 404).
  - Đã xong file `test_main.py` dùng `TestClient` (FastAPI + httpx + pytest): **7/7 test cases PASS 100%**.

---

### ⏳ Đang làm (Tuần 3: Xử lý dữ liệu với Pandas)
- **Bài 13: pandas cơ bản**
  - File đang viết: `lesson13.py` (đã có khung đọc file `users.json`, `df.shape`, `mean()`, filter `df[df["age"] > 25]`, `value_counts()`, `groupby()`).
  - **Bài tập tiếp theo cần làm:**
    1. Chạy `lesson13.py` kiểm tra kết quả in ra.
    2. Viết filter kết hợp điều kiện: Tìm người ở "HCM" và có tuổi > 20: `df[(df["city"] == "HCM") & (df["age"] > 20)]`.
    3. Tạo cột mới `age_group` ("under_25" / "25_plus") bằng `.apply()` hoặc lambda, sau đó đếm số lượng mỗi nhóm bằng `value_counts()`.
    4. Xuất bảng ra file CSV: `df.to_csv("report.csv", index=False)`.
    5. Xử lý dữ liệu khuyết tật (Missing data / NaN): thử `df.dropna()` và `df["age"].fillna(0)`.

---

## 3. Bản đồ đối chiếu kiến thức (Android Kotlin vs Python AI)

| Android (Kotlin) | FastAPI / Python | Ghi chú |
| :--- | :--- | :--- |
| `data class User(...)` | `class User(BaseModel):` (Pydantic) | Tự validate kiểu dữ liệu, sai trả về 422 |
| Retrofit `@GET("users/{id}")` | `@app.get("/users/{user_id}")` | Path parameter |
| Retrofit `@Query("city")` | `def list_users(city: Optional[str] = None)` | Query parameter |
| `String?` | `Optional[str]` (Python 3.9) hoặc `str \| None` (Python 3.10+) | Kiểu có thể null |
| `users.filter { ... }` | `df[df["age"] > 25]` (pandas) | Lọc dữ liệu cực nhanh |
| `users.groupBy { ... }` | `df.groupby("city")["age"].mean()` | Gom nhóm tính toán |
| `MockWebServer` | `TestClient(app)` (fastapi.testclient) | Test API không cần bật uvicorn |
| `androidTest / test` | `pytest test_main.py` | Chạy bộ test tự động |

---

## 4. Prompt dán vào máy mới để tiếp tục ngay lập tức

> *"Mình là Android Dev đang học chuyển hướng sang Mobile + AI. Mình đã hoàn thành xong Bài 12 (FastAPI CRUD + TestClient 7/7 test pass trong main.py và test_main.py). Hiện tại mình đang ở Bài 13: Xử lý dữ liệu với Pandas (file lesson13.py). Hãy tiếp tục hướng dẫn mình làm tiếp các bài tập của Bài 13 nhé!"*
