import pandas as pd

# Dữ liệu thô (giả lập dữ liệu thật hay bị bẩn: trùng dòng, viết hoa/thường lộn xộn, dư dấu cách, null)
users_raw = [
    {"user_id": 1, "name": "An", "city": " hcm "},
    {"user_id": 2, "name": "Binh", "city": "Hn"},
    {"user_id": 3, "name": "Chi", "city": "HCM"},
    {"user_id": 1, "name": "An", "city": " hcm "},  # Bị trùng!
]

tx_raw = [
    {"tx_id": "T01", "user_id": 1, "amount": 150000, "status": "SUCCESS"},
    {"tx_id": "T02", "user_id": 1, "amount": 200000, "status": "FAILED"},
    {"tx_id": "T03", "user_id": 2, "amount": 500000, "status": "SUCCESS"},
    {"tx_id": "T04", "user_id": 3, "amount": None, "status": "SUCCESS"},
    {"tx_id": "T05", "user_id": 99, "amount": 100000, "status": "SUCCESS"},  # user_id chưa có trong df_users
]

df_users = pd.DataFrame(users_raw)
df_tx = pd.DataFrame(tx_raw)

print("=== DỮ LIỆU BAN ĐẦU ===")
print("Users:\n", df_users)
print("\nTransactions:\n", df_tx)

# TODO 1: Làm sạch df_users
# - Xóa dòng trùng bằng .drop_duplicates() (nhớ dùng .copy() nếu gán sang biến mới)
# - Chuẩn hóa cột "city": bỏ khoảng trắng thừa + viết HOA (.str.strip().str.upper())
df_users_clean = df_users.drop_duplicates().copy()
df_users_clean["city"] = df_users_clean["city"].str.strip().str.upper()

# TODO 2: Làm sạch df_tx
# - Điền giá trị 0 cho các ô amount bị thiếu (.fillna(0))
# - Chỉ lọc các giao dịch có status == "SUCCESS"
df_tx_clean = df_tx.copy()
df_tx_clean["amount"] = df_tx_clean["amount"].fillna(0)
df_tx_clean = df_tx_clean[df_tx_clean["status"] == "SUCCESS"]

# TODO 3: Ghép (JOIN) 2 bảng theo cột "user_id"
# - Dùng pd.merge(df_tx_clean, df_users_clean, on="user_id", how="inner")
# - Thử đổi sang how="left" xem dòng T05 (user_id=99) hiển thị thế nào
df_merged = pd.merge(df_users_clean, df_tx_clean, on="user_id", how="inner")
print("\n=== SAU KHI MERGE (INNER) ===\n", df_merged)

# TODO 4: Thống kê doanh thu theo thành phố
# - Dùng .groupby("city")["amount"].agg(["count", "sum", "mean"])
# - Sắp xếp giảm dần theo cột "sum" bằng .sort_values("sum", ascending=False)
report = (
    df_merged.groupby("city")["amount"]
    .agg(["count", "sum", "mean"])
    .sort_values("sum", ascending=False)
)
print("\n=== BÁO CÁO DOANH THU THEO THÀNH PHỐ ===\n", report)