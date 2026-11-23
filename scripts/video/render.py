"""미국주식 늬우스 '간밤 미장 요약' 세로 영상 렌더러.

python3 scripts/video/render.py video/2026-11-21.json out/          (TTS: supertonic, 깃허브 러너에서)
python3 scripts/video/render.py video/2026-11-21.json out/ --dry    (목소리 없이 길이만 추정 — 화면 점검용)

입력 JSON(video/D.json):
{ "date": "2026-11-21", "wd": "토", "title": "...", "description": "...", "tags": [...],
  "thumb": {"head": "엔비디아 -14%", "sub": "S&P 7일 연속 하락"},
  "scenes": [ {"kind": "intro|story|market|news|schedule|outro", "tag": "1면", "head": "제목", "img": "img/...jpg",
               "rows": [["S&P 500", "6,910.39", "-3.70%"], ...], "lines": ["나레이션 한 문장", ...]} ] }
자막 = 나레이션 원문(토씨까지 동일). 읽기는 ko_read.read() 로 숫자·약어를 바꿔 TTS 에 넣는다.
"""
import json, math, os, re, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from ko_read import read

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FD = os.path.join(ROOT, 'assets', 'fonts')
F = lambda w, s: ImageFont.truetype(os.path.join(FD, f'Pretendard-{w}.otf'), s)
W, H, FPS = 1080, 1920, 30
PAPER, INK, MUTE, UP, DN = (237, 237, 237), (17, 17, 17), (110, 110, 110), (22, 140, 70), (200, 40, 40)
SR = 44100
X0, X1 = 90, 990          # 좌우 안전 여백(쇼츠 UI)
SUB_Y = 1330              # 자막 기준선(하단 UI 위)
VOICE = os.getenv('VOICE', 'F1'); PITCH = float(os.getenv('PITCH_ST', '2')); SPEED = float(os.getenv('SPEED', '1.0'))


# ── 음성 ───────────────────────────────────────────────
class Voice:
    def __init__(self, dry):
        self.dry = dry
        self.vdir = os.getenv('VOICE_DIR')        # 맥 Qwen 마스코트 목소리(미리 다듬은 44.1kHz wav, 파일명 = 장면_줄.wav)
        if not dry and not self.vdir:
            from supertonic import TTS
            self.tts = TTS()
            self.style = self.tts.get_voice_style(VOICE)

    def say(self, text, path):
        spoken = read(text)
        if self.vdir and not self.dry:
            return load_wav(os.path.join(self.vdir, os.path.basename(path))), spoken
        if self.dry:
            dur = max(1.2, len(spoken) * 0.115)
            a = np.zeros(int(dur * SR), np.float32)
        else:
            wav, _ = self.tts.synthesize(spoken, voice_style=self.style, lang='ko', speed=SPEED)
            raw = path + '.raw.wav'
            self.tts.save_audio(wav, raw)
            # 피치 +2음(rubberband: 길이 유지, 포먼트 보존)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af',
                            f'rubberband=pitch={2 ** (PITCH / 12):.5f}:formant=preserved,aresample={SR}', '-ac', '1', path], check=True)
            a = load_wav(path)
        return a, spoken


def load_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(1)
    return x


def bgm(sec):
    """밝고 잔잔한 패드 + 가벼운 아르페지오(한 곡 쭉)."""
    t = np.arange(int(sec * SR)) / SR
    prog = [(60, 64, 67, 71), (57, 60, 64, 67), (53, 57, 60, 64), (55, 59, 62, 65)]   # Cmaj7 Am7 Fmaj7 G7
    bar = 4.0
    out = np.zeros_like(t)
    for i in range(int(sec // bar) + 1):
        ch = prog[i % 4]; s = int(i * bar * SR); e = min(len(t), int((i + 1) * bar * SR) + SR)
        if s >= len(t): break
        tt = t[s:e] - i * bar
        env = np.minimum(1, tt / 0.8) * np.exp(-np.maximum(0, tt - bar) * 3)
        for n in ch:
            f = 440 * 2 ** ((n - 69) / 12)
            out[s:e] += 0.05 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt))
        for k in range(8):  # 아르페지오
            n = ch[k % 4] + 12; st = s + int(k * bar / 8 * SR); en = min(len(t), st + int(0.45 * SR))
            if st >= len(t): break
            tt2 = (np.arange(en - st)) / SR
            out[st:en] += 0.035 * np.exp(-tt2 * 6) * np.sin(2 * np.pi * 440 * 2 ** ((n - 69) / 12) * tt2)
    fade = np.minimum(1, np.minimum(t / 1.5, (sec - t) / 2.0))
    return out * np.clip(fade, 0, 1)


# ── 그리기 도우미 ──────────────────────────────────────
def wrap(d, text, font, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines


def sub_chunks(text, maxw=X1 - X0 - 40):
    """자막 한 줄씩(1~4어절, 폭 넘으면 끊기). 원문 그대로."""
    d = ImageDraw.Draw(Image.new('L', (10, 10)))
    f = F('ExtraBold', 62)
    out, cur = [], ''
    for w_ in text.split(' '):
        t = (cur + ' ' + w_).strip()
        if cur and (d.textlength(t, font=f) > maxw or len(cur.split(' ')) >= 4 or cur.endswith((',', '.', '?'))):
            out.append(cur); cur = w_
        else:
            cur = t
    if cur: out.append(cur)
    return out


def chg_col(s):
    return DN if s.strip().startswith(('-', '−', '▼')) else UP if s.strip().startswith(('+', '▲')) else INK


def header(d, date, wd):
    m, dd = int(date[5:7]), int(date[8:10])
    d.text((X0, 150), '미국주식 늬우스', font=F('Bold', 40), fill=MUTE)
    d.text((X0, 200), f'{m}월 {dd}일', font=F('Black', 120), fill=INK)
    d.text((X0 + d.textlength(f'{m}월 {dd}일', font=F('Black', 120)) + 22, 262), f'({wd}) 간밤 미장', font=F('ExtraBold', 52), fill=INK)
    d.line((X0, 350, X1, 350), fill=INK, width=5)


def scene_base(sc, V):
    """장면 바탕(움직이지 않는 부분)과 줌할 그림을 만든다."""
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    header(d, V['date'], V['wd'])
    y = 390
    if sc.get('tag'):
        f = F('ExtraBold', 40); tw = d.textlength(sc['tag'], font=f)
        d.rectangle((X0, y, X0 + tw + 28, y + 58), fill=INK); d.text((X0 + 14, y + 6), sc['tag'], font=f, fill=PAPER); y += 80
    if sc.get('head'):
        f = F('Black', 80 if len(sc['head']) < 18 else 68)
        for ln in wrap(d, sc['head'], f, X1 - X0)[:3]:
            d.text((X0, y), ln, font=f, fill=INK); y += int(f.size * 1.22)
        y += 18
    pic = None
    if sc.get('img'):
        p = Image.open(os.path.join(ROOT, sc['img'])).convert('RGB')
        pw = X1 - X0; ph = int(p.height * pw / p.width); ph = min(ph, SUB_Y - 80 - y)
        pic = (p, (X0, y, pw, ph)); y += ph + 20
    if sc.get('rows'):
        f1, f2 = F('Bold', 62), F('ExtraBold', 68)
        for name, v, c in sc['rows']:          # 11/22 발행인: 지수 값(포인트)은 빼고 등락률(%)만
            d.text((X0, y), name, font=f1, fill=INK)
            d.text((X1, y), c, font=f2, fill=chg_col(c), anchor='ra')
            y += 96; d.line((X0, y - 12, X1, y - 12), fill=(200, 200, 200), width=2)
    if sc.get('items'):
        f1, f2 = F('ExtraBold', 52), F('SemiBold', 38)
        boxes = []
        for a, b in sc['items']:
            y0 = y
            d.text((X0 + 24, y), a, font=f2, fill=MUTE); y += 46
            for ln in wrap(d, b, f1, X1 - X0 - 24)[:1 if len(sc['items']) > 3 else 2]:
                d.text((X0 + 24, y), ln, font=f1, fill=INK); y += 62
            boxes.append((y0 - 8, y + 4)); y += 20
        sc['_boxes'] = boxes
    if sc['kind'] == 'outro':
        d.text((W // 2, 760), 'stocknews.jintar.co.kr', font=F('Black', 70), fill=INK, anchor='mm')
        d.text((W // 2, 850), '매일 아침 미국 증시를 신문 한 장으로', font=F('Bold', 44), fill=MUTE, anchor='mm')
    d.text((X0, 1840), '※ 투자 판단과 책임은 본인에게 있습니다', font=F('SemiBold', 28), fill=MUTE)
    return im, pic


def draw_sub(im, text):
    d = ImageDraw.Draw(im)
    f = F('ExtraBold', 62)
    tw = d.textlength(text, font=f)
    x = (W - tw) / 2
    d.rounded_rectangle((x - 26, SUB_Y - 70, x + tw + 26, SUB_Y + 18), 14, fill=(255, 255, 255), outline=INK, width=3)
    d.text((x, SUB_Y - 62), text, font=f, fill=INK)


def thumbnail(V, out):
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    m, dd = int(V['date'][5:7]), int(V['date'][8:10])
    d.rectangle((0, 0, W, 760), fill=INK)
    d.text((W // 2, 300), f'{m}.{dd}', font=F('Black', 330), fill=PAPER, anchor='mm')
    d.text((W // 2, 590), f"({V['wd']}) 간밤 미장 요약", font=F('ExtraBold', 76), fill=PAPER, anchor='mm')
    T = V.get('thumb', {})
    y = 900
    for ln in wrap(d, T.get('head', ''), F('Black', 118), X1 - X0)[:3]:
        d.text((W // 2, y), ln, font=F('Black', 118), fill=INK, anchor='mm'); y += 140
    for ln in wrap(d, T.get('sub', ''), F('ExtraBold', 64), X1 - X0)[:2]:
        d.text((W // 2, y + 20), ln, font=F('ExtraBold', 64), fill=DN, anchor='mm'); y += 84
    d.text((W // 2, 1700), '미국주식 늬우스', font=F('Bold', 48), fill=MUTE, anchor='mm')
    im.save(out, quality=90)
    return im


def main(spec, outdir, dry=False):
    V = json.load(open(spec, encoding='utf-8'))
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, 'tmp'); os.makedirs(tmp, exist_ok=True)
    voice = Voice(dry)
    GAP, SCENE_GAP = 0.32, 0.55
    audio, timeline, t = [], [], 0.6      # timeline: (start, end, scene_idx, sub_text)
    audio.append(np.zeros(int(0.6 * SR), np.float32))
    scenes = []
    for si, sc in enumerate(V['scenes']):
        s0 = t
        for li, line in enumerate(sc.get('lines', [])):
            a, spoken = voice.say(line, os.path.join(tmp, f'{si:02d}_{li:02d}.wav'))
            dur = len(a) / SR
            chunks = sub_chunks(line); tot = sum(len(c) for c in chunks)
            ct = t
            for c in chunks:
                cd = dur * len(c) / tot
                timeline.append((ct, ct + cd, si, c, li)); ct += cd
            audio.append(a); audio.append(np.zeros(int(GAP * SR), np.float32)); t += dur + GAP
        audio.append(np.zeros(int(SCENE_GAP * SR), np.float32)); t += SCENE_GAP
        scenes.append((s0, t))
    total = t + 0.8
    voice_track = np.concatenate(audio + [np.zeros(int(0.8 * SR), np.float32)])
    mix = voice_track * 0.95 + bgm(len(voice_track) / SR) * (0.6 if not dry else 1)
    mix = np.clip(mix, -1, 1)
    wav_p = os.path.join(tmp, 'mix.wav')
    with wave.open(wav_p, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

    bases = [scene_base(sc, V) for sc in V['scenes']]
    n = int(total * FPS)
    mp4 = os.path.join(outdir, f"{V['date']}-summary.mp4")
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', wav_p, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p',
                           '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-shortest', mp4], stdin=subprocess.PIPE)
    ti = 0; sheet = []
    marks = {int(n * k / 9) for k in range(1, 9)}
    for fi in range(n):
        tt = fi / FPS
        si = next((k for k, (a, b) in enumerate(scenes) if a <= tt < b), len(scenes) - 1)
        base, pic = bases[si]
        fr = base.copy()
        if pic:
            p, (x, y, pw, ph) = pic
            a, b = scenes[si]; prog = min(1, max(0, (tt - a) / max(0.1, b - a)))
            z = 1.0 + 0.05 * prog
            big = p.resize((int(pw * z), int(p.height * pw / p.width * z)))
            ox = (big.width - pw) // 2; oy = int((big.height - ph) * 0.5)
            fr.paste(big.crop((ox, oy, ox + pw, oy + ph)), (x, y))
            ImageDraw.Draw(fr).rectangle((x - 2, y - 2, x + pw + 1, y + ph + 1), outline=INK, width=3)
        while ti < len(timeline) and timeline[ti][1] <= tt: ti += 1
        cur = timeline[ti] if ti < len(timeline) and timeline[ti][0] <= tt else None
        bx = V['scenes'][si].get('_boxes')
        if bx and cur and cur[2] == si:
            k = cur[4] - (len(V['scenes'][si]['lines']) - len(bx))
            if 0 <= k < len(bx):
                y0, y1 = bx[k]; dr = ImageDraw.Draw(fr)
                dr.rectangle((X0, y0, X0 + 10, y1), fill=DN)
        if cur:
            draw_sub(fr, cur[3])
        # 장면 전환: 앞 0.25초 페이드
        a = scenes[si][0]
        if si and tt - a < 0.25:
            prev = bases[si - 1][0]
            fr = Image.blend(prev, fr, (tt - a) / 0.25)
        ff.stdin.write(fr.tobytes())
        if fi in marks: sheet.append(fr.resize((270, 480)))
    ff.stdin.close(); ff.wait()
    cs = Image.new('RGB', (270 * 4, 480 * 2), 'white')
    for k, s in enumerate(sheet[:8]): cs.paste(s, ((k % 4) * 270, (k // 4) * 480))
    cs.save(os.path.join(outdir, f"{V['date']}-sheet.jpg"), quality=80)
    thumbnail(V, os.path.join(outdir, f"{V['date']}-thumb.jpg"))
    json.dump({'mp4': mp4, 'sec': round(total, 1), 'subs': [x[3] for x in timeline]}, open(os.path.join(outdir, f"{V['date']}-render.json"), 'w', encoding='utf-8'), ensure_ascii=False)
    print('ok', mp4, round(total, 1), 's')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], '--dry' in sys.argv)
