"""NOIRXU Reels 環境音：合成（無版權）。python3 -I reel_audio.py IN_DIR OUT_DIR"""
import sys, os, subprocess, numpy as np
from scipy.io import wavfile
SR = 44100
def note(f, dur, t0, total, amp, decay=2.2):
    n = int(total * SR); out = np.zeros(n)
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * decay) * np.minimum(1, t / 0.005)
    s = (np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t) + 0.1*np.sin(2*np.pi*3.01*f*t)) * env * amp
    i = int(t0 * SR); e = min(n, i + len(s)); out[i:e] += s[:e-i]
    return out
def pad(total, seed):
    t = np.arange(int(total * SR)) / SR
    freqs = [110.0, 164.81, 220.0, 246.94, 329.63]  # A2 E3 A3 B3 E4 (A sus/9)
    sig = np.zeros_like(t)
    for k, f in enumerate(freqs):
        lfo = 0.5 + 0.5 * np.sin(2*np.pi*(0.07 + 0.03*k)*t + k + seed)
        sig += (np.sin(2*np.pi*f*t) + 0.4*np.sin(2*np.pi*f*1.002*t)) * (0.35 + 0.65*lfo) * (0.9 if k < 2 else 0.5)
    return sig / len(freqs)
def make(total, seed):
    rng = np.random.default_rng(seed)
    x = pad(total, seed) * 0.55
    scale = [440.0, 493.88, 554.37, 659.25, 739.99, 880.0]  # A major-pentatonic-ish, airy
    t0 = 0.6
    while t0 < total - 1.5:
        x += note(float(rng.choice(scale)), 2.8, t0, total, 0.12)
        t0 += float(rng.uniform(1.6, 2.8))
    # soft sub-tap at 0.0 to anchor
    x += note(55.0, 1.0, 0.0, total, 0.25, decay=4)
    fade = int(1.2 * SR); x[:int(0.3*SR)] *= np.linspace(0, 1, int(0.3*SR)); x[-fade:] *= np.linspace(1, 0, fade)
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.5
    return x
if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
    for i, fn in enumerate(sorted(f for f in os.listdir(src) if f.endswith(".mp4"))):
        d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",os.path.join(src,fn)]))
        wav = os.path.join(dst, fn[:-4] + ".wav")
        wavfile.write(wav, SR, (make(d, 7 + i) * 32767).astype(np.int16))
        subprocess.check_call(["ffmpeg","-v","error","-y","-i",os.path.join(src,fn),"-i",wav,"-c:v","copy","-c:a","aac","-b:a","160k","-shortest",os.path.join(dst,fn)])
        os.remove(wav); print(fn, round(d,1))
