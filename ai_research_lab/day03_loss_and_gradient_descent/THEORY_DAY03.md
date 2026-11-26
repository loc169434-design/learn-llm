# Lý Thuyết Ngày 03: Mở Hộp Đen `model.fit()` — Hàm Mất Mát (`Cross-Entropy Loss`) & Thuật Toán Hạ Đồi (`Gradient Descent`)

> **Mục tiêu hiểu bản chất:** Ở Ngày 02, bạn chỉ cần gọi đúng 1 dòng `model.fit(X_train, y_train)` là máy tự học ra trọng số $W$ phân loại 4 nhãn. Ở Ngày 03, ta **mở nắp hộp đen** để xem bên trong `model.fit()` thực chất đang chạy vòng lặp toán học gì giúp máy "tự sửa sai" qua từng bước!

---

# TIẾT 1: Hàm Mất Mát (`Cross-Entropy Loss`) — "Thước Đo Nỗi Đau Khi AI Đoán Sai"

## 1. Muốn máy tự sửa sai, trước hết phải chấm điểm nó "sai nặng tới mức nào"!

Trong một mô hình phân loại (như Logistic Regression hay Deep Learning PyTorch ở Ngày 04), khi đọc 1 tin nhắn `URGENT`, mô hình xuất ra **xác suất dự đoán $p$** cho nhãn đúng `URGENT` (nằm từ `0.0` đến `1.0`):
- **Tình huống A (Tốt):** Máy đoán xác suất `URGENT` là **`p = 0.95`** (95% chắc chắn) → Sai số cực nhỏ!
- **Tình huống B (Hơi do dự):** Máy đoán **`p = 0.60`** → Đúng nhưng chưa tự tin, cần phạt nhẹ.
- **Tình huống C (Nguy hiểm — "Sai mà lại cực kỳ tự tin!"):** Thật sự là `URGENT`, nhưng máy đoán `URGENT` chỉ có **`p = 0.01`** (tức tự tin tới 99% đó là tin rác!) → **Phải phạt cực nặng!**

---

## 2. Công thức `Cross-Entropy Loss` (Hàm phạt bằng Logarit âm)

Để trừng phạt theo đúng tâm lý trên, hầu hết mọi mô hình phân loại (từ Logistic Regression đến PyTorch, PhoBERT, thậm chí cả lúc huấn luyện ChatGPT/Gemini dự đoán từ tiếp theo!) đều dùng chung 1 công thức huyền thoại:

$$\mathcal{L} = -\log(p_{\text{nhãn đúng}})$$

Hãy thay 3 tình huống ở trên vào bấm thử (dùng logarit tự nhiên $\ln$):
- Nếu $p = 0.99$ (đoán cực chuẩn) $\rightarrow \mathcal{L} = -\ln(0.99) \approx \mathbf{0.01}$ *(Gần như không bị phạt!)*.
- Nếu $p = 0.50$ (đoán 50/50 như tung đồng xu) $\rightarrow \mathcal{L} = -\ln(0.50) \approx \mathbf{0.69}$ *(Phạt vừa)*.
- Nếu $p = 0.01$ (đoán sai bét mà lại cực tự tin) $\rightarrow \mathcal{L} = -\ln(0.01) \approx \mathbf{4.61}$ *(Phạt nặng gấp **460 lần** so với $p = 0.99$!)*.
- Nếu $p \to 0$ $\rightarrow \mathcal{L} \to \mathbf{+\infty}$ *(Phạt vô cực!)*.

👉 **Tại sao hàm `Loss` phải liên tục & trơn tru (khác với `Accuracy` chỉ có `0` hoặc `1`)?**
- `Accuracy` giống kiểu chấm *"Đúng = 1, Sai = 0"* — nó là **bậc thang đứt gãy**, nên máy không biết nhích trọng số $W$ sang trái hay sang phải thì có tốt lên không!
- `Cross-Entropy Loss` là một **đường cong dốc trơn tru** → ta có thể **tính độ dốc (đạo hàm)** để biết chính xác nên chỉnh trọng số $W$ theo hướng nào để giảm lỗi!

---

# TIẾT 2: Thuật Toán Hạ Đồi (`Gradient Descent`) & Tốc Độ Học (`Learning Rate`)

## 3. Hình ảnh "Người bịt mắt đi xuống thung lũng trong sương mù"

Hãy tưởng tượng tổng `Loss` là một **ngọn núi có đáy thung lũng** (nơi đáy thung lũng chính là vị trí trọng số $W^*$ tốt nhất có sai số nhỏ nhất):
1. Lúc mới khởi tạo (chưa học gì), trọng số $W$ nằm ngẫu nhiên trên sườn núi (`Loss` rất cao).
2. Tại chỗ đang đứng, máy **dò độ dốc bằng chân** — tức là tính **Đạo hàm (*Gradient*)** $\frac{\partial \mathcal{L}}{\partial W}$:
   - Nếu sườn núi đang **dốc lên về phía bên phải** (đạo hàm **dương** $> 0$) $\rightarrow$ muốn đi xuống đáy phải **bước sang trái** (trừ bớt $W$).
   - Nếu sườn núi đang **dốc xuống về phía bên phải** (đạo hàm **âm** $< 0$) $\rightarrow$ muốn đi xuống đáy phải **bước sang phải** (cộng thêm $W$).
3. Gộp cả 2 trường hợp lại thành **1 công thức cập nhật trọng số duy nhất của toàn ngành Deep Learning**:

$$W_{\text{mới}} = W_{\text{cũ}} - \eta \cdot \frac{\partial \mathcal{L}}{\partial W}$$

Trong đó **$\eta$ (`lr` — Learning Rate / Tốc độ học)** chính là **độ dài sải chân mỗi bước**:
- **`lr` quá nhỏ** (VD `0.00001`): Bước từng milimet → đi cả ngày không tới đáy (train cực chậm!).
- **`lr` quá lớn** (VD `10.0`): Bước sải quá dài → nhảy vọt qua luôn đáy thung lũng sang bờ núi bên kia, nảy qua nảy lại rồi **văng lên trời (`Loss = NaN / Diverge`)**!
- **`lr` vừa đẹp** (VD `0.01` – `0.1` với ML cơ bản, `1e-3` với Adam/PyTorch, `2e-5` khi Fine-tune Transformer): Đi êm ái xuống đúng đáy thung lũng!

👉 **Chính vòng lặp lặp đi lặp lại 3 bước này gọi là 1 Epoch huấn luyện:**
1. **Forward Pass:** Tính dự đoán $\hat{y}$ và đo nỗi đau `Loss`.
2. **Backward Pass (Gradient):** Tính độ dốc $\frac{\partial \mathcal{L}}{\partial W}$.
3. **Update Step:** Nhích $W \leftarrow W - \text{lr} \cdot \text{gradient}$.
