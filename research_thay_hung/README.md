# Kho Tài Liệu Nghiên Cứu & Định Hướng Dự Án AI — TS. Bùi Thanh Hùng

Thư mục này lưu trữ toàn bộ dữ liệu thu thập, phân tích cơ chế từng công trình khoa học và đề xuất dự án thực chiến dựa trên trang Google Sites chính thức của **TS. Bùi Thanh Hùng**:
- **URL gốc thầy gửi:** `https://sites.google.com/site/hungthanhbui1980/my-to-do` (Trang **Research** chính thức của thầy — giữ lại đường dẫn `/my-to-do` từ thời Google Sites phiên bản cũ).

---

## 1. Chân Dung Học Thuật & "Gu" Nghiên Cứu Của TS. Bùi Thanh Hùng

Hiểu rõ nền tảng và phong cách làm việc của thầy sẽ giúp bạn định vị dự án trúng đích ngay từ lần trao đổi đầu tiên:

- **Học vấn nền tảng cực kỳ bài bản:**
  - Kỹ sư CNTT — **ĐH Bách Khoa Hà Nội** (1998–2003, tốt nghiệp Top 5%).
  - Thạc sĩ (2008–2010) & **Tiến sĩ Khoa học Thông tin (2010–2013)** tại **JAIST** (*Japan Advanced Institute of Science and Technology*, Nhật Bản) — chuyên sâu về Xử lý Ngôn ngữ Tự nhiên (NLP), Phân tích cú pháp câu pháp lý và Dịch máy (Machine Translation).
- **Vị trí hiện tại:**
  - **Trưởng Bộ môn Khoa học Dữ liệu (Head of Data Science Department)**, Khoa CNTT, Đại học Công nghiệp TP.HCM (**IUH**) (từ 12/2025; công tác tại IUH từ 10/2022).
  - Giảng viên thỉnh giảng/cơ hữu nhiều năm tại **ĐH FPT**, từng làm Giám đốc AI Lab tại **ĐH Tôn Đức Thắng (TDTU)** và Giám đốc DAAI Lab tại **ĐH Thủ Dầu Một (TDMU)**.
  - Thành viên Ban biên tập (Editorial Board) của **PLOS ONE**, **Discover Artificial Intelligence**, **Discover Computing**, **Discover Robotics** (Springer Nature).

---

## 2. Sáu Trụ Cột Nghiên Cứu Chủ Lực (Đặc biệt giai đoạn 2024 – 2026)

Trên trang `/my-to-do`, thầy nêu rõ 3 chủ đề trọng tâm gần đây (**Recent Subjects**):
1. **Visual Question Answering (VQA) & Multimodal Vision-Language Models (VLM)**
2. **Recommender Systems (Hệ thống gợi ý kết hợp Đồ thị Tri thức & Ảnh)**
3. **Explainable Artificial Intelligence (XAI — AI có khả năng giải thích hộp đen)**

Khi đọc sâu vào toàn bộ các bài báo và GitHub của nhóm nghiên cứu thầy (2013–2026), có **6 mô-típ kỹ thuật cốt lõi** lặp đi lặp lại:

| Trụ cột | Công trình tiêu biểu của thầy | Đặc trưng cơ chế kỹ thuật |
| :--- | :--- | :--- |
| **1. Trích xuất thông tin chứng từ / hóa đơn scan** | **ConBGAT** (*PeerJ CS*, 2024) | Kết hợp **OCR Bounding Box + ResNet50 (Ảnh) + DistilBERT (Chữ) + Graph Attention Network (GAT)** theo tọa độ không gian 4 hướng $(D_L, D_T, D_R, D_B)$ trên tập hóa đơn `SROIE`, `CORD`. |
| **2. Hỏi đáp thị giác (VQA) & Đa phương thức (VLM)** | **ExVQA** (2025), **Global-Local VLM** (*Discover AI*, 2026), **Interactive VQA** (2026) | Không đưa mỗi ảnh thô vào model: luôn kết hợp **Global View + Local Auto-Crop Patch**, dùng **Stacked Attention / xLSTM** hoặc **Clarification Question** (hỏi lại khi ảnh/câu hỏi mơ hồ). |
| **3. AI có khả năng giải thích (Explainable AI - XAI)** | **Global-Local VLM XAI** (2026), **Twin Systems XAI** (*PeerJ CS*, 2026) | Mở "hộp đen" AI bằng **Cross-Attention Heatmap** (chỉ rõ AI nhìn vào vùng nào trên ảnh) và **Example-based Twin Systems** (đối chiếu ca tương đồng trong lịch sử để giải thích lý do). |
| **4. Hệ thống gợi ý & Đồ thị tri thức (Knowledge Graph)** | **KGRec** (*PLOS ONE*, 2026), **DCARES** (2025) | Xây dựng **Collaborative Knowledge Graph**, nhúng quan hệ bằng **TransR** và lan truyền **Bi-Interaction Graph Attention** tối ưu bằng hàm loss **BPR**. |
| **5. Xử lý ngôn ngữ & tiếng nói tiếng Việt** | **Legal Segmentation** (2013), **Vietnamese QA & Diacritics** (2019), **VN Voice** (2022) | Khôi phục dấu tiếng Việt, phân loại câu hỏi, tách cấu trúc câu phức thành `[Chủ đề] - [Điều kiện] - [Hệ quả]` bằng CRF/MaxEnt, phân loại giọng nói qua Mel-Spectrogram. |
| **6. Hybrid Edge/Security & Đánh giá dữ liệu** | **Robust Federated Learning** (2024), **3Br-MGD** (2026), **SALF** (2025) | Học liên kết trên mạng biên di động (Mobile Edge), học ít mẫu (Few-shot Meta-learning 3 nhánh), chấm điểm chất lượng bản ghi bằng công thức toán tường minh. |

> **Nhận xét quan trọng trước khi đem dự án trình thầy:**
> Thầy Hùng là người làm nghiên cứu thực nghiệm rất kỹ. Nếu bạn chỉ mang tới một app "gọi thẳng Gemini/GPT API rồi in chữ ra màn hình", thầy sẽ đánh giá là **chưa có hàm lượng kỹ thuật AI (chỉ là API Wrapper)**.
> Ngược lại, nếu dự án của bạn có **Pipeline lai (Hybrid Pipeline)**: *Tiền xử lý Global-Local / OCR không gian trên Android Edge -> Chuẩn hóa tiếng Việt không dấu -> Truy xuất RAG / Twin-case có ngưỡng lọc chống bịa -> Trả lời kèm Giải thích XAI (khoanh vùng bằng chứng trên ảnh + trích dẫn nguồn)* + **có bảng đo lường thực nghiệm (Accuracy/F1/Latency)**, thầy sẽ cực kỳ ấn tượng!

---

## 3. Cấu Trúc Thư Mục Này

1. [01_DANH_MUC_TOAN_BO_SITE_VA_CONG_BO.md](01_DANH_MUC_TOAN_BO_SITE_VA_CONG_BO.md): Bản thu thập toàn bộ 7 trang trên Google Sites của thầy (Home, Bio, Research `/my-to-do`, Teaching, Student, Funding, Contact), danh sách 35+ bài báo tạp chí quốc tế, các môn giảng dạy và link GitHub code của học trò thầy.
2. [02_GIAI_MA_CO_CHE_TUNG_TAI_LIEU.md](02_GIAI_MA_CO_CHE_TUNG_TAI_LIEU.md): **Tài liệu luyện AI cốt lõi** — mổ xẻ chi tiết từng bài báo và source code GitHub của thầy (từ kiến trúc, công thức toán, luồng tensor cho đến liên hệ thực tế với Python/Kotlin).
3. [03_DE_XUAT_DU_AN_AI_TRINH_THAY.md](03_DE_XUAT_DU_AN_AI_TRINH_THAY.md): Thiết kế chi tiết các phương án dự án AI kết hợp thế mạnh **Android + Fintech/Ô tô** của bạn với **đúng hướng nghiên cứu của thầy**, kèm sơ đồ kiến trúc và kịch bản trình bày với thầy.
4. `papers_pdf/`: Lưu trữ các bản PDF bài báo toàn văn Open-Access tải trực tiếp từ liên kết trên site của thầy:
   - `2013_IJNLC_Legal_Sentence_Segmentation_MaxEnt_Rule_Selection.pdf`
   - `2023_IJISAE_AI_Security_MTECC_DNN_Gazelle_Optimization.pdf`
   - `2025_JASTT_SALF_Blockchain_Academic_Ledger_Incentive_Model.pdf`
   - `2026_DiscoverAI_Global_Local_Hybrid_VLM_Intrinsic_XAI.pdf`
