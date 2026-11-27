"""8비트 1면 쇼츠 범용 엔진 (2026-11-26) — 매일 파이썬 장면 코드를 새로 짜지 않는다.
대본은 JSON 하나(usstock-news 저장소 video/D-top.json, 발행 작업이 신문과 함께 써 둔다).

  python3 top8.py <spec.json> job NAME PATH   # 맥 qtts 작업 파일(c1 테이크만; 피치 튄 줄은 _c2 로 다시)
  python3 top8.py <spec.json> times           # 장면 길이·총 길이(60초 이하 확인)
  python3 top8.py <spec.json> stills 1,8,20   # 검수용 정지 컷(out/s_*.png)
  python3 top8.py <spec.json> audio | full    # 오디오 / 전체 프레임
  python3 top8.py <spec.json> thumb OUT.jpg   # 썸네일(스타일은 spec.thumb.style, 없으면 날짜로 돌아가며)

scene type: stage(마스코트 전체 화면, host true) · line(값 흐름 선) · names(종목 줄) · react(사람들 반응 카드)
            bars(막대 비교) · compare(이전→이후 두 상자) · cards(볼 것/짚을 점 카드)
줄(lines): [자막({강조}), 내레이션(읽는 대로 한글)] — 자막과 내레이션 뜻이 같게, 첫 장면 첫 줄에 종목+숫자.
색으로 상승·하락을 나누지 않는다(노랑/하늘은 강조용일 뿐). 투자 권유 문구 금지."""
import os, sys, json, datetime
# narr_prep.py 처럼 모듈로 불러올 땐 환경변수 TOP8_SPEC 로 대본 경로를 준다
if os.environ.get("TOP8_SPEC"): SPEC_PATH = os.environ["TOP8_SPEC"]; ARGS = (sys.argv[2:] if len(sys.argv) > 1 and sys.argv[1].endswith(".json") else sys.argv[1:]) if __name__ == "__main__" else []
else: SPEC_PATH = sys.argv[1]; ARGS = sys.argv[2:]; os.environ["TOP8_SPEC"] = os.path.abspath(SPEC_PATH)
SP = json.load(open(SPEC_PATH, encoding="utf-8"))
# 11/28: 픽셀 폰트에 한자가 없어 네모(⊠)로 나옴 → 자주 쓰는 한 글자 약칭은 한글로, 나머지 한자는 지움
_HJ = {"中": "중국", "美": "미국", "日": "일본", "韓": "한국", "英": "영국", "獨": "독일", "佛": "프랑스", "台": "대만", "對": "대"}
def _dehan(o):
    import re
    if isinstance(o, str): return re.sub(r"[\u4e00-\u9fff]", "", "".join(_HJ.get(c, c) for c in o))
    if isinstance(o, list): return [_dehan(x) for x in o]
    if isinstance(o, dict): return {k: _dehan(v) for k, v in o.items()}
    return o
SP = _dehan(SP)
VIDNAME = SP.get("vid") or ("top" + SP["date"][5:7] + SP["date"][8:10])
os.environ["VID"] = "nvda"                      # 엔진 모듈 로드용(곧 덮어씀)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 배경 규칙(발행인 11/26, 11/27 재지적): 모눈·격자 무늬 금지 → 단색에 아주 살짝 세로 그라데이션만.
# 엔진 모듈들이 make_video.bg_img 를 import 하기 전에 바꿔 끼운다(이후 모든 장면 배경에 적용).
import make_video as _MV
from functools import lru_cache as _lru
from PIL import Image as _Im
@_lru(None)
def _grad_bg(kind="grid", top=(28, 26, 46), bot=(16, 14, 26)):
    im = _Im.new("RGB", (_MV.W, _MV.H)); px = im.load()
    for y in range(_MV.H):
        u = y / max(1, _MV.H - 1); c = tuple(int(top[i] + (bot[i] - top[i]) * u) for i in range(3))
        for x in range(_MV.W): px[x, y] = c
    return im
_MV.bg_img = _grad_bg
import d1121_video as V
from d1121_video import (head, tag, stage, path, punch, seg_len, slam, stamp_slam, debris, box, CX, WHT2,
                         YEL, CYAN, WHITE, GRAY, DIM, NEU, GOLD, F24, F12, F9, prog, ease, dk)

BASE = os.path.dirname(os.path.abspath(__file__))
V.OUT = os.path.join(BASE, f"top_{VIDNAME}/out"); os.makedirs(V.OUT, exist_ok=True)
V.NDIR = os.path.join(BASE, f"top_{VIDNAME}/narr"); os.makedirs(V.NDIR, exist_ok=True)
COL = {"yel": YEL, "cyan": CYAN, None: YEL}
def C(s, default="yel"): return COL.get(s or default, YEL)

# ---------------------------------------------------------------- 장면 그리기
def g_stage(S):
    def f(img, d, t, seg, dur):
        stage(img, d, t, S["big"], S.get("small", ""), C(S.get("col")), note=S.get("note"))
    return f

def g_line(S):
    ys = [float(v) for v in S["ys"]]; lo, hi = min(ys), max(ys); rng = (hi - lo) or 1
    n = len(ys); xs = [40 + int(i * 170 / max(1, n - 1)) for i in range(n)]
    py = [232 - int((v - lo) / rng * 100) for v in ys]
    def f(img, d, t, seg, dur):
        head(d, t, S.get("small", ""), S["big"], C(S.get("col")))
        T0 = seg[0]; L = seg_len(seg, dur, 0)
        pts = path(xs, py, 2); u = ease(prog(t, T0 + 0.2, T0 + L * 0.7))
        box(d, 30, 104, 220, 252, DIM); V.line_chart(d, pts, u)
        for j, (i, txt) in enumerate(S.get("labels", [])):
            i = int(i) if int(i) >= 0 else n + int(i)
            Ti = T0 + L * (0.25 + 0.5 * i / max(1, n - 1))
            if t > Ti:
                vis, o = slam(t, Ti, 0.2); right = xs[i] > 150
                yy = max(108, min(236, py[i] - 18 if j % 2 == 0 else py[i] + 6))
                tag(d, xs[i] + (4 if right else -4) * 0, yy + o, txt, YEL if j % 2 == 0 else CYAN, right=right)
        if S.get("foot") and len(seg) > 1 and t > seg[1]:
            vis, o = slam(t, seg[1], 0.2)
            d.rectangle([30, 266 + o, 220, 292 + o], fill=(14, 16, 32), outline=WHITE)
            d.text((CX, 273 + o), S["foot"], font=F9, fill=WHITE, anchor="ma")
        return punch(t, T0 + L * 0.72, 3)
    return f

def g_names(S):
    rows = S["rows"][:4]
    def f(img, d, t, seg, dur):
        head(d, t, S.get("small", ""), S["big"], C(S.get("col")))
        T0 = seg[0]; L = dur - 0.65 - T0
        for k, r in enumerate(rows):
            a, p = r[0], r[1]; b = r[2] if len(r) > 2 else ""
            ta = T0 + 0.1 + k * L * 0.18
            if t < ta: continue
            vis, o = slam(t, ta, 0.18); y0 = 106 + k * 46 + o
            box(d, 30, y0, 220, y0 + 40, CYAN if k % 2 else YEL)
            d.text((40, y0 + 5), a, font=F12, fill=WHITE); d.text((212, y0 + 5), p, font=F12, fill=YEL, anchor="ra")
            d.text((40, y0 + 23), b, font=F9, fill=GRAY)
        return {}
    return f

def g_react(S):
    cards = S["cards"][:4]
    def f(img, d, t, seg, dur):
        head(d, t, S.get("small", "사람들 반응"), S["big"], C(S.get("col")))
        T0 = seg[0]; L = dur - 0.65 - T0
        for k, (a, b) in enumerate(cards):
            ta = T0 + 0.1 + k * L * 0.2
            if t < ta: continue
            vis, o = slam(t, ta, 0.18); y0 = 106 + k * 46 + o
            box(d, 30, y0, 220, y0 + 40, YEL if k % 2 == 0 else CYAN)
            d.text((40, y0 + 5), a, font=F9, fill=GRAY); d.text((40, y0 + 20), b, font=F12, fill=WHITE)
        return {}
    return f

def g_bars(S):
    items = S["items"][:3]; mx = max(float(i[1]) for i in items) or 1
    gap = 82 if len(items) == 2 else 62; x0 = 62 if len(items) == 2 else 44
    def f(img, d, t, seg, dur):
        head(d, t, S.get("small", ""), S["big"], C(S.get("col")))
        T0 = seg[0]
        for i, it in enumerate(items):
            nm, v = it[0], float(it[1]) / mx; lab = it[2] if len(it) > 2 else ""
            col = GRAY if i < len(items) - 1 else YEL
            x = x0 + i * gap; w = 44; h = int(ease(prog(t, T0 + 0.2 + i * 0.45, T0 + 0.9 + i * 0.45)) * v * 100)
            d.rectangle([x, 236 - h, x + w, 236], fill=dk(col, 0.6), outline=col)
            d.text((x + w // 2, 242), nm, font=F9, fill=WHITE, anchor="ma")
            if t > T0 + 0.9 + i * 0.45 and lab: d.text((x + w // 2, 236 - h - 16), lab, font=F9, fill=col, anchor="ma")
        Ts = T0 + 0.9 + len(items) * 0.45
        if S.get("note") and t > Ts: d.text((CX, 262), S["note"], font=F12, fill=YEL, anchor="ma")
        if S.get("stamp") and t > Ts + 0.3: stamp_slam(img, CX, 292, S["stamp"], YEL, t, Ts + 0.3, "24", -6)
        if S.get("foot") and len(seg) > 1 and t > seg[1]:
            vis, o = slam(t, seg[1], 0.2)
            d.rectangle([30, 280 + o, 220, 306 + o], fill=(14, 16, 32), outline=WHITE)
            d.text((CX, 287 + o), S["foot"], font=F9, fill=WHITE, anchor="ma")
        return punch(t, Ts, 3)
    return f

def g_compare(S):
    a, b = S["a"], S["b"]
    def f(img, d, t, seg, dur):
        head(d, t, S.get("small", ""), S["big"], C(S.get("col")))
        T0 = seg[0]; L = seg_len(seg, dur, 0)
        box(d, 40, 120, 210, 170, GRAY)
        d.text((CX, 128), a[0], font=F9, fill=GRAY, anchor="ma"); d.text((CX, 144), a[1], font=F12, fill=WHT2, anchor="ma")
        Ts = T0 + L * 0.45
        if t > Ts:
            vis, o = slam(t, Ts, 0.2)
            box(d, 40, 190 + o, 210, 248 + o, YEL); d.text((CX, 198 + o), b[0], font=F9, fill=YEL, anchor="ma")
            fb = F24 if d.textlength(b[1], font=F24) < 160 else F12
            d.text((CX, 214 + o), b[1], font=fb, fill=WHITE, anchor="ma")
            if len(b) > 2: d.text((CX, 256), b[2], font=F9, fill=WHT2, anchor="ma")
        return punch(t, Ts, 3)
    return f

def g_cards(S):
    cards = S["cards"][:3]; step = 70 if len(cards) <= 2 else 52; hh = 60 if len(cards) <= 2 else 46
    def f(img, d, t, seg, dur):
        head(d, t, S.get("small", ""), S["big"], C(S.get("col"), "cyan"))
        for k, (a, b) in enumerate(cards):
            ta = seg[0] + 0.1 + k * 0.9
            if t < ta: continue
            vis, o = slam(t, ta, 0.2); y0 = 112 + k * step + o
            box(d, 30, y0, 220, y0 + hh, CYAN if k % 2 == 0 else YEL)
            d.text((CX, y0 + 8), a, font=F12, fill=WHITE, anchor="ma"); d.text((CX, y0 + hh - 24), b, font=F9, fill=WHT2, anchor="ma")
        return {}
    return f

# 매일 시리즈 배지(11/26 발행인: 날짜 + '매일' 뉘앙스로 구독 유도) — 모든 장면 아래쪽 안전 영역에 고정
_d = datetime.date.fromisoformat(SP["date"]); _wd = "월화수목금토일"[_d.weekday()]
BADGE = SP.get("badge") or f"{_d.month}.{_d.day}({_wd}) · 매일 아침 미장 이슈" + (f" {SP['no']}" if SP.get("no") else "")
def with_badge(fn):
    def g(img, d, t, seg, dur):
        r = fn(img, d, t, seg, dur)
        w = int(d.textlength(BADGE, font=F12)) + 14; x0 = CX - w // 2
        # 위치: 화면 위쪽(자막 1296px 줄과 겹치지 않게). 마스코트 전체 화면 장면(stage)은 제목 자리라 넣지 않는다
        d.rectangle([x0, 30, x0 + w, 48], fill=(10, 14, 30), outline=YEL); d.text((CX, 32), BADGE, font=F9 if w > 200 else F12, fill=YEL, anchor="ma")
        return r
    return g

MAKERS = dict(stage=g_stage, line=g_line, names=g_names, react=g_react, bars=g_bars, compare=g_compare, cards=g_cards)
SCRIPT, HOST = [], set()
for k, S in enumerate(SP["scenes"]):
    fn = MAKERS[S["type"]](S) if S["type"] == "stage" else with_badge(MAKERS[S["type"]](S)); fn.__name__ = f"g{k:02d}_{S['type']}"
    if S["type"] == "stage": HOST.add(fn.__name__)
    SCRIPT.append((fn, [(ln[0], ln[1], f"s{k:02d}_{i}") for i, ln in enumerate(S["lines"])]))
V.SCRIPT, V.HOST = SCRIPT, HOST
clip_path = V.clip_path; NDIR = V.NDIR; OUT = V.OUT          # narr_prep.py 가 쓰는 이름

# ---------------------------------------------------------------- 썸네일 (매일 다른 틀)
def thumb(out):
    from PIL import Image, ImageDraw
    from d1121_thumbs import F, BLK, BLD, W, H, mascot, ctext
    T = SP.get("thumb", {})
    styles = ["split", "receipt", "extra", "card"]
    st = T.get("style") or styles[datetime.date.fromisoformat(SP["date"]).toordinal() % 4]
    date = T.get("date", ""); big = T.get("big", ""); small = T.get("small", ""); top = T.get("top", ""); bot = T.get("bottom", "")
    def fit(d, s, path, size, maxw=W - 140):
        while size > 40 and d.textlength(s, font=F(path, size)) > maxw: size -= 6
        return F(path, size)
    if st == "split":
        im = Image.new("RGB", (W, H), (14, 18, 30)); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, H // 2], fill=(240, 200, 40))
        ctext(d, 170, date, fit(d, date, BLK, 84), (20, 20, 20))
        ctext(d, 400, top, fit(d, top, BLK, 260), (20, 20, 20))
        ctext(d, 1010, big or bot, fit(d, big or bot, BLK, 260), (120, 200, 255))   # 11/28: big 이 빠지고 마스코트가 숫자를 가리던 문제
        if big and bot: ctext(d, 1400, bot, fit(d, bot, BLK, 84), (255, 255, 255))
        ctext(d, 1540, small, fit(d, small, BLD, 64, W - 600), (200, 205, 215))
        m = mascot(260); im.paste(m, (W - m.width - 50, H - m.height - 90), m)
    elif st == "receipt":
        im = Image.new("RGB", (W, H), (40, 44, 52)); d = ImageDraw.Draw(im)
        d.rectangle([110, 160, W - 110, 1560], fill=(250, 248, 240))
        for x in range(110, W - 110, 40): d.polygon([(x, 1560), (x + 20, 1590), (x + 40, 1560)], fill=(250, 248, 240))
        ctext(d, 220, date, fit(d, date, BLK, 80, W - 300), (30, 30, 30))
        for y in (340, 900):
            for x in range(160, W - 160, 30): d.line([(x, y), (x + 15, y)], fill=(150, 150, 150), width=4)
        ctext(d, 420, top, fit(d, top, BLK, 110, W - 300), (30, 30, 30))
        ctext(d, 600, big, fit(d, big, BLK, 180, W - 300), (210, 60, 40))
        ctext(d, 980, small, fit(d, small, BLK, 76, W - 300), (30, 30, 30))
        ctext(d, 1110, bot, fit(d, bot, BLD, 60, W - 300), (90, 90, 90))
        m = mascot(330); im.paste(m, (W - m.width - 150, 1230), m)
    elif st == "extra":
        im = Image.new("RGB", (W, H), (238, 233, 220)); d = ImageDraw.Draw(im)
        d.rectangle([60, 250, W - 60, 262], fill=(20, 20, 20))
        ctext(d, 272, "미국주식 늬우스  ·  호외", F(BLK, 64), (20, 20, 20))
        d.rectangle([60, 358, W - 60, 364], fill=(20, 20, 20))
        ctext(d, 420, date, fit(d, date, BLK, 110), (20, 20, 20))
        ctext(d, 640, top, fit(d, top, BLK, 150), (180, 30, 30))
        ctext(d, 860, big, fit(d, big, BLK, 220), (20, 20, 20))
        ctext(d, 1160, small, fit(d, small, BLD, 70), (60, 60, 60))
        ctext(d, 1260, bot, fit(d, bot, BLD, 60), (60, 60, 60))
        m = mascot(300); im.paste(m, ((W - m.width) // 2, 1380), m)
    else:  # card
        im = Image.new("RGB", (W, H), (16, 20, 40)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([80, 300, W - 80, 1300], 40, fill=(26, 32, 64), outline=(240, 200, 40), width=8)
        ctext(d, 340, date, fit(d, date, BLK, 90, W - 260), (240, 200, 40))
        ctext(d, 520, top, fit(d, top, BLK, 120, W - 260), (255, 255, 255))
        ctext(d, 720, big, fit(d, big, BLK, 240, W - 260), (240, 200, 40))
        ctext(d, 1040, small, fit(d, small, BLK, 72, W - 260), (200, 220, 255))
        ctext(d, 1150, bot, fit(d, bot, BLD, 56, W - 260), (170, 180, 210))
        m = mascot(300); im.paste(m, (W - m.width - 120, 1330), m)
    im.save(out, quality=90); print("thumb", st, out)

if __name__ == "__main__":
    A = ARGS; mode = A[0] if A else "full"
    if mode == "job":
        j = V.qtts_job(A[1]); j["items"] = [i for i in j["items"] if i["id"].endswith("_c1")]
        json.dump(j, open(A[2], "w"), ensure_ascii=False, indent=1); print(len(j["items"]), "줄"); sys.exit()
    if mode == "thumb": thumb(A[1]); sys.exit()
    V.placeholder_narration()
    scenes, starts = V.layout(); total = starts[-1]
    print("scene durations:", [round(s["dur"], 1) for s in scenes], "total:", round(total, 1), "(60초 넘으면 줄을 뺀다)" if total > 60 else "")
    json.dump(V.spec(scenes, starts, total), open(f"{V.OUT}/spec.json", "w"), ensure_ascii=False, indent=1)
    from PIL import Image
    if mode == "times": sys.exit()
    if mode == "stills":
        for T in [float(x) for x in A[1].split(",")]:
            V.render_px(T, scenes, starts, total).resize((360, 640), Image.LANCZOS).save(f"{V.OUT}/s_{T:05.1f}.png")
        sys.exit()
    V.make_audio(f"{V.OUT}/mix.wav", scenes, starts, total)
    if mode == "audio": sys.exit()
    n = int(total * V.FPS); os.makedirs(f"{V.OUT}/px", exist_ok=True)
    for i in range(n):
        V.render_px(i / V.FPS, scenes, starts, total).save(f"{V.OUT}/px/{i:05d}.png", compress_level=1)
        if i % 300 == 0: print(i, "/", n, flush=True)
    print("done", total)
