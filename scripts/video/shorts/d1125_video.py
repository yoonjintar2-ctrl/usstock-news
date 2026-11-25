"""미국주식 늬우스 11/25(수) 1면 두 건 → 8비트 쇼츠 2편 (d1121 엔진 재사용)
VID=semi25 | dell25  python3 d1125_video.py [job NAME PATH|times|stills T,T|audio|full]
사실(출처: 미국주식 늬우스 2026-11-25호, 기준 11/24 미국 종가, 환율 1,341원/달러):
 semi25: 필라델피아 반도체 -7.88%(전날 +14.03%), 나스닥 -1.48% S&P -0.50% 다우 +0.85%
         NVDA -5.86% $155.38(약 21만 원), ADI -17.37%(실적 상회, 1분기 전망·이익률 실망), TXN -11.25%, MU -11.01%(BNP 중립 하향)
         번스타인 NVDA 상향 적정 200달러(약 27만 원, 종가 대비 +29%), SOXX 20일 지지 122.20달러(약 16만 원), 수요일 밤 PCE
 dell25: 3분기 매출 549.4억 달러(약 74조 원, +103%, 예상 506억), AI 수주잔고 1,323억 달러(약 177조 원, 직전 950억)
         연매출 전망 1,920억→2,020억 달러(약 271조 원), 정규장 -11.83% $295.28(약 40만 원), 시간외 +1.79% $300.57
         4분기 AI 서버 매출 전망 3분기보다 약 6% 많은 데 그침, 재고 294억 달러(약 39조 원) 연초의 세 배 가까이
투자 권유 아님. 상승/하락 빨강·초록 구분 없음."""
import os, sys, math, json
VID = os.environ.get("VID", "semi25")
os.environ["VID"] = "nvda"
import d1121_video as V
from d1121_video import (head, tag, stage, path, punch, seg_len, slam, stamp_slam, debris, box, CX, WHT2,
                         YEL, CYAN, WHITE, GRAY, DIM, NEU, GOLD, PAPER, INK, F24, F12, F9, prog, ease, lerp, dk)

BASE = os.path.dirname(os.path.abspath(__file__))
V.OUT = os.path.join(BASE, f"d1125_{VID}/out"); os.makedirs(V.OUT, exist_ok=True)
V.NDIR = os.path.join(BASE, f"d1125_{VID}/narr"); os.makedirs(V.NDIR, exist_ok=True)

def react_cards(d, t, seg, dur, title, big, cards, col=YEL):
    head(d, t, title, big, col)
    T0 = seg[0]; L = dur - 0.65 - T0
    for k, (a, b) in enumerate(cards):
        ta = T0 + 0.1 + k * L * 0.2
        if t < ta: continue
        vis, o = slam(t, ta, 0.18); y0 = 106 + k * 46 + o
        box(d, 30, y0, 220, y0 + 40, col if k % 2 == 0 else CYAN)
        d.text((40, y0 + 5), a, font=F9, fill=GRAY); d.text((40, y0 + 20), b, font=F12, fill=WHITE)
    return {}

def bars(d, t, T0, items, base_y=230, scale=70, x0=60, gap=80, w=44):
    for i, (nm, v, col, lab) in enumerate(items):
        x = x0 + i * gap; h = int(ease(prog(t, T0 + 0.2 + i * 0.45, T0 + 0.9 + i * 0.45)) * v * scale)
        d.rectangle([x, base_y - h, x + w, base_y], fill=dk(col, 0.6), outline=col)
        d.text((x + w // 2, base_y + 6), nm, font=F9, fill=WHITE, anchor="ma")
        if t > T0 + 0.9 + i * 0.45 and lab: d.text((x + w // 2, base_y - h - 16), lab, font=F9, fill=col, anchor="ma")

# ---------------- semi25 ----------------
def s_hook(img, d, t, seg, dur): stage(img, d, t, "반도체 -7.9%", "하루 만에 되밀렸다")
def s_mid(img, d, t, seg, dur): stage(img, d, t, "근데 말이죠", "월가는 다시 '매수'", CYAN)
def s_end(img, d, t, seg, dur): stage(img, d, t, "다시 오를까?", "여러분 생각은?", note="※ 투자 권유 아님 · 11/24 미국 종가 기준")

def s_swing(img, d, t, seg, dur):
    head(d, t, "필라델피아 반도체 지수", "이틀 롤러코스터")
    T0 = seg[0]; L = seg_len(seg, dur, 0)
    xs = [40, 100, 160, 210]; ys = [220, 222, 130, 182]
    pts = path(xs, ys, 2); u = ease(prog(t, T0 + 0.2, T0 + L * 0.7))
    box(d, 30, 104, 220, 252, DIM); V.line_chart(d, pts, u)
    if t > T0 + L * 0.4: tag(d, 120, 112, "11/23 +14.0%", YEL)
    Th = T0 + L * 0.72
    if t > Th:
        vis, o = slam(t, Th, 0.2); tag(d, 214, 196 + o, "11/24 -7.9%", CYAN, right=True)
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 266 + o, 220, 292 + o], fill=(14, 16, 32), outline=WHITE)
        d.text((CX, 273 + o), "나스닥 -1.5% · 다우는 +0.9%", font=F9, fill=WHITE, anchor="ma")
    return punch(t, Th, 3)

NAMES = [("엔비디아", "-5.86%", "155달러 · 약 21만 원"), ("아날로그디바이스", "-17.37%", "실적은 좋았는데 전망 실망"),
         ("텍사스인스트루먼트", "-11.25%", "아날로그 동반 하락"), ("마이크론", "-11.01%", "BNP파리바 '중립' 하향")]
def s_names(img, d, t, seg, dur):
    head(d, t, "11/24 많이 빠진 반도체", "4종목")
    T0 = seg[0]; L = dur - 0.65 - T0
    for k, (a, p, b) in enumerate(NAMES):
        ta = T0 + 0.1 + k * L * 0.18
        if t < ta: continue
        vis, o = slam(t, ta, 0.18); y0 = 106 + k * 46 + o
        box(d, 30, y0, 220, y0 + 40, CYAN if k % 2 else YEL)
        d.text((40, y0 + 5), a, font=F12, fill=WHITE); d.text((212, y0 + 5), p, font=F12, fill=YEL, anchor="ra")
        d.text((40, y0 + 23), b, font=F9, fill=GRAY)
    return {}

def s_react(img, d, t, seg, dur):
    return react_cards(d, t, seg, dur, "급락 날 사람들 반응", "엇갈림", [
        ("스톡트윗 엔비디아 게시판", "그래도 '매우 낙관'"), ("CNBC 스티브 아이스먼", "'큰 총알은 피했다'"),
        ("블룸버그 서베일런스", "'아직 순항은 아니다'"), ("UBS 마크 헤펠레", "'AI 이야기 안 깨졌다'")])

def s_target(img, d, t, seg, dur):
    head(d, t, "번스타인 · 엔비디아 다시 상향", "적정 200달러", CYAN)
    T0 = seg[0]
    bars(d, t, T0, [("11/24 종가", 155.38 / 200, GRAY, "155달러"), ("적정 주가", 1.0, YEL, "200달러 · 약 27만 원")], base_y=236, scale=100, x0=62, gap=82)
    Ts = T0 + 1.6
    if t > Ts: stamp_slam(img, CX, 290, "+29%", YEL, t, Ts, "24", -6)
    return punch(t, Ts, 3)

def s_watch(img, d, t, seg, dur):
    head(d, t, "오늘 밤 볼 것", "2가지", CYAN)
    cards = [("10월 PCE 물가", "밤 10시 반 · GDP 수정치도"), ("반도체 ETF 지지선", "122달러(약 16만 원) 지키나")]
    for k, (a, b) in enumerate(cards):
        ta = seg[0] + 0.1 + k * 0.9
        if t < ta: continue
        vis, o = slam(t, ta, 0.2); y0 = 112 + k * 70 + o
        box(d, 30, y0, 220, y0 + 60, CYAN)
        d.text((CX, y0 + 10), a, font=F12, fill=WHITE, anchor="ma"); d.text((CX, y0 + 34), b, font=F9, fill=WHT2, anchor="ma")
    return {}

# ---------------- dell25 ----------------
def d_hook(img, d, t, seg, dur): stage(img, d, t, "델 AI 주문 177조 원", "수주잔고 사상 최대")
def d_mid(img, d, t, seg, dur): stage(img, d, t, "근데 말이죠", "주가는 -11.8%였어요", CYAN)
def d_end(img, d, t, seg, dur): stage(img, d, t, "AI 서버 붐", "계속될까?", note="※ 투자 권유 아님 · 11/24 미국 종가 기준")

def d_rev(img, d, t, seg, dur):
    head(d, t, "델 3분기 매출", "+103%")
    T0 = seg[0]
    bars(d, t, T0, [("작년 3분기", 1.0, GRAY, ""), ("올해 3분기", 2.03, YEL, "549억 달러")], base_y=236, scale=52, x0=62, gap=82)
    if t > T0 + 1.4: d.text((CX, 256), "약 74조 원 · 두 배 넘게", font=F12, fill=YEL, anchor="ma")
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 280 + o, 220, 306 + o], fill=(14, 16, 32), outline=WHITE)
        d.text((CX, 287 + o), "시장 예상 506억 달러도 넘었어요", font=F9, fill=WHITE, anchor="ma")
    return {}

def d_backlog(img, d, t, seg, dur):
    head(d, t, "쌓여 있는 AI 서버 주문", "수주잔고")
    T0 = seg[0]
    bars(d, t, T0, [("지난 분기", 950 / 1323, GRAY, "950억 달러"), ("이번 분기", 1.0, YEL, "1,323억 달러")], base_y=236, scale=96, x0=62, gap=82)
    Ts = T0 + 1.5
    if t > Ts:
        vis, o = slam(t, Ts, 0.2); d.text((CX, 258 + o), "약 177조 원 · 사상 최대", font=F12, fill=YEL, anchor="ma")
        debris(d, 166, 130, t, Ts, 10, (YEL, WHITE, GOLD), 40, 0.6, 4, 2)
    return punch(t, Ts, 3)

def d_guide(img, d, t, seg, dur):
    head(d, t, "올해 연매출 전망", "또 올렸다")
    T0 = seg[0]; L = seg_len(seg, dur, 0)
    vis, o = slam(t, T0 + 0.1, 0.2)
    box(d, 40, 120, 210, 170, GRAY); d.text((CX, 128), "이전 전망", font=F9, fill=GRAY, anchor="ma"); d.text((CX, 144), "1,920억 달러", font=F12, fill=WHT2, anchor="ma")
    Ts = T0 + L * 0.45
    if t > Ts:
        vis, o = slam(t, Ts, 0.2)
        box(d, 40, 190 + o, 210, 248 + o, YEL); d.text((CX, 198 + o), "새 전망", font=F9, fill=YEL, anchor="ma")
        d.text((CX, 214 + o), "2,020억 달러", font=F24, fill=WHITE, anchor="ma")
        d.text((CX, 256), "약 271조 원", font=F9, fill=WHT2, anchor="ma")
    return punch(t, Ts, 3)

def d_react(img, d, t, seg, dur):
    return react_cards(d, t, seg, dur, "실적에 사람들 반응", "환호", [
        ("스톡트윗 개인 투자자", "'매우 낙관' · 글 160%↑"), ("X 투자 계정", "'3분기를 박살냈다'"),
        ("야후 파이낸스", "'압도적인 분기'"), ("팁랭크스 집계", "긍정 14 · 중립 7")])

def d_price(img, d, t, seg, dur):
    head(d, t, "11/24 델 주가", "정규장 vs 시간외")
    T0 = seg[0]
    box(d, 30, 112, 220, 172, CYAN)
    d.text((CX, 120), "정규장 · HPE 이익률 경고 여파", font=F9, fill=GRAY, anchor="ma"); d.text((CX, 138), "-11.83%  295달러", font=F12, fill=WHITE, anchor="ma")
    Ts = T0 + 1.2
    if t > Ts:
        vis, o = slam(t, Ts, 0.2)
        box(d, 30, 190 + o, 220, 250 + o, YEL)
        d.text((CX, 198 + o), "실적 발표 직후 시간외", font=F9, fill=GRAY, anchor="ma"); d.text((CX, 216 + o), "+1.79%  300달러", font=F12, fill=YEL, anchor="ma")
        d.text((CX, 262), "약 40만 원", font=F9, fill=WHT2, anchor="ma")
    return {}

def d_risk(img, d, t, seg, dur):
    head(d, t, "다만 짚은 점", "숙제 2개", CYAN)
    cards = [("4분기 AI 서버 매출", "3분기보다 약 6%만 더"), ("재고 294억 달러", "약 39조 원 · 연초의 세 배 가까이")]
    for k, (a, b) in enumerate(cards):
        ta = seg[0] + 0.1 + k * 1.0
        if t < ta: continue
        vis, o = slam(t, ta, 0.2); y0 = 112 + k * 70 + o
        box(d, 30, y0, 220, y0 + 60, CYAN)
        d.text((CX, y0 + 10), a, font=F12, fill=WHITE, anchor="ma"); d.text((CX, y0 + 34), b, font=F9, fill=WHT2, anchor="ma")
    return {}

SCRIPTS = {
 "semi25": dict(HOST={"s_hook", "s_mid", "s_end"}, SCRIPT=[
    (s_hook, [("필라델피아 반도체 {-7.9%}\n하루 만에 {되밀렸어요}", "필라델피아 반도체 지수가 하루 만에 칠 점 구 퍼센트 빠졌어요.", "h1"),
              ("전날엔 {+14%}였는데요", "전날엔 십사 퍼센트 올랐는데요.", "h2")]),
    (s_swing, [("월요일 {+14%} 뒤 화요일 {-7.9%}\n오른 몫의 {절반 넘게} 반납", "월요일에 십사 퍼센트 오르고, 화요일에 칠 점 구 퍼센트 빠지면서, 오른 몫의 절반 넘게 돌려줬어요.", "a1"),
               ]),
    (s_names, [("엔비디아 {-5.9%}\n아날로그디바이스 {-17%}", "엔비디아는 오 점 구 퍼센트. 아날로그디바이스는 실적이 좋았는데도, 전망에 실망해 십칠 퍼센트 급락했어요.", "b1"),
               ("텍사스인스트루먼트·마이크론\n둘 다 {-11%}", "텍사스인스트루먼트와 마이크론도 십일 퍼센트씩 빠졌죠.", "b2")]),
    (s_react, [("엔비디아 게시판은 그래도 {매우 낙관}\n'{큰 총알은 피했다}'", "그래도 엔비디아 게시판 분위기는 여전히 매우 낙관이에요. 큰 총알은 피했다는 말도 나왔고요.", "r1")]),
    (s_mid, [("근데 말이죠\n월가는 다시 {'사라'}", "근데 말이죠. 월가에선 다시 사라는 의견이 나왔어요.", "t1")]),
    (s_target, [("번스타인 엔비디아 적정 {200달러}\n종가보다 {29%} 높아요", "번스타인은 엔비디아 적정 주가를 이백 달러, 약 이십칠만 원으로 봤어요. 종가보다 이십구 퍼센트 높죠.", "c1")]),
    (s_watch, [("오늘 밤 {PCE 물가}, 그리고\n반도체 ETF {지지선}", "오늘 밤 피씨이 물가, 그리고 반도체 이티에프가 지지선을 지키는지 보세요.", "d1")]),
    (s_end, [("반도체, 다시 오를까요?\n{댓글로 알려주세요!}", "반도체, 다시 오를까요? 여러분 생각을 댓글로 알려주세요!", "e1")]),
 ]),
 "dell25": dict(HOST={"d_hook", "d_mid", "d_end"}, SCRIPT=[
    (d_hook, [("델 AI 수주잔고 {1,323억 달러}\n약 {177조 원}", "델의 에이아이 수주잔고가 천삼백이십삼억 달러, 약 백칠십칠조 원이에요.", "h1"),
              ("{사상 최대}예요", "사상 최대예요.", "h2")]),
    (d_rev, [("3분기 매출 {549억 달러}, 약 74조 원\n1년 전의 {두 배 넘게}", "삼 분기 매출은 오백사십구억 달러, 약 칠십사조 원. 일 년 전보다 두 배 넘게 늘었어요.", "a1"),
             ("시장 예상 {506억 달러}도\n크게 넘었고요", "시장 예상 오백육억 달러도 크게 넘었고요.", "a2")]),
    (d_backlog, [("수주잔고 {950억} → {1,323억 달러}\n한 분기 만에", "지난 분기 구백오십억 달러였던 수주잔고가, 한 분기 만에 천삼백이십삼억 달러가 됐어요.", "b1")]),
    (d_guide, [("연매출 전망 {2,020억 달러}\n약 {271조 원}으로 상향", "연간 매출 전망도 이천이십억 달러, 약 이백칠십일조 원으로 올렸어요.", "c1")]),
    (d_react, [("개인 투자자 {매우 낙관}\n{'압도적인 분기'}", "반응은 뜨거워요. 개인 투자자는 매우 낙관, 압도적인 분기라는 평가도 나왔죠.", "r1")]),
    (d_mid, [("근데 말이죠\n정규장에선 {-11.8%}", "근데 말이죠. 정규장에선 십일 점 팔 퍼센트 빠졌어요.", "t1")]),
    (d_price, [("{HPE 이익률 경고} 여파\n발표 직후 시간외 {+1.8%}", "에이치피이의 이익률 경고 여파였는데, 실적 발표 직후 시간외에선 일 점 팔 퍼센트 올랐어요.", "d1")]),
    (d_risk, [("다만 {AI 서버 성장 둔화}·\n{재고 세 배} 지적도", "다만 다음 분기 에이아이 서버 성장이 느려지고, 재고가 크게 늘었다는 지적도 있어요.", "d2")]),
    (d_end, [("AI 서버 붐, 계속될까요?\n{댓글로 알려주세요!}", "에이아이 서버 붐, 계속될까요? 댓글로 알려주세요!", "e1")]),
 ]),
}
V.HOST = SCRIPTS[VID]["HOST"]; V.SCRIPT = SCRIPTS[VID]["SCRIPT"]
SCRIPT = V.SCRIPT; HOST = V.HOST; clip_path = V.clip_path; NDIR = V.NDIR; OUT = V.OUT

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "job":
        j = V.qtts_job(sys.argv[2]); j["items"] = [i for i in j["items"] if i["id"].endswith("_c1")]
        json.dump(j, open(sys.argv[3], "w"), ensure_ascii=False, indent=1); sys.exit()
    V.placeholder_narration()
    scenes, starts = V.layout(); total = starts[-1]
    print("scene durations:", [round(s["dur"], 1) for s in scenes], "total:", round(total, 1))
    json.dump(V.spec(scenes, starts, total), open(f"{V.OUT}/spec.json", "w"), ensure_ascii=False, indent=1)
    from PIL import Image
    if mode == "times": sys.exit()
    if mode == "stills":
        for T in [float(x) for x in sys.argv[2].split(",")]:
            V.render_px(T, scenes, starts, total).resize((360, 640), Image.LANCZOS).save(f"{V.OUT}/s_{T:05.1f}.png")
        sys.exit()
    V.make_audio(f"{V.OUT}/mix.wav", scenes, starts, total)
    if mode == "audio": sys.exit()
    n = int(total * V.FPS); os.makedirs(f"{V.OUT}/px", exist_ok=True)
    for i in range(n):
        V.render_px(i / V.FPS, scenes, starts, total).save(f"{V.OUT}/px/{i:05d}.png", compress_level=1)
    print("done", total)
