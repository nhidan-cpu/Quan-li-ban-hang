from copy import deepcopy


mau_nha_cung_cap = {
    "ma_nha_cung_cap": "",
    "ten_nha_cung_cap": "",
    "so_dien_thoai": "",
    "dia_chi": "",
    "tong_giao_dich": 0,
    "cong_no": 0,
    "trang_thai": "DANG_HOAT_DONG",
    "ghi_chu": ""
}


danh_sach_nha_cung_cap = []


# Tìm nhà cung cấp theo mã
def tim_nha_cung_cap(ma_nha_cung_cap):
    for nha_cung_cap in danh_sach_nha_cung_cap:
        if nha_cung_cap["ma_nha_cung_cap"] == ma_nha_cung_cap:
            return nha_cung_cap
    return None


# Tạo mã nhà cung cấp mới
def tao_ma_nha_cung_cap():
    so_ma_lon_nhat = 0

    for nha_cung_cap in danh_sach_nha_cung_cap:
        ma_nha_cung_cap = nha_cung_cap["ma_nha_cung_cap"]

        if not ma_nha_cung_cap.startswith("NCC-"):
            continue

        try:
            so_ma = int(ma_nha_cung_cap[4:])
        except ValueError:
            continue

        if so_ma > so_ma_lon_nhat:
            so_ma_lon_nhat = so_ma

    return f"NCC-{so_ma_lon_nhat + 1:04d}"


# Tạo nhà cung cấp mới
def tao_nha_cung_cap(
    ten_nha_cung_cap,
    so_dien_thoai="",
    dia_chi="",
    ghi_chu=""
):
    if not isinstance(ten_nha_cung_cap, str):
        raise ValueError("Tên nhà cung cấp phải là chuỗi.")

    if not ten_nha_cung_cap.strip():
        raise ValueError("Tên nhà cung cấp không được để trống.")

    nha_cung_cap_moi = deepcopy(mau_nha_cung_cap)

    nha_cung_cap_moi["ma_nha_cung_cap"] = tao_ma_nha_cung_cap()
    nha_cung_cap_moi["ten_nha_cung_cap"] = (
        ten_nha_cung_cap.strip()
    )
    nha_cung_cap_moi["so_dien_thoai"] = so_dien_thoai
    nha_cung_cap_moi["dia_chi"] = dia_chi
    nha_cung_cap_moi["ghi_chu"] = ghi_chu

    danh_sach_nha_cung_cap.append(nha_cung_cap_moi)

    return nha_cung_cap_moi


# Sửa thông tin nhà cung cấp
def sua_nha_cung_cap(
    ma_nha_cung_cap,
    ten_nha_cung_cap=None,
    so_dien_thoai=None,
    dia_chi=None,
    ghi_chu=None
):
    nha_cung_cap = tim_nha_cung_cap(ma_nha_cung_cap)

    if nha_cung_cap is None:
        raise ValueError("Không tìm thấy nhà cung cấp.")

    if ten_nha_cung_cap is not None:
        if not isinstance(ten_nha_cung_cap, str):
            raise ValueError(
                "Tên nhà cung cấp phải là chuỗi."
            )

        if not ten_nha_cung_cap.strip():
            raise ValueError(
                "Tên nhà cung cấp không được để trống."
            )

        nha_cung_cap["ten_nha_cung_cap"] = (
            ten_nha_cung_cap.strip()
        )

    if so_dien_thoai is not None:
        nha_cung_cap["so_dien_thoai"] = so_dien_thoai

    if dia_chi is not None:
        nha_cung_cap["dia_chi"] = dia_chi

    if ghi_chu is not None:
        nha_cung_cap["ghi_chu"] = ghi_chu

    return nha_cung_cap


# Thay đổi trạng thái nhà cung cấp
def doi_trang_thai_nha_cung_cap(
    ma_nha_cung_cap,
    trang_thai_moi
):
    trang_thai_hop_le = [
        "DANG_HOAT_DONG",
        "NGUNG_HOAT_DONG"
    ]

    if trang_thai_moi not in trang_thai_hop_le:
        raise ValueError(
            "Trạng thái nhà cung cấp không hợp lệ."
        )

    nha_cung_cap = tim_nha_cung_cap(ma_nha_cung_cap)

    if nha_cung_cap is None:
        raise ValueError("Không tìm thấy nhà cung cấp.")

    nha_cung_cap["trang_thai"] = trang_thai_moi

    return nha_cung_cap


# Cập nhật tổng giao dịch
def cap_nhat_tong_giao_dich(
    ma_nha_cung_cap,
    so_tien_thay_doi
):
    nha_cung_cap = tim_nha_cung_cap(ma_nha_cung_cap)

    if nha_cung_cap is None:
        raise ValueError("Không tìm thấy nhà cung cấp.")

    tong_giao_dich_moi = (
        nha_cung_cap["tong_giao_dich"]
        + so_tien_thay_doi
    )

    if tong_giao_dich_moi < 0:
        raise ValueError(
            "Tổng giao dịch không thể nhỏ hơn 0."
        )

    nha_cung_cap["tong_giao_dich"] = (
        tong_giao_dich_moi
    )

    return nha_cung_cap


# Cập nhật công nợ
def cap_nhat_cong_no(
    ma_nha_cung_cap,
    so_tien_thay_doi
):
    nha_cung_cap = tim_nha_cung_cap(ma_nha_cung_cap)

    if nha_cung_cap is None:
        raise ValueError("Không tìm thấy nhà cung cấp.")

    cong_no_moi = (
        nha_cung_cap["cong_no"]
        + so_tien_thay_doi
    )

    if cong_no_moi < 0:
        raise ValueError(
            "Công nợ không thể nhỏ hơn 0."
        )

    nha_cung_cap["cong_no"] = cong_no_moi

    return nha_cung_cap