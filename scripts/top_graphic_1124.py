"""2026-11-24 1면 그림: 엔비디아 '가격 사다리'(52주 고점·50일선·20일선·11/20 종가·11/23 종가를 한 세로축에) + 핵심 숫자 박스 + 지수 하루 등락 숫자 칸.
11/21(꺾은선·가로 막대)·11/21b(캔들·세로 막대)와 겹치지 않게 세로 가격축 사다리 구성. 숫자는 data/summary.txt(CNBC 일봉 11/23) 확인값."""
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
S={l.split('|')[0]:l.split('|')[1].split(',') for l in open('data/summary.txt').read().split('\n')[1:] if '|' in l}
nv=S['NVDA']; c,p,ch,hi52=float(nv[1]),float(nv[2]),float(nv[3]),float(nv[13]); m20,m50=float(nv[7]),float(nv[8])
W,H=1200,750; P=236; INK=18
im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.text((40,22),'NVDA',font=F(B,132),fill=INK)
d.text((46,182),'엔비디아 · 가격 사다리 (11/23 종가 기준)',font=F(BD,26),fill=60)
# 세로 가격축
ax=150; y0,y1=660,240; lo,hi=115,250
Y=lambda v:y0-(v-lo)/(hi-lo)*(y0-y1)
d.line((ax,y1-10,ax,y0+6),fill=INK,width=4)
marks=[(hi52,'52주 최고가 (10/6)',120),(m50,'50일 이동평균',120),(m20,'20일 이동평균',120),(c,'11/23 종가',INK),(p,'11/20 종가',INK)]
for v,lab,col in marks:
    y=Y(v); big=col==INK
    d.line((ax-14,y,ax+(470 if big else 300),y),fill=col,width=4 if big else 2)
    d.text((ax-22,y),f'{v:.2f}',font=F(B if big else BD,30 if big else 22),fill=col,anchor='rm')
    d.text((ax+(480 if big else 310),y),lab,font=F(BD,22),fill=col,anchor='lm')
# 화살표 11/20 → 11/23
xa=ax+250; ya,yb=Y(p)-8,Y(c)+10
d.line((xa,ya,xa,yb+18),fill=INK,width=12)
d.polygon([(xa-26,yb+22),(xa+26,yb+22),(xa,yb-6)],fill=INK)
d.rectangle((xa+30,(ya+yb)/2-34,xa+230,(ya+yb)/2+34),fill=INK)
d.text((xa+130,(ya+yb)/2),f'{ch:+.2f}%',font=F(B,40),fill=P,anchor='mm')
# 오른쪽 숫자 칸
d.line((760,40,760,H-60),fill=INK,width=2)
def box(y,big,small,inv=False):
    d.rectangle((786,y,1172,y+118),outline=INK,width=3,fill=INK if inv else P)
    d.text((806,y+4),big,font=F(B,60),fill=P if inv else INK)
    d.text((808,y+82),small,font=F(BD,22),fill=P if inv else 60)
box(40,f'+{c-p:.2f}달러','하루 상승 폭 (125.53 → 165.05달러)',True)
box(176,f'{(c/hi52-1)*100:.1f}%','52주 최고가 대비 아직 남은 거리')
d.text((786,322),'11/23 하루 등락',font=F(B,30),fill=INK)
rows=[('필라델피아 반도체',S['^SOX'][3]),('나스닥 종합',S['^IXIC'][3]),('S&P 500',S['^GSPC'][3]),('VIX(변동성)',S['^VIX'][3])]
for i,(nm,v) in enumerate(rows):
    y=372+i*70
    d.line((786,y+58,1172,y+58),fill=150,width=1)
    d.text((790,y+28),nm,font=F(BD,26),fill=INK,anchor='lm')
    d.text((1168,y+28),f'{float(v):+.2f}%',font=F(B,32),fill=INK,anchor='rm')
d.rectangle((40,676,640,722),fill=INK); d.text((54,680),'젠슨 황 CEO 복귀 · 하루 +31.48%',font=F(B,28),fill=P)
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.24 · 시세: CNBC 일봉(11/23 종가)',font=F(BD,16),fill=90,anchor='rm')
im.convert('RGB').save('img/2026-11-24-top.jpg',quality=88); print('ok')
