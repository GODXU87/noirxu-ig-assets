"""免費名單磁鐵：停扣成本速查表（2 頁）。用法：python3 -I lead_magnet.py OUTDIR
數字全部由程式計算：每月 1 萬、年化 6%、按月複利、30 年；先計息再投入。"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "style"))
import noirxu_style as ns
from noirxu_style import *
import feed_lib as fl
from PIL import Image

OUT = sys.argv[1]
BASE = "每月投入 1 萬　年化 6%　按月複利　30 年　情境試算，非投資建議"
FAIL = "報酬更低或中斷更久，結果會不同。"

def series(skip=None, late_m=0, n=360, pmt=1.0, a=0.06):
    m = (1 + a) ** (1 / 12) - 1
    b = 0.0
    for i in range(1, n + 1):
        b *= 1 + m
        if skip and skip[0] < i <= skip[1]:
            continue
        if i <= late_m:
            continue
        b += pmt
    return b

A = series()
STOPS = (1, 2, 3, 5)
WHEN = (("前期", 1), ("中期", 11), ("後期", 21))
grid = [[A - series(((y0 - 1) * 12, (y0 - 1 + k) * 12)) for _, y0 in WHEN] for k in STOPS]
LATE = (1, 2, 5, 10)
late = [(k, series(late_m=k * 12), A - series(late_m=k * 12)) for k in LATE]
print("A", round(A, 1)); print("grid", [[round(v, 1) for v in r] for r in grid]); print("late", [(k, round(v, 1), round(g, 1)) for k, v, g in late])

def grid_page(path):
    new_slide(PAPER); frame(1, 2, side="MONEY　速查表")
    ttext(ML, 170, "停扣成本速查表", font(SANS_R, 26), VERM, 6)
    fl.fit(ML, 225, "停多久、停在哪，少多少？", SERIF_L, 66, INK, 5, 860)
    ttext(ML, 320, f"和「30 年一直投」終值 {A:.1f} 萬相比，少掉的金額（萬）。", font(SANS_L, 26), GRAY, 3)
    cw0 = 190; colw = (MR - ML - cw0) / 3; y = 430
    hline(ML, MR, y, INK, 1.2)
    ttext(ML, y + 22, "停多久", font(SANS_L, 26), GRAY, 3)
    for j, (lab, y0) in enumerate(WHEN):
        x = ML + cw0 + j * colw
        ttext(x, y + 22, lab, font(SANS_R, 28), INK, 3)
        ttext(x, y + 62, f"第 {y0} 年起停", font(SANS_L, 22), GRAY, 2)
    y += 120
    mx = max(max(r) for r in grid)
    for i, k in enumerate(STOPS):
        hline(ML, MR, y, INK if i == 0 else HAIR, 1.2)
        ttext(ML, y + 34, f"{k} 年", font(SERIF_M, 46), INK, 2)
        for j, v in enumerate(grid[i]):
            x = ML + cw0 + j * colw
            hi = (i == len(STOPS) - 1 and j == 0)
            ttext(x, y + 26, f"{v:.1f}", font(SERIF_L, 60), VERM if hi else INK, 1)
            rect(x, y + 108, x + (colw - 40) * v / mx, y + 116, fill=INK if hi else BAR)
        y += 138
    hline(ML, MR, y, INK, 1.2)
    ttext(ML, y + 26, "越早停、停越久，少得越多：前期少投的錢，少掉的是最長的複利時間。", font(SANS_L, 24), INK, 2)
    ttext(ML, y + 70, "長條從 0 起算，同一把尺。", font(SANS_L, 22), GRAY, 2)
    fl.foot([BASE, FAIL]); save(OUT, path)

def late_page(path):
    fl.bars(OUT, path, 2, 2, "MONEY　速查表", "晚開始速查", "晚幾年開始，終點少多少？",
            [(f"晚 {k} 年開始", f"終值 {v:.1f} 萬", g) for k, v, g in late], "萬", "{:.1f}",
            "同一個終點（第 30 年），晚開始就少投那幾年。長條＝少掉的金額，從 0 起算。",
            [BASE, FAIL], hi=len(late) - 1, y0=400, rowh=185)

grid_page("cheatsheet_1.png")
late_page("cheatsheet_2.png")
ims = [Image.open(os.path.join(OUT, n)).convert("RGB") for n in ("cheatsheet_1.png", "cheatsheet_2.png")]
ims[0].save(os.path.join(OUT, "NOIRXU_停扣成本速查表.pdf"), save_all=True, append_images=ims[1:], resolution=144)
print("ok")
