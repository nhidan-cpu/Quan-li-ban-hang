import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from thao_tac_danh_sach_san_pham import chuan_bi_sua, danh_sach_san_pham, luu_san_pham, tao_san_pham, chuan_bi_them, luu_them_moi, tim_san_pham, chuan_bi_xoa, xoa_san_pham

cua_so_danh_sach_san_pham = tk.Tk()
cua_so_danh_sach_san_pham.title("Quản lý sản phẩm")
cua_so_danh_sach_san_pham.geometry("600x400")

cot_danh_sach_san_pham = ("ma", "ten", "gia", "dvt")
bang_danh_sach_san_pham = ttk.Treeview(cua_so_danh_sach_san_pham, columns=cot_danh_sach_san_pham, show="headings")

bang_danh_sach_san_pham.heading("ma", text="Mã hàng")
bang_danh_sach_san_pham.heading("ten", text="Tên sản phẩm")
bang_danh_sach_san_pham.heading("gia", text="Giá bán lẻ")
bang_danh_sach_san_pham.heading("dvt", text="Đơn vị")

bang_danh_sach_san_pham.column("ma", width=100, anchor="center")
bang_danh_sach_san_pham.column("ten", width=200, anchor="w")
bang_danh_sach_san_pham.column("gia", width=100, anchor="e")
bang_danh_sach_san_pham.column("dvt", width=80, anchor="center")

bang_danh_sach_san_pham.pack(fill="both", expand=True)

def mo_form_them_san_pham():
    
    form_them_san_pham = tk.Toplevel(cua_so_danh_sach_san_pham)
    form_them_san_pham.title("Thêm sản phẩm")

    ds_ma_vach_le = []

    tk.Label(form_them_san_pham, text="Mã vạch lẻ:").pack()
    o_ma_vach_moi = tk.Entry(form_them_san_pham)
    o_ma_vach_moi.pack()

    hop_ma_vach_le = tk.Listbox(form_them_san_pham)
    hop_ma_vach_le.pack()

    def xu_ly_them_ma_vach():
        ma_moi = o_ma_vach_moi.get()
        if ma_moi == "":
            return
        ds_ma_vach_le.append(ma_moi)
        hop_ma_vach_le.insert("end",ma_moi)
        o_ma_vach_moi.delete(0,"end")
    
    nut_them_ma_vach = tk.Button(form_them_san_pham, text="Thêm mã vạch", command=xu_ly_them_ma_vach)
    nut_them_ma_vach.pack()

    tk.Label(form_them_san_pham, text="Tên sản phẩm:").pack()
    o_ten = tk.Entry(form_them_san_pham)
    o_ten.pack()
    
    tk.Label(form_them_san_pham, text="Giá bán lẻ:").pack()
    o_gia = tk.Entry(form_them_san_pham)
    o_gia.pack()
 
    tk.Label(form_them_san_pham, text="Mã tìm nhanh:").pack()
    o_ma_tim_nhanh = tk.Entry(form_them_san_pham)
    o_ma_tim_nhanh.pack()

    tk.Label(form_them_san_pham, text="Giá nhập:").pack()
    o_gia_nhap = tk.Entry(form_them_san_pham)
    o_gia_nhap.pack()

    tk.Label(form_them_san_pham, text="Danh mục:").pack()
    o_danh_muc = tk.Entry(form_them_san_pham)
    o_danh_muc.pack()

    tk.Label(form_them_san_pham, text="Mã VAT").pack()
    o_ma_vat = tk.Entry(form_them_san_pham)
    o_ma_vat.pack()

    tk.Label(form_them_san_pham, text="Đơn vị tính chính").pack()
    o_dvt_chinh = tk.Entry(form_them_san_pham)
    o_dvt_chinh.pack()

    khung_thu = tk.Frame(form_them_san_pham)
    khung_thu.pack()
    o_thu = tk.Entry(khung_thu)
    o_thu.pack()
    nut_thu = tk.Button(khung_thu, text="X")
    nut_thu.pack(side="left")

    def xu_ly_luu():
        ten_san_pham = o_ten.get()
        gia_ban_le = int(o_gia.get())
        ma = o_ma_tim_nhanh.get()
        # TODO: dvt_quy_doi hiện vẫn đang tạm (vì độ phức tạp) - cần làm riêng
        ma_vach_le = ds_ma_vach_le
        ma_vat = o_ma_vat.get()
        danh_muc = o_danh_muc.get()
        gia_nhap = int(o_gia_nhap.get())
        dvt_chinh = o_dvt_chinh.get()
        dvt_quy_doi = []

        san_pham_moi = tao_san_pham(
            ma_vach_san_pham=ma_vach_le,
            ma_tim_nhanh=ma,
            ma_vat=ma_vat,
            ten_san_pham=ten_san_pham,
            danh_muc=danh_muc,
            gia_nhap=gia_nhap,
            gia_ban=gia_ban_le,
            dvt_chinh=dvt_chinh,
            dvt_quy_doi=dvt_quy_doi
        )
        san_pham_moi_hop_le = chuan_bi_them(danh_sach_san_pham, san_pham_moi)
        if san_pham_moi_hop_le is not None:
            luu_them_moi(danh_sach_san_pham, san_pham_moi_hop_le)
            bang_danh_sach_san_pham.insert("", "end", values=(san_pham_moi_hop_le["ma_tim_nhanh"], san_pham_moi_hop_le["ten_san_pham"], san_pham_moi_hop_le["gia_ban_le"], san_pham_moi_hop_le["dvt_chinh"]))
            form_them_san_pham.destroy()
     
    nut_luu_san_pham = tk.Button(form_them_san_pham, text="Lưu sản phẩm", command=xu_ly_luu)
    nut_luu_san_pham.pack()

def lay_san_pham_dang_chon():
    chon = bang_danh_sach_san_pham.selection()
    if chon == ():
        messagebox.showwarning("Thông báo", "Bạn chưa chọn sản phẩm nào")
        return None
    gia_tri = bang_danh_sach_san_pham.item(chon[0], "values")
    san_pham = tim_san_pham(danh_sach_san_pham, gia_tri[0])
    return san_pham

def xu_ly_xoa():
    san_pham = lay_san_pham_dang_chon()
    if san_pham is None:
        return
    xac_nhan = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sản phẩm: {san_pham['ten_san_pham']}?")
    if xac_nhan:
        san_pham_can_xoa = chuan_bi_xoa(danh_sach_san_pham, san_pham["ma_tim_nhanh"])
        if san_pham_can_xoa is not None:
            xoa_san_pham(danh_sach_san_pham, san_pham_can_xoa)
            chon = bang_danh_sach_san_pham.selection()
            bang_danh_sach_san_pham.delete(chon[0])

def mo_form_sua_san_pham():
    san_pham = lay_san_pham_dang_chon()
    if san_pham is None:
        return

    form_sua_san_pham = tk.Toplevel(cua_so_danh_sach_san_pham)
    form_sua_san_pham.title("Sửa sản phẩm")

    ds_ma_vach_le = list(san_pham["ma_vach_le"])

    tk.Label(form_sua_san_pham, text="Mã vạch lẻ:").pack()
    o_ma_vach_moi = tk.Entry(form_sua_san_pham)
    o_ma_vach_moi.pack()

    hop_ma_vach_le = tk.Listbox(form_sua_san_pham)
    hop_ma_vach_le.pack()

    for ma in ds_ma_vach_le:
        hop_ma_vach_le.insert("end",ma)

    def xu_ly_them_ma_vach():
        ma_moi = o_ma_vach_moi.get()
        if ma_moi == "":
            return
        ds_ma_vach_le.append(ma_moi)
        hop_ma_vach_le.insert("end",ma_moi)
        o_ma_vach_moi.delete(0,"end")

    nut_them_ma_vach = tk.Button(form_sua_san_pham, text="Thêm mã vạch", command=xu_ly_them_ma_vach)
    nut_them_ma_vach.pack()

    tk.Label(form_sua_san_pham, text="Tên sản phẩm").pack()
    o_ten = tk.Entry(form_sua_san_pham)
    o_ten.insert(0,san_pham["ten_san_pham"])
    o_ten.pack()

    tk.Label(form_sua_san_pham, text="Giá bán lẻ:").pack()
    o_gia = tk.Entry(form_sua_san_pham)
    o_gia.insert(0, str(san_pham["gia_ban_le"]))
    o_gia.pack()

    tk.Label(form_sua_san_pham, text="Mã tìm nhanh").pack()
    o_ma_tim_nhanh = tk.Entry(form_sua_san_pham)
    o_ma_tim_nhanh.insert(0,san_pham["ma_tim_nhanh"])
    o_ma_tim_nhanh.pack()

    tk.Label(form_sua_san_pham, text="Giá nhập:").pack()
    o_gia_nhap = tk.Entry(form_sua_san_pham)
    o_gia_nhap.insert(0, str(san_pham["gia_nhap"]))
    o_gia_nhap.pack()

    tk.Label(form_sua_san_pham, text="Danh mục:").pack()
    o_danh_muc = tk.Entry(form_sua_san_pham)
    o_danh_muc.insert(0, str(san_pham["danh_muc"]))
    o_danh_muc.pack()

    tk.Label(form_sua_san_pham, text="Mã VAT").pack()
    o_ma_vat = tk.Entry(form_sua_san_pham)
    o_ma_vat.insert(0, str(san_pham["ma_vat"]))
    o_ma_vat.pack()

    tk.Label(form_sua_san_pham, text="Đơn vị tính chính").pack()
    o_dvt_chinh = tk.Entry(form_sua_san_pham)
    o_dvt_chinh.insert(0, str(san_pham["dvt_chinh"]))
    o_dvt_chinh.pack()

    def cap_nhat_san_pham():
        thay_doi = {
            "ma_vach_le": ds_ma_vach_le,
            "ten_san_pham": o_ten.get(),
            "gia_ban_le": int(o_gia.get()),
            "ma_tim_nhanh": o_ma_tim_nhanh.get(),
            "gia_nhap": int(o_gia_nhap.get()),
            "danh_muc": o_danh_muc.get(),
            "ma_vat": o_ma_vat.get(),
            "dvt_chinh": o_dvt_chinh.get()
        }
        ket_qua = chuan_bi_sua(danh_sach_san_pham, san_pham["ma_tim_nhanh"], thay_doi)

        if ket_qua is not None:
            san_pham_can_sua, san_pham_nhap = ket_qua
            luu_san_pham(san_pham_can_sua, san_pham_nhap)
            chon = bang_danh_sach_san_pham.selection()
            bang_danh_sach_san_pham.item(
                chon[0],
                values=(
                    san_pham_can_sua["ma_tim_nhanh"],
                    san_pham_can_sua["ten_san_pham"],
                    san_pham_can_sua["gia_ban_le"],
                    san_pham_can_sua["dvt_chinh"]
                )
            )
            form_sua_san_pham.destroy()

    nut_luu_sua = tk.Button(form_sua_san_pham, text="Lưu thay đổi", command=cap_nhat_san_pham)
    nut_luu_sua.pack()        
 
nut_them_san_pham = tk.Button(cua_so_danh_sach_san_pham, text="Thêm sản phẩm", command=mo_form_them_san_pham)
nut_them_san_pham.pack()

nut_xoa_san_pham = tk.Button(cua_so_danh_sach_san_pham, text="Xóa sản phẩm", command=xu_ly_xoa)
nut_xoa_san_pham.pack()

nut_sua_san_pham = tk.Button(cua_so_danh_sach_san_pham, text="Sửa sản phẩm", command=mo_form_sua_san_pham)
nut_sua_san_pham.pack()

san_pham_mau = tao_san_pham(
    ma_vach_san_pham=["A1", "A2"],
    ma_tim_nhanh="SP001",
    ma_vat="VAT001",
    ten_san_pham="Coca Cola lon",
    danh_muc="Coca-Cola",
    gia_nhap=8000,
    gia_ban=10000,
    dvt_chinh="lon",
    dvt_quy_doi=[
        {"ten_dvt": "thùng", "mv": ["T1"], "so_luong": 24, "gia_ban": 200000}
    ]
)
san_pham_mau_hop_le = chuan_bi_them(danh_sach_san_pham, san_pham_mau)
if san_pham_mau_hop_le is not None:
    luu_them_moi(danh_sach_san_pham, san_pham_mau_hop_le)

for san_pham in danh_sach_san_pham:
    bang_danh_sach_san_pham.insert("", "end", values=(san_pham["ma_tim_nhanh"], san_pham["ten_san_pham"], san_pham["gia_ban_le"], san_pham["dvt_chinh"]))

cua_so_danh_sach_san_pham.mainloop()
