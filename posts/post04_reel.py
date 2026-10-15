"""Reel 1080x1920：停扣成本（純字幕、無配音）。用法：python3 -I post04_reel.py OUTDIR"""
import sys, os, shutil, subprocess
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import (PAPER, INK, GRAY, HAIR, VERM, VERM_T, INDIGO, INDIGO_L, INDIGO_H, PAPER2,
                          SERIF_XL, SERIF_L, SERIF_M, SERIF_SB, SANS_L, SANS_R, ML, MR, font)
from PIL import Image

ns.H = 1920            # 9:16
OUT = sys.argv[1]
FPS, FADE = 30, 0.3
LIGHT = "#F2F2F2"

# ---- 數字全部由程式計算 ----
a = ns.compound_series()[-1]
b = ns.compound_series(skip=(120, 144))[-1]
gap = a - b
print(f"{a:.1f} {b:.1f} {gap:.1f} 本金差 24 複利差 {gap-24:.1f}")
A, B, G, C = f"{a:.1f}", f"{b:.1f}", f"{gap:.1f}", f"{gap-24:.1f}"

def done():
    return ns.im.resize((1080, 1920), Image.LANCZOS)

def tag(dark=False):
    ns.ttext(ML, 300, "NOIRXU", font(SANS_R, 26), LIGHT if dark else INK, 8)
    ns.ttext(MR, 300, "MONEY　停扣成本", font(SANS_L, 24), INDIGO_L if dark else GRAY, 4, "r")
    ns.hline(ML, MR, 345, INDIGO_H if dark else INK, 1.2)

def s1():
    ns.new_slide(PAPER); tag()
    ns.ttext(ML, 620, "每月存 1 萬，", font(SERIF_M, 64), INK, 6)
    ns.ttext(ML, 730, "只停 2 年。", font(SERIF_L, 150), INK, 6)
    ns.rect(ML, 1010, ML + 64, 1014, fill=VERM)
    w = ns.ttext(ML, 1050, "30 年後，會差多少", font(SERIF_M, 62), INK, 6)
    ns.ttext(ML + w + 6, 1050, "？", font(SERIF_M, 62), VERM, 0)
    ns.seal(MR - 60, 1430, 100)
    return done()

XL, STEP = ML + 8, (MR - 8 - (ML + 8)) / 29
Y0 = 760
def s2(k, label=False):
    """k = 已填入的格數 (0..360)，逐年(欄)由左到右、每欄由上到下。"""
    ns.new_slide(PAPER); tag()
    ns.ttext(ML, 450, "360", font(SERIF_L, 150), INK, 2)
    ns.ttext(ML + 330, 535, "個月　＝　30 年", font(SERIF_M, 46), INK, 4)
    n = 0
    sz = 17
    for c in range(30):
        for r in range(12):
            if n >= k: break
            cx, cy = XL + c * STEP, Y0 + r * STEP
            box = [(cx - sz / 2) * ns.S, (cy - sz / 2) * ns.S, (cx + sz / 2) * ns.S, (cy + sz / 2) * ns.S]
            if c in (10, 11):
                ns.d.rectangle(box, outline=ns.hexc(VERM), width=int(2.4 * ns.S))
            else:
                ns.d.rectangle(box, fill=ns.hexc(INK))
            n += 1
    if label:
        y = 1250
        ns.d.rectangle([ML * ns.S, (y + 8) * ns.S, (ML + 20) * ns.S, (y + 28) * ns.S], fill=ns.hexc(INK))
        ns.ttext(ML + 40, y, "有投入", font(SANS_R, 34), INK, 4)
        ns.d.rectangle([(ML + 300) * ns.S, (y + 8) * ns.S, (ML + 320) * ns.S, (y + 28) * ns.S],
                       outline=ns.hexc(VERM), width=int(2.4 * ns.S))
        ns.ttext(ML + 340, y, "停扣 24 個月", font(SANS_R, 34), VERM, 4)
    return done()

def s3():
    ns.new_slide(PAPER); tag()
    ns.ttext(ML, 520, "一直投", font(SANS_R, 36), GRAY, 6)
    w = ns.ttext(ML, 590, A, font(SERIF_L, 190), INK, 2)
    ns.ttext(ML + w + 14, 690, "萬", font(SERIF_M, 64), INK, 0)
    ns.hline(ML, MR, 900, INK, 1.2)
    ns.ttext(ML, 960, "中間停 2 年", font(SANS_R, 36), GRAY, 6)
    w = ns.ttext(ML, 1030, B, font(SERIF_L, 190), VERM, 2)
    ns.ttext(ML + w + 14, 1130, "萬", font(SERIF_M, 64), VERM, 0)
    ns.ttext(ML, 1420, "每月 1 萬　年化 6%　按月複利", font(SANS_L, 28), GRAY, 3)
    return done()

def s4():
    ns.new_slide(INDIGO, dark=True); tag(True)
    ns.ttext(ML, 560, "差了", font(SERIF_M, 64), LIGHT, 8)
    w = ns.ttext(ML - 6, 650, G, font(SERIF_XL, 330), LIGHT, 2)
    ns.ttext(ML + w + 8, 860, "萬", font(SERIF_M, 80), LIGHT, 0)
    ns.hline(ML, MR, 1130, INDIGO_H, 1.2)
    ns.ttext(ML, 1180, "少投的本金，只有 24 萬。", font(SERIF_M, 52), LIGHT, 5)
    ns.ttext(ML, 1260, f"其餘 {C} 萬，是複利。", font(SERIF_M, 52), "#B8B8B8", 5)
    return done()

def s5():
    ns.new_slide(PAPER); tag()
    ns.ttext(ML, 660, "停掉的不只是本金，", font(SERIF_M, 64), INK, 6)
    ns.ttext(ML, 780, "還有它後面", font(SERIF_M, 64), INK, 6)
    ns.ttext(ML, 900, "18 到 20 年的複利。", font(SERIF_L, 80), VERM, 5)
    ns.rect(ML, 1090, ML + 64, 1094, fill=VERM)
    return done()

def s6():
    ns.new_slide(PAPER2); tag()
    ns.ttext(ML, 450, "暫停前，", font(SERIF_L, 96), INK, 8)
    ns.ttext(ML, 570, "先問三件事。", font(SERIF_M, 96), INK, 8)
    items = ["能不能只降額，不全停？", "要停幾個月？先寫下恢復日期。", "三個月後，這個原因還在嗎？"]
    y = 800
    for i, t in enumerate(items, 1):
        ns.hline(ML, MR, y, INK if i == 1 else HAIR, 1.2)
        ns.ttext(ML, y + 52, f"0{i}", font(SERIF_L, 64), VERM, 2)
        ns.ttext(ML + 120, y + 62, t, font(SERIF_M, 44), INK, 3)
        y += 150
    ns.hline(ML, MR, y, INK, 1.2)
    return done()

def s7():
    ns.new_slide(PAPER); tag()
    ns.ttext(ML, 650, "傳給那個說", font(SERIF_M, 72), INK, 8)
    ns.ttext(ML, 780, "「先停一陣子」", font(SERIF_L, 100), VERM, 6)
    ns.ttext(ML, 930, "的人。", font(SERIF_M, 72), INK, 8)
    ns.seal(MR - 70, 1250, 110)
    ns.ttext(ML, 1420, "情境試算，非投資建議。報酬更低或中斷更久，結果會不同。", font(SANS_L, 24), GRAY, 2)
    return done()

# ---- 場景：(frames 產生器, 秒數) ----
scenes = []
im1 = s1();            scenes.append(([im1], 2.8))
fill = [s2(int(360 * min(1, i / 60))) for i in range(61)]       # 2 秒填滿
final2 = s2(360, True)
scenes.append((fill + [final2], 4.6, 2.0))                      # 前 2 秒動畫，之後停住
scenes += [([s3()], 3.2), ([s4()], 3.4), ([s5()], 3.0), ([s6()], 4.2), ([s7()], 2.6)]

# ---- 展開成每幀 ----
seq = []   # 每場景的 PIL 幀清單
for sc in scenes:
    imgs, dur = sc[0], sc[1]
    n = int(dur * FPS)
    if len(imgs) == 1:
        seq.append([imgs[0]] * n)
    else:
        anim = imgs[:-1]; hold = imgs[-1]
        na = len(anim)
        seq.append(anim + [hold] * (n - na))
fn = int(FADE * FPS)
frames = []
for i, s in enumerate(seq):
    for j, f in enumerate(s):
        if i + 1 < len(seq) and j >= len(s) - fn:
            t = (j - (len(s) - fn) + 1) / (fn + 1)
            f = Image.blend(f, seq[i + 1][0], t)
        frames.append(f)
print("frames", len(frames), "sec", len(frames) / FPS)

tmp = os.path.join(OUT, "frames"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
last = None; lastp = None
for k, f in enumerate(frames):
    p = os.path.join(tmp, f"f{k:04d}.jpg")
    if f is last:
        shutil.copyfile(lastp, p)
    else:
        f.save(p, quality=95, subsampling=0); last, lastp = f, p
mp4 = os.path.join(OUT, "post04_reel.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart",
                "-r", str(FPS), mp4], check=True)
frames[0].save(os.path.join(OUT, "post04_cover.png"))
shutil.rmtree(tmp)
print("done", mp4)
