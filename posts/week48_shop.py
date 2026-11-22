"""2026 W48（11/23–11/27）商店導流貼文：輪播 2、單圖 1。用法：python3 -I posts/week48_shop.py OUTDIR
數字全部由程式計算；基準：每月 1 萬、年化 6%、按月複利、先計息再投入、30 年＝974.5 萬。
每個數字都用「封閉公式」與「逐月迴圈」兩種算法 assert 互相驗算。"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "style"))
import noirxu_style as ns
from noirxu_style import *
import feed_lib as fl

OUT = sys.argv[1]
N = 360
FAIL = "報酬更低或中斷更久，結果會不同。"


def mrate(a):
    return (1 + a) ** (1 / 12) - 1


def fv(n, a=0.06, p=1.0):
    """封閉公式：每月期末投入 p（萬）、共 n 期的終值。"""
    m = mrate(a)
    return p * ((1 + m) ** n - 1) / m


def loop(n, a=0.06, p=1.0):
    """逐月迴圈：先計息再投入。"""
    m, b = mrate(a), 0.0
    for _ in range(n):
        b = b * (1 + m) + p
    return b


def months_closed(T, a, p):
    """封閉公式反解：終值第一次 ≥ T 的月份。"""
    m = mrate(a)
    return math.ceil(math.log(1 + T * m / p) / math.log(1 + m) - 1e-12)


def months_loop(T, a, p):
    """逐月迴圈：一個月一個月加，第一次 ≥ T 的月份。"""
    m, b, i = mrate(a), 0.0, 0
    while b < T:
        i += 1
        b = b * (1 + m) + p
    return i


def close(a, b, tol=1e-6):
    assert abs(a - b) < tol, (a, b)


# ---------- 基準 ----------
A = loop(N)
close(A, fv(N))
assert abs(A - 974.5) < 0.05, A

# ---------- 題材 1：20、30、40 歲開始，到 60 歲（單圖） ----------
AGES = []
for age in (20, 30, 40):
    n = (60 - age) * 12
    v = fv(n); close(v, loop(n))
    AGES.append((age, n // 12, n * 1.0, v))
assert abs(AGES[1][3] - A) < 1e-9
RATIO = AGES[0][3] / AGES[2][3]
print("T1", [(a, y, p, round(v, 1)) for a, y, p, v in AGES], "ratio", round(RATIO, 2))

# ---------- 題材 2：到 1000 萬要多久（輪播） ----------
PM, RT = (1, 2, 3), (0.04, 0.06, 0.08)
GRID = {}
for p in PM:
    for a in RT:
        n = months_closed(1000, a, p)
        assert n == months_loop(1000, a, p), (p, a)
        assert fv(n, a, p) >= 1000 > fv(n - 1, a, p)
        GRID[(p, a)] = n
Y = {k: v / 12 for k, v in GRID.items()}
assert fv(360) < 1000 and GRID[(1, 0.06)] > 360          # 30 年 974.5 萬，還差一點
SAVE2X = Y[(1, 0.06)] - Y[(2, 0.06)]
SAVE8 = Y[(1, 0.06)] - Y[(1, 0.08)]
# 圖上顯示的四捨五入數字相減，要和直接算的一致
assert round(round(Y[(1, 0.06)], 1) - round(Y[(2, 0.06)], 1), 1) == round(SAVE2X, 1)
print("T2", {f"{p}萬@{a:.0%}": (n, round(n / 12, 1)) for (p, a), n in GRID.items()}, "2x", round(SAVE2X, 1), "8%", round(SAVE8, 1))

# ---------- 題材 3：月投 5,000 也算數（輪播） ----------
P5 = 0.5
F5 = fv(N, p=P5); close(F5, loop(N, p=P5)); close(F5, A / 2)
PR5 = P5 * N
MS = {T: months_closed(T, 0.06, P5) for T in (50, 100, 200, 300, 400)}
for T, n in MS.items():
    assert n == months_loop(T, 0.06, P5), T
MS_ROWS = []
prev = 0
for T in (100, 200, 300, 400):
    MS_ROWS.append((T, MS[T], MS[T] - prev)); prev = MS[T]
assert all(MS_ROWS[i][2] > MS_ROWS[i + 1][2] for i in range(3))   # 每 100 萬越來越快
print("T3 fv", round(F5, 1), "principal", PR5, "ms", MS, "rows", MS_ROWS)


# ===== 1. to1000 輪播：到 1000 萬要多久 =====
o = f"{OUT}/to1000"; SD = "MONEY　一千萬"; T = 5
B2 = "月投 1–3 萬　年化 4／6／8%　按月複利　先計息再投入　情境試算，非投資建議"
fl.cover(o, "s1.png", 1, T, SD, "金錢日誌　目標 1,000 萬", "存到 1,000 萬，", "要多久", "完整 9 格在第 3 張。",
         f"每月 1 萬、年化 6%，30 年是 {A:.1f} 萬。", [B2, FAIL])
fl.bars(o, "s2.png", 2, T, SD, "年化 6%，月投不同", "月投越多越快，但不是倍數。",
        [(f"月投 {p} 萬", f"第 {GRID[(p, 0.06)]} 個月達成", Y[(p, 0.06)]) for p in PM], "年", "{:.1f}",
        "條長度從 0 起算，單位：年（達成月數 ÷ 12）", [B2, FAIL], hi=0)
fl.table(o, "s3.png", 3, T, SD, "月投 × 年化報酬", "到 1,000 萬要幾年",
         ["月投", "年化 4%", "年化 6%", "年化 8%"],
         [[f"{p} 萬"] + [f"{Y[(p, a)]:.1f} 年" for a in RT] for p in PM],
         "達成月數 ÷ 12，取到小數一位。", [B2, FAIL], rowh=120)
fl.big(o, "s4.png", 4, T, SD, "年化 6%，月投從 1 萬加倍到 2 萬，只快", f"{SAVE2X:.1f}", "年",
       f"從 {Y[(1, 0.06)]:.1f} 年變 {Y[(2, 0.06)]:.1f} 年，不是減半。", "月投能縮短時間，但時間仍是複利的主角。", [B2, FAIL])
fl.text(o, "s5.png", 5, T, SD, [("1,000 萬，", SERIF_L, 72, INK, 7, 260), ("先看你在哪一格。", SERIF_M, 72, VERM, 7, 360),
        ("__rule__", 0, 0, 0, 0, 520),
        ("換成你的月投、報酬、目標金額，", SANS_R, 34, INK, 5, 570),
        ("主頁連結有免費試算和速查表，", SANS_R, 34, INK, 5, 640),
        ("複利帳本能看每個里程碑在哪個月。", SANS_R, 34, INK, 5, 700),
        ("存起來，設目標前先算一次。連結在主頁。", SERIF_M, 40, INK, 4, 840)], [B2, FAIL])

# ===== 2. ages 單圖：20、30、40 歲開始，到 60 歲 =====
B1 = "每月投入 1 萬　年化 6%　按月複利　先計息再投入　情境試算，非投資建議"
fl.table(f"{OUT}/ages", "single.png", 0, 0, "MONEY　起點", "每月 1 萬，年化 6%，都到 60 歲", "幾歲開始，差多少？",
         ["開始", "投入", "本金", "60 歲終值"],
         [[f"{a} 歲", f"{y} 年", f"{p:.0f} 萬", f"{v:,.1f} 萬"] for a, y, p, v in AGES],
         f"20 歲開始的本金是 40 歲的 2 倍，終值是 {RATIO:.1f} 倍。", [B1, FAIL], label="MONEY No.12", hi_row=0, rowh=120)

# ===== 3. m5000 輪播：月投 5,000 也算數 =====
o = f"{OUT}/m5000"; SD = "MONEY　小錢"; T = 5
B3 = "每月投入 5,000 元　年化 6%　按月複利　先計息再投入　情境試算，非投資建議"
fl.cover(o, "s1.png", 1, T, SD, "金錢日誌　月投 5,000", "月投 5,000 元，", "多久到 100 萬", "答案在第 3 張。",
         "不是 1 萬，也不是 0。", [B3, FAIL])
fl.bars(o, "s2.png", 2, T, SD, "30 年後", f"5,000 元，30 年後 {F5:.1f} 萬。",
        [("不投", "", 0.0), ("月投 5,000　本金", "30 年", PR5), ("月投 5,000　終值", "30 年", F5)],
        "萬", "{:.1f}", "條長度從 0 起算，單位：萬", [B3, FAIL], hi=2)
fl.big(o, "s3.png", 3, T, SD, "月投 5,000，第一個 100 萬在第", f"{MS[100]}", "個月",
       f"約 {MS[100] / 12:.1f} 年；這時本金是 {MS[100] * P5:.1f} 萬。", f"第一個 50 萬，在第 {MS[50]} 個月。", [B3, FAIL])
fl.table(o, "s4.png", 4, T, SD, "之後越來越快", "每多 100 萬，要幾個月",
         ["里程碑", "達成月份", "距上一個"], [[f"{t} 萬", f"第 {n} 月", f"{g} 個月"] for t, n, g in MS_ROWS],
         "第一個 100 萬最慢，之後每 100 萬越來越快。", [B3, FAIL], rowh=110)
fl.text(o, "s5.png", 5, T, SD, [("第一個 100 萬，", SERIF_L, 72, INK, 7, 260), ("最難也最重要。", SERIF_M, 72, VERM, 7, 360),
        ("__rule__", 0, 0, 0, 0, 520),
        ("月投多少都算數，先開始再調高。", SANS_R, 34, INK, 5, 570),
        ("主頁連結有免費試算和速查表，", SANS_R, 34, INK, 5, 640),
        ("複利帳本能標出你的每個里程碑。", SANS_R, 34, INK, 5, 700),
        ("存起來，覺得錢太少時看一次。連結在主頁。", SERIF_M, 40, INK, 4, 840)], [B3, FAIL])
print("ok")
