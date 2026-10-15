"""Reel AI 旁白：sherpa-onnx + MeloTTS(zh_en)，離線、無版權。
用法：python3 -I reel_voice.py IN.mp4 OUT.mp4 SPEC.json
SPEC: {"scenes":[[start_sec, dur_sec, "简体旁白"], ...]}  （模型只認簡體，旁白用簡體寫；畫面字幕維持繁體）"""
import sys, os, json, subprocess, tempfile, numpy as np
from scipy.io import wavfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_audio
TTS = "/tmp/claude-0/-home-claude-noirxu-ig-assets/d48ba390-2f52-5d77-aa46-4366d57cd1af/scratchpad/tts"
V = "1.12.20"; M = TTS + "/vits-melo-tts-zh_en"; SR = 44100
def say(text, out, scale):
    env = dict(os.environ, LD_LIBRARY_PATH=f"{TTS}/sherpa-onnx-v{V}-linux-x64-shared/lib")
    subprocess.run([f"{TTS}/sherpa-onnx-v{V}-linux-x64-shared/bin/sherpa-onnx-offline-tts",
        f"--vits-model={M}/model.onnx", f"--vits-lexicon={M}/lexicon.txt", f"--vits-tokens={M}/tokens.txt",
        f"--vits-dict-dir={M}/dict", f"--tts-rule-fsts={M}/phone.fst,{M}/date.fst,{M}/number.fst",
        "--num-threads=2", "--sid=1", f"--vits-length-scale={scale}", f"--output-filename={out}", text],
        env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def load(p):
    sr, x = wavfile.read(p); x = x.astype(np.float32) / 32768
    if sr != SR:
        import scipy.signal as ss; x = ss.resample_poly(x, SR, sr)
    return x
def main(src, dst, spec):
    total = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src]))
    voice = np.zeros(int(total * SR)); tmp = tempfile.mkdtemp()
    for i, (t0, dur, text) in enumerate(spec["scenes"]):
        w = os.path.join(tmp, f"{i}.wav"); scale = 0.92
        for _ in range(3):
            say(text, w, scale); x = load(w)
            if len(x) / SR <= dur - 0.35: break
            scale = max(0.6, scale * (len(x) / SR) / (dur - 0.35))
        x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
        s = int((t0 + 0.2) * SR); e = min(len(voice), s + len(x)); voice[s:e] += x[:e - s]
    music = reel_audio.make(total, 11) * 0.45
    # 簡易 ducking：旁白出現時背景降低
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    mix = voice * 1.0 + music * (1 - 0.65 * np.clip(env, 0, 1))
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.9
    wav = os.path.join(tmp, "mix.wav"); wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    subprocess.check_call(["ffmpeg","-v","error","-y","-i",src,"-i",wav,"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-af","loudnorm=I=-16:TP=-1.5","-shortest",dst])
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], json.load(open(sys.argv[3])))
