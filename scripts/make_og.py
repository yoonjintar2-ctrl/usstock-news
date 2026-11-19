"""공유 썸네일(og:image) 1200x630 — 그날 1면 제목·지수·1면 그림으로 매일 다르게.
  python3 scripts/make_og.py drafts/2026-11-19.json   → og/2026-11-19.png
흑백 신문 톤. 폰트: Noto CJK(서버) — 맥이면 FONT_DIR 환경변수로 지정."""
import json, os, sys, datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps

FD = os.environ.get('FONT_DIR', '/usr/share/fonts/opentype/noto')
SERIF = os.path.join(FD, 'NotoSerifCJK-Black.ttc')
SANS = os.path.join(FD, 'NotoSansCJK-Bold.ttc')
SANS_B = os.path.join(FD, 'NotoSansCJK-Black.ttc')
KR = 1  # ttc 안의 한국어 글꼴 번호
W, H = 1200, 630
PAPER, INK, MUTED = (246, 243, 234), (20, 20, 20), (110, 106, 98)
WD = '월화수목금토일'


def F(path, size): return ImageFont.truetype(path, size, index=KR)


def wrap(d, text, font, max_w, max_lines):
    """한글은 글자 단위로 줄바꿈(어절 우선)."""
    lines, cur = [], ''
    for word in text.split(' '):
        t = (cur + ' ' + word).strip()
        if d.textlength(t, font=font) <= max_w: cur = t; continue
        if cur: lines.append(cur); cur = ''
        for ch in word:  # 어절 하나가 너무 길면 글자 단위
            if d.textlength(cur + ch, font=font) <= max_w: cur += ch
            else: lines.append(cur); cur = ch
    if cur: lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]; lines[-1] = lines[-1].rstrip()[:-1] + '…'
    return lines


def make(draft, out_dir='og'):
    D = json.load(open(draft, encoding='utf-8'))
    date = datetime.date.fromisoformat(D['date'])
    top = D.get('top') or {}
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    # 제호
    d.text((48, 30), '미국주식 늬우스', font=F(SERIF, 54), fill=INK)
    meta = f"{date.year}년 {date.month}월 {date.day}일 ({WD[date.weekday()]}) · 제{D.get('no', '')}호"
    fm = F(SANS, 24); d.text((W - 48 - d.textlength(meta, font=fm), 52), meta, font=fm, fill=MUTED)
    d.rectangle((48, 112, W - 48, 116), fill=INK); d.rectangle((48, 121, W - 48, 122), fill=INK)
    # 오른쪽: 1면 그림
    img_path = top.get('img')
    x_text_max = W - 48
    if img_path and os.path.exists(img_path):
        pic = Image.open(img_path).convert('L')
        pic = ImageOps.contain(pic, (430, 300))
        px, py = W - 48 - pic.size[0], 150
        im.paste(Image.merge('RGB', (pic, pic, pic)), (px, py))
        d.rectangle((px - 2, py - 2, px + pic.size[0] + 1, py + pic.size[1] + 1), outline=INK, width=3)
        x_text_max = px - 32
    # 키커 + 제목
    kicker = top.get('kicker', '오늘의 1면')
    fk = F(SANS_B, 24); kw = d.textlength(kicker, font=fk)
    d.rectangle((48, 150, 48 + kw + 24, 190), outline=INK, width=3)
    d.text((60, 153), kicker, font=fk, fill=INK)
    title = top.get('title') or D.get('lead', '')
    for size in (62, 56, 50, 46):
        ft = F(SERIF, size); lines = wrap(d, title, ft, x_text_max - 48, 3)
        if len(lines) <= 3 and size * 1.25 * len(lines) <= 260: break
    y = 210
    for ln in lines:
        d.text((48, y), ln, font=ft, fill=INK); y += int(size * 1.25)
    # 아래: 지수 띠
    rows = ((D.get('market') or {}).get('rows') or [])[:4]
    d.rectangle((48, 488, W - 48, 490), fill=INK)
    if rows:
        cw = (W - 96) / len(rows); fn, fv = F(SANS, 22), F(SANS_B, 28)
        for i, r in enumerate(rows):
            x = 48 + i * cw + (0 if i == 0 else 18)
            if i: d.line((48 + i * cw, 500, 48 + i * cw, 570), fill=(200, 196, 186), width=2)
            c = r['close']['v']; ch = r['chg_pct']['v']
            d.text((x, 500), r['name'], font=fn, fill=MUTED)
            d.text((x, 530), f"{c:,.2f}", font=fv, fill=INK)
            arrow = '▲' if ch > 0 else '▼' if ch < 0 else '–'
            s = f"{arrow} {abs(ch):.2f}%"; fs = F(SANS_B, 22)
            d.text((x + d.textlength(f'{c:,.2f}', font=fv) + 12, 536), s, font=fs, fill=INK)
    d.rectangle((48, 582, W - 48, 583), fill=INK)
    fs = F(SANS, 20)
    d.text((48, 592), 'stocknews.jintar.co.kr', font=fs, fill=MUTED)
    pub = f"발행인 {D.get('publisher', '샌디스크 올인')} · 간밤 뉴욕장과 오늘 밤 일정을 한 장에"
    d.text((W - 48 - d.textlength(pub, font=fs), 592), pub, font=fs, fill=MUTED)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{D['date']}.png")
    im.save(out, optimize=True)
    return out


if __name__ == '__main__':
    print(make(sys.argv[1]))
