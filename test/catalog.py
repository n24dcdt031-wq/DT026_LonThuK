"""Danh muc 18 ca kiem thu doc lap cho DT026 (moi ca: ID, doi tuong, input, muc tieu, expected).

Expected duoc TINH TRUOC bang tay (hang so ghi san) hoac bang cong thuc/oracle doc lap
(sorted(a, reverse=True)[K-1] chi dung o day, khong dung trong src/). Moi ca tra ve
(input_str, expected_str, actual_str, passed, so_phep_kiem).
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import lon_thu_k as L  # noqa: E402


class _Dem:
    def __init__(self):
        self.n = 0
        self.ok = True

    def kiem(self, dieu_kien):
        self.n += 1
        if not dieu_kien:
            self.ok = False


def _tu_choi(f, *args):
    try:
        f(*args)
    except L.DauVaoKhongHopLe as e:
        return "TU CHOI: " + str(e)
    return "KHONG TU CHOI"


def _ca_gia_tri(a, K, gt, so_lc=None):
    """Ca chinh: ca 3 cach dung gt; so so sanh lua chon dung so_lc (neu cho)."""
    d = _Dem()
    r1, r2, r3 = L.lon_thu_K_lua_chon(a, K), L.lon_thu_K_sap_xep(a, K), L.lon_thu_K_quickselect(a, K)
    d.kiem(r1.gia_tri == gt)
    d.kiem(r2.gia_tri == gt)
    d.kiem(r3.gia_tri == gt)
    if so_lc is not None:
        d.kiem(r1.so_so_sanh == so_lc)
    inp = "a=%s; K=%d" % (a if len(a) <= 12 else "[... n=%d ...]" % len(a), K)
    exp = "gia_tri=%d" % gt + ("; so_sanh_lua_chon=%d" % so_lc if so_lc is not None else "")
    act = "gia_tri=%d/%d/%d (lua chon/sap xep/quickselect); so_sanh=%d/%d/%d" % (
        r1.gia_tri, r2.gia_tri, r3.gia_tri, r1.so_so_sanh, r2.so_so_sanh, r3.so_so_sanh)
    return inp, exp, act, d.ok, d.n


def vd01(): return _ca_gia_tri([7, 2, 9, 4], 2, 7, 5)          # 3+2
def vd02(): return _ca_gia_tri([5, 5, 3], 2, 5, 3)             # 2+1
def ph03(): return _ca_gia_tri([1, 9, 3], 1, 9, 2)
def ph04(): return _ca_gia_tri([1, 9, 3], 3, 1, 3)             # n(n-1)/2
def tk01(): return _ca_gia_tri([10, -3, 10, 8, -3, 10], 4, 8, 5 + 4 + 3 + 2)
def tk02(): return _ca_gia_tri([3, 1, 4, 1, 5, 9, 2, 6], 5, 3, 7 + 6 + 5 + 4 + 3)
def bien01(): return _ca_gia_tri([42], 1, 42, 0)
def bien02(): return _ca_gia_tri([2, 9, 4, 7, 4], 5, 2, 10)
def bien03(): return _ca_gia_tri([6, 6, 6, 6], 3, 6, 6)        # 3+2+1


def bien04():
    n, K = 5000, 2500
    a = list(range(n))
    random.Random(26).shuffle(a)                               # hoan vi 0..n-1
    # day giam la n-1..0 nen vi tri K co gia tri n-K
    return _ca_gia_tri(a, K, n - K, K * (n - 1) - K * (K - 1) // 2)


def loi01():
    r = _tu_choi(L.kiem_tra_K, 3, 0)
    d = _Dem(); d.kiem(r.startswith("TU CHOI")); d.kiem(_tu_choi(L.lon_thu_K_lua_chon, [1, 9, 3], 0).startswith("TU CHOI"))
    return "n=3; K=0", "TU CHOI (K<1)", r, d.ok, d.n


def loi02():
    r = _tu_choi(L.kiem_tra_K, 3, 4)
    d = _Dem(); d.kiem(r.startswith("TU CHOI")); d.kiem(_tu_choi(L.lon_thu_K_sap_xep, [1, 9, 3], 4).startswith("TU CHOI"))
    return "n=3; K=4", "TU CHOI (K>n)", r, d.ok, d.n


def loi03():
    d = _Dem()
    r = _tu_choi(L.kiem_tra_K, 5001, 1)
    d.kiem(r.startswith("TU CHOI"))
    d.kiem(_tu_choi(L.lon_thu_K_lua_chon, list(range(5001)), 1).startswith("TU CHOI"))
    d.kiem(L.kiem_tra_K(5000, 5000) is True)                   # bien tren hop le
    return "n=5001; K=1", "TU CHOI (n>5000); n=5000,K=5000 van hop le", r, d.ok, d.n


def loi04():
    d = _Dem()
    kq = [_tu_choi(L.kiem_tra_K, 3, True), _tu_choi(L.kiem_tra_K, 3, 2.0),
          _tu_choi(L.lon_thu_K_lua_chon, [1, 2.5, 3], 1), _tu_choi(L.lon_thu_K_lua_chon, [], 1)]
    for x in kq:
        d.kiem(x.startswith("TU CHOI"))
    return ("K=True; K=2.0; a=[1,2.5,3]; a=[]", "ca 4 input sai deu bi TU CHOI",
            "%d/4 bi tu choi" % sum(x.startswith("TU CHOI") for x in kq), d.ok, d.n)


def bat01():
    """Bat bien: sau luot i, i phan tu dau = i phan tu lon nhat theo thu tu giam."""
    d = _Dem()
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 10)
        a = [rng.randint(-5, 5) for _ in range(n)]
        vet = []
        K = rng.randint(1, n)
        L.lon_thu_K_lua_chon(a, K, vet)
        gold = sorted(a, reverse=True)
        for luot, _, b, _ in vet:
            d.kiem(b[:luot] == gold[:luot])
            d.kiem(sorted(b) == sorted(a))                       # khong mat phan tu
    return "300 mang ngau nhien (seed=1), n<=10, gia tri -5..5", "tien to i phan tu == i phan tu lon nhat, moi luot", \
        "%d phep kiem, %s" % (d.n, "dung het" if d.ok else "co sai"), d.ok, d.n


def doi01():
    """Doi chieu: moi mang n<=6 gia tri {0,1,2}, moi K, ba cach == oracle."""
    d = _Dem()
    tong = 0
    for n in range(1, 7):
        for code in range(3 ** n):
            a, c = [], code
            for _ in range(n):
                a.append(c % 3); c //= 3
            gold = sorted(a, reverse=True)
            for K in range(1, n + 1):
                g = gold[K - 1]
                tong += 1
                d.kiem(L.lon_thu_K_lua_chon(a, K).gia_tri == g)
                d.kiem(L.lon_thu_K_sap_xep(a, K).gia_tri == g)
                d.kiem(L.lon_thu_K_quickselect(a, K).gia_tri == g)
    return "moi mang n=1..6 gia tri {0,1,2}, moi K (%d cap (a,K))" % tong, "ba cach == sorted(a,reverse=True)[K-1]", \
        "%d phep kiem, %s" % (d.n, "dung het" if d.ok else "co sai"), d.ok, d.n


def cnt01():
    """So so sanh K luot chon == K(n-1)-K(K-1)/2 voi n=7, K=1..7 (gia tri tinh tay: 6,11,15,18,20,21,21)."""
    d = _Dem()
    a = [4, 8, 1, 9, 3, 7, 2]
    tay = [6, 11, 15, 18, 20, 21, 21]
    thuc = [L.lon_thu_K_lua_chon(a, K).so_so_sanh for K in range(1, 8)]
    for K in range(1, 8):
        d.kiem(thuc[K - 1] == tay[K - 1])
    return "a=[4,8,1,9,3,7,2]; K=1..7", "so_sanh = 6,11,15,18,20,21,21", "so_sanh = " + ",".join(map(str, thuc)), d.ok, d.n


def imm01():
    d = _Dem()
    a = [7, 2, 9, 4]
    goc = list(a)
    L.lon_thu_K_lua_chon(a, 2); L.lon_thu_K_sap_xep(a, 2); L.lon_thu_K_quickselect(a, 2); L.giai_bai(a, 3)
    d.kiem(a == goc)
    return "a=[7,2,9,4] sau khi goi ca ba ham", "a van = [7,2,9,4]", "a = %s" % a, d.ok, d.n


# (id, nhom, doi_tuong, muc_tieu, ham)
CASES = [
    ("VD01", "Vi du 1 phieu", "ham chinh (3 cach)", "Vi du 1: [7,2,9,4], K=2 cho 7", vd01),
    ("VD02", "Vi du 2 phieu", "ham chinh (3 cach)", "Vi du 2: gia tri trung chiem hai thu hang", vd02),
    ("PH03", "Ca phieu 3", "ham chinh", "K=1 cho phan tu lon nhat", ph03),
    ("PH04", "Ca phieu 4", "ham chinh", "K=n cho phan tu nho nhat; so sanh n(n-1)/2", ph04),
    ("LOI01", "Ca phieu 5a", "validator kiem_tra_K", "K=0 bi tu choi", loi01),
    ("LOI02", "Ca phieu 5b", "validator kiem_tra_K", "K>n bi tu choi", loi02),
    ("TK01", "Tu thiet ke 1", "ham chinh", "am + trung 3 lan: K roi vao giua cum trung", tk01),
    ("TK02", "Tu thiet ke 2", "ham chinh", "mang khong sap, co 2 so 1, K giua", tk02),
    ("BIEN01", "Bien 1", "ham chinh", "n=1 toi thieu, 0 so sanh", bien01),
    ("BIEN02", "Bien 2", "ham chinh", "K=n tren mang co trung", bien02),
    ("BIEN03", "Bien 3", "ham chinh", "tat ca bang nhau: moi phan tu chiem mot thu hang", bien03),
    ("BIEN04", "Bien 4", "ham chinh", "n=5000 (can tren), K=n/2", bien04),
    ("LOI03", "Input sai 3", "validator", "n=5001 vuot mien; n=5000 van hop le", loi03),
    ("LOI04", "Input sai 4", "validator", "K kieu bool/float, phan tu khong nguyen, mang rong", loi04),
    ("BAT01", "Bat bien", "lan vet lua chon", "sau luot i, tien to i phan tu la i phan tu lon nhat", bat01),
    ("DOI01", "Doi chieu", "ba cach vs oracle", "vet can moi mang n<=6, gia tri {0,1,2}", doi01),
    ("CNT01", "Bo dem", "so so sanh lua chon", "dem == K(n-1)-K(K-1)/2 tinh tay", cnt01),
    ("IMM01", "Khong sua input", "ba ham", "mang vao khong bi thay doi", imm01),
]
TABLE = {c[0]: c for c in CASES}
