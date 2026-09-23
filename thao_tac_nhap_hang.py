from datetime import datetime
from copy import deepcopy

from thao_tac_danh_sach_san_pham import (lay_he_so_quy_doi, tim_san_pham)

from thao_tac_kho import (ap_dung_phieu_nhap_vao_kho, hoan_tac_phieu_nhap_vao_kho)

# ============================================================
# 1. CẤU TRÚC DỮ LIỆU
# ============================================================

# Cấu trúc phiếu nhập
phieu_nhap = {
    "ma_phieu_nhap": "",
    "ma_kho_nhap": "",
    "ngay_nhap": "",
    "nha_cung_cap": "",
    "ghi_chu": "",
    "chi_tiet": [],
    "tong_thanh_tien": 0
}


# Cấu trúc chi tiết phiếu nhập
chi_tiet_nhap = {
    "ma_san_pham": "",
    "ten_san_pham": "",
    "dvt_nhap": "",
    "so_luong": 0,
    "loai_gia": "",
    "don_gia": 0,
    "ck": 0,

    "he_so_quy_doi": 0,
    "so_luong_quy_doi": 0,
    "don_gia_sau_ck": 0,
    "thanh_tien_tung_dong": 0
}


# ============================================================
# 2. TẠO PHIẾU NHẬP
# ============================================================

# Tạo phiếu nhập mới
def tao_phieu_nhap(ma_phieu):

    return {
        "ma_phieu_nhap": ma_phieu,
        "ma_kho_nhap": "",
        "ngay_nhap": datetime.now(),
        "nha_cung_cap": "",
        "ghi_chu": "",
        "chi_tiet": [],
        "tong_thanh_tien": 0
    }


# Tạo chi tiết phiếu nhập
def tao_chi_tiet_nhap(
    san_pham,
    dvt_nhap,
    so_luong,
    loai_gia,
    don_gia,
    ck
):

    # Lấy hệ số quy đổi
    he_so_quy_doi = lay_he_so_quy_doi(
        san_pham,
        dvt_nhap
    )

    # Tính số lượng theo DVT chính
    so_luong_quy_doi = (
        so_luong * he_so_quy_doi
    )

    # Nếu chia thẳng thì không có chiết khấu
    if loai_gia == "CHIA THANG":

        ck = 0
        don_gia_sau_ck = don_gia

    # Nếu có chiết khấu thì tính lại đơn giá
    elif loai_gia == "CHIET KHAU":

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
        "ma_san_pham": san_pham["ma_san_pham"][0],
        "ten_san_pham": san_pham["ten_san_pham"],
        "dvt_nhap": dvt_nhap,
        "so_luong": so_luong,
        "loai_gia": loai_gia,
        "don_gia": don_gia,
        "ck": ck,

        "he_so_quy_doi": he_so_quy_doi,
        "so_luong_quy_doi": so_luong_quy_doi,
        "don_gia_sau_ck": don_gia_sau_ck,
        "thanh_tien_tung_dong": thanh_tien_tung_dong
    }


# ============================================================
# 3. TÍNH TOÁN CHI TIẾT
# ============================================================

# Tính lại một dòng chi tiết phiếu nhập
def tinh_lai_chi_tiet_nhap(
    san_pham,
    chi_tiet
):

    # Lấy lại hệ số quy đổi
    he_so_quy_doi = lay_he_so_quy_doi(
        san_pham,
        chi_tiet["dvt_nhap"]
    )

    if he_so_quy_doi is None:

        raise ValueError(
            f"ĐVT '{chi_tiet['dvt_nhap']}' "
            f"không tồn tại trong sản phẩm"
        )

    chi_tiet["he_so_quy_doi"] = he_so_quy_doi

    # Tính số lượng theo DVT chính
    chi_tiet["so_luong_quy_doi"] = (
        chi_tiet["so_luong"] * he_so_quy_doi
    )

    # Tính đơn giá sau chiết khấu
    if chi_tiet["loai_gia"] == "CHIA THANG":

        chi_tiet["ck"] = 0

        chi_tiet["don_gia_sau_ck"] = (
            chi_tiet["don_gia"]
        )

    elif chi_tiet["loai_gia"] == "CHIET KHAU":

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


# Tính tổng thành tiền của phiếu nhập
def tinh_tong_thanh_tien(phieu):

    tong_thanh_tien = sum(
        chi_tiet["thanh_tien_tung_dong"]
        for chi_tiet in phieu["chi_tiet"]
    )

    return tong_thanh_tien


# Cập nhật tổng thành tiền
def cap_nhat_tong_thanh_tien(phieu):

    phieu["tong_thanh_tien"] = (
        tinh_tong_thanh_tien(phieu)
    )

    return phieu


# Tính lại toàn bộ phiếu nhập
def cap_nhat_tinh_toan_phieu_nhap(
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

        # Tính lại chi tiết
        tinh_lai_chi_tiet_nhap(
            san_pham,
            chi_tiet
        )

    # Cập nhật tổng phiếu
    cap_nhat_tong_thanh_tien(phieu)

    return phieu


# ============================================================
# 4. THÊM CHI TIẾT VÀO PHIẾU NHẬP
# ============================================================

# Thêm một chi tiết vào phiếu nhập
def them_chi_tiet_vao_phieu_nhap(
    danh_sach_san_pham,
    phieu,
    chi_tiet
):

    # Kiểm tra sản phẩm tồn tại
    san_pham = tim_san_pham(
        danh_sach_san_pham,
        chi_tiet["ma_san_pham"]
    )

    if san_pham is None:

        raise ValueError(
            f"Không tìm thấy sản phẩm "
            f"'{chi_tiet['ma_san_pham']}'"
        )

    # Tính lại chi tiết trước khi thêm
    tinh_lai_chi_tiet_nhap(
        san_pham,
        chi_tiet
    )

    # Thêm vào phiếu
    phieu["chi_tiet"].append(chi_tiet)

    # Cập nhật toàn bộ phiếu
    cap_nhat_tong_thanh_tien(phieu)

    return phieu


# ============================================================
# 5. KIỂM TRA DỮ LIỆU PHIẾU NHẬP
# ============================================================

# Kiểm tra phiếu nhập có hợp lệ tối thiểu hay không
def kiem_tra_du_lieu_phieu_nhap(phieu):

    # Phiếu phải có ít nhất một dòng hàng
    if not phieu["chi_tiet"]:

        print(
            "Lỗi: Phiếu nhập phải có "
            "ít nhất một sản phẩm"
        )

        return False

    return True


# Danh sách phiếu nhập
danh_sach_phieu_nhap = []


# ============================================================
# 6. LƯU PHIẾU NHẬP MỚI
# ============================================================

# Lưu phiếu nhập mới
def luu_phieu_nhap(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu
):
    # Kiểm tra dữ liệu
    if not kiem_tra_du_lieu_phieu_nhap(phieu):
        return False

    # Tính lại toàn bộ phiếu trước khi lưu
    cap_nhat_tinh_toan_phieu_nhap(
        danh_sach_san_pham,
        phieu
    )

    # Lưu phiếu
    danh_sach_phieu_nhap.append(phieu)

    # Cập nhật tồn kho
    ap_dung_phieu_nhap_vao_kho(
        danh_sach_ton_kho,
        danh_sach_kho,
        phieu
    )

    print("Lưu phiếu nhập thành công")

    return True


# ============================================================
# 7. SỬA PHIẾU NHẬP
# ============================================================

# Tạo bản nháp phiếu nhập cần sửa
def sua_phieu_nhap(phieu_can_sua):

    # Tạo bản sao độc lập
    phieu_nhap = deepcopy(phieu_can_sua)

    return phieu_nhap


# Sửa thông tin đầu phiếu
def sua_header_phieu_nhap(
    phieu_nhap,
    ngay_nhap=None,
    nha_cung_cap=None,
    ghi_chu=None
):

    if ngay_nhap is not None:
        phieu_nhap["ngay_nhap"] = ngay_nhap

    if nha_cung_cap is not None:
        phieu_nhap["nha_cung_cap"] = nha_cung_cap

    if ghi_chu is not None:
        phieu_nhap["ghi_chu"] = ghi_chu

    return phieu_nhap


# ============================================================
# 8. THÊM / SỬA / XÓA DÒNG KHI SỬA PHIẾU
# ============================================================

# Thêm dòng mới vào phiếu đang sửa
def them_chi_tiet_phieu_nhap(
    danh_sach_san_pham,
    phieu_nhap,
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

    # Tính lại dòng mới
    tinh_lai_chi_tiet_nhap(
        san_pham,
        chi_tiet_moi
    )

    # Thêm dòng
    phieu_nhap["chi_tiet"].append(
        chi_tiet_moi
    )

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(
        phieu_nhap
    )

    return phieu_nhap


# Sửa một dòng chi tiết
def sua_dong_chi_tiet_phieu_nhap(
    danh_sach_san_pham,
    phieu_nhap,
    vi_tri,
    thay_doi
):

    # Lấy dòng cần sửa
    chi_tiet = phieu_nhap["chi_tiet"][vi_tri]

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
    tinh_lai_chi_tiet_nhap(
        san_pham,
        chi_tiet
    )

    # Tính lại toàn bộ phiếu
    cap_nhat_tinh_toan_phieu_nhap(
        danh_sach_san_pham,
        phieu_nhap
    )

    return phieu_nhap


# Xóa một dòng chi tiết
def xoa_chi_tiet_phieu_nhap(
    phieu_nhap,
    vi_tri
):

    # Xóa dòng
    del phieu_nhap["chi_tiet"][vi_tri]

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(
        phieu_nhap
    )

    return phieu_nhap


# ============================================================
# 9. XÁC NHẬN LƯU PHIẾU ĐÃ SỬA
# ============================================================

def xac_nhan_luu(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu_nhap
):
    # Kiểm tra phiếu
    if not kiem_tra_du_lieu_phieu_nhap(
        phieu_nhap
    ):
        return None

    # Tính lại toàn bộ phiếu trước khi lưu
    cap_nhat_tinh_toan_phieu_nhap(
        danh_sach_san_pham,
        phieu_nhap
    )

    # Tìm phiếu gốc
    for vi_tri, phieu_cu in enumerate(
        danh_sach_phieu_nhap
    ):
        if (
            phieu_cu["ma_phieu_nhap"]
            == phieu_nhap["ma_phieu_nhap"]
        ):
            # Hoàn tác ảnh hưởng của phiếu cũ
            hoan_tac_phieu_nhap_vao_kho(
                danh_sach_ton_kho,
                danh_sach_kho,
                phieu_cu
            )

            # Áp dụng ảnh hưởng của phiếu mới
            ap_dung_phieu_nhap_vao_kho(
                danh_sach_ton_kho,
                danh_sach_kho,
                phieu_nhap
            )

            # Thay thế phiếu cũ bằng phiếu mới
            danh_sach_phieu_nhap[vi_tri] = (
                phieu_nhap
            )

            print("Sửa phiếu nhập thành công")

            return phieu_nhap

    print("Không tìm thấy phiếu nhập cần sửa")

    return None


