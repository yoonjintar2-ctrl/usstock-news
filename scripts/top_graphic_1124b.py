"""2026-11-24 1면 두 번째 그림: 크라우드스트라이크의 지스케일러 주식 교환 인수 — '계산서' 구성(교환비율·발표 가치 vs 11/23 종가로 다시 계산한 가치 막대 + CRWD 이틀 종가).
NVDA 사다리 그림·11/21 그림(꺾은선·캔들)과 겹치지 않게 비교 막대+계산식 구성."""
from PIL import Image, ImageDraw, ImageFont
import json
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
mv={l.split(',')[0]:l.split(',') for l in open('data/movers_raw.txt').read().split('\n') if l}
c=float(mv['CRWD'][2]); ch=float(mv['CRWD'][3]); prev=round(c/(1+ch/100),2)
R=1.135; HEAD=260.41; now=round(R*c,2)
W,H=1200,750; P=236; INK=18
im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.text((40,26),'CRWD',font=F(B,104),fill=INK)
d.text((372,52),'→',font=F(B,80),fill=INK)
d.text((470,26),'ZS',font=F(B,104),fill=INK)
d.text((44,154),'크라우드스트라이크, 지스케일러를 전액 주식으로 인수',font=F(BD,28),fill=50)
# 계산식 줄
d.rectangle((40,208,700,286),outline=INK,width=3)
d.text((60,247),f'ZS 1주 = CRWD {R}주',font=F(B,42),fill=INK,anchor='lm')
# 가치 비교 막대 (ZS 1주당)
d.text((40,318),'ZS 1주가 받는 몫 (달러)',font=F(B,30),fill=INK)
x0=60; sc=600/280
for i,(lab,v,col) in enumerate([('발표 기준 (11/20 CRWD 종가)',HEAD,INK),('11/23 CRWD 종가로 다시 계산',now,120)]):
    y=372+i*120
    d.rectangle((x0,y,x0+v*sc,y+62),fill=col)
    d.text((x0+v*sc-14,y+31),f'{v:.2f}',font=F(B,38),fill=P,anchor='rm')
    d.text((x0,y+70),lab,font=F(BD,22),fill=60)
d.text((60,628),f'하루 새 약 {HEAD-now:.0f}달러 줄어든 셈 (교환 비율 고정)',font=F(BD,24),fill=INK)
# 오른쪽 숫자 칸
d.line((744,40,744,H-60),fill=INK,width=2)
def box(y,big,small,inv=False):
    d.rectangle((770,y,1172,y+112),outline=INK,width=3,fill=INK if inv else P)
    d.text((790,y+4),big,font=F(B,54),fill=P if inv else INK)
    d.text((792,y+76),small,font=F(BD,21),fill=P if inv else 60)
box(40,'439억 달러','인수 규모 · 약 59조 원',True)
box(168,'약 34%','11/20 종가 대비 웃돈(발표 기준)')
box(296,f'{ch:+.2f}%',f'CRWD 11/23 · {prev}→{c}달러')
box(424,'84.1%','합친 회사에서 CRWD 주주 몫')
d.text((772,560),'마무리: CRWD 2028 회계연도 하반기',font=F(BD,22),fill=60)
d.text((772,592),'지분 약 34% 창업자 측 찬성 약정',font=F(BD,22),fill=60)
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.24 · 조건: 회사 발표(야후 파이낸스) · 시세: CNBC 일봉 · 재계산 값은 1.135×종가',font=F(BD,15),fill=90,anchor='rm')
im.convert('RGB').save('img/2026-11-24-top2.jpg',quality=88); print('ok',prev,c,now)
