"""Demo DT026 - Tim phan tu lon thu K.

  python demo.py                 chay Vi du 1 va Vi du 2 cua phieu (co lan vet)
  python demo.py --vd 1|2        chi chay Vi du 1 hoac Vi du 2 cua phieu (co lan vet)
  python demo.py --ca MA_CA      chay mot ca trong danh muc (VD01, TK01, BIEN03, LOI01, ...)
  python demo.py --loi           chay cac ca input sai (LOI01..LOI04)
  python demo.py --nhap          nhap tu ban phim: dong 1 la cac so nguyen cua a, dong 2 la K
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))
sys.path.insert(0, os.path.join(HERE, "test"))
import lon_thu_k as L  # noqa: E402


def chay(a, K, ten=""):
    print("== %s" % ten if ten else "==")
    print("Input   : a=%s ; K=%d ; n=%d" % (a, K, len(a)))
    vet = []
    r1 = L.lon_thu_K_lua_chon(a, K, vet)
    for luot, vt, mang, dem in vet:
        print("  luot %d: max o vi tri %d -> mang %s ; so_sanh tich luy=%d" % (luot, vt, mang, dem))
    r2 = L.lon_thu_K_sap_xep(a, K)
    r3 = L.lon_thu_K_quickselect(a, K)
    print("Output  : gia_tri=%d  (day giam: %s)" % (r1.gia_tri, sorted(a, reverse=True)))
    print("So so sanh: K luot chon=%d | sap toan bo (quicksort)=%d | quickselect=%d" % (
        r1.so_so_sanh, r2.so_so_sanh, r3.so_so_sanh))
    assert r1.gia_tri == r2.gia_tri == r3.gia_tri
    return r1


def nhap_ban_phim():
    print("Nhap cac so nguyen cua mang a (cach nhau dau cach):")
    a = [int(x) for x in input().split()]
    print("Nhap K:")
    K = int(input())
    try:
        chay(a, K, "nhap tu ban phim")
    except L.DauVaoKhongHopLe as e:
        print("TU CHOI input:", e)


def main(argv):
    if len(argv) >= 2 and argv[1] == "--nhap":
        nhap_ban_phim()
    elif len(argv) >= 3 and argv[1] == "--vd":
        if argv[2] == "1":
            chay([7, 2, 9, 4], 2, "Vi du 1 (phieu): expected gia_tri=7")
        elif argv[2] == "2":
            chay([5, 5, 3], 2, "Vi du 2 (phieu): expected gia_tri=5")
        else:
            print("Chi co --vd 1 hoac --vd 2")
            return 2
    elif len(argv) >= 3 and argv[1] == "--ca":
        from catalog import TABLE
        cid = argv[2].upper()
        if cid not in TABLE:
            print("Khong co ca", cid, "- cac ca:", ", ".join(TABLE))
            return 2
        _, nhom, dt, muc, f = TABLE[cid]
        inp, exp, act, ok, nk = f()
        print("== Ca %s (%s) - %s" % (cid, nhom, muc))
        print("Doi tuong: %s" % dt)
        print("Input    : %s" % inp)
        print("Expected : %s" % exp)
        print("Actual   : %s" % act)
        print("Ket luan : %s (%d phep kiem)" % ("PASS" if ok else "FAIL", nk))
        return 0 if ok else 1
    elif len(argv) >= 2 and argv[1] == "--loi":
        from catalog import TABLE
        for cid in ("LOI01", "LOI02", "LOI03", "LOI04"):
            inp, exp, act, ok, nk = TABLE[cid][4]()
            print("%s | input: %s\n      expected: %s\n      actual  : %s\n      => %s" % (
                cid, inp, exp, act, "PASS" if ok else "FAIL"))
    else:
        chay([7, 2, 9, 4], 2, "Vi du 1 (phieu): expected gia_tri=7")
        print()
        chay([5, 5, 3], 2, "Vi du 2 (phieu): expected gia_tri=5")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
