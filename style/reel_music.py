"""NOIRXU Reels 配樂 v2：合成 lo-fi 電鋼琴 + 輕節拍（無版權）。
python3 -I reel_music.py IN_DIR OUT_DIR [bpm]"""
import sys, os, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter, fftconvolve
SR = 44100
def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, fc, o=2): b, a = butter(o, fc / (SR / 2), "low"); return lfilter(b, a, x)
def hp(x, fc, o=2): b, a = butter(o, fc / (SR / 2), "high"); return lfilter(b, a, x)
def epiano(m, dur, vel=1.0):
    f = mf(m); t = np.arange(int(dur * SR)) / SR
    idx = 1.6 * vel * np.exp(-t * 5.0) + 0.25
    mod = np.sin(2 * np.pi * f * 1.0 * t) * idx
    car = np.sin(2 * np.pi * f * t + mod)
    tine = 0.12 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t * 28)
    env = np.exp(-t * 2.3) * np.minimum(1, t / 0.004) * np.minimum(1, (dur - t) / 0.15)
    return (car + tine) * env * vel
def bass(m, dur):
    f = mf(m); t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 2.6) * np.minimum(1, t / 0.01)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)) * env
def kick():
    t = np.arange(int(0.35 * SR)) / SR
    return np.sin(2 * np.pi * (48 * t + 70 * (1 - np.exp(-t * 40)) / 40)) * np.exp(-t * 11)
def snare(rng):
    t = np.arange(int(0.22 * SR)) / SR
    return hp(rng.standard_normal(len(t)), 1200) * np.exp(-t * 22) * 0.6 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.3
def hat(rng):
    t = np.arange(int(0.06 * SR)) / SR
    return hp(rng.standard_normal(len(t)), 6500) * np.exp(-t * 70)
def put(buf, s, t0, g):
    i = int(t0 * SR)
    if i >= len(buf): return
    e = min(len(buf), i + len(s)); buf[i:e] += s[:e - i] * g
CHORDS = [(33, [60, 64, 67, 71]), (29, [57, 60, 64, 67]), (36, [55, 59, 64, 67]), (31, [59, 62, 64, 67])]  # Am9 Fmaj7 Cmaj7 G6
MEL = [76, 74, 72, 71, 69, 67]
def make(total, seed=3, bpm=84):
    rng = np.random.default_rng(seed); n = int(total * SR)
    keys = np.zeros(n); drums = np.zeros(n); beat = 60 / bpm; bar = 4 * beat
    k = 0
    while k * bar < total - 0.5:
        root, ch = CHORDS[k % 4]; t0 = k * bar
        for j, m in enumerate(ch):                       # 微琶音，像真人彈
            put(keys, epiano(m, bar * 0.95, 0.8), t0 + j * 0.018, 0.16)
        for j, m in enumerate(ch[1:]):
            put(keys, epiano(m, beat * 1.4, 0.6), t0 + 2.5 * beat + j * 0.02 + 0.01, 0.10)
        put(keys, bass(root, bar * 0.9), t0, 0.34)
        put(keys, bass(root, beat * 1.2), t0 + 2.5 * beat, 0.22)
        if k % 2 == 1:                                    # 偶爾一個旋律音
            put(keys, epiano(float(rng.choice(MEL)), beat * 2, 0.7), t0 + 3 * beat, 0.11)
        put(drums, kick(), t0, 0.55); put(drums, kick(), t0 + 2.5 * beat, 0.4)
        put(drums, snare(rng), t0 + beat, 0.26); put(drums, snare(rng), t0 + 3 * beat, 0.26)
        for s in range(8):
            put(drums, hat(rng), t0 + s * beat / 2 + (0.035 if s % 2 else 0), 0.10 if s % 2 else 0.16)
        k += 1
    ir = rng.standard_normal(int(1.4 * SR)) * np.exp(-np.arange(int(1.4 * SR)) / SR * 3.2); ir = lp(ir, 3500)
    wet = fftconvolve(keys, ir)[:n] * 0.035
    x = lp(keys + wet, 4800) + lp(drums, 9000) * 0.9
    x = np.tanh(x * 1.5) / 1.5                           # 輕微磁帶飽和
    x += lp(rng.standard_normal(n), 7000) * 0.0025       # 極輕底噪
    fi = int(0.4 * SR); fo = int(1.6 * SR); x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    return x / (np.max(np.abs(x)) + 1e-9) * 0.55
if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]; bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 84
    os.makedirs(dst, exist_ok=True)
    for i, fn in enumerate(sorted(f for f in os.listdir(src) if f.endswith(".mp4"))):
        d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",os.path.join(src,fn)]))
        wav = os.path.join(dst, fn[:-4] + ".wav")
        wavfile.write(wav, SR, (make(d, 3 + i, bpm) * 32767).astype(np.int16))
        subprocess.check_call(["ffmpeg","-v","error","-y","-i",os.path.join(src,fn),"-i",wav,"-c:v","copy","-c:a","aac","-b:a","192k","-shortest",os.path.join(dst,fn)])
        os.remove(wav); print(fn, round(d,1))
