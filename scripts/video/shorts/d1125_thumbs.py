"""11/25 1면 쇼츠 썸네일 2장: semi25 = 위·아래 반반 대비형 / dell25 = 영수증형"""
import sys
sys.path.insert(0, '/home/claude/pixel_kit')
from d1121_thumbs import F, BLK, BLD, W, H, mascot, ctext
from PIL import Image, ImageDraw

# ---------- 반도체: 위아래 대비 ----------
im = Image.new('RGB', (W, H), (14, 18, 30)); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, H // 2], fill=(240, 200, 40))
ctext(d, 170, '11.25 (수) 간밤 미장', F(BLK, 84), (20, 20, 20))
ctext(d, 330, '월요일', F(BLK, 110), (20, 20, 20))
ctext(d, 480, '+14%', F(BLK, 300), (20, 20, 20))
ctext(d, 1010, '화요일', F(BLK, 110), (255, 255, 255))
ctext(d, 1150, '-7.9%', F(BLK, 300), (120, 200, 255))
ctext(d, 1500, '반도체 지수 하루 만에 되밀림', F(BLK, 76), (255, 255, 255))
m = mascot(280); im.paste(m, (W - m.width - 20, H // 2 - m.height // 2 + 120), m)
im.save('/home/claude/yt3/semi25-thumb.jpg', quality=90)

# ---------- 델: 영수증 ----------
im = Image.new('RGB', (W, H), (40, 44, 52)); d = ImageDraw.Draw(im)
d.rectangle([110, 160, W - 110, 1560], fill=(250, 248, 240))
for x in range(110, W - 110, 40): d.polygon([(x, 1560), (x + 20, 1590), (x + 40, 1560)], fill=(250, 248, 240))
ctext(d, 220, 'DELL · 11.25 (수)', F(BLK, 80), (30, 30, 30))
for y in (340, 900, 1260):
    for x in range(160, W - 160, 30): d.line([(x, y), (x + 15, y)], fill=(150, 150, 150), width=4)
ctext(d, 400, 'AI 수주잔고', F(BLK, 110), (30, 30, 30))
ctext(d, 575, '177조 원', F(BLK, 180), (210, 60, 40))
ctext(d, 790, '1,323억 달러 · 사상 최대', F(BLD, 60), (90, 90, 90))
ctext(d, 960, '매출 +103%', F(BLK, 120), (30, 30, 30))
ctext(d, 1110, '그런데 주가는 -11.8%?', F(BLK, 76), (30, 30, 30))
m = mascot(330); im.paste(m, (W - m.width - 150, 1260), m)
im.save('/home/claude/yt3/dell25-thumb.jpg', quality=90)
print('ok')
