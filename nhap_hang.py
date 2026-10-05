from datetime import datetime
from copy import deepcopy

from san_pham import (lay_he_so_quy_doi, tim_san_pham)

from kho import (ap_dung_phieu_nhap_vao_kho, hoan_tac_phieu_nhap_vao_kho)

from nha_cung_cap import (tim_nha_cung_cap, cap_nhat_tong_giao_dich)

from cong_no import (
    phat_sinh_cong_no_tu_phieu_nhap,
    hoan_tac_cong_no_tu_phieu_nhap
)


_KHONG_THAY_DOI = object()

# ============================================================
# 1. CẤU TRÚC DỮ LIỆU
# ============================================================

# Cấu trúc phiếu nhập
phieu_nhap = {
    "ma_phieu_nhap": "",
    "ma_kho_nhap": "",
    "ngay_nhap": "",
    "nha_cung_cap": None,
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
        "nha_cung_cap": None,
        "ghi_chu": "",
        "chi_tiet": [],
        "tong_thanh_tien": 0
    }

def kiem_tra_nha_cung_cap(nha_cung_cap):

    # Không nhập NCC → hợp lệ
    if nha_cung_cap is None:
        return True

    # Nếu đã nhập thì phải là chuỗi
    if not isinstance(nha_cung_cap, str):
        raise ValueError(
            "Nhà cung cấp phải là mã NCC hoặc để trống."
        )

    # Không chấp nhận chuỗi chỉ chứa khoảng trắng
    if not nha_cung_cap.strip():
        return True

    # Có nhập mã NCC → phải tồn tại
    if tim_nha_cung_cap(nha_cung_cap) is None:
        raise ValueError(
            f"Không tìm thấy nhà cung cấp "
            f"'{nha_cung_cap}'."
        )

    return True


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

    # Kiểm tra nhà cung cấp
    kiem_tra_nha_cung_cap(
        phieu["nha_cung_cap"]
    )

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

    # Tính lại toàn bộ phiếu trước khi tác động dữ liệu hệ thống
    cap_nhat_tinh_toan_phieu_nhap(
        danh_sach_san_pham,
        phieu
    )

    # Snapshot kho để có thể khôi phục chính xác nếu thao tác thất bại.
    danh_sach_ton_kho_cu = deepcopy(
        danh_sach_ton_kho
    )

    cong_no_da_phat_sinh = False
    giao_dich_ncc_da_cap_nhat = False

    try:

        # Cập nhật tồn kho trước khi đưa phiếu vào danh sách chính thức
        ap_dung_phieu_nhap_vao_kho(
            danh_sach_ton_kho,
            danh_sach_kho,
            phieu
        )

        # Phát sinh công nợ nếu có nhà cung cấp
        phat_sinh_cong_no_tu_phieu_nhap(
            phieu
        )

        cong_no_da_phat_sinh = True

        # Cập nhật tổng giao dịch của NCC nếu có
        if phieu["nha_cung_cap"] is not None:
            cap_nhat_tong_giao_dich(
                phieu["nha_cung_cap"],
                phieu["tong_thanh_tien"]
            )

            giao_dich_ncc_da_cap_nhat = True

    except Exception:

        # Hoàn tác tổng giao dịch NCC nếu bước cập nhật đã thành công.
        if giao_dich_ncc_da_cap_nhat:
            cap_nhat_tong_giao_dich(
                phieu["nha_cung_cap"],
                -phieu["tong_thanh_tien"]
            )

        # Hoàn tác công nợ nếu bước phát sinh đã thành công.
        if cong_no_da_phat_sinh:
            hoan_tac_cong_no_tu_phieu_nhap(
                phieu
            )

        # Khôi phục đúng trạng thái tồn kho trước khi lưu.
        danh_sach_ton_kho[:] = deepcopy(
            danh_sach_ton_kho_cu
        )

        raise

    # Chỉ đưa phiếu vào danh sách chính thức sau khi các tác động thành công
    danh_sach_phieu_nhap.append(
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
    nha_cung_cap=_KHONG_THAY_DOI,
    ghi_chu=None
):

    if ngay_nhap is not None:
        phieu_nhap["ngay_nhap"] = ngay_nhap

    if nha_cung_cap is not _KHONG_THAY_DOI:
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
    # Kiểm tra phiếu đang sửa
    if not kiem_tra_du_lieu_phieu_nhap(
        phieu_nhap
    ):
        return None

    # Tính lại toàn bộ phiếu trước khi tác động dữ liệu hệ thống
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
            != phieu_nhap["ma_phieu_nhap"]
        ):
            continue

        # Snapshot kho để khôi phục chính xác nếu phiếu mới lỗi.
        danh_sach_ton_kho_cu = deepcopy(
            danh_sach_ton_kho
        )

        cong_no_cu_da_hoan_tac = False
        giao_dich_ncc_cu_da_hoan_tac = False
        cong_no_moi_da_phat_sinh = False
        giao_dich_ncc_moi_da_cap_nhat = False

        try:

            # --------------------------------------------------------
            # 1. Hoàn tác toàn bộ ảnh hưởng của phiếu cũ
            # --------------------------------------------------------

            hoan_tac_phieu_nhap_vao_kho(
                danh_sach_ton_kho,
                danh_sach_kho,
                phieu_cu
            )

            hoan_tac_cong_no_tu_phieu_nhap(
                phieu_cu
            )

            cong_no_cu_da_hoan_tac = True

            if phieu_cu["nha_cung_cap"] is not None:
                cap_nhat_tong_giao_dich(
                    phieu_cu["nha_cung_cap"],
                    -phieu_cu["tong_thanh_tien"]
                )

                giao_dich_ncc_cu_da_hoan_tac = True

            # --------------------------------------------------------
            # 2. Áp dụng toàn bộ ảnh hưởng của phiếu mới
            # --------------------------------------------------------

            ap_dung_phieu_nhap_vao_kho(
                danh_sach_ton_kho,
                danh_sach_kho,
                phieu_nhap
            )

            phat_sinh_cong_no_tu_phieu_nhap(
                phieu_nhap
            )

            cong_no_moi_da_phat_sinh = True

            if phieu_nhap["nha_cung_cap"] is not None:
                cap_nhat_tong_giao_dich(
                    phieu_nhap["nha_cung_cap"],
                    phieu_nhap["tong_thanh_tien"]
                )

                giao_dich_ncc_moi_da_cap_nhat = True

            # --------------------------------------------------------
            # 3. Chỉ thay thế phiếu chính thức sau khi mọi tác động
            #    đã thành công.
            # --------------------------------------------------------

            danh_sach_phieu_nhap[vi_tri] = (
                phieu_nhap
            )

            print("Sửa phiếu nhập thành công")

            return phieu_nhap

        except Exception:

            # --------------------------------------------------------
            # 4. Hoàn tác công nợ và tổng giao dịch của phiếu mới
            #    nếu các bước tương ứng đã thành công.
            # --------------------------------------------------------

            if giao_dich_ncc_moi_da_cap_nhat:
                cap_nhat_tong_giao_dich(
                    phieu_nhap["nha_cung_cap"],
                    -phieu_nhap["tong_thanh_tien"]
                )

            if cong_no_moi_da_phat_sinh:
                hoan_tac_cong_no_tu_phieu_nhap(
                    phieu_nhap
                )

            # --------------------------------------------------------
            # 5. Khôi phục tồn kho chính xác về snapshot ban đầu.
            # --------------------------------------------------------

            danh_sach_ton_kho[:] = deepcopy(
                danh_sach_ton_kho_cu
            )

            # --------------------------------------------------------
            # 6. Khôi phục công nợ và tổng giao dịch của phiếu cũ.
            # --------------------------------------------------------

            if cong_no_cu_da_hoan_tac:
                phat_sinh_cong_no_tu_phieu_nhap(
                    phieu_cu
                )

            if giao_dich_ncc_cu_da_hoan_tac:
                cap_nhat_tong_giao_dich(
                    phieu_cu["nha_cung_cap"],
                    phieu_cu["tong_thanh_tien"]
                )

            raise

    print("Không tìm thấy phiếu nhập cần sửa")

    return None

