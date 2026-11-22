# Danh Mục Toàn Bộ Nội Dung Trang Google Sites — TS. Bùi Thanh Hùng

Tài liệu này tổng hợp đầy đủ dữ liệu thu thập từ toàn bộ **7 trang điều hướng** của website `https://sites.google.com/site/hungthanhbui1980` (bao gồm trang `my-to-do`) cùng các trang Lab và kho mã nguồn GitHub liên kết.

---

## 1. Sơ Đồ 7 Trang Trên Website (`sites.google.com/site/hungthanhbui1980`)

> **Lưu ý cấu trúc:** Website được nâng cấp từ Google Sites cũ (Classic) sang Google Sites mới, nên tên đường dẫn (slug) vẫn giữ tên cũ dù tiêu đề trang đã đổi:

| STT | Tên Menu trên Site | URL thực tế | Tóm tắt nội dung chính |
| :--- | :--- | :--- | :--- |
| 1 | **Home** | `.../home` | Thông tin chức danh tại Bộ môn Khoa học Dữ liệu (Khoa CNTT, ĐH Công nghiệp TP.HCM - IUH), email, hướng nghiên cứu chính. |
| 2 | **Bio** | `.../research-journal` | Quá trình công tác (IUH, TDTU, TDMU, FPTU, ĐH CSND), quá trình đào tạo (Bách Khoa HN, ThS & TS tại JAIST Nhật Bản), hơn 20 giải thưởng nghiên cứu khoa học (1995–2025). |
| 3 | **Research** | `.../my-to-do` | **Trang trọng tâm (~85.000 ký tự):** Danh sách đầy đủ 35+ bài báo tạp chí quốc tế/quốc gia (2013–2026), 11 đầu sách biên tập, 34 chương sách, 41 bài hội nghị quốc tế, 29 bài hội nghị trong nước, 5 bằng sáng chế, 4 đề tài nghiên cứu, ban biên tập & ~60 bài keynote/invited talks. |
| 4 | **Teaching** | `.../project` | Danh mục 25 học phần giảng dạy bậc Đại học & Cao học tại IUH, TDTU, TDMU, FPTU, ĐHSP, ĐHKHTN. |
| 5 | **Student** | `.../advisor-to-do` | Danh sách nghiên cứu sinh Tiến sĩ, học viên Cao học, sinh viên Khóa luận/NCKH (2016–2026), thực tập sinh quốc tế (Pháp, Nhật, Ấn Độ), đội tuyển Olympic/ACM-ICPC, kèm link GitHub và YouTube demo sản phẩm sinh viên. |
| 6 | **Funding** | `.../weekly-report` | 9 nguồn tài trợ nghiên cứu: VINIF (Vingroup), NAFOSTED, TDMU, PPU, JAIST Foundation, Đề án 322 Chính phủ VN. |
| 7 | **Contact** | `.../contact` | Liên hệ, hồ sơ học thuật (Google Scholar `kbucD0EAAAAJ`, ORCID `0000-0002-9400-7582`, Scopus `58409698900`, DBLP) và link các phòng Lab (`daailabtdmu`, `ailab-tdtu`). |

---

## 2. Kho Mã Nguồn GitHub Liên Kết Từ Nhóm Nghiên Cứu Của Thầy

Đây là các kho code thực tế của học viên/sinh viên làm dưới sự hướng dẫn của thầy:

1. **KGRec (PLOS ONE 2026 — Knowledge Graph Recommender System):**
   - Link: `https://github.com/TrinhDuongHoan/KGREC_implementation`
   - Công nghệ: Python 3.10+, PyTorch, cấu trúc chuẩn research (`configs/` YAML, `loaders/`, `models/KGRec.py`, so sánh trực tiếp với `KGAT`, `KGNN_LS`, `CKAN`, `AMIE`, `MCRec` trên 4 tập dữ liệu lớn: `Amazon-Book`, `Last-FM`, `MovieLens-1M`, `Yelp2018`).
2. **ExVQA (Computers & Electrical Engineering 2025 — Visual Question Answering):**
   - Link: `https://github.com/Hovohoangduy/ExVQA`
   - Công nghệ: PyTorch + HuggingFace (`google/siglip-base-patch16-224` + `EleutherAI/gpt-neo-125m`) + `StackedAttentionNets` (4 tầng) + `xLSTM` (`mLSTM`/`sLSTM` với `CausalConv1D`).
3. **3Br-MGD (Scientific Reports 2026 — Few-shot Meta-Learning):**
   - Link: `https://github.com/ThaoNguyen2368/3Br-MGD`
   - Công nghệ: Python 3.11, PyTorch 2.3, PyTorch Geometric 2.7, RDKit; kiến trúc 3 nhánh (`FingerprintMLP`, `GCNEncoder`, `SequenceDCNN`) kết hợp Prototypical Meta-learning với tập episode cố định `seed=42`.
4. **ImageCaption (MTFIC 2025 — Fashion Image Captioning):**
   - Link trên trang Student: `https://github.com/huyquoc22/ImageCaption` *(Hiện tại repo này đang để Private hoặc đã gỡ - HTTP 404)*.

---

## 3. Toàn Bộ 35 Bài Báo Tạp Chí Khoa Học Trên Trang `/my-to-do` (2013 – 2026)

### Nhóm A: Multimodal AI, Visual Question Answering (VQA), OCR Chứng Từ & Image Captioning
1. **(2026) Global-Local Hybrid VLM + XAI:** Lang Hoang Son, Bui Thanh Hung — *A global-local hybrid vision-language framework for interpretable grapevine disease diagnosis*, **Discover Artificial Intelligence** 6:1389. (`https://doi.org/10.1007/s44163-026-02463-x`) — **[Đã tải PDF trong `papers_pdf/`]**
2. **(2026) Interactive VQA:** Nguyen Ha Manh Khang, Nguyen Tuan Anh, Nguyen Minh Hoang, Bui Thanh Hung — *Improved interactivity and automated response for visual question answering*, **IJEECS** 42(3), pp. 742–752. (`https://doi.org/10.11591/ijeecs.v42.i3.pp742-752`)
3. **(2025) ExVQA:** Bui Thanh Hung, Ho Vo Hoang Duy — *ExVQA: A novel Stacked Attention Networks with Extended Long Short-Term Memory Model for Visual Question Answering*, **Computers and Electrical Engineering** 126:110439. (`https://doi.org/10.1016/j.compeleceng.2025.110439`)
4. **(2025) MTFIC:** Bui Thanh Hung, Vo Quoc Huy — *MTFIC: enhanced fashion image captioning via multi-transformer architecture with contrastive and bidirectional encodings*, **The Visual Computer**. (`https://doi.org/10.1007/s00371-025-04072-8`)
5. **(2024) ConBGAT (Scanned Document IE):** Ho Vo Hoang Duy, Vo Quoc Huy, Hung Bui Thanh — *ConBGAT: A novel model combining convolutional neural networks, transformer and graph attention network for information extraction from scanned image*, **PeerJ Computer Science** 10:e2536. (`https://doi.org/10.7717/peerj-cs.2536`)
6. **(2024) Multimodal Sentiment:** Bui Thanh Hung, Nguyen Hoang Minh Thu — *Novelty Fused Image and Text Models based on Deep Neural Network and Transformer for Multimodal Sentiment Analysis*, **Multimedia Tools and Applications**. (`https://doi.org/10.1007/s11042-023-18105-8`)
7. **(2023) CBIR:** Bui Thanh Hung, Sabyasachi Pramanik — *Content-Based Image Retrieval using Multi Deep Neural Networks and K-Nearest Neighbor Approaches*, **Research Square**. (`https://doi.org/10.21203/rs.3.rs-1425795/v1`)

### Nhóm B: Explainable AI (XAI), Recommender Systems & Knowledge Graph
8. **(2026) Twin Systems XAI:** Trinh Nguyen Hoang Vu, Hung Bui Thanh — *A letter from the black box: interpreting artificial intelligence through example-based Twin systems*, **PeerJ Computer Science**. (`https://doi.org/10.7717/peerj-cs.3943`)
9. **(2026) KGRec:** Trinh Duong Hoan, Bui Thanh Hung — *KGRec: a knowledge graph attention-based model for recommender system*, **PLOS ONE** 21(3):e0344585. (`https://doi.org/10.1371/journal.pone.0344585`)
10. **(2025) DCARES:** Bui Thanh Hung, Nguyen Van Phuc Nhan, Nguyen Tien Sy — *DCARES: deep convolutional neural network with neural-based optimization for image-based product recommender system*, **Multimedia Tools and Applications**. (`https://link.springer.com/article/10.1007/s11042-025-20655-y`)

### Nhóm C: NLP, Tiếng Việt, Phân Tích Cảm Xúc, Tuyển Dụng & Nhận Diện Giọng Nói
11. **(2023) GARN Twitter Sentiment:** Nikhat Parveen, Prasun Chakrabarti, Bui Thanh Hung, Amjan Shaik — *Twitter Sentiment Analysis using Hybrid Gated Attention Recurrent Network*, **Journal of Big Data** 10:50. (`https://doi.org/10.1186/s40537-023-00726-3`)
12. **(2022) Vietnamese Voice DL:** Bui Thanh Hung — *Vietnamese Voice Classification based on Deep Learning Approach*, **IJMLNCE** 4(4), pp. 171–180. (`https://mlnce.net/index.php/Home/article/view/171`)
13. **(2022) Recruitment ML (EN):** Bui Thanh Hung — *Assessment of Recruitment Records using Machine Learning*, **IJMLNCE** 4(4), pp. 143–151. (`https://mlnce.net/index.php/Home/article/view/170`)
14. **(2020) Recruitment ML (VN):** Bùi Thanh Hùng — *Đánh giá hồ sơ tuyển dụng bằng Học máy*, **Tạp chí Khoa học ĐH Thủ Dầu Một** 49(6), tr. 3–13. (`https://vjol.info.vn/index.php/tdm/article/view/53527`)
15. **(2019) Vietnamese QA & Diacritics:** Bui Thanh Hung — *Integrating Diacritics Restoration and Question Classification into Vietnamese Question Answering System*, **ASTESJ** 4(5), pp. 207–212. (`https://doi.org/10.25046/aj040526`)
16. **(2013) Legal Sentence MT (JAIST):** Bui Thanh Hung, Nguyen Le Minh, Akira Shimazu — *Translating Legal Sentence by Segmentation and Rule Selection*, **IJNLC** 2(4), pp. 35–54. (`https://www.doi.org/10.5121/ijnlc.2013.2403`) — **[Đã tải PDF trong `papers_pdf/`]**

### Nhóm D: Few-Shot Meta-Learning, Y Sinh & Chẩn Đoán Y Tế
17. **(2026) 3Br-MGD Few-Shot:** Nguyen Thi Phuong Thao, Bui Thanh Hung — *3Br-MGD: few-shot toxicity prediction with a three-branch deep encoder and meta-learning framework*, **Scientific Reports** 16:31390. (`https://doi.org/10.1038/s41598-026-60814-1`)
18. **(2024) Cancer Prediction ML:** G S Pradeep Ghantasala, Bui Thanh Hung et al. — *Artificial Intelligence based Machine Learning Algorithm for Prediction of Cancer in Female Anatomy*, **Multimedia Tools and Applications**. (`https://doi.org/10.1007/s11042-024-19655-1`)
19. **(2023) Skin Cancer AI:** B. Prasanalakshmi et al., Hung Bui Thanh — *A Novel Artificial Intelligence-Based Predictive Analytics Technique to Detect Skin Cancer*, **PeerJ CS** 1387.
20. **(2023) Image Segmentation DL:** Pellakuri Vidyullatha, Bui Thanh Hung, Prasun Chakrabarti — *An Efficient Data Analytics and Optimized Algorithm for Enhancing the Performance of Image Segmentation Using Deep Learning Model*, **IJRITCC** 11(5), pp. 48–54.
21. **(2023) Segmentation & Classification Survey:** G Manikandan, Bui Thanh Hung et al. — *Enhanced Ai-Based Machine Learning Model for an Accurate Segmentation and Classification Methods*, **IJRITCC** 11(3s), pp. 11–18.
22. **(2023) LC-MS/MS Dacomitinib:** Tinku Gupta et al., Bui Thanh Hung — **Separation Science Plus**. (`https://doi.org/10.1002/sscp.202300131`)
23. **(2021) Osteoporosis Expert Systems:** U.M Prakash et al., Bui Thanh Hung — *4x- Expert Systems for Early Predication of Osteoporosis Using multi-model Algorithms*, **Measurement** 180. (`https://doi.org/10.1016/j.measurement.2021.109543`)
24. **(2021) Covid-19 Review:** Srinivasakumar KP, Bui Thanh Hung, Prasun Chakrabarti — **IJMSDR** 5(5), pp. 32–50.

### Nhóm E: Mobile Edge Federated Learning, IoT, An Ninh Mạng, Blockchain & Điều Khiển
25. **(2026) IoT Healthcare Blockchain Security:** Jyoti Parashar, Bui Thanh Hung et al. — **Array** 100759. (`https://doi.org/10.1016/j.array.2026.100759`)
26. **(2025) SALF Academic Blockchain:** Mustafizul Haque, Bui Thanh Hung et al. — *SALF: A Blockchain-Based Framework for Scalable Academic Credential Management and Institutional Governance*, **JASTT** 6(2), pp. 203–218. (`https://doi.org/10.38094/jastt62295`) — **[Đã tải PDF trong `papers_pdf/`]**
27. **(2024) Mobile Edge Federated Learning:** Long Tan Le et al., Bui Thanh Hung, Tuan Anh Le — *Distributionally Robust Federated Learning for Mobile Edge Networks*, **Mobile Networks and Applications**. (`https://doi.org/10.1007/s11036-024-02316-w`)
28. **(2024) SDN Intrusion Detection:** Panem Charanarur, Bui Thanh Hung et al. — *Design optimization-based software-defined networking scheme for detecting and preventing attacks*, **Multimedia Tools and Applications**. (`https://doi.org/10.1007/s11042-024-18466-8`)
29. **(2023) Network Intrusion DL:** S. Siva Shankar, Bui Thanh Hung et al. — **Education and Information Technologies** 29, pp. 3859–3883. (`https://doi.org/10.1007/s10639-023-11885-4`)
30. **(2023) DSVM Motor Control:** Md Asif Hussain et al., Bui Thanh Hung — *DSVM-Based Model-Free Predictive Current Control of an Induction Motor*, **Energies** 16(15):5657. (`https://doi.org/10.3390/en16155657`)
31. **(2023) Remote Health IoT:** Suresh Kallam, Bui Thanh Hung et al. — **IJRITCC** 11(5), pp. 42–47.
32. **(2023) MT-ECC + DNN-GO Security:** Amjan Shaik, Bui Thanh Hung et al. — *A Novel Intelligent AI-based Security to Enhance the Data Communication*, **IJISAE** 11(5s), pp. 400–412. — **[Đã tải PDF trong `papers_pdf/`]**
33. **(2022) Wireless RPA ML:** C. Murugamani et al., Bui Thanh Hung — **Wireless Communications and Mobile Computing**. (`https://doi.org/10.1155/2022/4723138`)
34. **(2021) IoT Smart Waste Industry 4.0:** M. Abul Hasan et al., Bui Thanh Hung — **JEPE** 22(6), pp. 2368–2378.
35. **(2015) E-learning System:** Bui Thanh Hung — *Pilot model online training system E-learning in the People's Police University*, Tạp chí KHGD CSND số 68.

---

## 4. Các Môn Giảng Dạy & Đề Tài Lớn Của Thầy

### Các môn cốt lõi thầy trực tiếp dạy (Trang `Teaching`)
- **Cao học (Master):** *Advanced Artificial Intelligence* (IUH), *Natural Language Processing* (TDTU, TDMU), *Mining Massive Datasets* (TDTU), *Text and Web Mining* (TDMU), *Programming for Data Analytics* (TDMU), *Advanced Algorithms* (ĐHSP).
- **Đại học (Undergraduate):** *Introduction to Data Science*, *New Technologies in IT Application Development*, *Python for Data Science / ML / DL*, *Introduction to AI*, *Data Structures & Algorithms*, *OOP*, *Capstone Project*.

### Các đề tài tài trợ & Bằng sáng chế tiêu biểu
- **Quỹ VINIF (Vingroup Innovation Foundation, 2020~):** Thành viên chủ chốt đề tài tối ưu hóa sản xuất tích hợp tri thức vật lý (*Physics-Informed Manufacturing Optimization*).
- **Quỹ NAFOSTED (2019~):** Nghiên cứu viên chính đề tài ứng dụng Học máy trong truyền dẫn dữ liệu đầu-cuối (*End-to-end Data Transmission ML*).
- **Đề tài cấp Trường TDMU (2019):** Chủ nhiệm đề tài Phân tích quan điểm/cảm xúc tiếng Việt (*Sentiment Analysis*).
- **Bằng sáng chế được cấp (L-106149/2021):** *Ref-Cite-Authenticator* (Xác thực trích dẫn tài liệu khoa học) cùng 4 hồ sơ sáng chế phân tích y sinh và nhận thức.
