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

danh_sach_phieu_chi = []

mau_phieu_chi = {
    "ma_phieu_chi": "",
    "ngay_phieu_chi": None,
    "loai_doi_tuong": "",
    "ma_doi_tuong": None,
    "ten_doi_tuong": None,
    "li_do_chi": "",
    "phuong_thuc_chi": "",
    "so_tien": 0,
    "nhan_vien_chi_tien": None,
    "nguoi_nhan_tien": None
}


# ============================================================
# 2. SINH MÃ PHIẾU CHI
# ============================================================

def sinh_ma_phieu_chi():
    so_lon_nhat = 0

    for phieu_chi in danh_sach_phieu_chi:
        ma_phieu = phieu_chi["ma_phieu_chi"]

        if not ma_phieu.startswith("PC"):
            continue

        try:
            so = int(ma_phieu[2:])
        except ValueError:
            continue

        so_lon_nhat = max(so_lon_nhat, so)

    return f"PC{so_lon_nhat + 1:05d}"


# ============================================================
# 3. TÌM PHIẾU CHI
# ============================================================

def tim_phieu_chi(ma_phieu_chi):
    for phieu_chi in danh_sach_phieu_chi:
        if phieu_chi["ma_phieu_chi"] == ma_phieu_chi:
            return phieu_chi

    return None


# ============================================================
# 4. LẤY TÊN ĐỐI TƯỢNG
# ============================================================

def lay_ten_doi_tuong_chi(loai_doi_tuong, ma_doi_tuong):
    if loai_doi_tuong == "NCC":
        nha_cung_cap = tim_nha_cung_cap(ma_doi_tuong)

        if nha_cung_cap is None:
            raise ValueError("Không tìm thấy nhà cung cấp.")

        return nha_cung_cap["ten_nha_cung_cap"]

    raise ValueError("Phiếu chi chỉ dành cho nhà cung cấp.")


# ============================================================
# 5. TẠO PHIẾU CHI
# ============================================================

def tao_phieu_chi(
    loai_doi_tuong,
    ma_doi_tuong,
    li_do_chi,
    phuong_thuc_chi,
    so_tien,
    nhan_vien_chi_tien=None,
    nguoi_nhan_tien=None
):
    if loai_doi_tuong != "NCC":
        raise ValueError("Loại đối tượng phải là NCC hoặc KH.")

    ten_doi_tuong = lay_ten_doi_tuong_chi(
        loai_doi_tuong,
        ma_doi_tuong
    )

    phieu_chi = deepcopy(mau_phieu_chi)

    phieu_chi["ma_phieu_chi"] = sinh_ma_phieu_chi()
    phieu_chi["ngay_phieu_chi"] = datetime.now()
    phieu_chi["loai_doi_tuong"] = loai_doi_tuong
    phieu_chi["ma_doi_tuong"] = ma_doi_tuong
    phieu_chi["ten_doi_tuong"] = ten_doi_tuong
    phieu_chi["li_do_chi"] = li_do_chi
    phieu_chi["phuong_thuc_chi"] = phuong_thuc_chi
    phieu_chi["so_tien"] = so_tien
    phieu_chi["nhan_vien_chi_tien"] = nhan_vien_chi_tien
    phieu_chi["nguoi_nhan_tien"] = nguoi_nhan_tien

    return phieu_chi


# ============================================================
# 6. KIỂM TRA PHIẾU CHI
# ============================================================

def kiem_tra_phieu_chi(phieu_chi):
    if not isinstance(phieu_chi, dict):
        raise ValueError("Phiếu chi phải là dictionary.")

    if not phieu_chi.get("ma_phieu_chi"):
        raise ValueError("Mã phiếu chi không được để trống.")

    if phieu_chi.get("loai_doi_tuong") != "NCC":
        raise ValueError("Loại đối tượng phải là NCC hoặc KH.")

    if phieu_chi.get("phuong_thuc_chi") not in (
        "TIEN_MAT",
        "CHUYEN_KHOAN"
    ):
        raise ValueError(
            "Phương thức chi phải là TIEN_MAT hoặc CHUYEN_KHOAN."
        )

    so_tien = phieu_chi.get("so_tien")

    if not isinstance(so_tien, (int, float)) or so_tien <= 0:
        raise ValueError("Số tiền chi phải lớn hơn 0.")

    if not phieu_chi.get("ma_doi_tuong"):
        raise ValueError("Mã đối tượng không được để trống.")

    return True


# ============================================================
# 7. PHÁT SINH GIẢM CÔNG NỢ TỪ PHIẾU CHI
# ============================================================

def phat_sinh_cong_no_tu_phieu_chi(phieu_chi):
    ma_doi_tuong = phieu_chi.get("ma_doi_tuong")

    if not ma_doi_tuong:
        return None

    cong_no_hien_tai = tinh_cong_no(
        phieu_chi["loai_doi_tuong"],
        ma_doi_tuong
    )

    if phieu_chi["so_tien"] > cong_no_hien_tai:
        raise ValueError(
            "Số tiền chi lớn hơn công nợ hiện tại."
        )

    return tao_phat_sinh_cong_no(
        loai_doi_tuong=phieu_chi["loai_doi_tuong"],
        ma_doi_tuong=ma_doi_tuong,
        loai_phat_sinh="PHIEU_CHI",
        ma_chung_tu=phieu_chi["ma_phieu_chi"],
        ngay_phat_sinh=phieu_chi["ngay_phieu_chi"],
        so_tien=-phieu_chi["so_tien"]
    )


# ============================================================
# 8. HOÀN TÁC CÔNG NỢ TỪ PHIẾU CHI
# ============================================================

def hoan_tac_cong_no_tu_phieu_chi(phieu_chi):
    return hoan_tac_phat_sinh_cong_no(
        loai_doi_tuong=phieu_chi["loai_doi_tuong"],
        ma_doi_tuong=phieu_chi["ma_doi_tuong"],
        loai_phat_sinh="PHIEU_CHI",
        ma_chung_tu=phieu_chi["ma_phieu_chi"]
    )


# ============================================================
# 9. LƯU PHIẾU CHI
# ============================================================

def luu_phieu_chi(phieu_chi):
    kiem_tra_phieu_chi(phieu_chi)

    if tim_phieu_chi(phieu_chi["ma_phieu_chi"]) is not None:
        raise ValueError("Phiếu chi đã tồn tại.")

    phat_sinh_cong_no_tu_phieu_chi(phieu_chi)

    danh_sach_phieu_chi.append(deepcopy(phieu_chi))

    return phieu_chi


# ============================================================
# 10. HỦY PHIẾU CHI
# ============================================================

def huy_phieu_chi(ma_phieu_chi):
    phieu_chi = tim_phieu_chi(ma_phieu_chi)

    if phieu_chi is None:
        raise ValueError("Không tìm thấy phiếu chi.")

    hoan_tac_cong_no_tu_phieu_chi(phieu_chi)

    danh_sach_phieu_chi.remove(phieu_chi)

    return phieu_chi