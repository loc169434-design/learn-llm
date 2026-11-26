import json
from pathlib import Path

import numpy as np
from pydantic import BaseModel

from lesson20 import embed_texts
from lesson21 import RAW_MANUAL_TEXT, ask_rag, chunk_text

INDEX_DIR = Path(__file__).resolve().parent / "vector_store"
CHUNKS_PATH = INDEX_DIR / "car_manual_chunks.json"
VECTORS_PATH = INDEX_DIR / "car_manual_vectors.npy"

# Tập câu hỏi kiểm thử RAG tự động (Evaluation Set)
# - `should_answer=True`: câu hỏi CÓ trong sổ tay xe, bắt buộc trả lời chứa ít nhất 1 từ khóa đúng và có trích dẫn nguồn.
# - `should_answer=False`: câu hỏi NGOÀI LỀ, bắt buộc hệ thống từ chối (`sources == []`) để chống bịa đặt!
EVAL_CASES = [
    {
        "question": "Lốp dự phòng nhỏ chạy tối đa bao nhiêu km/h?",
        "should_answer": True,
        "expected_keywords": ["80", "100"],
    },
    {
        "question": "Khi máy quá nhiệt báo đỏ thì chờ bao lâu mới mở nắp két nước?",
        "should_answer": True,
        "expected_keywords": ["30 phút", "30"],
    },
    {
        "question": "Vào máy rửa xe tự động cần tắt tính năng gì?",
        "should_answer": True,
        "expected_keywords": ["auto hold", "n"],
    },
    {
        "question": "Cách làm món bún bò Huế ngon tại nhà?",
        "should_answer": False,
        "expected_keywords": [],
    },
    {
        "question": "Giá Bitcoin hôm nay tăng hay giảm?",
        "should_answer": False,
        "expected_keywords": [],
    },
]


def save_vector_index(chunks: list[str], vectors: list[np.ndarray]) -> None:
    """
    TODO 1: Lưu danh sách đoạn văn (chunks) ra JSON và ma trận vector ra file nhị phân `.npy`
    để lần sau chạy lại KHÔNG phải gọi lại Gemini Embedding API (tiết kiệm tiền & tốc độ tức thì).

    Yêu cầu:
    1. Tạo thư mục `INDEX_DIR` nếu chưa tồn tại: `INDEX_DIR.mkdir(parents=True, exist_ok=True)`.
    2. Lưu `chunks` vào `CHUNKS_PATH` bằng `json.dumps(..., ensure_ascii=False, indent=2)`
       và `CHUNKS_PATH.write_text(..., encoding="utf-8")`.
    3. Xếp chồng `vectors` thành 1 ma trận 2 chiều `np.vstack(vectors)` và lưu xuống `VECTORS_PATH`
       bằng `np.save(VECTORS_PATH, matrix)`.
    """
    if CHUNKS_PATH.exists():
        CHUNKS_PATH.unlink()
    else:
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_PATH.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    matrix = np.vstack(vectors)
    np.save(VECTORS_PATH, matrix)


def load_or_build_vector_index(raw_text: str) -> tuple[list[str], list[np.ndarray]]:
    """
    TODO 2: Nạp Vector Index từ đĩa nếu đã có sẵn (Cache Hit); ngược lại mới gọi Gemini embed và lưu xuống đĩa.

    Yêu cầu:
    1. Kiểm tra nếu `CHUNKS_PATH.exists() and VECTORS_PATH.exists()`:
       - Đọc `chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))`
       - Đọc ma trận `matrix = np.load(VECTORS_PATH)` rồi chuyển thành `[row for row in matrix]`
       - In ra `"⚡ Đã nạp Vector Index từ ổ cứng (0 API calls)!"` và trả về `(chunks, vectors)`.
    2. Nếu chưa tồn tại trên đĩa:
       - Cắt `chunks = chunk_text(raw_text, chunk_size=260, overlap=50)`
       - Gọi `vectors = embed_texts(chunks)`
       - Gọi `save_vector_index(chunks, vectors)`
       - In ra `"🌐 Đã gọi Gemini Embedding và lưu Index xuống ổ cứng!"` và trả về `(chunks, vectors)`.
    """
    if CHUNKS_PATH.exists() & VECTORS_PATH.exists():
        chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
        matrix = np.load(VECTORS_PATH)
        print("⚡ Đã nạp Vector Index từ ổ cứng (0 API calls)!")
        return chunks, matrix
    else:
        chunks = chunk_text(raw_text, chunk_size=260, overlap=50)
        vectors = embed_texts(chunks)
        save_vector_index(chunks, vectors)
        print("🌐 Đã gọi Gemini Embedding và lưu Index xuống ổ cứng!")
        return chunks, vectors


class Detail(BaseModel):
    question: str
    answer: str
    should_answer: bool


def evaluate_rag_pipeline(
        eval_cases: list[dict],
        chunks: list[str],
        vectors: list[np.ndarray],
) -> dict:
    """
    TODO 3: Chạy chấm điểm tự động (RAG Evaluation) trên toàn bộ `eval_cases`.

    Cách chấm từng câu hỏi `case`:
    - Gọi `result = ask_rag(case["question"], chunks, vectors)`
    - Lấy `answer_lower = result["answer"].lower()` và `has_sources = len(result["sources"]) > 0`
    - Nếu `case["should_answer"]` là `True`:
        Pass khi `has_sources` là `True` VÀ có ít nhất 1 từ khóa trong `case["expected_keywords"]`
        nằm trong `answer_lower` (gợi ý: `any(kw.lower() in answer_lower for kw in case["expected_keywords"])`).
    - Nếu `case["should_answer"]` là `False` (câu ngoài lề — test chống bịa):
        Pass khi `not has_sources` (hệ thống từ chối trả lời, không lấy bừa nguồn!).
    - Đếm số câu pass (`passed_count`) và trả về dict:
      `{"total": len(eval_cases), "passed": passed_count, "pass_rate": passed_count / len(eval_cases), "details": details}`
      (mỗi phần tử trong `details` gồm `{"question": ..., "passed": ..., "answer": ...}`).
    """
    passed_count = 0
    list_details: list[dict] = []

    for eval_case in eval_cases:
        result = ask_rag(eval_case["question"], chunks, vectors)
        answer_lower = result["answer"].lower()
        has_sources = len(result["sources"]) > 0
        if eval_case["should_answer"]:
            has_keyword = any(
                kw.lower() in answer_lower for kw in eval_case["expected_keywords"]
            )
            is_passed = has_sources and has_keyword
        else:
            is_passed = not has_sources
        if is_passed:
            passed_count += 1
        list_details.append({
            "question": eval_case["question"],
            "passed": is_passed,
            "answer": result["answer"],
        })
    return {
        "total": len(eval_cases),
        "passed": passed_count,
        "pass_rate": passed_count / len(eval_cases),
        "details": list_details,
    }

    raise NotImplementedError("Hãy hoàn thiện TODO 3")


if __name__ == "__main__":
    chunks, vectors = load_or_build_vector_index(RAW_MANUAL_TEXT)
    print(f"✓ Pass TODO 1 & 2 — Có {len(chunks)} chunks, vector dim = {vectors[0].shape}")

    report = evaluate_rag_pipeline(EVAL_CASES, chunks, vectors)
    print(f"\n✓ Pass TODO 3 — RAG Eval Score: {report['passed']}/{report['total']} ({report['pass_rate']:.0%})\n")
    for item in report["details"]:
        icon = "✅" if item["passed"] else "❌"
        print(f"{icon} Q: {item['question']}")
        print(f"   A: {item['answer']}\n")
