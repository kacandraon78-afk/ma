"""완성본용 그림 10장 생성: 사용자 소재(Flow 노인 클립, 수묵화) + 코드로 그린 사물 → 공통 세피아 펜화 필터."""
import os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
W, H = 1080, 1920
CLIP = "../flow_assets/clip_old_man.mp4"
INK = "../flow_assets/ink_task.jpg"
os.makedirs("images", exist_ok=True); os.makedirs("build", exist_ok=True)
rng = np.random.default_rng(7)

# ---------- 공통 펜화(인그레이빙) 필터 ----------
yy, xx = np.mgrid[0:H, 0:W]
P1 = ((xx + yy) % 8) < 2
P2 = ((xx - yy) % 8) < 2
P3 = (yy % 6) < 2
P4 = ((xx + 2 * yy) % 7) < 2
def engrave(gray_img, edge_gain=1.0):
    g = np.asarray(gray_img.convert("L").resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2)), float) / 255
    ink = (g < 0.80) & P1
    ink |= (g < 0.58) & P2
    ink |= (g < 0.38) & P3
    ink |= (g < 0.20) & P4
    ink |= g < 0.08
    e = np.asarray(gray_img.convert("L").resize((W, H)).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(0.8)), float) / 255
    ink |= e * edge_gain > 0.16
    paper = np.array([238, 222, 186.0]) + rng.normal(0, 6, (H, W, 1))
    d = np.hypot((xx - W / 2) / W, (yy - H / 2) / H)
    paper *= (1 - 0.55 * d ** 1.8)[..., None]
    tone = paper * (0.55 + 0.45 * g[..., None])            # 세피아 명암
    out = np.where(ink[..., None], np.array([62, 42, 22.0]), tone)
    out = 0.82 * out + 0.18 * tone
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))

# ---------- 그리기 도우미 (회색조 + 조명) ----------
def canvas(bg=95):
    im = Image.new("L", (W, H), bg)
    return im, ImageDraw.Draw(im)
def glow(im, cx, cy, r, amt):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=amt)
    m = m.filter(ImageFilter.GaussianBlur(r * 0.45))
    return Image.fromarray(np.clip(np.asarray(im, int) + np.asarray(m, int), 0, 255).astype("uint8"))
def shade_ellipse(d, box, light, dark, steps=24):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / steps; c = int(dark + (light - dark) * t)
        dx = (x1 - x0) * t * 0.35; dy = (y1 - y0) * t * 0.35
        d.ellipse((x0 + dx * 0.6, y0 + dy * 0.6, x1 - dx * 1.4, y1 - dy * 1.4), fill=c)
def table(d, top=1350, c=60):
    d.rectangle((0, top, W, H), fill=c); d.rectangle((0, top, W, top + 30), fill=c + 35)
    for k in range(12): d.line((0, top + 60 + k * 45, W, top + 70 + k * 45), fill=c - 15, width=3)
def clock(d, cx, cy, r, h1=-60, h2=40):
    shade_ellipse(d, (cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18), 120, 35)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=225, outline=40, width=5)
    for k in range(12):
        a = math.radians(k * 30); d.line((cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82,
                                          cx + math.cos(a) * r * 0.95, cy + math.sin(a) * r * 0.95), fill=30, width=6)
    for ang, ln, w in ((h1, 0.5, 10), (h2, 0.75, 6)):
        a = math.radians(ang - 90); d.line((cx, cy, cx + math.cos(a) * r * ln, cy + math.sin(a) * r * ln), fill=20, width=w)
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=20)

# ---------- 장면 ----------
def frame_at(t, crop=0.88):
    p = f"build/clip_{t}.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", CLIP, "-frames:v", "1", p], check=True)
    im = Image.open(p); w, h = im.size
    return im.crop((0, 0, int(w * crop), int(h * crop)))   # 오른쪽 아래 Flow 로고 제거

def zoom(im, box):
    w, h = im.size; x0, y0, x1, y1 = box
    c = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))); cw, ch = c.size
    tw = int(ch * W / H)
    if tw <= cw: return c.crop(((cw - tw) // 2, 0, (cw - tw) // 2 + tw, ch))
    th = int(cw * H / W); return c.crop((0, (ch - th) // 2, cw, (ch - th) // 2 + th))

def s02_clocks():
    im, d = canvas(110)
    d.rectangle((0, 0, W, 1450), fill=120)
    for k in range(10): d.line((k * 115, 0, k * 115, 1450), fill=105, width=4)   # 벽 판자
    im = glow(im, 250, 500, 420, 60); d = ImageDraw.Draw(im)
    for (cx, cy, r, a, b) in [(270, 720, 150, -40, 120), (760, 640, 120, 30, 200), (540, 1020, 105, 90, -20),
                              (850, 1080, 85, 150, 60), (230, 1130, 80, -100, 10)]:
        clock(d, cx, cy, r, a, b)
    # 괘종시계
    d.rectangle((470, 300, 610, 820), fill=50); d.rectangle((488, 520, 592, 800), fill=150)
    d.line((540, 520, 520, 760), fill=40, width=5); d.ellipse((498, 740, 542, 784), fill=60)
    clock(d, 540, 400, 60, 10, 140)
    table(d, 1450, 55)
    for (cx, cy) in [(300, 1600), (700, 1560)]:                                   # 바닥의 회중시계
        d.ellipse((cx - 70, cy - 40, cx + 70, cy + 40), fill=200, outline=40, width=6)
    return im

def s03_hourglass():
    im, d = canvas(70)
    im = glow(im, 820, 760, 360, 110); d = ImageDraw.Draw(im)
    table(d, 1350, 50)
    cx = 540
    d.rectangle((cx - 230, 560, cx + 230, 610), fill=80); d.rectangle((cx - 230, 1290, cx + 230, 1340), fill=70)
    for x in (cx - 205, cx + 185): d.rectangle((x, 610, x + 20, 1290), fill=60)
    d.polygon([(cx - 170, 620), (cx + 170, 620), (cx + 20, 950), (cx - 20, 950)], fill=200)
    d.polygon([(cx - 20, 950), (cx + 20, 950), (cx + 170, 1280), (cx - 170, 1280)], fill=205)
    d.polygon([(cx - 110, 760), (cx + 110, 760), (cx + 14, 935), (cx - 14, 935)], fill=120)     # 위 모래
    d.polygon([(cx - 165, 1280), (cx + 165, 1280), (cx + 40, 1150), (cx - 40, 1150)], fill=115)  # 아래 모래
    d.line((cx, 950, cx, 1150), fill=120, width=5)
    for (x, y, a) in [(160, 700, 20), (880, 500, -30), (220, 1100, -15), (930, 1150, 35), (120, 420, 40), (800, 1230, 10)]:
        pg = Image.new("L", (190, 240), 225); ImageDraw.Draw(pg).rectangle((0, 0, 189, 239), outline=60, width=4)
        for k in range(6): ImageDraw.Draw(pg).line((20, 40 + k * 30, 170, 40 + k * 30), fill=150, width=3)
        pg = pg.rotate(a, expand=True, fillcolor=0); m = pg.point(lambda v: 255 if v > 0 else 0)
        im.paste(pg, (x - pg.width // 2, y - pg.height // 2), m)
    d = ImageDraw.Draw(im); d.rectangle((790, 980, 840, 1340), fill=225); d.ellipse((800, 920, 830, 985), fill=255)   # 촛불
    return im

def s05_scroll():
    im, d = canvas(65)
    im = glow(im, 760, 900, 420, 120); d = ImageDraw.Draw(im)
    for x in (90, 920): d.rectangle((x, 0, x + 90, 1300), fill=110); d.rectangle((x - 20, 0, x + 110, 60), fill=130)  # 기둥
    table(d, 1250, 55)
    d.polygon([(170, 1180), (820, 1180), (880, 1420), (110, 1420)], fill=220)                     # 펼친 두루마리
    for y in (1180, 1420): d.ellipse((90, y - 30, 190, y + 30), fill=170); d.ellipse((810, y - 30, 900, y + 30), fill=170)
    for k in range(7): d.line((220, 1220 + k * 28, 760, 1220 + k * 28), fill=120, width=4)
    d.line((640, 1300, 900, 900), fill=40, width=6)                                                # 깃펜
    d.polygon([(900, 900), (980, 760), (1000, 790), (930, 920)], fill=200)
    d.ellipse((700, 1060, 860, 1140), fill=90); d.polygon([(760, 1060), (800, 1060), (790, 990), (770, 990)], fill=250)  # 등잔
    return im

def s06_book_dawn():
    im, d = canvas(60)
    d.rectangle((560, 220, 1000, 1000), fill=235)                                                   # 새벽 창
    d.line((780, 220, 780, 1000), fill=60, width=14); d.line((560, 610, 1000, 610), fill=60, width=14)
    im = glow(im, 780, 610, 520, 70); d = ImageDraw.Draw(im)
    table(d, 1200, 50)
    for k in range(5): d.rectangle((90, 1130 - k * 60, 420 - k * 10, 1190 - k * 60), fill=90 + k * 25, outline=30, width=4)  # 책더미
    d.polygon([(330, 1300), (560, 1250), (560, 1480), (300, 1520)], fill=220); d.polygon([(560, 1250), (800, 1300), (830, 1520), (560, 1480)], fill=235)
    for k in range(7):
        d.line((350, 1320 + k * 25, 540, 1280 + k * 25), fill=130, width=3); d.line((580, 1280 + k * 25, 780, 1320 + k * 25), fill=130, width=3)
    d.ellipse((800, 1080, 960, 1180), fill=80); d.rectangle((850, 900, 910, 1090), fill=210); d.ellipse((855, 860, 905, 920), fill=255)
    return glow(im, 880, 900, 200, 60)

def s07_sapling():
    im, d = canvas(170)
    im = glow(im, 540, 400, 600, 60); d = ImageDraw.Draw(im)
    d.ellipse((-200, 1150, W + 200, 2300), fill=55)                                               # 흙
    for k in range(400):
        x, y = rng.integers(0, W), rng.integers(1200, H); d.ellipse((x, y, x + 8, y + 6), fill=int(rng.integers(30, 90)))
    d.line((540, 1240, 540, 820), fill=50, width=16)
    def leaf(cx, cy, ang, L, Wd):
        r = math.radians(ang); pts = []
        for k in range(40):
            t = k / 39 * 2 * math.pi; x = (math.cos(t) + 1) / 2 * L; y = math.sin(t) * Wd / 2
            pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
        d.polygon(pts, fill=205, outline=70)
        d.line((cx, cy, cx + L * math.cos(r), cy + L * math.sin(r)), fill=90, width=4)
    for (y, ang, L) in [(830, -150, 230), (830, -30, 230), (930, -160, 200), (930, -20, 200), (1040, -165, 160), (1040, -15, 160)]:
        leaf(540, y, ang, L, L * 0.42)
    d = ImageDraw.Draw(im)
    d.polygon([(760, 1250), (960, 1250), (940, 1450), (780, 1450)], fill=110); d.line((960, 1290, 1060, 1200), fill=90, width=22)   # 물뿌리개
    return im

def s10_watch():
    im, d = canvas(50)
    im = glow(im, 540, 900, 520, 90); d = ImageDraw.Draw(im)
    d.ellipse((140, 1100, 940, 1800), fill=150)                                                    # 손바닥
    for k, x in enumerate((180, 330, 480, 630)): d.rounded_rectangle((x, 1500, x + 130, 1900), 60, fill=140 - k * 5)
    shade_ellipse(d, (250, 640, 830, 1220), 210, 60)
    d.ellipse((290, 680, 790, 1180), fill=230, outline=40, width=8)
    for k in range(60):
        a = math.radians(k * 6); r1 = 225 if k % 5 else 200
        d.line((540 + math.cos(a) * r1, 930 + math.sin(a) * r1, 540 + math.cos(a) * 240, 930 + math.sin(a) * 240), fill=40, width=5 if k % 5 == 0 else 2)
    d.line((540, 930, 540, 780), fill=20, width=10); d.line((540, 930, 650, 1010), fill=20, width=7); d.ellipse((528, 918, 552, 942), fill=20)
    d.rectangle((510, 560, 570, 640), fill=110); d.ellipse((490, 500, 590, 580), outline=60, width=12)
    for k in range(14): d.ellipse((520 + k * 9, 470 - k * 30, 560 + k * 9, 500 - k * 30), outline=70, width=8)   # 체인
    return im

def s08_ink():
    im = Image.open(INK).convert("L"); w, h = im.size; s = max(W / w, H / h)
    im = im.resize((int(w * s) + 1, int(h * s) + 1)); l = (im.width - W) // 2
    return im.crop((l, 0, l + W, H))

scenes = {
    "s01": lambda: frame_at(0.5),
    "s02": s02_clocks,
    "s03": s03_hourglass,
    "s04": lambda: zoom(frame_at(3.0), (0.05, 0.22, 0.72, 0.72)),
    "s05": s05_scroll,
    "s06": s06_book_dawn,
    "s07": s07_sapling,
    "s08": s08_ink,
    "s09": lambda: zoom(frame_at(9.0), (0.12, 0.10, 0.88, 0.62)),
    "s10": s10_watch,
}
for k, f in scenes.items():
    engrave(f(), edge_gain=1.3 if k in ("s01", "s04", "s09") else 1.0).save(f"images/{k}.png")
    print("ok", k)
