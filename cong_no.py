# ============================================================
# NGHIỆP VỤ CÔNG NỢ
# ============================================================


# Danh sách toàn bộ các lần phát sinh công nợ.
# Không lưu số dư trực tiếp trong hồ sơ NCC/KH.
danh_sach_phat_sinh_cong_no = []


# Cấu trúc một lần phát sinh công nợ.
mau_phat_sinh_cong_no = {
    "loai_doi_tuong": "",
    "ma_doi_tuong": "",
    "loai_phat_sinh": "",
    "ma_chung_tu": "",
    "ngay_phat_sinh": None,
    "so_tien": 0,
    "ghi_chu": ""
}


# ============================================================
# 1. TÌM PHÁT SINH CÔNG NỢ
# ============================================================

def tim_phat_sinh_cong_no(
    loai_doi_tuong,
    ma_doi_tuong,
    loai_phat_sinh,
    ma_chung_tu
):

    for phat_sinh in danh_sach_phat_sinh_cong_no:

        if (
            phat_sinh["loai_doi_tuong"]
            == loai_doi_tuong
            and phat_sinh["ma_doi_tuong"]
            == ma_doi_tuong
            and phat_sinh["loai_phat_sinh"]
            == loai_phat_sinh
            and phat_sinh["ma_chung_tu"]
            == ma_chung_tu
        ):

            return phat_sinh

    return None


# ============================================================
# 2. TẠO PHÁT SINH CÔNG NỢ
# ============================================================

def tao_phat_sinh_cong_no(
    loai_doi_tuong,
    ma_doi_tuong,
    loai_phat_sinh,
    ma_chung_tu,
    ngay_phat_sinh,
    so_tien,
    ghi_chu=""
):

    if loai_doi_tuong not in ("NCC", "KH"):
        raise ValueError(
            "Loại đối tượng phải là 'NCC' hoặc 'KH'."
        )

    if not ma_doi_tuong:
        raise ValueError(
            "Mã đối tượng không được để trống."
        )

    if not loai_phat_sinh:
        raise ValueError(
            "Loại phát sinh không được để trống."
        )

    if not ma_chung_tu:
        raise ValueError(
            "Mã chứng từ không được để trống."
        )

    if not isinstance(so_tien, (int, float)):
        raise ValueError(
            "Số tiền phát sinh phải là số."
        )

    if so_tien == 0:
        raise ValueError(
            "Số tiền phát sinh không được bằng 0."
        )

    phat_sinh_cu = tim_phat_sinh_cong_no(
        loai_doi_tuong,
        ma_doi_tuong,
        loai_phat_sinh,
        ma_chung_tu
    )

    if phat_sinh_cu is not None:
        raise ValueError(
            f"Chứng từ '{ma_chung_tu}' "
            f"đã phát sinh công nợ."
        )

    phat_sinh = {
        "loai_doi_tuong": loai_doi_tuong,
        "ma_doi_tuong": ma_doi_tuong,
        "loai_phat_sinh": loai_phat_sinh,
        "ma_chung_tu": ma_chung_tu,
        "ngay_phat_sinh": ngay_phat_sinh,
        "so_tien": so_tien,
        "ghi_chu": ghi_chu
    }

    danh_sach_phat_sinh_cong_no.append(
        phat_sinh
    )

    return phat_sinh


# ============================================================
# 3. HOÀN TÁC PHÁT SINH CÔNG NỢ
# ============================================================

def hoan_tac_phat_sinh_cong_no(
    loai_doi_tuong,
    ma_doi_tuong,
    loai_phat_sinh,
    ma_chung_tu
):

    phat_sinh = tim_phat_sinh_cong_no(
        loai_doi_tuong,
        ma_doi_tuong,
        loai_phat_sinh,
        ma_chung_tu
    )

    if phat_sinh is None:
        return None

    danh_sach_phat_sinh_cong_no.remove(
        phat_sinh
    )

    return phat_sinh


# ============================================================
# 4. TÍNH CÔNG NỢ HIỆN TẠI
# ============================================================

def tinh_cong_no(
    loai_doi_tuong,
    ma_doi_tuong
):

    if loai_doi_tuong not in ("NCC", "KH"):
        raise ValueError(
            "Loại đối tượng phải là 'NCC' hoặc 'KH'."
        )

    if ma_doi_tuong is None:
        return 0

    tong_cong_no = 0

    for phat_sinh in danh_sach_phat_sinh_cong_no:

        if (
            phat_sinh["loai_doi_tuong"]
            == loai_doi_tuong
            and phat_sinh["ma_doi_tuong"]
            == ma_doi_tuong
        ):

            tong_cong_no += phat_sinh["so_tien"]

    return tong_cong_no


# ============================================================
# 5. CÔNG NỢ NCC - PHIẾU NHẬP
# ============================================================

def phat_sinh_cong_no_tu_phieu_nhap(
    phieu_nhap
):

    ma_nha_cung_cap = (
        phieu_nhap["nha_cung_cap"]
    )

    # Không có NCC → không phát sinh công nợ.
    if (
        ma_nha_cung_cap is None
        or (
            isinstance(ma_nha_cung_cap, str)
            and not ma_nha_cung_cap.strip()
        )
    ):
        return None

    return tao_phat_sinh_cong_no(
        loai_doi_tuong="NCC",
        ma_doi_tuong=ma_nha_cung_cap,
        loai_phat_sinh="PHIEU_NHAP",
        ma_chung_tu=phieu_nhap["ma_phieu_nhap"],
        ngay_phat_sinh=phieu_nhap["ngay_nhap"],
        so_tien=phieu_nhap["tong_thanh_tien"]
    )


def hoan_tac_cong_no_tu_phieu_nhap(
    phieu_nhap
):

    ma_nha_cung_cap = (
        phieu_nhap["nha_cung_cap"]
    )

    if (
        ma_nha_cung_cap is None
        or (
            isinstance(ma_nha_cung_cap, str)
            and not ma_nha_cung_cap.strip()
        )
    ):
        return None

    return hoan_tac_phat_sinh_cong_no(
        loai_doi_tuong="NCC",
        ma_doi_tuong=ma_nha_cung_cap,
        loai_phat_sinh="PHIEU_NHAP",
        ma_chung_tu=phieu_nhap["ma_phieu_nhap"]
    )


# ============================================================
# 6. CÔNG NỢ KH - PHIẾU GNTT
# ============================================================

def phat_sinh_cong_no_tu_gntt(
    phieu_gntt
):

    ma_khach_hang = (
        phieu_gntt["ma_khach_hang"]
    )

    # Không có KH → không phát sinh công nợ.
    if (
        ma_khach_hang is None
        or (
            isinstance(ma_khach_hang, str)
            and not ma_khach_hang.strip()
        )
    ):
        return None

    return tao_phat_sinh_cong_no(
        loai_doi_tuong="KH",
        ma_doi_tuong=ma_khach_hang,
        loai_phat_sinh="PHIEU_GNTT",
        ma_chung_tu=phieu_gntt["ma_phieu"],
        ngay_phat_sinh=phieu_gntt["thoi_gian_tao"],
        so_tien=phieu_gntt["tong_thanh_tien"]
    )


def hoan_tac_cong_no_tu_gntt(
    phieu_gntt
):

    ma_khach_hang = (
        phieu_gntt["ma_khach_hang"]
    )

    if (
        ma_khach_hang is None
        or (
            isinstance(ma_khach_hang, str)
            and not ma_khach_hang.strip()
        )
    ):
        return None

    return hoan_tac_phat_sinh_cong_no(
        loai_doi_tuong="KH",
        ma_doi_tuong=ma_khach_hang,
        loai_phat_sinh="PHIEU_GNTT",
        ma_chung_tu=phieu_gntt["ma_phieu"]
    )