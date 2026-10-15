import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import *

OUT = sys.argv[1]

# 里程碑：每月 1 萬、年化 6%、按月複利，累積到 100/200/300 萬各需幾個月
m = 1.06 ** (1 / 12) - 1
def reach(target):
    b, i = 0.0, 0
    while b < target * 1.0:
        i += 1
        b = b * (1 + m) + 1.0
    return i
r1, r2, r3 = reach(100), reach(200), reach(300)
legs = [("第 1 個 100 萬", r1), ("100 → 200 萬", r2 - r1), ("200 → 300 萬", r3 - r2)]
print(legs)

new_slide(PAPER)
frame(2, label="金錢日誌 No.02", side="金錢日誌　里程碑")
ttext(ML, 170, "里程碑", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "每多一個 100 萬，", font(SERIF_L, 80), INK, 6)
ttext(ML, 325, "都更快。", font(SERIF_M, 80), INK, 6)

y = 500
maxw = 520
for k, (lab, mo) in enumerate(legs):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.5)
    ttext(ML, y + 28, lab, font(SANS_R, 26), GRAY, 3)
    bw = maxw * mo / legs[0][1]
    rect(ML, y + 84, ML + bw, y + 112, fill=VERM if k == 0 else INK)
    yrs = f"{mo / 12:.1f}"
    w = ttext(MR, y + 64, "年", font(SERIF_M, 36), INK, 0, "r")
    ttext(MR - w - 8, y + 40, yrs, font(SERIF_L, 84), INK, 1, "r")
    ttext(ML + bw + 20, y + 84, f"{mo} 個月", font(SANS_L, 24), GRAY, 2)
    y += 170
hline(ML, MR, y, INK, 1.5)

rect(ML, 1080, ML + 56, 1084, fill=VERM)
ttext(ML, 1110, "前面最慢，後面加速。", font(SERIF_M, 48), INK, 5)
ttext(ML, 1245, "每月投入 1 萬　年化 6%　按月複利　情境試算，非投資建議", font(SANS_L, 22), GRAY, 2)
save(OUT, "post02_milestone.png")
