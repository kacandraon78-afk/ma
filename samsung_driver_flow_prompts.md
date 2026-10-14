# 삼성 임원 운전기사 쇼츠 · Flow(Google) 이미지 프롬프트

사용법
- Flow에서 비율 **9:16(세로)** 로 생성. 컷마다 [공통 스타일]을 맨 앞에 붙여서 넣으면 인물·톤이 일관됩니다.
- 첫 컷에서 마음에 드는 인물 이미지를 고른 뒤, 이후 컷은 그 이미지를 참조(Ingredients/레퍼런스)로 지정하세요.
- 영상 자막은 이미 들어 있으므로 이미지에는 **글자·로고가 나오지 않게** 했습니다(AI는 글자를 자주 깨뜨림).
- 실제 기업 로고·건물·실존 인물은 피했습니다(분쟁 방지). 이미지 위에 자막은 편집에서 얹으세요.

## 공통 스타일 (모든 컷 앞에 붙이기)
```
Cinematic vertical 9:16 photo, gritty documentary realism, moody low-key lighting, shallow depth of field, film grain, muted teal and amber color grade, 35mm lens. Main character: a tired Korean man in his late 40s, short black hair, dark suit, white driving gloves, kind but exhausted eyes. No text, no logos, no watermark.
```

## 컷별 프롬프트 (영상 순서와 동일)

**01 · 0~4초 훅 — "삼성 임원 운전기사 12년"**
```
[공통 스타일] Pre-dawn empty Seoul road, a black luxury sedan with glowing headlights parked in front of a glass skyscraper, the driver stands beside the open rear door in a crisp suit and white gloves, breath visible in the cold air, dramatic backlight, ominous quiet mood.
```

**02 · 4~10초 — 새벽 4~5시 기상 / 밤 11~12시 퇴근**
```
[공통 스타일] Split composition: top half a bedroom alarm clock showing 4:00 AM in a dark room, bottom half the same man washing a black sedan in an underground garage under harsh fluorescent light, exhausted expression, water drops, clock motif.
```

**03 · 10~15초 — 주말 새벽 골프장 수행**
```
[공통 스타일] Misty golf course clubhouse at 4 AM before sunrise, the driver standing alone holding a golf bag next to a luxury sedan, a wealthy silhouette in golf attire walking away in the fog, cold blue light, feeling of being invisible.
```

**04 · 15~20초 — 아이들 크는 모습 / 주말 여행 못 감**
```
[공통 스타일] Warm window light, an empty family dining table with a child's drawing and a small suitcase never opened, in the dark window reflection the driver in his car looks at his phone showing a blurred family photo, bittersweet, lonely.
```

**05 · 20~26초 — 2018.11 정규직 전환 (기대)**
```
[공통 스타일] The driver holding a company ID badge (blank, no logo) with a hopeful faint smile, golden hour light on his face, blurred modern corporate lobby behind him, a brief moment of hope, warm color grade.
```

**06 · 26~33초 — 급여 그대로 / 호칭 여전히 "기사"**
```
[공통 스타일] Corporate hallway, two rows of employees in smart casual lanyards walking past while the driver in a suit and white gloves stands to the side by the wall, nobody looks at him, cold desaturated light, sense of invisible hierarchy.
```

**07 · 33~39초 — 주말 15~17시간 근무, 수당은 12시간만**
```
[공통 스타일] Dashboard clock showing 11:40 PM, the driver slumped slightly at the wheel of a parked luxury sedan, eyes red, city lights bokeh through the windshield, empty coffee cup, extreme fatigue, cinematic close-up.
```

**08 · 39~44초 — 인상 요구 거절 / 노조·소송**
```
[공통 스타일] Dim HR office, the driver sits across a polished desk from a faceless official in a suit (face out of frame), a rejected paper form slid back across the desk, tense low-angle shot, cold fluorescent light, powerless feeling.
```

**09 · 44~50초 — 성과급 7억 5천 vs 시간당 수당 7,500원 (대비 컷)**
```
[공통 스타일] Strong split-screen contrast: left side a glamorous gold-lit executive boardroom with towers of cash and champagne, right side the driver alone in a dark car in the rain holding a few coins in his gloved palm, dramatic color contrast gold vs cold blue.
```

**10 · 50~55초 — 엔딩 (질문 던지기)**
```
[공통 스타일] The driver stands on a bridge at dawn facing the camera, direct eye contact, determined but tired expression, sunrise breaking over the city skyline behind him, hopeful yet unresolved, space left in the lower third for subtitles.
```

## 썸네일용 (9:16)
```
[공통 스타일] Extreme dramatic contrast thumbnail: top half a golden glowing mountain of cash and a luxury boardroom, bottom half a lonely driver in white gloves staring at the camera in a dark car, huge empty areas at top and bottom for large text, high contrast, bold saturated gold and red accents.
```

## 부정 프롬프트 (지원되면 입력)
```
text, letters, Korean characters, brand logos, watermark, distorted hands, extra fingers, cartoon, anime, overly bright smiling stock photo look
```

## Flow에서 영상으로 움직일 때 (선택, 컷당 4~6초)
- 01: slow push-in toward the driver, headlights flicker
- 03: slow pan following the walking silhouette into fog
- 07: slow zoom on tired eyes, city lights flicker
- 09: camera slides from the gold side to the cold blue side
- 10: slow push-in, sunrise light grows
