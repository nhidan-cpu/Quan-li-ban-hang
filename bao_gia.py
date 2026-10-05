from datetime import datetime
from copy import deepcopy


# ============================================================
# 1. CẤU TRÚC DỮ LIỆU
# ============================================================

# Danh sách mẫu báo giá đã lưu
danh_sach_mau_bao_gia = []


# ============================================================
# 2. TẠO MẪU BÁO GIÁ
# ============================================================

# Tạo mẫu báo giá mới
def tao_mau_bao_gia(ma_bao_gia):

    return {
        "ma_bao_gia": ma_bao_gia,
        "thoi_gian_tao": datetime.now(),
        "ma_khach_hang": "",
        "ten_khach_hang": "",
        "ghi_chu": "",

        "chi_tiet": []
    }


# ============================================================
# 3. TÌM MẪU BÁO GIÁ
# ============================================================

# Tìm mẫu báo giá theo mã
def tim_mau_bao_gia(ma_bao_gia):

    for mau_bao_gia in danh_sach_mau_bao_gia:

        if mau_bao_gia["ma_bao_gia"] == ma_bao_gia:

            return mau_bao_gia

    return None


# ============================================================
# 4. TẠO CHI TIẾT BÁO GIÁ
# ============================================================

# Tạo chi tiết báo giá
def tao_chi_tiet_bao_gia(
    san_pham,
    loai_gia,
    chiet_khau=0,
    don_gia_sau_chiet_khau=0
):

    # Lấy thông tin cơ bản từ sản phẩm
    ma_san_pham = san_pham["ma_san_pham"][0]
    ten_san_pham = san_pham["ten_san_pham"]
    dvt_chinh = san_pham["dvt_chinh"]

    # ========================================================
    # XỬ LÝ LOẠI GIÁ
    # ========================================================

    if loai_gia == "CHIET KHAU":

        # Giá niêm yết lấy từ sản phẩm
        gia_niem_yet = san_pham["gia_ban"]

        if gia_niem_yet <= 0:

            raise ValueError(
                "Sản phẩm chưa có giá niêm yết hợp lệ"
            )

        # Kiểm tra chiết khấu
        if chiet_khau < 0 or chiet_khau > 100:

            raise ValueError(
                "Chiết khấu phải từ 0 đến 100"
            )

        # Tính đơn giá sau chiết khấu
        don_gia_sau_chiet_khau = (
            gia_niem_yet
            * (1 - chiet_khau / 100)
        )

    elif loai_gia == "CHIA THANG":

        # Hai trường này không sử dụng
        gia_niem_yet = None
        chiet_khau = None

        # Người dùng nhập trực tiếp giá cuối
        if don_gia_sau_chiet_khau <= 0:

            raise ValueError(
                "Đơn giá sau chiết khấu phải lớn hơn 0"
            )

    else:

        raise ValueError(
            f"Loại giá không hợp lệ: {loai_gia}"
        )

    return {
        "ma_san_pham": ma_san_pham,
        "ten_san_pham": ten_san_pham,
        "dvt_chinh": dvt_chinh,

        "loai_gia": loai_gia,
        "gia_niem_yet": gia_niem_yet,
        "chiet_khau": chiet_khau,
        "don_gia_sau_chiet_khau": don_gia_sau_chiet_khau
    }


# ============================================================
# 5. THÊM CHI TIẾT VÀO MẪU BÁO GIÁ
# ============================================================

# Thêm một sản phẩm vào mẫu báo giá
def them_chi_tiet_vao_mau_bao_gia(
    mau_bao_gia,
    chi_tiet_bao_gia
):

    ma_san_pham = chi_tiet_bao_gia["ma_san_pham"]

    # Không cho thêm trùng sản phẩm
    for chi_tiet in mau_bao_gia["chi_tiet"]:

        if chi_tiet["ma_san_pham"] == ma_san_pham:

            raise ValueError(
                f"Sản phẩm '{ma_san_pham}' "
                "đã tồn tại trong báo giá"
            )

    mau_bao_gia["chi_tiet"].append(
        chi_tiet_bao_gia
    )

    return chi_tiet_bao_gia


# ============================================================
# 6. SỬA CHI TIẾT BÁO GIÁ
# ============================================================

# Sửa một dòng chi tiết báo giá
def sua_chi_tiet_bao_gia(
    mau_bao_gia,
    vi_tri,
    loai_gia=None,
    chiet_khau=None,
    don_gia_sau_chiet_khau=None
):

    if vi_tri < 0 or vi_tri >= len(
        mau_bao_gia["chi_tiet"]
    ):

        raise ValueError(
            "Vị trí chi tiết báo giá không hợp lệ"
        )

    chi_tiet = mau_bao_gia["chi_tiet"][vi_tri]

    # Giữ lại thông tin sản phẩm
    ma_san_pham = chi_tiet["ma_san_pham"]
    ten_san_pham = chi_tiet["ten_san_pham"]
    dvt_chinh = chi_tiet["dvt_chinh"]

    # Nếu không truyền loại giá mới
    # thì giữ loại giá hiện tại
    if loai_gia is None:

        loai_gia = chi_tiet["loai_gia"]

    # ========================================================
    # CHIẾT KHẤU
    # ========================================================

    if loai_gia == "CHIET KHAU":

        gia_niem_yet = chi_tiet["gia_niem_yet"]

        if gia_niem_yet is None:

            raise ValueError(
                "Không có giá niêm yết để tính chiết khấu"
            )

        if chiet_khau is None:

            chiet_khau = chi_tiet["chiet_khau"]

        if chiet_khau < 0 or chiet_khau > 100:

            raise ValueError(
                "Chiết khấu phải từ 0 đến 100"
            )

        don_gia_sau_chiet_khau = (
            gia_niem_yet
            * (1 - chiet_khau / 100)
        )

    # ========================================================
    # CHIA THẲNG
    # ========================================================

    elif loai_gia == "CHIA THANG":

        gia_niem_yet = None
        chiet_khau = None

        if don_gia_sau_chiet_khau is None:

            don_gia_sau_chiet_khau = (
                chi_tiet["don_gia_sau_chiet_khau"]
            )

        if don_gia_sau_chiet_khau <= 0:

            raise ValueError(
                "Đơn giá sau chiết khấu phải lớn hơn 0"
            )

    else:

        raise ValueError(
            f"Loại giá không hợp lệ: {loai_gia}"
        )

    # Cập nhật lại dòng
    chi_tiet.update({
        "ma_san_pham": ma_san_pham,
        "ten_san_pham": ten_san_pham,
        "dvt_chinh": dvt_chinh,

        "loai_gia": loai_gia,
        "gia_niem_yet": gia_niem_yet,
        "chiet_khau": chiet_khau,
        "don_gia_sau_chiet_khau":
            don_gia_sau_chiet_khau
    })

    return chi_tiet


# ============================================================
# 7. XÓA CHI TIẾT BÁO GIÁ
# ============================================================

# Xóa một dòng chi tiết báo giá
def xoa_chi_tiet_bao_gia(
    mau_bao_gia,
    vi_tri
):

    if vi_tri < 0 or vi_tri >= len(
        mau_bao_gia["chi_tiet"]
    ):

        raise ValueError(
            "Vị trí chi tiết báo giá không hợp lệ"
        )

    return mau_bao_gia["chi_tiet"].pop(
        vi_tri
    )


# ============================================================
# 8. LƯU MẪU BÁO GIÁ
# ============================================================

# Lưu mẫu báo giá mới
def luu_mau_bao_gia(
    mau_bao_gia
):

    # Không cho lưu trùng mã
    if tim_mau_bao_gia(
        mau_bao_gia["ma_bao_gia"]
    ) is not None:

        raise ValueError(
            f"Mã báo giá "
            f"'{mau_bao_gia['ma_bao_gia']}' "
            "đã tồn tại"
        )

    # Không cho lưu báo giá không có sản phẩm
    if not mau_bao_gia["chi_tiet"]:

        raise ValueError(
            "Báo giá phải có ít nhất một sản phẩm"
        )

    # Lưu bản sao để tách khỏi bản nháp
    mau_bao_gia_luu = deepcopy(
        mau_bao_gia
    )

    danh_sach_mau_bao_gia.append(
        mau_bao_gia_luu
    )

    return mau_bao_gia_luu


# ============================================================
# 9. TẠO BẢN NHÁP ĐỂ SỬA
# ============================================================

# Tạo bản sao báo giá để chỉnh sửa
def sua_mau_bao_gia(
    ma_bao_gia
):

    mau_bao_gia = tim_mau_bao_gia(
        ma_bao_gia
    )

    if mau_bao_gia is None:

        raise ValueError(
            f"Không tìm thấy báo giá "
            f"'{ma_bao_gia}'"
        )

    return deepcopy(
        mau_bao_gia
    )


# ============================================================
# 10. XÁC NHẬN LƯU BÁO GIÁ ĐÃ SỬA
# ============================================================

# Lưu lại báo giá sau khi sửa
def xac_nhan_luu_mau_bao_gia(
    mau_bao_gia
):

    if not mau_bao_gia["chi_tiet"]:

        raise ValueError(
            "Báo giá phải có ít nhất một sản phẩm"
        )

    for vi_tri, bao_gia in enumerate(
        danh_sach_mau_bao_gia
    ):

        if (
            bao_gia["ma_bao_gia"]
            == mau_bao_gia["ma_bao_gia"]
        ):

            danh_sach_mau_bao_gia[
                vi_tri
            ] = deepcopy(
                mau_bao_gia
            )

            return danh_sach_mau_bao_gia[
                vi_tri
            ]

    raise ValueError(
        f"Không tìm thấy báo giá "
        f"'{mau_bao_gia['ma_bao_gia']}' "
        "cần sửa"
    )