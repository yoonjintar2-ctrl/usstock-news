"""2026-11-21 1면 두 번째 기사 그림: 브로드컴 22거래일 캔들 + 구글 TPU 8i 2027 출하 계획(궈밍치 설문) — 실제 숫자 흑백 그래픽."""
import json, base64
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
m=json.load(open('data/tickers_mini.json'))['AVGO']; td=json.load(open('data/tm_daily.json'))['AVGO']
mn,mx=m[0],m[1]; b=base64.b64decode(m[2]); n=len(b)//4
q=lambda v:mn+v/255*(mx-mn)
O=[[q(b[i*4+k]) for k in range(4)] for i in range(n)]; O[-1][3]=td[4]
W,H=1200,750; P=236; INK=18
im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.text((40,28),'AVGO',font=F(B,112),fill=INK)
d.text((44,162),'브로드컴 · 최근 22거래일 일봉',font=F(BD,28),fill=50)
x0,x1,y0,y1=60,700,640,230; lo,hi=285,375
Y=lambda v:y0-(v-lo)/(hi-lo)*(y0-y1)
for v in (300,325,350):
    d.line((x0,Y(v),x1,Y(v)),fill=190,width=1); d.text((x0-8,Y(v)),f'{v}',font=F(BD,18),fill=110,anchor='rm')
cw=(x1-x0)/n
for i,(o,h,l,c) in enumerate(O):
    x=x0+cw*(i+.5); col=INK if c<o else 120
    d.line((x,Y(h),x,Y(l)),fill=col,width=2)
    d.rectangle((x-cw*.32,Y(max(o,c)),x+cw*.32,max(Y(min(o,c)),Y(max(o,c))+2)),fill=col if c<o else P,outline=col,width=2)
d.text((x1-4,Y(td[4])+30),f'11/20 종가 {td[4]:.2f}달러',font=F(B,26),fill=INK,anchor='rm')
d.rectangle((40,668,360,718),fill=INK); d.text((56,672),f'하루 {td[5]:+.2f}%',font=F(B,30),fill=P)
# 오른쪽: 2027 TPU 8i 출하 계획
d.line((750,40,750,H-60),fill=INK,width=2)
d.text((780,40),'구글 TPU 8i',font=F(B,52),fill=INK)
d.text((782,108),'2027년 출하 계획 (궈밍치 설문)',font=F(BD,24),fill=50)
bx,bw=800,130; base=600
for i,(lab,v) in enumerate((('기존 계획',100),('설문 뒤',80))):
    x=bx+i*(bw+80); top=base-v*3.4
    d.rectangle((x,top,x+bw,base),fill=INK if i==0 else 120)
    d.text((x+bw/2,top-26),f'{v}',font=F(B,34),fill=INK,anchor='mm')
    d.text((x+bw/2,base+28),lab,font=F(BD,24),fill=60,anchor='mm')
d.text((780,668),'약 100만 개(≈20%) 감소',font=F(B,30),fill=INK)
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.21 · 시세: CNBC 일봉 · 설문: TF인터내셔널 궈밍치(구글·브로드컴 미확인)',font=F(BD,15),fill=90,anchor='rm')
im.convert('RGB').save('img/2026-11-21-top2.jpg',quality=88)
