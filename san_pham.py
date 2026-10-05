from copy import deepcopy


# ============================================================
# 1. CẤU TRÚC DỮ LIỆU
# ============================================================


class DVTQuyDoi:
    """Đơn vị tính quy đổi thuộc một sản phẩm."""

    def __init__(
        self,
        ma_dvt_quy_doi,
        ten_dvt_quy_doi,
        so_luong_quy_doi,
        gia_ban_dvt_quy_doi
    ):
        self.ma_dvt_quy_doi = ma_dvt_quy_doi
        self.ten_dvt_quy_doi = ten_dvt_quy_doi
        self.so_luong_quy_doi = so_luong_quy_doi
        self.gia_ban_dvt_quy_doi = gia_ban_dvt_quy_doi

    def cap_nhat(self, thay_doi):
        """Cập nhật dữ liệu của chính DVT quy đổi."""

        for ten_truong, gia_tri in thay_doi.items():
            setattr(self, ten_truong, gia_tri)


class SanPham:
    """Sản phẩm và các dữ liệu thuộc về chính sản phẩm đó."""

    def __init__(
        self,
        ma_san_pham,
        ma_vat,
        ten_san_pham,
        danh_muc,
        dvt_chinh,
        gia_nhap,
        gia_ban,
        dvt_quy_doi
    ):
        self.ma_san_pham = ma_san_pham
        self.ma_vat = ma_vat
        self.ten_san_pham = ten_san_pham
        self.danh_muc = danh_muc
        self.dvt_chinh = dvt_chinh
        self.gia_nhap = gia_nhap
        self.gia_ban = gia_ban
        self.dvt_quy_doi = dvt_quy_doi

    def cap_nhat(self, thay_doi):
        """Cập nhật dữ liệu của chính sản phẩm."""

        for ten_truong, gia_tri in thay_doi.items():
            setattr(self, ten_truong, gia_tri)

    def lay_ma_san_pham(self):
        return self.ma_san_pham

    def lay_he_so_quy_doi(self, dvt_nhap):

        # Nếu DVT nhập là DVT chính
        if dvt_nhap == self.dvt_chinh:
            return 1

        # Nếu DVT nhập là DVT quy đổi
        for dvt in self.dvt_quy_doi:

            if dvt_nhap == dvt.ten_dvt_quy_doi:
                return dvt.so_luong_quy_doi

        # Không tìm thấy DVT
        return None

    def lay_tat_ca_ma(self):

        tat_ca_ma = []

        # Lấy tất cả mã sản phẩm
        tat_ca_ma.extend(
            ma for ma in self.ma_san_pham
            if ma
        )

        # Lấy mã VAT
        if self.ma_vat:
            tat_ca_ma.append(self.ma_vat)

        # Lấy mã của các DVT quy đổi
        for dvt in self.dvt_quy_doi:

            if dvt.ma_dvt_quy_doi:
                tat_ca_ma.append(dvt.ma_dvt_quy_doi)

        return tat_ca_ma

    def them_dvt_quy_doi(self, dvt_moi):
        self.dvt_quy_doi.append(dvt_moi)

    def sua_dvt_quy_doi(self, dvt_can_sua, thay_doi):
        dvt_can_sua.cap_nhat(thay_doi)

    def xoa_dvt_quy_doi(self, dvt_duoc_chon):
        self.dvt_quy_doi.remove(dvt_duoc_chon)

    def thong_tin_chi_tiet(self):
        return {
            "ma_san_pham": self.ma_san_pham,
            "ma_vat": self.ma_vat,
            "ten_san_pham": self.ten_san_pham,
            "danh_muc": self.danh_muc,
            "dvt_chinh": self.dvt_chinh,
            "gia_nhap": self.gia_nhap,
            "gia_ban": self.gia_ban,
            "dvt_quy_doi": self.dvt_quy_doi
        }


# ============================================================
# 2. QUẢN LÝ MÃ
# ============================================================


def kiem_tra_trung_ma(san_pham_cu, san_pham_moi):

    ma_cu = set(san_pham_cu.lay_tat_ca_ma())
    ma_moi = set(san_pham_moi.lay_tat_ca_ma())

    ma_trung = ma_cu.intersection(ma_moi)

    if ma_trung:

        print(f"Lỗi: Mã đã tồn tại: {ma_trung}")

        return False

    return True


# ============================================================
# 3. THÊM SẢN PHẨM
# ============================================================


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


def luu_them_moi(danh_sach_san_pham, san_pham_nhap):

    danh_sach_san_pham.append(san_pham_nhap)

    print("Thêm sản phẩm thành công")


# ============================================================
# 4. TÌM SẢN PHẨM
# ============================================================


def tim_san_pham(danh_sach_san_pham, ma_can_tim):

    for san_pham in danh_sach_san_pham:

        # Tìm trong toàn bộ mã
        if ma_can_tim in san_pham.lay_tat_ca_ma():
            return san_pham

    return None


# ============================================================
# 5. SỬA SẢN PHẨM
# ============================================================


def chuan_bi_sua(
    danh_sach_san_pham,
    san_pham_can_sua,
    thay_doi
):

    # Tạo bản nháp độc lập
    san_pham_nhap = deepcopy(san_pham_can_sua)

    # Áp dụng thay đổi vào bản nháp
    san_pham_nhap.cap_nhat(thay_doi)

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


def luu_san_pham(
    san_pham_can_sua,
    san_pham_nhap
):

    san_pham_can_sua.cap_nhat(
        san_pham_nhap.thong_tin_chi_tiet()
    )

    print("Sửa sản phẩm thành công")


# ============================================================
# 6. THÊM ĐƠN VỊ TÍNH QUY ĐỔI
# ============================================================


def chuan_bi_them_dvt(
    danh_sach_san_pham,
    san_pham,
    dvt_moi
):

    # Tạo bản nháp DVT độc lập
    dvt_nhap = deepcopy(dvt_moi)

    # Lấy mã DVT mới
    ma_dvt_moi = dvt_nhap.ma_dvt_quy_doi

    # DVT không có mã thì không cần kiểm tra
    if ma_dvt_moi:

        # Kiểm tra với các sản phẩm khác
        for san_pham_cu in danh_sach_san_pham:

            # Bỏ qua chính sản phẩm đang thêm DVT
            if san_pham_cu is san_pham:
                continue

            # Lấy toàn bộ mã của sản phẩm khác
            tat_ca_ma = san_pham_cu.lay_tat_ca_ma()

            # Kiểm tra mã DVT
            if ma_dvt_moi in tat_ca_ma:

                print(
                    f"Lỗi: Mã DVT quy đổi "
                    f"'{ma_dvt_moi}' đã tồn tại"
                )

                return None

    return dvt_nhap


def luu_them_dvt(san_pham, dvt_nhap):

    san_pham.them_dvt_quy_doi(dvt_nhap)

    print("Thêm đơn vị tính quy đổi thành công")


# ============================================================
# 7. SỬA ĐƠN VỊ TÍNH QUY ĐỔI
# ============================================================


def chuan_bi_sua_dvt(
    dvt_can_sua,
    thay_doi
):

    # Tạo bản nháp DVT độc lập
    dvt_nhap = deepcopy(dvt_can_sua)

    # Áp dụng thay đổi vào bản nháp
    dvt_nhap.cap_nhat(thay_doi)

    return (
        dvt_can_sua,
        dvt_nhap
    )


def kiem_tra_sua_dvt(
    danh_sach_san_pham,
    san_pham_chua_dvt,
    dvt_nhap,
    ten_dvt_quy_doi_moi
):

    # DVT quy đổi không được trùng với DVT chính
    if ten_dvt_quy_doi_moi == san_pham_chua_dvt.dvt_chinh:

        print(
            "Tên DVT quy đổi không được "
            "trùng với DVT chính"
        )

        return None

    # Lấy mã DVT sau khi sửa
    ma_dvt_moi = dvt_nhap.ma_dvt_quy_doi

    # DVT không có mã thì không cần kiểm tra
    if not ma_dvt_moi:
        return True

    # Kiểm tra với các sản phẩm khác
    for san_pham in danh_sach_san_pham:

        # Bỏ qua sản phẩm đang chứa DVT được sửa
        if san_pham is san_pham_chua_dvt:
            continue

        # Lấy toàn bộ mã của sản phẩm khác
        tat_ca_ma = san_pham.lay_tat_ca_ma()

        # Kiểm tra mã DVT mới
        if ma_dvt_moi in tat_ca_ma:

            print(
                f"Lỗi: Mã DVT quy đổi "
                f"'{ma_dvt_moi}' đã tồn tại"
            )

            return False

    return True


def luu_dvt_quy_doi(
    san_pham,
    dvt_can_sua,
    dvt_nhap
):

    thay_doi = {
        "ma_dvt_quy_doi": dvt_nhap.ma_dvt_quy_doi,
        "ten_dvt_quy_doi": dvt_nhap.ten_dvt_quy_doi,
        "so_luong_quy_doi": dvt_nhap.so_luong_quy_doi,
        "gia_ban_dvt_quy_doi": dvt_nhap.gia_ban_dvt_quy_doi
    }

    san_pham.sua_dvt_quy_doi(
        dvt_can_sua,
        thay_doi
    )

    print("Sửa DVT quy đổi thành công")


# ============================================================
# 8. XÓA ĐƠN VỊ TÍNH QUY ĐỔI
# ============================================================


def xoa_dvt_quy_doi(
    san_pham,
    dvt_duoc_chon
):

    san_pham.xoa_dvt_quy_doi(dvt_duoc_chon)

    print("Xóa đơn vị tính quy đổi thành công")


# ============================================================
# 9. XEM SẢN PHẨM
# ============================================================


def xem_danh_sach_san_pham(danh_sach_san_pham):

    for san_pham in danh_sach_san_pham:

        print(
            f"{san_pham.ma_san_pham} | "
            f"{san_pham.ten_san_pham} | "
            f"{san_pham.gia_ban} | "
            f"{san_pham.dvt_chinh}"
        )


def xem_chi_tiet_san_pham(san_pham):

    chi_tiet = san_pham.thong_tin_chi_tiet()

    print(chi_tiet)

    return chi_tiet


# ============================================================
# 10. XÓA SẢN PHẨM
# ============================================================


def xoa_san_pham(
    danh_sach_san_pham,
    san_pham_duoc_chon
):

    danh_sach_san_pham.remove(san_pham_duoc_chon)

    print("Xóa sản phẩm thành công")
