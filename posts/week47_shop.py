"""2026 W47（11/16–11/20）商店導流貼文：輪播 2、單圖 1。用法：python3 -I posts/week47_shop.py OUTDIR
數字全部由程式計算；基準：每月 1 萬、年化 6%、按月複利、先計息再投入、30 年＝974.5 萬。
每個數字都用「封閉公式」與「逐月迴圈」兩種算法 assert 互相驗算。"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "style"))
import noirxu_style as ns
from noirxu_style import *
import feed_lib as fl

OUT = sys.argv[1]
N = 360
M = 1.06 ** (1 / 12) - 1
BASE = "每月投入 1 萬　年化 6%　按月複利　30 年　情境試算，非投資建議"
FAIL = "報酬更低或中斷更久，結果會不同。"


def fv(n, m=M):
    """封閉公式：每月期末投入 1、共 n 期的終值。"""
    return ((1 + m) ** n - 1) / m


def loop(skip=lambda i: False, extra=lambda i: 0.0, n=N, m=M):
    """逐月迴圈：先計息再投入。skip(i) 為 True 的月份不投；extra(i) 為該月多投金額（萬）。"""
    b = 0.0
    for i in range(1, n + 1):
        b *= 1 + m
        if not skip(i):
            b += 1.0 + extra(i)
    return b


def close(a, b, tol=1e-6):
    assert abs(a - b) < tol, (a, b)


# ---------- 基準 ----------
A = loop()
close(A, fv(N))
assert abs(A - 974.5) < 0.05, A

# ---------- 題材 1：停了之後，要補多少才追得回 ----------
stop2 = lambda i: 120 < i <= 144              # 第 11–12 年（第 121–144 月）不投
B = loop(stop2)
B_closed = fv(N) - sum((1 + M) ** (N - i) for i in range(121, 145))
close(B, B_closed)
GAP = A - B
assert abs(GAP - 72.5) < 0.05, GAP

catch = []                                     # (開始補的年, 補幾年, 每月多投元, 多投本金萬)
for y0 in (13, 21, 26):
    start = (y0 - 1) * 12 + 1
    n_left = N - start + 1
    e = GAP / fv(n_left)                       # 封閉公式解方程
    lo, hi = 0.0, 5.0                          # 第二種算法：逐月迴圈 + 二分法
    for _ in range(80):
        mid = (lo + hi) / 2
        if loop(stop2, lambda i, s=start, x=mid: x if i >= s else 0.0) < A: lo = mid
        else: hi = mid
    close(e, (lo + hi) / 2, 1e-9)
    close(loop(stop2, lambda i, s=start: e if i >= s else 0.0), A, 1e-6)
    catch.append((y0, n_left // 12, e * 1e4, e * n_left))
E13 = catch[0][2]
assert round(E13) * 1e-4 * fv(N - 144) >= GAP   # 取整後的每月金額確實追得平
print("T1 A", round(A, 1), "B", round(B, 1), "gap", round(GAP, 1), "catch", [(y, n, round(e), round(p, 1)) for y, n, e, p in catch])

# ---------- 題材 2：停扣時把錢存著 vs 花掉 ----------
ML_ = 1.015 ** (1 / 12) - 1                    # 活存年息 1.5%，按月複利
SAV = fv(24, ML_)
s_loop = 0.0
for _ in range(24):
    s_loop = s_loop * (1 + ML_) + 1.0
close(SAV, s_loop)
SAV30 = SAV * (1 + M) ** (N - 144)            # 第 12 年底一次投入，再滾 216 個月
b_loop = 0.0                                   # 逐月迴圈：第 144 月底把活存一次投入
for i in range(1, N + 1):
    b_loop *= 1 + M
    if not stop2(i): b_loop += 1.0
    if i == 144: b_loop += s_loop
KEEP = B + SAV30
close(KEEP, b_loop)
SPEND = B
print("T2 sav", round(SAV, 2), "keep", round(KEEP, 1), "spend", round(SPEND, 1), "diff", round(KEEP - SPEND, 1), "vsA", round(A - KEEP, 1))
assert round(A, 1) - round(KEEP, 1) == round(A - KEEP, 1) or abs((round(A, 1) - round(KEEP, 1)) - (A - KEEP)) < 0.06

# ---------- 題材 3：連續停 2 年 vs 分散停 24 個月 ----------
spread = lambda i: i <= 288 and i % 12 == 0    # 第 1–24 年，每年第 12 個月不投
C = loop(spread)
close(C, fv(N) - sum((1 + M) ** (N - 12 * k) for k in range(1, 25)))
assert sum(1 for i in range(1, N + 1) if spread(i)) == 24 == sum(1 for i in range(1, N + 1) if stop2(i))
G_CONT, G_SPREAD = A - B, A - C
print("T3 cont", round(G_CONT, 1), "spread", round(G_SPREAD, 1), "C", round(C, 1))


def sq(y, hol_from=0, hol_to=0, sz=15):
    xl, xr = ML + 8, MR - 8; step = (xr - xl) / 29
    for c in range(30):
        cx = xl + c * step
        box = [(cx - sz / 2) * S, (y - sz / 2) * S, (cx + sz / 2) * S, (y + sz / 2) * S]
        if hol_from <= c < hol_to: ns.d.rectangle(box, outline=hexc(VERM), width=int(2 * S))
        else: ns.d.rectangle(box, fill=hexc(INK))


# ===== 1. catchup 輪播：停了之後，要補多少 =====
o = f"{OUT}/catchup"; SD = "MONEY　補回來"; T = 5


def rows1():
    for k, (lab, hf, ht) in enumerate((("一直投", 0, 0), ("第 11 年停 2 年，第 13 年恢復", 10, 12))):
        y = 930 + k * 110
        ttext(ML, y - 58, lab, font(SANS_R, 26), INK if k == 0 else GRAY, 3); sq(y, hf, ht)


fl.cover(o, "s1.png", 1, T, SD, "金錢日誌　停扣之後", "停了 2 年，", "每月要補多少", "答案在第 3 張。",
         "目標：第 30 年追平一直投的人。", [BASE, FAIL], rows=rows1)
fl.bars(o, "s2.png", 2, T, SD, "先看缺口", f"停 2 年，終點少 {GAP:.1f} 萬。",
        [("一直投", "30 年不停", A), ("第 11 年停 2 年", "少投 24 萬", B)], "萬", "{:.1f}",
        "條長度從 0 起算，單位：萬", [BASE, FAIL], hi=1, y0=470, rowh=250)
y0, ny, e, p = catch[0]
fl.big(o, "s3.png", 3, T, SD, "第 13 年恢復後，每月要多投", f"{e:,.0f}", "元",
       f"多投 {ny} 年，第 30 年剛好追平。", f"多投的本金共 {p:.1f} 萬，比少投的 24 萬還多。", [BASE, FAIL])
fl.table(o, "s4.png", 4, T, SD, "越晚補，越貴", f"追平 {A:.1f} 萬，每月要多投",
         ["開始補", "補幾年", "每月多投"], [[f"第 {y} 年", f"{n} 年", f"{e:,.0f} 元"] for y, n, e, _ in catch],
         "多投本金：" + "／".join(f"{p:.1f} 萬" for *_, p in catch) + "（依序）", [BASE, FAIL], rowh=120)
fl.text(o, "s5.png", 5, T, SD, [("補得回來，", SERIF_L, 72, INK, 7, 260), ("但越早越便宜。", SERIF_M, 72, VERM, 7, 360),
        ("__rule__", 0, 0, 0, 0, 520),
        ("停多久、從哪年補、每月補多少，", SANS_R, 34, INK, 5, 570),
        ("主頁連結有免費試算", SANS_R, 34, INK, 5, 640),
        ("和「停扣成本速查表」。連結在主頁。", SANS_R, 34, INK, 5, 700),
        ("存起來，恢復扣款那天算一次。", SERIF_M, 44, INK, 5, 840)], [BASE, FAIL])

# ===== 2. savekeep 輪播：停扣時把錢存著 vs 花掉 =====
o = f"{OUT}/savekeep"; SD = "MONEY　錢去哪"; T = 5
fl.cover(o, "s1.png", 1, T, SD, "金錢日誌　停扣的那 2 年", "停扣 2 年的錢，", "存著或花掉", "答案在第 3 張。",
         "同樣停 2 年，只差在那 24 萬去哪。", [BASE, FAIL])
fl.text(o, "s2.png", 2, T, SD, [("同樣停 2 年，", SERIF_L, 66, INK, 6, 200), ("錢去哪不一樣。", SERIF_M, 66, INK, 6, 290),
        ("__rule__", 0, 0, 0, 0, 440),
        ("A　一直投，30 年不停", SANS_R, 36, INK, 5, 480),
        ("B　第 11 年停 2 年，每月 1 萬存活存，", SANS_R, 36, INK, 5, 580),
        ("\u3000  第 13 年初一次投回", SANS_R, 36, INK, 5, 640),
        ("C　第 11 年停 2 年，錢花掉", SANS_R, 36, INK, 5, 740),
        ("活存年息 1.5%，按月複利。", SANS_L, 30, GRAY, 4, 860)], [BASE, FAIL], seal_xy=None)
fl.bars(o, "s3.png", 3, T, SD, "第 30 年，三個人", "存著的人，幾乎追平。",
        [("A　一直投", "", A), ("B　停 2 年，錢存著", "第 13 年初投回", KEEP), ("C　停 2 年，錢花掉", "", SPEND)],
        "萬", "{:.1f}", "條長度從 0 起算，單位：萬", [BASE, FAIL], hi=1)
fl.big(o, "s4.png", 4, T, SD, "存著 vs 花掉，第 30 年差", f"{KEEP - SPEND:.1f}", "萬",
       f"存下的 24 萬，活存 2 年變 {SAV:.1f} 萬，", f"投回後再滾 18 年，變成 {SAV30:.1f} 萬。", [BASE, FAIL])
fl.text(o, "s5.png", 5, T, SD, [("停扣，", SERIF_L, 72, INK, 7, 260), ("不等於停存。", SERIF_M, 72, VERM, 7, 360),
        ("__rule__", 0, 0, 0, 0, 520),
        ("活存利率、停多久、何時投回，", SANS_R, 34, INK, 5, 570),
        ("主頁連結有免費試算和速查表，", SANS_R, 34, INK, 5, 640),
        ("複利帳本可逐月記錄。連結在主頁。", SANS_R, 34, INK, 5, 700),
        ("存起來，想停扣時先看一次。", SERIF_M, 44, INK, 5, 840)], [BASE, FAIL])

# ===== 3. spread 單圖：連續停 vs 分散停 =====
fl.bars(f"{OUT}/spread", "single.png", 0, 0, "MONEY　怎麼停", "同樣少投 24 個月", "停多久，比怎麼停重要。",
        [("連續停 24 個月", "第 11–12 年", G_CONT), ("分散停 24 個月", "第 1–24 年，每年 12 月", G_SPREAD)],
        "萬", "{:.1f}", f"和一直投（{A:.1f} 萬）相比，第 30 年少的金額。條長從 0 起算。", [BASE, FAIL],
        label="MONEY No.11", y0=470, rowh=250)
print("ok")
