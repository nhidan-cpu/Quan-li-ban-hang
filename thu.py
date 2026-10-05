from copy import deepcopy
from datetime import datetime

from cong_no import (
    tinh_cong_no,
    tao_phat_sinh_cong_no,
    hoan_tac_phat_sinh_cong_no
)

from nha_cung_cap import tim_nha_cung_cap
from khach_hang import tim_khach_hang


# ============================================================
# 1. DỮ LIỆU
# ============================================================

danh_sach_phieu_thu = []

mau_phieu_thu = {
    "ma_phieu_thu": "",
    "ngay_phieu_thu": None,
    "loai_doi_tuong": "",
    "ma_doi_tuong": None,
    "ten_doi_tuong": None,
    "li_do_thu": "",
    "phuong_thuc_thu": "",
    "so_tien": 0,
    "nhan_vien_thu_tien": None,
    "nguoi_nop_tien": None
}


# ============================================================
# 2. SINH MÃ PHIẾU THU
# ============================================================

def sinh_ma_phieu_thu():
    so_lon_nhat = 0

    for phieu_thu in danh_sach_phieu_thu:
        ma_phieu = phieu_thu["ma_phieu_thu"]

        if not ma_phieu.startswith("PT"):
            continue

        try:
            so = int(ma_phieu[2:])
        except ValueError:
            continue

        so_lon_nhat = max(so_lon_nhat, so)

    return f"PT{so_lon_nhat + 1:05d}"


# ============================================================
# 3. TÌM PHIẾU THU
# ============================================================

def tim_phieu_thu(ma_phieu_thu):
    for phieu_thu in danh_sach_phieu_thu:
        if phieu_thu["ma_phieu_thu"] == ma_phieu_thu:
            return phieu_thu

    return None


# ============================================================
# 4. LẤY TÊN ĐỐI TƯỢNG
# ============================================================

def lay_ten_doi_tuong_thu(loai_doi_tuong, ma_doi_tuong):
    if loai_doi_tuong == "KH":
        khach_hang = tim_khach_hang(ma_doi_tuong)

        if khach_hang is None:
            raise ValueError("Không tìm thấy khách hàng.")

        return khach_hang["ten_khach_hang"]

    raise ValueError("Phiếu thu chỉ dành cho khách hàng.")


# ============================================================
# 5. TẠO PHIẾU THU
# ============================================================

def tao_phieu_thu(
    loai_doi_tuong,
    ma_doi_tuong,
    li_do_thu,
    phuong_thuc_thu,
    so_tien,
    nhan_vien_thu_tien=None,
    nguoi_nop_tien=None
):
    if loai_doi_tuong != "KH":
        raise ValueError("Phiếu thu chỉ dành cho khách hàng.")

    ten_doi_tuong = lay_ten_doi_tuong_thu(
        loai_doi_tuong,
        ma_doi_tuong
    )

    phieu_thu = deepcopy(mau_phieu_thu)

    phieu_thu["ma_phieu_thu"] = sinh_ma_phieu_thu()
    phieu_thu["ngay_phieu_thu"] = datetime.now()
    phieu_thu["loai_doi_tuong"] = loai_doi_tuong
    phieu_thu["ma_doi_tuong"] = ma_doi_tuong
    phieu_thu["ten_doi_tuong"] = ten_doi_tuong
    phieu_thu["li_do_thu"] = li_do_thu
    phieu_thu["phuong_thuc_thu"] = phuong_thuc_thu
    phieu_thu["so_tien"] = so_tien
    phieu_thu["nhan_vien_thu_tien"] = nhan_vien_thu_tien
    phieu_thu["nguoi_nop_tien"] = nguoi_nop_tien

    return phieu_thu


# ============================================================
# 6. KIỂM TRA PHIẾU THU
# ============================================================

def kiem_tra_phieu_thu(phieu_thu):
    if not isinstance(phieu_thu, dict):
        raise ValueError("Phiếu thu phải là dictionary.")

    if not phieu_thu.get("ma_phieu_thu"):
        raise ValueError("Mã phiếu thu không được để trống.")

    if phieu_thu.get("loai_doi_tuong") != "KH":
        raise ValueError("Phiếu thu chỉ dành cho khách hàng.")

    if phieu_thu.get("phuong_thuc_thu") not in (
        "TIEN_MAT",
        "CHUYEN_KHOAN"
    ):
        raise ValueError(
            "Phương thức thu phải là TIEN_MAT hoặc CHUYEN_KHOAN."
        )

    so_tien = phieu_thu.get("so_tien")

    if not isinstance(so_tien, (int, float)) or so_tien <= 0:
        raise ValueError("Số tiền thu phải lớn hơn 0.")

    if not phieu_thu.get("ma_doi_tuong"):
        raise ValueError("Mã đối tượng không được để trống.")

    return True


# ============================================================
# 7. PHÁT SINH GIẢM CÔNG NỢ TỪ PHIẾU THU
# ============================================================

def phat_sinh_cong_no_tu_phieu_thu(phieu_thu):
    ma_doi_tuong = phieu_thu.get("ma_doi_tuong")

    if not ma_doi_tuong:
        return None

    cong_no_hien_tai = tinh_cong_no(
        phieu_thu["loai_doi_tuong"],
        ma_doi_tuong
    )

    if phieu_thu["so_tien"] > cong_no_hien_tai:
        raise ValueError(
            "Số tiền thu lớn hơn công nợ hiện tại."
        )

    return tao_phat_sinh_cong_no(
        loai_doi_tuong=phieu_thu["loai_doi_tuong"],
        ma_doi_tuong=ma_doi_tuong,
        loai_phat_sinh="PHIEU_THU",
        ma_chung_tu=phieu_thu["ma_phieu_thu"],
        ngay_phat_sinh=phieu_thu["ngay_phieu_thu"],
        so_tien=-phieu_thu["so_tien"]
    )


# ============================================================
# 8. HOÀN TÁC CÔNG NỢ TỪ PHIẾU THU
# ============================================================

def hoan_tac_cong_no_tu_phieu_thu(phieu_thu):
    return hoan_tac_phat_sinh_cong_no(
        loai_doi_tuong=phieu_thu["loai_doi_tuong"],
        ma_doi_tuong=phieu_thu["ma_doi_tuong"],
        loai_phat_sinh="PHIEU_THU",
        ma_chung_tu=phieu_thu["ma_phieu_thu"]
    )


# ============================================================
# 9. LƯU PHIẾU THU
# ============================================================

def luu_phieu_thu(phieu_thu):
    kiem_tra_phieu_thu(phieu_thu)

    if tim_phieu_thu(phieu_thu["ma_phieu_thu"]) is not None:
        raise ValueError("Phiếu thu đã tồn tại.")

    phat_sinh_cong_no_tu_phieu_thu(phieu_thu)

    danh_sach_phieu_thu.append(deepcopy(phieu_thu))

    return phieu_thu


# ============================================================
# 10. HỦY PHIẾU THU
# ============================================================

def huy_phieu_thu(ma_phieu_thu):
    phieu_thu = tim_phieu_thu(ma_phieu_thu)

    if phieu_thu is None:
        raise ValueError("Không tìm thấy phiếu thu.")

    hoan_tac_cong_no_tu_phieu_thu(phieu_thu)

    danh_sach_phieu_thu.remove(phieu_thu)

    return phieu_thu