"""2026-11-25 1면 두 번째 그림: 델 '분기 계단' — AI 수주잔고(지난 분기 950억→1,323억 달러)·AI 서버 매출(164억→220억)·연간 매출 전망(1,920억→2,020억)
세 쌍의 '전→후' 계단 막대 + 11/24 하루 가격 범위(시가·고가·저가·종가)와 시간외 첫 값 점.
top(나비 막대)·11/24(사다리·계산식) 그림과 겹치지 않는 구성. 숫자: 델 실적 발표(BusinessWire, stocktitan), financefeeds(시간외), CNBC 일봉."""
import json
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
TD=json.load(open('data/tm_daily.json')); o,h,l,c,ch=TD['DELL'][1:6]
prev=334.91; ah=300.57
W,H=1200,750; P=236; INK=18
im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.text((40,18),'DELL',font=F(B,120),fill=INK)
d.text((44,150),'3분기 · 지난 분기 → 이번 분기',font=F(B,36),fill=INK)
d.text((46,200),'단위: 억 달러 · 회사 발표(11/24 장 마감 후)',font=F(BD,22),fill=70)
# 계단 막대 3쌍
pairs=[('AI 수주잔고',950,1323,'2분기 말 → 3분기 말'),('AI 서버 분기 매출',164,220,'2분기 → 3분기'),('연간 매출 전망',1920,2020,'이전 → 새 전망')]
x=50; base=640
for lab,a,b,sub in pairs:
    mx=max(a,b); sc=330/mx
    for j,(v,col) in enumerate([(a,150),(b,INK)]):
        x0=x+j*92; top=base-v*sc
        d.rectangle((x0,top,x0+78,base),fill=col)
        d.text((x0+39,top-8),f'{v:,}',font=F(B if j else BD,26 if j else 22),fill=INK if j else 70,anchor='ms')
    d.line((x+78,base-a*sc,x+92,base-b*sc),fill=INK,width=3)
    d.text((x+85,base+12),lab,font=F(B,22),fill=INK,anchor='mt')
    d.text((x+85,base+44),sub,font=F(BD,17),fill=80,anchor='mt')
    x+=230
# 오른쪽: 11/24 하루 가격 범위 + 시간외
d.line((740,40,740,H-60),fill=INK,width=2)
d.text((766,40),'11/24 주가 (달러)',font=F(B,30),fill=INK)
lo_,hi_=285,340; y0,y1=600,150
Y=lambda v:y0-(v-lo_)/(hi_-lo_)*(y0-y1)
xb=885
d.line((xb,Y(h),xb,Y(l)),fill=INK,width=6)
d.rectangle((xb-34,Y(o),xb+34,Y(c)),fill=INK)
for v,lab in [(prev,'11/23 종가'),(h,'고가'),(o,'시가'),(c,'종가'),(l,'저가')]:
    d.line((xb-60,Y(v),xb-40,Y(v)),fill=INK,width=2)
    d.text((xb-66,Y(v)),f'{v:.2f}',font=F(BD,20),fill=INK,anchor='rm')
    d.text((xb+44,Y(v)),lab,font=F(BD,19),fill=70,anchor='lm') if lab!='종가' else None
d.line((xb-40,Y(prev),xb+40,Y(prev)),fill=130,width=2)
d.text((xb,Y(l)+22),f'종가 {ch:+.2f}%',font=F(B,26),fill=INK,anchor='mt')
xa=1100; d.ellipse((xa-12,Y(ah)-12,xa+12,Y(ah)+12),fill=INK)
d.text((xa,Y(ah)-20),'시간외',font=F(BD,20),fill=INK,anchor='ms')
d.text((xa,Y(ah)+20),f'{ah:.2f}',font=F(B,22),fill=INK,anchor='mt')
d.text((xa,Y(ah)+48),'+1.79%',font=F(B,22),fill=INK,anchor='mt')
d.text((xa,Y(ah)+76),'16:37 ET',font=F(BD,16),fill=80,anchor='mt')
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.25 · 실적: 델 발표(BusinessWire) · 시세: CNBC 일봉 · 시간외: financefeeds 16:37 ET',font=F(BD,15),fill=90,anchor='rm')
im.convert('RGB').save('img/2026-11-25-top2.jpg',quality=88); print('ok',o,h,l,c)
