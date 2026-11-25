"""11/26 발행인: 목소리가 가끔 피치가 높아져 다른 사람처럼 들림 → 테이크별 중앙 음높이(F0)를 재서 튀는 테이크를 거른다.
python3 pitch_check.py <cand_dir>   → 전체 중앙값 대비 +15% 넘는(또는 -15% 밑) 테이크 id 목록 출력(다시 만들 대상)
다른 스크립트에서: from pitch_check import f0_median, pick_by_pitch"""
import sys, os, glob, json
import numpy as np
import librosa

def f0_median(path):
    y, sr = librosa.load(path, sr=16000)
    f0 = librosa.yin(y, fmin=120, fmax=600, sr=sr, frame_length=1024)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0][:len(f0)]
    v = f0[(rms > 0.02) & (f0 > 125) & (f0 < 590)]
    return float(np.median(v)) if len(v) > 10 else None

def table(cdir):
    out = {}
    for p in sorted(glob.glob(os.path.join(cdir, '*_c*.wav'))):
        out[p] = f0_median(p)
    return out

def pick_by_pitch(cands, T, ref):
    """같은 줄의 후보들 중 기준 음높이(ref)에 가장 가까운 것"""
    ok = [c for c in cands if T.get(c)]
    return min(ok, key=lambda c: abs(T[c] - ref)) if ok else cands[0]

if __name__ == '__main__':
    cdir = sys.argv[1]; T = table(cdir)
    vals = [v for v in T.values() if v]; ref = float(np.median(vals))
    bad = [os.path.basename(p)[:-4] for p, v in T.items() if v and abs(v / ref - 1) > 0.15]
    print(json.dumps({'ref_hz': round(ref, 1), 'outliers': bad, 'all': {os.path.basename(p): (round(v, 1) if v else None) for p, v in T.items()}}, ensure_ascii=False, indent=1))
