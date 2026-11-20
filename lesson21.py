import os

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

from lesson20 import cosine_similarity, embed_texts

load_dotenv()

CHAT_MODEL = "gemini-flash-lite-latest"

# Văn bản dài trích từ Sổ tay Hướng dẫn Xe (sẽ được cắt nhỏ thành các chunks)
RAW_MANUAL_TEXT = """
CHƯƠNG 1: CHẾ ĐỘ LÁI ECO VÀ SPORT
Chế độ ECO tối ưu mức tiêu hao nhiên liệu bằng cách làm mượt độ nhạy chân ga và chuyển số sớm ở vòng tua thấp, phù hợp khi đi trong phố đông đúc. Chế độ SPORT giữ vòng tua máy cao hơn và tăng độ nhạy vô lăng, phù hợp khi cần vượt xe trên cao tốc.

CHƯƠNG 2: SỬ DỤNG LỐP DỰ PHÒNG TẠM THỜI
Lốp dự phòng kích thước nhỏ (Compact Spare) chỉ dùng để chạy tạm thời tới tiệm vá vỏ gần nhất. Tuyệt đối không chạy quá tốc độ tối đa 80 km/h và không sử dụng liên tục quá 100 km vì có thể làm hỏng hệ thống vi sai và phanh ABS.

CHƯƠNG 3: CẢNH BÁO NHIỆT ĐỘ NƯỚC LÀM MÁT ĐỘNG CƠ
Khi đồng hồ nhiệt độ nước làm mát báo vạch đỏ hoặc đèn hình nhiệt kế đỏ sáng lên, động cơ đang bị quá nhiệt. Tài xế cần tấp xe vào lề an toàn, tắt máy ngay và ĐỢI ít nhất 30 phút cho máy nguội hoàn toàn mới được mở nắp két nước để tránh bị bỏng hơi nước áp suất cao.

CHƯƠNG 4: PHANH TAY ĐIỆN TỬ (EPB) VÀ AUTO HOLD
Khi bật Auto Hold, xe sẽ tự động giữ phanh khi dừng đèn đỏ ở vị trí cần số D mà tài xế không cần giữ chân phanh. Để di chuyển tiếp chỉ cần đạp nhẹ chân ga. Khi đưa xe vào máy rửa xe tự động, phải TẮT Auto Hold và chuyển cần số về N.
""".strip()


def chunk_text(text: str, chunk_size: int = 260, overlap: int = 50) -> list[str]:
    """
    TODO 1: Cắt văn bản dài thành các đoạn nhỏ (chunks) có phần gối đầu (overlap).

    Tại sao cần overlap? Để tránh việc một ý quan trọng bị cắt đứt làm đôi ở ranh giới 2 đoạn!
    Gợi ý:
    1. Chuẩn hóa khoảng trắng: clean_text = " ".join(text.split())
    2. step = chunk_size - overlap (kiểm tra step > 0)
    3. Dùng vòng while start < len(clean_text):
         chunk = clean_text[start : start + chunk_size]
         chunks.append(chunk)
         if start + chunk_size >= len(clean_text): break
         start += step
    4. return chunks
    """
    raise NotImplementedError("Hãy hoàn thiện TODO 1")


def retrieve_relevant_chunks(
    query: str,
    chunks: list[str],
    chunk_vectors: list[np.ndarray],
    top_k: int = 2,
    min_score: float = 0.55,
) -> list[dict]:
    """
    TODO 2: Tìm `top_k` đoạn giống `query` nhất và CHỈ GIỮ các đoạn có score >= min_score.

    Gợi ý:
    1. query_vec = embed_texts([query])[0]
    2. Duyệt idx, (chunk, vec) bằng enumerate(zip(chunks, chunk_vectors)):
       Tính score = cosine_similarity(query_vec, vec).
       Nếu score >= min_score -> thêm {"chunk_id": idx + 1, "score": round(score, 4), "text": chunk}
    3. Sắp xếp giảm dần theo score và trả về [:top_k]
    """
    raise NotImplementedError("Hãy hoàn thiện TODO 2")


def ask_rag(
    question: str,
    chunks: list[str],
    chunk_vectors: list[np.ndarray],
) -> dict:
    """
    TODO 3: Hoàn thiện luồng RAG (Retrieve -> Augment -> Generate).

    Gợi ý:
    1. Retrieve: matches = retrieve_relevant_chunks(question, chunks, chunk_vectors)
    2. Guardrail chống bịa: nếu matches rỗng -> return ngay:
       {"answer": "Xin lỗi, sổ tay xe hiện không có thông tin về vấn đề này.", "sources": []}
    3. Augment: Ghép context:
       context = "\\n\\n".join(f"[Đoạn #{m['chunk_id']}] {m['text']}" for m in matches)
    4. Generate: Gọi Gemini với system_instruction:
       "Bạn là trợ lý sổ tay xe. Chỉ trả lời dựa trên [Đoạn #...] được cung cấp và ghi rõ trích dẫn [Đoạn #...] ở cuối câu."
    5. return {"answer": response.text or "", "sources": matches}
    """
    raise NotImplementedError("Hãy hoàn thiện TODO 3")


if __name__ == "__main__":
    chunks = chunk_text(RAW_MANUAL_TEXT, chunk_size=260, overlap=50)
    print(f"Đã cắt sổ tay thành {len(chunks)} chunks.")
    chunk_vectors = embed_texts(chunks)

    questions = [
        "Đèn báo nhiệt độ nước làm mát sáng đỏ thì có mở nắp két nước châm thêm nước ngay được không?",
        "Đi rửa xe tự động cần tắt tính năng gì?",
        "Giá cổ phiếu Apple hôm nay bao nhiêu?",  # Câu ngoài lề -> test chống bịa!
    ]

    for q in questions:
        print(f"\n=== HỎI: {q} ===")
        result = ask_rag(q, chunks, chunk_vectors)
        print("TRẢ LỜI:", result["answer"])
        print("NGUỒN:", [(s["chunk_id"], s["score"]) for s in result["sources"]])
