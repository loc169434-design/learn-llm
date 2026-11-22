# Phòng Thí Nghiệm Tự Luyện & Tự Train AI Thực Nghiệm (`ai_research_lab`)

Thư mục này là **không gian rèn luyện hàng ngày** của bạn theo phương châm:
> **"Học tới đâu hiểu tận gốc bản chất lý thuyết tới đó — Tự tay code từ con số 0 trước khi dùng thư viện — Mỗi ngày tích lũy 1 mảnh ghép tiến tới Dự án Nghiên cứu hoàn chỉnh trình TS. Bùi Thanh Hùng & phỏng vấn Mobile AI."**

---

## 1. Quy Tắc Lớp Học Hàng Ngày (Bắt Buộc Tuân Thủ)

Mỗi ngày là một thư mục riêng (`day01_...` đến `day14_...`), đi theo **3 quy tắc sắt**:
1. **Học chậm theo từng tiết (nửa bài), hiểu tận gốc bản chất:** Đọc/nghe giảng kỹ từng công thức và cơ chế (`THEORY_DAYXX.md`), biết rõ *tại sao* trước khi gõ code.
2. **Kiểm tra 5–7 câu trắc nghiệm tương tác:** Bấm làm quiz ngay sau mỗi tiết lý thuyết để chắc chắn không hiểu lờ mờ.
3. **Quy tắc 15 phút tự lực (Chỉ nhận gợi ý hướng đi, KHÔNG xem code giải trước):**
   - Với mọi bài tập `# TODO` trong `labXX_...py`, AI **chỉ chỉ hướng tư duy & đầu vào/đầu ra**, tuyệt đối không đưa sẵn code giải.
   - Bấm giờ tự suy nghĩ và tự gõ trong ít nhất **15 phút**. Chỉ sau 15 phút (hoặc khi đã tự viết ra bản nháp để nhờ review) mới hỏi AI góp ý/gỡ bí.
4. **Ghi số liệu thực nghiệm vào `PROGRESS_TRACKER.md`:** Lưu con số đo được sau mỗi ngày và `git push` để đồng bộ giữa các máy.

---

## 2. Lộ Trình 14 Ngày: Từ Bản Chất Toán Học Tới Tự Train Model + XAI + RAG

### Giai đoạn 1 (Ngày 01 – 03): Bản chất Học Máy (Machine Learning) & Xử lý Ngôn ngữ Tiếng Việt
- **Ngày 01 (`day01_tfidf_and_vn_text`):** Bản chất số hóa ngôn ngữ, chuẩn hóa tiếng Việt không dấu/viết tắt, tự code công thức **TF-IDF** từ con số 0 (liên hệ bài *VN-QA 2019* & trọng số *LTF-MICF 2023* của thầy).
- **Ngày 02 (`day02_ml_classifiers_and_metrics`):** Bản chất ranh giới quyết định (*Decision Boundary*), Overfitting vs Underfitting, bẫy Accuracy khi lệch nhãn -> Tự train & đo **Precision, Recall, F1, Confusion Matrix** với `Logistic Regression`, `SVM`, `Random Forest` (bài *ML 2020/2022* của thầy).
- **Ngày 03 (`day03_loss_and_gradient_descent`):** Mở hộp đen quá trình "máy học": Tự code hàm mất mát **Cross-Entropy Loss** và thuật toán hạ đồi **Gradient Descent** bằng NumPy thuần để thấy tận mắt trọng số $W$ tự sửa sai qua từng vòng lặp!

### Giai đoạn 2 (Ngày 04 – 07): Mạng Nơ-ron Sâu (PyTorch), Cơ chế Attention & Fine-tune Transformer trên GPU Mac (`mps`)
- **Ngày 04 (`day04_pytorch_mlp_and_backprop`):** Bản chất Tensor, hàm kích hoạt phi tuyến (`ReLU`/`GELU`), lan truyền ngược (`Backpropagation`) và huấn luyện mạng **MLP** trên nhân GPU Apple Silicon.
- **Ngày 05 (`day05_bigru_and_self_attention`):** Bản chất mạng hồi quy 2 chiều **Bi-GRU** và tự code lớp **Attention Mechanism** (bài *GARN 2023* của thầy) — trích xuất trọng số chú ý để giải thích từ khóa nào quyết định nhãn `KHẨN CẤP`!
- **Ngày 06 (`day06_finetune_transformer_vn`):** Bản chất kiến trúc **Transformer / Pre-trained Model** -> Tự **Fine-tune PhoBERT / Multilingual DistilBERT** phân loại tin nhắn tiếng Việt và lập bảng đối sánh 3 thế hệ AI.
- **Ngày 07 (`day07_model_export_and_latency`):** Lượng tử hóa (**Quantization**) và đóng gói model tự train sang `.onnx` / `.pt`, đo tốc độ thực tế (`ms/câu`) so với gọi Cloud API.

### Giai đoạn 3 (Ngày 08 – 10): Thị Giác Máy Tính, Cắt Ảnh `CIE-LAB` & Giải Thích Hộp Đen `XAI`
- **Ngày 08 (`day08_cielab_saliency_autocrop`):** Bản chất không gian màu **CIE-LAB**, phân ngưỡng **Otsu** và **Moment hình ảnh** -> Tự code bộ cắt vùng bất thường không giám sát **Global-Local Auto-Crop** (đúng công thức bài *Discover AI 10/2026* của thầy!).
- **Ngày 09 (`day09_train_vision_mobilenet`):** Bản chất tích chập **CNN**, hiện tượng học vẹt nền *"Clever Hans"*, tự train **MobileNetV3** phân loại ảnh cảnh báo/chứng từ (so sánh Global vs Global+Local).
- **Ngày 10 (`day10_explainable_ai_gradcam_twins`):** Tự xuất **Bản đồ nhiệt `Grad-CAM`** tô vùng AI nhìn trên ảnh + **Hệ thống song sinh `Twin Cases`** (bài *PeerJ CS 2026* của thầy) tìm ca lịch sử tương đồng giải thích quyết định.

### Giai đoạn 4 (Ngày 11 – 14): Ghép RAG Chống Bịa, Tương Tác Làm Rõ & Hoàn Thiện Báo Cáo Trình Thầy
- **Ngày 11 (`day11_rule_structured_rag`):** Cắt chunk theo cấu trúc logic `[Chủ đề - Điều kiện - Hành động]` (bài *JAIST 2013* của thầy) + lọc ngưỡng Cosine chống ảo giác (nối từ `lesson21.py`).
- **Ngày 12 (`day12_uncertainty_and_clarification`):** Đo độ không chắc chắn (**Entropy / Confidence Threshold**) -> Tự động sinh câu hỏi làm rõ khi dự đoán mơ hồ hoặc ảnh mờ (bài *Interactive VQA 2026*).
- **Ngày 13 (`day13_ablation_study_and_fastapi`):** Chạy **Ablation Study** (thử nghiệm tắt/bật từng thành phần chứng minh hiệu quả khoa học) + Đóng gói toàn bộ vào FastAPI Backend.
- **Ngày 14 (`day14_final_paper_report_and_demo`):** Xuất biểu đồ, tổng hợp báo cáo thực nghiệm chuẩn khoa học để gửi thầy Bùi Thanh Hùng & kết nối demo trên Android `DriveSafeAI`.
