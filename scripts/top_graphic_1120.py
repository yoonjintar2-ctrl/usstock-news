"""2026-11-20 1면 그림: 실제 숫자로 그린 흑백 신문 그래픽 (추상 3D 소품 대신)."""
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; SR='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1 if 'Sans' in p else 0)
W,H=1200,750; PAPER=236; INK=18
im=Image.new('L',(W,H),PAPER); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.line((W//2,40,W//2,H-60),fill=INK,width=2)
# 왼쪽: 앤트로픽 첫날 주요 가격
d.text((40,32),'ANT',font=F(B,120),fill=INK)
d.text((44,175),'앤트로픽 · 나스닥 상장 첫날',font=F(BD,30),fill=50)
pts=[('공모가',83.0),('첫 체결',111.50),('장중 고가',114.99),('종가',97.17)]
x0,x1,y0,y1=100,520,580,290; lo,hi=75,120
P=[(x0+i*(x1-x0)/3, y0-(v-lo)/(hi-lo)*(y0-y1)) for i,(_,v) in enumerate(pts)]
d.line((x0,y0-(83-lo)/(hi-lo)*(y0-y1),x1,y0-(83-lo)/(hi-lo)*(y0-y1)),fill=150,width=2)
d.line(P,fill=INK,width=7,joint='curve')
for (lab,v),(x,y) in zip(pts,P):
    d.ellipse((x-11,y-11,x+11,y+11),fill=INK)
    t=f'{v:.2f}달러' if v!=83 else '83달러'
    for txt,yy,fn in ((t,y-42,F(B,28)),(lab,y+38,F(BD,22))):
        bb=d.textbbox((x,yy),txt,font=fn,anchor='mm'); d.rectangle((bb[0]-6,bb[1]-4,bb[2]+6,bb[3]+4),fill=PAPER)
        d.text((x,yy),txt,font=fn,fill=INK if fn.size==28 else 60,anchor='mm')
d.rectangle((40,668,330,718),fill=INK); d.text((56,672),'공모가 대비 +17.1%',font=F(B,30),fill=PAPER)
# 오른쪽: S&P 500 최근 7일 종가(6일 연속 하락)
d.text((640,32),'S&P 500',font=F(B,96),fill=INK)
d.text((644,150),'6거래일 연속 하락 · 2024년 이후 최장',font=F(BD,30),fill=50)
days=['11/11','11/12','11/13','11/16','11/17','11/18','11/19']
cl=[7619.4,7592.4,7561.7,7416.6,7340.5,7323.6,7175.8]
bx0,bx1,by0,by1=650,1160,600,250; lo,hi=7100,7650
bw=(bx1-bx0)/7
for i,(dd,v) in enumerate(zip(days,cl)):
    x=bx0+i*bw; top=by0-(v-lo)/(hi-lo)*(by0-by1)
    d.rectangle((x+8,top,x+bw-8,by0),fill=INK if i==6 else 110)
    d.text((x+bw/2,top-20),f'{v:,.0f}',font=F(BD,20),fill=INK,anchor='mm')
    d.text((x+bw/2,by0+22),dd,font=F(BD,20),fill=60,anchor='mm')
d.rectangle((640,668,950,718),fill=INK); d.text((656,672),'하루 -2.02% · 7,176',font=F(B,30),fill=PAPER)
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.20 · 시세: 야후 파이낸스 · AP',font=F(BD,16),fill=90,anchor='rm')
im.convert('RGB').save('img/2026-11-20-top.jpg',quality=88)
# 간밤 뉴스용 S&P 그림(같은 막대, 작게)
sp=im.crop((640,262,1170,630)).convert('RGB'); sp.save('/tmp/spxbars.png')
