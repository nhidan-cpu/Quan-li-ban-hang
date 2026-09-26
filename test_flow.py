from thao_tac_danh_sach_san_pham import (
    tao_san_pham
)

from thao_tac_kho import (
    danh_sach_ton_kho,
    khoi_tao_danh_sach_ton_kho,
    tim_ton_kho
)

from thao_tac_nhap_hang import (
    danh_sach_phieu_nhap,
    tao_phieu_nhap,
    tao_chi_tiet_nhap,
    them_chi_tiet_vao_phieu_nhap,
    luu_phieu_nhap,
    sua_phieu_nhap,
    sua_dong_chi_tiet_phieu_nhap,
    xac_nhan_luu
)

from thao_tac_ban_hang import (
    danh_sach_phieu_ban,
    danh_sach_phieu_gntt,

    tao_phieu_ban,
    tao_phieu_gntt,

    tao_chi_tiet_ban,
    them_chi_tiet_vao_phieu_ban,
    them_chi_tiet_phieu_ban,

    sua_header_phieu_ban,
    sua_dong_chi_tiet_phieu_ban,
    xoa_chi_tiet_phieu_ban,

    luu_phieu_ban,
    xac_nhan_luu_phieu_ban,

    tim_phieu_ban,
    tim_phieu_gntt,

    load_phieu_ban,
    load_phieu_gntt,

    sua_phieu_ban,

    phieu_co_thay_doi_chua_luu,
    dat_lai_trang_thai_phieu,

    luu_phieu_gntt,
    xac_nhan_luu_phieu_gntt
)

from nghiep_vu_khach_hang import (
    danh_sach_khach_hang,
    tao_khach_hang,
    tim_khach_hang,
    sua_khach_hang,
    doi_trang_thai_khach_hang,
    cap_nhat_tong_giao_dich,
    cap_nhat_cong_no
)

from nghiep_vu_gia import (
    danh_sach_gia_niem_yet,
    danh_sach_bang_gia_phan_khuc,

    tim_gia_niem_yet,
    tinh_gia_von_binh_quan,
    cap_nhat_gia_von,
    cap_nhat_toan_bo_gia_von,

    them_san_pham_vao_gia_niem_yet,
    dong_bo_san_pham_vao_gia_niem_yet,
    dong_bo_xoa_san_pham,
    dong_bo_toan_bo_gia_niem_yet,

    sua_gia_ban_niem_yet,
    dong_bo_gia_ban_tu_san_pham,

    them_bang_gia_phan_khuc,
    tim_bang_gia_phan_khuc,
    tim_san_pham_trong_bang_gia,
    xoa_bang_gia_phan_khuc,

    them_san_pham_vao_bang_gia_phan_khuc,
    them_lai_san_pham,
    xoa_san_pham_khoi_bang_gia,

    dong_bo_tu_gia_niem_yet,
    cap_nhat_gia_ban,

    tinh_gia_theo_cau_hinh,
    ap_dung_cau_hinh_tinh_gia
)

from nghiep_vu_bao_gia import (
    danh_sach_mau_bao_gia,
    tao_mau_bao_gia,
    tim_mau_bao_gia,

    tao_chi_tiet_bao_gia,
    them_chi_tiet_vao_mau_bao_gia,

    sua_chi_tiet_bao_gia,
    xoa_chi_tiet_bao_gia,

    luu_mau_bao_gia,
    sua_mau_bao_gia,
    xac_nhan_luu_mau_bao_gia
)


# ============================================================
# CHUẨN BỊ DỮ LIỆU TEST
# ============================================================

danh_sach_san_pham = [
    tao_san_pham(
        ["SP-0001"],
        "VAT-0001",
        "Sản phẩm test",
        "Danh mục test",
        "Cái",
        0,
        15000,
        []
    )
]


# Xóa dữ liệu test cũ

danh_sach_ton_kho.clear()
danh_sach_phieu_nhap.clear()
danh_sach_phieu_ban.clear()
danh_sach_khach_hang.clear()

danh_sach_gia_niem_yet.clear()
danh_sach_bang_gia_phan_khuc.clear()

danh_sach_mau_bao_gia.clear()


danh_sach_kho = [
    {
        "ma_kho": "KHO-01",
        "ten_kho": "Kho chính",
        "dia_chi": "HCM"
    }
]


khoi_tao_danh_sach_ton_kho(
    danh_sach_ton_kho,
    danh_sach_san_pham,
    danh_sach_kho
)


san_pham = danh_sach_san_pham[0]


ton = tim_ton_kho(
    danh_sach_ton_kho,
    "KHO-01",
    "SP-0001"
)


# ============================================================
# TEST 1 - TỒN KHO BAN ĐẦU
# ============================================================

assert ton["so_luong_ton"] == 0
assert ton["gia_tri_ton"] == 0

assert "gia_von_binh_quan" not in ton

print("TEST 1 PASSED")


# ============================================================
# TEST 2 - NHẬP HÀNG
# ============================================================

phieu_nhap_1 = tao_phieu_nhap(
    "PN260926-0001"
)

phieu_nhap_1["ma_kho_nhap"] = "KHO-01"


chi_tiet_nhap_1 = tao_chi_tiet_nhap(
    san_pham,
    san_pham["dvt_chinh"],
    100,
    "CHIA THANG",
    10000,
    0
)


them_chi_tiet_vao_phieu_nhap(
    danh_sach_san_pham,
    phieu_nhap_1,
    chi_tiet_nhap_1
)


luu_phieu_nhap(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu_nhap_1
)


assert ton["so_luong_ton"] == 100
assert ton["gia_tri_ton"] == 1_000_000

print("TEST 2 PASSED")


# ============================================================
# TEST 3 - KIỂM TRA PHIẾU NHẬP ĐÃ LƯU
# ============================================================

assert len(danh_sach_phieu_nhap) == 1

assert (
    danh_sach_phieu_nhap[0]["ma_phieu_nhap"]
    == "PN260926-0001"
)

print("TEST 3 PASSED")


# ============================================================
# TEST 4 - SỬA PHIẾU NHẬP
# ============================================================

phieu_nhap_sua = sua_phieu_nhap(
    danh_sach_phieu_nhap[0]
)


sua_dong_chi_tiet_phieu_nhap(
    danh_sach_san_pham,
    phieu_nhap_sua,
    0,
    {
        "so_luong": 120
    }
)


xac_nhan_luu(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu_nhap_sua
)


assert ton["so_luong_ton"] == 120
assert ton["gia_tri_ton"] == 1_200_000

print("TEST 4 PASSED")


# ============================================================
# TEST 5 - KIỂM TRA PHIẾU NHẬP SAU KHI SỬA
# ============================================================

assert len(danh_sach_phieu_nhap) == 1

assert (
    danh_sach_phieu_nhap[0]["chi_tiet"][0]["so_luong"]
    == 120
)

assert (
    danh_sach_phieu_nhap[0]["tong_thanh_tien"]
    == 1_200_000
)

print("TEST 5 PASSED")


# ============================================================
# TEST 6 - KHÔNG CỘNG TỒN KHO HAI LẦN
# ============================================================

assert ton["so_luong_ton"] == 120
assert ton["gia_tri_ton"] == 1_200_000

print("TEST 6 PASSED")


# ============================================================
# NHÓM TEST BÁN HÀNG / GNTT
# ============================================================

# TEST 7 - Tạo phiếu mới

phieu_ban_1 = tao_phieu_ban(
    "GNTT260926-0001"
)

assert phieu_ban_1["ma_phieu"] == "GNTT260926-0001"
assert phieu_ban_1["chi_tiet"] == []

assert phieu_ban_1["_da_load"] is False
assert phieu_ban_1["_da_thay_doi"] is False

assert (
    phieu_co_thay_doi_chua_luu(phieu_ban_1)
    is False
)

print("TEST 7 PASSED")


# ============================================================
# TEST 8 - THÊM DÒNG
# ============================================================

chi_tiet_1 = tao_chi_tiet_ban(
    san_pham,
    "KHO-01",
    san_pham["dvt_chinh"],
    20,
    "CHIET KHAU",
    15000,
    0
)


them_chi_tiet_vao_phieu_ban(
    danh_sach_san_pham,
    phieu_ban_1,
    chi_tiet_1
)


assert len(phieu_ban_1["chi_tiet"]) == 1
assert phieu_ban_1["_da_thay_doi"] is True

assert (
    phieu_co_thay_doi_chua_luu(phieu_ban_1)
    is True
)

assert (
    phieu_ban_1["tong_thanh_tien"]
    == 300000
)

print("TEST 8 PASSED")


# ============================================================
# TEST 9 - LƯU PHIẾU MỚI
# ============================================================

luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_ban_1
)


assert len(danh_sach_phieu_ban) == 1

assert (
    tim_phieu_ban("GNTT260926-0001")
    is not None
)

assert "_da_load" not in danh_sach_phieu_ban[0]
assert "_da_thay_doi" not in danh_sach_phieu_ban[0]

assert phieu_ban_1["_da_thay_doi"] is False

assert (
    phieu_co_thay_doi_chua_luu(phieu_ban_1)
    is False
)


assert ton["so_luong_ton"] == 100
assert ton["gia_tri_ton"] == 1_000_000

print("TEST 9 PASSED")


# ============================================================
# TEST 10 - LOAD PHIẾU
# ============================================================

phieu_load = load_phieu_ban(
    "GNTT260926-0001"
)


assert phieu_load is not None

assert (
    phieu_load
    is not danh_sach_phieu_ban[0]
)

assert phieu_load["_da_load"] is True
assert phieu_load["_da_thay_doi"] is False

assert (
    phieu_co_thay_doi_chua_luu(phieu_load)
    is False
)

print("TEST 10 PASSED")


# ============================================================
# TEST 11 - SỬA HEADER
# ============================================================

sua_header_phieu_ban(
    phieu_load,
    ma_khach_hang="KH-0001",
    ten_khach_hang="Khách hàng test",
    ghi_chu="Ghi chú mới"
)


assert phieu_load["ma_khach_hang"] == "KH-0001"
assert phieu_load["ten_khach_hang"] == "Khách hàng test"
assert phieu_load["ghi_chu"] == "Ghi chú mới"

assert phieu_load["_da_thay_doi"] is True

print("TEST 11 PASSED")


# ============================================================
# TEST 12 - THÊM DÒNG THỨ HAI
# ============================================================

chi_tiet_2 = tao_chi_tiet_ban(
    san_pham,
    "KHO-01",
    san_pham["dvt_chinh"],
    5,
    "CHIET KHAU",
    20000,
    10
)


them_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_load,
    chi_tiet_2
)


assert len(phieu_load["chi_tiet"]) == 2

assert (
    phieu_load["chi_tiet"][1]["don_gia_sau_ck"]
    == 18000
)

assert phieu_load["_da_thay_doi"] is True

print("TEST 12 PASSED")


# ============================================================
# TEST 13 - SỬA DÒNG
# ============================================================

phieu_load["chi_tiet"][0]["don_gia_von"] = 10000
phieu_load["chi_tiet"][0]["thanh_tien_von"] = 200000


sua_dong_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_load,
    0,
    {
        "so_luong": 25
    }
)


assert (
    phieu_load["chi_tiet"][0]["so_luong"]
    == 25
)

assert (
    phieu_load["chi_tiet"][0]["don_gia_von"]
    == 0
)

assert (
    phieu_load["chi_tiet"][0]["thanh_tien_von"]
    == 0
)

assert phieu_load["_da_thay_doi"] is True

print("TEST 13 PASSED")


# ============================================================
# TEST 14 - XÓA DÒNG
# ============================================================

xoa_chi_tiet_phieu_ban(
    phieu_load,
    1
)


assert len(phieu_load["chi_tiet"]) == 1

assert (
    phieu_load["chi_tiet"][0]["stt"]
    == 1
)

assert phieu_load["_da_thay_doi"] is True

print("TEST 14 PASSED")


# ============================================================
# TEST 15 - DATABASE CHƯA THAY ĐỔI
# ============================================================

phieu_da_luu = tim_phieu_ban(
    "GNTT260926-0001"
)


assert (
    phieu_da_luu["chi_tiet"][0]["so_luong"]
    == 20
)

assert phieu_da_luu["ma_khach_hang"] == ""

print("TEST 15 PASSED")


# ============================================================
# TEST 16 - UPDATE PHIẾU ĐÃ LOAD
# ============================================================

xac_nhan_luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_load
)


assert phieu_load["_da_thay_doi"] is False

assert (
    phieu_co_thay_doi_chua_luu(phieu_load)
    is False
)


phieu_sau_update = tim_phieu_ban(
    "GNTT260926-0001"
)


assert (
    phieu_sau_update["ma_khach_hang"]
    == "KH-0001"
)

assert (
    phieu_sau_update["ten_khach_hang"]
    == "Khách hàng test"
)

assert (
    phieu_sau_update["ghi_chu"]
    == "Ghi chú mới"
)

assert (
    phieu_sau_update["chi_tiet"][0]["so_luong"]
    == 25
)

assert "_da_load" not in phieu_sau_update
assert "_da_thay_doi" not in phieu_sau_update


assert ton["so_luong_ton"] == 95
assert ton["gia_tri_ton"] == 950_000

print("TEST 16 PASSED")


# ============================================================
# TEST 17 - LOAD LẠI SAU UPDATE
# ============================================================

phieu_load_lai = load_phieu_ban(
    "GNTT260926-0001"
)


assert phieu_load_lai["_da_load"] is True
assert phieu_load_lai["_da_thay_doi"] is False

assert (
    phieu_load_lai["chi_tiet"][0]["so_luong"]
    == 25
)

assert (
    phieu_co_thay_doi_chua_luu(phieu_load_lai)
    is False
)

print("TEST 17 PASSED")


# ============================================================
# TEST 18 - DIRTY CHỈ DO NGHIỆP VỤ
# ============================================================

sua_header_phieu_ban(
    phieu_load_lai,
    ghi_chu="Thay đổi chưa lưu"
)


assert (
    phieu_co_thay_doi_chua_luu(phieu_load_lai)
    is True
)


dat_lai_trang_thai_phieu(
    phieu_load_lai
)


assert phieu_load_lai["_da_thay_doi"] is False

assert (
    phieu_co_thay_doi_chua_luu(phieu_load_lai)
    is False
)

print("TEST 18 PASSED")


# ============================================================
# TEST 19 - HỦY THAY ĐỔI KHÔNG ẢNH HƯỞNG DATABASE
# ============================================================

phieu_load_lai = load_phieu_ban(
    "GNTT260926-0001"
)


sua_dong_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_load_lai,
    0,
    {
        "so_luong": 10
    }
)


assert phieu_load_lai["_da_thay_doi"] is True

assert (
    tim_phieu_ban("GNTT260926-0001")
    ["chi_tiet"][0]["so_luong"]
    == 25
)

assert ton["so_luong_ton"] == 95
assert ton["gia_tri_ton"] == 950_000

print("TEST 19 PASSED")


# ============================================================
# TEST 20 - KHÔNG ĐỦ TỒN KHO
# ============================================================

phieu_loi = tao_phieu_ban(
    "GNTT260926-FAIL"
)


chi_tiet_loi = tao_chi_tiet_ban(
    san_pham,
    "KHO-01",
    san_pham["dvt_chinh"],
    1000,
    "CHIET KHAU",
    10000,
    0
)


them_chi_tiet_vao_phieu_ban(
    danh_sach_san_pham,
    phieu_loi,
    chi_tiet_loi
)


try:

    luu_phieu_ban(
        danh_sach_san_pham,
        danh_sach_ton_kho,
        phieu_loi
    )

    assert False

except ValueError:

    pass


assert (
    tim_phieu_ban("GNTT260926-FAIL")
    is None
)

assert ton["so_luong_ton"] == 95

print("TEST 20 PASSED")


# ============================================================
# TEST 21 - GNTT DÙNG CHUNG LUỒNG BÁN HÀNG
# ============================================================

phieu_gntt = tao_phieu_gntt(
    "GNTT260926-0002"
)


chi_tiet_gntt = tao_chi_tiet_ban(
    san_pham,
    "KHO-01",
    san_pham["dvt_chinh"],
    5,
    "CHIET KHAU",
    20000,
    0
)


them_chi_tiet_vao_phieu_ban(
    danh_sach_san_pham,
    phieu_gntt,
    chi_tiet_gntt
)


luu_phieu_gntt(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_gntt
)


assert (
    tim_phieu_gntt("GNTT260926-0002")
    is not None
)

assert (
    tim_phieu_ban("GNTT260926-0002")
    is tim_phieu_gntt("GNTT260926-0002")
)

assert ton["so_luong_ton"] == 90

print("TEST 21 PASSED")


# ============================================================
# TEST 22 - LOAD GNTT
# ============================================================

gntt_load = load_phieu_gntt(
    "GNTT260926-0002"
)


assert gntt_load is not None
assert gntt_load["_da_load"] is True
assert gntt_load["_da_thay_doi"] is False

assert (
    gntt_load["chi_tiet"][0]["so_luong"]
    == 5
)

print("TEST 22 PASSED")


# ============================================================
# TEST 23 - TỔNG TIỀN GNTT
# ============================================================

assert (
    phieu_gntt["tong_thanh_tien"]
    == 100000
)

assert (
    phieu_gntt["tong_thanh_tien_von"]
    == 0
)

assert (
    phieu_gntt["loi_nhuan"]
    == 100000
)

print("TEST 23 PASSED")


# ============================================================
# TEST 24 - DATABASE KHÔNG LƯU METADATA FORM
# ============================================================

phieu_kiem_tra = load_phieu_ban(
    "GNTT260926-0001"
)


luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_kiem_tra
)


phieu_db = tim_phieu_ban(
    "GNTT260926-0001"
)


assert "_da_load" not in phieu_db
assert "_da_thay_doi" not in phieu_db

print("TEST 24 PASSED")


# ============================================================
# NHÓM TEST KHÁCH HÀNG
# ============================================================

# TEST 25 - Tạo khách hàng

khach_hang = tao_khach_hang(
    "Khách hàng test",
    "0900000000",
    "HCM",
    "THUONG",
    "Khách hàng dùng để test"
)


assert khach_hang["ma_khach_hang"] == "KH-0001"

assert (
    khach_hang["ten_khach_hang"]
    == "Khách hàng test"
)

print("TEST 25 PASSED")


# ============================================================
# TEST 26 - Tìm khách hàng
# ============================================================

khach_hang_tim_duoc = tim_khach_hang(
    "KH-0001"
)


assert khach_hang_tim_duoc is not None

assert (
    khach_hang_tim_duoc["ten_khach_hang"]
    == "Khách hàng test"
)

print("TEST 26 PASSED")


# ============================================================
# TEST 27 - Sửa khách hàng
# ============================================================

sua_khach_hang(
    "KH-0001",
    ten_khach_hang="Khách hàng đã sửa",
    so_dien_thoai="0911111111",
    dia_chi="Địa chỉ mới",
    phan_khuc_khach_hang="VIP"
)


khach_hang = tim_khach_hang(
    "KH-0001"
)


assert khach_hang["ten_khach_hang"] == "Khách hàng đã sửa"
assert khach_hang["so_dien_thoai"] == "0911111111"
assert khach_hang["dia_chi"] == "Địa chỉ mới"
assert khach_hang["phan_khuc_khach_hang"] == "VIP"

assert khach_hang["tong_giao_dich"] == 0
assert khach_hang["cong_no"] == 0

print("TEST 27 PASSED")


# ============================================================
# TEST 28 - TỔNG GIAO DỊCH
# ============================================================

cap_nhat_tong_giao_dich(
    "KH-0001",
    300_000
)

assert khach_hang["tong_giao_dich"] == 300_000


cap_nhat_tong_giao_dich(
    "KH-0001",
    -300_000
)

assert khach_hang["tong_giao_dich"] == 0


cap_nhat_tong_giao_dich(
    "KH-0001",
    450_000
)

assert khach_hang["tong_giao_dich"] == 450_000


cap_nhat_tong_giao_dich(
    "KH-0001",
    -450_000
)

assert khach_hang["tong_giao_dich"] == 0

print("TEST 28 PASSED")


# ============================================================
# TEST 29 - CÔNG NỢ
# ============================================================

cap_nhat_cong_no(
    "KH-0001",
    2_000_000
)

assert khach_hang["cong_no"] == 2_000_000


cap_nhat_cong_no(
    "KH-0001",
    -500_000
)

assert khach_hang["cong_no"] == 1_500_000

print("TEST 29 PASSED")


# ============================================================
# TEST 30 - TRẠNG THÁI KHÁCH HÀNG
# ============================================================

doi_trang_thai_khach_hang(
    "KH-0001",
    "NGUNG_HOAT_DONG"
)

assert (
    khach_hang["trang_thai"]
    == "NGUNG_HOAT_DONG"
)


doi_trang_thai_khach_hang(
    "KH-0001",
    "DANG_HOAT_DONG"
)

assert (
    khach_hang["trang_thai"]
    == "DANG_HOAT_DONG"
)

assert khach_hang["tong_giao_dich"] == 0
assert khach_hang["cong_no"] == 1_500_000

print("TEST 30 PASSED")


# ============================================================
# NHÓM TEST PHÂN KHÚC KHÁCH HÀNG
# ============================================================

# TEST 31

khach_hang_3 = tao_khach_hang(
    ten_khach_hang="Khách hàng C",
    so_dien_thoai="0900000003",
    phan_khuc_khach_hang="ĐẠI LÝ"
)


assert (
    khach_hang_3["phan_khuc_khach_hang"]
    == "ĐẠI LÝ"
)

print("TEST 31 PASSED")


# ============================================================
# TEST 32
# ============================================================

khach_hang_tim_duoc = tim_khach_hang(
    khach_hang_3["ma_khach_hang"]
)


assert khach_hang_tim_duoc is khach_hang_3

assert (
    khach_hang_tim_duoc["phan_khuc_khach_hang"]
    == "ĐẠI LÝ"
)

print("TEST 32 PASSED")


# ============================================================
# TEST 33
# ============================================================

ma_khach_hang_3 = khach_hang_3["ma_khach_hang"]


sua_khach_hang(
    ma_khach_hang_3,
    phan_khuc_khach_hang="BÁN LẺ"
)


assert (
    tim_khach_hang(ma_khach_hang_3)
    ["phan_khuc_khach_hang"]
    == "BÁN LẺ"
)

print("TEST 33 PASSED")


# ============================================================
# TEST 34
# ============================================================

assert (
    tim_khach_hang(ma_khach_hang_3)
    ["ma_khach_hang"]
    == ma_khach_hang_3
)

print("TEST 34 PASSED")


# ============================================================
# TEST 35
# ============================================================

sua_khach_hang(
    ma_khach_hang_3,
    phan_khuc_khach_hang=""
)


assert (
    tim_khach_hang(ma_khach_hang_3)
    ["phan_khuc_khach_hang"]
    == ""
)

print("TEST 35 PASSED")


# ============================================================
# NHÓM TEST GIÁ NIÊM YẾT
# ============================================================

# TEST 36 - Thêm sản phẩm

danh_sach_gia_niem_yet.clear()


dong_gia = them_san_pham_vao_gia_niem_yet(
    san_pham
)


assert dong_gia["ma_san_pham"] == "SP-0001"
assert dong_gia["ten_san_pham"] == "Sản phẩm test"
assert dong_gia["gia_von"] == 0
assert dong_gia["gia_ban"] == 15000

assert len(danh_sach_gia_niem_yet) == 1

print("TEST 36 PASSED")


# ============================================================
# TEST 37 - Không thêm trùng
# ============================================================

dong_gia_trung = them_san_pham_vao_gia_niem_yet(
    san_pham
)


assert dong_gia_trung is dong_gia
assert len(danh_sach_gia_niem_yet) == 1

print("TEST 37 PASSED")


# ============================================================
# TEST 38 - Tìm giá niêm yết
# ============================================================

assert (
    tim_gia_niem_yet("SP-0001")
    is dong_gia
)

assert (
    tim_gia_niem_yet("SP-9999")
    is None
)

print("TEST 38 PASSED")


# ============================================================
# TEST 39 - TÍNH GIÁ VỐN BÌNH QUÂN
# ============================================================

gia_von = tinh_gia_von_binh_quan(
    danh_sach_phieu_nhap,
    "SP-0001"
)


assert gia_von == 10000

print("TEST 39 PASSED")


# ============================================================
# TEST 40 - CẬP NHẬT GIÁ VỐN
# ============================================================

dong_gia = cap_nhat_gia_von(
    danh_sach_phieu_nhap,
    "SP-0001"
)


assert dong_gia["gia_von"] == 10000

print("TEST 40 PASSED")


# ============================================================
# TEST 41 - CẬP NHẬT TOÀN BỘ GIÁ VỐN
# ============================================================

cap_nhat_toan_bo_gia_von(
    danh_sach_phieu_nhap
)


assert (
    tim_gia_niem_yet("SP-0001")
    ["gia_von"]
    == 10000
)

print("TEST 41 PASSED")


# ============================================================
# TEST 42 - SỬA GIÁ BÁN
# ============================================================

sua_gia_ban_niem_yet(
    danh_sach_san_pham,
    "SP-0001",
    18000
)


assert (
    tim_gia_niem_yet("SP-0001")
    ["gia_ban"]
    == 18000
)

assert san_pham["gia_ban"] == 18000

print("TEST 42 PASSED")


# ============================================================
# TEST 43 - ĐỒNG BỘ GIÁ BÁN TỪ SẢN PHẨM
# ============================================================

san_pham["gia_ban"] = 20000


dong_bo_gia_ban_tu_san_pham(
    danh_sach_san_pham
)


assert (
    tim_gia_niem_yet("SP-0001")
    ["gia_ban"]
    == 20000
)

print("TEST 43 PASSED")


# ============================================================
# TEST 44 - ĐỒNG BỘ SẢN PHẨM
# ============================================================

dong_bo_san_pham_vao_gia_niem_yet(
    danh_sach_san_pham
)


assert len(danh_sach_gia_niem_yet) == 1

assert (
    tim_gia_niem_yet("SP-0001")
    ["ten_san_pham"]
    == "Sản phẩm test"
)

assert (
    tim_gia_niem_yet("SP-0001")
    ["gia_ban"]
    == 20000
)

print("TEST 44 PASSED")


# ============================================================
# TEST 45 - THÊM SẢN PHẨM MỚI
# ============================================================

san_pham_moi = tao_san_pham(
    ["SP-0002"],
    "VAT-0002",
    "Sản phẩm test 2",
    "Danh mục test",
    "Cái",
    0,
    25000,
    []
)


danh_sach_san_pham.append(
    san_pham_moi
)


dong_bo_san_pham_vao_gia_niem_yet(
    danh_sach_san_pham
)


assert len(danh_sach_gia_niem_yet) == 2

assert (
    tim_gia_niem_yet("SP-0002")
    ["ten_san_pham"]
    == "Sản phẩm test 2"
)

assert (
    tim_gia_niem_yet("SP-0002")
    ["gia_ban"]
    == 25000
)

print("TEST 45 PASSED")


# ============================================================
# TEST 46 - XÓA SẢN PHẨM
# ============================================================

danh_sach_san_pham.remove(
    san_pham_moi
)


dong_bo_xoa_san_pham(
    danh_sach_san_pham
)


assert (
    tim_gia_niem_yet("SP-0002")
    is None
)

assert len(danh_sach_gia_niem_yet) == 1

print("TEST 46 PASSED")


# ============================================================
# TEST 47 - ĐỒNG BỘ TOÀN BỘ
# ============================================================

dong_bo_toan_bo_gia_niem_yet(
    danh_sach_san_pham
)


assert len(danh_sach_gia_niem_yet) == 1

dong_gia = tim_gia_niem_yet(
    "SP-0001"
)


assert dong_gia is not None

assert (
    dong_gia["ten_san_pham"]
    == san_pham["ten_san_pham"]
)

assert (
    dong_gia["gia_ban"]
    == san_pham["gia_ban"]
)

print("TEST 47 PASSED")


# ============================================================
# TEST 48 - KHÔNG CHO GIÁ BÁN ÂM
# ============================================================

try:

    sua_gia_ban_niem_yet(
        danh_sach_san_pham,
        "SP-0001",
        -1000
    )

    assert False

except ValueError:

    pass

print("TEST 48 PASSED")


# ============================================================
# TEST 49 - SẢN PHẨM KHÔNG TỒN TẠI
# ============================================================

try:

    sua_gia_ban_niem_yet(
        danh_sach_san_pham,
        "SP-9999",
        10000
    )

    assert False

except ValueError:

    pass

print("TEST 49 PASSED")


# ============================================================
# NHÓM TEST BẢNG GIÁ PHÂN KHÚC
# ============================================================

# TEST 50 - TẠO BẢNG GIÁ

danh_sach_bang_gia_phan_khuc.clear()


bang_gia_khach_si = them_bang_gia_phan_khuc(
    "BG-KS",
    "Bảng giá khách sỉ"
)


assert bang_gia_khach_si["ma_bang_gia"] == "BG-KS"

assert (
    bang_gia_khach_si["ten_bang_gia"]
    == "Bảng giá khách sỉ"
)

assert (
    bang_gia_khach_si["danh_sach_san_pham"]
    == []
)

print("TEST 50 PASSED")


# ============================================================
# TEST 51 - KHÔNG TẠO TRÙNG
# ============================================================

try:

    them_bang_gia_phan_khuc(
        "BG-KS",
        "Bảng giá trùng"
    )

    assert False

except ValueError:

    pass

print("TEST 51 PASSED")


# ============================================================
# TEST 52 - THÊM SẢN PHẨM
# ============================================================

dong_gia_niem_yet = tim_gia_niem_yet(
    "SP-0001"
)


dong_gia_phan_khuc = (
    them_san_pham_vao_bang_gia_phan_khuc(
        bang_gia_khach_si,
        dong_gia_niem_yet
    )
)


assert (
    dong_gia_phan_khuc["ma_san_pham"]
    == "SP-0001"
)

assert (
    dong_gia_phan_khuc["gia_von"]
    == 10000
)

assert (
    dong_gia_phan_khuc["gia_niem_yet"]
    == 20000
)

assert (
    dong_gia_phan_khuc["gia_ban"]
    == 20000
)

print("TEST 52 PASSED")


# ============================================================
# TEST 53 - KHÔNG THÊM TRÙNG SẢN PHẨM
# ============================================================

dong_gia_trung = (
    them_san_pham_vao_bang_gia_phan_khuc(
        bang_gia_khach_si,
        dong_gia_niem_yet
    )
)


assert dong_gia_trung is dong_gia_phan_khuc

assert (
    len(
        bang_gia_khach_si["danh_sach_san_pham"]
    )
    == 1
)

print("TEST 53 PASSED")


# ============================================================
# TEST 54 - ĐỒNG BỘ TỪ GIÁ NIÊM YẾT
# ============================================================

dong_gia_niem_yet["gia_von"] = 11000
dong_gia_niem_yet["gia_ban"] = 22000


dong_bo_tu_gia_niem_yet(
    bang_gia_khach_si,
    danh_sach_gia_niem_yet
)


assert (
    dong_gia_phan_khuc["gia_von"]
    == 11000
)

assert (
    dong_gia_phan_khuc["gia_niem_yet"]
    == 22000
)

print("TEST 54 PASSED")


# ============================================================
# TEST 55 - XÓA SẢN PHẨM KHỎI BẢNG
# ============================================================

xoa_san_pham_khoi_bang_gia(
    bang_gia_khach_si,
    "SP-0001"
)


assert (
    tim_san_pham_trong_bang_gia(
        bang_gia_khach_si,
        "SP-0001"
    )
    is None
)

print("TEST 55 PASSED")


# ============================================================
# TEST 56 - ĐỒNG BỘ KHÔNG TỰ THÊM LẠI
# ============================================================

dong_bo_tu_gia_niem_yet(
    bang_gia_khach_si,
    danh_sach_gia_niem_yet
)


assert (
    tim_san_pham_trong_bang_gia(
        bang_gia_khach_si,
        "SP-0001"
    )
    is None
)

print("TEST 56 PASSED")


# ============================================================
# TEST 57 - CHỦ ĐỘNG THÊM LẠI
# ============================================================

dong_gia_phan_khuc = them_lai_san_pham(
    bang_gia_khach_si,
    dong_gia_niem_yet
)


assert (
    dong_gia_phan_khuc["ma_san_pham"]
    == "SP-0001"
)

assert dong_gia_phan_khuc["gia_von"] == 11000
assert dong_gia_phan_khuc["gia_niem_yet"] == 22000

print("TEST 57 PASSED")


# ============================================================
# TEST 58 - SỬA GIÁ BÁN THỦ CÔNG
# ============================================================

cap_nhat_gia_ban(
    bang_gia_khach_si,
    "SP-0001",
    25000
)


assert dong_gia_phan_khuc["gia_ban"] == 25000

print("TEST 58 PASSED")


# ============================================================
# TEST 59 - KHÔNG CHO GIÁ BÁN ÂM
# ============================================================

try:

    cap_nhat_gia_ban(
        bang_gia_khach_si,
        "SP-0001",
        -1
    )

    assert False

except ValueError:

    pass

print("TEST 59 PASSED")


# ============================================================
# TEST 60 - CỘNG SỐ TIỀN
# ============================================================

cau_hinh_cong_them = {
    "gia_co_so": "gia_von",
    "phep_tinh": "+",
    "don_vi": "gia_tri",
    "gia_tri": 5000,
}


gia = tinh_gia_theo_cau_hinh(
    dong_gia_phan_khuc,
    cau_hinh_cong_them
)


assert gia == 16000

print("TEST 60 PASSED")


# ============================================================
# TEST 61 - CỘNG THEO %
# ============================================================

cau_hinh_cong_phan_tram = {
    "gia_co_so": "gia_von",
    "phep_tinh": "+",
    "don_vi": "%",
    "gia_tri": 20,
}


gia = tinh_gia_theo_cau_hinh(
    dong_gia_phan_khuc,
    cau_hinh_cong_phan_tram
)


assert gia == 13200

print("TEST 61 PASSED")


# ============================================================
# TEST 62 - GIẢM TIỀN
# ============================================================

cau_hinh_giam_tien = {
    "gia_co_so": "gia_niem_yet",
    "phep_tinh": "-",
    "don_vi": "gia_tri",
    "gia_tri": 2000,
}


gia = tinh_gia_theo_cau_hinh(
    dong_gia_phan_khuc,
    cau_hinh_giam_tien
)


assert gia == 20000

print("TEST 62 PASSED")


# ============================================================
# TEST 63 - GIẢM %
# ============================================================

cau_hinh_giam_phan_tram = {
    "gia_co_so": "gia_niem_yet",
    "phep_tinh": "-",
    "don_vi": "%",
    "gia_tri": 10,
}


gia = tinh_gia_theo_cau_hinh(
    dong_gia_phan_khuc,
    cau_hinh_giam_phan_tram
)


assert gia == 19800

print("TEST 63 PASSED")


# ============================================================
# TEST 64 - NHÂN HỆ SỐ
# ============================================================

cau_hinh_nhan_he_so = {
    "gia_co_so": "gia_von",
    "phep_tinh": "*",
    "don_vi": "he_so",
    "gia_tri": 1.2,
}


gia = tinh_gia_theo_cau_hinh(
    dong_gia_phan_khuc,
    cau_hinh_nhan_he_so
)


assert gia == 13200

print("TEST 64 PASSED")


# ============================================================
# TEST 65 - ÁP DỤNG CHO TOÀN BỘ
# ============================================================

cau_hinh = {
    "gia_co_so": "gia_von",
    "phep_tinh": "+",
    "don_vi": "gia_tri",
    "gia_tri": 3000,
}


ap_dung_cau_hinh_tinh_gia(
    bang_gia_khach_si,
    cau_hinh
)


assert dong_gia_phan_khuc["gia_ban"] == 14000

print("TEST 65 PASSED")


# ============================================================
# TEST 66 - ÁP DỤNG CHO SẢN PHẨM ĐƯỢC CHỌN
# ============================================================

cau_hinh_moi = {
    "gia_co_so": "gia_niem_yet",
    "phep_tinh": "-",
    "don_vi": "%",
    "gia_tri": 10,
}


ap_dung_cau_hinh_tinh_gia(
    bang_gia_khach_si,
    cau_hinh_moi,
    ["SP-0001"]
)


assert dong_gia_phan_khuc["gia_ban"] == 19800

print("TEST 66 PASSED")


# ============================================================
# TEST 67 - PHÉP TÍNH KHÔNG HỢP LỆ
# ============================================================

try:

    tinh_gia_theo_cau_hinh(
        dong_gia_phan_khuc,
        {
            "gia_co_so": "gia_von",
            "phep_tinh": "/",
            "don_vi": "gia_tri",
            "gia_tri": 2,
        }
    )

    assert False

except ValueError:

    pass

print("TEST 67 PASSED")


# ============================================================
# TEST 68 - XÓA BẢNG GIÁ
# ============================================================

xoa_bang_gia_phan_khuc(
    "BG-KS"
)


assert (
    tim_bang_gia_phan_khuc("BG-KS")
    is None
)

print("TEST 68 PASSED")


# ============================================================
# NHÓM TEST BÁO GIÁ
# ============================================================

# TEST 69 - TẠO MẪU BÁO GIÁ

mau_bao_gia = tao_mau_bao_gia(
    "BG20260926-0001"
)


assert (
    mau_bao_gia["ma_bao_gia"]
    == "BG20260926-0001"
)

assert mau_bao_gia["ma_khach_hang"] == ""
assert mau_bao_gia["ten_khach_hang"] == ""
assert mau_bao_gia["ghi_chu"] == ""
assert mau_bao_gia["chi_tiet"] == []

print("TEST 69 PASSED")


# ============================================================
# TEST 70 - CHƯA LƯU
# ============================================================

assert (
    tim_mau_bao_gia("BG20260926-0001")
    is None
)

print("TEST 70 PASSED")


# ============================================================
# TEST 71 - CHIẾT KHẤU
# ============================================================

chi_tiet_bao_gia_1 = tao_chi_tiet_bao_gia(
    san_pham,
    "CHIET KHAU",
    chiet_khau=10
)


assert (
    chi_tiet_bao_gia_1["ma_san_pham"]
    == "SP-0001"
)

assert (
    chi_tiet_bao_gia_1["gia_niem_yet"]
    == 20000
)

assert (
    chi_tiet_bao_gia_1["chiet_khau"]
    == 10
)

assert (
    chi_tiet_bao_gia_1["don_gia_sau_chiet_khau"]
    == 18000
)

print("TEST 71 PASSED")


# ============================================================
# TEST 72 - THÊM VÀO BÁO GIÁ
# ============================================================

them_chi_tiet_vao_mau_bao_gia(
    mau_bao_gia,
    chi_tiet_bao_gia_1
)


assert len(mau_bao_gia["chi_tiet"]) == 1

assert (
    mau_bao_gia["chi_tiet"][0]["ma_san_pham"]
    == "SP-0001"
)

assert (
    mau_bao_gia["chi_tiet"][0]
    ["don_gia_sau_chiet_khau"]
    == 18000
)

print("TEST 72 PASSED")


# ============================================================
# TEST 73 - CHIA THẲNG
# ============================================================

chi_tiet_bao_gia_2 = tao_chi_tiet_bao_gia(
    san_pham,
    "CHIA THANG",
    don_gia_sau_chiet_khau=12000
)


assert (
    chi_tiet_bao_gia_2["loai_gia"]
    == "CHIA THANG"
)

assert (
    chi_tiet_bao_gia_2["gia_niem_yet"]
    is None
)

assert (
    chi_tiet_bao_gia_2["chiet_khau"]
    is None
)

assert (
    chi_tiet_bao_gia_2["don_gia_sau_chiet_khau"]
    == 12000
)

print("TEST 73 PASSED")


# ============================================================
# TEST 74 - KHÔNG TRÙNG SẢN PHẨM
# ============================================================

try:

    them_chi_tiet_vao_mau_bao_gia(
        mau_bao_gia,
        chi_tiet_bao_gia_2
    )

    assert False

except ValueError:

    pass

print("TEST 74 PASSED")


# ============================================================
# TEST 75 - CHIẾT KHẤU NGOÀI 0-100
# ============================================================

try:

    tao_chi_tiet_bao_gia(
        san_pham,
        "CHIET KHAU",
        chiet_khau=101
    )

    assert False

except ValueError:

    pass


try:

    tao_chi_tiet_bao_gia(
        san_pham,
        "CHIET KHAU",
        chiet_khau=-1
    )

    assert False

except ValueError:

    pass

print("TEST 75 PASSED")


# ============================================================
# TEST 76 - GIÁ CHIA THẲNG KHÔNG HỢP LỆ
# ============================================================

try:

    tao_chi_tiet_bao_gia(
        san_pham,
        "CHIA THANG",
        don_gia_sau_chiet_khau=0
    )

    assert False

except ValueError:

    pass


try:

    tao_chi_tiet_bao_gia(
        san_pham,
        "CHIA THANG",
        don_gia_sau_chiet_khau=-1000
    )

    assert False

except ValueError:

    pass

print("TEST 76 PASSED")


# ============================================================
# TEST 77 - LOẠI GIÁ KHÔNG HỢP LỆ
# ============================================================

try:

    tao_chi_tiet_bao_gia(
        san_pham,
        "LOAI GIA KHONG TON TAI",
        don_gia_sau_chiet_khau=10000
    )

    assert False

except ValueError:

    pass

print("TEST 77 PASSED")


# ============================================================
# TEST 78 - THÊM SẢN PHẨM THỨ HAI
# ============================================================

san_pham_2 = tao_san_pham(
    ["SP-0002"],
    "VAT-0002",
    "Sản phẩm test 2",
    "Danh mục test",
    "Cái",
    0,
    25000,
    []
)


chi_tiet_bao_gia_3 = tao_chi_tiet_bao_gia(
    san_pham_2,
    "CHIA THANG",
    don_gia_sau_chiet_khau=23000
)


them_chi_tiet_vao_mau_bao_gia(
    mau_bao_gia,
    chi_tiet_bao_gia_3
)


assert len(mau_bao_gia["chi_tiet"]) == 2

assert (
    mau_bao_gia["chi_tiet"][1]["ma_san_pham"]
    == "SP-0002"
)

print("TEST 78 PASSED")


# ============================================================
# TEST 79 - SỬA CHIẾT KHẤU
# ============================================================

sua_chi_tiet_bao_gia(
    mau_bao_gia,
    0,
    loai_gia="CHIET KHAU",
    chiet_khau=20
)


assert (
    mau_bao_gia["chi_tiet"][0]["gia_niem_yet"]
    == 20000
)

assert (
    mau_bao_gia["chi_tiet"][0]["chiet_khau"]
    == 20
)

assert (
    mau_bao_gia["chi_tiet"][0]
    ["don_gia_sau_chiet_khau"]
    == 16000
)

print("TEST 79 PASSED")


# ============================================================
# TEST 80 - SỬA CHIA THẲNG
# ============================================================

sua_chi_tiet_bao_gia(
    mau_bao_gia,
    1,
    loai_gia="CHIA THANG",
    don_gia_sau_chiet_khau=22000
)


assert (
    mau_bao_gia["chi_tiet"][1]["loai_gia"]
    == "CHIA THANG"
)

assert (
    mau_bao_gia["chi_tiet"][1]["gia_niem_yet"]
    is None
)

assert (
    mau_bao_gia["chi_tiet"][1]["chiet_khau"]
    is None
)

assert (
    mau_bao_gia["chi_tiet"][1]
    ["don_gia_sau_chiet_khau"]
    == 22000
)

print("TEST 80 PASSED")


# ============================================================
# TEST 81 - XÓA DÒNG
# ============================================================

xoa_chi_tiet_bao_gia(
    mau_bao_gia,
    1
)


assert len(mau_bao_gia["chi_tiet"]) == 1

assert (
    mau_bao_gia["chi_tiet"][0]["ma_san_pham"]
    == "SP-0001"
)

print("TEST 81 PASSED")


# ============================================================
# TEST 82 - KHÔNG LƯU BÁO GIÁ RỖNG
# ============================================================

mau_bao_gia_rong = tao_mau_bao_gia(
    "BG20260926-0002"
)


try:

    luu_mau_bao_gia(
        mau_bao_gia_rong
    )

    assert False

except ValueError:

    pass

print("TEST 82 PASSED")


# ============================================================
# TEST 83 - LƯU BÁO GIÁ
# ============================================================

mau_bao_gia["ma_khach_hang"] = "KH-0001"
mau_bao_gia["ten_khach_hang"] = "Khách hàng test"
mau_bao_gia["ghi_chu"] = "Báo giá tháng 09/2026"


luu_mau_bao_gia(
    mau_bao_gia
)


assert len(danh_sach_mau_bao_gia) == 1


bao_gia_da_luu = tim_mau_bao_gia(
    "BG20260926-0001"
)


assert bao_gia_da_luu is not None

assert (
    bao_gia_da_luu["ma_khach_hang"]
    == "KH-0001"
)

assert (
    bao_gia_da_luu["chi_tiet"][0]
    ["don_gia_sau_chiet_khau"]
    == 16000
)

print("TEST 83 PASSED")


# ============================================================
# TEST 84 - KHÔNG LƯU TRÙNG
# ============================================================

mau_bao_gia_trung = tao_mau_bao_gia(
    "BG20260926-0001"
)


mau_bao_gia_trung["chi_tiet"].append(
    chi_tiet_bao_gia_1.copy()
)


try:

    luu_mau_bao_gia(
        mau_bao_gia_trung
    )

    assert False

except ValueError:

    pass

print("TEST 84 PASSED")


# ============================================================
# TEST 85 - SỬA BÁO GIÁ ĐÃ LƯU
# ============================================================

mau_bao_gia_sua = sua_mau_bao_gia(
    "BG20260926-0001"
)


assert (
    mau_bao_gia_sua
    is not bao_gia_da_luu
)


mau_bao_gia_sua["ghi_chu"] = (
    "Đã cập nhật báo giá"
)


sua_chi_tiet_bao_gia(
    mau_bao_gia_sua,
    0,
    loai_gia="CHIET KHAU",
    chiet_khau=5
)


assert (
    mau_bao_gia_sua["chi_tiet"][0]
    ["chiet_khau"]
    == 5
)

assert (
    mau_bao_gia_sua["chi_tiet"][0]
    ["don_gia_sau_chiet_khau"]
    == 19000
)


xac_nhan_luu_mau_bao_gia(
    mau_bao_gia_sua
)


bao_gia_sau_khi_sua = tim_mau_bao_gia(
    "BG20260926-0001"
)


assert (
    bao_gia_sau_khi_sua["ghi_chu"]
    == "Đã cập nhật báo giá"
)

assert (
    bao_gia_sau_khi_sua["chi_tiet"][0]
    ["chiet_khau"]
    == 5
)

assert (
    bao_gia_sau_khi_sua["chi_tiet"][0]
    ["don_gia_sau_chiet_khau"]
    == 19000
)

print("TEST 85 PASSED")


# ============================================================
# NHÓM TEST GIÁ VỐN GNTT
# ============================================================

# Giá vốn lấy từ bảng giá niêm yết
# và được chốt vào phiếu tại thời điểm lưu.

def tinh_gia_von_tu_bang_gia_niem_yet(
    phieu,
    danh_sach_ton_kho
):

    for chi_tiet in phieu["chi_tiet"]:

        dong_gia = tim_gia_niem_yet(
            chi_tiet["ma_san_pham"]
        )

        if dong_gia is None:

            raise ValueError(
                f"Không tìm thấy giá vốn "
                f"của sản phẩm "
                f"'{chi_tiet['ma_san_pham']}'"
            )

        don_gia_von = dong_gia["gia_von"]

        chi_tiet["don_gia_von"] = don_gia_von

        chi_tiet["thanh_tien_von"] = (
            chi_tiet["so_luong_quy_doi"]
            * don_gia_von
        )

    return phieu


# ============================================================
# TEST 86 - GNTT CHỐT GIÁ VỐN
# ============================================================

cap_nhat_gia_von(
    danh_sach_phieu_nhap,
    "SP-0001"
)


assert (
    tim_gia_niem_yet("SP-0001")
    ["gia_von"]
    == 10000
)


phieu_cost_1 = tao_phieu_gntt(
    "GNTT260926-C01"
)


chi_tiet_cost_1 = tao_chi_tiet_ban(
    san_pham,
    "KHO-01",
    san_pham["dvt_chinh"],
    10,
    "CHIET KHAU",
    20000,
    0
)


them_chi_tiet_vao_phieu_ban(
    danh_sach_san_pham,
    phieu_cost_1,
    chi_tiet_cost_1
)


luu_phieu_gntt(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_cost_1,
    tinh_gia_von_tu_bang_gia_niem_yet
)


assert (
    phieu_cost_1["chi_tiet"][0]
    ["don_gia_von"]
    == 10000
)

assert (
    phieu_cost_1["chi_tiet"][0]
    ["thanh_tien_von"]
    == 100000
)

assert (
    phieu_cost_1["tong_thanh_tien_von"]
    == 100000
)

assert (
    phieu_cost_1["loi_nhuan"]
    == 100000
)

assert (
    phieu_cost_1["ty_suat"]
    == 50
)

print("TEST 86 PASSED")


# ============================================================
# TEST 87 - PHIẾU CŨ KHÔNG ĐỔI GIÁ VỐN
# ============================================================

tim_gia_niem_yet(
    "SP-0001"
)["gia_von"] = 15000


phieu_cost_da_luu = tim_phieu_gntt(
    "GNTT260926-C01"
)


assert (
    phieu_cost_da_luu["chi_tiet"][0]
    ["don_gia_von"]
    == 10000
)

assert (
    phieu_cost_da_luu["chi_tiet"][0]
    ["thanh_tien_von"]
    == 100000
)

assert (
    phieu_cost_da_luu["tong_thanh_tien_von"]
    == 100000
)

print("TEST 87 PASSED")


# ============================================================
# TEST 88 - GNTT MỚI LẤY GIÁ VỐN MỚI
# ============================================================

phieu_cost_2 = tao_phieu_gntt(
    "GNTT260926-C02"
)


chi_tiet_cost_2 = tao_chi_tiet_ban(
    san_pham,
    "KHO-01",
    san_pham["dvt_chinh"],
    5,
    "CHIET KHAU",
    20000,
    0
)


them_chi_tiet_vao_phieu_ban(
    danh_sach_san_pham,
    phieu_cost_2,
    chi_tiet_cost_2
)


luu_phieu_gntt(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_cost_2,
    tinh_gia_von_tu_bang_gia_niem_yet
)


assert (
    phieu_cost_2["chi_tiet"][0]
    ["don_gia_von"]
    == 15000
)

assert (
    phieu_cost_2["chi_tiet"][0]
    ["thanh_tien_von"]
    == 75000
)

print("TEST 88 PASSED")


# ============================================================
# TEST 89 - SỬA GNTT VÀ CHỐT LẠI GIÁ VỐN
# ============================================================

phieu_cost_2_sua = load_phieu_gntt(
    "GNTT260926-C02"
)


sua_dong_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_cost_2_sua,
    0,
    {
        "so_luong": 10
    }
)


xac_nhan_luu_phieu_gntt(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_cost_2_sua,
    tinh_gia_von_tu_bang_gia_niem_yet
)


assert (
    phieu_cost_2_sua["chi_tiet"][0]
    ["don_gia_von"]
    == 15000
)

assert (
    phieu_cost_2_sua["chi_tiet"][0]
    ["thanh_tien_von"]
    == 150000
)

assert (
    phieu_cost_2_sua["tong_thanh_tien_von"]
    == 150000
)

print("TEST 89 PASSED")


# ============================================================
# TEST 90 - LOAD GNTT SAU UPDATE
# ============================================================

phieu_cost_2_load = load_phieu_gntt(
    "GNTT260926-C02"
)


assert phieu_cost_2_load["_da_load"] is True
assert phieu_cost_2_load["_da_thay_doi"] is False

assert (
    phieu_cost_2_load["chi_tiet"][0]
    ["so_luong"]
    == 10
)

assert (
    phieu_cost_2_load["chi_tiet"][0]
    ["don_gia_von"]
    == 15000
)

assert (
    phieu_cost_2_load["chi_tiet"][0]
    ["thanh_tien_von"]
    == 150000
)

print("TEST 90 PASSED")


# ============================================================
# KẾT QUẢ
# ============================================================

print("=" * 60)
print("TẤT CẢ TEST 1-90 ĐỀU PASSED")
print("=" * 60)