# Google Flow 제작 가이드: 정미년 월살 쇼츠

`storyboard_wolsal_shorts.md`의 장면 구성을 Flow(Veo)에서 만들기 위한 프롬프트입니다.
Flow에서 생성한 파일을 저장소의 `flow_assets/`에 올려 주시면 자막, 인포그래픽과 합쳐 최종 영상으로 조립합니다.

## 0. 공통 설정
- 화면 비율: **9:16 세로**
- 클립 길이: 한 클립 약 8초(Veo 한도). 대사가 길면 클립을 나눕니다.
- 진행자 외형은 모든 클립에서 동일하게 유지해야 합니다. **1번 이미지를 먼저 만들고, 이후 클립은 그 이미지를 "Frames to Video"(첫 프레임)로 지정**하세요.

## 1. 진행자 기준 이미지 (먼저 생성)
파일명: `presenter_base.png`

```
A realistic photo of a mature Korean woman in her 60s with short wavy silver hair, light complexion, gentle expression, wearing a dark navy traditional Korean hanbok with a white collar. She sits at a large wooden desk with her hands resting on an old open book. Background: a bookshelf full of books, a potted plant on the left, a framed ink-wash artwork on the wall. Soft natural window light from the left, warm earthy wooden tones, medium shot, vertical 9:16, photorealistic.
```

## 2. 진행자 영상 클립 (Frames to Video, 시작 프레임 = presenter_base.png)

공통 프롬프트 앞부분(모든 클립에 동일하게 붙이세요):
```
The same woman speaks directly to the camera in natural Korean with calm, warm expression and slight hand gestures. Static camera, same room, same lighting. She says in Korean:
```

| 파일명 | 대사 |
|--------|------|
| `clip1a.mp4` | "이천이십칠년 정미년, 뱀띠, 닭띠, 소띠에게는 월살이 찾아옵니다." |
| `clip1b.mp4` | "이름이 낯설고 무겁게 들리죠? 하지만 겁먹을 일이 아닙니다." |
| `clip1c.mp4` | "끝까지 보시면 태어난 해별 한 줄 조언도 드려요." |
| `clip7a.mp4` | "사람의 일을 다하고 하늘의 뜻을 기다리라는 말이 있죠." |
| `clip7b.mp4` | "댓글에 태어난 해를 남겨 주시면 확인해 드릴게요. 구독하고 다음 이야기도 함께하세요." (마지막은 따뜻하게 미소) |

> 한국어 립싱크 품질이 부족하면, 영상은 무음(말하는 입 모양만)으로 받고 음성은 별도로 입히는 방법도 있습니다. 결과를 보고 알려 주세요.

## 3. 수묵화 배경 이미지 (Image 생성, 9:16)

`ink_task.png` (장면 4, 과제 3개 배경)
```
Traditional Korean ink wash painting of misty mountains at dawn, rays of sunlight breaking through clouds, a small village in the valley, monochrome black and grey with soft brown tones, high contrast, serene mood, empty space in the upper half for text overlay, vertical 9:16.
```

`ink_extra.png` (선택, 오프닝 전환용)
```
Traditional ink wash landscape of misty mountains with gnarled pine trees, soft diffused light, black grey and soft brown, tranquil, vertical 9:16.
```

## 4. 인포그래픽
도표·달력·카드는 글자 정확도가 중요해서 Flow가 아니라 **제가 코드로 만든 슬라이드**를 그대로 씁니다(`video_build/build.py`). 별도 작업 필요 없습니다.

## 5. 올려 주실 파일
`flow_assets/` 폴더에 위 파일명 그대로 저장소에 올려 주세요.
- 진행자: `clip1a.mp4`, `clip1b.mp4`, `clip1c.mp4`, `clip7a.mp4`, `clip7b.mp4`
- 배경: `ink_task.png`
- (선택) `presenter_base.png`, `ink_extra.png`

올려 주시면 진행자 클립과 슬라이드를 순서대로 이어 붙이고, 슬라이드 구간의 나레이션은 기존 음성으로 채워 조립하겠습니다. 클립의 음성이 마음에 들면 슬라이드 구간 음성도 같은 톤으로 맞추는 방법을 함께 찾아보겠습니다.
