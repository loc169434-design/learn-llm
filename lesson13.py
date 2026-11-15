import pandas as pd

# 1. Đọc dữ liệu từ file users.json vào DataFrame
df = pd.read_json("users.json")

print("--- 1. CẢ BẢNG DỮ LIỆU ---")
print(df)

print("\n--- 2. THÔNG TIN CƠ BẢN ---")
print("Kích thước (dòng, cột):", df.shape)
print("Kiểu dữ liệu từng cột:\n", df.dtypes)

print("\n--- 3. THỐNG KÊ NHANH CỘT TUỔI ---")
print("Tuổi trung bình:", df["age"].mean())
print("Tuổi lớn nhất:", df["age"].max())

print("\n--- 4. LỌC DỮ LIỆU (FILTER) ---")
# Chỉ lấy những người có tuổi > 25
print(df[df["age"] > 25])

print("\n--- 5. ĐẾM SỐ LƯỢNG THEO THÀNH PHỐ ---")
# Thay thế hoàn toàn vòng for đếm cities ở bài 12!
print(df["city"].value_counts())

print("\n--- 6. GOM NHÓM (GROUPBY) ---")
# Tính tuổi trung bình của từng thành phố
print(df.groupby("city")["age"].mean())