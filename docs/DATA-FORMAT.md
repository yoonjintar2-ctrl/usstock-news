# today.json / drafts/D.json 형식

숫자 칸은 모두 `{v, src, asof}` 객체로 쓴다. `v` 가 null 이면 지면에 "확인 중"으로 나온다.

```json
{
  "date": "2026-11-20", "no": 1,
  "lead": "한두 문장 리드",
  "fx": {"usdkrw": {"v": null, "src": "", "asof": ""}},
  "market": {
    "rows": [
      {"name": "S&P 500", "close": {"v": null, "src": "", "asof": ""}, "chg_pct": {"v": null, "src": "", "asof": ""}},
      {"name": "나스닥", "close": {...}, "chg_pct": {...}},
      {"name": "다우", "close": {...}, "chg_pct": {...}},
      {"name": "미 국채 10년", "close": {...}, "chg_pct": {...}}
    ],
    "note": "한 줄 해설(80자)"
  },
  "stock": {
    "ticker": "NVDA", "name": "엔비디아",
    "title": "제목(숫자가 있으면 본문 숫자와 같게)",
    "body": ["문단1", "문단2"],
    "price": {"close": {...}, "chg_pct": {...}},
    "chart": {"points": [["2026-11-13", 0.0], ...], "src": "", "asof": ""},
    "img": "img/D-stock.jpg", "video": "img/D-stock.mp4", "alt": "",
    "ai": "영어 그림 프롬프트(선택)",
    "sources": [{"title": "", "url": ""}]
  },
  "earnings": [{"date": "2026-11-20", "time": "장 마감 후", "company": "", "ticker": "", "src": ""}],
  "term": {"word": "", "body": ""},
  "quiz": {"q": "", "options": ["", "", ""], "answer": 0, "chart": {...}},
  "onthisday": [{"year": 1987, "title": "", "body": "", "sources": [""]}],
  "disclaimer": "투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다."
}
```

- 변화율 `chg_pct` 는 부호 있는 숫자(+1.23 / -0.85). 지면은 ▲▼ 와 부호로 표시하고 색은 보조로만.
- 달러 금액이 본문에 나오면 `scripts/check_numbers.py` 가 같은 문장 안에 `원` 환산이 있는지 본다.
