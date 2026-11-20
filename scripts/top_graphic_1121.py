"""2026-11-21 1면 그림: 엔비디아 22거래일 종가 흐름(꺾은선·면) + 핵심 숫자 박스 + 지수 하루 등락 가로 막대.
11/20 그림(왼쪽 점 4개 꺾은선 · 오른쪽 세로 막대 7개)과 구성이 겹치지 않게 했다.
종가 모양은 data/tickers_mini.json(야후 일봉 22개, 0~255 압축)을 풀어 그리고, 글자로 적는 숫자는 확인값만 쓴다."""
import json, base64
from PIL import Image, ImageDraw, ImageFont
B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F = lambda p, s: ImageFont.truetype(p, s, index=1)
W, H = 1200, 750; PAPER = 236; INK = 18
im = Image.new('L', (W, H), PAPER); d = ImageDraw.Draw(im)
d.rectangle((8, 8, W - 9, H - 9), outline=INK, width=3)
d.line((744, 40, 744, H - 60), fill=INK, width=2)

# ── 왼쪽: NVDA 최근 22거래일 종가 ──
m = json.load(open('data/tickers_mini.json', encoding='utf-8'))['NVDA']
raw = base64.b64decode(m[2]); mn, mx = m[0], m[1]
cl = [mn + raw[i * 4 + 3] / 255 * (mx - mn) for i in range(len(raw) // 4)]
cl[-1] = 125.53; cl[-2] = 145.98  # 마지막 두 날은 확인된 종가로
d.text((40, 24), 'NVDA', font=F(B, 132), fill=INK)
d.text((46, 182), '엔비디아 · 최근 22거래일 종가 (10/22~11/20)', font=F(BD, 26), fill=60)
x0, x1, y0, y1 = 60, 700, 600, 270; lo, hi = 115, 225
P = [(x0 + i * (x1 - x0) / (len(cl) - 1), y0 - (v - lo) / (hi - lo) * (y0 - y1)) for i, v in enumerate(cl)]
d.polygon(P + [(x1, y0), (x0, y0)], fill=200)
for yv in (125, 150, 175, 200):
    yy = y0 - (yv - lo) / (hi - lo) * (y0 - y1)
    d.line((x0, yy, x1, yy), fill=170, width=1)
    d.text((x0 - 6, yy), f'{yv}', font=F(BD, 18), fill=100, anchor='rm')
d.line(P, fill=INK, width=6, joint='curve')
d.line((x0, y0, x1, y0), fill=INK, width=2)
for x, y in (P[-2], P[-1]):
    d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=INK)
fn = F(B, 26)
for txt, xy in (('11/19 145.98달러', (P[-2][0] - 14, P[-2][1] - 30)), ('11/20 125.53달러', (P[-1][0] - 22, P[-1][1] + 24))):
    bb = d.textbbox(xy, txt, font=fn, anchor='rm'); d.rectangle((bb[0] - 6, bb[1] - 4, bb[2] + 6, bb[3] + 4), fill=PAPER)
    d.text(xy, txt, font=fn, fill=INK, anchor='rm')
d.text((x0, y0 + 14), '10/22', font=F(BD, 20), fill=60)
d.text((x1, y0 + 14), '11/20', font=F(BD, 20), fill=60, anchor='ra')
d.rectangle((40, 664, 560, 716), fill=INK)
d.text((56, 668), '하루 -14.01% · SEC 회계 조사 보도', font=F(B, 30), fill=PAPER)

# ── 오른쪽: 숫자 박스 + 지수 하루 등락 ──
def box(y, big, small):
    d.rectangle((772, y, 1172, y + 112), outline=INK, width=3)
    d.text((792, y + 6), big, font=F(B, 58), fill=INK)
    d.text((794, y + 78), small, font=F(BD, 22), fill=60)
box(40, '-47.5%', '10/6 최고 종가 239.24달러 대비')
box(168, '-11.9%', 'S&P 500 고점 대비 · 조정 진입')
d.text((772, 300), '11/20 하루 등락', font=F(B, 30), fill=INK)
rows = [('반도체', -10.73), ('나스닥', -5.28), ('S&P 500', -3.70), ('다우', -1.93)]
zx, maxw = 1172, 165
for i, (nm, v) in enumerate(rows):
    y = 352 + i * 74
    w = abs(v) / 11 * maxw
    d.rectangle((zx - w, y, zx, y + 46), fill=INK if i == 0 else 110)
    d.text((772, y + 23), nm, font=F(BD, 26), fill=INK, anchor='lm')
    d.text((995, y + 23), f'{v:.2f}%', font=F(B, 26), fill=INK, anchor='rm')
d.text((W - 24, H - 22), '미국주식 늬우스 · 2026.11.21 · 시세: 야후 파이낸스·CNBC 일봉 · 최고 종가: Motley Fool', font=F(BD, 16), fill=90, anchor='rm')
im.convert('RGB').save('img/2026-11-21-top.jpg', quality=88)
print('ok')
