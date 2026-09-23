from datetime import datetime
from copy import deepcopy

from thao_tac_danh_sach_san_pham import (
    lay_he_so_quy_doi,
    tim_san_pham
)

from thao_tac_kho import (
    tim_ton_kho,
    cap_nhat_ton_kho_tu_chi_tiet
)


# ============================================================
# 1. CẤU TRÚC DỮ LIỆU
# ============================================================

# Cấu trúc phiếu bán
phieu_ban = {
    "ma_phieu": "",
    "ngay_lap": "",
    "ma_khach_hang": "",
    "ten_khach_hang": "",
    "chi_tiet": [],
    "tong_thanh_tien": 0
}


# Cấu trúc chi tiết phiếu bán
chi_tiet_ban = {
    "stt": 0,
    "ma_kho": "",
    "ma_san_pham": "",
    "ten_san_pham": "",
    "dvt_ban": "",
    "so_luong": 0,
    "he_so_quy_doi": 0,
    "so_luong_quy_doi": 0,
    "don_gia": 0,
    "loai_gia": "",
    "ck": 0,
    "don_gia_sau_ck": 0,
    "thanh_tien_tung_dong": 0
}


# Danh sách phiếu bán
danh_sach_phieu_ban = []


# ============================================================
# 2. TẠO PHIẾU BÁN
# ============================================================

# Tạo phiếu bán mới
def tao_phieu_ban(ma_phieu):

    return {
        "ma_phieu": ma_phieu,
        "ngay_lap": datetime.now(),
        "ma_khach_hang": "",
        "ten_khach_hang": "",
        "chi_tiet": [],
        "tong_thanh_tien": 0
    }


# Tạo chi tiết phiếu bán
def tao_chi_tiet_ban(
    san_pham,
    ma_kho,
    dvt_ban,
    so_luong,
    loai_gia,
    don_gia=0,
    ck=0,
    don_gia_sau_ck=0
):

    # Lấy hệ số quy đổi
    he_so_quy_doi = lay_he_so_quy_doi(
        san_pham,
        dvt_ban
    )

    if he_so_quy_doi is None:

        raise ValueError(
            f"ĐVT '{dvt_ban}' "
            f"không tồn tại trong sản phẩm"
        )

    # Tính số lượng theo DVT chính
    so_luong_quy_doi = (
        so_luong * he_so_quy_doi
    )

    # Nếu chia thẳng
    if loai_gia == "CHIA THANG":

        # Hai ô này bị khóa trên giao diện
        don_gia = 0
        ck = 0

        # Giá được nhập trực tiếp
        if don_gia_sau_ck <= 0:

            raise ValueError(
                "Giá chia thẳng phải lớn hơn 0"
            )

    # Nếu chiết khấu
    elif loai_gia == "CHIET KHAU":

        if don_gia <= 0:

            raise ValueError(
                "Đơn giá phải lớn hơn 0"
            )

        if ck < 0 or ck > 100:

            raise ValueError(
                "Chiết khấu phải từ 0 đến 100"
            )

        don_gia_sau_ck = (
            don_gia * (1 - ck / 100)
        )

    else:

        raise ValueError(
            f"Loại giá không hợp lệ: {loai_gia}"
        )

    # Tính thành tiền
    thanh_tien_tung_dong = (
        so_luong * don_gia_sau_ck
    )

    return {
        "stt": 0,
        "ma_kho": ma_kho,
        "ma_san_pham": san_pham["ma_san_pham"][0],
        "ten_san_pham": san_pham["ten_san_pham"],
        "dvt_ban": dvt_ban,
        "so_luong": so_luong,
        "he_so_quy_doi": he_so_quy_doi,
        "so_luong_quy_doi": so_luong_quy_doi,
        "don_gia": don_gia,
        "loai_gia": loai_gia,
        "ck": ck,
        "don_gia_sau_ck": don_gia_sau_ck,
        "thanh_tien_tung_dong": thanh_tien_tung_dong
    }


# ============================================================
# 3. TÍNH TOÁN CHI TIẾT
# ============================================================

# Tính lại một dòng chi tiết phiếu bán
def tinh_lai_chi_tiet_ban(
    san_pham,
    chi_tiet
):

    # Lấy lại hệ số quy đổi
    he_so_quy_doi = lay_he_so_quy_doi(
        san_pham,
        chi_tiet["dvt_ban"]
    )

    if he_so_quy_doi is None:

        raise ValueError(
            f"ĐVT '{chi_tiet['dvt_ban']}' "
            f"không tồn tại trong sản phẩm"
        )

    chi_tiet["he_so_quy_doi"] = he_so_quy_doi

    # Tính số lượng theo DVT chính
    chi_tiet["so_luong_quy_doi"] = (
        chi_tiet["so_luong"]
        * he_so_quy_doi
    )

    # Tính giá
    if chi_tiet["loai_gia"] == "CHIA THANG":

        # Đơn giá và CK bị khóa
        chi_tiet["don_gia"] = 0
        chi_tiet["ck"] = 0

        if chi_tiet["don_gia_sau_ck"] <= 0:

            raise ValueError(
                "Giá chia thẳng phải lớn hơn 0"
            )

    elif chi_tiet["loai_gia"] == "CHIET KHAU":

        if chi_tiet["don_gia"] <= 0:

            raise ValueError(
                "Đơn giá phải lớn hơn 0"
            )

        if (
            chi_tiet["ck"] < 0
            or chi_tiet["ck"] > 100
        ):

            raise ValueError(
                "Chiết khấu phải từ 0 đến 100"
            )

        chi_tiet["don_gia_sau_ck"] = (
            chi_tiet["don_gia"]
            * (1 - chi_tiet["ck"] / 100)
        )

    else:

        raise ValueError(
            f"Loại giá không hợp lệ: "
            f"{chi_tiet['loai_gia']}"
        )

    # Tính thành tiền
    chi_tiet["thanh_tien_tung_dong"] = (
        chi_tiet["so_luong"]
        * chi_tiet["don_gia_sau_ck"]
    )

    return chi_tiet


# Tính tổng thành tiền
def tinh_tong_thanh_tien(phieu):

    return sum(
        chi_tiet["thanh_tien_tung_dong"]
        for chi_tiet in phieu["chi_tiet"]
    )


# Cập nhật tổng thành tiền
def cap_nhat_tong_thanh_tien(phieu):

    phieu["tong_thanh_tien"] = (
        tinh_tong_thanh_tien(phieu)
    )

    return phieu


# Tính lại toàn bộ phiếu bán
def cap_nhat_tinh_toan_phieu_ban(
    danh_sach_san_pham,
    phieu
):

    for chi_tiet in phieu["chi_tiet"]:

        # Tìm sản phẩm từ mã sản phẩm
        san_pham = tim_san_pham(
            danh_sach_san_pham,
            chi_tiet["ma_san_pham"]
        )

        if san_pham is None:

            raise ValueError(
                f"Không tìm thấy sản phẩm "
                f"'{chi_tiet['ma_san_pham']}'"
            )

        # Cập nhật tên sản phẩm
        chi_tiet["ten_san_pham"] = (
            san_pham["ten_san_pham"]
        )

        # Tính lại dòng
        tinh_lai_chi_tiet_ban(
            san_pham,
            chi_tiet
        )

    # Cập nhật tổng phiếu
    cap_nhat_tong_thanh_tien(phieu)

    return phieu


# ============================================================
# 4. THÊM CHI TIẾT VÀO PHIẾU BÁN
# ============================================================

# Thêm một chi tiết vào phiếu bán
def them_chi_tiet_vao_phieu_ban(
    danh_sach_san_pham,
    phieu,
    chi_tiet
):

    # Kiểm tra sản phẩm
    san_pham = tim_san_pham(
        danh_sach_san_pham,
        chi_tiet["ma_san_pham"]
    )

    if san_pham is None:

        raise ValueError(
            f"Không tìm thấy sản phẩm "
            f"'{chi_tiet['ma_san_pham']}'"
        )

    # Tính lại dòng trước khi thêm
    tinh_lai_chi_tiet_ban(
        san_pham,
        chi_tiet
    )

    # STT tự động theo vị trí dòng
    chi_tiet["stt"] = (
        len(phieu["chi_tiet"]) + 1
    )

    # Thêm vào phiếu
    phieu["chi_tiet"].append(
        chi_tiet
    )

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(phieu)

    return phieu


# ============================================================
# 5. KIỂM TRA DỮ LIỆU PHIẾU BÁN
# ============================================================

# Kiểm tra phiếu bán
def kiem_tra_du_lieu_phieu_ban(phieu):

    # Phiếu phải có ít nhất một dòng hàng
    if not phieu["chi_tiet"]:

        print(
            "Lỗi: Phiếu bán phải có "
            "ít nhất một sản phẩm"
        )

        return False

    # Kiểm tra từng dòng
    for chi_tiet in phieu["chi_tiet"]:

        if not chi_tiet["ma_kho"]:

            print(
                "Lỗi: Dòng sản phẩm "
                f"'{chi_tiet['ma_san_pham']}' "
                "chưa chọn kho"
            )

            return False

        if chi_tiet["so_luong"] <= 0:

            print(
                "Lỗi: Số lượng bán phải "
                "lớn hơn 0"
            )

            return False

    return True


# ============================================================
# 6. KIỂM TRA TỒN KHO
# ============================================================

# Kiểm tra tồn kho cho toàn bộ phiếu bán
def kiem_tra_ton_kho_phieu_ban(
    danh_sach_ton_kho,
    phieu
):

    for chi_tiet in phieu["chi_tiet"]:

        ton = tim_ton_kho(
            danh_sach_ton_kho,
            chi_tiet["ma_kho"],
            chi_tiet["ma_san_pham"]
        )

        if ton is None:

            raise ValueError(
                f"Không tìm thấy tồn kho "
                f"của sản phẩm "
                f"'{chi_tiet['ma_san_pham']}' "
                f"tại kho "
                f"'{chi_tiet['ma_kho']}'"
            )

        if (
            ton["so_luong_ton"]
            < chi_tiet["so_luong_quy_doi"]
        ):

            raise ValueError(
                f"Không đủ tồn kho: "
                f"SP '{chi_tiet['ma_san_pham']}', "
                f"Kho '{chi_tiet['ma_kho']}', "
                f"Tồn {ton['so_luong_ton']}, "
                f"Cần {chi_tiet['so_luong_quy_doi']}"
            )

    return True


# ============================================================
# 7. ÁP DỤNG PHIẾU BÁN VÀO KHO
# ============================================================

# Trừ tồn kho theo từng dòng
def ap_dung_phieu_ban_vao_kho(
    danh_sach_ton_kho,
    phieu
):

    # Kiểm tra trước khi trừ
    kiem_tra_ton_kho_phieu_ban(
        danh_sach_ton_kho,
        phieu
    )

    for chi_tiet in phieu["chi_tiet"]:

        ton = tim_ton_kho(
            danh_sach_ton_kho,
            chi_tiet["ma_kho"],
            chi_tiet["ma_san_pham"]
        )

        # Giá trị tồn giảm theo giá vốn bình quân
        gia_tri_xuat = (
            chi_tiet["so_luong_quy_doi"]
            * ton["gia_von_binh_quan"]
        )

        # Trừ số lượng và giá trị tồn
        cap_nhat_ton_kho_tu_chi_tiet(
            ton,
            -chi_tiet["so_luong_quy_doi"],
            -gia_tri_xuat
        )


# ============================================================
# 8. LƯU PHIẾU BÁN MỚI
# ============================================================

# Lưu phiếu bán mới
def luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu
):

    # Kiểm tra dữ liệu
    if not kiem_tra_du_lieu_phieu_ban(phieu):

        return False

    # Tính lại toàn bộ phiếu
    cap_nhat_tinh_toan_phieu_ban(
        danh_sach_san_pham,
        phieu
    )

    # Kiểm tra tồn kho trước khi lưu
    kiem_tra_ton_kho_phieu_ban(
        danh_sach_ton_kho,
        phieu
    )

    # Cập nhật tồn kho
    ap_dung_phieu_ban_vao_kho(
        danh_sach_ton_kho,
        phieu
    )

    # Lưu phiếu
    danh_sach_phieu_ban.append(phieu)

    print("Lưu phiếu bán thành công")

    return True


# ============================================================
# 9. SỬA PHIẾU BÁN
# ============================================================

# Tạo bản nháp phiếu bán cần sửa
def sua_phieu_ban(phieu_can_sua):

    # Tạo bản sao độc lập
    phieu_ban = deepcopy(
        phieu_can_sua
    )

    return phieu_ban


# Sửa thông tin đầu phiếu
def sua_header_phieu_ban(
    phieu_ban,
    ngay_lap=None,
    ma_khach_hang=None,
    ten_khach_hang=None
):

    if ngay_lap is not None:

        phieu_ban["ngay_lap"] = ngay_lap

    if ma_khach_hang is not None:

        phieu_ban["ma_khach_hang"] = (
            ma_khach_hang
        )

    if ten_khach_hang is not None:

        phieu_ban["ten_khach_hang"] = (
            ten_khach_hang
        )

    return phieu_ban


# ============================================================
# 10. THÊM / SỬA / XÓA DÒNG KHI SỬA PHIẾU
# ============================================================

# Thêm dòng mới vào phiếu đang sửa
def them_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_ban,
    chi_tiet_moi
):

    # Kiểm tra sản phẩm
    san_pham = tim_san_pham(
        danh_sach_san_pham,
        chi_tiet_moi["ma_san_pham"]
    )

    if san_pham is None:

        raise ValueError(
            f"Không tìm thấy sản phẩm "
            f"'{chi_tiet_moi['ma_san_pham']}'"
        )

    # Tính lại dòng
    tinh_lai_chi_tiet_ban(
        san_pham,
        chi_tiet_moi
    )

    # Gán STT
    chi_tiet_moi["stt"] = (
        len(phieu_ban["chi_tiet"]) + 1
    )

    # Thêm dòng
    phieu_ban["chi_tiet"].append(
        chi_tiet_moi
    )

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(
        phieu_ban
    )

    return phieu_ban


# Sửa một dòng chi tiết
def sua_dong_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_ban,
    vi_tri,
    thay_doi
):

    # Lấy dòng cần sửa
    chi_tiet = (
        phieu_ban["chi_tiet"][vi_tri]
    )

    # Áp dụng thay đổi
    chi_tiet.update(thay_doi)

    # Tìm sản phẩm
    san_pham = tim_san_pham(
        danh_sach_san_pham,
        chi_tiet["ma_san_pham"]
    )

    if san_pham is None:

        raise ValueError(
            f"Không tìm thấy sản phẩm "
            f"'{chi_tiet['ma_san_pham']}'"
        )

    # Tính lại dòng
    tinh_lai_chi_tiet_ban(
        san_pham,
        chi_tiet
    )

    # Tính lại toàn bộ phiếu
    cap_nhat_tinh_toan_phieu_ban(
        danh_sach_san_pham,
        phieu_ban
    )

    return phieu_ban


# Xóa một dòng chi tiết
def xoa_chi_tiet_phieu_ban(
    phieu_ban,
    vi_tri
):

    # Xóa dòng
    del phieu_ban["chi_tiet"][vi_tri]

    # Đánh lại STT
    for vi_tri, chi_tiet in enumerate(
        phieu_ban["chi_tiet"],
        start=1
    ):

        chi_tiet["stt"] = vi_tri

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(
        phieu_ban
    )

    return phieu_ban