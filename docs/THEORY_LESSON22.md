# Lý Thuyết Bài 22: Vector Index Cục Bộ (`Offline Indexing` vs `Online Querying`) & Đánh Giá RAG Tự Động (`RAG Eval`)

> **Mục tiêu hiểu bản chất:** Ở Bài 21 (`lesson21.py`), hệ thống RAG đã trả lời được câu hỏi kèm trích dẫn nguồn, nhưng còn **2 lỗ hổng lớn** chưa thể đưa lên Production: (1) mỗi lần chạy lại phải gọi Gemini Embedding lại từ đầu, và (2) chưa có bộ chấm điểm tự động để kiểm chứng mỗi khi chỉnh `chunk_size` hay `min_score`. Bài 22 giải quyết triệt để cả hai vấn đề này.

---

## 1. Tách Đôi `Offline Indexing` & `Online Querying` (Nền Tảng Của Mọi Vector DB)

Nếu bạn có 1 cuốn sổ tay xe 400 trang (~1.000 chunks) và 1.000 tài xế hỏi mỗi ngày:
- **Cách cũ (Bài 21):** Mỗi lần khởi động hoặc mỗi câu hỏi đều chạy `embed_texts(chunks)` → Tốn tiền API gấp 1.000 lần và chờ hàng chục giây!
- **Kiến trúc chuẩn Production:**
  1. **Giai đoạn Offline Indexing (Chỉ chạy 1 lần khi nạp/cập nhật tài liệu):**
     - Cắt văn bản thành `chunks` → Gọi Gemini Embedding **đúng 1 lần** → **Lưu cứng xuống ổ cứng** (`car_manual_chunks.json` cho text + `car_manual_vectors.npy` cho ma trận vector).
  2. **Giai đoạn Online Querying (Lúc user gửi câu hỏi thật):**
     - Nạp thẳng Index từ ổ cứng/RAM (`0 API calls` cho tài liệu!).
     - Chỉ tốn đúng **1 lần gọi Embedding cho câu hỏi ngắn của user**, tính Cosine Similarity trong vài mili-giây rồi gửi Top-K đoạn cho Gemini trả lời.

### Tại sao lưu vector ra file nhị phân `.npy` thay vì lưu chung vào `.json`?
- 1 vector Gemini có `3.072` số thực `float32`.
- Lưu dạng chuỗi trong `.json` (`0.022141287, -0.053276557, ...`) vừa **nặng dung lượng gấp 4–6 lần**, vừa phải parse chữ sang số cực chậm.
- `np.save()` / `np.load()` đọc/ghi thẳng mảng byte nhị phân `float32` vào RAM nhanh hơn hàng trăm lần!
- *(Khi dữ liệu phình lên hàng trăm nghìn → hàng triệu đoạn văn bản, ta nâng cấp file `.npy` lên **Vector Database** chuyên dụng như **FAISS, ChromaDB, Qdrant, pgvector** dùng cấu trúc đồ thị **HNSW** để tìm gần đúng siêu tốc $O(\log N)$ thay vì duyệt từng dòng $O(N)$.)*

---

## 2. Đánh Giá Hệ Thống RAG Tự Động (`RAG Evaluation`)

Trong kỹ thuật AI thực chiến, **không bao giờ đánh giá RAG bằng cảm tính** (*"thử hỏi 1 câu thấy có vẻ ổn"*). Mỗi lần bạn chỉnh `chunk_size`, `overlap`, `min_score`, hay đổi `system_prompt`, bạn phải chạy một **Golden Evaluation Set (`EVAL_CASES`)** gồm 2 nhóm bắt buộc:

1. **Nhóm Trong phạm vi (`In-Domain`, `should_answer = True`):**
   - Kiểm tra 2 điều kiện đồng thời:
     - **Retrieval đúng:** Tìm ra ít nhất 1 đoạn nguồn (`len(sources) > 0`).
     - **Generation trung thực (*Faithfulness / Correctness*):** Câu trả lời của Gemini có chứa thông tin/con số chính xác từ sổ tay (VD: `"80"` km/h, `"30 phút"`, `"Auto Hold"`).
2. **Nhóm Ngoài phạm vi (`Out-of-Domain`, `should_answer = False`):**
   - VD: *"Cách nấu bún bò Huế"*, *"Giá Bitcoin hôm nay?"*.
   - Kiểm tra **Khả năng từ chối (*Refusal Accuracy*)**: Bắt buộc hệ thống trả về `sources == []` và từ chối lịch sự — không tự bịa kiến thức bên ngoài!

---

## 3. Trade-off Của Ngưỡng `min_score` (Liên Hệ Trực Tiếp `Precision` vs `Recall` Ngày 02!)

- **Đặt `min_score` quá cao (VD `0.85`):** Chặn sạch 100% câu ngoài lề, nhưng **chặn oan luôn câu hỏi thật của tài xế** vì cách diễn đạt hơi khác sổ tay → **Tụt Recall!**
- **Đặt `min_score` quá thấp (VD `0.20`):** Không bỏ sót câu hỏi thật, nhưng câu *"Giá Bitcoin hôm nay?"* vẫn lọt lưới vớt bừa 1 đoạn sổ tay ô tô gửi cho LLM → **Tụt Precision & dễ gây ảo giác!**
- **Cách tối ưu chuẩn kỹ sư:** Dùng chính hàm `evaluate_rag_pipeline` ở Bài 22 đo thực nghiệm để chọn ngưỡng `min_score` cân bằng đẹp nhất (đạt `100%` trên cả câu trong phạm vi lẫn câu ngoài lề).
