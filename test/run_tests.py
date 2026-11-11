"""Chay 18 ca kiem thu DT026:  python test/run_tests.py   (thoat 0 neu tat ca PASS)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import CASES  # noqa: E402


def main():
    npass = nphep = 0
    print("DT026 - kiem thu 'Tim phan tu lon thu K'  (Ma Le Minh Hung, N24DCDT031)")
    print("%-7s %-34s %-6s %s" % ("Ca", "Doi tuong", "Ket qua", "So phep kiem"))
    for cid, nhom, dt, muc, f in CASES:
        inp, exp, act, ok, nk = f()
        nphep += nk
        npass += ok
        print("%-7s %-34s %-6s %d" % (cid, dt, "PASS" if ok else "FAIL", nk))
        if not ok:
            print("   input   :", inp)
            print("   expected:", exp)
            print("   actual  :", act)
    print("-" * 60)
    print("TONG KET: %d/%d ca doc lap PASS; %d phep kiem (assert) tong cong" % (npass, len(CASES), nphep))
    return 0 if npass == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
