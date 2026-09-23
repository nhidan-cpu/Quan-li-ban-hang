
from copy import deepcopy


# ============================================================
# 1. CẤU TRÚC DỮ LIỆU
# ============================================================

# Cấu trúc sản phẩm
san_pham = {
    "ma_san_pham": [],
    "ma_vat": "",
    "ten_san_pham": "",
    "danh_muc": "",
    "dvt_chinh": "",

    "gia_nhap": 0,
    "gia_ban": 0,

    "dvt_quy_doi": [
        {
            "ma_dvt_quy_doi": "",
            "ten_dvt_quy_doi": "",
            "so_luong_quy_doi": 0,
            "gia_ban_dvt_quy_doi": 0,
        }
    ]
}


# ============================================================
# 2. TẠO SẢN PHẨM
# ============================================================

def tao_san_pham(
    ma_san_pham,
    ma_vat,
    ten_san_pham,
    danh_muc,
    dvt_chinh,
    gia_nhap,
    gia_ban,
    dvt_quy_doi
):

    return {
        "ma_san_pham": ma_san_pham,
        "ma_vat": ma_vat,
        "ten_san_pham": ten_san_pham,
        "danh_muc": danh_muc,
        "dvt_chinh": dvt_chinh,

        "gia_nhap": gia_nhap,
        "gia_ban": gia_ban,

        "dvt_quy_doi": dvt_quy_doi
    }


# ============================================================
# 3. LẤY THÔNG TIN SẢN PHẨM
# ============================================================

# Lấy toàn bộ mã sản phẩm
def lay_ma_san_pham(san_pham):

    return san_pham["ma_san_pham"]


# ============================================================
# 4. ĐƠN VỊ TÍNH QUY ĐỔI
# ============================================================

# Tạo đơn vị tính quy đổi
def tao_dvt_quy_doi(
    ma_dvt_quy_doi,
    ten_dvt_quy_doi,
    so_luong_quy_doi,
    gia_ban_dvt_quy_doi
):

    return {
        "ma_dvt_quy_doi": ma_dvt_quy_doi,
        "ten_dvt_quy_doi": ten_dvt_quy_doi,
        "so_luong_quy_doi": so_luong_quy_doi,
        "gia_ban_dvt_quy_doi": gia_ban_dvt_quy_doi
    }


# Lấy hệ số quy đổi của sản phẩm
def lay_he_so_quy_doi(san_pham, dvt_nhap):

    # Nếu DVT nhập là DVT chính
    if dvt_nhap == san_pham["dvt_chinh"]:
        return 1

    # Nếu DVT nhập là DVT quy đổi
    for dvt in san_pham["dvt_quy_doi"]:

        if dvt_nhap == dvt["ten_dvt_quy_doi"]:
            return dvt["so_luong_quy_doi"]

    # Không tìm thấy DVT
    return None


# ============================================================
# 5. QUẢN LÝ MÃ
# ============================================================

# Lấy toàn bộ mã của một sản phẩm
def lay_tat_ca_ma(san_pham):

    tat_ca_ma = []

    # Lấy tất cả mã sản phẩm
    tat_ca_ma.extend(
        ma for ma in san_pham["ma_san_pham"]
        if ma
    )

    # Lấy mã VAT
    if san_pham["ma_vat"]:
        tat_ca_ma.append(san_pham["ma_vat"])

    # Lấy mã của các DVT quy đổi
    for dvt in san_pham["dvt_quy_doi"]:

        if dvt["ma_dvt_quy_doi"]:
            tat_ca_ma.append(dvt["ma_dvt_quy_doi"])

    return tat_ca_ma


# Kiểm tra mã của hai sản phẩm có bị trùng hay không
def kiem_tra_trung_ma(san_pham_cu, san_pham_moi):

    ma_cu = set(lay_tat_ca_ma(san_pham_cu))
    ma_moi = set(lay_tat_ca_ma(san_pham_moi))

    ma_trung = ma_cu.intersection(ma_moi)

    if ma_trung:

        print(f"Lỗi: Mã đã tồn tại: {ma_trung}")

        return False

    return True


# ============================================================
# 6. THÊM SẢN PHẨM
# ============================================================

# Chuẩn bị bản nháp sản phẩm mới
def chuan_bi_them(danh_sach_san_pham, san_pham_moi):

    # Tạo bản nháp độc lập
    san_pham_nhap = deepcopy(san_pham_moi)

    # Kiểm tra mã với các sản phẩm hiện có
    for san_pham_cu in danh_sach_san_pham:

        if not kiem_tra_trung_ma(
            san_pham_cu,
            san_pham_nhap
        ):
            return None

    return san_pham_nhap


# Lưu sản phẩm mới
def luu_them_moi(danh_sach_san_pham, san_pham_nhap):

    danh_sach_san_pham.append(san_pham_nhap)

    print("Thêm sản phẩm thành công")


# ============================================================
# 7. TÌM SẢN PHẨM
# ============================================================

# Tìm sản phẩm theo mã sản phẩm hoặc mã DVT quy đổi
def tim_san_pham(danh_sach_san_pham, ma_can_tim):

    for san_pham in danh_sach_san_pham:

        # Tìm trong toàn bộ mã sản phẩm
        if ma_can_tim in san_pham["ma_san_pham"]:
            return san_pham

        # Tìm theo mã VAT
        if ma_can_tim == san_pham["ma_vat"]:
            return san_pham

        # Tìm theo mã DVT quy đổi
        for dvt in san_pham["dvt_quy_doi"]:

            if ma_can_tim == dvt["ma_dvt_quy_doi"]:
                return san_pham

    return None


# ============================================================
# 8. SỬA SẢN PHẨM
# ============================================================

# Chuẩn bị bản nháp sản phẩm cần sửa
def chuan_bi_sua(
    danh_sach_san_pham,
    san_pham_can_sua,
    thay_doi
):

    # Tạo bản nháp độc lập
    san_pham_nhap = deepcopy(san_pham_can_sua)

    # Áp dụng thay đổi vào bản nháp
    san_pham_nhap.update(thay_doi)

    # Kiểm tra mã với các sản phẩm khác
    for san_pham in danh_sach_san_pham:

        # Bỏ qua chính sản phẩm đang sửa
        if san_pham is san_pham_can_sua:
            continue

        # Kiểm tra mã
        if not kiem_tra_trung_ma(
            san_pham,
            san_pham_nhap
        ):
            return None

    return (
        san_pham_can_sua,
        san_pham_nhap
    )


# Lưu sản phẩm sau khi sửa
def luu_san_pham(
    san_pham_can_sua,
    san_pham_nhap
):

    san_pham_can_sua.update(san_pham_nhap)

    print("Sửa sản phẩm thành công")


# ============================================================
# 9. THÊM ĐƠN VỊ TÍNH QUY ĐỔI
# ============================================================

# Chuẩn bị bản nháp DVT mới
def chuan_bi_them_dvt(
    danh_sach_san_pham,
    san_pham,
    dvt_moi
):

    # Tạo bản nháp DVT độc lập
    dvt_nhap = deepcopy(dvt_moi)

    # Lấy mã DVT mới
    ma_dvt_moi = dvt_nhap["ma_dvt_quy_doi"]

    # DVT không có mã thì không cần kiểm tra
    if ma_dvt_moi:

        # Kiểm tra với các sản phẩm khác
        for san_pham_cu in danh_sach_san_pham:

            # Bỏ qua chính sản phẩm đang thêm DVT
            if san_pham_cu is san_pham:
                continue

            # Lấy toàn bộ mã của sản phẩm khác
            tat_ca_ma = lay_tat_ca_ma(san_pham_cu)

            # Kiểm tra mã DVT
            if ma_dvt_moi in tat_ca_ma:

                print(
                    f"Lỗi: Mã DVT quy đổi "
                    f"'{ma_dvt_moi}' đã tồn tại"
                )

                return None

    return dvt_nhap


# Lưu DVT mới
def luu_them_dvt(san_pham, dvt_nhap):

    san_pham["dvt_quy_doi"].append(dvt_nhap)

    print("Thêm đơn vị tính quy đổi thành công")


# ============================================================
# 10. SỬA ĐƠN VỊ TÍNH QUY ĐỔI
# ============================================================

# Chuẩn bị bản nháp DVT cần sửa
def chuan_bi_sua_dvt(
    dvt_can_sua,
    thay_doi
):

    # Tạo bản nháp DVT độc lập
    dvt_nhap = deepcopy(dvt_can_sua)

    # Áp dụng thay đổi vào bản nháp
    dvt_nhap.update(thay_doi)

    return (
        dvt_can_sua,
        dvt_nhap
    )


# Kiểm tra DVT sau khi sửa
def kiem_tra_sua_dvt(
    danh_sach_san_pham,
    san_pham_chua_dvt,
    dvt_nhap,
    ten_dvt_quy_doi_moi
):

    # DVT quy đổi không được trùng với DVT chính
    if ten_dvt_quy_doi_moi == san_pham_chua_dvt["dvt_chinh"]:

        print(
            "Tên DVT quy đổi không được "
            "trùng với DVT chính"
        )

        return None

    # Lấy mã DVT sau khi sửa
    ma_dvt_moi = dvt_nhap["ma_dvt_quy_doi"]

    # DVT không có mã thì không cần kiểm tra
    if not ma_dvt_moi:
        return True

    # Kiểm tra với các sản phẩm khác
    for san_pham in danh_sach_san_pham:

        # Bỏ qua sản phẩm đang chứa DVT được sửa
        if san_pham is san_pham_chua_dvt:
            continue

        # Lấy toàn bộ mã của sản phẩm khác
        tat_ca_ma = lay_tat_ca_ma(san_pham)

        # Kiểm tra mã DVT mới
        if ma_dvt_moi in tat_ca_ma:

            print(
                f"Lỗi: Mã DVT quy đổi "
                f"'{ma_dvt_moi}' đã tồn tại"
            )

            return False

    return True


# Lưu DVT sau khi sửa
def luu_dvt_quy_doi(
    dvt_can_sua,
    dvt_nhap
):

    dvt_can_sua.update(dvt_nhap)

    print("Sửa DVT quy đổi thành công")


# ============================================================
# 11. XÓA ĐƠN VỊ TÍNH QUY ĐỔI
# ============================================================

def xoa_dvt_quy_doi(
    san_pham,
    dvt_duoc_chon
):

    san_pham["dvt_quy_doi"].remove(dvt_duoc_chon)

    print("Xóa đơn vị tính quy đổi thành công")


# ============================================================
# 12. XEM SẢN PHẨM
# ============================================================

# Xem danh sách sản phẩm
def xem_danh_sach_san_pham(danh_sach_san_pham):

    for san_pham in danh_sach_san_pham:

        print(
            f"{san_pham['ma_san_pham']} | "
            f"{san_pham['ten_san_pham']} | "
            f"{san_pham['gia_ban']} | "
            f"{san_pham['dvt_chinh']}"
        )


# Xem chi tiết một sản phẩm
def xem_chi_tiet_san_pham(san_pham):

    print(san_pham)

    return san_pham


# ============================================================
# 13. XÓA SẢN PHẨM
# ============================================================

def xoa_san_pham(
    danh_sach_san_pham,
    san_pham_duoc_chon
):

    danh_sach_san_pham.remove(san_pham_duoc_chon)

    print("Xóa sản phẩm thành công")
