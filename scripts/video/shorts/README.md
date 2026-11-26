# 1면 8비트 쇼츠 (pixel_kit 엔진)
- d1121_video.py: 엔진(장면·자막·BGM·믹스) + 11/21 엔비디아·브로드컴. d1124_video.py: 엔진을 import 해서 장면·대본만 바꾼 예(11/24 엔비디아 +31%·크라우드).
- 새 날짜는 d1124_video.py 를 복사해 장면·SCRIPTS 만 고쳐 쓴다. /home/claude/pixel_kit 에 복사해 실행(make_video·sandisk_video·nike_video·bgm_kit 필요).
- 순서: `VID=x python3 dMMDD_video.py job NAME out.json` → 맥 qtts → narr_prep.py <cand_dir> - dMMDD_video(VID 설정) → `stills` 검수 → `full` → talk_render2.py(호스트, 450px 8샘플 --resume) → host_compose.py → loudnorm -16.
- 썸네일: d1121_thumbs.py(신문 호외형·경고 테이프형) — 날짜 크게, 매번 다른 틀.
- **배경(2026-11-26 발행인, 다음 영상부터 계속): 모눈·격자 무늬 배경 금지.** 단색에 아주 살짝 세로 그라데이션만(엔진 `grad_bg()`, 위 (28,26,46) → 아래 (16,14,26) 정도). pixel_kit nike_video.render_low 등 배경을 그리는 곳의 모눈 그리기를 grad_bg 로 바꾸고, `stills` 검수 때 모눈이 남아 있지 않은지 확인한다.
