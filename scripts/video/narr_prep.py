"""맥 Qwen 클론 TTS 테이크 → 영상용 내레이션 클립 (2026-11-10 정리)
python3 narr_prep.py <cand_dir> <picks.json|-> <video_module>
 · 각 문장 끝에 붙인 ' 음.'(끝음 잘림 방지용 꼬리)은 마지막 짧은 발화 덩어리(0.6초 이하, 앞 무음 0.45초 이상)로 감지해 잘라냄
 · 문장 안 긴 쉼(0.45초 초과)은 0.34초로 줄임('혹시…' 같은 말줄임은 0.5초)
 · 24kHz → 44.1kHz, 영상 모듈의 clip_path(내레이션 문장) 위치에 .npy로 저장
 · SPEED=1.05 환경변수 → 피치 유지 배속(atempo)
 · picks.json = pick_takes 결과 {line_id: wav경로}. '-'면 c1/c2 중 꼬리 제거 후 길이가 중간값에 가까운 것"""
import sys, os, json, glob, re, importlib, wave
import numpy as np
from scipy.signal import resample_poly

def load(p):
    w = wave.open(p); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x, sr

def regions(x, sr, thr=0.02, hop_s=0.02, merge=0.12):
    hop = int(sr * hop_s); env = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    on = env > thr; regs = []; s = None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None: regs.append([s, i]); s = None
    if s is not None: regs.append([s, len(on)])
    m = []
    for a, b in regs:
        if m and (a - m[-1][1]) * hop_s < merge: m[-1][1] = b
        else: m.append([a, b])
    return [(a * hop, b * hop) for a, b in m if (b - a) * hop_s >= 0.06]

def clean(x, sr, text):
    R = regions(x, sr)
    if len(R) >= 2:
        a, b = R[-1]; pa, pb = R[-2]
        if text.rstrip().endswith('음.') and (b - a) / sr <= 0.6 and (a - pb) / sr >= 0.45: R = R[:-1]   # 옛 ' 음.' 꼬리만 제거(11/26 뒤로는 안 붙임)
    ell = '…' in text
    out = []; pad = int(0.06 * sr)
    s0 = max(0, R[0][0] - pad)
    for i, (a, b) in enumerate(R):
        seg = x[max(0, a - pad) if i else s0: min(len(x), b + pad)]
        if i:
            gap = (a - R[i - 1][1]) / sr
            keep = gap if gap <= 0.45 else (0.5 if ell and i == 1 else 0.34)
            if keep < gap: out.append(np.zeros(max(0, int((keep - 0.12) * sr)), np.float32))
            else: seg = x[R[i - 1][1] + pad: min(len(x), b + pad)]
        out.append(seg)
    # 11/27 발행인 지적: 문장 끝 '다'가 울림이 다 끝나기 전에 잘려 말이 끊긴 듯 들림.
    # 원인 — 끝 경계를 큰 문턱(0.02)으로 잡고 60ms만 더 남긴 뒤 40ms로 급히 줄였기 때문.
    # 고침 — 마지막 덩어리 뒤로 작은 문턱(0.004)까지 울림을 따라가 끝을 찾고, 150ms를 더 남긴 뒤 120ms 동안 서서히 줄인다.
    hop = int(sr * 0.01); e = R[-1][1]; lim = min(len(x), e + int(0.6 * sr))
    while e + hop <= lim and np.sqrt((x[e:e + hop] ** 2).mean()) > 0.004: e += hop
    tail_end = min(len(x), e + int(0.15 * sr)); cur_end = min(len(x), R[-1][1] + pad)
    if tail_end > cur_end: out.append(x[cur_end:tail_end])
    y = np.concatenate(out)
    fo = min(len(y), int(0.12 * sr)); y[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    return y

def raw_cut(x, sr):
    """TTS 원본 자체가 소리 나는 중에 끝났는지(마지막 30ms 세기 > 0.008) — 모델이 말 끝을 다 만들기 전에 멈춘 경우. 다시 만들어야 한다."""
    n = int(0.03 * sr); return len(x) > n and float(np.sqrt((x[-n:] ** 2).mean())) > 0.008

def tail_cut(y, sr):
    """검수용: 끝 60ms 평균 세기 — 0.01 넘으면 아직 소리가 나는 중에 잘린 것(끝 잘림 의심)."""
    n = int(0.06 * sr); return float(np.sqrt((y[-n * 2:-n] ** 2).mean())) if len(y) > 2 * n else 0.0

if __name__ == '__main__':
    cdir, picks, mod = sys.argv[1:4]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    V = importlib.import_module(mod)
    lines = {lid: n for _, ls in V.SCRIPT for _, n, lid in ls}
    P = json.load(open(picks)) if picks != '-' else {}
    REF_HZ = None
    try:
        from pitch_check import table
        _T = table(cdir); REF_HZ = float(np.median([v for v in _T.values() if v]))
    except Exception: pass
    for lid, n in lines.items():
        cands = sorted(glob.glob(os.path.join(cdir, f'{lid}_c*.wav')))
        if not cands: print('MISSING', lid); continue
        cl = {}
        for c in cands:
            x, sr = load(c); cl[c] = clean(x, sr, n)
        pick = P.get(lid)
        if pick not in cl:
            md = np.median([len(v) for v in cl.values()])
            from pitch_check import f0_median            # 11/26: 피치가 튄 테이크는 피한다
            F = {c: f0_median(c) for c in cl}; ref = REF_HZ or np.median([v for v in F.values() if v] or [200])
            CUT = {c: raw_cut(*load(c)) for c in cl}                # 11/27: 말 끝이 잘린 테이크도 피한다
            pick = min(cl, key=lambda c: abs(len(cl[c]) - md) / 24000 + (3 if F[c] and abs(F[c] / ref - 1) > 0.15 else 0) + (2 if CUT[c] else 0) + (0 if c.endswith('_c1.wav') else 0.01))
            if CUT[pick]: print(f'  ⚠ 끝 잘림 {os.path.basename(pick)} — 다시 만들기(--retake {lid})')
        y = resample_poly(cl[pick], 147, 80).astype(np.float32)               # 24000 → 44100
        sp = float(os.environ.get('SPEED', 1.0))                              # 예: SPEED=1.05 (60초 맞추기, 피치 유지)
        if abs(sp - 1) > 1e-3:
            import subprocess
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', '44100', '-ac', '1', '-i', '-', '-af', f'atempo={sp}',
                                  '-f', 'f32le', '-ar', '44100', '-ac', '1', '-'], input=y.tobytes(), capture_output=True, check=True).stdout
            y = np.frombuffer(raw, np.float32).copy()
        np.save(V.clip_path(n), y)
        print(lid, os.path.basename(pick), ' '.join(f'{os.path.basename(c)[-6:-4]}={len(v) / 24000:.2f}s' for c, v in cl.items()), '→', f'{len(y) / 44100:.2f}s')
