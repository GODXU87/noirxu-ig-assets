"""NOIRXU Reels 配樂 v3：日式商務風——留白、柔軟鋼琴 + 箏撥弦 + 暖 pad，無鼓。
音階：平調子（Hirajoshi）D E F A Bb。python3 -I reel_music.py IN_DIR OUT_DIR"""
import sys, os, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter, fftconvolve
SR = 44100
def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, fc, o=2): b, a = butter(o, fc / (SR / 2), "low"); return lfilter(b, a, x)
def piano(m, dur, vel=1.0):
    """柔軟（felt）鋼琴：低泛音為主，緩衰減。"""
    f = mf(m); t = np.arange(int(dur * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.1 + 0.9 * k)) for k, a in ((1, 1), (2, .42), (3, .16), (4, .07)))
    return s * np.minimum(1, t / 0.006) * np.minimum(1, (dur - t) / 0.2) * vel
def koto(m, dur=3.2, vel=1.0, seed=0):
    """Karplus-Strong 撥弦，近似箏。"""
    f = mf(m); n = int(dur * SR); N = int(SR / f); rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, N); buf = lp(buf, 6000, 1); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % N]
        buf[i % N] = 0.4985 * (buf[i % N] + buf[(i + 1) % N])
    return out * vel * np.minimum(1, (dur * SR - np.arange(n)) / (0.3 * SR))
def pad(total, notes):
    t = np.arange(int(total * SR)) / SR; sig = np.zeros_like(t)
    for k, m in enumerate(notes):
        f = mf(m); lfo = 0.55 + 0.45 * np.sin(2 * np.pi * (0.045 + 0.02 * k) * t + k * 1.7)
        sig += (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.003 * t)) * lfo
    return lp(sig / len(notes), 1400)
def put(buf, s, t0, g):
    i = int(t0 * SR)
    if i >= len(buf): return
    e = min(len(buf), i + len(s)); buf[i:e] += s[:e - i] * g
SCALE = [62, 64, 65, 69, 70, 74, 76, 77, 81]   # D E F A Bb 上下八度
PHR = [  # 每句 (拍位, 音) 以秒為單位，刻意留白
    [(0.0, 74), (1.5, 70), (3.0, 69)],
    [(0.5, 77), (2.0, 74), (4.0, 65)],
    [(0.0, 69), (1.8, 70), (3.2, 74)],
    [(1.0, 76), (3.0, 70)],
]
def make(total, seed=5):
    rng = np.random.default_rng(seed); n = int(total * SR)
    keys = np.zeros(n); bar = 5.6; k = 0
    while k * bar < total - 0.8:
        t0 = k * bar
        put(keys, piano(38 if k % 2 == 0 else 34, bar * 1.05, 0.9), t0, 0.30)          # D2 / Bb1 低音 ——穩
        put(keys, piano(50 if k % 2 == 0 else 46, bar * 0.9, 0.7), t0 + 0.03, 0.12)
        for dt, m in PHR[k % 4]:
            put(keys, piano(m, 3.4, 0.8), t0 + dt + float(rng.uniform(-0.04, 0.04)), 0.17)
        if k % 2 == 1:
            put(keys, koto(float(rng.choice(SCALE)) + 12, 3.2, 1.0, k), t0 + 2.6, 0.20)
        k += 1
    ped = pad(total, [38, 45, 50, 57, 62]) * 0.22
    ir_n = int(2.6 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 1.9); ir = lp(ir, 3000)
    wet = fftconvolve(keys, ir)[:n] * 0.045
    x = lp(keys + wet, 6500) + ped
    fi = int(0.8 * SR); fo = int(2.0 * SR); x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    return x / (np.max(np.abs(x)) + 1e-9) * 0.55
if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
    for i, fn in enumerate(sorted(f for f in os.listdir(src) if f.endswith(".mp4"))):
        d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",os.path.join(src,fn)]))
        wav = os.path.join(dst, fn[:-4] + ".wav")
        wavfile.write(wav, SR, (make(d, 5 + i) * 32767).astype(np.int16))
        subprocess.check_call(["ffmpeg","-v","error","-y","-i",os.path.join(src,fn),"-i",wav,"-c:v","copy","-af","loudnorm=I=-18:TP=-2:LRA=7","-ar","44100","-c:a","aac","-b:a","192k","-shortest",os.path.join(dst,fn)])
        os.remove(wav); print(fn, round(d,1))
