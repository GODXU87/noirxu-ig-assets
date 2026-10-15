"""NOIRXU IG 固定視覺：日式商務高級風 (v1)

用法：
    import noirxu_style as ns
    ns.new_slide(ns.PAPER)
    ns.frame(1, total=8)           # 輪播用；單圖用 ns.frame(2, label="No.02")
    ns.ttext(ns.ML, 300, "標題", ns.font(ns.SERIF_L, 96), ns.INK, 10)
    ns.save("/path/out", "name.png")

規則：色彩只用 PAPER/INK/GRAY/HAIR + 朱紅 VERM（重點與印章）；深藍 INDIGO 只用於「最重要數字」的滿版頁。
字體：標題細宋體(Light/Medium)加寬字距，小字細黑體(Light/Regular)。數字用細字重。
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

S = 2                      # 2x 超取樣，輸出時縮回 1080x1350
W, H = 1080, 1350
FD = "/usr/share/fonts/opentype/noto/"
SERIF_XL = FD + "NotoSerifCJK-ExtraLight.ttc"
SERIF_L = FD + "NotoSerifCJK-Light.ttc"
SERIF_M = FD + "NotoSerifCJK-Medium.ttc"
SERIF_SB = FD + "NotoSerifCJK-SemiBold.ttc"
SANS_L = FD + "NotoSansCJK-Light.ttc"
SANS_R = FD + "NotoSansCJK-Regular.ttc"

PAPER, INK, GRAY, HAIR = "#F3F3F3", "#202020", "#6E6E6E", "#D4D4D4"
VERM, VERM_T = "#000000", "#E3E3E3"   # v2：不再有彩色強調，VERM＝純黑（重點）
INDIGO, INDIGO_L, INDIGO_H = "#0E0E0E", "#A6A6A6", "#3B3B3B"   # v2：深色頁＝黑
PAPER2 = "#E8E8E8"         # 淺灰底（清單頁用）
BAR = "#B9B9B9"            # 非重點長條＝灰，重點＝黑
ML, MR = 118, W - 90       # 左右邊界

im = d = None
DARK = False
_idx = {}


def _tc(path):
    if path in _idx:
        return _idx[path]
    for i in range(10):
        try:
            f = ImageFont.truetype(path, 20, index=i)
        except Exception:
            break
        if "TC" in " ".join(f.getname()):
            _idx[path] = i
            return i
    _idx[path] = 0
    return 0


def font(path, size):
    return ImageFont.truetype(path, int(size * S), index=_tc(path))


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def P(pts):
    return [(x * S, y * S) for x, y in pts]


def new_slide(bg, dark=False):
    global im, d, DARK
    DARK = dark
    im = Image.new("RGB", (W * S, H * S), hexc(bg))
    d = ImageDraw.Draw(im)
    return im, d


def ttext(x, y, s, f, fill, track=0, anchor="l"):
    adv = [d.textlength(ch, font=f) / S + track for ch in s]
    total = sum(adv) - track
    if anchor == "c":
        x -= total / 2
    elif anchor == "r":
        x -= total
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


def rect(x0, y0, x1, y1, fill=None, outline=None, w=0):
    if fill == INK:            # v2：墨色長條一律畫成灰，重點（VERM=黑）才是黑
        fill = BAR
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=hexc(fill) if fill else None,
                outline=hexc(outline) if outline else None, width=int(w * S))


def seal(cx, cy, size, ch="", angle=0):
    """v2：不用印章，改為極簡 NOIRXU 字標（細框＋字距）。cx 為中心，右緣不超過 MR。"""
    w, h = size * 1.9, size * 0.5
    cx = min(cx, MR - w / 2)
    col = "#F2F2F2" if DARK else INK
    d.rectangle([(cx - w / 2) * S, (cy - h / 2) * S, (cx + w / 2) * S, (cy + h / 2) * S], outline=hexc(col), width=int(1.6 * S))
    f = font(SANS_R, size * 0.17)
    ttext(cx, cy - size * 0.1, "NOIRXU", f, col, 6, "c")

def frame(n, total=None, label=None, side="MONEY　停扣成本"):
    """固定外框：頂部 NOIRXU + 頁碼 + 細線，左側直書標籤。"""
    ink = "#F2F2F2" if DARK else INK
    gray = INDIGO_L if DARK else GRAY
    hair = INDIGO_H if DARK else INK
    ttext(ML, 56, "NOIRXU", font(SANS_R, 22), ink, 7)
    right = label if label else f"{n:02d} / {total:02d}"
    ttext(MR, 56, right, font(SANS_L, 22), gray, 4, "r")
    hline(ML, MR, 100, hair, 1.2)
    rect(44, 150, 52, 158, fill=VERM)
    vtext(48, 180, side, font(SANS_L, 21), gray, 9)
    ttext(MR, 1310, "noirxu.com", font(SANS_L, 20), gray, 3, "r")


def grain(img):
    noise = Image.effect_noise(img.size, 10).convert("RGB")
    return Image.blend(img, ImageChops.multiply(img, noise.point(lambda v: 240 + v // 24)), 0.12)


def save(outdir, name):
    os.makedirs(outdir, exist_ok=True)
    grain(im).resize((W, H), Image.LANCZOS).save(os.path.join(outdir, name))


def stat_row(y, items):
    """三欄數字列。items = [(標籤, 數值, 單位, 是否朱紅強調), ...]"""
    hline(ML, MR, y, INK, 1.2)
    colw = (MR - ML) / 3
    for k, (lab, val, unit, hi) in enumerate(items):
        x = ML + k * colw
        ttext(x, y + 22, lab, font(SANS_L, 24), GRAY, 3)
        w = ttext(x, y + 62, val, font(SERIF_L, 70), VERM if hi else INK, 1)
        ttext(x + w + 8, y + 94, unit, font(SERIF_M, 30), VERM if hi else INK, 0)


def matrix(y0, hollow_cols=(), cols=30, rows=12):
    """30x12 方陣 = 360 個月。空心朱紅方格 = 停扣的月份（以欄為單位）。"""
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


def compound_series(skip=None, months=360, pmt=1.0, annual=0.06):
    """每月投入 pmt（萬）、年化 annual、按月複利；skip=(a,b) 表示第 a+1..b 月不投。回傳每月終值（萬）。"""
    m = (1 + annual) ** (1 / 12) - 1
    b, out = 0.0, [0.0]
    for i in range(1, months + 1):
        b *= 1 + m
        if not (skip and skip[0] < i <= skip[1]):
            b += pmt
        out.append(b)
    return out
