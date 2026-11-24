"""2026-11-25 1면 그림: 반도체 '이틀 나비 막대' — 같은 종목의 11/23(월) 등락(왼쪽)과 11/24(화) 등락(오른쪽)을 가운데 축 양쪽으로.
11/24(가격 사다리)·11/24b(계산식·가치 막대)·11/21(꺾은선)·11/21b(캔들)와 겹치지 않는 구성. 숫자는 data/tm_daily.json·summary.txt(CNBC 일봉)와 archive/2026-11-24.json 트리맵."""
import json
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
S={l.split('|')[0]:l.split('|')[1].split(',') for l in open('data/summary.txt').read().split('\n')[1:] if '|' in l}
TD=json.load(open('data/tm_daily.json'))
A=json.load(open('archive/2026-11-24.json')); MON={i['t']:i['ch'] for i in A['treemap']['items']}
MON['^SOX']=float(S['^SOX'][3]) if False else 14.03  # 11/23 필라델피아 반도체(archive market 행)
rows=[('필라델피아 반도체','^SOX',MON['^SOX'],float(S['^SOX'][3])),
      ('엔비디아 NVDA','NVDA',MON['NVDA'],TD['NVDA'][5]),('마이크론 MU','MU',MON['MU'],TD['MU'][5]),
      ('텍사스인스트루먼트 TXN','TXN',MON['TXN'],TD['TXN'][5]),
      ('아날로그디바이스 ADI','ADI',MON['ADI'],TD['ADI'][5]),('인텔 INTC','INTC',MON['INTC'],TD['INTC'][5])]
W,H=1200,750; P=236; INK=18
im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.text((40,18),'SOX',font=F(B,120),fill=INK)
d.text((300,40),'반도체, 하루 만에 되밀림',font=F(B,46),fill=INK)
d.text((302,104),'하루 등락률 · 왼쪽 11/23(월) · 오른쪽 11/24(화)',font=F(BD,24),fill=70)
# 나비 막대
cx=400; sc=9.0; y=196; bh=40
d.text((cx-14,172),'◀ 11/23 월',font=F(BD,20),fill=90,anchor='rs'); d.text((cx+14,172),'11/24 화 ▶',font=F(BD,20),fill=INK,anchor='ls')
for lab,t,m,tu in rows:
    d.text((cx+10,y+2),lab,font=F(BD,20),fill=60,anchor='ls') if False else d.text((40,y),lab,font=F(BD,21),fill=INK,anchor='lt'); y+=28
    # 월요일(오른쪽 반대편: 왼쪽으로 뻗음, 회색)
    d.rectangle((cx-m*sc,y,cx,y+bh),fill=150)
    d.text((cx-m*sc-8,y+bh/2),f'+{m:.1f}%',font=F(BD,22),fill=70,anchor='rm')
    # 화요일(오른쪽으로, 길이=하락폭, 검정)
    w=abs(tu)*sc
    d.rectangle((cx,y,cx+w,y+bh),fill=INK)
    d.text((cx+w+8,y+bh/2),f'{tu:+.2f}%',font=F(B,26),fill=INK,anchor='lm')
    y+=bh+10
d.line((cx,188,cx,y),fill=INK,width=3)
# 오른쪽 숫자 칸
d.line((790,40,790,H-60),fill=INK,width=2)
def box(y,big,small,inv=False):
    d.rectangle((812,y,1172,y+112),outline=INK,width=3,fill=INK if inv else P)
    d.text((830,y+4),big,font=F(B,52),fill=P if inv else INK)
    d.text((832,y+76),small,font=F(BD,20),fill=P if inv else 60)
nv=TD['NVDA']
box(40,f"{float(S['^SOX'][1]):,.0f}",f"반도체 지수 11/24 종가 · {float(S['^SOX'][3]):+.2f}%",True)
box(168,f"{nv[4]:.2f}달러",f"엔비디아 종가 · 전날 {float(S['NVDA'][2]):.2f}달러")
box(296,f"{TD['ADI'][5]:+.1f}%",'ADI · 실적 뒤 1분기 전망에 실망')
box(424,f"{float(S['^DJI'][3]):+.2f}%",f"다우 {float(S['^DJI'][1]):,.0f} · 돈은 헬스케어로")
d.text((814,562),'나스닥 −1.48% · S&P 500 −0.50%',font=F(BD,22),fill=60)
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.25 · 시세: CNBC 일봉(11/23·11/24 종가) · 막대 길이 = 하루 등락률',font=F(BD,15),fill=90,anchor='rm')
im.convert('RGB').save('img/2026-11-25-top.jpg',quality=88); print('ok')
