"""複利帳本上架輪播（5 張）。用法：python3 -I shop_launch.py OUTDIR
數字全部由程式計算：每月 1 萬、年化 6%、按月複利、30 年；先計息再投入。"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "style"))
import noirxu_style as ns
from noirxu_style import *
import feed_lib as fl

OUT = sys.argv[1]
BASE = "每月投入 1 萬　年化 6%　按月複利　30 年　情境試算，非投資建議"
FAIL = "報酬更低或中斷更久，結果會不同。"
SD = "MONEY　停在哪"
T = 5

def series(skip_years=None, n=360, pmt=1.0, a=0.06):
    m = (1 + a) ** (1 / 12) - 1
    b, paid = 0.0, 0.0
    for i in range(1, n + 1):
        b *= 1 + m
        y = (i - 1) // 12 + 1
        if skip_years and skip_years[0] <= y < skip_years[0] + skip_years[1]:
            continue
        b += pmt; paid += pmt
    return b, paid

A, PA = series()
rows = []
for k in (1, 2, 5):
    r = [f"停 {k} 年"]
    for y0 in (1, 11, 21):
        r.append(f"{A - series((y0, k))[0]:.1f}")
    rows.append(r)
B, PB = series((11, 2))
gap, pgap = A - B, PA - PB
print("A", round(A, 1), "rows", rows, "gap", round(gap, 1), "principal", round(pgap, 1))
assert abs(A - 974.5) < 0.1 and abs(gap - 72.5) < 0.1

def sq(y, hol_from=0, hol_to=0, sz=15):
    xl, xr = ML + 8, MR - 8; step = (xr - xl) / 29
    for c in range(30):
        cx = xl + c * step
        box = [(cx - sz / 2) * S, (y - sz / 2) * S, (cx + sz / 2) * S, (y + sz / 2) * S]
        if hol_from <= c < hol_to: ns.d.rectangle(box, outline=hexc(VERM), width=int(2 * S))
        else: ns.d.rectangle(box, fill=hexc(INK))

def cover_rows():
    for k, (lab, hf, ht) in enumerate((("一直投", 0, 0), ("第 11 年停 2 年", 10, 12))):
        y = 930 + k * 110
        ttext(ML, y - 58, lab, font(SANS_R, 26), INK if k == 0 else GRAY, 3); sq(y, hf, ht)

o = OUT
fl.cover(o, "s1.png", 1, T, SD, "金錢日誌　工具", "停 2 年，", "差的只是 24 萬", "答案在第 3 張。",
         "一格＝一年，空心＝停扣的年份。", [BASE, FAIL], rows=cover_rows)

fl.table(o, "s2.png", 2, T, SD, "停多久 × 停在哪", "和一直投相比，少多少（萬）",
         ["", "前期 第1年起", "中期 第11年起", "後期 第21年起"], rows,
         f"基準：30 年一直投，終值 {A:.1f} 萬。越早停、停越久，少越多。", [BASE, FAIL])

fl.big(o, "s3.png", 3, T, SD, "第 11 年停 2 年，終點少", f"{gap:.1f}", "萬",
       f"少投的本金只有 {pgap:.0f} 萬。", f"其餘 {gap - pgap:.1f} 萬，是那 2 年的錢少滾了 18 年。", [BASE, FAIL])

fl.text(o, "s4.png", 4, T, SD, [("停之前，", SERIF_L, 72, INK, 7, 260), ("先算一次。", SERIF_M, 72, VERM, 7, 360),
        ("__rule__", 0, 0, 0, 0, 520),
        ("同一張表，換成你的月投、報酬、停幾年。", SANS_R, 34, INK, 5, 570),
        ("主頁連結有免費試算，", SANS_R, 34, INK, 5, 640),
        ("和兩頁「停扣成本速查表」。", SANS_R, 34, INK, 5, 700)], [BASE, FAIL], seal_xy=None)

fl.text(o, "s5.png", 5, T, SD, [("把 30 年", SERIF_L, 72, INK, 7, 260), ("算清楚。", SERIF_M, 72, VERM, 7, 360),
        ("__rule__", 0, 0, 0, 0, 520),
        ("NOIRXU 複利帳本：試算、里程碑、", SANS_R, 32, INK, 4, 570),
        ("逐月表、年度方陣、每月實際紀錄。", SANS_R, 32, INK, 4, 630),
        ("Excel／Google 試算表都能用。連結在主頁。", SANS_L, 30, GRAY, 4, 700),
        ("存起來，想停扣時先看一次。", SERIF_M, 44, INK, 5, 840)], [BASE, FAIL])
print("ok")
