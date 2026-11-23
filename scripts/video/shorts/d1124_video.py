"""미국주식 늬우스 11/24(화) 1면 두 건 → 8비트 쇼츠 2편 (d1121_video.py 엔진 재사용)
VID=nvda24 | crwd24  python3 d1124_video.py [job NAME PATH|times|stills T,T|audio|full]
사실(출처: 미국주식 늬우스 2026-11-24호, 기준 11/23 미국 종가, 환율 1,342원/달러):
 nvda24: 이사회가 11/12 물러났던 젠슨 황을 사장·CEO·이사로 복귀(8-K), 정부 고위층 의견 듣고 안보 위험 아님 판단
         NVDA +31.48% $165.05(약 22만 원), 2003년 5월 이후 최대 하루 상승, 시총 하루 약 9,540억 달러(약 1,280조 원) 증가
         나스닥 +6.51% S&P +4.73% 다우 +3.01%, 2025년 4월 이후 최고의 하루, S&P 7일 연속 하락 끝
         회사 독립 조사 계속, SEC 회계 건 새 소식 없음, 52주 최고가보다 32% 낮음
 crwd24: 크라우드스트라이크가 지스케일러를 전액 주식 약 439억 달러(약 59조 원)에 인수, ZS 1주=CRWD 1.135주, 웃돈 약 34%
         CRWD -8.92% $208.97(약 28만 원), ZS 오후 3시반 +16.8% $227.45(약 31만 원), 고정 비율이라 몫 약 $237.18
         3분기 순신규 ARR 4.19억 달러(약 5,620억 원) 사상 최대 +58%, 연간 전망 상향
         BTIG 실행 위험, JP모건 성장률·마진 희석, 제프리스 규제 심사
투자 권유 아님. 상승/하락 빨강·초록 구분 없음."""
import os, sys, math, json
VID = os.environ.get("VID", "nvda24")
os.environ["VID"] = "nvda"            # d1121 엔진 기본값 로드용(아래에서 다시 바꿈)
import d1121_video as V
from d1121_video import (head, tag, stage, line_chart, path, punch, seg_len, slam, stamp_slam, debris, box, CX, WHT2,
                         YEL, CYAN, WHITE, GRAY, DIM, NEU, GOLD, PAPER, INK, F24, F12, F9, prog, ease, lerp, typed, blink, dk)

BASE = os.path.dirname(os.path.abspath(__file__))
V.OUT = os.path.join(BASE, f"d1124_{VID}/out"); os.makedirs(V.OUT, exist_ok=True)
V.NDIR = os.path.join(BASE, f"d1124_{VID}/narr"); os.makedirs(V.NDIR, exist_ok=True)

def chair(d, x, y, on):
    d.rectangle([x, y, x + 60, y + 70], fill=(60, 40, 30) if on else (40, 40, 50), outline=GOLD if on else GRAY)
    d.rectangle([x - 6, y + 70, x + 66, y + 84], fill=(70, 50, 36) if on else (50, 50, 60), outline=GOLD if on else GRAY)
    d.line([(x + 30, y + 84), (x + 30, y + 108)], fill=GRAY, width=3); d.line([(x + 10, y + 112), (x + 50, y + 112)], fill=GRAY, width=3)

# ---------------- nvda24 ----------------
def n_hook(img, d, t, seg, dur): stage(img, d, t, "엔비디아 +31%", "시총 약 1,280조 원 늘었다")
def n_mid(img, d, t, seg, dur): stage(img, d, t, "근데 말이죠", "의혹은 아직 그대로", CYAN)
def n_end(img, d, t, seg, dur): stage(img, d, t, "진짜 바닥?", "여러분 생각은?", note="※ 투자 권유 아님 · 11/23 미국 종가 기준")

def n_return(img, d, t, seg, dur):
    head(d, t, "11/23 엔비디아 이사회 발표", "CEO 복귀")
    T1 = seg[0] + seg_len(seg, dur, 0) * 0.55
    on = t > T1
    chair(d, 95, 120, on)
    vis, o = slam(t, 0.3, 0.2)
    if vis:
        d.rectangle([60, 236 + o, 190, 258 + o], fill=PAPER if on else (90, 90, 100), outline=WHITE)
        d.text((CX, 240 + o), "CEO  젠슨 황" if on else "CEO  (공석)", font=F12, fill=INK if on else WHT2, anchor="ma")
    if on:
        debris(d, CX, 150, t, T1, 12, (YEL, WHITE, GOLD), 70, 0.8, 3, 2)
        tag(d, 36, 104, "11/12 사임 → 11/23 복귀", YEL)
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 274 + o, 220, 298 + o], fill=(14, 16, 32), outline=CYAN)
        d.text((CX, 281 + o), "정부 의견 청취 · 안보 위험 아님 판단", font=F9, fill=WHITE, anchor="ma")
    return punch(t, T1, 3)

def n_jump(img, d, t, seg, dur):
    head(d, t, "11/20 → 11/23 종가", "+31.48%")
    box(d, 30, 104, 220, 252, DIM)
    L = seg_len(seg, dur, 0); T0 = seg[0]
    xs = [40, 80, 120, 160, 200]; ys = [150, 190, 214, 222, 128]
    pts = path(xs, ys, 2)
    u = ease(prog(t, 0.3, T0 + L * 0.6)); line_chart(d, pts, u)
    if t > 0.5: tag(d, 120, 226, "$125.5", NEU)
    Thit = T0 + L * 0.58
    if t > Thit:
        vis, o = slam(t, Thit, 0.2); tag(d, 214, 108 + o, "$165 약 22만 원", YEL, right=True)
        debris(d, 200, 128, t, Thit, 12, (WHITE, YEL, GOLD), 50, 0.7, 7, 2)
    if len(seg) > 1 and t > seg[1]:
        d.text((CX, 262), "2003년 5월 이후 가장 큰 하루 상승", font=F9, fill=WHT2, anchor="ma")
    Ts = (seg[1] + 0.3) if len(seg) > 1 else Thit + 0.6
    if t > Ts: stamp_slam(img, CX, 300, "+31%", YEL, t, Ts, "24", -6)
    return punch(t, Thit, 4)

IDX = [("나스닥", 6.51), ("S&P 500", 4.73), ("다우", 3.01)]
def n_index(img, d, t, seg, dur):
    head(d, t, "11/23(월) 뉴욕 증시", "최고의 하루")
    T0 = seg[0]; L = dur - 0.65 - T0
    for i, (nm, v) in enumerate(IDX):
        y = 116 + i * 46; ts = T0 + 0.2 + i * L * 0.18
        d.text((34, y + 4), nm, font=F12, fill=WHITE)
        w = int(ease(prog(t, ts, ts + 0.7)) * v / 6.51 * 100)
        d.rectangle([104, y + 2, 104 + max(w, 1), y + 20], fill=dk(YEL, 0.6), outline=YEL)
        if t > ts + 0.6: d.text((104 + w + 4, y + 5), f"+{v:.2f}%", font=F9, fill=YEL)
    Tb = T0 + L * 0.7
    if t > Tb:
        vis, o = slam(t, Tb, 0.2)
        d.rectangle([30, 262 + o, 220, 288 + o], fill=(14, 16, 32), outline=YEL); d.rectangle([30, 262 + o, 36, 288 + o], fill=YEL)
        d.text((CX + 3, 264 + o), "2025년 4월 이후 최고", font=F12, fill=WHITE, anchor="ma")
        d.text((CX + 3, 278 + o), "S&P 7일 연속 하락 끝", font=F9, fill=GRAY, anchor="ma")
    return {}

def n_risk(img, d, t, seg, dur):
    head(d, t, "아직 남은 숙제", "의혹 2개", CYAN)
    cards = [("독립 조사 계속", "외국 정보기관 표적 의혹", seg[0] + 0.1), ("SEC 회계 건", "새 소식 확인 안 됨", seg[0] + 0.9)]
    for k, (a, b, ta) in enumerate(cards):
        if t < ta: continue
        vis, o = slam(t, ta, 0.2); y0 = 108 + k * 70 + o
        box(d, 30, y0, 220, y0 + 60, CYAN)
        d.text((CX, y0 + 10), a, font=F12, fill=WHITE, anchor="ma"); d.text((CX, y0 + 34), b, font=F9, fill=WHT2, anchor="ma")
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.text((CX, 262 + o), "최고가보다 아직 -32%", font=F12, fill=YEL, anchor="ma")
    return {}

# ---------------- crwd24 ----------------
def c_hook(img, d, t, seg, dur): stage(img, d, t, "크라우드 -8.9%", "59조 원 인수 발표한 날")
def c_mid(img, d, t, seg, dur): stage(img, d, t, "근데 말이죠", "실적은 사상 최대", CYAN)
def c_end(img, d, t, seg, dur): stage(img, d, t, "보안 공룡 탄생", "여러분 생각은?", note="※ 투자 권유 아님 · 11/23 미국 종가 기준")

def c_deal(img, d, t, seg, dur):
    head(d, t, "11/23 인수 발표 · 전액 주식", "약 59조 원")
    T0 = seg[0]; L = seg_len(seg, dur, 0)
    u = ease(prog(t, T0 + 0.2, T0 + L * 0.6))
    xa = lerp(30, 60, u); xb = lerp(156, 126, u)
    box(d, int(xa), 120, int(xa) + 64, 190, YEL); d.text((xa + 32, 146), "CRWD", font=F12, fill=YEL, anchor="ma")
    box(d, int(xb), 120, int(xb) + 64, 190, CYAN); d.text((xb + 32, 146), "ZS", font=F12, fill=CYAN, anchor="ma")
    if u >= 1:
        debris(d, CX, 155, t, T0 + L * 0.6, 10, (YEL, CYAN, WHITE), 50, 0.6, 4, 2)
        d.text((CX, 198), "약 439억 달러", font=F12, fill=WHITE, anchor="ma")
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 232 + o, 220, 262 + o], fill=(14, 16, 32), outline=WHITE)
        d.text((CX, 236 + o), "ZS 1주 = CRWD 1.135주", font=F12, fill=YEL, anchor="ma")
        d.text((CX, 250 + o), "발표 기준 웃돈 약 34%", font=F9, fill=GRAY, anchor="ma")
    return {}

def c_seesaw(img, d, t, seg, dur):
    head(d, t, "11/23 주가", "엇갈린 하루")
    T0 = seg[0]; L = seg_len(seg, dur, 0)
    a = ease(prog(t, T0 + 0.3, T0 + L * 0.5)) * 14
    cx, cy = CX, 210; r = 66; ang = math.radians(a)
    x1, y1 = cx - r * math.cos(ang), cy + r * math.sin(ang); x2, y2 = cx + r * math.cos(ang), cy - r * math.sin(ang)
    d.polygon([(cx - 10, cy + 22), (cx + 10, cy + 22), (cx, cy + 2)], fill=GRAY)
    d.line([(x1, y1), (x2, y2)], fill=WHITE, width=4)
    d.rectangle([x1 - 22, y1 - 34, x1 + 22, y1 - 4], fill=dk(YEL, 0.5), outline=YEL); d.text((x1, y1 - 26), "CRWD", font=F9, fill=YEL, anchor="ma")
    d.rectangle([x2 - 22, y2 - 34, x2 + 22, y2 - 4], fill=dk(CYAN, 0.5), outline=CYAN); d.text((x2, y2 - 26), "ZS", font=F9, fill=CYAN, anchor="ma")
    if t > T0 + L * 0.5:
        d.text((x1, y1 + 8), "-8.9%", font=F12, fill=YEL, anchor="ma"); d.text((x1, y1 + 24), "약 28만 원", font=F9, fill=GRAY, anchor="ma")
        d.text((x2, y2 + 8), "+16.8%", font=F12, fill=CYAN, anchor="ma"); d.text((x2, y2 + 24), "약 31만 원", font=F9, fill=GRAY, anchor="ma")
    if len(seg) > 1 and t > seg[1]:
        vis, o = slam(t, seg[1], 0.2)
        d.rectangle([30, 276 + o, 220, 300 + o], fill=(14, 16, 32), outline=WHITE)
        d.text((CX, 283 + o), "비율 고정 → 받는 몫 약 237달러", font=F9, fill=WHITE, anchor="ma")
    return {}

def c_record(img, d, t, seg, dur):
    head(d, t, "3분기 순신규 연간반복매출", "+58%")
    T0 = seg[0]; L = dur - 0.65 - T0
    vals = [("작년", 1.0), ("올해", 1.58)]
    for i, (nm, v) in enumerate(vals):
        x = 70 + i * 80; h = int(ease(prog(t, T0 + 0.2 + i * 0.4, T0 + 0.9 + i * 0.4)) * v * 70)
        d.rectangle([x, 230 - h, x + 44, 230], fill=dk(YEL if i else GRAY, 0.6), outline=YEL if i else GRAY)
        d.text((x + 22, 236), nm, font=F9, fill=WHITE, anchor="ma")
    if t > T0 + 1.4:
        tag(d, 40, 104, "약 5,620억 원 · 사상 최대", YEL)
    if t > T0 + L * 0.6:
        d.text((CX, 262), "연간 전망도 올렸어요", font=F12, fill=WHITE, anchor="ma")
    return {}

def c_risk(img, d, t, seg, dur):
    head(d, t, "증권사들이 짚은 것", "숙제 3개", CYAN)
    items = [("BTIG", "두 회사 합치는 실행 위험"), ("JP모건", "성장률·현금흐름 희석"), ("제프리스", "규제 심사 가능성")]
    T0 = seg[0]; L = dur - 0.65 - T0
    for k, (a, b) in enumerate(items):
        ta = T0 + 0.1 + k * L * 0.25
        if t < ta: continue
        vis, o = slam(t, ta, 0.18); y0 = 108 + k * 52 + o
        box(d, 30, y0, 220, y0 + 44, CYAN)
        d.text((40, y0 + 6), a, font=F12, fill=YEL); d.text((40, y0 + 26), b, font=F9, fill=WHT2)
    return {}

SCRIPTS = {
 "nvda24": dict(HOST={"n_hook", "n_mid", "n_end"}, SCRIPT=[
    (n_hook, [("엔비디아 하루 {+31%}\n시총 {약 1,280조 원} 늘었어요", "엔비디아가 하루에 삼십일 퍼센트 올랐어요. 시가총액이 천이백팔십조 원 늘었죠.", "h1"),
              ("{젠슨 황}이 돌아왔거든요", "젠슨 황이 돌아왔거든요.", "h2")]),
    (n_return, [("11/12 물러났던 젠슨 황\n이사회가 {곧바로 복귀}시켰어요", "십일월 십이일 물러났던 젠슨 황을, 이사회가 사장과 씨이오로 곧바로 복귀시켰어요.", "a1"),
                ("정부 의견을 듣고\n{안보 위험 아님} 판단", "미국 정부 고위층 의견을 듣고, 국가안보 위험이 아니라고 판단했대요.", "a2")]),
    (n_jump, [("{125달러}에서 {165달러}\n약 22만 원으로", "백이십오 달러에서 백육십오 달러, 약 이십이만 원이 됐어요.", "b1"),
              ("2003년 이후\n{가장 큰 하루 상승}", "이천삼년 이후 가장 큰 하루 상승이에요.", "b2")]),
    (n_index, [("나스닥 {+6.5%} S&P 500 {+4.7%}\n2025년 4월 이후 {최고의 하루}", "나스닥은 육 점 오 퍼센트, 에스앤피 오백은 사 점 칠 퍼센트. 이천이십오년 사월 이후 가장 좋은 하루였어요.", "c1")]),
    (n_mid, [("근데 말이죠\n{의혹}은 아직 그대로예요", "근데 말이죠. 의혹은 아직 그대로예요.", "t1")]),
    (n_risk, [("회사 {독립 조사}는 계속\n회계 건도 {새 소식 없음}", "회사의 독립 조사는 계속되고, 회계 조사 건도 새 소식이 없어요.", "d1"),
              ("주가는 아직\n최고가보다 {32%} 낮아요", "주가는 아직 최고가보다 삼십이 퍼센트 낮고요.", "d2")]),
    (n_end, [("이번엔 진짜 바닥일까요?\n{댓글로 알려주세요!}", "이번엔 진짜 바닥일까요? 여러분 생각을 댓글로 알려주세요!", "e1")]),
 ]),
 "crwd24": dict(HOST={"c_hook", "c_mid", "c_end"}, SCRIPT=[
    (c_hook, [("크라우드스트라이크 {-8.9%}\n{59조 원} 인수 발표한 날", "크라우드스트라이크가 오십구조 원짜리 인수를 발표한 날, 주가는 팔 점 구 퍼센트 빠졌어요.", "h1"),
              ("사는 쪽은 {내리고}\n팔리는 쪽은 {올랐죠}", "사는 쪽은 내리고, 팔리는 쪽은 올랐죠.", "h2")]),
    (c_deal, [("지스케일러를 {약 59조 원}에\n전부 {주식}으로 사요", "지스케일러를 사백삼십구억 달러, 약 오십구조 원에 전부 주식으로 사요.", "a1"),
              ("지스케일러 1주 =\n크라우드 {1.135주}", "지스케일러 한 주에, 크라우드스트라이크 일 점 일삼오 주를 주는 조건이에요.", "a2")]),
    (c_seesaw, [("크라우드 {209달러}, 약 28만 원\n지스케일러는 {+16.8%}", "크라우드스트라이크는 이백구 달러, 약 이십팔만 원. 지스케일러는 십육 점 팔 퍼센트 올랐어요.", "b1"),
                ("비율이 고정이라\n크라우드가 내리면 {몫도 줄어요}", "비율이 고정이라, 크라우드스트라이크가 내리면 받는 몫도 줄어요.", "b2")]),
    (c_mid, [("근데 말이죠\n같은 날 실적은 {사상 최대}", "근데 말이죠. 같은 날 발표한 실적은 사상 최대였어요.", "t1")]),
    (c_record, [("새 연간반복매출 {약 5,620억 원}\n{+58%}, 전망도 올렸어요", "새로 늘어난 연간반복매출이 약 오천육백이십억 원, 오십팔 퍼센트 늘었고, 연간 전망도 올렸어요.", "c1")]),
    (c_risk, [("다만 {합치는 실행 위험}과\n{규제 심사}가 남았어요", "다만 두 회사를 합치는 실행 위험과, 규제 심사가 남아 있어요.", "d1")]),
    (c_end, [("보안 공룡의 탄생, 어떻게 보세요?\n{댓글로 알려주세요!}", "보안 공룡의 탄생, 여러분은 어떻게 보세요? 댓글로 알려주세요!", "e1")]),
 ]),
}
V.HOST = SCRIPTS[VID]["HOST"]; V.SCRIPT = SCRIPTS[VID]["SCRIPT"]

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
