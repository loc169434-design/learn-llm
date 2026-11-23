from __future__ import annotations

import math
import re
from collections import Counter
import numpy as np

from dataset_vn_messages import RAW_SAMPLES, export_dataset

# Từ điển bung từ viết tắt & không dấu phổ biến trong tin nhắn Việt Nam
# (Lấy cảm hứng từ bước chuẩn hóa tiếng Việt trong bài ASTESJ 2019 của TS. Bùi Thanh Hùng)
VN_ABBREVIATIONS: dict[str, str] = {
    "bv": "bệnh viện",
    "ck": "chuyển khoản",
    "tk": "tài khoản",
    "sd": "số dư",
    "gd": "giao dịch",
    "km": "khuyến mãi",
    "cccd": "căn cước",
    "oi": "ơi",
    "sot": "sốt",
    "cap": "cấp",
    "cuu": "cứu",
    "gap": "gấp",
    "dua": "đưa",
}

# Các từ xuất hiện tràn lan nhưng không giúp phân biệt nhãn (Stopwords)
VN_STOPWORDS: set[str] = {
    "anh", "em", "ơi", "nhé", "nha", "vậy", "rồi", "là", "của", "và", "cho", "trong", "ở", "có"
}


def normalize_vn_message(text: str) -> list[str]:
    """
    TODO 1: Chuẩn hóa tin nhắn tiếng Việt và tách thành danh sách từ (tokens).

    Các bước thực hiện:
    1. Đổi toàn bộ chuỗi sang chữ thường: text = text.lower()
    2. Giữ lại chữ cái tiếng Việt và chữ số, thay dấu câu bằng khoảng trắng:
       clean = re.sub(r"[^\w\s]", " ", text)
    3. Tách thành list các từ bằng clean.split()
    4. Duyệt qua từng từ `w`:
       - Nếu `w` nằm trong từ điển `VN_ABBREVIATIONS`, thay nó bằng cụm từ đầy đủ
         (lưu ý cụm đầy đủ như "bệnh viện" có 2 từ -> dùng `.split()` để tách ra).
       - Ngược lại giữ nguyên `[w]`.
    5. Lọc bỏ các từ nằm trong tập `VN_STOPWORDS` và trả về `list[str]`.
    """
    expanded: list[str] = []
    text = text.lower()
    clean_text = re.sub(r"[^\w\s]", " ", text)
    list_text = clean_text.split()
    for word in list_text:
        if word in VN_ABBREVIATIONS:
            expanded.extend(VN_ABBREVIATIONS[word].split())
        else:
            expanded.append(word)
    return [w for w in expanded if w not in VN_STOPWORDS]

def compute_tf(tokens: list[str]) -> dict[str, float]:
    """
    TODO 2: Tính Term Frequency (TF) của từng từ trong 1 tin nhắn.

    Công thức: TF(t, d) = (số lần từ t xuất hiện trong tokens) / (tổng số từ trong tokens)
    - Nếu `tokens` rỗng -> trả về `{}`.
    - Gợi ý: Dùng `Counter(tokens)` để đếm nhanh số lần xuất hiện của mỗi từ.
    """
    if not tokens:
        return {}
    total = len(tokens)
    counts = Counter(tokens)
    tf_map: dict[str, float] = {}
    for word, count in counts.items():
        tf_map[word] = count / total
    return tf_map



def compute_idf(tokenized_docs: list[list[str]], vocab: list[str]) -> dict[str, float]:
    """
    TODO 3: Tính Smooth Inverse Document Frequency (IDF) cho từng từ trong bộ từ điển `vocab`.

    Công thức Smooth IDF:
        IDF(t) = math.log((N + 1) / (df_t + 1)) + 1.0

    Trong đó:
    - `N = len(tokenized_docs)` (tổng số tin nhắn trong kho).
    - `df_t`: Số lượng tin nhắn có chứa từ `t` (lưu ý: trong 1 tin nhắn dù từ `t` lặp lại 3 lần
      thì cũng chỉ tính là 1 tin nhắn có chứa nó -> dùng `set(doc)` khi kiểm tra!).
    """
    n = len(tokenized_docs)
    print(f"Số llượng từ n:" ,n)
    doc_sets: list[set[str]] = []
    for doc in tokenized_docs:
        doc_sets.append(set(doc))
    idf_map: dict[str, float] = {}

    for word in vocab:
        df_t = 0
        for doc_set in doc_sets:
            if word in doc_set:
                df_t += 1
        idf_map[word] = math.log((n + 1) / (df_t + 1)) + 1.0

    return idf_map



def build_tfidf_matrix(texts: list[str]) -> tuple[np.ndarray, list[str], dict[str, float]]:
    """Ghép TODO 1 + TODO 2 + TODO 3 thành ma trận số học (N dòng x V cột)."""
    tokenized_docs = [normalize_vn_message(t) for t in texts]
    vocab = sorted({word for doc in tokenized_docs for word in doc})
    word_to_col = {word: idx for idx, word in enumerate(vocab)}

    idf_map = compute_idf(tokenized_docs, vocab)
    matrix = np.zeros((len(texts), len(vocab)), dtype=np.float64)

    for row_idx, tokens in enumerate(tokenized_docs):
        tf_map = compute_tf(tokens)
        for word, tf_val in tf_map.items():
            col_idx = word_to_col[word]
            matrix[row_idx, col_idx] = tf_val * idf_map[word]

    return matrix, vocab, idf_map


def cosine_sim(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    denom = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if denom == 0.0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denom)


if __name__ == "__main__":
    export_dataset()
    texts = [item[0] for item in RAW_SAMPLES]
    labels = [item[1] for item in RAW_SAMPLES]

    # 1. Kiểm tra TODO 1
    sample_tokens = normalize_vn_message("Anh oi con sot cao dua di bv cap cuu gap!")
    assert "anh" not in sample_tokens, "Từ dừng 'anh' phải được lọc bỏ"
    assert "bệnh" in sample_tokens and "viện" in sample_tokens, "Từ 'bv' phải được bung thành 'bệnh', 'viện'"
    print("✓ Pass TODO 1 — Chuẩn hóa tiếng Việt:", sample_tokens)

    # 2. Kiểm tra TODO 2 & TODO 3
    tfidf_matrix, vocab, idf_map = build_tfidf_matrix(texts)
    assert tfidf_matrix.shape[0] == len(texts)
    assert tfidf_matrix.shape[1] == len(vocab)
    print(f"✓ Pass TODO 2 & 3 — Đã số hóa {len(texts)} tin nhắn thành ma trận shape = {tfidf_matrix.shape}")

    # 3. Quan sát bản chất: Top từ khóa có trọng số TF-IDF cao nhất của câu khẩn cấp không dấu (dòng số 1)
    row_vec = tfidf_matrix[1]
    top_indices = np.argsort(row_vec)[::-1][:5]
    print(f"\nTin nhắn gốc: '{texts[1]}'")
    print("Top 5 từ khóa mang năng lượng phân loại lớn nhất:")
    for idx in top_indices:
        if row_vec[idx] > 0:
            print(f"  - '{vocab[idx]}': TF-IDF = {row_vec[idx]:.4f} (IDF = {idf_map[vocab[idx]]:.4f})")

    # 4. Thử nghiệm Twin-Case Search (Tìm tin nhắn lịch sử giống nhất với câu không dấu)
    sims = [cosine_sim(tfidf_matrix[1], tfidf_matrix[i]) for i in range(len(texts))]
    nearest = np.argsort(sims)[::-1][1:4]  # Bỏ qua chính nó ở vị trí 0
    print("\n3 ca lịch sử giống nhất (Twin Examples):")
    for idx in nearest:
        print(f"  [{labels[idx]}] (score={sims[idx]:.3f}): {texts[idx]}")
