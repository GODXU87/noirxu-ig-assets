"""NOIRXU Reel 共用模組（1080x1920、純字幕、無配音）。
場景：text_scene / bars_scene(動畫長條) / bignum_scene。build() 組成 mp4 並輸出封面。
所有數字由呼叫端用程式算出後傳入。"""
import os, shutil, subprocess
import noirxu_style as ns
from noirxu_style import (PAPER, INK, GRAY, HAIR, VERM, INDIGO, INDIGO_L, INDIGO_H, PAPER2,
                          SERIF_XL, SERIF_L, SERIF_M, SERIF_SB, SANS_L, SANS_R, ML, MR, font)
from PIL import Image

ns.H = 1920
LIGHT, VERM_L = "#F3F0EA", "#E4A39C"
FPS, FADE = 30, 0.3

def done():
    return ns.im.resize((1080, 1920), Image.LANCZOS)

def tag(side, dark=False):
    ns.ttext(ML, 300, "NOIRXU", font(SANS_R, 26), LIGHT if dark else INK, 8)
    ns.ttext(MR, 300, side, font(SANS_L, 24), INDIGO_L if dark else GRAY, 4, "r")
    ns.hline(ML, MR, 345, INDIGO_H if dark else INK, 1.2)

def text_scene(side, lines, bg=PAPER, seal=False, foot=None, y0=620, dark=False, rule=None):
    """lines: [(文字, 字體路徑, 大小, 顏色, 字距, 與上一行的距離)]；文字可為 [(片段, 顏色), ...] 以混色。"""
    ns.new_slide(bg, dark=dark); tag(side, dark)
    y = y0
    for text, fp, sz, col, tr, gap in lines:
        y += gap
        if isinstance(text, list):
            x = ML
            for seg, c in text:
                x += ns.ttext(x, y, seg, font(fp, sz), c, tr) + tr
        else:
            ns.ttext(ML, y, text, font(fp, sz), col, tr)
    if rule is not None:
        ns.rect(ML, rule, ML + 64, rule + 4, fill=VERM)
    if seal:
        ns.seal(MR - 60, 1430, 100)
    if foot:
        ns.ttext(ML, 1500, foot, font(SANS_L, 24), INDIGO_L if dark else GRAY, 2)
    return done()

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

def bignum_scene(side, label, number, unit, sub1, sub2=None, dark=True, accent=False):
    bg = INDIGO if dark else PAPER
    ns.new_slide(bg, dark=dark); tag(side, dark)
    ink = LIGHT if dark else INK
    ns.ttext(ML, 560, label, font(SERIF_M, 62), ink, 8)
    size = 330
    while ns.tw(number, font(SERIF_XL if dark else SERIF_L, size), 2) > 700 and size > 120: size -= 10
    w = ns.ttext(ML - 6, 650, number, font(SERIF_XL if dark else SERIF_L, size), (VERM if (accent and not dark) else ink), 2)
    ns.ttext(ML + w + 8, 650 + int(size * 0.62), unit, font(SERIF_M, 78), ink, 0)
    ns.hline(ML, MR, 1130, INDIGO_H if dark else INK, 1.2)
    ns.ttext(ML, 1180, sub1, font(SERIF_M, 50), ink, 5)
    if sub2: ns.ttext(ML, 1260, sub2, font(SERIF_M, 50), VERM_L if dark else VERM, 5)
    return done()

def anim(fn, frames=48):
    """fn(k) → 影像，k 由 0 到 1，使用 ease-out。"""
    out = []
    for i in range(frames + 1):
        t = i / frames
        out.append(fn(1 - (1 - t) ** 3))
    return out

def build(scenes, outdir, name):
    """scenes: [(單張影像或影格清單, 秒數)]"""
    seq = []
    for imgs, dur in scenes:
        imgs = imgs if isinstance(imgs, list) else [imgs]
        n = int(dur * FPS)
        seq.append(imgs[:n] + [imgs[-1]] * max(0, n - len(imgs)))
    fn = int(FADE * FPS); frames = []
    for i, s in enumerate(seq):
        for j, f in enumerate(s):
            if i + 1 < len(seq) and j >= len(s) - fn:
                f = Image.blend(f, seq[i + 1][0], (j - (len(s) - fn) + 1) / (fn + 1))
            frames.append(f)
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, "frames_" + name); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    last = lastp = None
    for k, f in enumerate(frames):
        p = os.path.join(tmp, f"f{k:04d}.jpg")
        if f is last: shutil.copyfile(lastp, p)
        else: f.save(p, quality=95, subsampling=0); last, lastp = f, p
    mp4 = os.path.join(outdir, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart",
                    "-r", str(FPS), mp4], check=True)
    frames[0].save(os.path.join(outdir, name + "_cover.png"))
    shutil.rmtree(tmp)
    print(name, len(frames) / FPS, "sec")
    return mp4
