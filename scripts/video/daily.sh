#!/bin/bash
# 매일 영상 2편(① 요약 ② 1면 최대 이슈 8비트) 실행기 — docs/RUNBOOK_VIDEO.md 순서대로 부른다.
#   bash scripts/video/daily.sh setup <kit.tgz>      키트 풀기·설치·저장소 최신 스크립트 덮어쓰기
#   bash scripts/video/daily.sh jobs D              맥 qtts 작업 파일을 tts/queue/ 에 만들고 push (발행 작업이 이미 했으면 건너뜀)
#   bash scripts/video/daily.sh fetch NAME DIR      맥 대기기가 깃허브 tts-out 에 올린 결과를 받아 DIR 에 풂(없으면 exit 4 → 맥에서 직접 가져오기)
#   bash scripts/video/daily.sh sum D <후보폴더>      요약: 클립 정리 → 렌더 → 길이·피치 점검 → /home/claude/vid/D-summary.mp4
#   bash scripts/video/daily.sh top D <후보폴더> [대본]  8비트(대본 기본 video/top/D.json, 일요일 개념 영상은 video/top/D-concept.json): 내레이션 → 오디오 → 마스코트 → 합성 → /home/claude/vid/D-top.mp4 + 썸네일
#   bash scripts/video/daily.sh sheet <mp4>         검수용 12프레임 시트(<mp4>.sheet.jpg)
#   bash scripts/video/daily.sh split <mp4>         3.5MB 조각(<mp4>.part_aa …) — 크롬 file_upload 용
set -e
R=$(cd "$(dirname "$0")/../.." && pwd); K=/home/claude/pixel_kit; OUTV=/home/claude/vid; mkdir -p $OUTV
cmd=$1; shift
mmdd() { echo "${1:5:2}${1:8:2}"; }
# 0초 화면 = 표지: 썸네일 0.4초를 영상 맨 앞에 붙인다(쇼츠 피드 첫 화면). cover <mp4> <thumb.jpg>
cover() { local F=$1 T=$2 X=/tmp/cover_$$; mkdir -p $X
  ffmpeg -y -loglevel error -loop 1 -t 0.4 -i $T -f lavfi -t 0.4 -i anullsrc=r=48000:cl=stereo -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p" -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k -shortest $X/c.mp4
  ffmpeg -y -loglevel error -i $F -c:v libx264 -preset veryfast -crf 20 -vf fps=30,format=yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 $X/m.mp4
  printf "file '%s'\nfile '%s'\n" $X/c.mp4 $X/m.mp4 > $X/l.txt
  ffmpeg -y -loglevel error -f concat -safe 0 -i $X/l.txt -c copy -movflags +faststart $F.tmp.mp4 && mv $F.tmp.mp4 $F; rm -rf $X; }
case $cmd in
setup)
  T=$1; [ -n "$T" ] && tar xzf "$T" -C /home/claude
  pip install -q bpy==5.2.3 librosa soundfile scipy --break-system-packages 2>/dev/null || pip install -q librosa soundfile scipy --break-system-packages
  cp $R/scripts/video/shorts/top8.py $R/scripts/video/narr_prep.py $R/scripts/video/pitch_check.py $R/scripts/video/prep_sum.py $K/ 2>/dev/null || true
  echo "setup ok" ;;
jobs)
  D=$1; M=$(mmdd $D); mkdir -p $R/tts/queue
  python3 - $R/tts/queue $D <<'PY'
import os, sys, glob, datetime
q, D = sys.argv[1:3]; d = datetime.date.fromisoformat(D)
keep = {(d - datetime.timedelta(days=i)).strftime('%m%d') for i in range(3)}
for f in glob.glob(os.path.join(q, '0us*.json')):
    b = os.path.basename(f)
    if b[3:7].isdigit() and b[3:7] not in keep: os.remove(f)
PY
  [ -f $R/tts/queue/0us${M}_1sum.json ] || python3 $R/scripts/video/sum_job.py $R/video/$D.json 0us${M}_1sum $R/tts/queue/0us${M}_1sum.json
  if [ -f $R/video/top/$D.json ] && [ ! -f $R/tts/queue/0us${M}_2top.json ]; then
    python3 $R/scripts/video/top_job.py $R/video/top/$D.json 0us${M}_2top $R/tts/queue/0us${M}_2top.json
  fi
  if [ -f $R/video/top/$D-top2.json ] && [ ! -f $R/tts/queue/0us${M}_3top2.json ]; then
    python3 $R/scripts/video/top_job.py $R/video/top/$D-top2.json 0us${M}_3top2 $R/tts/queue/0us${M}_3top2.json
  fi
  cd $R && git add tts/queue && (git diff --cached --quiet || (git commit -qm "TTS 작업 $D" && git pull -q --rebase && git push -q)); echo "queue ok" ;;
fetch)
  N=$1; DIR=$2; mkdir -p $DIR
  curl -fsSL -o /tmp/$N.zip "https://raw.githubusercontent.com/yoonjintar2-ctrl/usstock-news/tts-out/$N.zip?$(date +%s)" || { echo "tts-out/$N.zip 없음"; exit 4; }
  python3 -c "import zipfile;zipfile.ZipFile('/tmp/$N.zip').extractall('$DIR')"; ls $DIR | wc -l ;;
sum)
  D=$1; C=$2; V=/tmp/sumclips_$D; rm -rf $V
  if [ -f $R/video/$D.remap.json ]; then   # 목소리를 만든 뒤 대본에서 장면을 뺀 경우: 클립 번호를 새 대본에 맞춤
    python3 - $C /tmp/remap_$D $R/video/$D.remap.json <<'PY'
import json, os, shutil, sys
src, dst, rp = sys.argv[1:4]; R = json.load(open(rp)); shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
for f in os.listdir(src):
    k = f[:3]
    if k in R.get('drop', []): continue
    shutil.copy(os.path.join(src, f), os.path.join(dst, R.get('map', {}).get(k, k) + f[3:]))
PY
    C=/tmp/remap_$D; fi
  python3 $R/scripts/video/pitch_check.py $C | tail -5 || true
  python3 $R/scripts/video/prep_sum.py $C $V | tail -3
  VOICE_DIR=$V python3 $R/scripts/video/render.py $R/video/$D.json /tmp/sumout_$D | tail -3
  cp /tmp/sumout_$D/$D-summary.mp4 $OUTV/$D-summary.mp4; cp /tmp/sumout_$D/$D-thumb.jpg $OUTV/$D-summary-thumb.jpg
  cover $OUTV/$D-summary.mp4 $OUTV/$D-summary-thumb.jpg
  L=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUTV/$D-summary.mp4)
  echo "summary $L 초"; python3 -c "import sys; sys.exit(0 if float('$L') <= 175 else 1)" || { echo '!! 2분 55초 넘음 — 덜 중요한 줄을 빼고 다시'; exit 3; } ;;
top)
  D=$1; C=$2; S=${3:-$R/video/top/$D.json}; S=$(readlink -f $S); TAG=$(basename $S .json | sed "s/^$D//; s/^-//"); TAG=${TAG:-top}; cd $K
  VNAME=$(python3 -c "import json;s=json.load(open('$S'));print(s.get('vid') or 'top'+s['date'][5:7]+s['date'][8:10])")
  O=$K/top_$VNAME/out
  python3 $R/scripts/video/pitch_check.py $C | tail -5 || true
  TOP8_SPEC=$S python3 narr_prep.py $C - top8 | tail -2
  python3 top8.py $S times
  L=$(python3 -c "import json;print(json.load(open('$O/spec.json'))['total'])"); python3 -c "import sys; sys.exit(0 if $L <= 60 else 1)" || { echo '!! 60초 넘음 — 덜 중요한 줄을 빼고 다시'; exit 3; }
  python3 top8.py $S audio
  bash $K/hosts_any.sh $O | tail -1
  rm -rf $O/px; python3 top8.py $S full | tail -1
  python3 host_compose.py $O/spec.json $O/px $O/m $O/mix.wav $OUTV/$D-$TAG-raw.mp4
  ffmpeg -y -loglevel error -i $OUTV/$D-$TAG-raw.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -movflags +faststart $OUTV/$D-$TAG.mp4
  python3 top8.py $S thumb $OUTV/$D-$TAG-thumb.jpg
  cover $OUTV/$D-$TAG.mp4 $OUTV/$D-$TAG-thumb.jpg
  echo "top $(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUTV/$D-$TAG.mp4) 초" ;;
sheet)
  F=$1; L=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); rm -rf /tmp/sh && mkdir -p /tmp/sh
  for i in $(seq 0 11); do T=$(python3 -c "print(round(0.3+($L-0.8)*$i/11,2))"); ffmpeg -loglevel error -y -ss $T -i $F -frames:v 1 -vf scale=270:480 /tmp/sh/$(printf %02d $i).jpg; done
  python3 -c "
from PIL import Image;import glob
fs=sorted(glob.glob('/tmp/sh/*.jpg'));g=Image.new('RGB',(270*6,480*2))
for i,f in enumerate(fs):g.paste(Image.open(f),(270*(i%6),480*(i//6)))
g.save('$F.sheet.jpg',quality=80)"; echo "$F.sheet.jpg" ;;
split)
  F=$1; rm -f $F.part_*; split -b 3500000 $F $F.part_; ls $F.part_* ;;
*) echo "모르는 명령: $cmd"; exit 1 ;;
esac
