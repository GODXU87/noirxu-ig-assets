"""單圖：年化報酬差 2 個百分點。用法：python3 -I post08_return.py OUTDIR"""
import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import *
OUT = sys.argv[1]
def fv(n, a):
    m = (1 + a) ** (1 / 12) - 1
    return ((1 + m) ** n - 1) / m
rows = [(a, fv(360, a)) for a in (0.04, 0.06, 0.08)]
print([(a, round(v, 1)) for a, v in rows], round(rows[2][1] - rows[0][1], 1))
new_slide(PAPER); frame(3, label="金錢日誌 No.03", side="金錢日誌　報酬差")
ttext(ML, 170, "每月 1 萬，30 年", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "年化差 2 個百分點，", font(SERIF_L, 74), INK, 5)
ttext(ML, 325, "終點差多遠？", font(SERIF_M, 74), INK, 5)
y = 480; bw_max = 560; mx = rows[2][1]
for k, (a, v) in enumerate(rows):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y + 24, f"年化 {a*100:.0f}%", font(SANS_R, 30), INK, 4)
    ttext(ML, y + 70, "本金一樣 360 萬", font(SANS_L, 22), GRAY, 2)
    bw = bw_max * v / mx
    rect(ML, y + 118, ML + bw, y + 156, fill=VERM if k == 2 else INK)
    ttext(ML + bw + 18, y + 100, f"{v:.1f}", font(SERIF_L, 60), VERM if k == 2 else INK, 1)
    y += 205
hline(ML, MR, y, INK, 1.2)
ttext(ML, y + 26, f"8% 比 4% 多 {rows[2][1]-rows[0][1]:.1f} 萬。投入的錢一樣，差在複利的速度。", font(SANS_R, 26), GRAY, 3)
ttext(ML, 1245, "每月投入 1 萬　30 年　按月複利　條長度從 0 起算，單位：萬　情境試算，非投資建議", font(SANS_L, 21), GRAY, 2)
ttext(ML, 1290, "實際報酬會波動，也可能低於這些假設。", font(SANS_L, 21), GRAY, 2)
save(OUT, "post08_return.png")
