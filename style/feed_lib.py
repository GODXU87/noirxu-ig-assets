"""NOIRXU 輪播／單圖版型模組（1080x1350）。每個函式畫一張並存檔。數字由呼叫端算出。"""
import noirxu_style as ns
from noirxu_style import *

LIGHT, VERM_L = "#F3F0EA", "#E4A39C"

def fit(x, y, s, fp, size, color, track=0, maxw=None, anchor="l"):
    maxw = maxw or (MR - x)
    while ns.tw(s, font(fp, size), track) > maxw and size > 24: size -= 2
    return ttext(x, y, s, font(fp, size), color, track, anchor)

def foot(lines, dark=False):
    for i, t in enumerate(lines):
        fit(ML, 1245 + i * 45, t, SANS_L, 22, INDIGO_L if dark else GRAY, 2)

def head(n, total, side, dark=False, label=None):
    frame(n, total, label=label, side=side)

def cover(out, name, n, total, side, kicker, l1, l2, hint, sub, foot_lines, rows=None):
    """rows: [(標籤, 方格列函式)]，可選。"""
    new_slide(PAPER); head(n, total, side)
    ttext(ML, 250, kicker, font(SANS_R, 28), VERM, 6)
    fit(ML, 330, l1, SERIF_L, 92, INK, 8, 860)
    w = fit(ML, 450, l2, SERIF_M, 92, INK, 8, 800)
    ttext(ML + w + 8, 450, "？", font(SERIF_M, 92), VERM, 0)
    rect(ML, 640, ML + 64, 644, fill=VERM)
    ttext(ML, 680, sub, font(SANS_R, 34), INK, 5)
    ttext(ML, 740, hint, font(SANS_L, 30), GRAY, 4)
    if rows: rows()
    seal(MR - 50, 1196, 84)
    foot(foot_lines); save(out, name)

def bars(out, name, n, total, side, kicker, title, items, unit, fmt, note, foot_lines, hi=None, label=None, y0=440, rowh=230, vmax=None):
    """items: [(標籤, 副標, 數值)]；長條從 0 起算。"""
    new_slide(PAPER); head(n, total, side, label=label)
    ttext(ML, 170, kicker, font(SANS_R, 26), VERM, 6)
    fit(ML, 225, title, SERIF_L, 70, INK, 5, 860)
    mx = vmax or max(v for _, _, v in items); y = y0
    for i, (lab, sub, v) in enumerate(items):
        hline(ML, MR, y, INK if i == 0 else HAIR, 1.2)
        ttext(ML, y + 24, lab, font(SANS_R, 28), INK, 3)
        if sub: ttext(MR, y + 28, sub, font(SANS_L, 24), GRAY, 2, "r")
        bw = 520 * v / mx; col = VERM if (hi is not None and i == hi) else INK
        rect(ML, y + 100, ML + bw, y + 132, fill=col)
        ttext(ML + bw + 18, y + 88, fmt.format(v), font(SERIF_L, 56), col, 1)
        ttext(MR, y + 112, unit, font(SANS_L, 24), GRAY, 2, "r")
        y += rowh
    hline(ML, MR, y, INK, 1.2)
    ttext(ML, y + 24, note, font(SANS_L, 22), GRAY, 2)
    foot(foot_lines); save(out, name)

def big(out, name, n, total, side, label_top, number, unit, sub1, sub2, foot_lines, dark=True, label=None):
    new_slide(INDIGO if dark else PAPER, dark=dark); head(n, total, side, label=label)
    ink = LIGHT if dark else INK; gray = INDIGO_L if dark else GRAY
    ttext(ML, 170, label_top, font(SANS_R, 30), ink, 5)
    f = SERIF_XL if dark else SERIF_L; size = 300
    while ns.tw(number, font(f, size), 2) > 720 and size > 120: size -= 10
    w = ttext(ML - 6, 240, number, font(f, size), ink if dark else VERM, 2)
    ttext(ML + w + 10, 240 + int(size * 0.62), unit, font(SERIF_M, 70), ink if dark else VERM, 0)
    hline(ML, MR, 700, INDIGO_H if dark else INK, 1.2)
    fit(ML, 740, sub1, SERIF_M, 50, ink, 5, 860)
    if sub2: fit(ML, 830, sub2, SANS_R, 32, VERM_L if dark else GRAY, 4, 860)
    foot(foot_lines, dark); save(out, name)

def text(out, name, n, total, side, lines, foot_lines, bg=PAPER2, seal_xy=(MR - 70, 1090), label=None):
    """lines: [(文字, 字體, 大小, 顏色, 字距, y)]"""
    new_slide(bg); head(n, total, side, label=label)
    for t, fp, sz, col, tr, y in lines:
        if t == "__rule__": hline(ML, MR, y, INK, 1.2); continue
        fit(ML, y, t, fp, sz, col, tr, 860)
    if seal_xy: seal(seal_xy[0], seal_xy[1], 112)
    foot(foot_lines); save(out, name)

def table(out, name, n, total, side, kicker, title, head_cols, rows, note, foot_lines, label=None, hi_row=None, rowh=104):
    """rows: [[欄1, 欄2, 欄3...]]；最後一欄為重點數字。"""
    new_slide(PAPER); head(n, total, side, label=label)
    ttext(ML, 170, kicker, font(SANS_R, 26), VERM, 6)
    fit(ML, 225, title, SERIF_L, 70, INK, 5, 860)
    cols = len(head_cols); colw = (MR - ML) / cols; y = 420
    hline(ML, MR, y, INK, 1.2)
    for j, h in enumerate(head_cols): ttext(ML + j * colw, y + 20, h, font(SANS_L, 26), GRAY, 3)
    y += 80
    for i, r in enumerate(rows):
        hline(ML, MR, y, HAIR if i else INK, 1.2)
        for j, c in enumerate(r):
            last = j == cols - 1; hi = (hi_row == i and last)
            fit(ML + j * colw, y + 18, c, SERIF_L if last else SERIF_M, 56 if last else 44, VERM if (last and (hi_row is None or hi)) else INK, 1, colw - 24)
        y += rowh
    hline(ML, MR, y, INK, 1.2)
    ttext(ML, y + 24, note, font(SANS_L, 22), GRAY, 2)
    foot(foot_lines); save(out, name)
