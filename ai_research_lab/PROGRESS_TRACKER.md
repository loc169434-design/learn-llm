# Bảng Theo Dõi Tiến Độ Hàng Ngày (`PROGRESS_TRACKER.md`)

Cập nhật file này mỗi khi hoàn thành 1 ngày để giữ mạch kiến thức và lưu lại các con số thực nghiệm (dùng làm bảng kết quả cuối kỳ trình thầy Hùng).

---

## Trạng Thái Hiện Tại
- **Ngày đã hoàn thành:** `Ngày 02 — day02_ml_classifiers_and_metrics` (✅ Đã xong Lý thuyết Tiết 1 + Tiết 2, Trắc nghiệm & pass 100% `lab02_ml_classifiers.py`).
- **Đang học:** `Ngày 03 — day03_loss_and_gradient_descent` (Tiết 1 Lý thuyết: *Hàm mất mát `Cross-Entropy Loss` & Thuật toán hạ đồi `Gradient Descent`*) + **Bài 22 (`lesson22.py`)**: Local Vector Store & Đánh giá RAG.

---

## Nhật Ký 14 Ngày Luyện Lý Thuyết & Thực Nghiệm Code

| Ngày | Chủ đề & Thư mục | Bản chất lý thuyết cần nắm vững | Trạng thái Code | Kết quả thực nghiệm ghi nhận |
| :--- | :--- | :--- | :---: | :--- |
| **Day 01** | `day01_tfidf_and_vn_text` | Tokenization, chuẩn hóa không dấu/viết tắt, công thức gốc `TF`, `IDF`, `TF-IDF` & `Cosine Similarity` | ✅ Hoàn thành | Ma trận TF-IDF `48 x 484`; Twin Search câu không dấu *"anh oi con sot cao dua di bv cap cuu gap"* khớp Top-3 đều `[URGENT]` (Top-1 `score=0.709`). Phát hiện nhiễu IDF từ không dấu chưa chuẩn hóa (`'di'`: `3.7932`). |
| **Day 02** | `day02_ml_classifiers_and_metrics` | Decision Boundary, Overfitting/Underfitting, Precision / Recall / F1-Score / Confusion Matrix | ✅ Hoàn thành | Split `36 Train / 12 Test` (`384` features, chống Data Leakage). **Linear SVM vô địch:** `Test Acc=83.3%`, `Macro-F1=0.831`, `URGENT Recall=100%` (`3/3`), đoán đúng `3/3` câu mới; Logistic Regression `Macro-F1=0.757`; Random Forest bị Overfitting nặng (`Train 100%` vs `Test 33.3%`, `URGENT Recall=0%`). |
| **Day 03** | `day03_loss_and_gradient_descent` | Hàm mất mát `Cross-Entropy Loss`, đạo hàm & `Gradient Descent`, vai trò của `Learning Rate` | ⏳ Đang học Tiết 1 | *(Mở hộp đen bên trong `model.fit()`)* |
| **Day 04** | `day04_pytorch_mlp_and_backprop` | PyTorch Tensor, hàm phi tuyến `ReLU`/`GELU`, `Backpropagation` trên GPU Apple Silicon (`mps`) | ⬜ Chưa mở | — |
| **Day 05** | `day05_bigru_and_self_attention` | Thứ tự chuỗi trong `Bi-GRU`, công thức trọng số `Self-Attention` ($\alpha_i$) giải thích từ khóa | ⬜ Chưa mở | — |
| **Day 06** | `day06_finetune_transformer_vn` | Cơ chế `Transformer` & `Transfer Learning`, tự Fine-tune model tiếng Việt | ⬜ Chưa mở | — |
| **Day 07** | `day07_model_export_and_latency` | Lượng tử hóa `Quantization`, xuất `.onnx` / `.pt`, đo tốc độ Local (`ms`) vs Cloud API | ⬜ Chưa mở | — |
| **Day 08** | `day08_cielab_saliency_autocrop` | Hệ màu `CIE-LAB`, ngưỡng tự động `Otsu`, `Image Moments` cắt vùng `Local Patch` | ⬜ Chưa mở | — |
| **Day 09** | `day09_train_vision_mobilenet` | Tích chập `CNN`, bẫy học vẹt nền *"Clever Hans"*, train `MobileNetV3` (Global vs Global+Local) | ⬜ Chưa mở | — |
| **Day 10** | `day10_explainable_ai_gradcam_twins` | Giải thích hộp đen `Grad-CAM` Heatmap trên ảnh & đối chiếu ca lịch sử `Twin Cases XAI` | ⬜ Chưa mở | — |
| **Day 11** | `day11_rule_structured_rag` | Cắt chunk cấu trúc `[Chủ đề - Điều kiện - Hành động]` & lọc ngưỡng `min_score` chống bịa | ⬜ Chưa mở | — |
| **Day 12** | `day12_uncertainty_and_clarification` | Đo độ bất định `Entropy / Confidence` & sinh câu hỏi làm rõ khi thông tin mơ hồ | ⬜ Chưa mở | — |
| **Day 13** | `day13_ablation_study_and_fastapi` | Thiết kế bảng `Ablation Study` chuẩn bài báo khoa học & tích hợp vào FastAPI | ⬜ Chưa mở | — |
| **Day 14** | `day14_final_paper_report_and_demo` | Hoàn thiện Báo cáo Thực nghiệm gửi thầy Hùng + Demo End-to-End trên Android | ⬜ Chưa mở | — |

---

## Câu Hỏi Tự Kiểm Tra Sau Mỗi Ngày (Hiểu Bản Chất = Trả Lời Được Không Cần Nhìn Sách)
- **Sau Ngày 01:**
  1. Tại sao nếu chỉ đếm số lần xuất hiện của từ (`TF`), các từ vô thưởng vô phạt như *"là"*, *"của"*, *"anh"*, *"ơi"* lại lấn át các từ quyết định như *"cấp cứu"* hay *"OTP"*?
  2. Hàm $\log\left(\frac{N}{\text{DF}(t)}\right)$ trong `IDF` làm nhiệm vụ "thưởng" hay "phạt" những từ xuất hiện ở hầu hết mọi tin nhắn?
  3. Tại sao khi người Việt nhắn tin không dấu viết tắt (`"ck 500k gap"`), nếu không có bước chuẩn hóa viết tắt trước khi tính vector thì máy sẽ coi `"ck"` và `"chuyển khoản"` là hai từ hoàn toàn xa lạ?
