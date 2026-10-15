"""第一週晚間 Reel 四支。用法：python3 -I reels_week1.py OUTDIR"""
import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
from reel_lib import *
OUT = sys.argv[1]

def fv(n, a=0.06, pmt=1.0):
    m = (1 + a) ** (1 / 12) - 1
    return pmt * ((1 + m) ** n - 1) / m
def fv_raise(rate=0.03, a=0.06):
    m = (1 + a) ** (1 / 12) - 1; b = 0.0
    for i in range(360):
        b = b * (1 + m) + (1 + rate) ** (i // 12)
    return b
def months_to(t, a=0.06):
    m = (1 + a) ** (1 / 12) - 1; b = 0.0; i = 0
    while b < t: i += 1; b = b * (1 + m) + 1.0
    return i

# ---------- R1 通膨 ----------
infl = [(f"{y} 年後" if y else "現在", "購買力", 100 / 1.02 ** y) for y in (0, 10, 20, 30)]
print("R1", [round(v, 1) for _, _, v in infl])
S = "MONEY　通膨"
build([
    (text_scene(S, [("放在抽屜的 100 萬，", SERIF_M, 64, INK, 6, 0), ("30 年後，", SERIF_L, 120, INK, 6, 110),
                    ([("還值多少", INK), ("？", VERM)], SERIF_M, 70, INK, 6, 190)], seal=True), 2.8),
    (anim(lambda k: bars_scene(S, ["同樣是 100 萬，", "購買力一路縮水。"], infl, "萬", k, "{:.1f}", "假設年通膨 2%", hi=3), 54), 5.2),
    (bignum_scene(S, "30 年後", f"{infl[3][2]:.1f}", "萬", "購買力只剩一半多。", "不是錢少了，是東西變貴。"), 3.6),
    (text_scene(S, [("錢放著不動，", SERIF_M, 64, INK, 6, 0), ("也是一種選擇。", SERIF_M, 64, INK, 6, 110),
                    ("只是它有成本。", SERIF_L, 80, VERM, 6, 130)], rule=1000), 3.2),
    (text_scene(S, [("傳給還在猶豫", SERIF_M, 72, INK, 8, 0), ("要不要動錢的人。", SERIF_M, 72, INK, 8, 120)], seal=True,
                foot="假設年通膨 2%，實際會不同。情境試算，非投資建議。"), 3.0),
], OUT, "r1_inflation")

# ---------- R2 小額加碼 ----------
f10, f11, f12 = fv(360, pmt=1.0), fv(360, pmt=1.1), fv(360, pmt=1.2)
d = f11 - f10; print("R2", round(f10, 1), round(f11, 1), round(f12, 1), round(d, 1), round(d - 36, 1))
S = "MONEY　小額加碼"
build([
    (text_scene(S, [("每月多存 1,000 元，", SERIF_M, 64, INK, 6, 0), ("30 年後，", SERIF_L, 120, INK, 6, 110),
                    ([("會差多少", INK), ("？", VERM)], SERIF_M, 70, INK, 6, 190)], seal=True), 2.8),
    (anim(lambda k: bars_scene(S, ["每月多一點，", "終點多一截。"], [("每月 1.0 萬", "", f10), ("每月 1.1 萬", "", f11), ("每月 1.2 萬", "", f12)],
                               "萬", k, "{:.1f}", "年化 6%　30 年　按月複利", hi=1), 54), 5.2),
    (bignum_scene(S, "每月多 1,000，多了", f"{d:.1f}", "萬", "多投入的本金，只有 36 萬。", f"其餘 {d-36:.1f} 萬，是複利。"), 3.6),
    (text_scene(S, [("小額加碼，", SERIF_M, 64, INK, 6, 0), ("也會被時間放大。", SERIF_L, 80, VERM, 6, 130)], rule=900), 3.0),
    (text_scene(S, [("傳給想先從", SERIF_M, 72, INK, 8, 0), ("小額開始的人。", SERIF_M, 72, INK, 8, 120)], seal=True,
                foot="情境試算，非投資建議。報酬更低或中斷更久，結果會不同。"), 3.0),
], OUT, "r2_topup")

# ---------- R3 里程碑 ----------
m1, m2, m3 = months_to(100), months_to(200), months_to(300)
legs = [("第 1 個 100 萬", f"{m1/12:.1f} 年", m1), ("100 → 200 萬", f"{(m2-m1)/12:.1f} 年", m2 - m1), ("200 → 300 萬", f"{(m3-m2)/12:.1f} 年", m3 - m2)]
print("R3", legs)
S = "MONEY　里程碑"
build([
    (text_scene(S, [("每月存 1 萬，", SERIF_M, 64, INK, 6, 0), ("第 1 個 100 萬，", SERIF_L, 100, INK, 6, 110),
                    ([("要存幾個月", INK), ("？", VERM)], SERIF_M, 70, INK, 6, 170)], seal=True), 2.8),
    (anim(lambda k: bars_scene(S, ["每多一個 100 萬，", "都更快。"], legs, "個月", k, "{:.0f}", "年化 6%　按月複利", hi=0), 54), 5.2),
    (bignum_scene(S, "從", f"{m1} → {m3-m2}", "個月", "最難的是第一段。", "後面，複利開始幫你。"), 3.6),
    (text_scene(S, [("前面最慢，", SERIF_M, 80, INK, 8, 0), ("後面加速。", SERIF_L, 100, VERM, 8, 140)], rule=1000), 3.0),
    (text_scene(S, [("傳給快放棄的人。", SERIF_M, 72, INK, 8, 0), ("存起來，想放棄時看一次。", SANS_R, 34, GRAY, 4, 130)], seal=True,
                foot="情境試算，非投資建議。實際報酬會波動，時間會不同。"), 3.0),
], OUT, "r3_milestone")

# ---------- R4 每年調高月投 ----------
fr = fv_raise(); dr = fr - f10
print("R4", round(f10, 1), round(fr, 1), round(dr, 1))
S = "MONEY　每年調高"
build([
    (text_scene(S, [("每年把月投，", SERIF_M, 64, INK, 6, 0), ("調高 3%，", SERIF_L, 120, INK, 6, 110),
                    ([("30 年差多少", INK), ("？", VERM)], SERIF_M, 70, INK, 6, 190)], seal=True), 2.8),
    (anim(lambda k: bars_scene(S, ["第 1 年 1 萬，", "之後每年多 3%。"], [("固定每月 1 萬", "", f10), ("每年調高 3%", "", fr)],
                               "萬", k, "{:.1f}", "年化 6%　30 年　按月複利", hi=1), 54), 5.2),
    (bignum_scene(S, "終點多了", f"{dr:.1f}", "萬", "每年只多一點點，", "30 年後是一大段。"), 3.6),
    (text_scene(S, [("一次小調整，", SERIF_M, 64, INK, 6, 0), ("比一次大決心，", SERIF_M, 64, INK, 6, 110),
                    ("更容易做到。", SERIF_L, 80, VERM, 6, 130)], rule=1000), 3.2),
    (text_scene(S, [("傳給剛加薪的人。", SERIF_M, 72, INK, 8, 0)], seal=True,
                foot="假設月投每年調高 3%。情境試算，非投資建議。報酬更低結果會不同。"), 2.8),
], OUT, "r4_raise")
