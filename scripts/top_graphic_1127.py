"""11/27 휴장일 호 그림: top(ES 선물 — S&P 500 최근 10일 종가 꺾은선 + 선물 박스), top2(대만·일본 막대 비교), 뉴스 카드 3장(타이포만)."""
from PIL import Image, ImageDraw, ImageFont
BL='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BO='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s: ImageFont.truetype(p,s)
D='2026-11-27'; P=(236,234,228); K=(20,20,20); G=(120,120,120)
ln=[l for l in open('data/raw_series.txt') if l.startswith('^GSPC|')][0]
v=[int(x)/10 for x in ln.split('|')[1].split()][-10:]
dts=open('data/raw_series.txt').readline().split('|')[1].split()[-10:]
# top
im=Image.new('RGB',(1200,750),P); d=ImageDraw.Draw(im)
d.text((50,30),'ES',font=F(BL,210),fill=K); d.text((60,265),'S&P 500 FUTURES · 추수감사절 휴장',font=F(BO,34),fill=K)
x0,y0,x1,y1=60,340,760,700; mn,mx=min(v)-20,max(v)+20
pts=[(x0+i*(x1-x0)/9, y1-(c-mn)/(mx-mn)*(y1-y0)) for i,c in enumerate(v)]
d.line(pts,fill=K,width=6)
for (x,y),dt in zip(pts,dts): d.ellipse((x-7,y-7,x+7,y+7),fill=K); d.text((x-22,y1+8),dt[:2]+'/'+dt[2:],font=F(BO,20),fill=G)
d.text((x0,y0-36),'S&P 500 최근 10거래일 종가',font=F(BO,24),fill=G)
d.rectangle((820,60,1150,300),outline=K,width=5); d.text((845,80),'선물(휴장 중)',font=F(BO,30),fill=K); d.text((845,140),'+0.7%',font=F(BL,96),fill=K)
d.rectangle((820,340,1150,520),outline=K,width=3); d.text((845,355),'11/25 종가',font=F(BO,28),fill=K); d.text((845,400),f'{v[-1]:,.2f}',font=F(BL,58),fill=K)
d.rectangle((820,560,1150,700),fill=K); d.text((845,580),'금 13:00 ET',font=F(BO,30),fill=P); d.text((845,630),'조기 폐장',font=F(BL,44),fill=P)
im.save(f'img/{D}-top.jpg',quality=88)
# top2
im=Image.new('RGB',(1200,750),P); d=ImageDraw.Draw(im)
d.text((50,30),'ASIA CHIPS',font=F(BL,140),fill=K); d.text((60,210),'미국 휴장 중 아시아 반도체 반등 · 11/26',font=F(BO,34),fill=K)
for i,(n,p) in enumerate([('대만 가권',2.5),('일본 닛케이',0.9)]):
    y=330+i*190; d.text((60,y+20),n,font=F(BL,54),fill=K); w=int(p/2.5*380)
    d.rectangle((420,y,420+w,y+120),fill=K if i==0 else G); d.text((440+w,y+20),f'▲ {p}%',font=F(BL,70),fill=K)
d.line((60,700,1140,700),fill=K,width=3)
im.save(f'img/{D}-top2.jpg',quality=88)
for name,big,sub,box in [('gold','GOLD','금 · 온스당','3,600달러 시험'),('bf','13:00','블랙프라이데이 조기 폐장','한국 토 03:00'),('btc','BTC','비트코인 · 기술 신호','일봉 약세')]:
    im=Image.new('RGB',(640,400),P); d=ImageDraw.Draw(im)
    d.text((30,20),big,font=F(BL,150),fill=K); d.text((36,215),sub,font=F(BO,32),fill=K)
    d.rectangle((30,290,610,370),fill=K); d.text((50,298),box,font=F(BL,46),fill=P)
    im.save(f'img/{D}-{name}.jpg',quality=88)
print('img ok', v[-1])
