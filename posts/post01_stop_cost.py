import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageChops

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
S = 2
W, H = 1080, 1350
TOTAL = 8
FD = "/usr/share/fonts/opentype/noto/"
SERIF_XL = FD + "NotoSerifCJK-ExtraLight.ttc"
SERIF_L = FD + "NotoSerifCJK-Light.ttc"
SERIF_M = FD + "NotoSerifCJK-Medium.ttc"
SERIF_SB = FD + "NotoSerifCJK-SemiBold.ttc"
SANS_L = FD + "NotoSansCJK-Light.ttc"
SANS_R = FD + "NotoSansCJK-Regular.ttc"

_idx = {}
def tc(path):
    if path in _idx: return _idx[path]
    for i in range(10):
        try:
            f = ImageFont.truetype(path, 20, index=i)
        except Exception:
            break
        if "TC" in " ".join(f.getname()):
            _idx[path] = i; return i
    _idx[path] = 0; return 0

def font(path, size):
    return ImageFont.truetype(path, int(size * S), index=tc(path))

def hexc(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

PAPER, INK, GRAY, HAIR = "#F6F4EF", "#1B1B1A", "#74726C", "#D5D1C8"
VERM, VERM_T = "#B7322A", "#F0DCD6"
INDIGO, INDIGO_L = "#16233B", "#AEB8CC"
ML, MR = 118, W - 90

im = d = None
DARK = False
def new_slide(bg, dark=False):
    global im, d, DARK
    DARK = dark
    im = Image.new("RGB", (W * S, H * S), hexc(bg))
    d = ImageDraw.Draw(im)

def P(pts): return [(x * S, y * S) for x, y in pts]

def ttext(x, y, s, f, fill, track=0, anchor="l"):
    adv = [d.textlength(ch, font=f) / S + track for ch in s]
    total = sum(adv) - track
    if anchor == "c": x = x - total / 2
    elif anchor == "r": x = x - total
    cx = x
    for ch, a in zip(s, adv):
        d.text((cx * S, y * S), ch, font=f, fill=hexc(fill))
        cx += a
    return total

def tw(s, f, track=0):
    return sum(d.textlength(ch, font=f) / S + track for ch in s) - track

def vtext(x, y, s, f, fill, track=8):
    sz = f.size / S
    for ch in s:
        d.text((x * S, y * S), ch, font=f, fill=hexc(fill), anchor="mt")
        y += sz + track

def hline(x0, x1, y, color=HAIR, w=1.5):
    d.line(P([(x0, y), (x1, y)]), fill=hexc(color), width=max(1, int(w * S)))

def vline(x, y0, y1, color=HAIR, w=1.5):
    d.line(P([(x, y0), (x, y1)]), fill=hexc(color), width=max(1, int(w * S)))

def seal(cx, cy, size, ch="帳", angle=-3):
    pad = 10
    layer = Image.new("RGBA", (int((size + pad * 2) * S), int((size + pad * 2) * S)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([pad * S, pad * S, (pad + size) * S, (pad + size) * S], radius=5 * S, fill=hexc(VERM))
    ld.rounded_rectangle([(pad + 6) * S, (pad + 6) * S, (pad + size - 6) * S, (pad + size - 6) * S], radius=3 * S,
                         outline=hexc("#F3E4E0"), width=int(2 * S))
    ld.text(((pad + size / 2) * S, (pad + size / 2) * S), ch, font=font(SERIF_SB, size * 0.56), fill=hexc("#F8EDEA"), anchor="mm")
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    im.paste(layer, (int(cx * S - layer.width / 2), int(cy * S - layer.height / 2)), layer)

def frame(n):
    ink = "#F3F0EA" if DARK else INK
    gray = INDIGO_L if DARK else GRAY
    hair = "#3A4A68" if DARK else HAIR
    ttext(ML, 56, "NOIRXU", font(SANS_R, 22), ink, 7)
    ttext(MR, 56, f"{n:02d} / {TOTAL:02d}", font(SANS_L, 22), gray, 4, "r")
    hline(ML, MR, 100, hair if DARK else INK, 1.2)
    # 左側直書
    d.rectangle([44 * S, 150 * S, 52 * S, 158 * S], fill=hexc(VERM))
    vtext(48, 180, "金錢日誌　停扣成本", font(SANS_L, 21), gray, 9)

def grain(img):
    noise = Image.effect_noise(img.size, 10).convert("RGB")
    return Image.blend(img, ImageChops.multiply(img, noise.point(lambda v: 240 + v // 24)), 0.22)

def save(n):
    grain(im).resize((W, H), Image.LANCZOS).save(os.path.join(OUT, f"b{n}.png"))

def matrix(y0, hollow_cols=()):
    cols, rows = 30, 12
    xl, xr = ML + 8, MR - 8
    step = (xr - xl) / (cols - 1)
    sz = 15
    for c in range(cols):
        for r in range(rows):
            cx, cy = xl + c * step, y0 + r * step
            box = [(cx - sz / 2) * S, (cy - sz / 2) * S, (cx + sz / 2) * S, (cy + sz / 2) * S]
            if c in hollow_cols:
                d.rectangle(box, outline=hexc(VERM), width=int(2 * S))
            else:
                d.rectangle(box, fill=hexc(INK))
    return xl, step

def stat_row(y, items):
    hline(ML, MR, y, INK, 1.2)
    colw = (MR - ML) / 3
    for k, (lab, val, unit, hi) in enumerate(items):
        x = ML + k * colw
        ttext(x, y + 22, lab, font(SANS_L, 24), GRAY, 3)
        f = font(SERIF_L, 70)
        w = ttext(x, y + 62, val, f, VERM if hi else INK, 1)
        ttext(x + w + 8, y + 94, unit, font(SERIF_M, 30), VERM if hi else INK, 0)

# ================= 1 封面 =================
new_slide(PAPER); frame(1)
ttext(ML, 300, "只停兩年，", font(SERIF_L, 132), INK, 12)
w = ttext(ML, 470, "會差多少", font(SERIF_M, 132), INK, 12)
ttext(ML + w + 12, 470, "？", font(SERIF_M, 132), VERM, 0)
hline(ML, MR, 700, INK, 2)
colw = (MR - ML) / 3
for k, (lab, val, unit) in enumerate([("每月投入", "1", "萬"), ("年化報酬", "6", "%"), ("投入期間", "30", "年")]):
    x = ML + k * colw
    ttext(x, 730, lab, font(SANS_L, 24), GRAY, 3)
    ww = ttext(x, 770, val, font(SERIF_L, 76), INK, 0)
    ttext(x + ww + 8, 808, unit, font(SERIF_M, 32), INK, 0)
hline(ML, MR, 900, HAIR, 1.5)
ttext(ML, 925, "中斷：第 11 至 12 年，共 24 個月", font(SANS_L, 28), GRAY, 3)
seal(MR - 70, 1090, 112)
ttext(ML, 1180, "往右翻　→", font(SERIF_M, 30), INK, 6)
save(1)

# ================= 2 共鳴（目錄式列表） =================
new_slide(PAPER); frame(2)
ttext(ML, 190, "你停過扣嗎？", font(SERIF_L, 104), INK, 10)
ttext(ML, 330, "很多人都停過。", font(SANS_L, 32), GRAY, 5)
rows = ["換工作", "急用錢", "想先觀望"]
y = 470
for k, t in enumerate(rows):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.5)
    ttext(ML, y + 52, f"{k + 1:02d}", font(SERIF_L, 44), VERM, 2)
    ttext(ML + 120, y + 36, t, font(SERIF_M, 68), INK, 8)
    y += 160
hline(ML, MR, y, INK, 1.5)
d.rectangle([ML * S, 1030 * S, (ML + 56) * S, 1034 * S], fill=hexc(VERM))
ttext(ML, 1062, "停之前，沒人告訴你價格。", font(SERIF_M, 48), INK, 5)
ttext(MR, 1250, "→", font(SERIF_M, 38), INK, 0, "r")
save(2)

# ================= 3 一直投 =================
new_slide(PAPER); frame(3)
ttext(ML, 170, "A　一直投", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "每個月都投，", font(SERIF_L, 84), INK, 8)
ttext(ML, 330, "投了三十年。", font(SERIF_M, 84), INK, 8)
matrix(500)
ttext(ML, 500 + 11 * 30.3 + 44, "一格 = 一個月　共 360 格", font(SANS_L, 24), GRAY, 3)
stat_row(930, [("投入本金", "360", "萬", False), ("終值", "974.5", "萬", True), ("增值", "614.5", "萬", False)])
ttext(ML, 1245, "每月 1 萬　年化 6%　按月複利　情境試算，非投資建議", font(SANS_L, 22), GRAY, 2)
save(3)

# ================= 4 停 2 年 =================
new_slide(PAPER); frame(4)
ttext(ML, 170, "B　停 2 年", font(SANS_R, 26), VERM, 6)
ttext(ML, 225, "空了 24 格，", font(SERIF_L, 84), INK, 8)
ttext(ML, 330, "其餘一樣。", font(SERIF_M, 84), INK, 8)
xl, step = matrix(500, hollow_cols=(10, 11))
bx0, bx1 = xl + 10 * step - 14, xl + 11 * step + 14
by = 500 + 11 * 30.3 + 30
d.line(P([(bx0, by), (bx0, by + 12), (bx1, by + 12), (bx1, by)]), fill=hexc(VERM), width=int(2 * S))
ttext((bx0 + bx1) / 2 + 150, by + 20, "第 11 至 12 年停扣", font(SANS_R, 24), VERM, 3, "c")
stat_row(930, [("投入本金", "336", "萬", False), ("終值", "902.0", "萬", True), ("增值", "566.0", "萬", False)])
ttext(ML, 1245, "每月 1 萬　年化 6%　按月複利　情境試算，非投資建議", font(SANS_L, 22), GRAY, 2)
save(4)

# ================= 5 差距（深藍滿版） =================
new_slide(INDIGO, True); frame(5)
ttext(ML, 175, "兩者相差", font(SANS_L, 32), INDIGO_L, 8)
w = ttext(ML - 6, 215, "72.5", font(SERIF_XL, 330), "#F3F0EA", 2)
ttext(ML + w + 14, 440, "萬", font(SERIF_L, 100), "#F3F0EA", 0)
hline(ML, MR, 740, "#3A4A68", 1.5)
r_big = 168
r_small = r_big / math.sqrt(72.5 / 24)
cy = 940
cxs, cxb = ML + 120, ML + 560
d.ellipse([(cxs - r_small) * S, (cy - r_small) * S, (cxs + r_small) * S, (cy + r_small) * S], outline=hexc("#F3F0EA"), width=int(2.5 * S))
d.ellipse([(cxb - r_big) * S, (cy - r_big) * S, (cxb + r_big) * S, (cy + r_big) * S], outline=hexc("#F3F0EA"), width=int(2.5 * S))
d.line(P([(cxs + r_small + 18, cy), (cxb - r_big - 18, cy)]), fill=hexc(INDIGO_L), width=int(1.5 * S))
ttext(cxs, cy - 42, "少投", font(SANS_L, 26), INDIGO_L, 4, "c")
ttext(cxs, cy - 8, "24 萬", font(SERIF_M, 42), "#F3F0EA", 1, "c")
ttext(cxb, cy - 52, "少賺", font(SANS_L, 28), INDIGO_L, 4, "c")
ttext(cxb, cy - 14, "72.5 萬", font(SERIF_M, 56), "#F3F0EA", 1, "c")
ttext(ML, 1215, "圓的面積與金額成比例。少投的錢，被放大約 3 倍。", font(SANS_L, 26), INDIGO_L, 2)
save(5)

# ================= 6 圖表（細線） =================
new_slide(PAPER); frame(6)
ttext(ML, 175, "停掉的，", font(SERIF_L, 84), INK, 8)
ttext(ML, 280, "不只是那 24 萬。", font(SERIF_M, 84), INK, 8)
m = (1.06) ** (1 / 12) - 1
def series(skip=None):
    b = 0; out = [0]
    for i in range(1, 361):
        b *= 1 + m
        if not (skip and skip[0] < i <= skip[1]): b += 10000
        out.append(b / 1e4)
    return out
full, stop = series(), series((120, 144))
cx0, cx1, cy0, cy1 = ML + 60, MR - 130, 520, 980
def px(mo): return cx0 + (cx1 - cx0) * mo / 360
def py(v): return cy1 - (cy1 - cy0) * v / 1000
# 停扣區間色帶
d.rectangle([px(120) * S, cy0 * S, px(144) * S, cy1 * S], fill=hexc(VERM_T))
ttext((px(120) + px(144)) / 2, cy0 - 38, "停 2 年", font(SANS_R, 22), VERM, 3, "c")
for v in (0, 250, 500, 750, 1000):
    hline(cx0, cx1, py(v), HAIR, 1.2)
    ttext(cx0 - 14, py(v) - 14, f"{v}", font(SANS_L, 20), GRAY, 0, "r")
for yr in (0, 10, 20, 30):
    ttext(px(yr * 12), cy1 + 16, f"{yr}", font(SANS_L, 22), GRAY, 0, "c")
ttext(cx1 + 14, cy1 + 16, "年", font(SANS_L, 22), GRAY, 0)
d.line(P([(px(i), py(full[i])) for i in range(0, 361, 2)]), fill=hexc(INK), width=int(3.5 * S), joint="curve")
d.line(P([(px(i), py(stop[i])) for i in range(0, 361, 2)]), fill=hexc(VERM), width=int(3.5 * S), joint="curve")
# 終端標註
ex = cx1 + 22
ttext(ex, py(full[360]) - 30, "974.5", font(SERIF_M, 32), INK, 1)
ttext(ex, py(stop[360]) + 4, "902.0", font(SERIF_M, 32), VERM, 1)
bx = cx1 + 12
vline(bx, py(full[360]), py(stop[360]), VERM, 2)
ttext(ex, py(stop[360]) + 50, "差 72.5", font(SANS_R, 22), VERM, 2)
ttext(ML, 1085, "複利吃的是時間，", font(SERIF_M, 46), INK, 5)
ttext(ML, 1145, "不是金額。", font(SERIF_M, 46), VERM, 5)
ttext(ML, 1245, "單位：萬　每月 1 萬　年化 6%　情境試算，非投資建議", font(SANS_L, 22), GRAY, 2)
save(6)

# ================= 7 清單 =================
new_slide("#ECE9E2"); frame(7)
ttext(ML, 185, "暫停前的", font(SANS_L, 32), GRAY, 8)
ttext(ML, 235, "三個問題", font(SERIF_L, 112), INK, 12)
qs = ["能不能只降額，不全停？", "要停幾個月？先寫下恢復日期。", "三個月後，這個原因還在嗎？"]
y = 470
for k, q in enumerate(qs):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.5)
    d.rectangle([ML * S, (y + 58) * S, (ML + 46) * S, (y + 104) * S], outline=hexc(INK), width=int(2.5 * S))
    ttext(ML + 86, y + 40, f"{k + 1:02d}", font(SERIF_L, 30), VERM, 2)
    ttext(ML + 86, y + 80, q, font(SERIF_M, 46), INK, 3)
    y += 190
hline(ML, MR, y, INK, 1.5)
d.rectangle([ML * S, 1100 * S, (ML + 56) * S, 1104 * S], fill=hexc(VERM))
ttext(ML, 1130, "存起來，下次想停時再看。", font(SERIF_M, 44), INK, 5)
save(7)

# ================= 8 收尾 =================
new_slide(PAPER); frame(8)
ttext(ML, 260, "傳給那個說", font(SANS_L, 34), GRAY, 8)
ttext(ML, 320, "「先停一陣子」", font(SERIF_L, 100), INK, 8)
ttext(ML, 450, "的人。", font(SERIF_M, 100), INK, 8)
hline(ML, MR, 640, INK, 2)
ttext(ML, 690, "算複利，先算會不會中斷。", font(SERIF_M, 44), INK, 5)
ttext(ML, 765, "自己的數字，簡介有計算器。", font(SANS_L, 28), GRAY, 4)
seal(MR - 90, 960, 128)
ttext(ML, 1190, "情境試算，假設報酬固定，非投資建議。", font(SANS_L, 22), GRAY, 2)
ttext(ML, 1228, "報酬更低、或中斷更久，結論會不同。", font(SANS_L, 22), GRAY, 2)
save(8)
print("ok")
