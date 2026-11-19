#!/bin/bash
# 더블클릭 한 번 → 모델을 맥 GPU에 올려 두고, Claude가 넣는 음성 작업을 자동으로 처리해요. 창을 닫으면 멈춰요.
cd "$(dirname "$0")"
exec > >(tee "$(pwd)/worker_log.txt") 2>&1
echo "== $(date) TTS 작업 대기기 시작 =="
"$HOME/qtts-env312/bin/python" tts_worker.py
echo "== 대기기가 멈췄어요. 이 창은 닫아도 돼요 =="
