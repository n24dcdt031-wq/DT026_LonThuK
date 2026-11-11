"""Khao sat ba quy mo Q1 (n=10), Q2 (n=100), Q3 (n=1000) voi K = 1, 3, n/2, n.

Du lieu: random.Random(26) sinh n so nguyen trong [-10^6, 10^6]. Do dem so sanh
(phep so sanh giua hai gia tri) cua K luot chon, sap toan bo (quicksort) va
quickselect. Co them thoi gian (trung vi 5 lan, giay) - chi mang tinh tham khao.
"""
import os
import random
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import lon_thu_k as L  # noqa: E402


def thoi_gian(f, a, K, lan=5):
    ds = []
    for _ in range(lan):
        t = time.perf_counter()
        f(a, K)
        ds.append(time.perf_counter() - t)
    return statistics.median(ds)


def main():
    print("Python", sys.version.split()[0], "| seed=26 | gia tri trong [-10^6,10^6]")
    print("%-3s %-5s %-5s %-9s %-14s %-12s %-14s | thoi gian trung vi (ms): chon / sap / qselect" % (
        "Bo", "n", "K", "gia_tri", "so_sanh_chon", "so_sanh_sap", "so_sanh_qsel"))
    for ten, n in (("Q1", 10), ("Q2", 100), ("Q3", 1000)):
        rng = random.Random(26)
        a = [rng.randint(-10 ** 6, 10 ** 6) for _ in range(n)]
        for K in (1, 3, n // 2, n):
            r1, r2, r3 = L.lon_thu_K_lua_chon(a, K), L.lon_thu_K_sap_xep(a, K), L.lon_thu_K_quickselect(a, K)
            assert r1.gia_tri == r2.gia_tri == r3.gia_tri == sorted(a, reverse=True)[K - 1]
            assert r1.so_so_sanh == L.so_so_sanh_lua_chon_ly_thuyet(n, K)
            t = [1000 * thoi_gian(f, a, K) for f in (L.lon_thu_K_lua_chon, L.lon_thu_K_sap_xep, L.lon_thu_K_quickselect)]
            print("%-3s %-5d %-5d %-9d %-14d %-12d %-14d | %.3f / %.3f / %.3f" % (
                ten, n, K, r1.gia_tri, r1.so_so_sanh, r2.so_so_sanh, r3.so_so_sanh, *t))


if __name__ == "__main__":
    main()
