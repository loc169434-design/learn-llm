# Lý Thuyết Ngày 02: Phân Loại Học Máy (`Logistic Regression`, `SVM`, `Random Forest`), Bẫy `Overfitting` & Bộ Chỉ Số Đánh Giá

> **Mục tiêu hiểu bản chất:** Ở Ngày 01, bạn đã biến 48 tin nhắn tiếng Việt thành ma trận số học TF-IDF (`48 × 484`). Ở Ngày 02, bạn sẽ hiểu tận gốc **cách 3 thuật toán Machine Learning kinh điển học ra quy luật phân loại 4 nhãn (`URGENT`, `BANKING`, `NORMAL`, `SPAM`)**, vì sao không được vừa học vừa thi trên cùng 1 tập đề, và cách đọc **Confusion Matrix / Precision / Recall / F1** chuẩn các bài báo ML 2020–2022 của TS. Bùi Thanh Hùng.

---

# TIẾT 1: Ranh Giới Quyết Định (`Decision Boundary`), 3 Mô Hình Kinh Điển & `Overfitting`

## 1. "Huấn luyện mô hình phân loại" thực chất là làm gì?

Hãy hình dung mỗi tin nhắn sau khi qua **TF-IDF (Ngày 01)** trở thành **1 điểm chấm** trong không gian nhiều chiều (trong bài của bạn là không gian 484 chiều — tạm tưởng tượng xuống mặt phẳng 2 chiều cho dễ nhìn: trục ngang là điểm từ khóa *khẩn cấp*, trục dọc là điểm từ khóa *quảng cáo*).

- Nhiệm vụ của thuật toán **Phân loại (Classification)** không có gì thần bí: nó chỉ đi tìm những **đường ranh giới (Decision Boundary)** để ngăn cách các nhóm điểm khác màu (`URGENT`, `BANKING`, `NORMAL`, `SPAM`) sao cho khi có **1 tin nhắn mới tinh** rơi vào mặt phẳng, máy chỉ cần nhìn xem điểm đó nằm ở phía nào của đường ranh giới để phán nhãn!

---

## 2. Cơ chế của 3 thuật toán kinh điển (hay dùng làm Baseline trong bài báo thầy Hùng)

### A. Logistic Regression (Hồi quy Logistic — "Chiếc cân trọng số có xác suất")
- **Tư duy gốc:** Gán cho mỗi từ trong từ điển một **trọng số $w_j$** (có thể dương hoặc âm):
  $$z = w_1 x_1 + w_2 x_2 + \dots + w_V x_V + b$$
  Ví dụ cho lớp `URGENT`: từ `"cấp"`, `"cứu"`, `"sốt"`, `"gấp"` sẽ học được trọng số dương lớn (`+2.5`, `+3.1`); còn từ `"khuyến"`, `"mãi"`, `"sale"` có trọng số âm (`-2.0`).
- **Biến tổng điểm $z$ thành xác suất từ `0%` đến `100%`:**
  - Nếu phân loại 2 lớp (nhị phân): dùng hàm **Sigmoid** $\sigma(z) = \frac{1}{1 + e^{-z}}$.
  - Nếu phân loại nhiều lớp (4 nhãn như bài của bạn): dùng hàm **Softmax** biến 4 điểm số $(z_1, z_2, z_3, z_4)$ thành 4 xác suất cộng lại bằng `1.0` (VD: `URGENT: 0.88, NORMAL: 0.08, BANKING: 0.03, SPAM: 0.01`).
- **Đặc trưng:** Ranh giới là **đường thẳng / siêu phẳng tuyến tính**, chạy cực nhanh (vài mili-giây), **dễ giải thích** (soi thẳng bảng trọng số $w_j$ là biết ngay từ nào đẩy nhãn lên cao!).

### B. SVM — Support Vector Machine ("Kẻ kẻ lề đường an toàn rộng nhất")
- **Vấn đề:** Có vô số đường thẳng đều chia đúng 2 nhóm điểm trên tập huấn luyện — đường nào là tốt nhất?
- **Ý tưởng thiên tài của SVM:** Không chỉ tìm 1 đường chia đúng, mà tìm **đường thẳng nằm chính giữa sao cho khoảng cách tới những điểm gần nó nhất (lề — *Margin*) là RỘNG NHẤT có thể**!
- Những điểm nằm sát mép ranh giới nhất (những tin nhắn mập mờ, khó phân loại nhất) được gọi là **Support Vectors (Vector hỗ trợ)** — chỉ chúng mới quyết định vị trí đường ranh giới.
- **Đặc trưng:** Cực kỳ mạnh trên **dữ liệu văn bản nhiều chiều (TF-IDF hàng trăm–hàng nghìn cột) nhưng ít mẫu** (như tập 48 tin nhắn của bạn hoặc các bài báo phân loại văn bản của thầy Hùng!).

### C. Random Forest (Rừng ngẫu nhiên — "Hội đồng hàng trăm cây `if-else` bỏ phiếu")
- **Cơ chế:**
  1. Một **Decision Tree (Cây quyết định)** tự học một chuỗi câu hỏi `if / else` dạng: *`if tfidf("gấp") > 0.25 -> URGENT else if tfidf("otp") > 0.2 -> BANKING ...`* — nhưng **1 cây đơn lẻ rất dễ học vẹt (Overfitting)**.
  2. **Random Forest** tạo ra **100 cây quyết định khác nhau** (mỗi cây chỉ được nhìn một phần ngẫu nhiên của dữ liệu và một tập con ngẫu nhiên các từ vựng).
  3. Khi có tin nhắn mới, cả 100 cây cùng bỏ phiếu → nhãn nào được nhiều phiếu nhất sẽ thắng (**Majority Voting**).
- **Đặc trưng:** Học được ranh giới **phi tuyến (gấp khúc phức tạp)**, rất mạnh trên dữ liệu dạng bảng (Fintech: tuổi, số tiền, lịch sử giao dịch), nhưng trên dữ liệu text thưa (`sparse TF-IDF`) ít mẫu thường kém hơn `Linear SVM` / `Logistic Regression`.

---

## 3. Tại sao phải chia `Train / Test Split`? — `Underfitting` vs `Overfitting`

Nếu bạn cho sinh viên ôn **100 câu trắc nghiệm có sẵn đáp án**, rồi hôm sau đem **y nguyên 100 câu đó** ra làm đề thi:
- Một bạn học vẹt thuộc lòng *"Câu 1 chọn B, Câu 2 chọn D"* sẽ được **10/10** trong phòng tập, nhưng gặp câu hỏi mới ngoài đời thực sẽ **thi rớt thảm hại**!
- Vì vậy trong Machine Learning, ta **bắt buộc tách dữ liệu thành 2 phần tách biệt ngay từ đầu**:
  - **Tập Train (thường 75–80%):** Đưa cho model học trọng số $W$.
  - **Tập Test (thường 20–25%):** **Giấu kín tuyệt đối**, chỉ mở ra chấm điểm sau khi model đã học xong!
  - *(Lưu ý sống còn — **Data Leakage / Rò rỉ dữ liệu**: Phải fit bộ từ điển & `IDF` chỉ trên tập **Train**, không được cho tập Test góp mặt vào bước tính `IDF` trước khi chia, kẻo model "nhìn trộm đề thi"!)*
  - *(Với bộ dữ liệu nhỏ có nhiều nhãn như 48 tin / 4 nhãn, phải dùng **Stratified Split** `stratify=y` để đảm bảo mỗi nhãn đều có tỷ lệ đều nhau ở cả Train lẫn Test — không bị cảnh tập Test thiếu hẳn nhãn `URGENT`!)*

### Ba trạng thái của mô hình (Cực hay hỏi khi phỏng vấn AI):
| Trạng thái | Điểm trên Tập Train | Điểm trên Tập Test | Bản chất đời thường |
| :--- | :---: | :---: | :--- |
| **Underfitting** *(Học chưa tới)* | Thấp (VD: 55%) | Thấp (VD: 50%) | Mô hình quá đơn giản hoặc học chưa đủ — đề cũ cũng sai, đề mới cũng sai. |
| **Good Fit** *(Học hiểu bản chất)* | Cao (VD: 92%) | Cao (VD: 89%) | Nắm được quy luật tổng quát — làm tốt cả đề cũ lẫn tin nhắn mới ngoài đời. |
| **Overfitting** *(Học vẹt)* | Rất cao (VD: 100%) | Rất thấp (VD: 60%) | Học thuộc luôn cả nhiễu của tập Train, mất khả năng tổng quát hóa sang dữ liệu mới. |

---

# TIẾT 2: Cái Bẫy `Accuracy`, `Confusion Matrix` & Bộ Ba `Precision / Recall / F1-Score`

## 4. Tại sao `Accuracy = 95%` đôi khi lại là một mô hình VÔ DỤNG?

Giả sử trên điện thoại tài xế trong 1 tuần có **100 tin nhắn**:
- **95 tin** là quảng cáo / bình thường (`NORMAL/SPAM`).
- Chỉ có **5 tin** là cấp cứu khẩn cấp (`URGENT`).

Một mô hình **"lười biếng"** không thèm học gì cả, cứ hễ có tin nhắn là phán bừa **`KHÔNG KHẨN CẤP`**.
- Số lần đoán đúng: `95 / 100` $\rightarrow$ **`Accuracy = 95%`**!
- Nhưng nó **bỏ lọt 100% tin nhắn cấp cứu (`5/5` ca nguy hiểm đều im lặng)**!

👉 Khi dữ liệu **lệch nhãn (*Imbalanced Dataset*)** hoặc chi phí bỏ sót ca nguy hiểm cực lớn (y tế, gian lận Fintech, tin khẩn cấp khi lái xe), **chỉ nhìn `Accuracy` là tự lừa dối mình**!

---

## 5. Ma Trận Nhầm Lẫn (`Confusion Matrix`) & Bộ Ba `Precision / Recall / F1`

Xét riêng nhãn `URGENT` (coi `URGENT` là **Dương tính — Positive**):
- **TP (True Positive):** Thật sự là `URGENT`, máy đoán đúng `URGENT`. *(Tốt!)*
- **FP (False Positive — Báo động giả):** Thật sự là `SPAM/NORMAL`, máy đoán nhầm là `URGENT` → Làm phiền tài xế đọc nhầm tin rác.
- **FN (False Negative — Bỏ sót nguy hiểm):** Thật sự là `URGENT` (con sốt đi cấp cứu), máy đoán nhầm là `SPAM` → **Bỏ lọt tin khẩn cấp!**
- **TN (True Negative):** Thật sự không khẩn cấp, máy cũng đoán không khẩn cấp. *(Tốt!)*

Từ 4 ô trên, ta rút ra 3 thước đo chuẩn trong mọi bài báo khoa học:

1. **Precision (Độ chính xác khi báo động):**
   $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
   *Trả lời câu hỏi:* **"Trong các tin máy báo là `URGENT`, có bao nhiêu % thật sự là `URGENT`?"** (Precision thấp = máy hay báo động giả).

2. **Recall (Độ phủ / Khả năng không bỏ sót):**
   $$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
   *Trả lời câu hỏi:* **"Trong tổng số tin thật sự `URGENT` ngoài đời, máy tóm được bao nhiêu %?"** (Với bài toán cấp cứu / chống gian lận Fintech, **Recall cực kỳ quan trọng** vì không được phép bỏ sót!).

3. **F1-Score (Trung bình điều hòa giữa Precision và Recall):**
   $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
   - Tại sao dùng *trung bình điều hòa* chứ không lấy `(Precision + Recall) / 2`?
   - Vì trung bình điều hòa **phạt rất nặng nếu 1 trong 2 chỉ số bị thấp**: ví dụ `Precision = 1.0`, `Recall = 0.0` → trung bình cộng vẫn ra `0.50` (tưởng tạm ổn), còn `F1` tụt thẳng về **`0.0`**!
   - Với bài toán nhiều lớp (4 nhãn `URGENT`, `BANKING`, `NORMAL`, `SPAM`), người ta dùng **Macro-F1** (tính F1 riêng cho từng nhãn rồi lấy trung bình cộng đều 4 nhãn — để không nhãn thiểu số nào bị che lấp!).
