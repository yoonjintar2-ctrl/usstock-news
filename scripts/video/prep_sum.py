"""맥 Qwen 테이크(s{장면}_{줄}_c1.wav) → 요약 영상용 44.1kHz 클립({장면}_{줄}.wav)
python3 prep_sum.py <cand_dir> <out_dir>"""
import sys, os, glob, re, wave
import numpy as np
from scipy.signal import resample_poly
sys.path.insert(0, os.environ.get('PIXEL_KIT', '/home/claude/pixel_kit'))
from narr_prep import load, clean

cdir, odir = sys.argv[1:3]; os.makedirs(odir, exist_ok=True)
for p in sorted(glob.glob(os.path.join(cdir, 's*_c1.wav'))):
    m = re.search(r's(\d+)_(\d+)_c1', p); si, li = m.groups()
    x, sr = load(p); y = clean(x, sr, '')
    y = resample_poly(y, 147, 80).astype(np.float32)
    y *= 0.11 / (np.sqrt((y ** 2).mean()) + 1e-9)
    if np.abs(y).max() > 0.9: y *= 0.9 / np.abs(y).max()
    with wave.open(os.path.join(odir, f'{si}_{li}.wav'), 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((y * 32767).astype(np.int16).tobytes())
    print(si, li, f'{len(x) / sr:.2f}s → {len(y) / 44100:.2f}s')
