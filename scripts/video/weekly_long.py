"""일요일 '주간 미장 정리' 롱폼(세로 1080x1920) — 한 주 동안 올린 8비트 1면 쇼츠를 날짜 카드와 함께 이어 붙인다.
python3 scripts/video/weekly_long.py OUT.mp4 OUT_thumb.jpg "11/24~11/29" clip1.mp4 "11/25(화) 반도체 -7.9%" clip2.mp4 "..." ...
 · 새 대본·TTS 없이 이미 만든 영상을 재사용(토큰 거의 안 씀). 클립은 맥 ~/Downloads/usstock_videos/ 에 매일 쌓아 둔 최종본.
 · 앞뒤에 표지·끝 카드(구독 안내), 각 클립 앞에 2초 날짜 카드. 배경음·내레이션은 각 클립 것 그대로."""
import os, sys, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FD = os.path.join(R, 'assets', 'fonts'); W, H = 1080, 1920
F = lambda w, s: ImageFont.truetype(os.path.join(FD, f'Pretendard-{w}.otf'), s)

def card(path, lines, bg=(16, 20, 40)):
    im = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(im); y = 640
    for txt, w, s, col in lines:
        f = F(w, s)
        while d.textlength(txt, font=f) > W - 200 and s > 40: s -= 6; f = F(w, s)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col); y += int(s * 1.45)
    im.save(path, quality=92); return path

def seg_from_img(img, sec, out):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', str(sec), '-i', img, '-f', 'lavfi', '-t', str(sec),
                    '-i', 'anullsrc=r=48000:cl=stereo', '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)

def norm(src, out):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', f'scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', out], check=True)

def main():
    out, thumb, week = sys.argv[1:4]; pairs = list(zip(sys.argv[4::2], sys.argv[5::2]))
    T = tempfile.mkdtemp(); parts = []
    YEL, WH, GR = (240, 200, 40), (255, 255, 255), (170, 180, 210)
    seg_from_img(card(f'{T}/c0.jpg', [('미국주식 늬우스', 'Bold', 60, GR), ('주간 미장 정리', 'Black', 130, WH), (week, 'Black', 110, YEL),
                                     (f'이번 주 큰 이슈 {len(pairs)}개', 'Bold', 64, GR)]), 3.0, f'{T}/p000.mp4'); parts.append(f'{T}/p000.mp4')
    for k, (clip, title) in enumerate(pairs, 1):
        seg_from_img(card(f'{T}/c{k}.jpg', [(f'{k} / {len(pairs)}', 'Bold', 60, GR), (title, 'Black', 92, WH)]), 2.0, f'{T}/p{k:02d}a.mp4')
        norm(clip, f'{T}/p{k:02d}b.mp4'); parts += [f'{T}/p{k:02d}a.mp4', f'{T}/p{k:02d}b.mp4']
    seg_from_img(card(f'{T}/ce.jpg', [('구독하고', 'Black', 120, WH), ('매일 아침 미국주식 소식', 'Black', 84, YEL), ('받아보세요', 'Black', 120, WH),
                                     ('투자 판단과 책임은 본인에게 있습니다.', 'SemiBold', 44, GR)]), 3.5, f'{T}/pzzz.mp4'); parts.append(f'{T}/pzzz.mp4')
    open(f'{T}/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-c:v', 'libx264', '-preset', 'veryfast',
                    '-crf', '22', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
    card(thumb, [('주간 미장 정리', 'Black', 140, WH), (week, 'Black', 130, YEL)] + [(t, 'Bold', 56, GR) for _, t in pairs[:5]])
    print('ok', out)

if __name__ == '__main__': main()
