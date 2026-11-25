"""2026-11-26 간밤 뉴스 카드 중 3D 소품이 없는 3장: 그날 실제 숫자로 그린 작은 흑백 막대 그래픽(640x400).
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
def card(name,tick,comp,kw,chg,bars,unit='%',fmt='{:+.2f}',FOOT='미국주식 늬우스 · 2026.11.26 · 시세: CNBC 일봉(11/25 종가)'):
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
        d.text((x0+w+8,yy+4+(bh-18)/2),fmt.format(v)+unit,font=F(B,20),fill=INK,anchor='lm')
    d.rectangle((6,6,W-7,H-7),outline=INK,width=3); d.line((14,H-34,W-14,H-34),fill=INK,width=1)
    d.text((18,H-30),FOOT,font=F(BD,14),fill=60)
    im.convert('RGB').save(f'img/2026-11-26-{name}.jpg',quality=86)
x=lambda k:float(S[k][3])
TD=__import__('json').load(open('data/tm_daily.json'))
card('earn','HPQ','HP · DEERE · DELL · NUTANIX','실적 뒤 엇갈림','▲ 11.4%',[('HP',11.4),('디어',TD['DE'][5]),('델',TD['DELL'][5]),('뉴타닉스(장 후반)',-17.6)],FOOT='미국주식 늬우스 · 2026.11.26 · HP Kiplinger·뉴타닉스 Parameter 보도 · 디어·델 CNBC 일봉')
card('orcl','ORCL','ORACLE · 5년 CDS','신용 위험 최고',f"▼ {abs(TD['ORCL'][5]):.2f}%",[('2025년 중반',35),('2025년 말',154),('11/24',360)],unit='bp',fmt='{:,.0f}',FOOT='미국주식 늬우스 · 2026.11.26 · CDS: S&P Global(Motley Fool 보도) · 주가 CNBC 일봉')
card('bigtech','META','META · AMAZON · ALPHABET','빅테크 엇갈림',f"▲ {TD['META'][5]:.2f}%",[('메타',TD['META'][5]),('애플',TD['AAPL'][5]),('마이크로소프트',TD['MSFT'][5]),('알파벳',TD['GOOGL'][5]),('아마존',TD['AMZN'][5])])
card('rebound','ADI','ANALOG DEVICES · AST SPACEMOBILE','급락 뒤 반등',f"▲ {TD['ADI'][5]:.2f}%",[('ADI 11/24',-17.37),('ADI 11/25',TD['ADI'][5]),('AST 스페이스모바일',mv['ASTS']),('아이온큐',mv['IONQ'])])
print('ok')
