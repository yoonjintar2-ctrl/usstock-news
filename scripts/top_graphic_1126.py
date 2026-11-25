"""2026-11-26 1면 그림: '장중 저점 → 종가' 덤벨 — 종목마다 전날 종가(0%)를 세로 기준선으로, 장중 저점(속 빈 원)과 종가(검은 원)를 잇는다.
11/25(나비 막대)·11/25b(세로 막대+캔들)와 겹치지 않는 구성. 숫자는 data/tm_daily.json·summary.txt(CNBC 일봉 11/25)."""
import json
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
S={l.split('|')[0]:l.split('|')[1].split(',') for l in open('data/summary.txt').read().split('\n')[1:] if '|' in l}
TD=json.load(open('data/tm_daily.json'))
def s_row(k):  # close, prev, low
    v=S[k]; return float(v[1]),float(v[2]),float(v[6])
def t_row(k):
    r=TD[k]; c=r[4]; prev=c/(1+r[5]/100); return c,prev,r[3]
rows=[('나스닥 종합','^IXIC',s_row('^IXIC')),('필라델피아 반도체','^SOX',s_row('^SOX')),
      ('엔비디아 NVDA','NVDA',t_row('NVDA')),('AMD','AMD',t_row('AMD')),('램리서치 LRCX','LRCX',t_row('LRCX')),
      ('마이크론 MU','MU',t_row('MU')),('오라클 ORCL','ORCL',t_row('ORCL'))]
W,H=1200,750; P=236; INK=18
im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.text((40,18),'SOX',font=F(B,120),fill=INK)
d.text((300,40),'장중 -8% → 종가 -0.65%',font=F(B,46),fill=INK)
d.text((302,104),'11/25(수) 전날 종가 대비 · ○ 장중 저점 → ● 종가',font=F(BD,24),fill=70)
x0=640; sc=27  # 0% 위치, 1%p = 27px
yt=176
for v in (0,-2,-4,-6,-8,-10,-12):
    x=x0+v*sc; d.line((x,yt,x,yt+468),fill=INK if v==0 else 190,width=3 if v==0 else 1)
    d.text((x,yt-4),f'{v}%' if v else '0',font=F(BD,17),fill=90,anchor='ms')
y=yt+14
for lab,k,(c,p,lo) in rows:
    cp=(c/p-1)*100; lp=(lo/p-1)*100
    d.text((40,y+22),lab,font=F(BD,23),fill=INK,anchor='lm')
    xl,xc=x0+lp*sc,x0+cp*sc
    d.line((xl,y+22,xc,y+22),fill=INK,width=8)
    d.ellipse((xl-11,y+11,xl+11,y+33),outline=INK,width=4,fill=P)
    d.ellipse((xc-12,y+10,xc+12,y+34),fill=INK)
    d.text((xl-16,y+22),f'{lp:.1f}%',font=F(BD,19),fill=80,anchor='rm')
    d.text((x0+12,y+22),f'{cp:+.2f}%',font=F(B,24),fill=INK,anchor='lm')
    y+=66
d.line((790,40,790,H-60),fill=INK,width=2) if False else None
# 오른쪽 숫자 칸
def box(y,big,small,inv=False):
    d.rectangle((842,y,1172,y+104),outline=INK,width=3,fill=INK if inv else P)
    d.text((858,y+2),big,font=F(B,48),fill=P if inv else INK)
    d.text((860,y+70),small,font=F(BD,19),fill=P if inv else 60)
sc_,sp_,sl_=s_row('^SOX'); v_c,v_p,_=s_row('^VIX'); vh=float(S['^VIX'][5])
nc,np_,nl=t_row('NVDA')
box(176,f'{sc_:,.0f}',f'반도체 지수 종가 · 장중 {sl_:,.0f}',True)
box(296,f'{nc:.2f}달러',f'엔비디아 종가 · 장중 {nl:.2f}')
box(416,f'{vh:.2f}',f'VIX 장중 최고 → 종가 {v_c:.2f}')
box(536,'1,314bp','코어위브 5년 CDS 사상 최고')
d.text((858,660),'S&P Global 집계 · 11/25',font=F(BD,17),fill=80)
d.line((14,H-40,W-14,H-40),fill=INK,width=1)
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.26 · 시세: CNBC 일봉(11/25) · CDS: Motley Fool·S&P Global',font=F(BD,15),fill=70,anchor='rm')
im.convert('RGB').save('img/2026-11-26-top.jpg',quality=88)
print('ok')
