"""2026-11-24 간밤 뉴스 카드 중 3D 소품이 없는 3장: 그날 실제 숫자로 그린 작은 흑백 막대 그래픽(640x400).
news_cards.py 와 같은 틀(왼쪽 큰 티커·회사·키워드·등락, 오른쪽 그림, 아래 줄)."""
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
W,H=640,400; P=236; INK=10
mv={l.split(',')[0]:float(l.split(',')[3]) for l in open('data/movers_raw.txt') if l.strip()}
S={l.split('|')[0]:l.split('|')[1].split(',') for l in open('data/summary.txt').read().split('\n')[1:] if '|' in l}
def fit(t,mw,s,p=B):
    while s>12 and F(p,s).getbbox(t)[2]>mw: s-=2
    return F(p,s)
def card(name,tick,comp,kw,chg,bars,unit='%'):
    im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
    ft=fit(tick,270,120); d.text((26,34),tick,font=ft,fill=INK); y=d.textbbox((26,34),tick,font=ft)[3]+10
    fc=fit(comp,270,22,BD); d.text((28,y),comp,font=fc,fill=40); y=d.textbbox((28,y),comp,font=fc)[3]+18
    fk=F(B,30); kb=d.textbbox((0,0),kw,font=fk); d.rectangle((26,y,26+kb[2]+20,y+kb[3]+16),fill=INK); d.text((36,y+4),kw,font=fk,fill=P); y+=kb[3]+30
    d.text((28,y),chg,font=F(B,28),fill=INK)
    # 오른쪽 가로 막대
    x0,x1=330,610; mx=max(abs(v) for _,v in bars); n=len(bars); top=40; bh=min(54,(300)/n-12)
    for i,(lab,v) in enumerate(bars):
        yy=top+i*(bh+12)+18
        d.text((x0,yy-2),lab,font=F(BD,17),fill=50,anchor='ls')
        w=abs(v)/mx*(x1-x0-90)
        d.rectangle((x0,yy+4,x0+w,yy+4+bh-18),fill=INK if v>0 else 130)
        d.text((x0+w+8,yy+4+(bh-18)/2),f'{v:+.2f}{unit}',font=F(B,20),fill=INK,anchor='lm')
    d.rectangle((6,6,W-7,H-7),outline=INK,width=3); d.line((14,H-34,W-14,H-34),fill=INK,width=1)
    d.text((18,H-30),'미국주식 늬우스 · 2026.11.24 · 시세: CNBC 일봉(11/23 종가)',font=F(BD,14),fill=60)
    im.convert('RGB').save(f'img/2026-11-24-{name}.jpg',quality=86)
x=lambda k:float(S[k][3])
card('spx','SPX','S&P 500 · 7일 연속 하락 끝','최고의 하루',f"▲ {x('^GSPC'):.2f}%",[('반도체 지수',x('^SOX')),('나스닥',x('^IXIC')),('S&P 500',x('^GSPC')),('러셀 2000',x('^RUT')),('다우',x('^DJI')),('VIX',x('^VIX'))])
card('earn','ZM','ZOOM · HEWLETT PACKARD ENT.','첫 배당 0.25달러','장 후 실적 · 시간외 약세',[('줌 매출 증가율',4.9),('기업 고객 매출',8.6),('온라인 매출',-0.6)])
card('soft','ORCL','ORACLE · TESLA · PALANTIR','AI 빚 걱정 완화',f"▲ {mv['ORCL']:.2f}%",[('오라클',mv['ORCL']),('테슬라',mv['TSLA']),('팔란티어',mv['PLTR']),('메타',mv['META']),('알파벳 A',mv['GOOGL'])])
print('ok')
