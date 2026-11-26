"""맥 Qwen 테이크(s{장면}_{줄}_c1.wav) → 요약 영상용 44.1kHz 클립({장면}_{줄}.wav)
python3 prep_sum.py <cand_dir> <out_dir>"""
import sys, os, glob, re, wave
import numpy as np
from scipy.signal import resample_poly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narr_prep import load, clean, raw_cut

from pitch_check import table, pick_by_pitch

cdir, odir = sys.argv[1:3]; os.makedirs(odir, exist_ok=True)
# 11/26 발행인: 피치가 튀어 다른 사람 목소리처럼 들리는 테이크를 피한다 — 줄마다 후보(c1, c2…) 중 전체 중앙 음높이에 가장 가까운 것
T = table(cdir); REF = float(np.median([v for v in T.values() if v]))
lines = {}
for p in sorted(glob.glob(os.path.join(cdir, 's*_c*.wav'))):
    m = re.search(r's(\d+)_(\d+)_c\d+\.wav$', os.path.basename(p))
    if m: lines.setdefault(m.groups(), []).append(p)
for (si, li), cands in sorted(lines.items()):
    ok = [c for c in cands if not raw_cut(*load(c))] or cands           # 11/27: 말 끝이 잘린 테이크는 피한다
    p = pick_by_pitch(ok, T, REF)
    if raw_cut(*load(p)): print(f'  ⚠ 끝 잘림 {os.path.basename(p)} — 다시 만들기 권장(--retake s{si}_{li})')
    if T.get(p) and abs(T[p] / REF - 1) > 0.15: print(f'  ⚠ 피치 튐 {os.path.basename(p)} {T[p]:.0f}Hz (기준 {REF:.0f}Hz) — 다시 만들기 권장')
    x, sr = load(p); y = clean(x, sr, '')
    y = resample_poly(y, 147, 80).astype(np.float32)
    y *= 0.11 / (np.sqrt((y ** 2).mean()) + 1e-9)
    if np.abs(y).max() > 0.9: y *= 0.9 / np.abs(y).max()
    with wave.open(os.path.join(odir, f'{si}_{li}.wav'), 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((y * 32767).astype(np.int16).tobytes())
    print(si, li, f'{len(x) / sr:.2f}s → {len(y) / 44100:.2f}s')
