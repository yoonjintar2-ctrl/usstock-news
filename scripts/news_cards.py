"""흑백 신문풍 뉴스 이미지: 큰 티커/회사명 타이포 + 하프톤 처리한 3D 소품 그림.
실존 인물 사진·회사 로고는 쓰지 않는다(이름은 일반 글꼴 텍스트로만)."""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

R = '/home/claude/renders'
OUT = sys.argv[1]
BLACK = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
W, H = 640, 400
PAPER = 236

CARDS = {  # name: (render, ticker, company, 키워드, 등락)
    'ipo':      ('ipo', 'ANT', 'ANTHROPIC · NASDAQ IPO', '역대 최대 공모', '공모가 약 11만 원'),
    'nvda':     ('nvda', 'NVDA', 'NVIDIA CORP.', '실적 vs 주가', '▼ 2.89%'),
    'fed':      ('fed', 'FOMC', 'FEDERAL RESERVE', '12월 인상?', '확률 95.7%'),
    'cyber':    ('cyber', 'PANW', 'PALO ALTO · CROWDSTRIKE', '보안주 급등', '▲ 9.90%'),
    'health':   ('health', 'UNH', 'UNITEDHEALTH GROUP', '건강보험 급락', '▼ 10.21%'),
    'memory':   ('memory', 'SNDK', 'SANDISK · MICRON', '낸드 과잉 우려', '▼ 2.64%'),
    'gold_oil': ('gold_oil', 'GOLD', 'GOLD · WTI CRUDE', '14개월 최저', '온스 약 499만 원 ↓'),
}


def halftone(img, cell=6):
    g = ImageOps.autocontrast(img.convert('L'), cutoff=2)
    w, h = g.size
    out = Image.new('L', (w, h), PAPER)
    d = ImageDraw.Draw(out)
    small = g.resize((w // cell, h // cell), Image.LANCZOS)
    for y in range(small.size[1]):
        for x in range(small.size[0]):
            v = small.getpixel((x, y))
            r = (1 - v / 255) * cell * 0.72
            if r > 0.4:
                cx, cy = x * cell + cell / 2, y * cell + cell / 2
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=20)
    return out


def fit(font_path, text, max_w, start, idx=0):
    s = start
    while s > 10:
        f = ImageFont.truetype(font_path, s, index=idx)
        if f.getbbox(text)[2] <= max_w: return f
        s -= 2
    return ImageFont.truetype(font_path, 10, index=idx)


def card(name, src, tick, comp, kw, chg):
    im = Image.open(os.path.join(R, src + '.png')).convert('RGB')
    # 소품 부분만 크게 잘라 오른쪽에
    w, h = im.size
    crop = im.crop((int(w * .12), int(h * .08), int(w * .92), int(h * .92)))
    ht = halftone(crop.resize((380, int(380 * crop.size[1] / crop.size[0]))))
    canvas = Image.new('L', (W, H), PAPER)
    canvas.paste(ht, (W - ht.size[0] + 30, (H - ht.size[1]) // 2 + 6))
    # 왼쪽 글자 영역은 비우고 경계는 그라데이션으로
    mask = Image.new('L', (W, H), 0); md = ImageDraw.Draw(mask)
    for i in range(W):
        md.line([(i, 0), (i, H)], fill=255 if i < 300 else max(0, int(255 * (1 - (i - 300) / 50))))
    canvas = Image.composite(Image.new('L', (W, H), PAPER), canvas, mask)
    d = ImageDraw.Draw(canvas)
    # 티커
    ft = fit(BLACK, tick, 270, 140, 1)
    d.text((26, 34), tick, font=ft, fill=10)
    tb = d.textbbox((26, 34), tick, font=ft)
    y = tb[3] + 10
    fc = fit(BOLD, comp, 270, 22, 1)
    d.text((28, y), comp, font=fc, fill=40)
    y = d.textbbox((28, y), comp, font=fc)[3] + 18
    fk = ImageFont.truetype(BLACK, 30, index=1)
    kb = d.textbbox((0, 0), kw, font=fk)
    d.rectangle((26, y, 26 + kb[2] + 20, y + kb[3] + 16), fill=10)
    d.text((36, y + 4), kw, font=fk, fill=PAPER)
    y += kb[3] + 30
    fch = ImageFont.truetype(BLACK, 28, index=1)
    d.text((28, y), chg, font=fch, fill=10)
    # 신문 테두리
    d.rectangle((6, 6, W - 7, H - 7), outline=10, width=3)
    d.line((14, H - 34, W - 14, H - 34), fill=10, width=1)
    fs = ImageFont.truetype(BOLD, 14, index=1)
    d.text((18, H - 30), '미국주식 늬우스 · 2026.11.19', font=fs, fill=60)
    canvas.save(os.path.join(OUT, f'2026-11-19-{name}.jpg'), quality=86)


for k, v in CARDS.items():
    card(k, *v)
print('ok')
