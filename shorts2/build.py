"""쇼츠 2 자동 조립: images/sNN.(png|jpg) + 자막 + 고정 제목 + 배경음 → shorts2.mp4"""
import os, subprocess, glob
import numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
W, H, FPS, CUT = 1080, 1920, 30, 4.0
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
TITLE = ["이 습관 하나가", "10년 뒤 인생을 바꾼다"]
CUTS = [
 ("s01", ["젊을 때 시간 쓰는 법이", "노후를 결정하는 진짜 이유"]),
 ("s02", ["지금은 시간이", "끝없이 남아 보인다"]),
 ("s02", ["오늘 못 하면", "내일 하면 된다고 믿는다"]),
 ("s03", ["그렇게 미룬 하루가", "한 달이 되고, 한 해가 된다"]),
 ("s03", ["하지만 세월은", "누구도 기다려 주지 않는다"]),
 ("s04", ["어느 날 몸이 먼저", "말을 듣지 않기 시작한다"]),
 ("s04", ["배우고 싶던 것도 가고 싶던 곳도", "이제는 버겁기만 하다"]),
 ("s01", ["'그때 해 둘 걸'", "그 후회가 가장 무겁다"]),
 ("s05", ["세네카는 말했다", "인생이 짧은 것이 아니라", "우리가 헛되이 쓸 뿐이라고"]),
 ("s06", ["젊은 날의 시간은", "쉬라고 주어진 것이 아니다"]),
 ("s07", ["미래의 나를 위해", "미리 심어 두라고 주어진 것이다"]),
 ("s06", ["하루 한 시간", "읽고, 걷고, 배우는 사람은"]),
 ("s08", ["십 년 뒤", "전혀 다른 곳에 서 있다"]),
 ("s09", ["젊어서 아낀 시간은", "늙어서 자유가 되어 돌아온다"]),
 ("s10", ["오늘의 한 시간을", "어디에 쓸지 정해 보라"]),
 ("s09", ["그 선택이", "10년 뒤 당신의 얼굴이 된다"]),
]
def F(s): return ImageFont.truetype(FONT, s)

def load_bg(key):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = f"images/{key}.{ext}"
        if os.path.exists(p):
            im = Image.open(p).convert("RGB"); w, h = im.size; s = max(W / w, H / h)
            im = im.resize((int(w * s + 1), int(h * s + 1)), Image.LANCZOS)
            l, t = (im.width - W) // 2, (im.height - H) // 2
            return ImageEnhance.Brightness(im.crop((l, t, l + W, t + H))).enhance(0.92), True
    # 그림이 아직 없으면 세피아 종이 배경
    rng = np.random.default_rng(abs(hash(key)) % 2**32)
    base = np.zeros((H, W, 3)) + np.array([196, 168, 120])
    base += rng.normal(0, 10, (H, W, 1))
    yy, xx = np.mgrid[0:H, 0:W]; d = np.hypot((xx - W / 2) / W, (yy - H / 2) / H)
    base *= (1 - 0.9 * d ** 1.6)[..., None]
    im = Image.fromarray(np.clip(base, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.5))
    return im, False

def text_block(d, lines, y, font, fill, stroke=6, gap=1.25):
    for i, l in enumerate(lines):
        bb = d.textbbox((0, 0), l, font=font, stroke_width=stroke)
        d.text(((W - (bb[2] - bb[0])) / 2, y + i * font.size * gap), l, font=font, fill=fill,
               stroke_width=stroke, stroke_fill=(15, 10, 5))

def frame(key, sub):
    im, real = load_bg(key); d = ImageDraw.Draw(im)
    text_block(d, TITLE, 110, F(84), (255, 214, 64), stroke=7)        # 고정 노란 제목
    f = F(64); top = 1180 - (len(sub) - 1) * 40
    text_block(d, sub, top, f, (255, 255, 255), stroke=6)               # 흰 자막
    if not real:
        ImageDraw.Draw(im).text((40, H - 70), f"[그림 {key} 자리]", font=F(34), fill=(90, 70, 45))
    return im

def end_card():
    im = Image.new("RGB", (W, H), (8, 8, 8)); d = ImageDraw.Draw(im)
    text_block(d, ["오늘의 한 문장"], 560, F(56), (255, 214, 64), stroke=0)
    text_block(d, ["“인생은 짧지 않다.", "우리가 짧게 쓸 뿐이다.”"], 720, F(72), (255, 255, 255), stroke=0, gap=1.4)
    text_block(d, ["— 세네카"], 960, F(48), (200, 200, 200), stroke=0)
    text_block(d, ["구독하고", "매일 한 문장 받아 가세요"], 1300, F(60), (255, 214, 64), stroke=4)
    return im

def music(sec, path):
    sr = 44100; t = np.arange(int(sr * sec)) / sr; y = np.zeros_like(t)
    def note(f, s, dur, a):
        env = np.clip((t - s) / 1.2, 0, 1) * np.clip((s + dur - t) / 1.8, 0, 1)
        return a * env * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t))
    y += note(55.0, 0, sec, 0.4) + note(82.41, 0, sec, 0.25)            # A 단조 드론
    chords = [(220, 261.63, 329.63), (174.61, 220, 261.63), (196, 246.94, 293.66), (164.81, 207.65, 246.94)]
    for i, x in enumerate(np.arange(0, sec, 4.0)):
        for f in chords[i % 4]: y += note(f, x, 4.6, 0.12)
    y *= np.clip(t / 2, 0, 1) * np.clip((sec - t) / 3, 0, 1); y /= np.abs(y).max()
    st = (np.stack([y, np.roll(y, 220)], 1) * 0.8 * 32767).astype("<i2")
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes()); w.close()

os.makedirs("build", exist_ok=True)
segs = [(frame(k, s), CUT) for k, s in CUTS] + [(end_card(), 5.0)]
for i, (im, dur) in enumerate(segs):
    im.save(f"build/c{i:02d}.png"); n = int(dur * FPS)
    z = f"min(1+0.05*on/{n},1.05)" if i < len(CUTS) else "1"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-i", f"build/c{i:02d}.png",
        "-vf", f"scale={W*2}:{H*2},zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps={FPS},format=yuv420p",
        "-frames:v", str(n), "-c:v", "libx264", "-crf", "21", f"build/c{i:02d}.mp4"], check=True)
open("build/list.txt", "w").write("".join(f"file 'c{i:02d}.mp4'\n" for i in range(len(segs))))
total = sum(d for _, d in segs); music(total, "build/bgm.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", "build/list.txt", "-i", "build/bgm.wav",
    "-af", "volume=0.35", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "shorts2.mp4"], check=True)
print(f"shorts2.mp4  {total:.0f}s  (그림 {len(glob.glob('images/s*'))}/10)")
