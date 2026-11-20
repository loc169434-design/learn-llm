import os

import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"

# Giả lập các đoạn trích từ Sổ tay Hướng dẫn sử dụng Ô tô
CAR_MANUAL_DOCS = [
    {
        "id": "doc_tpms",
        "title": "Đèn cảnh báo áp suất lốp (TPMS)",
        "content": "Đèn màu vàng hình mặt cắt lốp xe có dấu chấm than sáng lên khi một hoặc nhiều bánh xe bị non hơi, rò rỉ van hoặc chênh lệch áp suất quá 20%. Hãy tấp vào lề an toàn và bơm lại đúng chuẩn 2.2 - 2.4 bar.",
    },
    {
        "id": "doc_check_engine",
        "title": "Đèn báo lỗi động cơ (Check Engine)",
        "content": "Biểu tượng động cơ màu vàng sáng đứng là lỗi cảm biến khí thải, nắp bình xăng chưa vặn chặt hoặc bugi đánh lửa kém. Nếu đèn nhấp nháy liên tục cần dừng xe gọi cứu hộ để tránh hỏng bộ xúc tác.",
    },
    {
        "id": "doc_oil_change",
        "title": "Lịch thay dầu nhớt và lọc nhớt",
        "content": "Xe chạy điều kiện đô thị Việt Nam nên thay dầu máy định kỳ mỗi 5.000 km hoặc 6 tháng (dầu tổng hợp toàn phần có thể chạy tới 10.000 km). Thay lọc nhớt mỗi 2 lần thay dầu.",
    },
    {
        "id": "doc_battery",
        "title": "Đèn cảnh báo hệ thống sạc ắc quy",
        "content": "Biểu tượng bình ắc quy màu đỏ báo hiệu máy phát điện không sạc được cho ắc quy hoặc dây curoa bị đứt. Cần tắt điều hòa, tắt màn hình giải trí và đưa xe tới gara gần nhất trước khi xe chết máy.",
    },
    {
        "id": "doc_abs",
        "title": "Đèn cảnh báo hệ thống chống bó cứng phanh (ABS)",
        "content": "Khi đèn ABS sáng vàng, phanh thường vẫn hoạt động nhưng tính năng chống trượt bánh khi phanh gấp đã tạm ngưng. Không nên chạy tốc độ cao trên đường trơn trượt.",
    },
]


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    TODO 1: Tính độ tương đồng Cosine giữa 2 vector bằng NumPy.

    Công thức: dot(a, b) / (norm(a) * norm(b))
    Gợi ý:
    - norm_a = np.linalg.norm(vec_a)
    - norm_b = np.linalg.norm(vec_b)
    - Nếu norm_a == 0 or norm_b == 0 -> return 0.0
    - return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
    """
    nom_a = np.linalg.norm(vec_a)
    nom_b = np.linalg.norm(vec_b)
    if nom_a == 0 or nom_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (nom_a * nom_b))

def embed_texts(texts: list[str]) -> list[np.ndarray]:
    """
    TODO 2: Gọi Gemini Embedding API chuyển danh sách văn bản thành danh sách vector NumPy.

    Gợi ý:
    1. Kiểm tra os.getenv("GEMINI_API_KEY"), thiếu -> raise ValueError(...)
    2. client = genai.Client()
    3. response = client.models.embed_content(model=EMBEDDING_MODEL, contents=texts)
    4. return [np.array(item.values, dtype=np.float32) for item in response.embeddings]
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Chưa cấu hình GEMINI_API_KEY")
    client = genai.Client()
    response = client.models.embed_content(model=EMBEDDING_MODEL, contents=texts)
    return [np.array(item.values, dtype=np.float32) for item in response.embeddings]


def semantic_search(query: str, docs: list[dict], top_k: int = 2) -> list[dict]:
    """
    TODO 3: Tìm `top_k` tài liệu giống với câu hỏi `query` nhất theo NGỮ NGHĨA.

    Gợi ý:
    1. Lấy list nội dung từng doc: doc_texts = [f"{d['title']}: {d['content']}" for d in docs]
    2. Tạo vector cho tất cả docs: doc_vectors = embed_texts(doc_texts)
    3. Tạo vector cho câu hỏi: query_vector = embed_texts([query])[0]
    4. Duyệt từng doc + doc_vector, tính score = cosine_similarity(query_vector, doc_vector)
    5. Sắp xếp theo score giảm dần (reverse=True) và trả về top_k phần tử đầu tiên:
       [{"title": ..., "score": round(score, 4), "content": ...}, ...]
    """
    doc_texts = [f"{d['title']}: {d['content']}" for d in docs]
    doc_vectors = embed_texts(doc_texts)
    query_vector = embed_texts([query])[0]
    scored = []
    for doc, vec in zip(docs, doc_vectors):
        score = cosine_similarity(query_vector, vec)
        scored.append({
            "title": doc["title"],
            "score": round(score, 4),
            "content": doc["content"],
        })
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    test_queries = [
        "Bánh xe bị xì hơi non áp suất thì bơm mấy ký?",
        "Đi bao nhiêu cây số thì phải thay dầu máy mới?",
        "Đèn hình bình điện màu đỏ hiện lên trên taplo là hư gì?",
    ]

    for q in test_queries:
        print(f"\n=== CÂU HỎI: {q} ===")
        results = semantic_search(q, CAR_MANUAL_DOCS, top_k=2)
        for rank, item in enumerate(results, start=1):
            print(f"  #{rank} [{item['score']}] {item['title']}")
            print(f"      -> {item['content']}")
