"""NOIRXU Reel 共用模組（1080x1920、純字幕、無配音）。
場景：text_scene / bars_scene(動畫長條) / bignum_scene。build() 組成 mp4 並輸出封面。
所有數字由呼叫端用程式算出後傳入。"""
import os, shutil, subprocess
import noirxu_style as ns
from noirxu_style import (PAPER, INK, GRAY, HAIR, VERM, INDIGO, INDIGO_L, INDIGO_H, PAPER2,
                          SERIF_XL, SERIF_L, SERIF_M, SERIF_SB, SANS_L, SANS_R, ML, MR, font)
from PIL import Image, ImageChops

ns.H = 1920
LIGHT, VERM_L = "#F2F2F2", "#B8B8B8"
FPS, FADE = 30, 0.3

import io
class Seq:
    """壓縮影格暫存（避免整支影片的影格同時佔用記憶體）。"""
    def __init__(self, imgs=None):
        self.b = []
        for im in (imgs or []): self.add(im)
    def add(self, im):
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=96, subsampling=0); self.b.append(buf.getvalue())
    def __len__(self): return len(self.b)
    def __getitem__(self, i):
        i = max(0, min(len(self.b) - 1, i)); return Image.open(io.BytesIO(self.b[i])).convert("RGB")

def done():
    return ns.im.resize((1080, 1920), Image.LANCZOS)

def tag(side, dark=False):
    ns.ttext(ML, 300, "NOIRXU", font(SANS_R, 26), LIGHT if dark else INK, 8)
    ns.ttext(MR, 300, side, font(SANS_L, 24), INDIGO_L if dark else GRAY, 4, "r")
    ns.hline(ML, MR, 345, INDIGO_H if dark else INK, 1.2)

def _draw_line(y, text, fp, sz, col, tr):
    if isinstance(text, list):
        x = ML
        for seg, c in text:
            x += ns.ttext(x, y, seg, font(fp, sz), c, tr) + tr
    else:
        ns.ttext(ML, y, text, font(fp, sz), col, tr)

def _ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def _reveal(bg, dark, side, parts, chrome_after=None, stagger=0.32, dur=0.5, rise=46, t0=0.12, total=None):
    """parts: [callable] 各自在空白版面（含頁首）上畫一個元素；逐個淡入並上浮。回傳影格清單。"""
    def blank():
        ns.new_slide(bg, dark=dark); tag(side, dark)
    blank(); B = done()
    if chrome_after:
        blank(); chrome_after(); C = done()
    else:
        C = None
    mC = ImageChops.difference(C, B).convert("L").point(lambda v: min(255, v * 10)) if C is not None else None
    layers = []
    for fn in parts:
        blank(); fn(); L = done()
        m = ImageChops.difference(L, B).convert("L").point(lambda v: min(255, v * 10))
        layers.append((L, m))
    n_total = int((total or (t0 + stagger * len(parts) + dur + 0.3)) * FPS)
    frames = Seq()
    for f in range(n_total):
        t = f / FPS; fr = B.copy()
        for i, (L, m) in enumerate(layers):
            k = _ease((t - t0 - stagger * i) / dur)
            if k <= 0: continue
            dy = int(rise * (1 - k))
            mm = m.point(lambda v, k=k: int(v * k))
            fr.paste(L, (0, dy), mm)
        if C is not None:
            k = _ease((t - (t0 + stagger * len(parts) + 0.1)) / 0.5)
            if k > 0: fr.paste(C, (0, 0), mC.point(lambda v, k=k: int(v * k)))
        frames.add(fr)
    return frames

def text_scene(side, lines, bg=PAPER, seal=False, foot=None, y0=620, dark=False, rule=None):
    """lines: [(文字, 字體路徑, 大小, 顏色, 字距, 與上一行的距離)]；文字可為 [(片段, 顏色), ...] 以混色。
    回傳影格清單：每行文字依序淡入上浮，印章/頁尾最後出現。"""
    ys, y = [], y0
    for ln in lines:
        y += ln[5]; ys.append(y)
    parts = []
    for (text, fp, sz, col, tr, gap), yy in zip(lines, ys):
        parts.append(lambda text=text, fp=fp, sz=sz, col=col, tr=tr, yy=yy: _draw_line(yy, text, fp, sz, col, tr))
    def tail():
        if rule is not None:
            ns.rect(ML, rule, ML + 64, rule + 4, fill=VERM)
        if seal:
            ns.seal(MR - 60, 1430, 100)
        if foot:
            ns.ttext(ML, 1500, foot, font(SANS_L, 24), INDIGO_L if dark else GRAY, 2)
    return _reveal(bg, dark, side, parts, chrome_after=tail if (rule is not None or seal or foot) else None)

def bars_scene(side, title, items, unit, k=1.0, fmt="{:.1f}", foot=None, hi=None):
    """items: [(標籤, 副標, 數值)]；長條從 0 起算，k=0..1 為動畫進度；hi=要用朱紅的項目索引。"""
    ns.new_slide(PAPER); tag(side)
    y = 440
    for t in title:
        ns.ttext(ML, y, t, font(SERIF_L, 66), INK, 6); y += 100
    mx = max(v for _, _, v in items)
    n = len(items); rowh = min(210, int(760 / n)); y = 760
    for i, (lab, sub, v) in enumerate(items):
        ns.hline(ML, MR, y, INK if i == 0 else HAIR, 1.2)
        ns.ttext(ML, y + 22, lab, font(SANS_R, 34), INK, 4)
        if sub: ns.ttext(MR, y + 28, sub, font(SANS_L, 26), GRAY, 2, "r")
        bw = 560 * (v / mx) * k
        col = VERM if (hi is not None and i == hi) else INK
        ns.rect(ML, y + 82, ML + max(bw, 2), y + 122, fill=col)
        ns.ttext(ML + bw + 20, y + 66, fmt.format(v * k), font(SERIF_L, 62), col, 1)
        ns.ttext(MR, y + 100, unit, font(SANS_L, 26), GRAY, 2, "r")
        y += rowh
    ns.hline(ML, MR, y, INK, 1.2)
    if foot: ns.ttext(ML, y + 30, foot, font(SANS_L, 24), GRAY, 2)
    return done()

def _num_parts(number):
    import re
    m = re.fullmatch(r"(\d+)(?:\.(\d+))?", number)
    return (float(number), len(m.group(2)) if m.group(2) else 0) if m else None

def bignum_scene(side, label, number, unit, sub1, sub2=None, dark=True, accent=False):
    """回傳影格清單：標籤淡入 → 大數字由 0 滾動到目標 → 分隔線與說明逐行浮現。"""
    bg = INDIGO if dark else PAPER
    ink = LIGHT if dark else INK
    fnt_path = SERIF_XL if dark else SERIF_L
    size = 330
    while ns.tw(number, font(fnt_path, size), 2) > 700 and size > 120: size -= 10
    ncol = VERM if (accent and not dark) else ink
    def draw_num(txt):
        w = ns.ttext(ML - 6, 650, txt, font(fnt_path, size), ncol, 2)
        ns.ttext(ML + w + 8, 650 + int(size * 0.62), unit, font(SERIF_M, 78), ink, 0)
    parts = [lambda: ns.ttext(ML, 560, label, font(SERIF_M, 62), ink, 8),
             lambda: ns.hline(ML, MR, 1130, INDIGO_H if dark else INK, 1.2),
             lambda: ns.ttext(ML, 1180, sub1, font(SERIF_M, 50), ink, 5)]
    if sub2: parts.append(lambda: ns.ttext(ML, 1260, sub2, font(SERIF_M, 50), VERM_L if dark else VERM, 5))
    base = _reveal(bg, dark, side, parts, stagger=0.4, dur=0.5, t0=0.1 + 0.0, total=3.4)
    # 大數字：第 0.35 秒起滾動 1.2 秒（ease-out），之後固定
    np_ = _num_parts(number)
    def num_img(txt):
        ns.new_slide(bg, dark=dark); tag(side, dark); draw_num(txt); return done()
    blank = None
    ns.new_slide(bg, dark=dark); tag(side, dark); blankimg = done()
    out = Seq()
    for f in range(len(base)):
        fr = base[f]
        t = f / FPS
        if t < 0.35: out.add(fr); continue
        k = _ease((t - 0.35) / 1.2)
        txt = number if (np_ is None or k >= 1) else f"{np_[0] * k:.{np_[1]}f}"
        if np_ is None: k = 1.0
        n_img = num_img(txt)
        m = ImageChops.difference(n_img, blankimg).convert("L").point(lambda v: min(255, v * 10))
        a = _ease((t - 0.35) / 0.4)
        fr = fr.copy(); fr.paste(n_img, (0, int(30 * (1 - a))), m.point(lambda v, a=a: int(v * a)))
        out.add(fr)
    return out

def anim(fn, frames=48):
    """fn(k) → 影像，k 由 0 到 1，使用 ease-out。"""
    out = Seq()
    for i in range(frames + 1):
        t = i / frames
        out.add(fn(1 - (1 - t) ** 3))
    return out

def _zoom(img, k):
    if k <= 1.0001: return img
    W, H = img.size; w, h = W / k, H / k
    l, t = (W - w) / 2, (H - h) / 2
    return img.resize((W, H), Image.BICUBIC, box=(l, t, l + w, t + h))

def _io(t):  # ease-in-out
    t = max(0.0, min(1.0, t)); return 3 * t * t - 2 * t * t * t

def _transition(kind, a, b, p):
    W, H = a.size; p = _io(p)
    if kind == "push":      # 上推：舊頁上移離開、新頁自下方進入
        c = Image.new("RGB", (W, H)); dy = int(H * p)
        c.paste(a, (0, -dy)); c.paste(b, (0, H - dy)); return c
    if kind == "wipe":      # 左到右擦除，邊緣一條細線
        x = int(W * p); c = a.copy()
        if x > 0: c.paste(b.crop((0, 0, x, H)), (0, 0))
        if 0 < x < W:
            from PIL import ImageDraw
            ImageDraw.Draw(c).rectangle([x - 1, 0, x + 1, H], fill=(20, 20, 20))
        return c
    # zoom：舊頁微放大並淡出，新頁淡入
    return Image.blend(_zoom(a, 1 + 0.10 * p), _zoom(b, 0.94 + 0.06 * p) if False else b, p)

KINDS = ["push", "wipe", "zoom", "push", "wipe"]
KB = 0.035  # 場景內緩慢推進（Ken Burns）幅度

def build(scenes, outdir, name):
    """scenes: [(單張影像或影格序列, 秒數)]。每場景緩慢推進；換場輪流用 上推/擦除/縮放。邊算邊寫檔。"""
    seq = []
    for imgs, dur in scenes:
        n = int(dur * FPS)
        if not hasattr(imgs, "__getitem__") or isinstance(imgs, Image.Image): imgs = Seq([imgs])
        elif isinstance(imgs, list): imgs = Seq(imgs)
        seq.append((imgs, n))
    T = int(0.5 * FPS)
    def get(i, j):
        im, n = seq[i]; return _zoom(im[min(j, len(im) - 1)], 1 + KB * (j / n))
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, "frames_" + name); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    k = 0
    for i, (im, n) in enumerate(seq):
        for j in range(n):
            if i + 1 < len(seq) and j >= n - T:
                q = j - (n - T)
                f = _transition(KINDS[i % len(KINDS)], get(i, j), seq[i + 1][0][0], (q + 1) / (T + 1))
            else:
                f = get(i, j)
            f.save(os.path.join(tmp, f"f{k:04d}.jpg"), quality=95, subsampling=0); k += 1
    mp4 = os.path.join(outdir, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart",
                    "-r", str(FPS), mp4], check=True)
    seq[0][0][min(len(seq[0][0]) - 1, int(2.0 * FPS))].save(os.path.join(outdir, name + "_cover.png"))
    shutil.rmtree(tmp)
    print(name, k / FPS, "sec")
    return mp4
