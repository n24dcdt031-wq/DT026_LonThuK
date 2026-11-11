"""DT026 - Tim phan tu lon thu K (INT13185, nhom 03).

Sinh vien: Ma Le Minh Hung - MSSV N24DCDT031 - lop D24CQDT01-N.
Giao trinh INT1306: Chuong 2, muc 2.7.4; bai tap 2.8 bai 26 (trang in 58-59, 61).

Quy uoc
  * Mang a la list[int], 1 <= n <= 5000, 1 <= K <= n.
  * "Lon thu K" tinh tren day sap GIAM, tinh ca lap: gia tri trung van chiem
    thu hang rieng (khong tim gia tri phan biet thu K).
  * K ngoai mien, n ngoai mien hoac phan tu khong phai so nguyen -> raise
    DauVaoKhongHopLe (la ValueError).
  * "So so sanh" = so lan thuc hien mot phep so sanh giua HAI GIA TRI cua mang
    (a[j] > a[m] ...). Phep so sanh chi so / bien dieu khien vong lap khong tinh.

Ba cach tinh (phan tu cai):
  lon_thu_K_lua_chon  : K luot chon max (bat buoc theo phieu).
  lon_thu_K_sap_xep   : tu sap toan bo bang quicksort roi lay vi tri K.
  lon_thu_K_quickselect : tuy chon, phan hoach, chi giu nhanh chua thu hang K.
Khong ham nao sua mang dau vao (moi ham lam viec tren ban sao).
"""

from collections import namedtuple

N_MAX = 5000

KetQua = namedtuple("KetQua", ["gia_tri", "so_so_sanh"])


class DauVaoKhongHopLe(ValueError):
    """Dau vao vi pham dieu kien cua phieu DT026."""


# --------------------------------------------------------------------------
# Kiem tra dau vao
# --------------------------------------------------------------------------
def _la_so_nguyen(x):
    # bool la lop con cua int trong Python nhung khong phai so nguyen cua bai.
    return isinstance(x, int) and not isinstance(x, bool)


def kiem_tra_K(n, K):
    """Kiem tra 1 <= n <= N_MAX va 1 <= K <= n truoc khi doc ket qua.

    Tra ve True neu hop le; nguoc lai raise DauVaoKhongHopLe co ly do.
    """
    if not _la_so_nguyen(n):
        raise DauVaoKhongHopLe("n phai la so nguyen, nhan %r" % (n,))
    if not _la_so_nguyen(K):
        raise DauVaoKhongHopLe("K phai la so nguyen, nhan %r" % (K,))
    if n < 1 or n > N_MAX:
        raise DauVaoKhongHopLe("n=%d ngoai mien 1..%d" % (n, N_MAX))
    if K < 1 or K > n:
        raise DauVaoKhongHopLe("K=%d ngoai mien 1..n (n=%d)" % (K, n))
    return True


def kiem_tra_mang(a):
    """Kiem tra a la list[int] khong rong, n <= N_MAX."""
    if not isinstance(a, list):
        raise DauVaoKhongHopLe("a phai la list, nhan %s" % type(a).__name__)
    if len(a) == 0:
        raise DauVaoKhongHopLe("a rong (n=0): khong co phan tu nao de xep hang")
    for i, x in enumerate(a):
        if not _la_so_nguyen(x):
            raise DauVaoKhongHopLe("a[%d]=%r khong phai so nguyen" % (i + 1, x))
    return True


def _kiem_tra_tat_ca(a, K):
    kiem_tra_mang(a)
    kiem_tra_K(len(a), K)


# --------------------------------------------------------------------------
# Cach 1: K luot lua chon max (Chuong 2, muc 2.2.2 + 2.7.4)
# --------------------------------------------------------------------------
def lon_thu_K_lua_chon(a, K, vet=None):
    """K luot lua chon: luot i dua phan tu lon nhat cua a[i..n] ve vi tri i.

    Sau luot i, i phan tu dau la i phan tu lon nhat theo thu tu giam
    (bat bien). Khong can sap phan con lai. Tra ve KetQua(gia_tri, so_so_sanh).

    vet: neu la list thi them moi luot mot tuple
         (luot, vi_tri_max, mang_sau_luot, so_sanh_luy_ke) de lan vet.
    So so sanh chinh xac = sum_{i=1..K} (n - i) = K(n-1) - K(K-1)/2.
    """
    _kiem_tra_tat_ca(a, K)
    b = list(a)
    n = len(b)
    dem = 0
    for i in range(K):                 # luot thu i+1 (0-based i)
        m = i                          # vi tri max tam thoi cua b[i..n-1]
        for j in range(i + 1, n):
            dem += 1                   # so sanh b[j] voi b[m]
            if b[j] > b[m]:            # strict: giu vi tri dau khi bang nhau
                m = j
        if m != i:
            b[i], b[m] = b[m], b[i]
        if vet is not None:
            vet.append((i + 1, m + 1, list(b), dem))
    return KetQua(b[K - 1], dem)


# --------------------------------------------------------------------------
# Cach 2: tu sap toan bo (quicksort giam) roi lay vi tri K
# --------------------------------------------------------------------------
def _phan_hoach_giam(b, l, r, dem):
    """Phan hoach Hoare, chot giua, sap GIAM. dem la list 1 phan tu (so sanh).

    Sau khi xong tra ve (i, j) voi j < i: b[l..j] >= chot, b[i..r] <= chot,
    cac phan tu o giua (neu co) bang chot. Con tro luon tien sau khi doi cho
    ke ca khi khoa bang chot nen khong lap vo han tren day toan so bang nhau.
    """
    chot = b[(l + r) // 2]
    i, j = l, r
    while i <= j:
        while True:
            dem[0] += 1
            if b[i] > chot:
                i += 1
            else:
                break
        while True:
            dem[0] += 1
            if b[j] < chot:
                j -= 1
            else:
                break
        if i <= j:
            b[i], b[j] = b[j], b[i]
            i += 1
            j -= 1
    return i, j


def _sap_doan(b, l, r, dem):
    """Quicksort giam tren b[l..r]: de quy doan ngan, lap tren doan dai (do sau O(log n))."""
    while l < r:
        i, j = _phan_hoach_giam(b, l, r, dem)
        if j - l < r - i:
            _sap_doan(b, l, j, dem)
            l = i
        else:
            _sap_doan(b, i, r, dem)
            r = j


def sap_giam(a):
    """Tra ve (ban_sao_sap_giam, so_so_sanh) bang quicksort tu cai."""
    b = list(a)
    dem = [0]
    _sap_doan(b, 0, len(b) - 1, dem)
    return b, dem[0]


def lon_thu_K_sap_xep(a, K):
    """Sap giam toan bo roi lay b[K] (1-based). Tra ve KetQua."""
    _kiem_tra_tat_ca(a, K)
    b, dem = sap_giam(a)
    return KetQua(b[K - 1], dem)


# --------------------------------------------------------------------------
# Cach 3 (tuy chon): quickselect - chi giu nhanh chua thu hang K
# --------------------------------------------------------------------------
def lon_thu_K_quickselect(a, K):
    """Phan hoach roi chi tiep tuc o nhanh chua vi tri dich t = K-1 (0-based).

    Trung binh O(n), xau nhat O(n^2) voi chot giua (khong co bao dam nhu
    median-of-medians). Tra ve KetQua(gia_tri, so_so_sanh).
    """
    _kiem_tra_tat_ca(a, K)
    b = list(a)
    t = K - 1
    l, r = 0, len(b) - 1
    dem = [0]
    while l < r:
        i, j = _phan_hoach_giam(b, l, r, dem)
        if t <= j:
            r = j
        elif t >= i:
            l = i
        else:          # j < t < i: moi phan tu o giua bang chot
            break
    return KetQua(b[t], dem[0])


# --------------------------------------------------------------------------
# Tien ich de demo / kiem thu
# --------------------------------------------------------------------------
def so_so_sanh_lua_chon_ly_thuyet(n, K):
    """Cong thuc dong K(n-1) - K(K-1)/2 (dung de kiem, khong dung trong thuat toan)."""
    return K * (n - 1) - K * (K - 1) // 2


def giai_bai(a, K):
    """Chay ca ba cach, tra ve dict ket qua va kiem tra chung bang nhau."""
    r1 = lon_thu_K_lua_chon(a, K)
    r2 = lon_thu_K_sap_xep(a, K)
    r3 = lon_thu_K_quickselect(a, K)
    if not (r1.gia_tri == r2.gia_tri == r3.gia_tri):
        raise AssertionError("ba cach cho ket qua khac nhau: %r %r %r" % (r1, r2, r3))
    return {"gia_tri": r1.gia_tri, "lua_chon": r1, "sap_xep": r2, "quickselect": r3}
