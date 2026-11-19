"""한마디 카드용 인물 실루엣(실존 인물 얼굴이 아닌 역할별 일반형). img/sil/<kind>.png 240x240
  python3 scripts/silhouettes.py"""
from PIL import Image, ImageDraw
import os
INK = (26, 26, 26, 255); BG = (236, 233, 224, 255); W = 240
os.makedirs('img/sil', exist_ok=True)

def base():
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, W - 1, W - 1], fill=BG)
    return im, d

def mask_circle(im):
    m = Image.new('L', (W, W), 0); ImageDraw.Draw(m).ellipse([0, 0, W - 1, W - 1], fill=255)
    out = Image.new('RGBA', (W, W), (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

def body(d, neck=True):
    d.ellipse([28, 150, 212, 330], fill=INK)               # 어깨
    if neck: d.rectangle([100, 128, 140, 165], fill=INK)

def head(d, cx=120, cy=92, r=44):
    d.ellipse([cx - r, cy - r - 4, cx + r, cy + r + 4], fill=INK)

def make(kind):
    im, d = base()
    if kind == 'firm':                                      # 증권사: 기둥 건물
        d.polygon([(48, 92), (120, 48), (192, 92)], fill=INK)
        d.rectangle([52, 96, 188, 106], fill=INK)
        for x in (62, 92, 122, 152):
            d.rectangle([x, 112, x + 18, 172], fill=INK)
        d.rectangle([46, 176, 194, 190], fill=INK)
        return mask_circle(im)
    body(d); head(d)
    if kind in ('suit', 'suit_g'):                          # 정장 + 셔츠 V + 넥타이
        d.polygon([(100, 160), (120, 205), (140, 160)], fill=BG)
        d.polygon([(114, 166), (126, 166), (130, 200), (120, 214), (110, 200)], fill=INK)
    if kind in ('suit_g', 'glasses'):                       # 안경
        for x in (92, 128):
            d.rounded_rectangle([x, 84, x + 26, 102], 6, outline=BG, width=5)
        d.line([118, 92, 128, 92], fill=BG, width=4)
    if kind == 'woman':                                     # 단발 머리
        d.ellipse([66, 40, 174, 150], fill=INK)
        d.rectangle([70, 96, 170, 150], fill=INK)
        d.polygon([(102, 150), (120, 186), (138, 150)], fill=BG)
    if kind == 'mic':                                       # 방송 진행자: 마이크
        d.polygon([(100, 160), (120, 200), (140, 160)], fill=BG)
        d.ellipse([160, 150, 196, 186], fill=INK, outline=BG, width=5)
        d.rectangle([173, 184, 183, 226], fill=INK)
    if kind == 'tee':                                       # 티셔츠 차림 창업자
        d.ellipse([98, 150, 142, 178], fill=BG); d.ellipse([104, 146, 136, 170], fill=INK)
    if kind == 'hood':                                      # 후드 차림 투자자
        d.ellipse([66, 38, 174, 158], outline=INK, width=14)
        d.line([108, 168, 104, 214], fill=BG, width=4); d.line([132, 168, 136, 214], fill=BG, width=4)
    return mask_circle(im)

for k in ('suit', 'suit_g', 'glasses', 'woman', 'mic', 'tee', 'hood', 'firm'):
    make(k).save(f'img/sil/{k}.png', optimize=True)
print('ok')
