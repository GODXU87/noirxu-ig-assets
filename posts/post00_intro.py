"""NOIRXU 品牌介紹輪播 6 張。文字全部取自使用者提供的 ABOUT 內容。用法：python3 -I post00_intro.py OUTDIR"""
import sys
sys.path.insert(0, "/home/claude/noirxu-ig-assets/style")
import noirxu_style as ns
from noirxu_style import *
import feed_lib as fl
OUT = sys.argv[1]; T = 6; SD = "ABOUT　NOIRXU"; LIGHT = "#F2F2F2"

# 1 封面
new_slide(PAPER); frame(1, T, side=SD)
ttext(ML, 250, "INDEPENDENT PERSONAL BRAND", font(SANS_R, 24), GRAY, 8)
fl.fit(ML, 310, "NOIRXU", SERIF_L, 200, INK, 18, 872)
hline(ML, MR, 620, INK, 2)
ttext(ML, 670, "Think Independently.", font(SERIF_M, 60), INK, 4)
ttext(ML, 760, "Create Differently.", font(SERIF_M, 60), INK, 4)
ttext(ML, 900, "由 XU 創立的獨立個人品牌", font(SANS_L, 30), GRAY, 4)
ttext(ML, 1180, "往右翻　→", font(SERIF_M, 30), INK, 6)
save(OUT, "s1.png")

# 2 五個特色
new_slide(PAPER); frame(2, T, side=SD)
ttext(ML, 170, "FIVE PRINCIPLES", font(SANS_R, 24), GRAY, 8)
ttext(ML, 215, "品牌的五個特色", font(SERIF_L, 84), INK, 8)
items = ["獨立思考", "科技與實踐", "金融與投資研究", "創作與生活美學", "極簡而有辨識度的設計"]
y = 420
for k, t in enumerate(items):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y + 36, f"{k+1:02d}", font(SERIF_L, 40), GRAY, 2)
    fl.fit(ML + 110, y + 28, t, SERIF_M, 56, INK, 6, MR - ML - 110)
    y += 150
hline(ML, MR, y, INK, 1.2)
save(OUT, "s2.png")

# 3 理念（黑底）
new_slide(INDIGO, dark=True); frame(3, T, side=SD)
ttext(ML, 420, "不只分享想法，", font(SERIF_L, 84), LIGHT, 8)
ttext(ML, 560, "也把想法做出來。", font(SERIF_L, 84), LIGHT, 8)
hline(ML, MR, 760, INDIGO_H, 1.2)
ttext(ML, 800, "品牌理念", font(SANS_R, 26), INDIGO_L, 8)
ttext(ML, 860, "持續學習、研究、創造與實驗。", font(SANS_L, 32), INDIGO_L, 4)
save(OUT, "s3.png")

# 4 正在做什麼
new_slide(PAPER); frame(4, T, side=SD)
ttext(ML, 170, "WHAT IS NOIRXU DOING", font(SANS_R, 24), GRAY, 8)
ttext(ML, 215, "正在做的事", font(SERIF_L, 84), INK, 8)
rows = [("NOIRXU RADAR", "市場觀察、股票篩選與強弱分析"), ("NOIRXU TERMINAL", "金融市場技術分析工具"), ("NOIRXU PHOTO", "攝影作品與視覺創作"),
        ("NOIRXU FIT", "健身與運動生活"), ("YORU LAB", "投資研究、觀點與深度內容"), ("AI GAME LAB", "互動遊戲與創意實驗")]
y = 400
for k, (n, dsc) in enumerate(rows):
    hline(ML, MR, y, INK if k == 0 else HAIR, 1.2)
    ttext(ML, y + 20, n, font(SANS_R, 24), GRAY, 5)
    fl.fit(ML, y + 56, dsc, SERIF_M, 40, INK, 4, MR - ML)
    y += 140
hline(ML, MR, y, INK, 1.2)
save(OUT, "s4.png")

# 5 共同方向
new_slide(PAPER2); frame(5, T, side=SD)
ttext(ML, 170, "THE COMMON DIRECTION", font(SANS_R, 24), GRAY, 8)
ttext(ML, 215, "共同的方向", font(SERIF_L, 84), INK, 8)
hline(ML, MR, 400, INK, 1.2)
for k, t in enumerate(["運用科技提升效率，", "透過研究建立判斷，", "再把個人的想法", "轉化為實際成果。"]):
    ttext(ML, 450 + k * 120, t, font(SERIF_M, 62), INK, 6)
save(OUT, "s5.png")

# 6 收尾
new_slide(PAPER); frame(6, T, side=SD)
ttext(ML, 300, "Think Independently.", font(SERIF_L, 72), INK, 4)
ttext(ML, 400, "Create Differently.", font(SERIF_L, 72), INK, 4)
hline(ML, MR, 600, INK, 2)
ttext(ML, 650, "noirxu.com", font(SANS_R, 40), INK, 6)
ttext(ML, 740, "追蹤，看接下來做出什麼。", font(SERIF_M, 46), INK, 5)
seal(MR - 70, 1000, 112)
save(OUT, "s6.png")
print("intro ok")
