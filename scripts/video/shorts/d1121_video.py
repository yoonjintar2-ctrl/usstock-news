"""미국주식 늬우스 11/21(토) 1면 두 건 → 8비트 쇼츠 2편 (2026-11-22 제작, press_video.py 틀)
VID=nvda | avgo  python3 d1121_video.py [times|stills T,T|audio|full]
사실(출처: 미국주식 늬우스 2026-11-21호, 기준 11/20 미국 종가, 환율 1,346원/달러):
 nvda: 로이터 'SEC가 엔비디아 회계 문제 가능성 조사' 보도 · NVDA -14.01% $125.53(약 17만 원) · 시총 약 4,910억 달러(약 661조 원) 증발
       10/6 최고 종가 $239.24(약 32만 원) 대비 -47.5% · SOX -10.73% · 나스닥 -5.28% · S&P 500 -3.70%, 7일 연속 하락·조정 진입
       SEC·엔비디아 무응답 · CNN 공포탐욕 장중 14(3/30 이후 최저) · S&P RSI 25 · 조사가 곧 잘못은 아님
 avgo: 궈밍치(TF인터내셔널) X 게시 업계 설문 '구글 2027년 브로드컴 설계 TPU 8i 출하 약 100만 개(약 20%) 축소, 미디어텍 설계 TPU 8t 확대'
       AVGO -12.19% $304.41(약 41만 원) · 시총 약 1,910억 달러(약 257조 원) 증발 · 최고가 대비 -36% · 마벨 -10%
       구글·브로드컴 확인 안 함 · '투자 축소가 아니라 배분 조정' 해석(팁랭크스) · 반도체 전체 투매일 · 12/9 실적 발표
투자 권유 아님. 상승/하락 빨강·초록 구분 없음."""
import os, sys, math, json, hashlib, wave
import numpy as np
from PIL import Image, ImageDraw

from make_video import (W, H, FW, FH, FPS, F24, F12, F9, WHITE, YEL, CYAN, ORG, GRAY, DIM, BG, prog, ease, lerp, tone, mtof, SR, typed, blink)
from sandisk_video import box, slam, CX, WHT2, chip
from nike_video import stamp_slam, debris, dk, DARK, render_low, shutter_mask, dissolve_mask, clamp, TR, warn_icon
from bgm_kit import bgm as bgm_make, level_plan

VID = os.environ.get("VID", "nvda")
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, f"d1121_{VID}/out"); os.makedirs(OUT, exist_ok=True)
NDIR = os.path.join(BASE, f"d1121_{VID}/narr"); os.makedirs(NDIR, exist_ok=True)
def clip_path(n): return os.path.join(NDIR, hashlib.md5(f"q|{n}".encode()).hexdigest() + ".npy")
GAP, TAIL = 0.32, 0.5
NEU = (200, 206, 220)
GOLD = (240, 190, 60); PAPER = (230, 226, 210); INK = (40, 40, 50)

def head(d, t, small, big, col=YEL):
    d.text((CX, 52), small, font=F9, fill=GRAY, anchor="ma")
    s = typed(big, t, 0.1, 20)
    d.text((CX - d.textlength(big, font=F24) / 2, 64), s, font=F24, fill=col)

def tag(d, x, y, s, col=CYAN, font=F9, right=False):
    w = int(d.textlength(s, font=font)) + 8; x0 = x - w if right else x
    d.rectangle([x0, y, x0 + w, y + 14], fill=(10, 14, 30), outline=col); d.text((x0 + 4, y + 2), s, font=font, fill=col)

def punch(t, t0, amp=4):
    u = t - t0
    return {"shake": (int(math.sin(u * 60) * amp * max(0, 1 - u / 0.3)), 0)} if 0 <= u < 0.3 else {}

def seg_len(seg, dur, i=0):
    return (seg[i + 1] - seg[i]) if i + 1 < len(seg) else dur - seg[i] - TAIL - 0.15

# ================================================================ host stage
STARS = [((i * 73) % 250 + 10, (i * 151) % 190 + 8, i % 3) for i in range(26)]
def stage(img, d, t, title, small, col=YEL, note=None):
    for (x, y, k) in STARS:
        if ((t * 1.3 + k * 0.4 + x * 0.01) % 1) < 0.75: d.point((x, y), fill=(120, 130, 170) if k else (200, 205, 230))
    for s in range(14):
        y0 = 150 + s * 22; hw = 22 + s * 9
        d.rectangle([W // 2 - hw, y0, W // 2 + hw, y0 + 22], fill=(26, 32, 62))
    d.rectangle([0, 452, W, H], fill=(18, 14, 18)); d.line([(0, 452), (W, 452)], fill=(220, 150, 50), width=1)
    tw = d.textlength(title, font=F24)
    d.text((W // 2 - tw / 2 + 1, 29), title, font=F24, fill=(0, 0, 0)); d.text((W // 2 - tw / 2, 28), title, font=F24, fill=col)
    if small: d.text((W // 2, 58), small, font=F12, fill=WHITE, anchor="ma")
    if note: d.text((W // 2, 466), note, font=F9, fill=GRAY, anchor="ma")

# ================================================================ sprites
def doc(d, x, y, title):
    d.rectangle([x, y, x + 70, y + 88], fill=PAPER, outline=GRAY)
    d.polygon([(x + 56, y), (x + 70, y), (x + 70, y + 14)], fill=(190, 186, 170))
    d.text((x + 6, y + 5), title, font=F9, fill=INK)
    for r in range(7):
        w = 56 if r % 3 else 40
        d.rectangle([x + 6, y + 22 + r * 9, x + 6 + w, y + 24 + r * 9], fill=(150, 150, 160))

def magnifier(d, x, y):
    d.ellipse([x - 14, y - 14, x + 14, y + 14], outline=WHITE, width=3)
    d.ellipse([x - 11, y - 11, x + 11, y + 11], outline=CYAN)
    d.line([(x + 10, y + 10), (x + 24, y + 24)], fill=GOLD, width=5)

def line_chart(d, pts, u, col=NEU):
    n = max(2, int(len(pts) * u))
    if n > 1: d.line(pts[:n], fill=col, width=2)
    x, y = pts[n - 1]; d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=WHITE)
    return pts[n - 1]

def path(xs, ys, seed=0):
    out = []
    for i in range(len(xs) - 1):
        for k in range(10):
            f = k / 10; x = lerp(xs[i], xs[i + 1], f); y = lerp(ys[i], ys[i + 1], f)
            y += math.sin(x * 0.5 + seed) * 1.5 * (1 if i < len(xs) - 2 else 0.2)
            out.append((x, y))
    out.append((xs[-1], ys[-1])); return out

# ================================================================ NVDA scenes
def n_hook(img, d, t, seg, dur): stage(img, d, t, "엔비디아 -14%", "시총 약 661조 원 증발")
def n_mid(img, d, t, seg, dur): stage(img, d, t, "근데 말이죠", "조사 = 잘못? 아직 몰라요", CYAN)
def n_end(img, d, t, seg, dur): stage(img, d, t, "기회? 함정?", "여러분 생각은?", note="※ 투자 권유 아님 · 11/20 미국 종가 기준")

def n_news(img, d, t, seg, dur):
    head(d, t, "로이터 단독 보도 · 11/20", "회계 조사?")
    L = seg_len(seg, dur, 0); T0 = seg[0]
    doc(d, 90, 118, "NVDA 장부")
    # 돋보기가 장부 위를 훑음
    if t > T0 + 0.2:
        u = prog(t, T0 + 0.2, T0 + 0.2 + L * 0.6)
        mx = 104 + math.sin(u * math.pi * 3) * 22; my = 140 + u * 46
        magnifier(d, mx, my)
    vis, o = slam(t, 0.25, 0.2)
    if vis:
        tag(d, 32, 102 + o, "SEC", YEL, F12)
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 222 + o, 220, 246 + o], fill=(14, 16, 32), outline=GRAY)
        d.text((CX, 229 + o), "SEC · 엔비디아  모두 무응답", font=F9, fill=WHT2, anchor="ma")
    Ts = T0 + L * 0.72
    if t > Ts: stamp_slam(img, CX, 286, "조사 중?", YEL, t, Ts, "24", -8)
    return punch(t, Ts, 3)

def n_drop(img, d, t, seg, dur):
    head(d, t, "10/6 최고 종가 → 11/20 종가", "고점 -47.5%")
    box(d, 30, 104, 220, 252, DIM)
    L = seg_len(seg, dur, 0); T0 = seg[0]
    ys = [128, 150, 170, 162, 200, 238]; xs = [40, 80, 120, 150, 182, 210]
    pts = path(xs, ys, 1)
    u = ease(prog(t, 0.3, T0 + L * 0.75))
    x, y = line_chart(d, pts, u)
    if t > 0.4: tag(d, 36, 108, "$239 약 32만 원", CYAN)
    Thit = T0 + L * 0.72
    if t > Thit:
        vis, o = slam(t, Thit, 0.2); tag(d, 214, 216 + o, "$125.5 약 17만 원", YEL, right=True)
        debris(d, 210, 238, t, Thit, 10, (WHITE, YEL, NEU), 40, 0.6, 2, 2)
    Ts = Thit + 0.5
    if len(seg) > 1:
        Ts = seg[1] + 0.2
        if t > seg[1]: d.text((CX, 260), "하루 만에 -14% · 시총 약 661조 원", font=F9, fill=WHT2, anchor="ma")
    if t > Ts: stamp_slam(img, CX, 304, "-14%", YEL, t, Ts, "24", -8)
    fx = punch(t, Thit, 4)
    if Ts <= t < Ts + 0.08: fx["flash"] = 0.18
    return fx

DOM = [("엔비디아", "-14.0%"), ("반도체", "-10.7%"), ("나스닥", "-5.3%"), ("S&P", "-3.7%")]
def n_domino(img, d, t, seg, dur):
    head(d, t, "같이 무너진 금요일", "도미노")
    L = dur - TAIL - 0.15 - seg[0]; T0 = seg[0]
    hits = [T0 + 0.2 + L * f for f in (0.0, 0.2, 0.42, 0.62)]
    for k, ((nm, v), th) in enumerate(zip(DOM, hits)):
        x = 40 + k * 46; ytop = 120
        a = ease(prog(t, th, th + 0.35)) * (70 if k < 3 else 0)
        # 기울어지는 도미노(사각형 회전)
        cxp, cyp = x + 30, ytop + 100          # 오른쪽 아래 모서리를 축으로 오른쪽으로 쓰러짐(기준선 아래로 안 내려감)
        ang = math.radians(a)
        corners = [(-24, -100), (0, -100), (0, 0), (-24, 0)]
        poly = [(cxp + px * math.cos(ang) - py * math.sin(ang), cyp + px * math.sin(ang) + py * math.cos(ang)) for px, py in corners]
        on = t > th
        d.polygon(poly, fill=(30, 34, 60) if not on else (60, 52, 30), outline=YEL if on else GRAY)
        d.text((x + 18, ytop + 110), nm, font=F9, fill=WHITE, anchor="ma")
        if on:
            vis, o = slam(t, th, 0.18); d.text((x + 18, ytop + 126 + o), v, font=F9, fill=YEL, anchor="ma")
    Tb = T0 + L * 0.8
    if t > Tb:
        vis, o = slam(t, Tb, 0.2)
        d.rectangle([30, 268 + o, 220, 296 + o], fill=(14, 16, 32), outline=YEL); d.rectangle([30, 268 + o, 36, 296 + o], fill=YEL)
        d.text((CX + 3, 271 + o), "S&P 500 조정 진입", font=F12, fill=WHITE, anchor="ma")
        d.text((CX + 3, 285 + o), "7일 연속 하락 · 고점 대비 -10%↓", font=F9, fill=GRAY, anchor="ma")
    fx = {}
    for th in hits: fx.update(punch(t, th + 0.3, 2))
    return fx

def n_gauge(img, d, t, seg, dur):
    head(d, t, "CNN 공포·탐욕 지수 (장중)", "공포 14", CYAN)
    cx, cy, r = CX, 214, 74
    # 반원 띠(굵은 호 5칸, 방사선 없음)
    cols = [(70, 80, 140), (90, 100, 160), (120, 120, 140), (160, 140, 90), (200, 170, 70)]
    for i, c in enumerate(cols):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180 + i * 36 + 1, 180 + (i + 1) * 36 - 1, fill=c, width=14)
    d.text((cx - r - 2, cy + 6), "공포", font=F9, fill=GRAY); d.text((cx + r - 22, cy + 6), "탐욕", font=F9, fill=GRAY)
    v = lerp(37, 14, ease(prog(t, 0.4, 1.6)))
    a = math.radians(180 + v / 100 * 180)
    d.line([(cx, cy), (cx + math.cos(a) * (r - 18), cy + math.sin(a) * (r - 18))], fill=WHITE, width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=YEL)
    d.text((cx, cy + 14), f"{int(round(v))}", font=F24, fill=YEL, anchor="ma")
    if t > 1.7: d.text((cx, cy + 44), "3월 30일 이후 최저 · 1주 전 37", font=F9, fill=WHT2, anchor="ma")
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 284 + o, 220, 306 + o], fill=(14, 16, 32), outline=CYAN)
        d.text((CX, 290 + o), "조사 ≠ 잘못 · 많은 조사가 제재 없이 끝나요", font=F9, fill=WHITE, anchor="ma")
    return {}

# ================================================================ AVGO scenes
def a_hook(img, d, t, seg, dur): stage(img, d, t, "브로드컴 -12%", "시총 약 257조 원 증발")
def a_mid(img, d, t, seg, dur): stage(img, d, t, "근데 말이죠", "구글·브로드컴 확인 없음", CYAN)
def a_end(img, d, t, seg, dur): stage(img, d, t, "과했을까?", "설문 한 장에 -12%", note="※ 투자 권유 아님 · 11/20 미국 종가 기준")

def a_post(img, d, t, seg, dur):
    head(d, t, "11/20 · X 게시물 한 장", "설문 한 장")
    L = seg_len(seg, dur, 0); T0 = seg[0]
    vis, o = slam(t, 0.3, 0.22)
    if vis:
        y = 104 + o
        d.rectangle([30, y, 220, y + 118], fill=(240, 240, 236), outline=WHITE)
        d.ellipse([38, y + 8, 58, y + 28], fill=(90, 110, 150))
        d.text((64, y + 9), "궈밍치", font=F12, fill=INK); d.text((64, y + 23), "TF인터내셔널 애널리스트", font=F9, fill=(110, 110, 120))
        lines = ["구글, 2027년", "브로드컴 설계 TPU 8i", "약 100만 개 축소", "(약 20%) · 업계 설문"]
        for i, s in enumerate(lines):
            ts = T0 + 0.2 + i * L * 0.16
            if t > ts: d.text((40, y + 44 + i * 16), typed(s, t, ts, 26), font=F12 if i < 3 else F9, fill=INK if i != 2 else (180, 60, 40))
    Ts = T0 + L * 0.8
    if t > Ts: stamp_slam(img, CX, 270, "-12%", YEL, t, Ts, "24", -8)
    return punch(t, Ts, 3)

def a_shift(img, d, t, seg, dur):
    head(d, t, "구글 AI칩(TPU) 설계 파트너", "물량 이동?", CYAN)
    L = dur - TAIL - 0.15 - seg[0]; T0 = seg[0]
    box(d, 30, 116, 116, 230, YEL); box(d, 134, 116, 220, 230, CYAN)
    d.text((73, 120), "브로드컴", font=F12, fill=YEL, anchor="ma"); d.text((73, 134), "TPU 8i", font=F9, fill=GRAY, anchor="ma")
    d.text((177, 120), "미디어텍", font=F12, fill=CYAN, anchor="ma"); d.text((177, 134), "TPU 8t", font=F9, fill=GRAY, anchor="ma")
    u = prog(t, T0 + 0.3, T0 + L * 0.7)
    moved = int(u * 3)
    def mchip(x, y, col):
        d.rectangle([x, y, x + 15, y + 15], fill=dk(col, 0.45), outline=col)
        d.rectangle([x + 5, y + 5, x + 10, y + 10], fill=col)
        for q in (3, 7, 11):
            d.point((x + q, y - 1), fill=GRAY); d.point((x + q, y + 16), fill=GRAY)
    for i in range(9):
        r, c = divmod(i, 3)
        if i >= 9 - moved: continue
        mchip(40 + c * 24, 150 + r * 22, YEL)
    for i in range(moved):
        mchip(144 + i * 24, 150, CYAN)
    if 0 < u < 1:
        fu = (u * 3) % 1; x = lerp(88, 144 + int(u * 3) * 24, fu); y = 194 - math.sin(fu * math.pi) * 34
        mchip(int(x), int(y), WHITE)
    n = int(round(lerp(100, 80, ease(u))))
    d.text((73, 236), f"{n}", font=F24, fill=YEL, anchor="ma")
    if t > T0 + L * 0.75:
        d.text((CX, 270), "계획 100 → 80 (약 100만 개↓)", font=F9, fill=WHT2, anchor="ma")
        d.text((CX, 284), "*궈밍치 업계 설문 · 회사 확인 아님", font=F9, fill=GRAY, anchor="ma")
    return {}

def a_drop(img, d, t, seg, dur):
    head(d, t, "브로드컴 · 11/20 종가", "$304.41")
    box(d, 30, 104, 220, 236, DIM)
    L = seg_len(seg, dur, 0); T0 = seg[0]
    xs = [40, 74, 104, 136, 168, 186, 210]; ys = [124, 130, 152, 146, 168, 176, 222]
    pts = path(xs, ys, 4)
    u = ease(prog(t, 0.3, T0 + L * 0.7))
    line_chart(d, pts, u)
    if t > 0.4: tag(d, 36, 108, "최고가", CYAN)
    Thit = T0 + L * 0.68
    if t > Thit:
        vis, o = slam(t, Thit, 0.2); tag(d, 214, 196 + o, "약 41만 원", YEL, right=True)
        debris(d, 210, 222, t, Thit, 10, (WHITE, YEL, NEU), 40, 0.6, 5, 2)
        d.text((CX, 242), "최고가보다 -36%", font=F12, fill=WHITE, anchor="ma")
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 262 + o, 220, 284 + o], fill=(14, 16, 32), outline=CYAN)
        d.text((CX, 268 + o), "맞춤 AI칩 설계 마벨도 -10%", font=F9, fill=WHITE, anchor="ma")
    return punch(t, Thit, 4)

def a_counter(img, d, t, seg, dur):
    head(d, t, "다른 해석도 있어요", "진짜 악재?", CYAN)
    T0 = seg[0]; T1 = seg[1] if len(seg) > 1 else T0 + 2
    cards = [("배분 조정", "AI 투자를 줄이는 게", "아니라 나누는 것", T0 + 0.1), ("투매의 날", "반도체 30종목이", "모두 내린 날", T1 + 0.05)]
    for k, (ttl, a, b, ta) in enumerate(cards):
        if t < ta: continue
        vis, o = slam(t, ta, 0.2)
        y0 = 108 + k * 92 + (o if k == 0 else -o)
        on = (k == 0 and t < T1) or (k == 1 and t >= T1)
        box(d, 30, y0, 220, y0 + 82, YEL if on else DIM)
        d.text((CX, y0 + 8), ttl, font=F24 if on else F12, fill=YEL if on else WHITE, anchor="ma")
        d.text((CX, y0 + 44), a, font=F9, fill=WHT2, anchor="ma"); d.text((CX, y0 + 58), b, font=F9, fill=WHT2, anchor="ma")
    return {}

def a_cal(img, d, t, seg, dur):
    head(d, t, "답이 나올 날", "12월 9일")
    T0 = seg[0]
    vis, o = slam(t, 0.3, 0.25)
    if vis:
        x0, y0 = 70, 112 + o
        d.rectangle([x0, y0, x0 + 110, y0 + 112], fill=PAPER, outline=WHITE)
        d.rectangle([x0, y0, x0 + 110, y0 + 24], fill=(180, 60, 50))
        d.text((x0 + 55, y0 + 6), "DEC", font=F12, fill=WHITE, anchor="ma")
        for rx in (x0 + 26, x0 + 84): d.rectangle([rx, y0 - 6, rx + 4, y0 + 4], fill=GRAY)
        d.text((x0 + 55, y0 + 40), "9", font=F24, fill=INK, anchor="ma")
        if blink(t, 1.4): d.ellipse([x0 + 34, y0 + 34, x0 + 76, y0 + 76], outline=(200, 60, 50), width=2)
        d.text((x0 + 55, y0 + 88), "브로드컴 실적", font=F9, fill=INK, anchor="ma")
    if t > T0 + 0.8:
        d.text((CX, 246), "2027년 AI 매출 전망이 관건", font=F12, fill=WHITE, anchor="ma")
    return {}

# ================================================================ scripts
SCRIPTS = {
 "nvda": dict(HOST={"n_hook", "n_mid", "n_end"}, SCRIPT=[
    (n_hook, [("엔비디아 하루 {-14%}\n시총 {약 661조 원} 증발", "엔비디아 하루 십사 퍼센트, 시가총액 육백육십일조 원이 사라졌어요.", "h1"),
              ("이유는 {회계 조사}\n보도 한 줄", "이유는, 회계 조사 보도 한 줄이었어요.", "h2")]),
    (n_news, [("로이터 \"SEC가 엔비디아\n{회계 문제} 들여다본다\"", "로이터가, 미국 증권거래위원회가 엔비디아의 회계 문제를 들여다보고 있다고 보도했거든요.", "a1"),
              ("SEC도 엔비디아도\n{아직 답이 없어요}", "증권거래위원회도, 엔비디아도 아직 답하지 않았어요.", "a2")]),
    (n_drop, [("10월 최고 {239달러}에서\n{125달러}, 약 17만 원", "시월 최고 이백삼십구 달러에서, 백이십오 달러, 약 십칠만 원까지 내려왔어요.", "b1"),
              ("고점보다 {47.5%} 낮아요", "고점보다 사십칠 퍼센트 넘게 낮아요.", "b2")]),
    (n_domino, [("반도체지수 {-10.7%} 나스닥 {-5.3%}\nS&P 500은 {조정} 진입", "반도체지수는 십 퍼센트, 나스닥은 오 퍼센트 넘게 빠졌고, 에스앤피 오백은 고점보다 십 퍼센트 넘게 빠진 조정에 들어갔어요.", "c1")]),
    (n_mid, [("근데 말이죠\n조사 = {잘못 확정}은 아니에요", "근데 말이죠. 조사를 받는다고, 잘못이 확정된 건 아니에요.", "t1")]),
    (n_gauge, [("공포·탐욕 지수 {14}\n3월 이후 가장 겁먹은 시장", "공포 탐욕 지수는 십사. 삼월 이후 가장 겁먹은 시장이에요.", "d1"),
               ("많은 조사는\n{제재 없이} 끝나기도 해요", "그리고 많은 조사는, 제재 없이 끝나기도 하죠.", "d2")]),
    (n_end, [("기회일까요, 함정일까요?\n{댓글로 알려주세요!}", "지금은 기회일까요, 함정일까요? 여러분 생각을 댓글로 남겨주세요!", "e1")]),
 ]),
 "avgo": dict(HOST={"a_hook", "a_mid", "a_end"}, SCRIPT=[
    (a_hook, [("브로드컴 하루 {-12%}\n시총 {약 257조 원} 증발", "브로드컴 하루 십이 퍼센트, 시가총액 이백오십칠조 원이 사라졌어요.", "h1"),
              ("시작은 {설문 한 장}이었어요", "시작은, 설문 한 장이었어요.", "h2")]),
    (a_post, [("궈밍치 \"구글, 내년 브로드컴 칩\n{약 100만 개(20%)} 줄였다\"", "궈밍치 애널리스트가, 구글이 내년 브로드컴 설계 인공지능 칩을 백만 개, 이십 퍼센트쯤 줄였다는 업계 설문을 올렸어요.", "a1")]),
    (a_shift, [("대신 {미디어텍} 설계 칩을\n늘린다는 내용", "대신, 미디어텍이 설계한 칩을 늘린다는 내용이었죠.", "a2")]),
    (a_drop, [("브로드컴 {304달러}, 약 41만 원\n최고가보다 {36%} 낮아요", "브로드컴은 삼백사 달러, 약 사십일만 원. 최고가보다 삼십육 퍼센트 낮아졌어요.", "b1"),
              ("맞춤 AI칩 {마벨}도 -10%", "맞춤형 인공지능 칩을 만드는 마벨도, 십 퍼센트 빠졌고요.", "b2")]),
    (a_mid, [("근데 말이죠\n구글도 브로드컴도 {확인 안 했어요}", "근데 말이죠. 구글도 브로드컴도, 아직 확인해 주지 않았어요.", "t1")]),
    (a_counter, [("투자를 줄이는 게 아니라\n{배분을 바꾼 것}이란 해석도", "투자를 줄이는 게 아니라, 배분을 바꾸는 것이란 해석도 있고요.", "c1"),
                 ("그날은 {반도체 전체}가\n무너진 날이기도 해요", "그날은 반도체 전체가 무너진 날이기도 했어요.", "c2")]),
    (a_cal, [("답은 {12월 9일}\n브로드컴 실적 발표에서", "결국 답은, 십이월 구 일 브로드컴 실적 발표에서 나올 것 같아요.", "d1")]),
    (a_end, [("설문 한 장에 -12%, 과했을까요?\n{댓글로 알려주세요!}", "설문 한 장에 십이 퍼센트, 과했을까요? 댓글로 알려주세요!", "e1")]),
 ]),
}
HOST = SCRIPTS[VID]["HOST"]; SCRIPT = SCRIPTS[VID]["SCRIPT"]

def placeholder_narration():
    for _, lines in SCRIPT:
        for _, n, _ in lines:
            p = clip_path(n)
            if not os.path.exists(p):
                syl = len([c for c in n if '가' <= c <= '힣'])
                np.save(p, np.zeros(int(syl / 6.3 * SR), np.float32))

def layout():
    scenes = []
    for k, (fn, lines) in enumerate(SCRIPT):
        t = 0.12 if k == 0 else TR + 0.12
        seg, lens = [], []
        for sub, n, _ in lines:
            L = len(np.load(clip_path(n))) / SR
            seg.append(t); lens.append(L); t += L + GAP
        host = fn.__name__ in HOST
        dur = t - GAP + (TAIL + (0.25 if host else 0.15))
        scenes.append(dict(fn=fn, seg=seg, lens=lens, dur=dur, host=host, subs=[s for s, _, _ in lines], narr=[n for _, n, _ in lines]))
    return scenes, np.cumsum([0] + [s["dur"] for s in scenes]).tolist()

def spec(scenes, starts, total):
    hosts, bubbles, subs = [], [], []
    for k, sc in enumerate(scenes):
        S = starts[k]
        if sc["host"]:
            hosts.append(dict(k=k, t0=S, t1=S + sc["dur"], fade_in=(k > 0)))
            for i, s in enumerate(sc["subs"]):
                t0 = S + sc["seg"][i]; t1 = S + (sc["seg"][i + 1] if i + 1 < len(sc["subs"]) else sc["seg"][i] + sc["lens"][i] + 0.35)
                bubbles.append(dict(t0=t0, t1=t1, text=s, first=(i == 0), last=(i == len(sc["subs"]) - 1)))
        else:
            for i, s in enumerate(sc["subs"]):
                t0 = S + sc["seg"][i]; t1 = S + (sc["seg"][i + 1] - 0.05 if i + 1 < len(sc["subs"]) else min(sc["dur"] - 0.05, sc["seg"][i] + sc["lens"][i] + 0.45))
                subs.append(dict(t0=t0, t1=t1, text=s))
    return dict(total=total, hosts=hosts, bubbles=bubbles, subs=subs)

# ================================================================ audio
def make_audio(path, scenes, starts, total):
    N = int((total + 0.5) * SR)
    sfx = np.zeros(N); nv = np.zeros(N)
    for k, sc in enumerate(scenes):
        for i, n in enumerate(sc["narr"]):
            x = np.load(clip_path(n)).astype(np.float64)
            if np.abs(x).max() > 0:
                x *= 0.11 / (np.sqrt((x ** 2).mean()) + 1e-9)
                if np.abs(x).max() > 0.5: x *= 0.5 / np.abs(x).max()
            st = int((starts[k] + sc["seg"][i]) * SR); nv[st:st + len(x)] += x[:max(0, N - st)]
    S = list(starts)
    bar = 60 / 92 * 4
    quiet = [(S[k], S[k] + sc["dur"]) for k, sc in enumerate(scenes) if sc["host"]]
    try:
        bg = bgm_make("lofi", total + 0.5, level_plan(total + 0.5, bar, quiet))
        bgm = bg.mean(axis=1)[:N] if bg.ndim == 2 else bg[:N]
        bgm = np.pad(bgm, (0, max(0, N - len(bgm)))) * 0.35
    except Exception as e:
        print("bgm_kit 실패, 무음", e); bgm = np.zeros(N)
    ie = int(total * SR); fo = int(1.6 * SR); fi = int(0.2 * SR)
    bgm[:fi] *= np.linspace(0, 1, fi); bgm[ie - fo:ie] *= np.linspace(1, 0, fo); bgm[ie:] = 0
    def swoosh(T): tone(sfx, T, 0.25, 0, 0.05, "noise", decay=0.08); tone(sfx, T, 0.22, 900, 0.03, "sq", 0.5, f1=200)
    def thump(T): tone(sfx, T, 0.3, 120, 0.3, "sin", f1=40, decay=0.12); tone(sfx, T, 0.12, 0, 0.08, "noise", decay=0.04)
    def pop(T): tone(sfx, T, 0.06, 600, 0.04, "sq", 0.5, f1=1300, decay=0.04)
    def bpop(T): tone(sfx, T, 0.07, 500, 0.03, "sin", f1=1100, decay=0.05)
    def stampfx(T): thump(T); tone(sfx, T, 0.18, 0, 0.12, "noise", decay=0.05)
    for k in range(1, len(scenes)): swoosh(S[k] - 0.05)
    for k, sc in enumerate(scenes):
        fn = sc["fn"].__name__; seg = sc["seg"]; dur = sc["dur"]
        if sc["host"]:
            for i in range(len(sc["subs"])): bpop(S[k] + seg[i] - 0.04)
            continue
        L0 = seg_len(seg, dur, 0)
        if fn == "n_news": stampfx(S[k] + seg[0] + L0 * 0.72); pop(S[k] + 0.25)
        if fn == "n_drop":
            thump(S[k] + seg[0] + L0 * 0.72); stampfx(S[k] + (seg[1] + 0.2 if len(seg) > 1 else seg[0] + L0 * 0.72 + 0.5))
        if fn == "n_domino":
            L = dur - TAIL - 0.15 - seg[0]
            for f in (0.0, 0.2, 0.42, 0.62): thump(S[k] + seg[0] + 0.2 + L * f + 0.3)
            pop(S[k] + seg[0] + L * 0.8)
        if fn == "n_gauge" and len(seg) > 1: pop(S[k] + seg[1])
        if fn == "a_post": pop(S[k] + 0.3); stampfx(S[k] + seg[0] + L0 * 0.8)
        if fn == "a_drop": thump(S[k] + seg[0] + L0 * 0.68); [pop(S[k] + seg[1]) for _ in [0] if len(seg) > 1]
        if fn == "a_counter": pop(S[k] + seg[0] + 0.1); [pop(S[k] + seg[1] + 0.05) for _ in [0] if len(seg) > 1]
        if fn == "a_cal": pop(S[k] + 0.3)
    win = int(0.12 * SR); pk = np.maximum.reduceat(np.abs(nv), np.arange(0, N, win))
    env = np.convolve(np.repeat(pk, win)[:N], np.ones(win) / win, mode="same")
    act = np.clip(env / 0.04, 0, 1)
    mix = np.tanh((bgm * (1 - 0.58 * act) * 0.9 + sfx * (1 - 0.35 * act)) * 1.2) / np.tanh(1.2) * 0.55 + nv
    g = 0.89 / max(1e-6, np.abs(mix).max()); mix = mix * g
    for p, a, ch in ((path, mix, 2), (path.replace(".wav", "_narr.wav"), nv * g, 1)):
        pcm = (np.clip(a, -1, 1) * 32767).astype(np.int16)
        with wave.open(p, "wb") as w:
            w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(pcm.tobytes() if ch == 1 else np.repeat(pcm[:, None], 2, axis=1).tobytes())

def render_px(T, scenes, starts, total):
    k = min(max(i for i in range(len(scenes)) if starts[i] <= T + 1e-9), len(scenes) - 1)
    t = T - starts[k]; sc = scenes[k]
    low = render_low(sc, t)
    if k > 0 and t < TR:
        prev = render_low(scenes[k - 1], scenes[k - 1]["dur"] + t)
        mask = shutter_mask(t / TR) if k % 2 else dissolve_mask(k, t / TR)
        low = Image.composite(low, prev, mask)
    a = np.asarray(low.resize((FW, FH), Image.NEAREST)).copy()
    a[3::4] = (a[3::4] * 0.82).astype(np.uint8)
    if T > total - 0.8: a = (a * clamp((total - T) / 0.8)).astype(np.uint8)
    return Image.fromarray(a)

def qtts_job(name):
    items = []
    for take in (1, 2):
        for _, lines in SCRIPT:
            for _, n, lid in lines:
                items.append({"id": f"{lid}_c{take}", "text": n.rstrip(".!?") + ("!" if n.endswith("!") else ("?" if n.endswith("?") else ".")) + " 음.", "gen": {"non_streaming_mode": True}})
    return {"name": name, "mode": "clone", "ref_audio": "out/casual1/E_think.wav", "ref_text": "음… 그럼 데이터센터는 이제 못 짓는 건가?",
            "gen": {"temperature": 0.75, "top_p": 0.9}, "reload_every": 4, "retries": 4, "items": items}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "job":
        json.dump(qtts_job(sys.argv[2]), open(sys.argv[3], "w"), ensure_ascii=False, indent=1); sys.exit()
    placeholder_narration()
    scenes, starts = layout(); total = starts[-1]
    print("scene durations:", [round(s["dur"], 1) for s in scenes], "total:", round(total, 1))
    json.dump(spec(scenes, starts, total), open(f"{OUT}/spec.json", "w"), ensure_ascii=False, indent=1)
    if mode == "times":
        for k, s in enumerate(scenes): print(k, s["fn"].__name__, round(starts[k], 2), [round(starts[k] + x, 2) for x in s["seg"]], round(s["dur"], 2))
        sys.exit()
    if mode == "stills":
        for T in [float(x) for x in sys.argv[2].split(",")]:
            render_px(T, scenes, starts, total).resize((360, 640), Image.LANCZOS).save(f"{OUT}/s_{T:05.1f}.png")
        sys.exit()
    make_audio(f"{OUT}/mix.wav", scenes, starts, total)
    if mode == "audio": sys.exit()
    n = int(total * FPS); os.makedirs(f"{OUT}/px", exist_ok=True)
    for i in range(n):
        render_px(i / FPS, scenes, starts, total).save(f"{OUT}/px/{i:05d}.png", compress_level=1)
        if i % 300 == 0: print(i, "/", n, flush=True)
    print("done", total)
