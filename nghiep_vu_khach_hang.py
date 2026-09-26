from copy import deepcopy


mau_khach_hang = {
    "ma_khach_hang": "",
    "ten_khach_hang": "",
    "so_dien_thoai": "",
    "dia_chi": "",
    "phan_khuc_khach_hang": "",
    "tong_giao_dich": 0,
    "cong_no": 0,
    "trang_thai": "DANG_HOAT_DONG",
    "ghi_chu": ""
}


danh_sach_khach_hang = []


# Tìm khách hàng theo mã
def tim_khach_hang(ma_khach_hang):
    for khach_hang in danh_sach_khach_hang:
        if khach_hang["ma_khach_hang"] == ma_khach_hang:
            return khach_hang
    return None


# Tạo mã khách hàng mới
def tao_ma_khach_hang():
    so_ma_lon_nhat = 0

    for khach_hang in danh_sach_khach_hang:
        ma_khach_hang = khach_hang["ma_khach_hang"]

        if not ma_khach_hang.startswith("KH-"):
            continue

        try:
            so_ma = int(ma_khach_hang[3:])
        except ValueError:
            continue

        if so_ma > so_ma_lon_nhat:
            so_ma_lon_nhat = so_ma

    return f"KH-{so_ma_lon_nhat + 1:04d}"


# Tạo khách hàng mới
def tao_khach_hang(
    ten_khach_hang,
    so_dien_thoai="",
    dia_chi="",
    phan_khuc_khach_hang="",
    ghi_chu=""
):
    if not isinstance(ten_khach_hang, str):
        raise ValueError("Tên khách hàng phải là chuỗi.")

    if not ten_khach_hang.strip():
        raise ValueError("Tên khách hàng không được để trống.")

    khach_hang_moi = deepcopy(mau_khach_hang)

    khach_hang_moi["ma_khach_hang"] = tao_ma_khach_hang()
    khach_hang_moi["ten_khach_hang"] = ten_khach_hang.strip()
    khach_hang_moi["so_dien_thoai"] = so_dien_thoai
    khach_hang_moi["dia_chi"] = dia_chi
    khach_hang_moi["phan_khuc_khach_hang"] = phan_khuc_khach_hang
    khach_hang_moi["ghi_chu"] = ghi_chu

    danh_sach_khach_hang.append(khach_hang_moi)

    return khach_hang_moi


# Sửa thông tin khách hàng
def sua_khach_hang(
    ma_khach_hang,
    ten_khach_hang=None,
    so_dien_thoai=None,
    dia_chi=None,
    phan_khuc_khach_hang=None,
    ghi_chu=None
):
    khach_hang = tim_khach_hang(ma_khach_hang)

    if khach_hang is None:
        raise ValueError("Không tìm thấy khách hàng.")

    if ten_khach_hang is not None:
        if not isinstance(ten_khach_hang, str):
            raise ValueError("Tên khách hàng phải là chuỗi.")

        if not ten_khach_hang.strip():
            raise ValueError("Tên khách hàng không được để trống.")

        khach_hang["ten_khach_hang"] = ten_khach_hang.strip()

    if so_dien_thoai is not None:
        khach_hang["so_dien_thoai"] = so_dien_thoai

    if dia_chi is not None:
        khach_hang["dia_chi"] = dia_chi

    if phan_khuc_khach_hang is not None:
        khach_hang["phan_khuc_khach_hang"] = (
            phan_khuc_khach_hang
        )

    if ghi_chu is not None:
        khach_hang["ghi_chu"] = ghi_chu

    return khach_hang


# Thay đổi trạng thái khách hàng
def doi_trang_thai_khach_hang(
    ma_khach_hang,
    trang_thai_moi
):
    trang_thai_hop_le = [
        "DANG_HOAT_DONG",
        "NGUNG_HOAT_DONG"
    ]

    if trang_thai_moi not in trang_thai_hop_le:
        raise ValueError(
            "Trạng thái khách hàng không hợp lệ."
        )

    khach_hang = tim_khach_hang(ma_khach_hang)

    if khach_hang is None:
        raise ValueError("Không tìm thấy khách hàng.")

    khach_hang["trang_thai"] = trang_thai_moi

    return khach_hang


# Cập nhật tổng giao dịch
def cap_nhat_tong_giao_dich(
    ma_khach_hang,
    so_tien_thay_doi
):
    khach_hang = tim_khach_hang(ma_khach_hang)

    if khach_hang is None:
        raise ValueError("Không tìm thấy khách hàng.")

    tong_giao_dich_moi = (
        khach_hang["tong_giao_dich"]
        + so_tien_thay_doi
    )

    if tong_giao_dich_moi < 0:
        raise ValueError(
            "Tổng giao dịch không thể nhỏ hơn 0."
        )

    khach_hang["tong_giao_dich"] = (
        tong_giao_dich_moi
    )

    return khach_hang


# Cập nhật công nợ
def cap_nhat_cong_no(
    ma_khach_hang,
    so_tien_thay_doi
):
    khach_hang = tim_khach_hang(ma_khach_hang)

    if khach_hang is None:
        raise ValueError("Không tìm thấy khách hàng.")

    cong_no_moi = (
        khach_hang["cong_no"]
        + so_tien_thay_doi
    )

    if cong_no_moi < 0:
        raise ValueError(
            "Công nợ không thể nhỏ hơn 0."
        )

    khach_hang["cong_no"] = cong_no_moi

    return khach_hang
