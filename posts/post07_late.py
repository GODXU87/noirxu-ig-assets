"""輪播 6 張：晚開始。用法：python3 -I post07_late.py OUTDIR"""
import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import *
OUT = sys.argv[1]; TOTAL = 6; SIDE = "金錢日誌　晚開始"; LIGHT = "#F3F0EA"

def fv(n, a=0.06):
    m = (1 + a) ** (1 / 12) - 1
    return ((1 + m) ** n - 1) / m
A = fv(360)
cs = []
for name, late in (("A", 0), ("B", 5), ("C", 10)):
    n = 360 - 12 * late
    cs.append(dict(name=name, late=late, n=n, same=fv(n), need=A / fv(n), gap=A - fv(n)))
for c in cs: print(c["name"], f"{c['same']:.1f} {c['gap']:.1f} 需 {c['need']:.3f} 本金 {c['need']*c['n']:.1f}")
B_, C_ = cs[1], cs[2]
LAB = {"A": "現在開始", "B": "晚 5 年開始", "C": "晚 10 年開始"}

def rowsq(y, nhol, dark=False, sz=15):
    xl, xr = ML + 8, MR - 8; step = (xr - xl) / 29
    for c in range(30):
        cx = xl + c * step
        box = [(cx - sz / 2) * S, (y - sz / 2) * S, (cx + sz / 2) * S, (y + sz / 2) * S]
        if c < nhol: ns.d.rectangle(box, outline=hexc("#E4A39C" if dark else VERM), width=int(2 * S))
        else: ns.d.rectangle(box, fill=hexc(LIGHT if dark else INK))

def foot(dark=False, extra=None):
    ttext(ML, 1245, "終點同一天　年化 6%　按月複利　情境試算，非投資建議", font(SANS_L, 22), INDIGO_L if dark else GRAY, 2)
    if extra: ttext(ML, 1290, extra, font(SANS_L, 22), INDIGO_L if dark else GRAY, 2)

# 1 封面
new_slide(PAPER); frame(1, TOTAL, side=SIDE)
ttext(ML, 250, "還在等「之後再開始」？", font(SANS_R, 28), VERM, 6)
ttext(ML, 330, "晚 5 年開始，", font(SERIF_L, 92), INK, 8)
ttext(ML, 450, "每月要多存多少", font(SERIF_M, 92), INK, 6)
ttext(ML + 92 * 7 + 6 * 6 + 6, 450, "？", font(SERIF_M, 92), VERM, 0)
rect(ML, 640, ML + 64, 644, fill=VERM)
ttext(ML, 680, "想在同一天，存到一樣多。", font(SANS_R, 34), INK, 5)
ttext(ML, 740, "答案在第 4 張。", font(SANS_L, 30), GRAY, 4)
for k, c in enumerate(cs):
    y = 905 + k * 105
    ttext(ML, y - 56, c["name"], font(SERIF_L, 34), VERM, 0)
    rowsq(y, c["late"])
seal(MR - 50, 1196, 84)
foot()
save(OUT, "s1.png")

# 2 設定
new_slide(PAPER); frame(2, TOTAL, side=SIDE)
ttext(ML, 170, "三個人", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "同一天要存到 974.5 萬。", font(SERIF_L, 70), INK, 5)
ttext(ML, 330, "一個方格 ＝ 1 年，空心 ＝ 還沒開始投的年份。", font(SANS_L, 26), GRAY, 3)
for k, c in enumerate(cs):
    y = 540 + k * 220
    hline(ML, MR, y - 60, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y - 32, c["name"], font(SERIF_L, 54), VERM, 0)
    ttext(ML + 70, y - 22, f"{LAB[c['name']]}（可投 {c['n']//12} 年）", font(SANS_R, 30), INK, 4)
    rowsq(y + 70, c["late"], sz=17)
hline(ML, MR, 540 + 3 * 220 - 60, INK, 1.2)
foot()
save(OUT, "s2.png")

# 3 晚 5 年，同樣月投
new_slide(PAPER); frame(3, TOTAL, side=SIDE)
ttext(ML, 170, "B　晚 5 年開始，仍然每月 1 萬", font(SANS_R, 30), INK, 4)
rowsq(260, 5, sz=17)
ttext(ML, 360, "最後少了", font(SANS_R, 30), GRAY, 5)
w = ttext(ML - 4, 410, f"{B_['gap']:.1f}", font(SERIF_L, 230), VERM, 2)
ttext(ML + w + 10, 585, "萬", font(SERIF_M, 64), VERM, 0)
ly = 820
hline(ML, MR, ly, INK, 1.2)
colw = (MR - ML) / 2
for j, (lab, val, hi) in enumerate((("現在開始", f"{A:.1f}", False), ("晚 5 年開始", f"{B_['same']:.1f}", True))):
    x = ML + j * colw
    ttext(x, ly + 28, lab, font(SANS_L, 26), GRAY, 3)
    w2 = ttext(x, ly + 70, val, font(SERIF_L, 76), VERM if hi else INK, 1)
    ttext(x + w2 + 8, ly + 108, "萬", font(SERIF_M, 32), VERM if hi else INK, 0)
ttext(ML, ly + 230, "只少投 5 年的本金（60 萬），卻少了這麼多。", font(SANS_R, 28), GRAY, 3)
foot()
save(OUT, "s3.png")

# 4 答案（深藍）
new_slide(INDIGO, dark=True); frame(4, TOTAL, side=SIDE)
ttext(ML, 170, "要追上，B 每月要投", font(SANS_R, 30), LIGHT, 5)
w = ttext(ML - 6, 240, f"{B_['need']:.2f}", font(SERIF_XL, 300), LIGHT, 2)
ttext(ML + w + 10, 470, "萬", font(SERIF_M, 70), LIGHT, 0)
hline(ML, MR, 700, INDIGO_H, 1.2)
ttext(ML, 740, f"比原本的 1 萬，多了 {round((B_['need']-1)*100)}%。", font(SERIF_M, 50), LIGHT, 5)
ttext(ML, 830, f"總共投入 {B_['need']*B_['n']:.0f} 萬，", font(SANS_R, 32), INDIGO_L, 4)
ttext(ML, 885, f"比 A 的 360 萬多出 {B_['need']*B_['n']-360:.0f} 萬。", font(SANS_R, 32), "#E4A39C", 4)
foot(True)
save(OUT, "s4.png")

# 5 圖表
new_slide(PAPER); frame(5, TOTAL, side=SIDE)
ttext(ML, 170, "同一天存到 974.5 萬", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "越晚開始，月投越高。", font(SERIF_L, 76), INK, 6)
y = 440; bw_max = 520; mx = cs[2]["need"]
for k, c in enumerate(cs):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y + 24, f"{c['name']}　{LAB[c['name']]}", font(SANS_R, 28), INK, 3)
    ttext(ML, y + 66, f"總投入 {c['need']*c['n']:.0f} 萬", font(SANS_L, 24), GRAY, 2)
    bw = bw_max * c["need"] / mx
    rect(ML, y + 120, ML + bw, y + 152, fill=VERM if k == 2 else INK)
    ttext(ML + bw + 18, y + 108, f"{c['need']:.2f}", font(SERIF_L, 56), VERM if k == 2 else INK, 1)
    ttext(MR, y + 128, "萬／月", font(SANS_L, 24), GRAY, 2, "r")
    y += 230
hline(ML, MR, y, INK, 1.2)
ttext(ML, y + 24, "條長度從 0 起算，單位：萬／月", font(SANS_L, 22), GRAY, 2)
foot()
save(OUT, "s5.png")

# 6 收尾
new_slide(PAPER2); frame(6, TOTAL, side=SIDE)
ttext(ML, 300, "每晚一年，", font(SERIF_L, 72), INK, 7)
ttext(ML, 400, "月投都要再往上加。", font(SERIF_M, 72), VERM, 7)
hline(ML, MR, 560, INK, 1.2)
ttext(ML, 600, "不是要你焦慮，", font(SANS_R, 34), INK, 5)
ttext(ML, 660, "是讓「之後再開始」有個價格。", font(SANS_R, 34), INK, 5)
ttext(ML, 800, "傳給還在等「之後」的人。", font(SERIF_M, 46), INK, 5)
ttext(ML, 870, "存起來，等下次想拖的時候看。", font(SANS_L, 30), GRAY, 4)
seal(MR - 70, 1090, 112)
foot(extra="報酬更低或中斷更久，結果會不同。")
save(OUT, "s6.png")
