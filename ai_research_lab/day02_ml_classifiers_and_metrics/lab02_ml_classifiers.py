from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

# Tái sử dụng hàm chuẩn hóa tiếng Việt không dấu/viết tắt bạn vừa tự viết ở Ngày 01!
DAY01_DIR = Path(__file__).resolve().parent.parent / "day01_tfidf_and_vn_text"
sys.path.insert(0, str(DAY01_DIR))
from lab01_tfidf_from_scratch import normalize_vn_message  # noqa: E402

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "vn_messages.csv"
LABEL_ORDER = ["URGENT", "BANKING", "NORMAL", "SPAM"]


def prepare_train_test_vectors(
        texts: list[str],
        labels: list[str],
        test_size: float = 0.25,
        random_state: int = 42,
):
    """
    TODO 1: Chia tập Train / Test (Stratified) và vector hóa TF-IDF chống Data Leakage.

    Yêu cầu:
    1. Dùng `train_test_split(texts, labels, test_size=test_size, random_state=random_state, stratify=labels)`
       để tách ra `X_train_text, X_test_text, y_train, y_test`.
    2. Khởi tạo `TfidfVectorizer(tokenizer=normalize_vn_message, token_pattern=None)`.
    3. Học từ điển & IDF CHỈ trên tập Train bằng `fit_transform(X_train_text)`,
       còn tập Test CHỈ dùng `transform(X_test_text)`.
    4. Trả về tuple 5 phần tử: `(vectorizer, X_train, X_test, y_train, y_test)`.
    """
    x_train_test, x_test_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=test_size,
        random_state=random_state,
        stratify=labels,
    )
    vectorizer = TfidfVectorizer(tokenizer=normalize_vn_message, token_pattern=None)
    x_train = vectorizer.fit_transform(x_train_test)
    x_test = vectorizer.transform(x_test_test)
    return vectorizer,x_train, x_test, y_train, y_test



def train_and_evaluate_model(
        model_name: str,
        model,
        X_train,
        X_test,
        y_train: list[str],
        y_test: list[str],
) -> dict:
    """
    TODO 2: Huấn luyện 1 model ML và đo đủ 4 chỉ số đánh giá (phát hiện Overfitting + bỏ sót URGENT).

    Yêu cầu:
    1. Huấn luyện model trên `(X_train, y_train)` bằng `model.fit(...)`.
    2. Dự đoán trên cả tập Train (`train_pred`) và tập Test (`test_pred`) bằng `model.predict(...)`.
    3. Tính các chỉ số:
       - `train_acc`: `accuracy_score(y_train, train_pred)`
       - `test_acc`: `accuracy_score(y_test, test_pred)`
       - `macro_f1`: `f1_score(y_test, test_pred, average="macro", zero_division=0)`
       - `urgent_recall`: Recall riêng cho nhãn `"URGENT"`
         (gợi ý: `recall_score(y_test, test_pred, labels=["URGENT"], average=None, zero_division=0)[0]`)
       - `cm`: `confusion_matrix(y_test, test_pred, labels=LABEL_ORDER)`
    4. Trả về dict gồm các key:
       `"name"`, `"model"`, `"train_acc"`, `"test_acc"`, `"macro_f1"`, `"urgent_recall"`, `"cm"`.
    """
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, test_pred)
    macro_f1 = float(f1_score(y_test, test_pred, average="macro", zero_division=0))
    urgent_recall = float(recall_score(y_test, test_pred, labels=["URGENT"], average=None, zero_division=0)[0])
    cm = confusion_matrix(y_test, test_pred,labels=LABEL_ORDER)
    return {
        "name": model_name,
        "model": model,
        "train_acc": train_acc,
        "test_acc": test_acc,
        "macro_f1": macro_f1,
        "urgent_recall": urgent_recall,
        "cm": cm,
    }


def compare_three_models(
        X_train,
        X_test,
        y_train: list[str],
        y_test: list[str],
) -> list[dict]:
    """
    TODO 3: Khởi tạo và chấm điểm song song 3 model kinh điển trong bài báo ML của thầy Hùng.



    3 model cần so sánh:
    1. ("Logistic Regression", LogisticRegression(max_iter=1000, random_state=42))
    2. ("Linear SVM", LinearSVC(random_state=42))
    3. ("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42))

    Duyệt qua 3 model, gọi `train_and_evaluate_model(...)` cho từng model và trả về `list[dict]`.
    """
    candidates = [
        ("Logistic Regression", LogisticRegression(max_iter=1000, random_state=42)),
        ("Linear SVM", LinearSVC(random_state=42)),
        ("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42)),
    ]
    results: list[dict] = []
    for name, model in candidates:
        res = train_and_evaluate_model(name, model, X_train, X_test, y_train, y_test)
        results.append(res)
    return results


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    texts = df["text"].tolist()
    labels = df["label"].tolist()

    vectorizer, X_train, X_test, y_train, y_test = prepare_train_test_vectors(texts, labels)
    print(f"✓ Pass TODO 1 — Train: {X_train.shape}, Test: {X_test.shape}")

    results = compare_three_models(X_train, X_test, y_train, y_test)
    assert len(results) == 3, "Cần trả về kết quả của đủ 3 model"
    print("✓ Pass TODO 2 & 3 — Bảng so sánh thực nghiệm (Chuẩn báo cáo khoa học):\n")

    print(f"{'Model':<22} | {'Train Acc':>9} | {'Test Acc':>8} | {'Macro-F1':>8} | {'URGENT Recall':>13}")
    print("-" * 72)
    for res in results:
        print(
            f"{res['name']:<22} | {res['train_acc']:>8.1%} | {res['test_acc']:>7.1%} | "
            f"{res['macro_f1']:>8.3f} | {res['urgent_recall']:>12.1%}"
        )

    best = max(results, key=lambda item: item["macro_f1"])
    print(f"\n🏆 Model tốt nhất theo Macro-F1: {best['name']} (Macro-F1 = {best['macro_f1']:.3f})")
    print(f"\nConfusion Matrix của {best['name']} (hàng=Thật, cột=Dự đoán, thứ tự={LABEL_ORDER}):")
    print(best["cm"])

    # Thử nghiệm với 3 tin nhắn Zalo mới tinh chưa từng xuất hiện trong tập dữ liệu
    unseen_messages = [
        "anh oi con sot cao qua dua di bv gap",
        "TK 1903xxx vua tru 2.500.000 VND ma OTP 889912",
        "Sieu sale cuoi thang giam 50% voucher mua sam ngay hom nay",
    ]
    X_unseen = vectorizer.transform(unseen_messages)
    preds = best["model"].predict(X_unseen)
    print(f"\nThử nghiệm dự đoán bằng {best['name']} trên tin nhắn mới:")
    for msg, pred in zip(unseen_messages, preds):
        print(f"  [{pred:<7}] <- '{msg}'")
