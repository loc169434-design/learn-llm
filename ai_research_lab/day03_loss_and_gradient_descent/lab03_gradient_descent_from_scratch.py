from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

# Tái sử dụng bộ chuẩn bị dữ liệu chống Data Leakage từ Ngày 02 (dùng chính normalize_vn_message Ngày 01!)
DAY02_DIR = Path(__file__).resolve().parent.parent / "day02_ml_classifiers_and_metrics"
sys.path.insert(0, str(DAY02_DIR))
from lab02_ml_classifiers import LABEL_ORDER, prepare_train_test_vectors  # noqa: E402

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "vn_messages.csv"


def softmax(logits: np.ndarray) -> np.ndarray:
    """
    TODO 1: Chuyển ma trận điểm số thô `logits` (shape: N x C) thành ma trận xác suất (shape: N x C, tổng mỗi hàng = 1.0).

    Hướng dẫn từng bước (có Numerical Stability chống tràn số exp -> inf):
    1. Tìm giá trị lớn nhất của TỪNG HÀNG (giữ nguyên 2 chiều để trừ được theo từng hàng) rồi lấy `logits` trừ đi nó.
    2. Lấy hàm mũ `e^x` cho từng phần tử.
    3. Chia từng phần tử cho TỔNG của chính hàng đó (cũng giữ nguyên 2 chiều).
    """

    rows, cols = logits.shape
    row_max = []
    for row in rows:
        row_max.append(np.max(logits[row:, :]))






    shape = logits.shape

    raise NotImplementedError("Hãy hoàn thiện TODO 1")


def compute_cross_entropy_loss(probs: np.ndarray, y_true_idx: np.ndarray) -> float:
    """
    TODO 2: Tính Cross-Entropy Loss trung bình trên N mẫu:
        Loss = -mean(ln(p_nhãn_đúng))

    Input:
      - `probs`: ma trận xác suất dự đoán (shape: N x C)
      - `y_true_idx`: mảng chỉ số nhãn thật (shape: N,), mỗi phần tử nằm trong 0..C-1
    Hướng dẫn từng bước:
    1. Với từng hàng `i` từ `0` tới `N-1`, rút đúng xác suất ở cột `y_true_idx[i]`.
    2. Kẹp (clip) các xác suất này vào khoảng `[1e-12, 1.0]` để tránh lỗi toán học `ln(0) = -inf`.
    3. Lấy `-mean(ln(...))` và ép kiểu trả về `float` chuẩn Python.
    """
    raise NotImplementedError("Hãy hoàn thiện TODO 2")


def train_softmax_gd(
        X_train: np.ndarray,
        y_train_idx: np.ndarray,
        num_classes: int,
        lr: float = 1.5,
        epochs: int = 200,
) -> tuple[np.ndarray, np.ndarray, list[float]]:
    """
    TODO 3: Tự viết vòng lặp Gradient Descent bằng NumPy thuần (mở hộp đen `model.fit()`!).

    Input:
      - `X_train`: ma trận TF-IDF (shape: N x F)
      - `y_train_idx`: mảng chỉ số nhãn thật (shape: N,)
      - `num_classes`: số lớp C (ở đây là 4)
    Hướng dẫn từng bước:
    1. Lấy `n_samples, n_features` từ kích thước của `X_train`.
    2. Khởi tạo ma trận trọng số `W` toàn số 0 (shape: F x C) và vector bias `b` toàn số 0 (shape: C,).
    3. Chuyển `y_train_idx` sang ma trận One-Hot `y_one_hot` (shape: N x C, mỗi hàng chỉ có đúng 1 số 1.0 ở cột nhãn thật).
    4. Tạo danh sách rỗng `loss_history`, rồi lặp `epochs` lần, mỗi Epoch làm đúng 3 bước:
       - Bước 1 (Forward Pass):
           Tính `logits = X_train @ W + b` -> qua `softmax` ra `probs` -> tính `loss` -> lưu vào `loss_history`.
       - Bước 2 (Backward Pass — Công thức đạo hàm Softmax + Cross-Entropy):
           * Sai lệch trung bình từng ô: `diff = (probs - y_one_hot) / n_samples` (shape: N x C)
           * Độ dốc theo W: `grad_W` = tích ma trận giữa chuyển vị của `X_train` (F x N) với `diff` (N x C) -> shape: F x C
           * Độ dốc theo b: `grad_b` = tổng theo từng cột (axis=0) của `diff` -> shape: C
       - Bước 3 (Update Step — Đi ngược chiều dốc xuống thung lũng):
           Cập nhật `W` và `b` theo công thức `tham_số_mới = tham_số_cũ - lr * grad`.
    5. Trả về tuple `(W, b, loss_history)`.
    """
    raise NotImplementedError("Hãy hoàn thiện TODO 3")


def predict_classes(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    probs = softmax(X @ W + b)
    return np.argmax(probs, axis=1)


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    texts = df["text"].tolist()
    labels = df["label"].tolist()

    label_to_idx = {label: idx for idx, label in enumerate(LABEL_ORDER)}
    vectorizer, X_train_sparse, X_test_sparse, y_train, y_test = prepare_train_test_vectors(texts, labels)

    # Chuyển ma trận thưa sang mảng NumPy thường để tự nhân ma trận `X @ W + b`
    X_train = X_train_sparse.toarray()
    X_test = X_test_sparse.toarray()
    y_train_idx = np.array([label_to_idx[y] for y in y_train])
    y_test_idx = np.array([label_to_idx[y] for y in y_test])

    # Kiểm tra nhanh TODO 1 & TODO 2
    demo_probs = softmax(np.array([[2.0, 1.0, 0.1, 0.0]]))
    assert np.isclose(demo_probs.sum(), 1.0), "Tổng xác suất Softmax phải bằng 1.0"
    demo_loss = compute_cross_entropy_loss(np.array([[0.99, 0.01]]), np.array([0]))
    assert demo_loss < 0.02, "Loss của p=0.99 phải gần 0 (~0.01)"
    print(f"✓ Pass TODO 1 & 2 — Softmax sum = {demo_probs.sum():.2f}, Loss(p=0.99) = {demo_loss:.4f}")

    # Huấn luyện tự viết bằng Gradient Descent thuần NumPy!
    W, b, loss_history = train_softmax_gd(X_train, y_train_idx, num_classes=len(LABEL_ORDER), lr=1.5, epochs=200)
    print(
        f"✓ Pass TODO 3 — Loss giảm từ Epoch 1 ({loss_history[0]:.4f}) "
        f"-> Epoch 50 ({loss_history[49]:.4f}) -> Epoch 200 ({loss_history[-1]:.4f})"
    )

    train_pred = predict_classes(X_train, W, b)
    test_pred = predict_classes(X_test, W, b)
    print(
        f"\nKết quả model TỰ VIẾT BẰNG NUMPY THUẦN (0 dòng sklearn.fit!):\n"
        f"  Train Acc = {accuracy_score(y_train_idx, train_pred):.1%}\n"
        f"  Test Acc  = {accuracy_score(y_test_idx, test_pred):.1%}\n"
        f"  Macro-F1  = {f1_score(y_test_idx, test_pred, average='macro', zero_division=0):.3f}"
    )

    # Thử nghiệm tốc độ học quá nhỏ vs vừa đẹp vs quá lớn!
    print("\nThí nghiệm Learning Rate (so sánh Loss cuối sau 50 epochs):")
    for test_lr in [0.05, 1.5, 50.0]:
        _, _, hist = train_softmax_gd(X_train, y_train_idx, num_classes=len(LABEL_ORDER), lr=test_lr, epochs=50)
        print(f"  lr = {test_lr:<5} | Epoch 1 Loss = {hist[0]:.4f} -> Epoch 50 Loss = {hist[-1]:.4f}")
