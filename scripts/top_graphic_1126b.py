"""2026-11-26 1면 두 번째 그림: '예상 vs 실제' 성적표(왼쪽, 가로 점 비교) + 미 국채 10년 최근 6거래일 종가 계단(오른쪽).
11/25b(세로 막대+캔들)·오늘 1면(덤벨)과 다른 구성. 지표 숫자: BEA·Reuters·CalculatedRisk 보도, 금리: archive indicators·CNBC 일봉."""
import json, glob
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
S={l.split('|')[0]:l.split('|')[1].split(',') for l in open('data/summary.txt').read().split('\n')[1:] if '|' in l}
tn=[]
for f in sorted(glob.glob('archive/2026-11-*.json')):
    a=json.load(open(f)); i={x['name']:x['v'] for x in a.get('indicators',[])}
    if i.get('미 국채 10년'): tn.append((a['session'][5:10].replace('-','/'),i['미 국채 10년']))
tn.append(('11/25',float(S['^TNX'][1])))
W,H=1200,750; P=236; INK=18
im=Image.new('L',(W,H),P); d=ImageDraw.Draw(im)
d.rectangle((8,8,W-9,H-9),outline=INK,width=3)
d.text((40,18),'PCE',font=F(B,120),fill=INK)
d.text((300,40),'물가·성장, 예상보다 뜨거웠다',font=F(B,46),fill=INK)
d.text((302,100),'10월 PCE · 3분기 GDP 수정치 · 고용 · 주택 (11/25 발표)',font=F(BD,23),fill=70)
rows=[('근원 PCE (전년 대비)','3.2%','3.3%','이전 3.1%'),('PCE (전년 대비)','3.8%','3.8%','이전 3.6%'),
      ('3분기 GDP (연율)','3.5%','4.3%','속보 3.4%'),('실업수당 청구','20.0만','18.9만','적을수록 고용 탄탄'),
      ('10월 신규주택판매','66.0만','70.1만','9월 61.4만')]
y=170
d.text((330,y),'예상',font=F(BD,20),fill=90,anchor='ms'); d.text((470,y),'실제',font=F(B,22),fill=INK,anchor='ms')
y+=16
for lab,e,a,note in rows:
    d.line((40,y,690,y),fill=190,width=1)
    d.text((40,y+36),lab,font=F(BD,23),fill=INK,anchor='lm')
    d.text((330,y+36),e,font=F(BD,26),fill=110,anchor='mm')
    d.rectangle((410,y+10,530,y+62),fill=INK); d.text((470,y+36),a,font=F(B,30),fill=P,anchor='mm')
    d.text((548,y+36),note,font=F(BD,17),fill=90,anchor='lm')
    y+=78
d.line((40,y,690,y),fill=190,width=1)
# 오른쪽: 10년물 계단 + 인상 확률
d.line((720,150,720,H-60),fill=INK,width=2)
d.text((748,160),'미 국채 10년 (%) · 종가',font=F(B,24),fill=INK)
lo,hi=4.80,5.10; top,bot=240,450; X0,X1=770,1150
yy=lambda v: bot-(v-lo)/(hi-lo)*(bot-top)
n=len(tn); step=(X1-X0)/n
for i,(dt,v) in enumerate(tn):
    x=X0+i*step; yv=yy(v)
    d.rectangle((x+6,yv,x+step-6,bot),fill=INK if i==n-1 else 160)
    d.text((x+step/2,yv-8),f'{v:.2f}',font=F(B if i==n-1 else BD,21),fill=INK,anchor='ms')
    d.text((x+step/2,bot+24),dt,font=F(BD,17),fill=70,anchor='ms')
d.line((X0,bot,X1,bot),fill=INK,width=2)
d.text((748,490),'뜨거운 물가에도 금리는 하락 — 주식 급락에 채권으로',font=F(BD,18),fill=60)
d.rectangle((748,530,1172,648),fill=INK)
d.text((766,532),'약 95.8%',font=F(B,52),fill=P)
d.text((768,606),'12월 FOMC 0.25%p 인상 확률(11/25 오후)',font=F(BD,19),fill=P)
d.line((14,H-40,W-14,H-40),fill=INK,width=1)
d.text((W-24,H-22),'미국주식 늬우스 · 2026.11.26 · BEA·Reuters·CalculatedRisk · 금리: CNBC·지난 호 · 확률: CME 선물 기준 계산(PredictionMarketsPicks)',font=F(BD,14),fill=70,anchor='rm')
im.convert('RGB').save('img/2026-11-26-top2.jpg',quality=88)
print('ok',tn)
