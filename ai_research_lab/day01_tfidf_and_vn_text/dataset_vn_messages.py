from __future__ import annotations

from pathlib import Path
import pandas as pd

# Bộ dữ liệu thực nghiệm Tin nhắn Tiếng Việt (Có dấu + Không dấu + Viết tắt thực tế)
# 4 Nhãn phục vụ bài toán Lính gác cửa (Gatekeeper) cho Trợ lý Lái xe & Fintech:
# - URGENT  : Khẩn cấp (tai nạn, y tế, sự cố gia đình/công việc cần dừng xe xử lý ngay)
# - BANKING : Biến động số dư, mã OTP, hóa đơn thanh toán ngân hàng
# - NORMAL  : Trò chuyện hàng ngày, hẹn ăn uống, hỏi thăm bình thường
# - SPAM    : Quảng cáo, khuyến mãi, vay tín dụng đen, trúng thưởng rác

RAW_SAMPLES: list[tuple[str, str]] = [
    # --- 1. URGENT (Khẩn cấp) ---
    ("Anh ơi con sốt cao 40 độ co giật rồi đưa đi bệnh viện cấp cứu gấp", "URGENT"),
    ("anh oi con sot cao dua di bv cap cuu gap", "URGENT"),
    ("Mẹ bị trượt ngã trong nhà tắm đau không đứng dậy được về ngay nhé", "URGENT"),
    ("me bi nga dau lam ve nha ngay di anh", "URGENT"),
    ("Cháy chập điện ở kho hàng tầng trệt rồi gọi cứu hỏa và về mở cửa gấp", "URGENT"),
    ("Sếp gọi họp khẩn sự cố sập server thanh toán khách hàng đang khiếu nại dữ dội", "URGENT"),
    ("server thanh toan sap roi sep goi hop khan cap ngay bay gio", "URGENT"),
    ("Xe của em bị va quệt ngoài ngã tư Hàng Xanh công an đang giữ giấy tờ anh qua gấp", "URGENT"),
    ("Ông nội khó thở tức ngực đang gọi xe cấp cứu 115 qua viện Tim", "URGENT"),
    ("Bố bị tụt huyết áp chóng mặt ngoài đường em đang chạy qua đón đi viện", "URGENT"),
    ("Cửa cuốn ở nhà bị cạy mở bất thường camera báo động đỏ anh kiểm tra ngay", "URGENT"),
    ("vo chuyen da dau bung sinh roi anh chay ve bv tu du ngay nhe", "URGENT"),

    # --- 2. BANKING (Ngân hàng / Tài chính) ---
    ("TK 1903456789 GD -250,000VND luc 11:30 SD 14,520,000VND ND thanh toan tien dien T11", "BANKING"),
    ("Ma OTP xac thuc giao dich chuyen khoan cua quy khach la 482910 tuyet doi khong cung cap cho ai", "BANKING"),
    ("Biến động số dư TK +23,000,000VND nội dung chuyển khoản lương tháng 11", "BANKING"),
    ("Thẻ tín dụng Visa đuôi 8899 vừa thanh toán 450,000đ tại trạm xăng Petrolimex", "BANKING"),
    ("Nhắc lịch thanh toán dư nợ thẻ tín dụng kỳ sao kê tháng 11 số tiền tối thiểu 1,200,000VND", "BANKING"),
    ("em vua ck 500k tien an trua vao tk techcombank cua anh roi nhe", "BANKING"),
    ("GD thanh cong -1,500,000VND tai Cty Bao Hiem xe o to SD cuoi 8,200,000VND", "BANKING"),
    ("Mã xác thực Smart OTP cho giao dịch thanh toán hóa đơn nước là 993120 hiệu lực 2 phút", "BANKING"),
    ("Tài khoản tiết kiệm trực tuyến kỳ hạn 6 tháng đã tất toán lãi cộng vào tài khoản chính", "BANKING"),
    ("anh nho ck dong hoc phi cho con truoc 5h chieu nay nha", "BANKING"),
    ("Thông báo thu phí duy trì dịch vụ SMS Banking tháng 11 số tiền 11,000VND", "BANKING"),
    ("Hoàn tiền 50,000VND ưu đãi hoàn tiền chi tiêu siêu thị vào tài khoản thẻ tín dụng", "BANKING"),

    # --- 3. NORMAL (Trò chuyện bình thường) ---
    ("Anh ơi tối nay đi làm về nhớ ghé chợ mua thêm bó rau muống với vỉ trứng nhé", "NORMAL"),
    ("toi nay ve an com nha hay an ngoai vay anh oi", "NORMAL"),
    ("Cuối tuần này hội bạn cấp ba rủ đi uống cà phê sáng chủ nhật bạn đi được không", "NORMAL"),
    ("Chiều về đón con giúp em nhé hôm nay em ở lại văn phòng làm nốt báo cáo thêm 30 phút", "NORMAL"),
    ("Trời đang mưa to đấy lái xe về từ từ cẩn thận kẻo ngập đường nhé", "NORMAL"),
    ("troi mua to ngap duong lai xe can than nha anh", "NORMAL"),
    ("Đặt bàn quán nướng tối thứ bảy lúc 7 giờ tối rồi nhé nhớ tới đúng giờ", "NORMAL"),
    ("Gửi lại cho mình xin file tài liệu họp tuần trước lúc nào rảnh cũng được nha", "NORMAL"),
    ("Hôm qua xem trận bóng đá hay quá cuối tuần làm trận giao hữu sân cỏ nhân tạo nhé", "NORMAL"),
    ("Em để sẵn hộp cơm trưa trong ngăn mát tủ lạnh mai anh nhớ mang đi làm", "NORMAL"),
    ("Lúc nào về tới nhà nhắn cho mẹ một tiếng để mẹ yên tâm đi ngủ nhé", "NORMAL"),
    ("chut nua ranh gui cho minh xin dia chi quan phở hom truoc nhe", "NORMAL"),

    # --- 4. SPAM (Quảng cáo / Rác / Lừa đảo) ---
    ("Khuyến mãi cực sốc giảm giá 50% toàn bộ phụ kiện thời trang duy nhất hôm nay bấm link ngay", "SPAM"),
    ("km giam gia 70% san sale cuoi thang nhan voucher mien phi van chuyen ngay", "SPAM"),
    ("Hỗ trợ vay tiêu dùng tín chấp giải ngân nhanh trong 15 phút không cần thẩm định người thân", "SPAM"),
    ("Chúc mừng thuê bao quý khách đã trúng thưởng phiếu quà tặng trị giá 50 triệu đồng truy cập nhận giải", "SPAM"),
    ("Bán cắt lỗ căn hộ chung cư mặt tiền chiết khấu ngay 8% tặng gói nội thất cao cấp", "SPAM"),
    ("Tuyển cộng tác viên làm việc tại nhà ngày kiếm 800k chỉ cần điện thoại có kết nối mạng", "SPAM"),
    ("vay tien nhanh lai suat thap giai ngan trong ngay chi can cccd", "SPAM"),
    ("Ưu đãi độc quyền tặng 100k vào ví khi đăng ký mở tài khoản game đổi thưởng uy tín", "SPAM"),
    ("Giảm ngay 40% liệu trình chăm sóc da chuyên sâu tại thẩm mỹ viện đăng ký nhận suất trải nghiệm", "SPAM"),
    ("Cơ hội đầu tư cổ phiếu quốc tế cam kết lợi nhuận 30% mỗi tháng có chuyên gia hỗ trợ 1 kèm 1", "SPAM"),
    ("Sim số đẹp phong thủy tài lộc giá rẻ thanh lý kho sim tam hoa tứ quý giao tận nơi", "SPAM"),
    ("Tang ban ma giam gia 200k khi mua sam dien may cuoi tuan nay dung bo lo", "SPAM"),
]


def export_dataset() -> Path:
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data_dir / "vn_messages.csv"

    df = pd.DataFrame(RAW_SAMPLES, columns=["text", "label"])
    df.to_csv(csv_path, index=False, encoding="utf-8")
    return csv_path


if __name__ == "__main__":
    out_path = export_dataset()
    df = pd.read_csv(out_path)
    print(f"Đã xuất {len(df)} mẫu tin nhắn tiếng Việt tại: {out_path}")
    print("\nPhân bố số lượng theo nhãn:")
    print(df["label"].value_counts())
