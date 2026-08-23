from copy import deepcopy

#============================================================
# CẤU TRÚC DỮ LIỆU CHUẨN CỦA SẢN PHẨM
#============================================================
san_pham = {
    "ma_vach_san_pham": [],
    "ma_tim_nhanh":"",
    "ma_vat":"",
    "ten_san_pham":"",
    "danh_muc":"",
    "dvt_chinh":"",
    "gia_nhap":0,
    "gia_ban":0,
    "dvt_quy_doi": [
        {
            "ma_dvt_quy_doi": "",
            "ten_dvt_quy_doi":"",
            "so_luong_quy_doi":0,
            "gia_ban_dvt_quy_doi":0,
        }
    ]
}

#============================================================
# TẠO SẢN PHẨM
#============================================================
def tao_san_pham(ma_vach_san_pham, ma_tim_nhanh, ma_vat, ten_san_pham, danh_muc, dvt_chinh, gia_nhap, gia_ban, dvt_quy_doi):
    return {
        "ma_vach_san_pham": ma_vach_san_pham,
        "ma_tim_nhanh": ma_tim_nhanh,
        "ma_vat": ma_vat,
        "ten_san_pham": ten_san_pham,
        "danh_muc": danh_muc,
        "dvt_chinh": dvt_chinh,
        "gia_nhap": gia_nhap,
        "gia_ban": gia_ban,
        "dvt_quy_doi": dvt_quy_doi
    }

#============================================================
# LẤY THÔNG TIN SẢN PHẨM
#============================================================
def lay_ma_vach_san_pham(san_pham):
    return san_pham["ma_vach_san_pham"]

#============================================================
# ĐƠN VỊ QUY ĐỔI
#============================================================
def tao_dvt_quy_doi(ma_dvt_quy_doi, ten_dvt_quy_doi, so_luong_quy_doi, gia_ban_dvt_quy_doi):
    return {
        "ma_dvt_quy_doi": ma_dvt_quy_doi,
        "ten_dvt_quy_doi": ten_dvt_quy_doi,
        "so_luong_quy_doi": so_luong_quy_doi,
        "gia_ban_dvt_quy_doi": gia_ban_dvt_quy_doi
    }
# Tạo 2 thông tin đvt_quy_đổi mẫu
dvt_loc = tao_dvt_quy_doi(
    ma_dvt_quy_doi="SP001-loc",
    ten_dvt_quy_doi="Lốc",
    so_luong_quy_doi=6,
    gia_ban_dvt_quy_doi=55000
)
dvt_thung = tao_dvt_quy_doi(
    ma_dvt_quy_doi="SP001-thung",
    ten_dvt_quy_doi="Thùng",
    so_luong_quy_doi=12,
    gia_ban_dvt_quy_doi=100000
)
# Tạo 1 sản phẩm hoàn chỉnh mô phỏng
san_pham_1 = tao_san_pham(
    ["SP001", "HH001"],
    "sp1",
    "VAT001",
    "Sản phẩm 1",
    "SẢN PHẨM TEST",
    "cái",
    8000,
    10000,
    [dvt_loc, dvt_thung]
)

#============================================================
# KIỂM TRA MÃ SẢN PHẨM
#============================================================
def lay_tat_ca_ma(san_pham):

    tat_ca_ma = []

    # Mã vạch sản phẩm
    tat_ca_ma.extend(san_pham["ma_vach_san_pham"])

    # Mã tìm nhanh
    if san_pham["ma_tim_nhanh"]:
        tat_ca_ma.append(san_pham["ma_tim_nhanh"])

    # Mã đvt quy đổi
    for dvt in san_pham["dvt_quy_doi"]:
        ma_dvt = dvt["ma_dvt_quy_doi"]

        # DVT có thể không có mã
        if ma_dvt:
            tat_ca_ma.append(ma_dvt)

    return tat_ca_ma

# Kiểm tra trùng mã của 2 sản phẩm
def kiem_tra_trung_ma(san_pham_cu, san_pham_moi):

    # Gom toàn bộ mã của 2 sản phẩm trước
    ma_cua_sp_cu = lay_tat_ca_ma(san_pham_cu)
    ma_cua_sp_moi = lay_tat_ca_ma(san_pham_moi)

    # Kiểm tra toàn bộ mã
    for ma in ma_cua_sp_moi:
        if ma in ma_cua_sp_cu:
            print(f"Lỗi: Mã '{ma}' đã tồn tại") 
            return False

    return True

#============================================================
# THÊM SẢN PHẨM
#============================================================
def chuan_bi_them(danh_sach_san_pham, san_pham_moi):
    
    for san_pham_cu in danh_sach_san_pham:
        if not kiem_tra_trung_ma(san_pham_cu, san_pham_moi):
            return None

    return san_pham_moi

def luu_them_moi(danh_sach_san_pham, san_pham_moi):
    danh_sach_san_pham.append(san_pham_moi)
    print("Thêm sản phẩm thành công")

danh_sach_san_pham = []

san_pham_hop_le = chuan_bi_them(danh_sach_san_pham,san_pham_1)
if san_pham_hop_le is not None:
    luu_them_moi(danh_sach_san_pham,san_pham_hop_le)

#============================================================
# TÌM SẢN PHẨM
#============================================================
def tim_san_pham(danh_sach_san_pham, ma_can_tim):

    for san_pham in danh_sach_san_pham:

        # Tìm sản phẩm theo mã tìm nhanh
        if ma_can_tim == san_pham["ma_tim_nhanh"]:
            return san_pham

        # Tìm sản phẩm theo mã vạch sản phẩm
        if ma_can_tim in san_pham["ma_vach_san_pham"]:
            return san_pham

        # Tìm sản phẩm theo mã DVT quy đổi
        for dvt in san_pham["dvt_quy_doi"]:
            if ma_can_tim == dvt["ma_dvt_quy_doi"]:
                return san_pham

    return None

#============================================================
# SỬA SẢN PHẨM
#============================================================
# 1. Chuẩn bị nháp
def chuan_bi_sua(danh_sach_san_pham, san_pham_can_sua, thay_doi):

    # Tạo bản nháp độc lập hoàn toàn
    san_pham_nhap = deepcopy(san_pham_can_sua)

    # Áp dụng các thay đổi vào bản nháp
    san_pham_nhap.update(thay_doi)

    # Kiểm tra mã với tất cả sản phẩm khác
    for san_pham in danh_sach_san_pham:

        # Bỏ qua chính sản phẩm đang sửa
        if san_pham is san_pham_can_sua:
            continue

        # Có mã bị trùng → không cho lưu
        if not kiem_tra_trung_ma(
            san_pham,
            san_pham_nhap
        ):
            return None

    # Trả về sản phẩm thật + bản nháp
    return san_pham_can_sua, san_pham_nhap


# 2. Lưu
def luu_san_pham(san_pham_can_sua, san_pham_nhap):
    san_pham_can_sua.update(san_pham_nhap)
    print("Sửa sản phẩm thành công")

#============================================================
# THÊM ĐƠN VỊ TÍNH QUY ĐỔI
#============================================================
# 1. Chuẩn bị nháp
def chuan_bi_them_dvt(danh_sach_san_pham, san_pham, dvt_moi):

    # Tạo bản nháp dvt độc lập
    dvt_nhap = deepcopy(dvt_moi)

    # Kiểm tra dvt mới với các sản phẩm khác
    ma_dvt_moi = dvt_nhap["ma_dvt_quy_doi"]

    # Đvt không có mã thì không cần kiểm tra mã
    if ma_dvt_moi:

        for san_pham_cu in danh_sach_san_pham:

            # Bỏ qua chính sản phẩm đang thêm đvt
            if san_pham_cu is san_pham:
                continue

            # Lấy toàn bộ mã của sản phẩm khác
            tat_ca_ma = lay_tat_ca_ma(san_pham_cu)

            if ma_dvt_moi in tat_ca_ma:
                print(
                    f"Lỗi: Mã DVT quy đổi "
                    f"'{ma_dvt_moi}' đã tồn tại"
                )
                return None
    return dvt_nhap

#2. Lưu
def luu_them_dvt(san_pham, dvt_moi):
    san_pham["dvt_quy_doi"].append(dvt_moi)
    print("Thêm đơn vị tính quy đổi thành công")

#============================================================
# SỬA ĐƠN VỊ TÍNH QUY ĐỔI
#============================================================
# 1. Chuẩn bị nháp
def chuan_bi_sua_dvt(dvt_can_sua, thay_doi):
    dvt_nhap = deepcopy(dvt_can_sua)
    dvt_nhap.update(thay_doi)

    return dvt_can_sua, dvt_nhap


# Kiểm tra DVT quy đổi trước khi sửa
def kiem_tra_sua_dvt(danh_sach_san_pham,san_pham_chua_dvt,dvt_nhap):

    # Lấy mã DVT sau khi sửa
    ma_dvt_moi = dvt_nhap["ma_dvt_quy_doi"]

    # DVT không có mã
    if not ma_dvt_moi:
        return True

    # Kiểm tra với các sản phẩm khác
    for san_pham in danh_sach_san_pham:

        # Bỏ qua sản phẩm đang chứa DVT được sửa
        if san_pham is san_pham_chua_dvt:
            continue

        # Gom tất cả mã thuộc sản phẩm khác
        tat_ca_ma = lay_tat_ca_ma(san_pham)

        # Kiểm tra mã DVT mới
        if ma_dvt_moi in tat_ca_ma:
            print(
                f"Lỗi: Mã ĐVT quy đổi "
                f"'{ma_dvt_moi}' đã tồn tại"
            )
            return False
    return True

# 2. Lưu
def luu_dvt_quy_doi(dvt_can_sua, dvt_nhap):

    dvt_can_sua.update(dvt_nhap)

    print("Sửa DVT quy đổi thành công")

#============================================================
# XÓA ĐVT QUY ĐỔI
#============================================================
def xoa_dvt_quy_doi(san_pham, dvt_duoc_chon):
    san_pham["dvt_quy_doi"].remove(dvt_duoc_chon)
    print("Xóa đơn vị tính quy đổi thành công")

#============================================================
# XEM SẢN PHẨM
#============================================================
# 1. Xem danh sách sản phẩm
def xem_danh_sach_san_pham(danh_sach_san_pham):
    for san_pham in danh_sach_san_pham:
        print(
            f"{san_pham['ma_tim_nhanh']} | "
            f"{san_pham['ten_san_pham']} | "
            f"{san_pham['gia_ban']} | "
            f"{san_pham['dvt_chinh']}"
        )

# 2. Xem chi tiết 1 sản phẩm
def xem_chi_tiet_san_pham(san_pham):

    print(san_pham)
    return san_pham

#============================================================
# XÓA SẢN PHẨM
#============================================================
def xoa_san_pham(danh_sach_san_pham, san_pham_duoc_chon):
    danh_sach_san_pham.remove(san_pham_duoc_chon)

#============================================================
# KHỐI TEST
#============================================================

if __name__ == "__main__":

    danh_sach_san_pham = []

    # TEST 1
    # Tạo DVT quy đổi
    # KỲ VỌNG: Tạo thành công
    dvt_test_1 = tao_dvt_quy_doi(
        ma_dvt_quy_doi="SP001-LOC",
        ten_dvt_quy_doi="Lốc",
        so_luong_quy_doi=6,
        gia_ban_dvt_quy_doi=55000
    )
    print("\nTEST 1 - TẠO DVT")
    print(dvt_test_1)

    #-------------------------------------------------------------
    # TEST 2
    # Tạo sản phẩm
    # KỲ VỌNG: Tạo thành công
    san_pham_test_1 = tao_san_pham(
        ma_vach_san_pham=["A001", "A002"],
        ma_tim_nhanh="SP001",
        ma_vat="VAT001",
        ten_san_pham="Sản phẩm 1",
        danh_muc="TEST",
        dvt_chinh="cái",
        gia_nhap=8000,
        gia_ban=10000,
        dvt_quy_doi=[
            dvt_test_1
        ]
    )
    print("\nTEST 2 - TẠO SẢN PHẨM")
    print(san_pham_test_1)

    #-------------------------------------------------------------
    # TEST 3
    # Lấy mã vạch sản phẩm
    # KỲ VỌNG: ['A001', 'A002']
    print("\nTEST 3 - LẤY MÃ VẠCH")
    print(lay_ma_vach_san_pham(san_pham_test_1))

    #-------------------------------------------------------------
    # TEST 4
    # Lấy tất cả mã của sản phẩm
    # KỲ VỌNG:
    # ['A001', 'A002', 'SP001-LOC']
    print("\nTEST 4 - LẤY TẤT CẢ MÃ")
    print(lay_tat_ca_ma(san_pham_test_1))

    #-------------------------------------------------------------
    # TEST 5
    # Thêm sản phẩm đầu tiên
    # KỲ VỌNG: Thành công
    san_pham_hop_le = chuan_bi_them(
        danh_sach_san_pham,
        san_pham_test_1
    )
    if san_pham_hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            san_pham_hop_le
        )

    #-------------------------------------------------------------
    # TEST 6
    # Tìm bằng mã tìm nhanh
    # KỲ VỌNG: Tìm thấy Sản phẩm 1
    ket_qua = tim_san_pham(
        danh_sach_san_pham,
        "SP001"
    )
    print("\nTEST 6 - TÌM BẰNG MÃ TÌM NHANH")
    print(ket_qua["ten_san_pham"] if ket_qua else None)

    #-------------------------------------------------------------
    # TEST 7
    # Tìm bằng mã vạch sản phẩm
    # KỲ VỌNG: Tìm thấy Sản phẩm 1
    ket_qua = tim_san_pham(
        danh_sach_san_pham,
        "A002"
    )
    print("\nTEST 7 - TÌM BẰNG MÃ VẠCH")
    print(ket_qua["ten_san_pham"] if ket_qua else None)

    #-------------------------------------------------------------
    # TEST 8
    # Tìm bằng mã DVT quy đổi
    # KỲ VỌNG: Tìm thấy Sản phẩm 1
    ket_qua = tim_san_pham(
        danh_sach_san_pham,
        "SP001-LOC"
    )
    print("\nTEST 8 - TÌM BẰNG MÃ DVT")
    print(ket_qua["ten_san_pham"] if ket_qua else None)

    #-------------------------------------------------------------
    # TEST 9
    # Tìm mã không tồn tại
    # KỲ VỌNG: None
    ket_qua = tim_san_pham(
        danh_sach_san_pham,
        "KHONG-TON-TAI"
    )
    print("\nTEST 9 - TÌM MÃ KHÔNG TỒN TẠI")
    print(ket_qua)

    #-------------------------------------------------------------
    # TEST 10
    # Thêm SP2 trùng mã tìm nhanh
    # KỲ VỌNG: BỊ CHẶN
    sp2 = tao_san_pham(
        ma_vach_san_pham=["B001"],
        ma_tim_nhanh="SP001",
        ma_vat="VAT002",
        ten_san_pham="Sản phẩm 2",
        danh_muc="TEST",
        dvt_chinh="cái",
        gia_nhap=9000,
        gia_ban=11000,
        dvt_quy_doi=[]
    )
    san_pham_hop_le = chuan_bi_them(
        danh_sach_san_pham,
        sp2
    )
    if san_pham_hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            san_pham_hop_le
        )   

    #-------------------------------------------------------------
    # TEST 11
    # Thêm SP2 trùng mã vạch sản phẩm
    # KỲ VỌNG: BỊ CHẶN
    sp2 = tao_san_pham(
        ma_vach_san_pham=["A002"],
        ma_tim_nhanh="SP002",
        ma_vat="VAT002",
        ten_san_pham="Sản phẩm 2",
        danh_muc="TEST",
        dvt_chinh="cái",
        gia_nhap=9000,
        gia_ban=11000,
        dvt_quy_doi=[]
    )
    san_pham_hop_le = chuan_bi_them(
        danh_sach_san_pham,
        sp2
    )
    if san_pham_hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            san_pham_hop_le
        )

    #-------------------------------------------------------------
    # TEST 12
    # Thêm SP2 có mã DVT trùng với mã vạch của SP1
    # KỲ VỌNG: BỊ CHẶN
    #
    # Đây là test quan trọng:
    # mã vạch + mã DVT nằm chung một nhóm mã để check.
    dvt_trung = tao_dvt_quy_doi(
        ma_dvt_quy_doi="A001",
        ten_dvt_quy_doi="Thùng",
        so_luong_quy_doi=12,
        gia_ban_dvt_quy_doi=100000
    )
    sp2 = tao_san_pham(
        ma_vach_san_pham=["B001"],
        ma_tim_nhanh="SP002",
        ma_vat="VAT002",
        ten_san_pham="Sản phẩm 2",
        danh_muc="TEST",
        dvt_chinh="cái",
        gia_nhap=9000,
        gia_ban=11000,
        dvt_quy_doi=[
            dvt_trung
        ]
    )
    san_pham_hop_le = chuan_bi_them(
        danh_sach_san_pham,
        sp2
    )
    if san_pham_hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            san_pham_hop_le
        )

    #-------------------------------------------------------------
    # TEST 13
    # Thêm SP2 hoàn toàn hợp lệ
    # KỲ VỌNG: Thành công
    dvt_sp2 = tao_dvt_quy_doi(
        ma_dvt_quy_doi="SP002-LOC",
        ten_dvt_quy_doi="Lốc",
        so_luong_quy_doi=6,
        gia_ban_dvt_quy_doi=60000
    )
    sp2 = tao_san_pham(
        ma_vach_san_pham=["B001"],
        ma_tim_nhanh="SP002",
        ma_vat="VAT002",
        ten_san_pham="Sản phẩm 2",
        danh_muc="TEST",
        dvt_chinh="cái",
        gia_nhap=9000,
        gia_ban=11000,
        dvt_quy_doi=[
            dvt_sp2
        ]
    )
    san_pham_hop_le = chuan_bi_them(
        danh_sach_san_pham,
        sp2
    )
    if san_pham_hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            san_pham_hop_le
        )

    #-------------------------------------------------------------
    # TEST 14
    # Sửa giá bán SP1
    # KỲ VỌNG: Thành công
    ket_qua = chuan_bi_sua(
        danh_sach_san_pham,
        "SP001",
        {
            "gia_ban": 12000
        }
    )
    if ket_qua is not None:

        san_pham_can_sua, san_pham_nhap = ket_qua

        luu_san_pham(
            san_pham_can_sua,
            san_pham_nhap
        )

    #-------------------------------------------------------------
    # TEST 15
    # Sửa SP1 thành mã tìm nhanh của SP2
    # KỲ VỌNG: BỊ CHẶN
    ket_qua = chuan_bi_sua(
        danh_sach_san_pham,
        "SP001",
        {
            "ma_tim_nhanh": "SP002"
        }
    )
    if ket_qua is not None:
        san_pham_can_sua, san_pham_nhap = ket_qua
        luu_san_pham(
            san_pham_can_sua,
            san_pham_nhap
        )

    #-------------------------------------------------------------
    # TEST 16
    # Sửa SP1 thành mã thuộc SP2
    # KỲ VỌNG: BỊ CHẶN
    ket_qua = chuan_bi_sua(
        danh_sach_san_pham,
        "SP001",
        {
            "ma_vach_san_pham": ["B001"]
        }
    )
    if ket_qua is not None:
        san_pham_can_sua, san_pham_nhap = ket_qua
        luu_san_pham(
            san_pham_can_sua,
            san_pham_nhap
        )

    #-------------------------------------------------------------
    # TEST 17
    # Sửa mã tìm nhanh của SP1 thành mã mới
    # KỲ VỌNG: Thành công
    ket_qua = chuan_bi_sua(
        danh_sach_san_pham,
        "SP001",
        {
            "ma_tim_nhanh": "SP001-MOI"
        }
    )
    if ket_qua is not None:
        san_pham_can_sua, san_pham_nhap = ket_qua
        luu_san_pham(
            san_pham_can_sua,
            san_pham_nhap
        )

    #-------------------------------------------------------------
    # TEST 18
    # Sửa DVT Lốc - chỉ sửa giá
    # KỲ VỌNG: Thành công
    ket_qua = chuan_bi_sua_dvt(
        dvt_test_1,
        {
            "gia_ban_dvt_quy_doi": 60000
        }
    )
    if ket_qua is not None:
        dvt_can_sua, dvt_nhap = ket_qua
        if kiem_tra_sua_dvt(
            danh_sach_san_pham,
            san_pham_test_1,
            dvt_nhap
        ):
            luu_dvt_quy_doi(
                dvt_can_sua,
                dvt_nhap
            )  

    #-------------------------------------------------------------
    # TEST 19
    # Sửa mã DVT thành mã của SP2
    # KỲ VỌNG: BỊ CHẶN
    ket_qua = chuan_bi_sua_dvt(
        dvt_test_1,
        {
            "ma_dvt_quy_doi": "SP002-LOC"
        }
    )
    if ket_qua is not None:
        dvt_can_sua, dvt_nhap = ket_qua
        if kiem_tra_sua_dvt(
            danh_sach_san_pham,
            san_pham_test_1,
            dvt_nhap
        ):
            luu_dvt_quy_doi(
                dvt_can_sua,
                dvt_nhap
            )

    #-------------------------------------------------------------
    # TEST 20
    # Sửa mã DVT thành mã đã tồn tại trong chính SP1
    # KỲ VỌNG: ĐƯỢC PHÉP
    #
    # Vì mã trong cùng một dictionary sản phẩm được phép trùng.
    ket_qua = chuan_bi_sua_dvt(
        dvt_test_1,
        {
            "ma_dvt_quy_doi": "A001"
        }
    )
    if ket_qua is not None:
        dvt_can_sua, dvt_nhap = ket_qua
        if kiem_tra_sua_dvt(
            danh_sach_san_pham,
            san_pham_test_1,
            dvt_nhap
        ):
            luu_dvt_quy_doi(
                dvt_can_sua,
                dvt_nhap
            )

    #-------------------------------------------------------------
    # TEST 21
    # Xem danh sách
    print("\n================ DANH SÁCH SP ================")
    xem_danh_sach_san_pham(
        danh_sach_san_pham
    )

    #-------------------------------------------------------------
    # TEST 22
    # Xem chi tiết SP1
    print("\n================ CHI TIẾT SP1 ================")
    xem_chi_tiet_san_pham(
        danh_sach_san_pham,
        "SP001-MOI"
    )

    #-------------------------------------------------------------
    # TEST 23
    # Xóa SP2
    # KỲ VỌNG: Xóa thành công
    san_pham_duoc_chon = tim_san_pham(
        danh_sach_san_pham,
        "SP002"
    )
    if san_pham_duoc_chon is not None:

        xoa_san_pham(
            danh_sach_san_pham,
            san_pham_duoc_chon
        )

    #-------------------------------------------------------------
    # TEST 24
    # Kiểm tra SP2 sau khi xóa
    # KỲ VỌNG: None
    ket_qua = tim_san_pham(
        danh_sach_san_pham,
        "SP002"
    )
    print("\nTEST 24 - TÌM SP2 SAU KHI XÓA")
    print(ket_qua)

    #-------------------------------------------------------------
    # TEST 25
    # Danh sách cuối cùng
    print("\n================ DANH SÁCH CUỐI ================")
    xem_danh_sach_san_pham(
        danh_sach_san_pham
    )

    #-------------------------------------------------------------
    # TEST 26
    # Sản phẩm có nhiều mã vạch
    # KỲ VỌNG: Gom đầy đủ tất cả mã
    danh_sach_san_pham = []

    dvt_test = tao_dvt_quy_doi(
        "SP100-LOC",
        "Lốc",
        6,
        60000
    )
    sp_test = tao_san_pham(
        ["A100", "A101", "A102"],
        "SP100",
        "VAT100",
        "Sản phẩm 100",
        "TEST",
        "cái",
        8000,
        10000,
        [dvt_test]
    )
    luu_them_moi(
        danh_sach_san_pham,
        sp_test
    )
    print("\nTEST 26 - NHIỀU MÃ VẠCH")
    print(lay_tat_ca_ma(sp_test))

    #-------------------------------------------------------------
    # TEST 27
    # Tìm bằng từng mã vạch
    # KỲ VỌNG: Cả 3 mã đều tìm được SP100
    for ma in ["A100", "A101", "A102"]:
        ket_qua = tim_san_pham(
        danh_sach_san_pham,
        ma
    )
    print(
        f"TEST 27 - {ma}:",
        ket_qua["ma_tim_nhanh"] if ket_qua else None
    )

    #-------------------------------------------------------------
    # TEST 28
    # DVT quy đổi không có mã
    # KỲ VỌNG: Không lỗi 
    dvt_khong_ma = tao_dvt_quy_doi(
        "",
        "Thùng",
        12,
        100000
    )
    sp_khong_ma = tao_san_pham(
        ["B100"],
        "SP101",
        "VAT101",
        "Sản phẩm không mã DVT",
        "TEST",
        "cái",
        8000,
        10000,
        [dvt_khong_ma]
    )
    print("\nTEST 28 - DVT KHÔNG CÓ MÃ")
    print(lay_tat_ca_ma(sp_khong_ma))

    #-------------------------------------------------------------
    # TEST 29
    # Thêm sản phẩm có DVT không mã
    # KỲ VỌNG: Thành công
    hop_le = chuan_bi_them(
    danh_sach_san_pham,
    sp_khong_ma
    )

    if hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            hop_le
        )

    #-------------------------------------------------------------
    # TEST 30
    # Một sản phẩm có nhiều DVT
    # KỲ VỌNG: Tất cả mã DVT đều được gom
    dvt_1 = tao_dvt_quy_doi(
        "SP102-LOC",
        "Lốc",
        6,
        60000
    )
    dvt_2 = tao_dvt_quy_doi(
        "SP102-THUNG",
        "Thùng",
        12,
        110000
    )
    dvt_3 = tao_dvt_quy_doi(
        "",
        "Bao",
        24,
        200000
    )
    sp_nhieu_dvt = tao_san_pham(
        ["C100", "C101"],
        "SP102",
        "VAT102",
        "Sản phẩm nhiều DVT",
        "TEST",
        "cái",
        8000,
        10000,
        [
            dvt_1,
            dvt_2,
            dvt_3
        ]
    )
    print("\nTEST 30 - NHIỀU DVT")
    print(lay_tat_ca_ma(sp_nhieu_dvt))

    #-------------------------------------------------------------
    # TEST 31
    # Thêm sản phẩm nhiều DVT
    # KỲ VỌNG: Thành công
    hop_le = chuan_bi_them(
        danh_sach_san_pham,
        sp_nhieu_dvt
    )

    if hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            hop_le
        )

    #-------------------------------------------------------------
    # TEST 32
    # Sửa 1 DVT
    # DVT khác không được ảnh hưởng 
    danh_sach_dvt_truoc = deepcopy(
    sp_nhieu_dvt["dvt_quy_doi"]
        )
    ket_qua = chuan_bi_sua_dvt(
        dvt_1,
        {
            "gia_ban_dvt_quy_doi": 65000
        }
    )
    if ket_qua is not None:
        dvt_can_sua, dvt_nhap = ket_qua
    if kiem_tra_sua_dvt(
        danh_sach_san_pham,
        sp_nhieu_dvt,
        dvt_nhap
    ):
        luu_dvt_quy_doi(
            dvt_can_sua,
            dvt_nhap
        )
    print("\nTEST 32 - SAU KHI SỬA DVT")
    print(sp_nhieu_dvt["dvt_quy_doi"])

    #-------------------------------------------------------------
    # TEST 33
    # Kiểm tra DVT 2 và DVT 3 không bị thay đổi
    # KỲ VỌNG:
    # DVT 2 vẫn 110000
    # DVT 3 vẫn 200000 
    print("\nTEST 33 - KIỂM TRA DVT KHÁC")
    print(
        "DVT 2:",
        sp_nhieu_dvt["dvt_quy_doi"][1]
    )
    print(
        "DVT 3:",
        sp_nhieu_dvt["dvt_quy_doi"][2]
    )     

    #-------------------------------------------------------------
    # TEST 34
    # Sửa DVT bằng mã trùng với mã vạch của SP khác
    # KỲ VỌNG: BỊ CHẶN
    ket_qua = chuan_bi_sua_dvt(
        dvt_1,
        {
            "ma_dvt_quy_doi": "B100"
        }
    )

    if ket_qua is not None:
        dvt_can_sua, dvt_nhap = ket_qua
    if kiem_tra_sua_dvt(
        danh_sach_san_pham,
        sp_nhieu_dvt,
        dvt_nhap
    ):
        luu_dvt_quy_doi(
            dvt_can_sua,
            dvt_nhap
        )

    #-------------------------------------------------------------
    # TEST 35
    # Sửa sản phẩm nhưng không thay đổi mã
    # KỲ VỌNG: Thành công
    ket_qua = chuan_bi_sua(
    danh_sach_san_pham,
    "SP100",
    {
        "ten_san_pham": "Sản phẩm 100 - đã sửa"
    }
    )
    if ket_qua is not None:
        san_pham_can_sua, san_pham_nhap = ket_qua
    luu_san_pham(
        san_pham_can_sua,
        san_pham_nhap
    )

    #-------------------------------------------------------------
    # TEST 36
    # Sửa sản phẩm nhưng thử đưa mã của chính nó vào cùng dictionary
    # KỲ VỌNG:
    # Theo quy tắc hiện tại → ĐƯỢC PHÉP
    ket_qua = chuan_bi_sua(
        danh_sach_san_pham,
        "SP100",
        {
            "ma_vach_san_pham": [
                "A100",
                "A101",
                "A102",
                "SP100-LOC"
            ]
        }
    )
    if ket_qua is not None:
        san_pham_can_sua, san_pham_nhap = ket_qua
    luu_san_pham(
        san_pham_can_sua,
        san_pham_nhap
    )

    #-------------------------------------------------------------
    # TEST 37
    # Xóa SP100
    sp_duoc_chon = tim_san_pham(
    danh_sach_san_pham,
    "SP100"
    )
    if sp_duoc_chon is not None:
        xoa_san_pham(
        danh_sach_san_pham,
        sp_duoc_chon
    )

    #-------------------------------------------------------------
    # TEST 38
    # Sau khi xóa SP100, các mã của SP100 phải được giải phóng
    # Thử tạo SP mới dùng lại A100
    # KỲ VỌNG: ĐƯỢC PHÉP        
    sp_moi = tao_san_pham(
        ["A100"],
        "SP100-MOI",
        "VAT200",
        "Sản phẩm mới dùng lại mã",
        "TEST",
        "cái",
        7000,
        9000,
        []
    )
    hop_le = chuan_bi_them(
        danh_sach_san_pham,
        sp_moi
    )
    if hop_le is not None:
        luu_them_moi(
            danh_sach_san_pham,
            hop_le
        )

    #-------------------------------------------------------------
    #  TEST 39
    # Thử xóa chính sản phẩm vừa chọn  
    sp_duoc_chon = tim_san_pham(
        danh_sach_san_pham,
        "SP100-MOI"
    )
    if sp_duoc_chon is not None:
        xoa_san_pham(
            danh_sach_san_pham,
            sp_duoc_chon
        )

    #-------------------------------------------------------------
    # TEST 40
    # Kiểm tra danh sách cuối 
    print("\n================ TEST 40 - DANH SÁCH CUỐI ================")
    xem_danh_sach_san_pham(
        danh_sach_san_pham
    )    



     





        




    