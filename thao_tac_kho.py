# Cấu trúc một dòng tồn kho
ton_kho = {
    "ma_kho": "",
    "ma_san_pham": "",
    "ma_vat": "",
    "ten_san_pham": "",
    "dvt_chinh": "",
    "so_luong_ton": 0,
    "gia_tri_ton": 0,
    "gia_von_binh_quan": 0,
}


# Danh sách toàn bộ tồn kho
danh_sach_ton_kho = []


# Tạo một dòng tồn kho mới
def tao_ton_kho(ma_kho, san_pham):
    return {
        "ma_kho": ma_kho,
        "ma_san_pham": san_pham["ma_san_pham"][0],
        "ma_vat": san_pham["ma_vat"],
        "ten_san_pham": san_pham["ten_san_pham"],
        "dvt_chinh": san_pham["dvt_chinh"],
        "so_luong_ton": 0,
        "gia_tri_ton": 0,
        "gia_von_binh_quan": 0,
    }


# Khởi tạo toàn bộ danh sách tồn kho
def khoi_tao_danh_sach_ton_kho(
    danh_sach_ton_kho,
    danh_sach_san_pham,
    danh_sach_kho
):
    if danh_sach_ton_kho:
        return

    for kho in danh_sach_kho:
        for san_pham in danh_sach_san_pham:
            ton_moi = tao_ton_kho(
                kho["ma_kho"],
                san_pham
            )

            danh_sach_ton_kho.append(ton_moi)


# Tìm tồn kho theo kho và sản phẩm
def tim_ton_kho(
    danh_sach_ton_kho,
    ma_kho,
    ma_san_pham
):
    for ton in danh_sach_ton_kho:
        if (
            ton["ma_kho"] == ma_kho
            and ton["ma_san_pham"] == ma_san_pham
        ):
            return ton

    return None


# Tìm kho theo tên kho
def tim_kho_theo_ten(
    danh_sach_kho,
    ten_kho
):
    for kho in danh_sach_kho:
        if kho["ten_kho"] == ten_kho:
            return kho

    return None


# Tìm kho theo mã kho
def tim_kho_theo_ma(
    danh_sach_kho,
    ma_kho
):
    for kho in danh_sach_kho:
        if kho["ma_kho"] == ma_kho:
            return kho

    return None


# Cập nhật một dòng tồn kho sau khi nhập hàng
def cap_nhat_ton_kho_tu_chi_tiet(
    ton_kho,
    so_luong_nhap,
    gia_tri_nhap
):
    ton_kho["so_luong_ton"] += so_luong_nhap
    ton_kho["gia_tri_ton"] += gia_tri_nhap

    if ton_kho["so_luong_ton"] > 0:
        ton_kho["gia_von_binh_quan"] = (
            ton_kho["gia_tri_ton"]
            / ton_kho["so_luong_ton"]
        )
    else:
        ton_kho["gia_von_binh_quan"] = 0


# Áp dụng một phiếu nhập vào tồn kho
def ap_dung_phieu_nhap_vao_kho(
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu_nhap
):
    kho = tim_kho_theo_ma(
        danh_sach_kho,
        phieu_nhap["ma_kho_nhap"]
    )

    if kho is None:
        raise ValueError(
            f"Không tìm thấy kho: "
            f"{phieu_nhap['ma_kho_nhap']}"
        )

    ma_kho = kho["ma_kho"]

    for chi_tiet in phieu_nhap["chi_tiet"]:
        ma_san_pham = chi_tiet["ma_san_pham"]

        ton = tim_ton_kho(
            danh_sach_ton_kho,
            ma_kho,
            ma_san_pham
        )

        if ton is None:
            raise ValueError(
                f"Không tìm thấy tồn kho cho "
                f"kho {ma_kho}, sản phẩm {ma_san_pham}"
            )

        cap_nhat_ton_kho_tu_chi_tiet(
            ton,
            chi_tiet["so_luong_quy_doi"],
            chi_tiet["thanh_tien_tung_dong"]
        )


# Hoàn tác ảnh hưởng của một phiếu nhập khỏi tồn kho
def hoan_tac_phieu_nhap_vao_kho(
    danh_sach_ton_kho,
    danh_sach_kho,
    phieu_nhap
):
    kho = tim_kho_theo_ma(
        danh_sach_kho,
        phieu_nhap["ma_kho_nhap"]
    )

    if kho is None:
        raise ValueError(
            f"Không tìm thấy kho: "
            f"{phieu_nhap['ma_kho_nhap']}"
        )

    ma_kho = kho["ma_kho"]

    for chi_tiet in phieu_nhap["chi_tiet"]:
        ma_san_pham = chi_tiet["ma_san_pham"]

        ton = tim_ton_kho(
            danh_sach_ton_kho,
            ma_kho,
            ma_san_pham
        )

        if ton is None:
            raise ValueError(
                f"Không tìm thấy tồn kho cho "
                f"kho {ma_kho}, sản phẩm {ma_san_pham}"
            )

        ton["so_luong_ton"] -= (
            chi_tiet["so_luong_quy_doi"]
        )

        ton["gia_tri_ton"] -= (
            chi_tiet["thanh_tien_tung_dong"]
        )

        if ton["so_luong_ton"] > 0:
            ton["gia_von_binh_quan"] = (
                ton["gia_tri_ton"]
                / ton["so_luong_ton"]
            )
        else:
            ton["gia_von_binh_quan"] = 0




    