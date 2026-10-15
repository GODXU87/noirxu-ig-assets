"""輪播 7 張：停的位置不同。用法：python3 -I post06_position.py OUTDIR"""
import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import *

OUT = sys.argv[1]
TOTAL = 7
SIDE = "MONEY　停的位置"
LIGHT = "#F2F2F2"
full = compound_series()[-1]
cases = []
for name, win, hol, rest in (("A", (336, 360), (28, 29), "那 24 筆本來只能複利 0–2 年"), ("B", (120, 144), (10, 11), "那 24 筆本來能複利 18–20 年"),
                             ("C", (0, 24), (0, 1), "那 24 筆本來能複利 28–30 年")):
    v = compound_series(skip=win)[-1]
    cases.append(dict(name=name, win=win, hol=hol, final=v, gap=full - v, rest=rest))
for c in cases: print(c["name"], f"{c['final']:.1f} {c['gap']:.1f}")
FULL, (A, B, C) = f"{full:.1f}", cases

LAB = {"A": "停在最後 2 年", "B": "停在中間 2 年", "C": "停在最前面 2 年"}
YRS = {"A": "第 29–30 年", "B": "第 11–12 年", "C": "第 1–2 年"}

def rowsq(y, hol, dark=False, sz=15):
    xl, xr = ML + 8, MR - 8
    step = (xr - xl) / 29
    for c in range(30):
        cx = xl + c * step
        box = [(cx - sz / 2) * S, (y - sz / 2) * S, (cx + sz / 2) * S, (y + sz / 2) * S]
        if c in hol:
            d_ = ns.d; d_.rectangle(box, outline=hexc("#B8B8B8" if dark else VERM), width=int(2 * S))
        else:
            ns.d.rectangle(box, fill=hexc(LIGHT if dark else INK))

def disclaimer(dark=False):
    ttext(ML, 1245, "每月投入 1 萬　年化 6%　按月複利　30 年　情境試算，非投資建議",
          font(SANS_L, 22), INDIGO_L if dark else GRAY, 2)

# 1 封面
new_slide(PAPER); frame(1, TOTAL, side=SIDE)
ttext(ML, 250, "同樣停 2 年", font(SANS_R, 28), VERM, 8)
ttext(ML, 330, "停在哪一年，", font(SERIF_L, 92), INK, 8)
w = ttext(ML, 450, "差最多", font(SERIF_M, 92), INK, 8)
ttext(ML + w + 8, 450, "？", font(SERIF_M, 92), VERM, 0)
rect(ML, 640, ML + 64, 644, fill=VERM)
ttext(ML, 680, "每月 1 萬，30 年。", font(SANS_R, 34), INK, 5)
ttext(ML, 740, "三種停法，答案在第 5 張。", font(SANS_L, 30), GRAY, 4)
for k, c in enumerate(cases):
    y = 905 + k * 105
    ttext(ML, y - 56, c["name"], font(SERIF_L, 34), VERM, 0)
    rowsq(y, c["hol"])
seal(MR - 50, 1196, 84)
disclaimer()
save(OUT, "s1.png")

# 2 三種位置
new_slide(PAPER); frame(2, TOTAL, side=SIDE)
ttext(ML, 170, "三種停法", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "都是 24 個月。", font(SERIF_L, 76), INK, 6)
ttext(ML, 330, "一個方格 ＝ 1 年，空心 ＝ 沒投的那 2 年。", font(SANS_L, 26), GRAY, 3)
for k, c in enumerate(cases):
    y = 540 + k * 220
    hline(ML, MR, y - 60, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y - 32, c["name"], font(SERIF_L, 54), VERM, 0)
    ttext(ML + 70, y - 22, f"{LAB[c['name']]}（{YRS[c['name']]}）", font(SANS_R, 30), INK, 4)
    rowsq(y + 70, c["hol"], sz=17)
hline(ML, MR, 540 + 3 * 220 - 60, INK, 1.2)
disclaimer()
save(OUT, "s2.png")

# 3、4、5 各一種位置（最大的放第 5 張，深藍）
for n, c in zip((3, 4, 5), cases):
    dark = (n == 5)
    new_slide(INDIGO if dark else PAPER, dark=dark); frame(n, TOTAL, side=SIDE)
    ink = LIGHT if dark else INK
    gray = INDIGO_L if dark else GRAY
    acc = "#B8B8B8" if dark else VERM
    ttext(ML, 170, c["name"], font(SERIF_L, 60), acc, 0)
    ttext(ML + 76, 188, f"{LAB[c['name']]}（{YRS[c['name']]}）", font(SANS_R, 30), ink, 4)
    rowsq(300, c["hol"], dark=dark, sz=17)
    ttext(ML, 400, "最後少了", font(SANS_R, 30), gray, 5)
    gs = f"{c['gap']:.1f}"
    if dark:
        w = ttext(ML - 6, 440, gs, font(SERIF_XL, 270), ink, 2)
        ttext(ML + w + 10, 640, "萬", font(SERIF_M, 70), ink, 0)
        ly = 860
    else:
        w = ttext(ML - 4, 450, gs, font(SERIF_L, 230), acc, 2)
        ttext(ML + w + 10, 625, "萬", font(SERIF_M, 64), acc, 0)
        ly = 860
    hline(ML, MR, ly, INDIGO_H if dark else INK, 1.2)
    colw = (MR - ML) / 2
    for j, (lab, val, hi) in enumerate((("一直投", FULL, False), (f"{LAB[c['name']]}", f"{c['final']:.1f}", True))):
        x = ML + j * colw
        ttext(x, ly + 28, lab, font(SANS_L, 26), gray, 3)
        w2 = ttext(x, ly + 70, val, font(SERIF_L, 76), acc if hi else ink, 1)
        ttext(x + w2 + 8, ly + 108, "萬", font(SERIF_M, 32), acc if hi else ink, 0)
    ttext(ML, ly + 230, c["rest"] + "。", font(SANS_R, 28), gray, 3)
    disclaimer(dark)
    save(OUT, f"s{n}.png")

# 6 圖表：三個差距並排
new_slide(PAPER); frame(6, TOTAL, side=SIDE)
ttext(ML, 170, "同樣少投 24 萬", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "差在它們能複利幾年。", font(SERIF_L, 76), INK, 6)
mx = max(c["gap"] for c in cases)
y = 440
bw_max = 520
for k, c in enumerate(cases):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y + 24, f"{c['name']}　{LAB[c['name']]}", font(SANS_R, 28), INK, 3)
    ttext(ML, y + 66, c["rest"], font(SANS_L, 24), GRAY, 2)
    bw = bw_max * c["gap"] / mx
    rect(ML, y + 120, ML + bw, y + 152, fill=VERM if k == 2 else INK)
    ttext(ML + bw + 18, y + 108, f"{c['gap']:.1f}", font(SERIF_L, 56), VERM if k == 2 else INK, 1)
    y += 230
hline(ML, MR, y, INK, 1.2)
ttext(ML, y + 24, "條長度從 0 起算，單位：萬（與一直投相比少的金額）", font(SANS_L, 22), GRAY, 2)
disclaimer()
save(OUT, "s6.png")

# 7 收尾
new_slide(PAPER2); frame(7, TOTAL, side=SIDE)
ttext(ML, 300, "越早的那一筆，", font(SERIF_L, 72), INK, 7)
ttext(ML, 400, "後面陪它的時間越長。", font(SERIF_M, 72), VERM, 7)
hline(ML, MR, 560, INK, 1.2)
ttext(ML, 600, "停扣不是不行，", font(SANS_R, 34), INK, 5)
ttext(ML, 660, "只是停的位置，會改變代價。", font(SANS_R, 34), INK, 5)
ttext(ML, 800, "傳給正在猶豫要不要停的人。", font(SERIF_M, 46), INK, 5)
ttext(ML, 870, "存起來，下次停之前再算一次。", font(SANS_L, 30), GRAY, 4)
seal(MR - 70, 1090, 112)
disclaimer()
ttext(ML, 1290, "報酬更低或中斷更久，結果會不同。", font(SANS_L, 22), GRAY, 2)
save(OUT, "s7.png")
