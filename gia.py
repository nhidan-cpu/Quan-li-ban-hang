# Cấu trúc một dòng trong bảng giá niêm yết
gia_niem_yet = {
    "ma_san_pham": "",
    "ten_san_pham": "",
    "gia_von": 0,
    "gia_ban": 0,
}

# Danh sách sản phẩm trong bảng giá niêm yết
danh_sach_gia_niem_yet = []


# Tìm sản phẩm trong bảng giá niêm yết theo mã sản phẩm
def tim_gia_niem_yet(
    ma_san_pham
):
    for dong_gia in danh_sach_gia_niem_yet:
        if dong_gia["ma_san_pham"] == ma_san_pham:
            return dong_gia
    return None


# Tìm sản phẩm trong danh sách sản phẩm theo mã sản phẩm
def tim_san_pham(
    danh_sach_san_pham,
    ma_san_pham
):
    for san_pham in danh_sach_san_pham:
        if ma_san_pham in san_pham["ma_san_pham"]:
            return san_pham
    return None


# Tính giá vốn bình quân của một sản phẩm từ các phiếu nhập
def tinh_gia_von_binh_quan(
    danh_sach_phieu_nhap,
    ma_san_pham
):
    tong_so_luong = 0
    tong_gia_tri = 0

    for phieu_nhap in danh_sach_phieu_nhap:
        for chi_tiet in phieu_nhap["chi_tiet"]:
            if chi_tiet["ma_san_pham"] != ma_san_pham:
                continue

            tong_so_luong += chi_tiet["so_luong_quy_doi"]
            tong_gia_tri += chi_tiet["thanh_tien_tung_dong"]

    if tong_so_luong == 0:
        return 0

    return tong_gia_tri / tong_so_luong


# Cập nhật giá vốn của một sản phẩm trong bảng giá niêm yết
def cap_nhat_gia_von(
    danh_sach_phieu_nhap,
    ma_san_pham
):
    dong_gia = tim_gia_niem_yet(ma_san_pham)

    if dong_gia is None:
        raise ValueError(
            f"Không tìm thấy sản phẩm trong bảng giá niêm yết: "
            f"{ma_san_pham}"
        )

    gia_von_moi = tinh_gia_von_binh_quan(
        danh_sach_phieu_nhap,
        ma_san_pham
    )

    dong_gia["gia_von"] = gia_von_moi

    return dong_gia


# Cập nhật giá vốn của toàn bộ sản phẩm trong bảng giá niêm yết
def cap_nhat_toan_bo_gia_von(
    danh_sach_phieu_nhap
):
    for dong_gia in danh_sach_gia_niem_yet:
        cap_nhat_gia_von(
            danh_sach_phieu_nhap,
            dong_gia["ma_san_pham"]
        )


# Thêm một sản phẩm vào bảng giá niêm yết
def them_san_pham_vao_gia_niem_yet(
    san_pham,
    gia_von=0
):
    ma_san_pham = san_pham["ma_san_pham"][0]

    dong_gia = tim_gia_niem_yet(ma_san_pham)

    if dong_gia is not None:
        return dong_gia

    dong_gia_moi = {
        "ma_san_pham": ma_san_pham,
        "ten_san_pham": san_pham["ten_san_pham"],
        "gia_von": gia_von,
        "gia_ban": san_pham["gia_ban"],
    }

    danh_sach_gia_niem_yet.append(dong_gia_moi)

    return dong_gia_moi


# Đồng bộ thông tin sản phẩm vào bảng giá niêm yết
def dong_bo_san_pham_vao_gia_niem_yet(
    danh_sach_san_pham
):
    for san_pham in danh_sach_san_pham:
        ma_san_pham = san_pham["ma_san_pham"][0]

        dong_gia = tim_gia_niem_yet(ma_san_pham)

        if dong_gia is None:
            them_san_pham_vao_gia_niem_yet(
                san_pham
            )
            continue

        dong_gia["ten_san_pham"] = san_pham["ten_san_pham"]
        dong_gia["gia_ban"] = san_pham["gia_ban"]


# Xóa những sản phẩm không còn tồn tại trong danh sách sản phẩm
def dong_bo_xoa_san_pham(
    danh_sach_san_pham
):
    ma_san_pham_hien_tai = {
        san_pham["ma_san_pham"][0]
        for san_pham in danh_sach_san_pham
    }

    danh_sach_gia_niem_yet[:] = [
        dong_gia
        for dong_gia in danh_sach_gia_niem_yet
        if dong_gia["ma_san_pham"] in ma_san_pham_hien_tai
    ]


# Đồng bộ toàn bộ bảng giá niêm yết với danh sách sản phẩm
def dong_bo_toan_bo_gia_niem_yet(
    danh_sach_san_pham
):
    dong_bo_san_pham_vao_gia_niem_yet(
        danh_sach_san_pham
    )

    dong_bo_xoa_san_pham(
        danh_sach_san_pham
    )


# Sửa giá bán trực tiếp từ bảng giá niêm yết
def sua_gia_ban_niem_yet(
    danh_sach_san_pham,
    ma_san_pham,
    gia_ban_moi
):
    dong_gia = tim_gia_niem_yet(ma_san_pham)

    if dong_gia is None:
        raise ValueError(
            f"Không tìm thấy sản phẩm trong bảng giá niêm yết: "
            f"{ma_san_pham}"
        )

    if gia_ban_moi < 0:
        raise ValueError(
            "Giá bán không thể nhỏ hơn 0."
        )

    san_pham = tim_san_pham(
        danh_sach_san_pham,
        ma_san_pham
    )

    if san_pham is None:
        raise ValueError(
            f"Không tìm thấy sản phẩm: {ma_san_pham}"
        )

    dong_gia["gia_ban"] = gia_ban_moi
    san_pham["gia_ban"] = gia_ban_moi

    return dong_gia


# Đồng bộ giá bán từ danh sách sản phẩm sang bảng giá niêm yết
def dong_bo_gia_ban_tu_san_pham(
    danh_sach_san_pham
):
    for san_pham in danh_sach_san_pham:
        ma_san_pham = san_pham["ma_san_pham"][0]

        dong_gia = tim_gia_niem_yet(ma_san_pham)

        if dong_gia is None:
            continue

        dong_gia["gia_ban"] = san_pham["gia_ban"]


# Cấu trúc một bảng giá phân khúc
bang_gia_phan_khuc = {
    "ma_bang_gia": "",
    "ten_bang_gia": "",
    "cau_hinh_tinh_gia": {},
    "danh_sach_san_pham": [],
}

# Danh sách các bảng giá phân khúc
danh_sach_bang_gia_phan_khuc = []


# Tìm bảng giá phân khúc theo mã bảng giá
def tim_bang_gia_phan_khuc(ma_bang_gia):
    for bang_gia in danh_sach_bang_gia_phan_khuc:
        if bang_gia["ma_bang_gia"] == ma_bang_gia:
            return bang_gia

    return None


# Tìm sản phẩm trong một bảng giá phân khúc
def tim_san_pham_trong_bang_gia(
    bang_gia,
    ma_san_pham
):
    for dong_gia in bang_gia["danh_sach_san_pham"]:
        if dong_gia["ma_san_pham"] == ma_san_pham:
            return dong_gia

    return None


# Thêm một bảng giá phân khúc
def them_bang_gia_phan_khuc(
    ma_bang_gia,
    ten_bang_gia,
    cau_hinh_tinh_gia=None
):
    if tim_bang_gia_phan_khuc(ma_bang_gia) is not None:
        raise ValueError(
            f"Đã tồn tại bảng giá phân khúc: {ma_bang_gia}"
        )

    if cau_hinh_tinh_gia is None:
        cau_hinh_tinh_gia = {}

    bang_gia_moi = {
        "ma_bang_gia": ma_bang_gia,
        "ten_bang_gia": ten_bang_gia,
        "cau_hinh_tinh_gia": cau_hinh_tinh_gia,
        "danh_sach_san_pham": [],
    }

    danh_sach_bang_gia_phan_khuc.append(bang_gia_moi)

    return bang_gia_moi


# Xóa một bảng giá phân khúc
def xoa_bang_gia_phan_khuc(ma_bang_gia):
    bang_gia = tim_bang_gia_phan_khuc(ma_bang_gia)

    if bang_gia is None:
        raise ValueError(
            f"Không tìm thấy bảng giá phân khúc: {ma_bang_gia}"
        )

    danh_sach_bang_gia_phan_khuc.remove(bang_gia)


# Lấy giá cơ sở của một sản phẩm
def lay_gia_co_so(
    dong_gia,
    gia_co_so
):
    if gia_co_so == "gia_von":
        return dong_gia["gia_von"]

    if gia_co_so == "gia_niem_yet":
        return dong_gia["gia_niem_yet"]

    if gia_co_so == "gia_ban_hien_tai":
        return dong_gia["gia_ban"]

    raise ValueError(
        f"Giá cơ sở không hợp lệ: {gia_co_so}"
    )


# Tính giá theo cấu hình đã chọn
def tinh_gia_theo_cau_hinh(
    dong_gia,
    cau_hinh_tinh_gia
):
    gia_co_so = lay_gia_co_so(
        dong_gia,
        cau_hinh_tinh_gia["gia_co_so"]
    )

    phep_tinh = cau_hinh_tinh_gia["phep_tinh"]
    don_vi = cau_hinh_tinh_gia.get("don_vi", "gia_tri")
    gia_tri = cau_hinh_tinh_gia["gia_tri"]

    if phep_tinh == "+":
        if don_vi == "%":
            return gia_co_so * (1 + gia_tri / 100)

        return gia_co_so + gia_tri

    if phep_tinh == "-":
        if don_vi == "%":
            return gia_co_so * (1 - gia_tri / 100)

        return gia_co_so - gia_tri

    if phep_tinh == "*":
        return gia_co_so * gia_tri

    raise ValueError(
        f"Phép tính không hợp lệ: {phep_tinh}"
    )


# Thêm sản phẩm từ bảng giá niêm yết vào bảng giá phân khúc
def them_san_pham_vao_bang_gia_phan_khuc(
    bang_gia,
    dong_gia_niem_yet
):
    ma_san_pham = dong_gia_niem_yet["ma_san_pham"]

    dong_gia = tim_san_pham_trong_bang_gia(
        bang_gia,
        ma_san_pham
    )

    if dong_gia is not None:
        return dong_gia

    dong_gia_moi = {
        "ma_san_pham": ma_san_pham,
        "ten_san_pham": dong_gia_niem_yet["ten_san_pham"],
        "gia_von": dong_gia_niem_yet["gia_von"],
        "gia_niem_yet": dong_gia_niem_yet["gia_ban"],
        "gia_ban": dong_gia_niem_yet["gia_ban"],
    }

    bang_gia["danh_sach_san_pham"].append(dong_gia_moi)

    return dong_gia_moi


# Đồng bộ sản phẩm mới và thông tin thay đổi từ bảng giá niêm yết
# Sản phẩm đã bị người dùng xóa khỏi bảng giá phân khúc sẽ không tự quay lại
def dong_bo_tu_gia_niem_yet(
    bang_gia,
    danh_sach_gia_niem_yet
):
    ma_san_pham_da_co = {
        dong_gia["ma_san_pham"]
        for dong_gia in bang_gia["danh_sach_san_pham"]
    }

    for dong_gia_niem_yet in danh_sach_gia_niem_yet:
        ma_san_pham = dong_gia_niem_yet["ma_san_pham"]

        if ma_san_pham in ma_san_pham_da_co:
            dong_gia = tim_san_pham_trong_bang_gia(
                bang_gia,
                ma_san_pham
            )

            dong_gia["ten_san_pham"] = dong_gia_niem_yet["ten_san_pham"]
            dong_gia["gia_von"] = dong_gia_niem_yet["gia_von"]
            dong_gia["gia_niem_yet"] = dong_gia_niem_yet["gia_ban"]

            continue

        # Chỉ thêm sản phẩm mới chưa từng bị xóa khỏi bảng giá.
        # Sản phẩm mới thực sự được thêm bằng hàm thêm riêng.
        continue


# Thêm lại một sản phẩm đã bị xóa khỏi bảng giá phân khúc
def them_lai_san_pham(
    bang_gia,
    dong_gia_niem_yet
):
    return them_san_pham_vao_bang_gia_phan_khuc(
        bang_gia,
        dong_gia_niem_yet
    )


# Xóa một sản phẩm khỏi bảng giá phân khúc
def xoa_san_pham_khoi_bang_gia(
    bang_gia,
    ma_san_pham
):
    dong_gia = tim_san_pham_trong_bang_gia(
        bang_gia,
        ma_san_pham
    )

    if dong_gia is None:
        raise ValueError(
            f"Không tìm thấy sản phẩm trong bảng giá: {ma_san_pham}"
        )

    bang_gia["danh_sach_san_pham"].remove(dong_gia)


# Cập nhật giá bán cho một sản phẩm
def cap_nhat_gia_ban(
    bang_gia,
    ma_san_pham,
    gia_ban_moi
):
    if gia_ban_moi < 0:
        raise ValueError(
            "Giá bán không thể nhỏ hơn 0."
        )

    dong_gia = tim_san_pham_trong_bang_gia(
        bang_gia,
        ma_san_pham
    )

    if dong_gia is None:
        raise ValueError(
            f"Không tìm thấy sản phẩm trong bảng giá: {ma_san_pham}"
        )

    dong_gia["gia_ban"] = gia_ban_moi

    return dong_gia


# Áp dụng công thức cho toàn bộ sản phẩm trong bảng giá
def ap_dung_cau_hinh_tinh_gia(
    bang_gia,
    cau_hinh_tinh_gia,
    danh_sach_ma_san_pham=None
):
    bang_gia["cau_hinh_tinh_gia"] = cau_hinh_tinh_gia

    for dong_gia in bang_gia["danh_sach_san_pham"]:
        if (
            danh_sach_ma_san_pham is not None
            and dong_gia["ma_san_pham"] not in danh_sach_ma_san_pham
        ):
            continue

        dong_gia["gia_ban"] = tinh_gia_theo_cau_hinh(
            dong_gia,
            cau_hinh_tinh_gia
        )

    return bang_gia

