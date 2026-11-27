"""11/28 호 그림: top(SNDK 최근 15일 종가 막대 + 마지막 날 강조 + 숫자 박스), top2(세 지수 하루 등락 가로 막대 + 앤트로픽 박스), 뉴스 카드 2장(타이포)."""
from PIL import Image, ImageDraw, ImageFont
import json
BL='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BO='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s: ImageFont.truetype(p,s)
D='2026-11-28'; P=(236,234,228); K=(20,20,20); G=(130,130,130)
S={l.split('|')[0]:l.split('|')[1].split(',') for l in open('data/summary.txt') if '|' in l and not l.startswith('sym')}
v=[r[4] for r in json.load(open('data/sndk_daily.json'))][-15:]
sn=float(S['SNDK'][1]); sc=float(S['SNDK'][3]); hi=float(S['SNDK'][13])
assert abs(v[-1]-sn)<0.01
im=Image.new('RGB',(1200,750),P); d=ImageDraw.Draw(im)
d.text((50,20),'SNDK',font=F(BL,200),fill=K); d.text((60,250),'SANDISK · 블랙프라이데이 메모리 반등 · 11/27',font=F(BO,32),fill=K)
x0,y0,x1,y1=60,330,760,700; mx=max(v)*1.05; bw=(x1-x0)/len(v)
for i,c in enumerate(v):
    h=(c/mx)*(y1-y0); col=K if i==len(v)-1 else G
    d.rectangle((x0+i*bw+4,y1-h,x0+(i+1)*bw-4,y1),fill=col)
d.text((x0,y0-34),'최근 15거래일 종가(달러)',font=F(BO,24),fill=G)
d.rectangle((820,40,1150,280),outline=K,width=5); d.text((845,60),'하루 등락',font=F(BO,30),fill=K); d.text((840,115),f'+{sc:.1f}%',font=F(BL,80),fill=K)
d.rectangle((820,320,1150,500),outline=K,width=3); d.text((845,335),'11/27 종가',font=F(BO,28),fill=K); d.text((845,380),f'${sn:.2f}',font=F(BL,66),fill=K)
d.rectangle((820,540,1150,700),fill=K); d.text((845,560),'52주 고점 대비',font=F(BO,28),fill=P); d.text((845,605),f'{(sn/hi-1)*100:.0f}%',font=F(BL,66),fill=P)
im.save(f'img/{D}-top.jpg',quality=88)
im=Image.new('RGB',(1200,750),P); d=ImageDraw.Draw(im)
d.text((50,30),'WEEKLY',font=F(BL,170),fill=K); d.text((60,240),'S&P 500 1년 반 만의 최고 주간 · 11/27 하루 등락',font=F(BO,32),fill=K)
rows=[('나스닥',float(S['^IXIC'][3])),('S&P 500',float(S['^GSPC'][3])),('다우',float(S['^DJI'][3])),('반도체',float(S['^SOX'][3]))]
for i,(n,p) in enumerate(rows):
    y=320+i*95; d.text((60,y+5),n,font=F(BL,46),fill=K); w=int(p/6.5*330)
    d.rectangle((300,y+8,300+w,y+70),fill=K if n=='반도체' else G); d.text((315+w,y+5),f'▲ {p:.2f}%',font=F(BL,48),fill=K)
d.rectangle((860,320,1150,690),outline=K,width=5); d.text((885,340),'ANT',font=F(BL,90),fill=K); d.text((885,460),'앤트로픽',font=F(BO,32),fill=K); d.text((885,520),'약 +11%',font=F(BL,52),fill=K); d.text((880,615),'공모가 83달러 위',font=F(BO,24),fill=K)
im.save(f'img/{D}-top2.jpg',quality=88)
print('ok', v[-3:], sn)
