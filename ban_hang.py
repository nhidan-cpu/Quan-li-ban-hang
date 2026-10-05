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

from khach_hang import (
    tim_khach_hang,
    cap_nhat_tong_giao_dich
)

from cong_no import (
    phat_sinh_cong_no_tu_gntt,
    hoan_tac_cong_no_tu_gntt
)


# ============================================================
# 1. CẤU TRÚC DỮ LIỆU
# ============================================================

phieu_ban = {
    "ma_phieu": "",
    "thoi_gian_tao": "",
    "ma_khach_hang": "",
    "ten_khach_hang": "",
    "chi_tiet": [],
    "tong_thanh_tien": 0
}


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


danh_sach_phieu_gntt = []

# Tên cũ dùng cho các đoạn code đang gọi module bán hàng.
danh_sach_phieu_ban = danh_sach_phieu_gntt


# ============================================================
# 2. TRẠNG THÁI BẢN NHÁP
# ============================================================

_KHONG_THAY_DOI = object()


def danh_dau_phieu_da_thay_doi(phieu):

    phieu["_da_thay_doi"] = True

    return phieu


def phieu_co_thay_doi_chua_luu(phieu):

    return phieu.get("_da_thay_doi", False)


def dat_lai_trang_thai_phieu(phieu):

    phieu["_da_thay_doi"] = False

    return phieu


def tao_ban_luu_phieu(phieu):

    ban_luu = deepcopy(phieu)

    ban_luu.pop("_da_load", None)
    ban_luu.pop("_da_thay_doi", None)

    return ban_luu


# ============================================================
# 3. SINH MÃ GNTT
# ============================================================

def sinh_ma_phieu_gntt():

    ngay_hien_tai = datetime.now().strftime("%d%m%y")

    tien_to = f"BH{ngay_hien_tai}-"
    so_lon_nhat = 0

    for phieu in danh_sach_phieu_gntt:

        ma_phieu = phieu.get("ma_phieu")

        if not isinstance(ma_phieu, str):
            continue

        if not ma_phieu.startswith(tien_to):
            continue

        phan_so = ma_phieu[len(tien_to):]

        if phan_so.isdigit():
            so_lon_nhat = max(
                so_lon_nhat,
                int(phan_so)
            )

    return f"{tien_to}{so_lon_nhat + 1:04d}"


# ============================================================
# 4. TẠO PHIẾU BÁN
# ============================================================

def tao_phieu_ban(ma_phieu=None):

    if ma_phieu is None:
        ma_phieu = sinh_ma_phieu_gntt()

    return {
        "ma_phieu": ma_phieu,
        "thoi_gian_tao": datetime.now(),
        "ma_khach_hang": None,
        "ten_khach_hang": None,
        "ghi_chu": "",
        "tong_thanh_tien": 0,
        "tong_thanh_tien_von": 0,
        "loi_nhuan": 0,
        "ty_suat": 0,
        "chi_tiet": [],
        "_da_load": False,
        "_da_thay_doi": False
    }


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

    he_so_quy_doi = lay_he_so_quy_doi(
        san_pham,
        dvt_ban
    )

    if he_so_quy_doi is None:

        raise ValueError(
            f"ĐVT '{dvt_ban}' không tồn tại trong sản phẩm"
        )

    if so_luong <= 0:

        raise ValueError(
            "Số lượng bán phải lớn hơn 0"
        )

    so_luong_quy_doi = (
        so_luong * he_so_quy_doi
    )

    if loai_gia == "CHIA THANG":

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

        don_gia_sau_ck = (
            don_gia * (1 - ck / 100)
        )

    else:

        raise ValueError(
            f"Loại giá không hợp lệ: {loai_gia}"
        )

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
        "thanh_tien_von": 0,
        "ghi_chu": ghi_chu
    }


# ============================================================
# 5. TÍNH TOÁN CHI TIẾT
# ============================================================

def tinh_lai_chi_tiet_ban(
    san_pham,
    chi_tiet
):

    he_so_quy_doi = lay_he_so_quy_doi(
        san_pham,
        chi_tiet["dvt_ban"]
    )

    if he_so_quy_doi is None:

        raise ValueError(
            f"ĐVT '{chi_tiet['dvt_ban']}' không tồn tại trong sản phẩm"
        )

    chi_tiet["he_so_quy_doi"] = he_so_quy_doi

    if chi_tiet["so_luong"] <= 0:

        raise ValueError(
            "Số lượng bán phải lớn hơn 0"
        )

    chi_tiet["so_luong_quy_doi"] = (
        chi_tiet["so_luong"]
        * he_so_quy_doi
    )

    if chi_tiet["loai_gia"] == "CHIA THANG":

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

        chi_tiet["don_gia_sau_ck"] = (
            chi_tiet["don_gia"]
            * (1 - chi_tiet["ck"] / 100)
        )

    else:

        raise ValueError(
            f"Loại giá không hợp lệ: "
            f"{chi_tiet['loai_gia']}"
        )

    chi_tiet["thanh_tien_tung_dong"] = (
        chi_tiet["so_luong"]
        * chi_tiet["don_gia_sau_ck"]
    )

    return chi_tiet


def tinh_tong_thanh_tien(phieu):

    return sum(
        chi_tiet["thanh_tien_tung_dong"]
        for chi_tiet in phieu["chi_tiet"]
    )


def tinh_tong_thanh_tien_von(phieu):

    return sum(
        chi_tiet.get("thanh_tien_von", 0)
        for chi_tiet in phieu["chi_tiet"]
    )


def tinh_loi_nhuan(phieu):

    return (
        phieu["tong_thanh_tien"]
        - phieu["tong_thanh_tien_von"]
    )


def tinh_ty_suat(phieu):

    if phieu["tong_thanh_tien"] == 0:
        return 0

    return (
        phieu["loi_nhuan"]
        / phieu["tong_thanh_tien"]
        * 100
    )


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


def cap_nhat_tinh_toan_phieu_ban(
    danh_sach_san_pham,
    phieu
):

    for chi_tiet in phieu["chi_tiet"]:

        san_pham = tim_san_pham(
            danh_sach_san_pham,
            chi_tiet["ma_san_pham"]
        )

        if san_pham is None:

            raise ValueError(
                f"Không tìm thấy sản phẩm "
                f"'{chi_tiet['ma_san_pham']}'"
            )

        chi_tiet["ten_san_pham"] = (
            san_pham["ten_san_pham"]
        )

        if "ghi_chu" not in chi_tiet:
            chi_tiet["ghi_chu"] = ""

        tinh_lai_chi_tiet_ban(
            san_pham,
            chi_tiet
        )

    cap_nhat_tong_thanh_tien(phieu)

    return phieu


# ============================================================
# 6. THÊM CHI TIẾT VÀO PHIẾU
# ============================================================

def them_chi_tiet_vao_phieu_ban(
    danh_sach_san_pham,
    phieu,
    chi_tiet
):

    san_pham = tim_san_pham(
        danh_sach_san_pham,
        chi_tiet["ma_san_pham"]
    )

    if san_pham is None:

        raise ValueError(
            f"Không tìm thấy sản phẩm "
            f"'{chi_tiet['ma_san_pham']}'"
        )

    tinh_lai_chi_tiet_ban(
        san_pham,
        chi_tiet
    )

    chi_tiet["stt"] = (
        len(phieu["chi_tiet"]) + 1
    )

    phieu["chi_tiet"].append(
        chi_tiet
    )

    cap_nhat_tong_thanh_tien(phieu)

    danh_dau_phieu_da_thay_doi(phieu)

    return phieu


# ============================================================
# 7. KIỂM TRA DỮ LIỆU
# ============================================================

def kiem_tra_du_lieu_phieu_ban(phieu):

    if not phieu["chi_tiet"]:

        print(
            "Lỗi: Phiếu bán phải có "
            "ít nhất một sản phẩm"
        )

        return False

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

    if phieu["ma_khach_hang"] is None:
        return True

    if not isinstance(
        phieu["ma_khach_hang"],
        str
    ):

        raise ValueError(
            "Khách hàng phải là mã khách hàng "
            "hoặc để trống."
        )

    if not phieu["ma_khach_hang"].strip():

        phieu["ma_khach_hang"] = None

        return True

    if tim_khach_hang(
        phieu["ma_khach_hang"]
    ) is None:

        raise ValueError(
            f"Không tìm thấy khách hàng "
            f"'{phieu['ma_khach_hang']}'."
        )

    return True


def kiem_tra_trung_ma_phieu(ma_phieu):

    for phieu in danh_sach_phieu_ban:

        if phieu["ma_phieu"] == ma_phieu:

            return True

    return False


# ============================================================
# 8. KIỂM TRA TỒN KHO
# ============================================================

def tong_hop_so_luong_xuat(phieu):

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

        ton = tim_ton_kho(
            danh_sach_ton_kho,
            ma_kho,
            ma_san_pham
        )

        if ton is None:

            raise ValueError(
                f"Không tìm thấy tồn kho "
                f"của sản phẩm '{ma_san_pham}' "
                f"tại kho '{ma_kho}'"
            )

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
# 9. CẬP NHẬT TỒN KHO
# ============================================================

def ap_dung_phieu_ban_vao_kho(
    danh_sach_ton_kho,
    phieu,
    dung_gia_von_da_luu=False
):

    kiem_tra_ton_kho_phieu_ban(
        danh_sach_ton_kho,
        phieu
    )

    for chi_tiet in phieu["chi_tiet"]:

        ton = tim_ton_kho(
            danh_sach_ton_kho,
            chi_tiet["ma_kho"],
            chi_tiet["ma_san_pham"]
        )

        if dung_gia_von_da_luu and "thanh_tien_von" in chi_tiet:

            # Dùng lại đúng giá vốn lịch sử của lần xuất cũ.
            gia_tri_xuat = chi_tiet["thanh_tien_von"]

        elif ton["so_luong_ton"] > 0:

            # Phiếu bán mới → tính giá vốn theo tồn hiện tại.
            gia_tri_xuat = (
                chi_tiet["so_luong_quy_doi"]
                * ton["gia_tri_ton"]
                / ton["so_luong_ton"]
            )

        else:

            gia_tri_xuat = 0

        cap_nhat_ton_kho_tu_chi_tiet(
            ton,
            -chi_tiet["so_luong_quy_doi"],
            -gia_tri_xuat
        )


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
                f"tại kho '{chi_tiet['ma_kho']}'"
            )

        so_luong_hoan = (
            chi_tiet["so_luong_quy_doi"]
        )

        # Nếu phiếu đã lưu giá vốn lịch sử, hoàn tác đúng
        # giá trị vốn của chính lần xuất hàng đó.
        # Đây là giá trị cần dùng khi sửa phiếu sau khi
        # kho đã phát sinh thêm các giao dịch khác.
        if "thanh_tien_von" in chi_tiet:

            gia_tri_hoan = chi_tiet["thanh_tien_von"]

        elif ton["so_luong_ton"] > 0:

            # Tương thích với dữ liệu cũ chưa có giá vốn lịch sử.
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
# 10. LƯU PHIẾU BÁN
# ============================================================

def luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu,
    ham_tinh_gia_von=None
):

    if not kiem_tra_du_lieu_phieu_ban(phieu):
        return False

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

        try:

            phat_sinh_cong_no_tu_gntt(
                phieu
            )

            if phieu["ma_khach_hang"] is not None:

                cap_nhat_tong_giao_dich(
                    phieu["ma_khach_hang"],
                    phieu["tong_thanh_tien"]
                )

        except Exception:

            hoan_tac_cong_no_tu_gntt(
                phieu
            )

            hoan_tac_phieu_ban_vao_kho(
                danh_sach_ton_kho,
                phieu
            )

            raise

        ban_luu = tao_ban_luu_phieu(
            phieu
        )

        danh_sach_phieu_ban.append(
            ban_luu
        )

        dat_lai_trang_thai_phieu(
            phieu
        )

        print(
            "Lưu phiếu bán thành công"
        )

        return True

    return xac_nhan_luu_phieu_ban(
        danh_sach_san_pham,
        danh_sach_ton_kho,
        phieu,
        ham_tinh_gia_von
    )


# ============================================================
# 11. TÌM / LOAD PHIẾU BÁN
# ============================================================

def tim_phieu_ban(ma_phieu):

    for phieu in danh_sach_phieu_ban:

        if phieu["ma_phieu"] == ma_phieu:

            return phieu

    return None


def load_phieu_ban(ma_phieu):

    phieu_can_load = tim_phieu_ban(
        ma_phieu
    )

    if phieu_can_load is None:
        return None

    phieu_nhap = deepcopy(
        phieu_can_load
    )

    phieu_nhap["_da_load"] = True
    phieu_nhap["_da_thay_doi"] = False

    return phieu_nhap


# ============================================================
# 12. SỬA PHIẾU BÁN
# ============================================================

def sua_phieu_ban(phieu_can_sua):

    phieu_nhap = deepcopy(
        phieu_can_sua
    )

    phieu_nhap["_da_load"] = True
    phieu_nhap["_da_thay_doi"] = False

    return phieu_nhap


def sua_header_phieu_ban(
    phieu_ban,
    thoi_gian_tao=None,
    ma_khach_hang=_KHONG_THAY_DOI,
    ten_khach_hang=None,
    ghi_chu=None
):

    if thoi_gian_tao is not None:

        phieu_ban["thoi_gian_tao"] = (
            thoi_gian_tao
        )

    if ma_khach_hang is not _KHONG_THAY_DOI:

        if (
            isinstance(ma_khach_hang, str)
            and not ma_khach_hang.strip()
        ):

            ma_khach_hang = None

        phieu_ban["ma_khach_hang"] = (
            ma_khach_hang
        )

        if ma_khach_hang is not None:

            khach_hang = tim_khach_hang(
                ma_khach_hang
            )

            if khach_hang is None:

                raise ValueError(
                    f"Không tìm thấy khách hàng "
                    f"'{ma_khach_hang}'."
                )

            phieu_ban["ten_khach_hang"] = (
                khach_hang["ten_doi_tuong"]
            )

        else:

            phieu_ban["ten_khach_hang"] = None

    elif ten_khach_hang is not None:

        phieu_ban["ten_khach_hang"] = (
            ten_khach_hang
        )

    if ghi_chu is not None:

        phieu_ban["ghi_chu"] = ghi_chu

    if (
        thoi_gian_tao is not None
        or ma_khach_hang is not _KHONG_THAY_DOI
        or ten_khach_hang is not None
        or ghi_chu is not None
    ):

        danh_dau_phieu_da_thay_doi(
            phieu_ban
        )

    return phieu_ban


def them_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_ban,
    chi_tiet_moi
):

    san_pham = tim_san_pham(
        danh_sach_san_pham,
        chi_tiet_moi["ma_san_pham"]
    )

    if san_pham is None:

        raise ValueError(
            f"Không tìm thấy sản phẩm "
            f"'{chi_tiet_moi['ma_san_pham']}'"
        )

    if "ghi_chu" not in chi_tiet_moi:
        chi_tiet_moi["ghi_chu"] = ""

    tinh_lai_chi_tiet_ban(
        san_pham,
        chi_tiet_moi
    )

    chi_tiet_moi["stt"] = (
        len(phieu_ban["chi_tiet"]) + 1
    )

    phieu_ban["chi_tiet"].append(
        chi_tiet_moi
    )

    cap_nhat_tong_thanh_tien(
        phieu_ban
    )

    danh_dau_phieu_da_thay_doi(
        phieu_ban
    )

    return phieu_ban


def sua_dong_chi_tiet_phieu_ban(
    danh_sach_san_pham,
    phieu_ban,
    vi_tri,
    thay_doi
):

    chi_tiet = (
        phieu_ban["chi_tiet"][vi_tri]
    )

    chi_tiet.update(
        thay_doi
    )

    if (
        "ma_san_pham" in thay_doi
        or "ma_kho" in thay_doi
        or "dvt_ban" in thay_doi
        or "so_luong" in thay_doi
    ):

        chi_tiet["don_gia_von"] = 0
        chi_tiet["thanh_tien_von"] = 0

    san_pham = tim_san_pham(
        danh_sach_san_pham,
        chi_tiet["ma_san_pham"]
    )

    if san_pham is None:

        raise ValueError(
            f"Không tìm thấy sản phẩm "
            f"'{chi_tiet['ma_san_pham']}'"
        )

    tinh_lai_chi_tiet_ban(
        san_pham,
        chi_tiet
    )

    cap_nhat_tinh_toan_phieu_ban(
        danh_sach_san_pham,
        phieu_ban
    )

    danh_dau_phieu_da_thay_doi(
        phieu_ban
    )

    return phieu_ban


def xoa_chi_tiet_phieu_ban(
    phieu_ban,
    vi_tri
):

    del phieu_ban["chi_tiet"][vi_tri]

    for stt, chi_tiet in enumerate(
        phieu_ban["chi_tiet"],
        start=1
    ):

        chi_tiet["stt"] = stt

    cap_nhat_tong_thanh_tien(
        phieu_ban
    )

    danh_dau_phieu_da_thay_doi(
        phieu_ban
    )

    return phieu_ban


# ============================================================
# 13. XÁC NHẬN LƯU PHIẾU ĐÃ SỬA
# ============================================================

def xac_nhan_luu_phieu_ban(
    danh_sach_san_pham,
    danh_sach_ton_kho,
    phieu_ban,
    ham_tinh_gia_von=None
):

    if not kiem_tra_du_lieu_phieu_ban(
        phieu_ban
    ):

        return None

    phieu_cu = tim_phieu_ban(
        phieu_ban["ma_phieu"]
    )

    if phieu_cu is None:

        print(
            "Không tìm thấy phiếu bán "
            "cần sửa"
        )

        return None

    cap_nhat_tinh_toan_phieu_ban(
        danh_sach_san_pham,
        phieu_ban
    )

    # Hoàn tác dữ liệu cũ trước khi áp dụng dữ liệu mới.
    hoan_tac_phieu_ban_vao_kho(
        danh_sach_ton_kho,
        phieu_cu
    )

    hoan_tac_cong_no_tu_gntt(
        phieu_cu
    )

    if phieu_cu["ma_khach_hang"] is not None:

        cap_nhat_tong_giao_dich(
            phieu_cu["ma_khach_hang"],
            -phieu_cu["tong_thanh_tien"]
        )

    try:

        kiem_tra_ton_kho_phieu_ban(
            danh_sach_ton_kho,
            phieu_ban
        )

        if ham_tinh_gia_von is not None:

            ham_tinh_gia_von(
                phieu_ban,
                danh_sach_ton_kho
            )

            cap_nhat_tong_thanh_tien(
                phieu_ban
            )

        ap_dung_phieu_ban_vao_kho(
            danh_sach_ton_kho,
            phieu_ban
        )

        phat_sinh_cong_no_tu_gntt(
            phieu_ban
        )

        if phieu_ban["ma_khach_hang"] is not None:

            cap_nhat_tong_giao_dich(
                phieu_ban["ma_khach_hang"],
                phieu_ban["tong_thanh_tien"]
            )

    except Exception:

        # Khôi phục phiếu cũ.
        ap_dung_phieu_ban_vao_kho(
            danh_sach_ton_kho,
            phieu_cu,
            dung_gia_von_da_luu=True
        )

        phat_sinh_cong_no_tu_gntt(
            phieu_cu
        )

        if phieu_cu["ma_khach_hang"] is not None:

            cap_nhat_tong_giao_dich(
                phieu_cu["ma_khach_hang"],
                phieu_cu["tong_thanh_tien"]
            )

        if phieu_ban["ma_khach_hang"] is not None:

            cap_nhat_tong_giao_dich(
                phieu_ban["ma_khach_hang"],
                -phieu_ban["tong_thanh_tien"]
            )

        raise

    for vi_tri, phieu in enumerate(
        danh_sach_phieu_ban
    ):

        if phieu["ma_phieu"] == (
            phieu_ban["ma_phieu"]
        ):

            danh_sach_phieu_ban[vi_tri] = (
                tao_ban_luu_phieu(phieu_ban)
            )

            dat_lai_trang_thai_phieu(
                phieu_ban
            )

            print(
                "Sửa phiếu bán thành công"
            )

            return phieu_ban

    return None


# ============================================================
# 14. HÀM TƯƠNG THÍCH CHO GNTT
# ============================================================

def tim_phieu_gntt(ma_phieu):

    return tim_phieu_ban(
        ma_phieu
    )


def tao_phieu_gntt(ma_phieu=None):

    return tao_phieu_ban(
        ma_phieu
    )


def load_phieu_gntt(ma_phieu):

    return load_phieu_ban(
        ma_phieu
    )


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
