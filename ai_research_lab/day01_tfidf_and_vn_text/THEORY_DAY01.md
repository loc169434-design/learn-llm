# Lý Thuyết Ngày 01: Bản Chất Số Hóa Ngôn Ngữ, Tiếng Việt Không Dấu & Công Thức TF-IDF

> **Mục tiêu hiểu bản chất:** Sau 10 phút đọc file này, bạn sẽ hiểu tận gốc **làm thế nào một câu tin nhắn tiếng Việt biến thành một mảng số học (`Vector`)** để đưa vào huấn luyện AI, và vì sao các bài báo của TS. Bùi Thanh Hùng luôn đặt khâu **Chuẩn hóa tiếng Việt + Trọng số từ** ở ngay đầu pipeline.

---

## 1. Câu Hỏi Gốc Rễ: Tại Sao Phải Biến Chữ Thành Số?

Mọi thuật toán Học Máy (từ `SVM`, `Random Forest` tới `PyTorch Deep Learning` hay `GPT/Gemini`) về bản chất chỉ là các phép nhân ma trận $y = W \cdot x + b$. Máy tính không thể lấy `W * "cấp cứu"` được — nó bắt buộc phải nhận đầu vào $x$ là một dãy con số thực, ví dụ:
$$x = [0.0,\; 0.82,\; 0.0,\; 0.45,\; \dots]$$

Quá trình biến câu chữ thành dãy số $x$ gọi là **Vectorization (Vector hóa văn bản)**.

---

## 2. Tại Sao Chỉ "Đếm Số Lần Từ Xuất Hiện" Lại Thất Bại?

Giả sử bạn có 2 tin nhắn gửi tới khi đang lái xe:
- **Câu 1 (Khẩn cấp):** `"Anh ơi con sốt cao đưa đi viện gấp anh ơi"` (10 từ)
- **Câu 2 (Bình thường):** `"Anh ơi tối nay về ăn cơm nhé anh ơi"` (10 từ)

Nếu ta chỉ đếm tần suất từ (**TF — Term Frequency**):
$$\text{TF}(t, d) = \frac{\text{Số lần từ } t \text{ xuất hiện trong câu } d}{\text{Tổng số từ của câu } d}$$

Trong Câu 1:
- Từ `"anh"` và `"ơi"` xuất hiện 2 lần $\rightarrow \text{TF} = \frac{2}{10} = 0.20$ (**Cao nhất câu!**)
- Từ `"sốt"`, `"viện"`, `"gấp"` chỉ xuất hiện 1 lần $\rightarrow \text{TF} = \frac{1}{10} = 0.10$ (**Thấp bằng một nửa!**)

👉 **Hậu quả tai hại:** Nếu đem vector này đi train AI, máy sẽ tưởng Câu 1 và Câu 2 **rất giống nhau** vì cả hai đều có điểm cao chót vót ở chữ `"anh"` và `"ơi"`, trong khi chữ quyết định sinh tử là `"sốt"`, `"viện"`, `"gấp"` lại bị lép vế!

---

## 3. Ý Tưởng Thiên Tài Của `IDF`: Phạt Từ Phổ Biến, Thưởng Từ Đặc Trưng

Để sửa sai lầm trên, các nhà khoa học nhân thêm một đại lượng gọi là **IDF (Inverse Document Frequency — Nghịch đảo tần suất văn bản)**:

$$\text{IDF}(t) = \log\left(\frac{N + 1}{\text{DF}(t) + 1}\right) + 1$$

Trong đó:
- $N$: Tổng số tin nhắn trong kho dữ liệu (ví dụ $N = 100$ tin nhắn).
- $\text{DF}(t)$ (*Document Frequency*): Số lượng tin nhắn có chứa từ $t$.
- *(Cộng thêm `+1` ở tử và mẫu gọi là **Smooth IDF** để không bao giờ bị lỗi chia cho `0` khi gặp từ mới!)*

Hãy nhẩm thử bằng con số thực tế với $N = 100$:
- Từ `"anh"` xuất hiện ở **80/100** tin nhắn $\rightarrow \text{IDF}(\text{"anh"}) = \log\left(\frac{101}{81}\right) + 1 \approx \mathbf{1.22}$ *(Điểm thấp)*.
- Từ `"viện"` chỉ xuất hiện ở **2/100** tin nhắn $\rightarrow \text{IDF}(\text{"viện"}) = \log\left(\frac{101}{3}\right) + 1 \approx \mathbf{4.52}$ *(Điểm cao gấp gần 4 lần!)*.

Ghép cả hai lại ta được công thức huyền thoại **TF-IDF**:
$$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t)$$

Một từ chỉ đạt điểm **TF-IDF cao vọt** khi thỏa đồng thời 2 điều kiện:
1. Xuất hiện nổi bật trong câu hiện tại (**TF cao**).
2. Hiếm khi xuất hiện tràn lan ở các câu khác (**IDF cao**).

---

## 4. Liên Hệ Trực Tiếp Với 2 Bài Báo Của TS. Bùi Thanh Hùng

1. **Bài toán Tiếng Việt Không Dấu & Viết Tắt (*ASTESJ, 2019*):**
   - Ngoài đời thực, tài xế hoặc người thân nhắn vội trên Zalo: `"ck 500k gap"`, `"dua con di bv ngay"`, `"km giam gia 50%"`.
   - Với máy tính, chuỗi `"bv"`, `"benh vien"`, và `"bệnh viện"` là **3 chuỗi ký tự khác nhau hoàn toàn**! Nếu không có bước **Chuẩn hóa từ viết tắt & tiếng Việt** trước khi tính TF-IDF, dữ liệu bị phân mảnh làm model học kém đi rất nhiều.
2. **Nâng cấp lên Trọng số theo Lớp Nhãn (*LTF-MICF trong bài GARN, Journal of Big Data 2023*):**
   - Trong bài báo năm 2023, thầy Hùng cải tiến thêm một nấc: Không chỉ xét từ đó hiếm trong toàn kho văn bản ($N$), mà xét xem từ đó có **chỉ tập trung ở đúng 1 nhãn cụ thể** hay không (ví dụ từ `"OTP"`, `"số dư"` chỉ xuất hiện ở nhãn `BANKING` chứ không bao giờ nằm ở `SPAM` hay `NORMAL`). Khi sang Ngày 02 train model phân loại, các trọng số tuyến tính $W$ của `Logistic Regression` / `SVM` sẽ tự học chính xác độ lệch theo nhãn này!

---

## 5. Đối Chiếu Tư Duy Kotlin (Android) Sang Python (NumPy)

| Khái niệm Toán AI | Tương đương trong code Kotlin / Python của bạn |
| :--- | :--- |
| Bộ từ điển `vocab` ($V$ từ duy nhất) | `List<String>` cố định thứ tự từ cột `0` đến cột `V - 1` |
| Vector TF-IDF của 1 tin nhắn | `FloatArray(V)` (mảng 1 chiều gồm $V$ con số thực) |
| Ma trận TF-IDF của $N$ tin nhắn | Mảng 2 chiều `shape = (N, V)` — gồm $N$ dòng (tin nhắn) $\times$ $V$ cột (từ vựng) |

👉 Giờ bạn hãy mở file `lab01_tfidf_from_scratch.py` và hoàn thành **3 `# TODO`** để tự tay tạo ra bộ máy Vector hóa đầu tiên của mình nhé!
