"""11/21 1면 쇼츠 썸네일 2장 (1080x1920)
nvda: 신문 1면 호외 스타일 / avgo: 경고 테이프 스타일 — 날짜 크게, 핵심 글자는 가운데 영역"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W, H = 1080, 1920
BLK = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
BLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def F(p, s): return ImageFont.truetype(p, s, index=1)   # KR
def mascot(h):
    m = Image.open('/home/claude/mascot3d/ev/host_A.png').convert('RGBA')
    a = np.asarray(m).copy()
    if a[..., 3].min() == 255:                       # 흰 배경 → 투명
        wh = (a[..., :3].min(axis=2) > 245); a[wh, 3] = 0
    m = Image.fromarray(a); bb = m.getbbox(); m = m.crop(bb)
    return m.resize((int(m.width * h / m.height), h), Image.LANCZOS)
def ctext(d, y, s, f, fill, stroke=0, sf=None):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sf)

# ---------- 1) 엔비디아: 신문 호외 ----------
im = Image.new('RGB', (W, H), (238, 233, 220)); d = ImageDraw.Draw(im)
rng = np.random.default_rng(3)
n = (rng.random((H, W)) * 14).astype(np.uint8)
im = Image.fromarray(np.clip(np.asarray(im).astype(int) - n[..., None], 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
d.rectangle([60, 250, W - 60, 262], fill=(20, 20, 20))
ctext(d, 272, '미국주식 늬우스  ·  호외', F(BLK, 64), (20, 20, 20))
d.rectangle([60, 358, W - 60, 364], fill=(20, 20, 20))
d.rectangle([90, 400, 520, 640], fill=(20, 20, 20))
d.text((118, 408), '11.21', font=F(BLK, 150), fill=(238, 233, 220))
d.text((120, 590), '토요일 · 간밤 미장', font=F(BLD, 36), fill=(238, 233, 220))
d.text((560, 420), 'SEC', font=F(BLK, 120), fill=(180, 30, 30))
d.text((560, 560), '회계 조사 보도', font=F(BLK, 58), fill=(20, 20, 20))
ctext(d, 680, '엔비디아', F(BLK, 230), (20, 20, 20))
ctext(d, 900, '-14%', F(BLK, 290), (180, 30, 30))
d.rectangle([60, 1300, W - 60, 1306], fill=(20, 20, 20))
ctext(d, 1325, '하루 만에 약 661조 원 증발', F(BLK, 72), (20, 20, 20))
ctext(d, 1425, '기회일까, 함정일까?', F(BLD, 60), (90, 90, 90))
m = mascot(430); im.paste(m, (W - m.width - 40, H - m.height - 40), m)
for k in range(5): d.rectangle([90, 1560 + k * 34, 560, 1572 + k * 34], fill=(150, 145, 135))
im.save('/home/claude/yt2/nvda-thumb.jpg', quality=90)

# ---------- 2) 브로드컴: 경고 테이프 ----------
im = Image.new('RGB', (W, H), (24, 26, 34)); d = ImageDraw.Draw(im)
def tape(y, ang, text):
    t = Image.new('RGBA', (W + 400, 120), (0, 0, 0, 0)); td = ImageDraw.Draw(t)
    td.rectangle([0, 0, W + 400, 120], fill=(250, 205, 40))
    for x in range(-120, W + 400, 120): td.polygon([(x, 0), (x + 60, 0), (x + 120, 120), (x + 60, 120)], fill=(20, 20, 20))
    td.rectangle([0, 30, W + 400, 90], fill=(250, 205, 40))
    f = F(BLK, 50); s = (text + '   ') * 6; td.text((20, 30), s, font=f, fill=(20, 20, 20))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.paste(t, (-200, y - t.height // 2), t)
tape(330, 4, '주의 · 설문 한 장')
d = ImageDraw.Draw(im)
ctext(d, 450, '11.21 (토)', F(BLK, 120), (250, 205, 40))
ctext(d, 610, '브로드컴', F(BLK, 220), (255, 255, 255))
ctext(d, 850, '-12%', F(BLK, 300), (250, 205, 40))
ctext(d, 1200, '구글 AI칩 20% 줄였다?', F(BLK, 76), (255, 255, 255))
ctext(d, 1300, '회사 확인 없는 설문 한 장', F(BLD, 56), (180, 185, 200))
tape(1460, -5, '12월 9일 실적이 답')
m = mascot(380); im.paste(m, (60, H - m.height - 30), m)
im.save('/home/claude/yt2/avgo-thumb.jpg', quality=90)
print('ok')
