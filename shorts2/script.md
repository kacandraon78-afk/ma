# 쇼츠 2: "이 습관 하나가 10년 뒤 인생을 바꾼다"

## 레퍼런스 구조 분석 (70초, 9:16)
- 컷: 약 19컷, 3~4초마다 그림 전환 (줌 없이 컷 전환)
- 그림: 19세기 유럽풍 **세피아 펜화(크로스해칭)**, 젊은 남성 ↔ 노인 대비
- 상단: **노란색 고정 제목** 2줄 (영상 내내 유지)
- 중앙 하단: **흰 글씨 + 검은 외곽선** 자막 1~3줄
- 흐름: 훅(진짜 이유) → 젊을 때의 착각 → 반전("그러나 나이가 들면") → 노년의 현실 → 교훈 → **철학자 명언** → 대비 교훈 → 결론 → 엔딩 카드(검은 배경)
- 음성 트랙 없음(받은 파일 기준)

## 새 영상 (구조만 같고 주제·문장·그림은 새로 작성)
- 주제: 돈 → **시간을 쓰는 습관**, 철학자: 쇼펜하우어 → **세네카**
- 고정 제목: "이 습관 하나가 / 10년 뒤 인생을 바꾼다"
- 엔딩: 책 광고 대신 **오늘의 한 문장 + 구독 유도**

| 컷 | 그림 | 자막 |
|---|---|---|
| 1 | s01 | 젊을 때 시간 쓰는 법이 / 노후를 결정하는 진짜 이유 |
| 2 | s02 | 지금은 시간이 / 끝없이 남아 보인다 |
| 3 | s02 | 오늘 못 하면 / 내일 하면 된다고 믿는다 |
| 4 | s03 | 그렇게 미룬 하루가 / 한 달이 되고, 한 해가 된다 |
| 5 | s03 | 하지만 세월은 / 누구도 기다려 주지 않는다 |
| 6 | s04 | 어느 날 몸이 먼저 / 말을 듣지 않기 시작한다 |
| 7 | s04 | 배우고 싶던 것도 가고 싶던 곳도 / 이제는 버겁기만 하다 |
| 8 | s01 | '그때 해 둘 걸' / 그 후회가 가장 무겁다 |
| 9 | s05 | 세네카는 말했다 / 인생이 짧은 것이 아니라 / 우리가 헛되이 쓸 뿐이라고 |
| 10 | s06 | 젊은 날의 시간은 / 쉬라고 주어진 것이 아니다 |
| 11 | s07 | 미래의 나를 위해 / 미리 심어 두라고 주어진 것이다 |
| 12 | s06 | 하루 한 시간 / 읽고, 걷고, 배우는 사람은 |
| 13 | s08 | 십 년 뒤 / 전혀 다른 곳에 서 있다 |
| 14 | s09 | 젊어서 아낀 시간은 / 늙어서 자유가 되어 돌아온다 |
| 15 | s10 | 오늘의 한 시간을 / 어디에 쓸지 정해 보라 |
| 16 | s09 | 그 선택이 / 10년 뒤 당신의 얼굴이 된다 |
| 끝 | 검은 카드 | 오늘의 한 문장: "인생은 짧지 않다. 우리가 짧게 쓸 뿐이다." — 세네카 / 구독하고 매일 한 문장 받아 가세요 |

## 그림 프롬프트 (Flow 이미지 또는 Canva, 9:16)
공통 앞부분:
```
Vintage sepia pen-and-ink crosshatched engraving illustration, 19th-century European style, warm brown and ochre tones, detailed linework, dramatic light. Original characters, vertical 9:16, empty space at top for text, no text, no letters.
```
| 파일 | 공통 앞부분 뒤에 붙일 장면 |
|---|---|
| s01 | A lonely elderly man with thin white hair sits in a worn armchair in a dim old room, looking down tiredly, a large pendulum wall clock beside him. |
| s02 | A carefree young man in a waistcoat lounges lazily on an old sofa with his feet up, surrounded by clocks and pocket watches, an unopened book beside him. |
| s03 | A large brass hourglass with sand running on an old wooden desk, torn calendar pages flying around it, candle light. |
| s04 | A frail elderly man in a worn coat struggles up a steep old wooden staircase, gripping the railing. |
| s05 | An ancient Roman stoic philosopher with a short beard, in a toga, writing on a scroll by oil lamp light, columns behind. |
| s06 | A focused young man reads and takes notes at a wooden desk by an oil lamp near a window at early dawn, stacks of books. |
| s07 | Close-up of a young man's hands planting a small sapling in dark soil, morning light. |
| s08 | A healthy upright elderly man with white hair and a walking stick strides along a mountain path, wide valley behind, hopeful light. |
| s09 | A warm smiling elderly man teaches a young child to read from a large book in a cozy study. |
| s10 | Close-up of an open antique pocket watch resting in an open palm, chain hanging, no numbers on the face. |

> Canva에 이미 s01, s02, s03이 생성돼 있습니다 (Canva 업로드 목록에서 내려받기).

## 조립
그림을 `shorts2/images/s01.png` ~ `s10.png`(jpg도 가능)로 넣고 `python3 shorts2/build.py` 실행 → `shorts2/shorts2.mp4`.
그림이 없는 컷은 세피아 종이 배경으로 대체됩니다.
