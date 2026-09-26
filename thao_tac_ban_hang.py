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
    "thoi_gian_tao": "",
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
    "thanh_tien_tung_dong": 0,

    "don_gia_von": 0,
    "thanh_tien_von": 0
}


# Danh sách phiếu bán
danh_sach_phieu_gntt = []

# Giữ tên cũ để không làm hỏng code đang gọi module bán hàng.
danh_sach_phieu_ban = danh_sach_phieu_gntt


# ============================================================
# TRẠNG THÁI BẢN NHÁP
# ============================================================

# Đánh dấu phiếu đã có thay đổi nhưng chưa lưu.
def danh_dau_phieu_da_thay_doi(phieu):

    phieu["_da_thay_doi"] = True

    return phieu


# Kiểm tra phiếu có thay đổi chưa lưu hay không.
def phieu_co_thay_doi_chua_luu(phieu):

    return phieu.get("_da_thay_doi", False)


# Đặt lại trạng thái bản nháp sau khi lưu thành công.
def dat_lai_trang_thai_phieu(phieu):

    phieu["_da_thay_doi"] = False

    return phieu


# Tạo bản dữ liệu để lưu vào danh sách phiếu,
# không lưu các trường trạng thái chỉ phục vụ User Form.
def tao_ban_luu_phieu(phieu):

    ban_luu = deepcopy(phieu)

    ban_luu.pop("_da_load", None)
    ban_luu.pop("_da_thay_doi", None)

    return ban_luu


# ============================================================
# 2. TẠO PHIẾU BÁN
# ============================================================

# Tạo phiếu bán mới
def tao_phieu_ban(ma_phieu):

    return {
        "ma_phieu": ma_phieu,
        "thoi_gian_tao": datetime.now(),
        "ma_khach_hang": "",
        "ten_khach_hang": "",
        "ghi_chu": "",

        "tong_thanh_tien": 0,
        "tong_thanh_tien_von": 0,
        "loi_nhuan": 0,
        "ty_suat": 0,

        "chi_tiet": [],

        # Trạng thái chỉ dùng cho bản nháp/User Form.
        "_da_load": False,
        "_da_thay_doi": False
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
    don_gia_sau_ck=0,
    ghi_chu=""
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

    # Kiểm tra số lượng
    if so_luong <= 0:

        raise ValueError(
            "Số lượng bán phải lớn hơn 0"
        )

    # Tính số lượng theo DVT chính
    so_luong_quy_doi = (
        so_luong * he_so_quy_doi
    )

    # Xử lý loại giá
    if loai_gia == "CHIA THANG":

        # Đơn giá và CK không sử dụng
        don_gia = 0
        ck = 0

        if don_gia_sau_ck <= 0:

            raise ValueError(
                "Đơn giá sau CK phải lớn hơn 0"
            )

    elif loai_gia == "CHIET KHAU":

        if don_gia <= 0:

            raise ValueError(
                "Đơn giá phải lớn hơn 0"
            )

        if ck < 0 or ck > 100:

            raise ValueError(
                "Chiết khấu phải từ 0 đến 100"
            )

        # Tính đơn giá sau chiết khấu
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
        "thanh_tien_tung_dong": thanh_tien_tung_dong,

        "don_gia_von": 0,
        "thanh_tien_von": 0
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

    # Cập nhật hệ số quy đổi
    chi_tiet["he_so_quy_doi"] = he_so_quy_doi

    # Tính số lượng theo DVT chính
    chi_tiet["so_luong_quy_doi"] = (
        chi_tiet["so_luong"]
        * he_so_quy_doi
    )

    # Kiểm tra số lượng
    if chi_tiet["so_luong"] <= 0:

        raise ValueError(
            "Số lượng bán phải lớn hơn 0"
        )

    # Xử lý loại giá
    if chi_tiet["loai_gia"] == "CHIA THANG":

        # Đơn giá và CK không sử dụng
        chi_tiet["don_gia"] = 0
        chi_tiet["ck"] = 0

        if chi_tiet["don_gia_sau_ck"] <= 0:

            raise ValueError(
                "Đơn giá sau CK phải lớn hơn 0"
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

        # Tính đơn giá sau chiết khấu
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


# Tính tổng giá vốn
def tinh_tong_thanh_tien_von(phieu):
    return sum(
        chi_tiet.get("thanh_tien_von", 0)
        for chi_tiet in phieu["chi_tiet"]
    )


# Tính lợi nhuận
def tinh_loi_nhuan(phieu):
    return (
        phieu["tong_thanh_tien"]
        - phieu["tong_thanh_tien_von"]
    )


# Tính tỷ suất lợi nhuận
def tinh_ty_suat(phieu):
    if phieu["tong_thanh_tien"] == 0:
        return 0

    return (
        phieu["loi_nhuan"]
        / phieu["tong_thanh_tien"]
        * 100
    )


# Cập nhật tổng số liệu của phiếu
def cap_nhat_tong_thanh_tien(phieu):

    phieu["tong_thanh_tien"] = (
        tinh_tong_thanh_tien(phieu)
    )

    phieu["tong_thanh_tien_von"] = (
        tinh_tong_thanh_tien_von(phieu)
    )

    phieu["loi_nhuan"] = (
        tinh_loi_nhuan(phieu)
    )

    phieu["ty_suat"] = (
        tinh_ty_suat(phieu)
    )

    return phieu


# Tính lại toàn bộ phiếu bán
def cap_nhat_tinh_toan_phieu_ban(
    danh_sach_san_pham,
    phieu
):

    for chi_tiet in phieu["chi_tiet"]:

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

        # Cập nhật tên sản phẩm
        chi_tiet["ten_san_pham"] = (
            san_pham["ten_san_pham"]
        )

        # Đảm bảo dòng chi tiết luôn có ghi chú
        if "ghi_chu" not in chi_tiet:
            chi_tiet["ghi_chu"] = ""

        # Tính lại chi tiết
        tinh_lai_chi_tiet_ban(
            san_pham,
            chi_tiet
        )

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(phieu)

    return phieu


# ============================================================
# 4. THÊM CHI TIẾT VÀO PHIẾU
# ============================================================

# Thêm một dòng vào phiếu bán
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

    # Tính lại chi tiết
    tinh_lai_chi_tiet_ban(
        san_pham,
        chi_tiet
    )

    # Gán STT
    chi_tiet["stt"] = (
        len(phieu["chi_tiet"]) + 1
    )

    # Thêm dòng
    phieu["chi_tiet"].append(
        chi_tiet
    )

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(phieu)

    danh_dau_phieu_da_thay_doi(phieu)

    return phieu


# ============================================================
# 5. KIỂM TRA DỮ LIỆU PHIẾU
# ============================================================

# Kiểm tra dữ liệu cơ bản
def kiem_tra_du_lieu_phieu_ban(phieu):

    # Phiếu phải có ít nhất một dòng
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


# Kiểm tra mã phiếu đã tồn tại chưa
def kiem_tra_trung_ma_phieu(
    ma_phieu
):

    for phieu in danh_sach_phieu_ban:

        if phieu["ma_phieu"] == ma_phieu:

            return True

    return False


# ============================================================
# 6. KIỂM TRA TỒN KHO
# ============================================================

# Gom số lượng cần xuất theo kho và sản phẩm
def tong_hop_so_luong_xuat(
    phieu
):

    tong_hop = {}

    for chi_tiet in phieu["chi_tiet"]:

        khoa = (
            chi_tiet["ma_kho"],
            chi_tiet["ma_san_pham"]
        )

        if khoa not in tong_hop:

            tong_hop[khoa] = 0

        tong_hop[khoa] += (
            chi_tiet["so_luong_quy_doi"]
        )

    return tong_hop


# Kiểm tra tồn kho
def kiem_tra_ton_kho_phieu_ban(
    danh_sach_ton_kho,
    phieu
):

    tong_hop = tong_hop_so_luong_xuat(
        phieu
    )

    for (
        (ma_kho, ma_san_pham),
        so_luong_can_xuat
    ) in tong_hop.items():

        # Tìm tồn kho
        ton = tim_ton_kho(
            danh_sach_ton_kho,
            ma_kho,
            ma_san_pham
        )

        if ton is None:

            raise ValueError(
                f"Không tìm thấy tồn kho "
                f"của sản phẩm "
                f"'{ma_san_pham}' "
                f"tại kho '{ma_kho}'"
            )

        # Kiểm tra số lượng
        if (
            ton["so_luong_ton"]
            < so_luong_can_xuat
        ):

            raise ValueError(
                f"Không đủ tồn kho: "
                f"SP '{ma_san_pham}', "
                f"Kho '{ma_kho}', "
                f"Tồn {ton['so_luong_ton']}, "
                f"Cần {so_luong_can_xuat}"
            )

    return True


# ============================================================
# 7. CẬP NHẬT TỒN KHO
# ============================================================

# Áp dụng phiếu bán vào kho
def ap_dung_phieu_ban_vao_kho(
    danh_sach_ton_kho,
    phieu
):

    # Kiểm tra tồn trước
    kiem_tra_ton_kho_phieu_ban(
        danh_sach_ton_kho,
        phieu
    )

    # Xuất từng dòng
    for chi_tiet in phieu["chi_tiet"]:

        ton = tim_ton_kho(
            danh_sach_ton_kho,
            chi_tiet["ma_kho"],
            chi_tiet["ma_san_pham"]
        )

        # Lấy giá trị tồn theo tỷ lệ
        if ton["so_luong_ton"] > 0:

            gia_tri_xuat = (
                chi_tiet["so_luong_quy_doi"]
                * ton["gia_tri_ton"]
                / ton["so_luong_ton"]
            )

        else:

            gia_tri_xuat = 0

        # Trừ tồn
        cap_nhat_ton_kho_tu_chi_tiet(
            ton,
            -chi_tiet["so_luong_quy_doi"],
            -gia_tri_xuat
        )


# Hoàn tác phiếu bán khỏi kho
def hoan_tac_phieu_ban_vao_kho(
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

        # Hoàn lại số lượng
        so_luong_hoan = (
            chi_tiet["so_luong_quy_doi"]
        )

        # V1 hoàn tác theo giá trị tồn hiện tại.
        # Cơ chế giá vốn lịch sử sẽ xây sau.
        if ton["so_luong_ton"] > 0:

            gia_tri_hoan = (
                so_luong_hoan
                * ton["gia_tri_ton"]
                / ton["so_luong_ton"]
            )

        else:

            gia_tri_hoan = 0

        cap_nhat_ton_kho_tu_chi_tiet(
            ton,
            so_luong_hoan,
            gia_tri_hoan
        )


# ============================================================
# 8. LƯU PHIẾU BÁN
# ============================================================

# Lưu phiếu bán.
# Nếu mã chưa tồn tại: lưu mới.
# Nếu mã đã tồn tại: cập nhật toàn bộ phiếu.
def luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu,
    ham_tinh_gia_von=None
):

    # Kiểm tra dữ liệu trước khi thay đổi dữ liệu chính.
    if not kiem_tra_du_lieu_phieu_ban(
        phieu
    ):
        return False

    # Mã chưa tồn tại → lưu phiếu mới.
    if not kiem_tra_trung_ma_phieu(
        phieu["ma_phieu"]
    ):

        cap_nhat_tinh_toan_phieu_ban(
            danh_sach_san_pham,
            phieu
        )

        kiem_tra_ton_kho_phieu_ban(
            danh_sach_ton_kho,
            phieu
        )

        # Chốt giá vốn nếu được cung cấp.
        if ham_tinh_gia_von is not None:
            ham_tinh_gia_von(
                phieu,
                danh_sach_ton_kho
            )

            cap_nhat_tong_thanh_tien(
                phieu
            )

        ap_dung_phieu_ban_vao_kho(
            danh_sach_ton_kho,
            phieu
        )

        # Lưu bản nghiệp vụ, không lưu trạng thái User Form.
        ban_luu = tao_ban_luu_phieu(phieu)

        danh_sach_phieu_ban.append(
            ban_luu
        )

        dat_lai_trang_thai_phieu(phieu)

        print(
            "Lưu phiếu bán thành công"
        )

        return True

    # Mã đã tồn tại → cập nhật toàn bộ phiếu.
    return xac_nhan_luu_phieu_ban(
        danh_sach_san_pham,
        danh_sach_ton_kho,
        phieu,
        ham_tinh_gia_von
    )


# ============================================================
# 9. TÌM PHIẾU BÁN
# ============================================================

# Tìm phiếu bán theo mã
def tim_phieu_ban(
    ma_phieu
):

    for phieu in danh_sach_phieu_ban:

        if phieu["ma_phieu"] == ma_phieu:

            return phieu

    return None


# Tải phiếu bán đã lưu thành một bản nháp để chỉnh sửa.
def load_phieu_ban(ma_phieu):

    phieu_can_load = tim_phieu_ban(
        ma_phieu
    )

    if phieu_can_load is None:
        return None

    phieu_nhap = deepcopy(
        phieu_can_load
    )

    # Đã load nhưng chưa có thay đổi.
    phieu_nhap["_da_load"] = True
    phieu_nhap["_da_thay_doi"] = False

    return phieu_nhap


# ============================================================
# 10. SỬA PHIẾU BÁN
# ============================================================

# Tạo bản nháp phiếu bán cần sửa
def sua_phieu_ban(
    phieu_can_sua
):

    phieu_nhap = deepcopy(
        phieu_can_sua
    )

    phieu_nhap["_da_load"] = True
    phieu_nhap["_da_thay_doi"] = False

    return phieu_nhap


# Sửa thông tin đầu phiếu
def sua_header_phieu_ban(
    phieu_ban,
    thoi_gian_tao=None,
    ma_khach_hang=None,
    ten_khach_hang=None,
    ghi_chu=None
):

    if thoi_gian_tao is not None:

        phieu_ban["thoi_gian_tao"] = (
            thoi_gian_tao
        )

    if ma_khach_hang is not None:

        phieu_ban["ma_khach_hang"] = (
            ma_khach_hang
        )

    if ten_khach_hang is not None:

        phieu_ban["ten_khach_hang"] = (
            ten_khach_hang
        )

    if ghi_chu is not None:

        phieu_ban["ghi_chu"] = ghi_chu

    if any(value is not None for value in (
        thoi_gian_tao,
        ma_khach_hang,
        ten_khach_hang,
        ghi_chu
    )):
        danh_dau_phieu_da_thay_doi(phieu_ban)

    return phieu_ban


# ============================================================
# 11. THÊM / SỬA / XÓA DÒNG KHI SỬA PHIẾU
# ============================================================

# Thêm dòng mới
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

    # Đảm bảo dòng chi tiết luôn có ghi chú
    if "ghi_chu" not in chi_tiet_moi:
        chi_tiet_moi["ghi_chu"] = ""

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

    danh_dau_phieu_da_thay_doi(phieu_ban)

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
    chi_tiet.update(
        thay_doi
    )

    # Nếu thay đổi dữ liệu ảnh hưởng đến giá vốn,
    # giá vốn cũ không được giữ lại.
    if (
        "ma_san_pham" in thay_doi
        or "ma_kho" in thay_doi
        or "dvt_ban" in thay_doi
        or "so_luong" in thay_doi
    ):
        chi_tiet["don_gia_von"] = 0
        chi_tiet["thanh_tien_von"] = 0

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

    danh_dau_phieu_da_thay_doi(phieu_ban)

    return phieu_ban


# Xóa một dòng chi tiết
def xoa_chi_tiet_phieu_ban(
    phieu_ban,
    vi_tri
):

    # Xóa dòng
    del phieu_ban["chi_tiet"][vi_tri]

    # Đánh lại STT
    for stt, chi_tiet in enumerate(
        phieu_ban["chi_tiet"],
        start=1
    ):

        chi_tiet["stt"] = stt

    # Cập nhật tổng
    cap_nhat_tong_thanh_tien(
        phieu_ban
    )

    danh_dau_phieu_da_thay_doi(phieu_ban)

    return phieu_ban


# ============================================================
# 12. XÁC NHẬN LƯU PHIẾU ĐÃ SỬA
# ============================================================

# Xác nhận lưu phiếu sau khi sửa
def xac_nhan_luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_ban,
    ham_tinh_gia_von=None
):

    # Kiểm tra dữ liệu
    if not kiem_tra_du_lieu_phieu_ban(
        phieu_ban
    ):

        return None

    # Tìm phiếu cũ
    phieu_cu = tim_phieu_ban(
        phieu_ban["ma_phieu"]
    )

    if phieu_cu is None:

        print(
            "Không tìm thấy phiếu bán "
            "cần sửa"
        )

        return None

    # Tính lại phiếu mới
    cap_nhat_tinh_toan_phieu_ban(
        danh_sach_san_pham,
        phieu_ban
    )

    # Tạm thời hoàn tác phiếu cũ
    hoan_tac_phieu_ban_vao_kho(
        danh_sach_ton_kho,
        phieu_cu
    )

    try:

        # Kiểm tra tồn sau khi hoàn tác
        kiem_tra_ton_kho_phieu_ban(
            danh_sach_ton_kho,
            phieu_ban
        )

        # Tính lại và đóng băng giá vốn của phiếu mới.
        if ham_tinh_gia_von is not None:
            ham_tinh_gia_von(
                phieu_ban,
                danh_sach_ton_kho
            )

            cap_nhat_tong_thanh_tien(
                phieu_ban
            )

        # Áp dụng phiếu mới
        ap_dung_phieu_ban_vao_kho(
            danh_sach_ton_kho,
            phieu_ban
        )

    except Exception:

        # Nếu phiếu mới không hợp lệ,
        # khôi phục lại ảnh hưởng của phiếu cũ
        ap_dung_phieu_ban_vao_kho(
            danh_sach_ton_kho,
            phieu_cu
        )

        raise

    # Tìm lại vị trí phiếu cũ
    for vi_tri, phieu in enumerate(
        danh_sach_phieu_ban
    ):

        if phieu["ma_phieu"] == (
            phieu_ban["ma_phieu"]
        ):

            # Lưu bản nghiệp vụ, không lưu trạng thái User Form.
            danh_sach_phieu_ban[
                vi_tri
            ] = tao_ban_luu_phieu(phieu_ban)

            dat_lai_trang_thai_phieu(phieu_ban)

            print(
                "Sửa phiếu bán thành công"
            )

            return phieu_ban

    return None

# ============================================================
# 13. HÀM TƯƠNG THÍCH CHO GNTT
# ============================================================

# Tìm phiếu GNTT theo mã.
def tim_phieu_gntt(ma_phieu):
    return tim_phieu_ban(ma_phieu)


# Tạo phiếu GNTT mới.
def tao_phieu_gntt(ma_phieu):
    return tao_phieu_ban(ma_phieu)


# Tải phiếu GNTT đã lưu thành bản nháp để chỉnh sửa.
def load_phieu_gntt(ma_phieu):
    return load_phieu_ban(
        ma_phieu
    )


# Lưu phiếu GNTT.
def luu_phieu_gntt(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu,
    ham_tinh_gia_von=None
):
    return luu_phieu_ban(
        danh_sach_san_pham,
        danh_sach_ton_kho,
        phieu,
        ham_tinh_gia_von
    )


# Xác nhận lưu phiếu GNTT đã sửa.
def xac_nhan_luu_phieu_gntt(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu,
    ham_tinh_gia_von=None
):
    return xac_nhan_luu_phieu_ban(
        danh_sach_san_pham,
        danh_sach_ton_kho,
        phieu,
        ham_tinh_gia_von
    )
