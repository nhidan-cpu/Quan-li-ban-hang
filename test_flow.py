# ============================================================
# TEST FLOW: NHẬP HÀNG → KHO
# ============================================================

from thao_tac_nhap_hang import (
    danh_sach_phieu_nhap,
    tao_phieu_nhap,
    tao_chi_tiet_nhap,
    them_chi_tiet_vao_phieu_nhap,
    luu_phieu_nhap,
    sua_phieu_nhap,
    sua_dong_chi_tiet_phieu_nhap,
    xac_nhan_luu,
)

from thao_tac_kho import (
    khoi_tao_danh_sach_ton_kho,
    tim_ton_kho,
)


# ============================================================
# 1. DỮ LIỆU TEST
# ============================================================

danh_sach_san_pham = [
    {
        "ma_san_pham": ["SP001"],
        "ma_vat": "VAT001",
        "ten_san_pham": "Sản phẩm A",
        "danh_muc": "Hàng hóa",
        "dvt_chinh": "Cái",
        "gia_nhap": 0,
        "gia_ban": 0,
        "dvt_quy_doi": [],
    }
]


danh_sach_kho = [
    {
        "ma_kho": "KHO01",
        "ten_kho": "Kho chính",
        "dia_chi": "123 Nguyễn Trãi",
    }
]


# ============================================================
# 2. DANH SÁCH TỒN KHO TEST
# ============================================================

danh_sach_ton_kho = []


# ============================================================
# 3. KHỞI TẠO TỒN KHO
# ============================================================

khoi_tao_danh_sach_ton_kho(
    danh_sach_ton_kho,
    danh_sach_san_pham,
    danh_sach_kho,
)


# ============================================================
# TEST 1: TỒN KHO BAN ĐẦU
# ============================================================

print("\n===== TEST 1: TỒN KHO BAN ĐẦU =====")

ton = tim_ton_kho(
    danh_sach_ton_kho,
    "KHO01",
    "SP001",
)

print(ton)

assert ton is not None
assert ton["ma_kho"] == "KHO01"
assert ton["ma_san_pham"] == "SP001"
assert ton["ma_vat"] == "VAT001"
assert ton["ten_san_pham"] == "Sản phẩm A"
assert ton["dvt_chinh"] == "Cái"
assert ton["so_luong_ton"] == 0
assert ton["gia_tri_ton"] == 0
assert ton["gia_von_binh_quan"] == 0

print("PASS")


# ============================================================
# 4. TẠO PHIẾU NHẬP TEST
# ============================================================

phieu = tao_phieu_nhap(
    "PN230926-0001"
)

phieu["ma_kho_nhap"] = "KHO01"


# ============================================================
# 5. TẠO CHI TIẾT PHIẾU NHẬP
# ============================================================

chi_tiet = tao_chi_tiet_nhap(
    danh_sach_san_pham[0],
    "Cái",
    100,
    "CHIA THANG",
    10000,
    0,
)


them_chi_tiet_vao_phieu_nhap(
    danh_sach_san_pham,
    phieu,
    chi_tiet,
)


# ============================================================
# TEST 2: LƯU PHIẾU NHẬP → CẬP NHẬT KHO
# ============================================================

print("\n===== TEST 2: LƯU PHIẾU NHẬP =====")

ket_qua = luu_phieu_nhap(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu,
)

assert ket_qua is True


ton = tim_ton_kho(
    danh_sach_ton_kho,
    "KHO01",
    "SP001",
)

print(ton)

assert ton["so_luong_ton"] == 100
assert ton["gia_tri_ton"] == 1000000
assert ton["gia_von_binh_quan"] == 10000

print("PASS")


# ============================================================
# TEST 3: KIỂM TRA PHIẾU ĐÃ ĐƯỢC LƯU
# ============================================================

print("\n===== TEST 3: KIỂM TRA DANH SÁCH PHIẾU =====")

assert len(danh_sach_phieu_nhap) == 1

assert (
    danh_sach_phieu_nhap[0]["ma_phieu_nhap"]
    == "PN230926-0001"
)

print("Số phiếu đang lưu:", len(danh_sach_phieu_nhap))
print("PASS")


# ============================================================
# 6. TẠO BẢN NHÁP SỬA PHIẾU
# ============================================================

phieu_nhap_sua = sua_phieu_nhap(
    phieu
)


# ============================================================
# 7. SỬA SỐ LƯỢNG
# ============================================================

sua_dong_chi_tiet_phieu_nhap(
    danh_sach_san_pham,
    phieu_nhap_sua,
    0,
    {
        "so_luong": 120,
    },
)


# ============================================================
# TEST 4: XÁC NHẬN SỬA PHIẾU
# ============================================================

print("\n===== TEST 4: SỬA PHIẾU 100 → 120 =====")

phieu_sau_khi_sua = xac_nhan_luu(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu_nhap_sua,
)

assert phieu_sau_khi_sua is not None


ton = tim_ton_kho(
    danh_sach_ton_kho,
    "KHO01",
    "SP001",
)

print(ton)

assert ton["so_luong_ton"] == 120
assert ton["gia_tri_ton"] == 1200000
assert ton["gia_von_binh_quan"] == 10000

print("PASS")


# ============================================================
# TEST 5: PHIẾU CŨ ĐÃ ĐƯỢC THAY THẾ
# ============================================================

print("\n===== TEST 5: KIỂM TRA PHIẾU SAU KHI SỬA =====")

assert len(danh_sach_phieu_nhap) == 1

phieu_da_luu = danh_sach_phieu_nhap[0]

assert (
    phieu_da_luu["ma_phieu_nhap"]
    == "PN230926-0001"
)

assert (
    phieu_da_luu["chi_tiet"][0]["so_luong"]
    == 120
)

print(
    "Số lượng trên phiếu:",
    phieu_da_luu["chi_tiet"][0]["so_luong"],
)

print("PASS")


# ============================================================
# TEST 6: KIỂM TRA KHÔNG CỘNG TRÙNG
# ============================================================

print("\n===== TEST 6: KIỂM TRA KHÔNG CỘNG TRÙNG =====")

print(
    "Số lượng tồn cuối cùng:",
    ton["so_luong_ton"],
)

assert ton["so_luong_ton"] == 120
assert ton["so_luong_ton"] != 220

assert ton["gia_tri_ton"] == 1200000
assert ton["gia_tri_ton"] != 2200000

print("PASS")


# ============================================================
# KẾT QUẢ CUỐI CÙNG
# ============================================================

print("\n========================================")
print("TẤT CẢ TEST FLOW ĐỀU PASS")
print("========================================")