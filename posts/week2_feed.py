"""10/23–10/31 主貼文（輪播 3、單圖 6）。用法：python3 -I week2_feed.py OUTDIR"""
import sys, math
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import *
import feed_lib as fl
OUT = sys.argv[1]
def fv(n, a=0.06, pmt=1.0):
    m = (1 + a) ** (1 / 12) - 1
    return pmt * ((1 + m) ** n - 1) / m
A = fv(360)
BASE = "每月投入 1 萬　年化 6%　按月複利　情境試算，非投資建議"
FAIL = "報酬更低或中斷更久，結果會不同。"
def sq(y, hol_from=0, hol_to=0, sz=15):
    xl, xr = ML + 8, MR - 8; step = (xr - xl) / 29
    for c in range(30):
        cx = xl + c * step
        box = [(cx - sz / 2) * S, (y - sz / 2) * S, (cx + sz / 2) * S, (y + sz / 2) * S]
        if hol_from <= c < hol_to: ns.d.rectangle(box, outline=hexc(VERM), width=int(2 * S))
        else: ns.d.rectangle(box, fill=hexc(INK))

# ===== p10 輪播：本金一樣，早晚差多少 =====
o = f"{OUT}/p10"; SD = "MONEY　早晚"; T = 5
B15 = fv(180, pmt=2.0); gap = A - B15
print("p10", round(A, 1), round(B15, 1), round(gap, 1))
def rows10():
    for k, (lab, hf, ht) in enumerate((("A", 0, 0), ("B", 0, 15))):
        y = 930 + k * 110
        ttext(ML, y - 56, lab, font(SERIF_L, 34), VERM, 0); sq(y, hf, ht)
fl.cover(o, "s1.png", 1, T, SD, "本金一樣，都是 360 萬", "同樣投入 360 萬，", "早晚差多少", "答案在第 3 張。", "兩個人，只有「開始的時間」不同。",
         [BASE, FAIL], rows=rows10)
new_slide(PAPER); frame(2, T, side=SD)
ttext(ML, 170, "兩個人", font(SANS_R, 26), VERM, 6); ttext(ML, 225, "投入一樣多的錢。", font(SERIF_L, 70), INK, 5)
ttext(ML, 330, "一個方格 ＝ 1 年，空心 ＝ 還沒開始投的年份。", font(SANS_L, 26), GRAY, 3)
for k, (lab, t1, t2, hf, ht) in enumerate((("A", "現在開始，每月 1 萬", "投 30 年，本金 360 萬", 0, 0), ("B", "15 年後才開始，每月 2 萬", "投 15 年，本金 360 萬", 0, 15))):
    y = 560 + k * 270
    hline(ML, MR, y - 70, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y - 44, lab, font(SERIF_L, 56), VERM, 0); ttext(ML + 72, y - 40, t1, font(SANS_R, 32), INK, 4)
    ttext(ML + 72, y + 8, t2, font(SANS_L, 26), GRAY, 3); sq(y + 100, hf, ht, 17)
hline(ML, MR, 560 + 2 * 270 - 70, INK, 1.2)
fl.foot([BASE])
save(o, "s2.png")
fl.bars(o, "s3.png", 3, T, SD, "同一天，終點", "本金一樣，終點差很多。", [("A　現在開始", "每月 1 萬 × 30 年", A), ("B　15 年後開始", "每月 2 萬 × 15 年", B15)],
        "萬", "{:.1f}", "條長度從 0 起算，單位：萬", [BASE, FAIL], hi=1, y0=470, rowh=250)
fl.big(o, "s4.png", 4, T, SD, "同樣的 360 萬，早 15 年投", f"{gap:.1f}", "萬", "終點多出這一段，不是你多存的。", "是時間給的。", [BASE, FAIL])
fl.text(o, "s5.png", 5, T, SD, [("本金可以補，", SERIF_L, 72, INK, 7, 300), ("時間補不回。", SERIF_M, 72, VERM, 7, 400), ("__rule__", 0, 0, 0, 0, 560),
        ("加倍月投，也追不上早開始。", SANS_R, 34, INK, 5, 600), ("傳給覺得「等有錢再投」的人。", SERIF_M, 46, INK, 5, 800),
        ("存起來，想拖延時看一次。", SANS_L, 30, GRAY, 4, 870)], [BASE, FAIL])

# ===== p11 單圖：月薪存多少比例 =====
sal = [("存 10%", "每月 0.5 萬", 0.5 * A), ("存 20%", "每月 1.0 萬", 1.0 * A), ("存 30%", "每月 1.5 萬", 1.5 * A)]
print("p11", [round(v, 1) for _, _, v in sal])
fl.bars(f"{OUT}/p11", "single.png", 0, 0, "MONEY　存多少", "月薪 5 萬，30 年", "月薪 5 萬，存多少比例？", sal, "萬", "{:.1f}",
        "條長度從 0 起算，單位：萬", ["月薪固定 5 萬、不調薪　年化 6%　按月複利　情境試算，非投資建議", FAIL], hi=2, label="MONEY No.05")

# ===== p12 輪播：平均報酬陷阱 =====
o = f"{OUT}/p12"; SD = "MONEY　平均報酬"; T = 5
fin = [100 * 1.06 ** 30, 100 * (1.3 * 0.82) ** 15, 100 * (1.2 * 0.92) ** 15]
g_b, g_c = ((1.3 * 0.82) ** 0.5 - 1) * 100, ((1.2 * 0.92) ** 0.5 - 1) * 100
print("p12", [round(x, 1) for x in fin], round(g_b, 2), round(g_c, 2))
def rows12():
    for k, t in enumerate(("A　每年 +6%", "B　+30% 與 −18% 交替", "C　+20% 與 −8% 交替")):
        ttext(ML, 920 + k * 90, t, font(SANS_R, 32), INK, 4)
fl.cover(o, "s1.png", 1, T, SD, "平均報酬都是 6%", "一次投入 100 萬，", "30 年後一樣嗎", "答案在第 3 張。", "三種走法，算術平均都是 6%。",
         ["一次投入 100 萬、不再加碼　每年報酬依規律固定　簡化情境，非預測", "情境試算，非投資建議。"], rows=rows12)
fl.text(o, "s2.png", 2, T, SD, [("平均都是 6%，", SERIF_L, 66, INK, 6, 200), ("路徑不同。", SERIF_M, 66, INK, 6, 290), ("__rule__", 0, 0, 0, 0, 440),
        ("A　每年 +6%", SANS_R, 36, INK, 5, 480), ("B　+30%、−18%、+30%、−18%……", SANS_R, 36, INK, 5, 580),
        ("C　+20%、−8%、+20%、−8%……", SANS_R, 36, INK, 5, 680), ("三種的算術平均，都是 6%。", SANS_L, 30, GRAY, 4, 820)],
        ["一次投入 100 萬、不再加碼　簡化情境，非預測"], seal_xy=None)
fl.bars(o, "s3.png", 3, T, SD, "30 年後，100 萬變成", "平均相同，終點差很多。", [("A　每年 +6%", "穩定", fin[0]), ("B　+30% / −18%", "波動大", fin[1]), ("C　+20% / −8%", "波動中", fin[2])],
        "萬", "{:.1f}", "條長度從 0 起算，單位：萬", ["一次投入 100 萬、不再加碼　簡化情境，非預測", "情境試算，非投資建議。"], hi=1)
fl.big(o, "s4.png", 4, T, SD, "B 的實際年化報酬", f"{g_b:.2f}", "%", "平均 6%，實際只剩 3.25%。", "波動越大，實際年化越低於平均值。", ["簡化情境，非預測", "情境試算，非投資建議。"])
fl.text(o, "s5.png", 5, T, SD, [("看報酬，", SERIF_L, 72, INK, 7, 300), ("別只看平均。", SERIF_M, 72, VERM, 7, 400), ("__rule__", 0, 0, 0, 0, 560),
        ("看到「平均報酬」，先問：", SANS_R, 34, INK, 5, 600), ("中間波動有多大？", SANS_R, 34, INK, 5, 660), ("傳給只看平均報酬的人。", SERIF_M, 46, INK, 5, 800),
        ("存起來，下次看績效時對照。", SANS_L, 30, GRAY, 4, 870)], ["簡化情境，非預測。情境試算，非投資建議。"])

# ===== p13 單圖：小抄 =====
rows13 = [[f"{y} 年", f"{y*12} 萬" if False else f"{y*12*1} 萬".replace(f"{y*12} 萬", f"{y*12} 萬"), f"{fv(12*y):.1f} 萬"] for y in (5, 10, 15, 20, 25, 30)]
print("p13", rows13)
fl.table(f"{OUT}/p13", "single.png", 0, 0, "MONEY　小抄", "每月 1 萬，年化 6%", "複利小抄", ["時間", "本金", "終值"], rows13,
         "存起來，想放棄時看一次。", [BASE, FAIL], label="MONEY No.06", hi_row=5)

# ===== p14 輪播：月領 5 萬要先存多少 =====
o = f"{OUT}/p14"; SD = "MONEY　退休金"; T = 5
need = 5 * 12 / 0.04
pm = {y: need / fv(12 * y) for y in (20, 30, 40)}
print("p14", need, {k: round(v, 2) for k, v in pm.items()})
fl.cover(o, "s1.png", 1, T, SD, "常見經驗法則：每年提領 4%", "想每月領 5 萬，", "要先存多少", "答案在第 3 張。", "月領 5 萬 ＝ 一年 60 萬。",
         ["4% 提領率為常見經驗法則，非保證，未計通膨與稅費", "情境試算，非投資建議。"])
fl.text(o, "s2.png", 2, T, SD, [("一年 60 萬，", SERIF_L, 66, INK, 6, 200), ("除以 4% 提領率，", SERIF_L, 66, INK, 6, 290), ("__rule__", 0, 0, 0, 0, 440),
        ("60 ÷ 4% ＝", SANS_R, 40, INK, 5, 500), (f"{need:,.0f} 萬", SERIF_L, 150, VERM, 4, 580),
        ("4% 是常見的經驗法則，不是保證。", SANS_L, 30, GRAY, 4, 830)], ["未計通膨與稅費　情境試算，非投資建議"], seal_xy=None)
fl.big(o, "s3.png", 3, T, SD, "要在 30 年後存到 1,500 萬，每月要投", f"{pm[30]:.2f}", "萬", "30 年，每月 1.54 萬。", "年化 6%、按月複利。", [BASE.replace("每月投入 1 萬　", ""), FAIL])
fl.bars(o, "s4.png", 4, T, SD, "存到 1,500 萬，每月要投", "越早開始，每月越輕。", [("20 年後", "", pm[20]), ("30 年後", "", pm[30]), ("40 年後", "", pm[40])],
        "萬／月", "{:.2f}", "條長度從 0 起算，單位：萬／月", [BASE.replace("每月投入 1 萬　", ""), FAIL], hi=2)
fl.text(o, "s5.png", 5, T, SD, [("先有目標，", SERIF_L, 72, INK, 7, 300), ("才知道月投多少。", SERIF_M, 72, VERM, 7, 400), ("__rule__", 0, 0, 0, 0, 560),
        ("數字不是答案，", SANS_R, 34, INK, 5, 600), ("是讓目標有個價格。", SANS_R, 34, INK, 5, 660), ("傳給在想「退休要多少」的人。", SERIF_M, 46, INK, 5, 800),
        ("存起來，之後照這個算。", SANS_L, 30, GRAY, 4, 870)], ["4% 提領為經驗法則，不保證；未計通膨與稅費。情境試算，非投資建議。"])

# ===== p15 單圖：購買力 =====
real = A / 1.02 ** 30
print("p15", round(real, 1), round(1.02 ** 30, 2))
fl.big(f"{OUT}/p15", "single.png", 0, 0, "MONEY　購買力", "974.5 萬的購買力", f"{real:.1f}", "萬", "數字會變大，東西也會變貴。",
       f"年通膨 2%，30 年後物價約為現在的 {1.02**30:.2f} 倍。", ["每月 1 萬　年化 6%　按月複利　年通膨 2%　情境試算，非投資建議", "實際通膨與報酬都會變動。"], label="MONEY No.07")

# ===== p16 單圖：每天 100 元 =====
d100 = [(f"{y} 年", f"本金 {0.3*12*y:.0f} 萬", 0.3 * fv(12 * y)) for y in (10, 20, 30)]
print("p16", [round(v, 1) for _, _, v in d100])
fl.bars(f"{OUT}/p16", "single.png", 0, 0, "MONEY　日常", "每天少一杯 100 元", "每天省 100 元，會變多少？", d100, "萬", "{:.1f}",
        "每天 100 元以每月 3,000 元計，條長度從 0 起算，單位：萬", ["年化 6%　按月複利　情境試算，非投資建議", FAIL], hi=2, label="MONEY No.08")

# ===== p17 單圖：72 法則 =====
rows17 = [[f"{r}%", f"{72/r:.1f} 年", f"{math.log(2)/math.log(1+r/100):.1f} 年"] for r in (2, 4, 6, 8)]
print("p17", rows17)
fl.table(f"{OUT}/p17", "single.png", 0, 0, "MONEY　翻倍", "本金翻倍", "72 法則：幾年翻一倍？", ["年化報酬", "72 ÷ 報酬", "精算"], rows17,
         "72 ÷ 年化報酬 ≈ 本金翻倍年數（粗估）。", ["按年複利　情境試算，非投資建議", "實際報酬會波動，也可能低於這些假設。"], label="MONEY No.09")

# ===== p18 單圖：本月整理 =====
a_ = A
stop = a_ - (lambda: (lambda m: (lambda b: b)(sum((1 + m) ** (360 - i) for i in range(1, 361) if not (120 < i <= 144))))((1.06) ** (1 / 12) - 1))()
late5 = A / fv(300) - 1
fee = A - fv(360, a=0.05)
topup = fv(360, pmt=1.1) - A
raise_ = None
m_ = 1.06 ** (1 / 12) - 1; b_ = 0.0
for i in range(360): b_ = b_ * (1 + m_) + 1.03 ** (i // 12)
raise_ = b_ - A
rows18 = [["中間停扣 2 年", f"−{stop:.1f} 萬"], ["晚 5 年開始，月投要多", f"+{late5*100:.0f}%"], ["每年 1% 費用", f"−{fee:.1f} 萬"],
          ["每月多存 1,000 元", f"+{topup:.1f} 萬"], ["每年調高月投 3%", f"+{raise_:.1f} 萬"]]
print("p18", rows18)
fl.table(f"{OUT}/p18", "single.png", 0, 0, "MONEY　本月整理", "10 月的 5 個數字", "每月 1 萬、年化 6%、30 年", ["題材", "與基準 974.5 萬相比"], rows18,
         "存起來，想起來時看一次。", [BASE, FAIL], label="MONEY No.10", hi_row=None, rowh=112)
