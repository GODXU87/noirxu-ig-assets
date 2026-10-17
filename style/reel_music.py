"""NOIRXU Reels 配樂 v4：明亮流行律動（原創，非任何現有歌曲）——
馬林巴 riff + 彈性貝斯 + 切分鼓組，96 BPM，C-G-Am-F。python3 -I reel_music.py IN_DIR OUT_DIR"""
import sys, os, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter, fftconvolve
SR = 44100; BPM = 96
def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def filt(x, fc, kind="low", o=2): b, a = butter(o, fc / (SR / 2), kind); return lfilter(b, a, x)
def marimba(m, dur=0.5, vel=1.0):
    f = mf(m); t = np.arange(int(dur * SR)) / SR
    s = np.sin(2*np.pi*f*t)*np.exp(-t*7) + 0.35*np.sin(2*np.pi*f*4*t)*np.exp(-t*22) + 0.08*np.sin(2*np.pi*f*10*t)*np.exp(-t*60)
    return s * np.minimum(1, t / 0.002) * vel
def bass(m, dur=0.4, vel=1.0):
    f = mf(m); t = np.arange(int(dur * SR)) / SR
    s = (np.sin(2*np.pi*f*t) + 0.3*np.sin(4*np.pi*f*t)) * np.exp(-t*5.5)
    return s * np.minimum(1, t / 0.004) * np.minimum(1, (dur - t) / 0.03) * vel
def chord(ms, dur):
    t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for m in ms:
        f = mf(m); s += np.sin(2*np.pi*f*t) + 0.4*np.sin(2*np.pi*f*1.004*t) + 0.2*np.sin(4*np.pi*f*t)
    return filt(s / len(ms), 2200) * np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.05)
def kick():
    t = np.arange(int(0.28 * SR)) / SR
    return np.sin(2*np.pi*(46*t + 90*(1-np.exp(-t*45))/45)) * np.exp(-t*13)
def clap(rng):
    t = np.arange(int(0.2 * SR)) / SR; n = filt(rng.standard_normal(len(t)), 1100, "high")
    env = sum(np.exp(-np.maximum(t - d, 0) * 40) * (t >= d) for d in (0, 0.011, 0.022)) * 0.5 + np.exp(-t * 18) * 0.5
    return n * env * 0.7
def hat(rng, o=False):
    t = np.arange(int((0.16 if o else 0.04) * SR)) / SR
    return filt(rng.standard_normal(len(t)), 7000, "high") * np.exp(-t * (22 if o else 90))
def put(buf, s, t0, g):
    i = int(t0 * SR)
    if i >= len(buf): return
    e = min(len(buf), i + len(s)); buf[i:e] += s[:e - i] * g
PROG = [(48, [60, 64, 67], [72, 76, 79, 84]), (43, [59, 62, 67], [67, 71, 74, 79]),
        (45, [57, 60, 64], [69, 72, 76, 81]), (41, [57, 60, 65], [69, 72, 77, 81])]
RH = [0, 3, 6, 8, 10, 12, 14]; CON = [2, 3, 2, 0, 1, 2, 1]; CON2 = [2, 3, 1, 0, 2, 3, 1]
def make(total, seed=1):
    rng = np.random.default_rng(seed); n = int(total * SR)
    mel = np.zeros(n); low = np.zeros(n); dr = np.zeros(n); pad = np.zeros(n); kk = np.zeros(n)
    e8 = 60 / BPM / 2; s16 = e8 / 2; bar = 8 * e8; k = 0
    while k * bar < total - 0.3:
        t0 = k * bar; root, ch, arp = PROG[k % 4]; con = CON if (k // 4) % 2 == 0 else CON2
        put(pad, chord(ch, bar * 0.98), t0, 0.5)
        for st, c in zip(RH, con):
            put(mel, marimba(arp[c], 0.45, 0.8 + 0.2 * (st % 4 == 0)), t0 + st * s16, 0.30)
        put(low, bass(root, e8 * 2.6, 1.0), t0, 0.55)
        put(low, bass(root, e8 * 1.5, 0.8), t0 + 3 * e8, 0.45)
        put(low, bass(root + (7 if k % 2 else 0), e8 * 1.4, 0.8), t0 + 6 * e8, 0.40)
        for ke in (0, 3, 6):
            put(dr, kick(), t0 + ke * e8, 0.75); put(kk, np.ones(int(0.18 * SR)), t0 + ke * e8, 1.0)
        put(dr, clap(rng), t0 + 4 * e8, 0.45); put(dr, clap(rng), t0 + 7 * e8 + s16, 0.12)
        for s in range(16):
            put(dr, hat(rng, s % 8 == 6), t0 + s * s16 + (0.012 if s % 2 else 0), 0.10 if s % 4 else 0.15)
        k += 1
    duck = 1 - 0.6 * np.minimum(1, filt(kk, 18, "low", 1) * 6)       # 側鏈壓縮
    ir = rng.standard_normal(int(0.9 * SR)) * np.exp(-np.arange(int(0.9 * SR)) / SR * 6); ir = filt(ir, 4000)
    wet = fftconvolve(mel, ir)[:n] * 0.05
    x = (pad * 0.55 * np.clip(duck, 0.3, 1)) + mel + wet + low + dr * 0.9
    x = np.tanh(x * 1.2) / 1.2
    fi = int(0.2 * SR); fo = int(1.2 * SR); x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    return x / (np.max(np.abs(x)) + 1e-9) * 0.7
if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
    for i, fn in enumerate(sorted(f for f in os.listdir(src) if f.endswith(".mp4"))):
        d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",os.path.join(src,fn)]))
        wav = os.path.join(dst, fn[:-4] + ".wav")
        wavfile.write(wav, SR, (make(d, 1 + i) * 32767).astype(np.int16))
        subprocess.check_call(["ffmpeg","-v","error","-y","-i",os.path.join(src,fn),"-i",wav,"-af","loudnorm=I=-16:TP=-1.5:LRA=7","-ar","44100","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",os.path.join(dst,fn)])
        os.remove(wav); print(fn, round(d,1))
