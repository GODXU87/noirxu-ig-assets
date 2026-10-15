"""10/23–10/30 晚間 Reel 五支。用法：python3 -I week2_reels.py OUTDIR"""
import sys, math
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
from reel_lib import *
OUT = sys.argv[1]
def fv(n, a=0.06, pmt=1.0):
    m = (1 + a) ** (1 / 12) - 1
    return pmt * ((1 + m) ** n - 1) / m
A = fv(360)
Q = lambda parts, sz=70: (parts, SERIF_M, sz, INK, 6)

def hook(S, l1, big, l3):
    return text_scene(S, [(l1, SERIF_M, 64, INK, 6, 0), (big, SERIF_L, 110, INK, 6, 110), ([(l3, INK), ("？", VERM)], SERIF_M, 70, INK, 6, 180)], seal=True)
def closing(S, a, b, foot):
    return text_scene(S, [(a, SERIF_M, 72, INK, 8, 0), (b, SERIF_M, 72, INK, 8, 120)], seal=True, foot=foot)

# R5 72 法則
dbl = [(f"年化 {r}%", f"72÷{r}＝{72/r:.0f}", math.log(2) / math.log(1 + r / 100)) for r in (4, 6, 8)]
print("R5", [round(v, 2) for _, _, v in dbl])
S = "MONEY　72 法則"
build([(hook(S, "本金想翻一倍，", "要幾年", ""), 2.8) if False else
       (text_scene(S, [("本金想翻一倍，", SERIF_M, 64, INK, 6, 0), ([("要幾年", INK), ("？", VERM)], SERIF_L, 120, INK, 6, 110)] , seal=True), 2.6),
       (anim(lambda k: bars_scene(S, ["年化越高，", "翻倍越快。"], dbl, "年", k, "{:.1f}", "按年複利", hi=1), 54), 5.2),
       (bignum_scene(S, "年化 6%", f"{dbl[1][2]:.1f}", "年", "本金翻倍，約 12 年。", "72 ÷ 6 ＝ 12，粗估很準。"), 3.6),
       (text_scene(S, [("72 ÷ 年化報酬，", SERIF_M, 64, INK, 6, 0), ("就是翻倍的年數。", SERIF_L, 80, VERM, 6, 130)], rule=900), 3.2),
       (closing(S, "傳給想知道", "多快的人。", "按年複利的粗估。情境試算，非投資建議。"), 2.8)], OUT, "r5_rule72")

# R6 購買力
real = A / 1.02 ** 30
print("R6", round(real, 1))
S = "MONEY　購買力"
build([(hook(S, "存了 30 年的 974.5 萬，", "購買力", "還剩多少"), 2.8),
       (anim(lambda k: bars_scene(S, ["數字會變大，", "東西也會變貴。"], [("帳面金額", "", A), ("扣掉通膨後", "購買力", real)], "萬", k, "{:.1f}", "年通膨 2%　以現在的幣值換算", hi=1), 54), 5.2),
       (bignum_scene(S, "30 年後的購買力", f"{real:.1f}", "萬", "物價約為現在的 1.81 倍。", "帳面 974.5 萬，只買得到這麼多。"), 3.6),
       (text_scene(S, [("看報酬，", SERIF_M, 64, INK, 6, 0), ("也要看通膨。", SERIF_L, 80, VERM, 6, 130)], rule=900), 3.0),
       (closing(S, "傳給只看", "帳面數字的人。", "每月 1 萬　年化 6%　年通膨 2%。情境試算，非投資建議。"), 3.0)], OUT, "r6_real")

# R7 每天 100 元
d = [(f"{y} 年", f"本金 {0.3*12*y:.0f} 萬", 0.3 * fv(12 * y)) for y in (10, 20, 30)]
print("R7", [round(v, 1) for _, _, v in d])
S = "MONEY　日常"
build([(hook(S, "每天少花 100 元，", "30 年後", "會變多少"), 2.8),
       (anim(lambda k: bars_scene(S, ["每月 3,000 元，", "時間越久越多。"], d, "萬", k, "{:.1f}", "年化 6%　按月複利", hi=2), 54), 5.2),
       (bignum_scene(S, "30 年後", f"{d[2][2]:.1f}", "萬", "本金只有 108 萬，", f"其餘 {d[2][2]-108:.1f} 萬，是複利。"), 3.6),
       (text_scene(S, [("小小的日常，", SERIF_M, 64, INK, 6, 0), ("也會被時間放大。", SERIF_L, 80, VERM, 6, 130)], rule=900), 3.0),
       (closing(S, "傳給每天", "都在買飲料的人。", "每天 100 元以每月 3,000 元計。情境試算，非投資建議。"), 3.0)], OUT, "r7_daily")

# R8 平均報酬
fin = [100 * 1.06 ** 30, 100 * (1.3 * 0.82) ** 15, 100 * (1.2 * 0.92) ** 15]
gb = ((1.3 * 0.82) ** 0.5 - 1) * 100
print("R8", [round(x, 1) for x in fin], round(gb, 2))
S = "MONEY　平均報酬"
build([(text_scene(S, [("平均報酬都是 6%，", SERIF_M, 64, INK, 6, 0), ("30 年後", SERIF_L, 110, INK, 6, 110), ([("一樣嗎", INK), ("？", VERM)], SERIF_M, 70, INK, 6, 180)], seal=True), 2.8),
       (anim(lambda k: bars_scene(S, ["一次投入 100 萬，", "終點差很多。"], [("A 每年 +6%", "穩定", fin[0]), ("B +30%／−18%", "波動大", fin[1]), ("C +20%／−8%", "波動中", fin[2])], "萬", k, "{:.1f}", "一次投入、不再加碼", hi=1), 54), 5.6),
       (bignum_scene(S, "B 的實際年化", f"{gb:.2f}", "%", "平均 6%，實際只剩 3.25%。", "波動越大，實際年化越低。"), 3.6),
       (text_scene(S, [("看報酬，", SERIF_M, 64, INK, 6, 0), ("別只看平均。", SERIF_L, 80, VERM, 6, 130)], rule=900), 3.0),
       (closing(S, "傳給只看", "平均報酬的人。", "簡化情境，非預測。情境試算，非投資建議。"), 3.0)], OUT, "r8_average")

# R9 月領 5 萬
need = 5 * 12 / 0.04
pm = {y: need / fv(12 * y) for y in (20, 30, 40)}
print("R9", need, {k: round(v, 2) for k, v in pm.items()})
S = "MONEY　退休金"
build([(text_scene(S, [("想每月領 5 萬，", SERIF_M, 64, INK, 6, 0), ("要先存", SERIF_L, 110, INK, 6, 110), ([("多少", INK), ("？", VERM)], SERIF_M, 70, INK, 6, 170)], seal=True), 2.8),
       (text_scene(S, [("一年 60 萬，", SERIF_M, 60, INK, 6, 0), ("÷ 4% 提領率", SERIF_M, 60, INK, 6, 100), (f"＝ {need:,.0f} 萬", SERIF_L, 120, VERM, 4, 180),
                       ("4% 是常見經驗法則，不是保證。", SANS_L, 28, GRAY, 3, 200)], rule=None), 3.8),
       (bignum_scene(S, "30 年存到 1,500 萬", f"{pm[30]:.2f}", "萬／月", "每月要投 1.54 萬。", "年化 6%、按月複利。"), 3.4),
       (anim(lambda k: bars_scene(S, ["越早開始，", "每月越輕。"], [("20 年", "", pm[20]), ("30 年", "", pm[30]), ("40 年", "", pm[40])], "萬／月", k, "{:.2f}", "存到 1,500 萬所需月投", hi=2), 54), 5.0),
       (closing(S, "傳給在想", "「退休要多少」的人。", "4% 為經驗法則，不保證；未計通膨稅費。非投資建議。"), 3.0)], OUT, "r9_retire")
