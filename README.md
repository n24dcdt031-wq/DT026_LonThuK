# DT026 — Tìm phần tử lớn thứ K

- Họ tên / MSSV / lớp: **Mã Lê Minh Hùng** / **N24DCDT031** / **D24CQDT01-N**
- Học phần: INT13185 (INT1306) — Cấu trúc dữ liệu và giải thuật, nhóm 03, GV Hồ Nhựt Minh
- Mã đề: **DT026** — Tìm phần tử lớn thứ K
- Giáo trình: Chương 2, mục 2.7.4; mục 2.8 bài 26; trang in 58–59, 61; trang PDF 70–71, 73
- Ngôn ngữ: **Python 3.13** (chỉ dùng thư viện chuẩn; chạy được từ Python 3.8 trở lên). Không cần cài thêm gói.

## Bài toán
Cho `a` (list số nguyên, 1 ≤ n ≤ 5000) và `K` (1 ≤ K ≤ n), tìm giá trị đứng thứ K khi
`a` xếp **giảm**, tính cả các lần lặp (giá trị trùng vẫn chiếm thứ hạng riêng). K ngoài miền → báo lỗi
(`DauVaoKhongHopLe`). Ví dụ: `a=[7,2,9,4], K=2 → 7`; `a=[5,5,3], K=2 → 5`.

## Cấu trúc
```
src/lon_thu_k.py     kiem_tra_K, lon_thu_K_lua_chon (bắt buộc), lon_thu_K_sap_xep (tự quicksort), lon_thu_K_quickselect (tùy chọn)
demo.py              ví dụ phiếu, từng ca, input sai, nhập bàn phím
test/catalog.py      18 ca kiểm độc lập (ID, đối tượng, input, expected)
test/run_tests.py    chạy toàn bộ ca, in tổng kết
scripts/khao_sat.py  khảo sát ba quy mô Q1 (n=10), Q2 (n=100), Q3 (n=1000)
docs/anh_ket_qua/    ảnh minh chứng A01–A11 (nếu có) ; docs/logs/ log chạy thật
```

## Lệnh chạy
```
python --version
python demo.py                  # Ví dụ 1 và Ví dụ 2 của phiếu (có lần vết từng lượt)
python demo.py --vd 1|2        # chỉ Ví dụ 1 hoặc Ví dụ 2 (có lần vết)
python demo.py --ca TK01        # một ca bất kỳ: VD01 VD02 PH03 PH04 TK01 TK02 BIEN01..BIEN04 LOI01..LOI04 BAT01 DOI01 CNT01 IMM01
python demo.py --loi            # các input sai bị từ chối
python demo.py --nhap           # nhập mới: dòng 1 là các số của a (cách nhau dấu cách), dòng 2 là K
python test/run_tests.py        # bộ kiểm thử 18 ca
python scripts/khao_sat.py      # khảo sát Q1–Q3
```
(Dùng `python3` thay `python` trên Linux/macOS.) Dùng trực tiếp trong mã:
```python
from lon_thu_k import lon_thu_K_lua_chon
print(lon_thu_K_lua_chon([7, 2, 9, 4], 2))   # KetQua(gia_tri=7, so_so_sanh=5)
```

## Kết quả kiểm thử
18 ca độc lập, 18/18 PASS; 20 184 phép kiểm (assert) — số ca và số assert tính riêng.
"Số so sánh" là số lần so sánh giữa hai giá trị của mảng; K lượt chọn đúng bằng K(n−1) − K(K−1)/2.

## Công bố và kiểm tra bản clone
```
git clone <URL_GITHUB> kiem_tra_ban_nop
cd kiem_tra_ban_nop
git rev-parse HEAD
python demo.py
python test/run_tests.py
```
