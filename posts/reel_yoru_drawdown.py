"""Reel：虧損與回本不對稱（YORU LAB 風格：交易紀律）。用法：python3 -I reel_yoru_drawdown.py OUTDIR"""
import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
from reel_lib import *
OUT = sys.argv[1]
need = lambda dd: (1 / (1 - dd) - 1) * 100
items = [(f"跌 {int(d*100)}%", "需要上漲", need(d)) for d in (0.10, 0.20, 0.30, 0.50)]
print([round(v, 1) for _, _, v in items])
S = "YORU LAB　失效點"
build([
    (text_scene(S, [("跌 50%，", SERIF_M, 64, INK, 6, 0), ("要漲多少", SERIF_L, 110, INK, 6, 110),
                    ([("才回本", INK), ("？", VERM)], SERIF_M, 70, INK, 6, 180)], seal=True), 2.8),
    (anim(lambda k: bars_scene(S, ["跌得越深，", "回本越難。"], items, "%", k, "{:.1f}", "回本所需漲幅 ＝ 1 ÷ (1 − 跌幅) − 1", hi=3), 54), 5.4),
    (bignum_scene(S, "跌 50%，要漲", f"{need(0.5):.0f}", "%", "才能回到原點。", "跌的和漲的，不是對稱的。"), 3.6),
    (text_scene(S, [("交易不是預測，", SERIF_M, 64, INK, 6, 0), ("是紀律。", SERIF_M, 64, INK, 6, 100),
                    ("先定失效點，", SERIF_L, 84, VERM, 6, 160), ("再談進場。", SERIF_L, 84, VERM, 6, 110)], rule=1130), 3.8),
    (text_scene(S, [("傳給正在盯盤", SERIF_M, 72, INK, 8, 0), ("的人。", SERIF_M, 72, INK, 8, 120)], seal=True,
                foot="數學計算，不涉及個股或買賣點，非投資建議。"), 2.8),
], OUT, "r0_drawdown")
