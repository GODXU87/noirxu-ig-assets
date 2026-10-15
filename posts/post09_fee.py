"""單圖：費用 1% 吃掉多少。用法：python3 -I post09_fee.py OUTDIR"""
import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import *
OUT = sys.argv[1]
def fv(n, a):
    m = (1 + a) ** (1 / 12) - 1
    return ((1 + m) ** n - 1) / m
full = fv(360, 0.06); r1 = fv(360, 0.05); r2 = fv(360, 0.04)
print(round(full, 1), round(r1, 1), round(r2, 1), round(full - r1, 1), round((full - r1) / full * 100, 1))
new_slide(PAPER); frame(4, label="MONEY No.04", side="MONEY　費用")
ttext(ML, 170, "每年 1% 的費用", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "30 年後，", font(SERIF_L, 74), INK, 5)
ttext(ML, 325, "從終點吃掉多少？", font(SERIF_M, 74), INK, 5)
ttext(ML, 470, "少了", font(SANS_R, 30), GRAY, 5)
w = ttext(ML - 4, 515, f"{full-r1:.1f}", font(SERIF_L, 200), VERM, 2)
ttext(ML + w + 10, 670, "萬", font(SERIF_M, 60), VERM, 0)
ttext(ML, 775, f"約占終值的 {(full-r1)/full*100:.0f}%。", font(SERIF_M, 40), INK, 5)
y = 890; bw_max = 560
for k, (lab, v) in enumerate((("費用 0%（年化 6%）", full), ("費用 1%（年化 5%）", r1), ("費用 2%（年化 4%）", r2))):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y + 14, lab, font(SANS_R, 26), INK, 3)
    bw = bw_max * v / full
    rect(ML, y + 56, ML + bw, y + 80, fill=VERM if k == 1 else INK)
    ttext(ML + bw + 16, y + 40, f"{v:.1f}", font(SERIF_L, 44), VERM if k == 1 else INK, 1)
    y += 108
hline(ML, MR, y, INK, 1.2)
ttext(ML, 1245, "每月投入 1 萬　30 年　簡化為年化報酬直接扣除費用率　條長度從 0 起算，單位：萬", font(SANS_L, 20), GRAY, 2)
ttext(ML, 1290, "實際費用結構因商品而異，情境試算，非投資建議。", font(SANS_L, 20), GRAY, 2)
save(OUT, "post09_fee.png")
