import random, math, subprocess, wave, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from tts import say

W, H = 1080, 1920
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
def F(s): return ImageFont.truetype(FONT, s)
BEIGE=(240,232,214); INK=(40,36,32); RED=(180,40,36); NAVY=(30,45,90)
random.seed(7)

def paper():
    im = Image.new("RGB",(W,H),BEIGE)
    n = Image.effect_noise((W,H),18).convert("RGB")
    im = Image.blend(im,n,0.05)
    v = Image.new("L",(W,H),0); d=ImageDraw.Draw(v)
    d.ellipse((-300,-300,W+300,H+300),fill=255); v=v.filter(ImageFilter.GaussianBlur(250))
    return Image.composite(im, Image.new("RGB",(W,H),(215,203,178)), v)

def center(d, y, text, font, fill=INK, w=W):
    bb = d.textbbox((0,0),text,font=font); d.text(((w-(bb[2]-bb[0]))/2,y),text,font=font,fill=fill)

def title(im, t):
    d=ImageDraw.Draw(im); center(d,150,t,F(70),INK)
    d.line((340,250,740,250),fill=RED,width=6)

def ink_mountains(task=None):
    im = Image.new("RGB",(W,H),(226,222,210))
    d = ImageDraw.Draw(im)
    for y in range(H):  # sky gradient with dawn glow
        t=y/H; c=int(232-30*t); d.line((0,y,W,y),fill=(c,c-3,c-12))
    glow=Image.new("L",(W,H),0); ImageDraw.Draw(glow).ellipse((300,500,780,980),fill=150)
    im.paste((246,236,205),mask=glow.filter(ImageFilter.GaussianBlur(120)))
    for i,(base,amp,shade) in enumerate([(900,260,150),(1150,230,110),(1400,200,70),(1650,160,35)]):
        pts=[(0,H)]; ph=random.random()*6
        for x in range(0,W+40,40):
            y=base-amp*abs(math.sin(x/230+ph+i))-60*math.sin(x/80+i)
            pts.append((x,y))
        pts.append((W,H))
        layer=Image.new("L",(W,H),0); ImageDraw.Draw(layer).polygon(pts,fill=255)
        layer=layer.filter(ImageFilter.GaussianBlur(3))
        im.paste((shade,shade,shade+4),mask=layer)
        mist=Image.new("L",(W,H),0); ImageDraw.Draw(mist).rectangle((0,base+40,W,base+160),fill=110)
        im.paste((235,232,222),mask=mist.filter(ImageFilter.GaussianBlur(60)))
    return im

def presenter(smile=False):
    im=Image.new("RGB",(W,H),(176,138,98)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,1100),fill=(205,178,140))                   # wall
    # window light
    d.rectangle((60,260,380,760),fill=(250,240,205)); d.line((220,260,220,760),fill=(150,120,85),width=8); d.line((60,510,380,510),fill=(150,120,85),width=8)
    # bookshelf
    d.rectangle((640,200,1040,1000),fill=(110,75,45))
    cols=[(150,60,50),(40,70,110),(200,170,90),(60,100,70),(120,90,140),(180,120,70)]
    for r in range(5):
        y=230+r*150; d.rectangle((650,y+110,1030,y+130),fill=(80,52,30))
        x=655
        while x<1015:
            w=random.randint(18,34); h=random.randint(70,105)
            d.rectangle((x,y+110-h,x+w,y+110),fill=random.choice(cols)); x+=w+3
    # frame art + plant
    d.rectangle((430,300,600,500),fill=(90,60,35)); d.rectangle((442,312,588,488),fill=(226,222,210)); d.polygon([(442,488),(500,380),(540,440),(570,400),(588,488)],fill=(110,110,110))
    d.rectangle((120,880,210,1000),fill=(130,90,60)); 
    for a in range(-50,60,25): d.ellipse((165+a*2-30,760-abs(a),165+a*2+30,900),fill=(60,110,60))
    # desk
    d.rectangle((0,1250,W,H),fill=(120,78,44)); d.rectangle((0,1250,W,1280),fill=(150,100,60))
    # figure
    d.polygon([(250,1300),(330,1010),(750,1010),(830,1300)],fill=NAVY)       # hanbok body
    d.polygon([(470,1010),(540,1130),(610,1010)],fill=(245,245,240))          # collar
    d.rectangle((500,930,580,1030),fill=(236,205,175))                        # neck
    d.ellipse((410,640,670,960),fill=(240,212,182))                            # face
    d.pieslice((395,600,685,930),180,360,fill=(205,205,212)); d.ellipse((395,650,440,860),fill=(205,205,212)); d.ellipse((640,650,685,860),fill=(205,205,212))
    for ex in (480,600): d.ellipse((ex-12,790,ex+12,806),fill=INK)
    if smile: d.arc((490,850,590,905),10,170,fill=(150,60,60),width=6)
    else: d.line((500,880,580,880),fill=(150,60,60),width=6)
    # arms + open book
    d.polygon([(250,1300),(330,1100),(420,1180),(420,1300)],fill=NAVY); d.polygon([(830,1300),(750,1100),(660,1180),(660,1300)],fill=NAVY)
    d.polygon([(330,1290),(540,1240),(540,1380),(330,1420)],fill=(235,225,195)); d.polygon([(540,1240),(750,1290),(750,1420),(540,1380)],fill=(245,236,210))
    for k in range(5): d.line((360,1305+k*20,520,1275+k*20),fill=(150,130,100),width=3); d.line((560,1275+k*20,720,1305+k*20),fill=(150,130,100),width=3)
    d.rectangle((0,1560,W,H),fill=(100,64,36))
    return im.filter(ImageFilter.GaussianBlur(1.2))

def slide_agenda():
    im=paper(); title(im,"오늘 확인할 3가지"); d=ImageDraw.Draw(im)
    for i,t in enumerate(["월살이 무엇인지","올해 해야 할 3가지 과제","조심할 달 · 기회의 달"]):
        y=520+i*260; d.text((160,y-20),str(i+1),font=F(170),fill=RED); d.text((330,y+30),t,font=F(64),fill=INK)
        d.line((330,y+140,930,y+140),fill=(190,175,150),width=3)
    return im

def slide_wheel():
    im=paper(); title(im,"삼합(三合)으로 보는 월살"); d=ImageDraw.Draw(im)
    cx,cy,R=540,800,330; names=["자","축","인","묘","진","사","오","미","신","유","술","해"]
    hi={1:"소",5:"뱀",9:"닭"}
    pos={}
    for i,n in enumerate(names):
        a=math.radians(-90+i*30); x=cx+R*math.cos(a); y=cy+R*math.sin(a); pos[i]=(x,y)
    tri=[pos[1],pos[5],pos[9]]; d.polygon(tri,outline=RED,width=8)
    d.ellipse((cx-R-70,cy-R-70,cx+R+70,cy+R+70),outline=(160,145,120),width=4)
    for i,n in enumerate(names):
        x,y=pos[i]; on=i in hi; r=62 if on else 48
        d.ellipse((x-r,y-r,x+r,y+r),fill=RED if on else (225,215,190),outline=INK,width=3)
        center_t=n; f=F(56 if on else 44); bb=d.textbbox((0,0),n,font=f)
        d.text((x-(bb[2]-bb[0])/2,y-(bb[3]-bb[1])/2-6),n,font=f,fill=(255,255,255) if on else INK)
    center(d,1260,"금(金) 삼합: 소 · 뱀 · 닭",F(60),RED)
    center(d,1345,"2027 정미년 = 미(未)의 해",F(52),INK)
    return im

def ink_real():
    return Image.open('../flow_assets/ink_task.jpg').convert('RGB').resize((W,H),Image.LANCZOS)
def slide_tasks():
    im=ink_real(); d=ImageDraw.Draw(im)
    box=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(box); bd.rounded_rectangle((70,180,1010,900),30,fill=(246,240,225,225))
    im.paste(box,(0,0),box); d=ImageDraw.Draw(im); center(d,230,"올해의 과제",F(78),RED)
    for i,t in enumerate(["새로 벌이기보다 기초 다지기","불필요한 약속 · 지출 정리","몸과 마음의 리듬 챙기기"]):
        y=400+i*160; d.rectangle((130,y,200,y+70),outline=INK,width=6); d.line((140,y+36,165,y+60),fill=RED,width=8); d.line((165,y+60,205,y-5),fill=RED,width=8)
        d.text((240,y+2),t,font=F(52),fill=INK)
    return im

def slide_calendar():
    im=paper(); title(im,"2027 정미년 달력"); d=ImageDraw.Draw(im)
    caution={7}; chance={4,8,12}
    for m in range(12):
        r,c=divmod(m,3); x=110+c*300; y=340+r*250
        fill=(226,150,140) if (m+1) in chance else ((120,115,110) if (m+1) in caution else (228,218,194))
        d.rounded_rectangle((x,y,x+260,y+220),24,fill=fill,outline=INK,width=3)
        tc=(255,255,255) if (m+1) in caution else INK
        center_x=x+130; t=f"{m+1}월"; bb=d.textbbox((0,0),t,font=F(64)); d.text((center_x-(bb[2]-bb[0])/2,y+70),t,font=F(64),fill=tc)
    d.rectangle((150,1330,210,1380),fill=(226,150,140)); d.text((230,1325),"기회의 달",font=F(46),fill=INK)
    d.rectangle((560,1330,620,1380),fill=(120,115,110)); d.text((640,1325),"조심할 달",font=F(46),fill=INK)
    return im

def slide_cards():
    im=paper(); title(im,"띠별 한 줄 조언"); d=ImageDraw.Draw(im)
    for i,(a,b) in enumerate([("뱀띠","서두르지 않기"),("닭띠","말을 아끼기"),("소띠","정리하고 비우기")]):
        y=340+i*370; d.rounded_rectangle((100,y,980,y+320),30,fill=(246,240,225),outline=INK,width=3)
        d.ellipse((150,y+60,350,y+260),fill=RED); bb=d.textbbox((0,0),a,font=F(64)); d.text((250-(bb[2]-bb[0])/2,y+130),a,font=F(64),fill=(255,255,255))
        d.text((400,y+120),b,font=F(66),fill=INK)
    return im

def outro():
    im=ink_real(); box=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(box).rounded_rectangle((90,300,990,760),30,fill=(246,240,225,225))
    im.paste(box,(0,0),box); d=ImageDraw.Draw(im)
    center(d,360,"구독 · 댓글 · 알림 설정",F(70),RED); center(d,500,"태어난 해를 댓글로 남겨 주세요",F(52),INK); center(d,600,"다음 이야기도 함께해요",F(52),INK)
    return im
SCENES=[
 (slide_agenda(),["오늘은 세 가지만 확인합니다.","월살이 무엇인지, 올해 해야 할 과제, 그리고 조심할 달과 기회의 달입니다."]),
 (slide_wheel(),["뱀 닭 소는 금의 기운으로 묶이는 삼합입니다.","이 팀에게 정미년의 미는 특정 신살 자리에 해당해서 월살이 됩니다.","쉽게 말해, 한 해의 흐름을 천천히 다지라는 신호예요."]),
 (slide_tasks(),["첫째, 무리하게 새로 벌이기보다 기초를 다지세요.","둘째, 불필요한 약속과 지출을 정리하세요.","셋째, 몸과 마음의 리듬을 먼저 챙기세요."]),
 (slide_calendar(),["조심할 달은 일정이 빡빡해지기 쉬운 칠월, 기회의 달은 같은 팀 기운이 모이는 달입니다.","미뤄 둔 부탁이나 약속은 기회의 달에 하세요."]),
 (slide_cards(),["뱀띠는 서두르지 않기, 닭띠는 말을 아끼기, 소띠는 정리하고 비우기.","이 정도만 기억해도 충분합니다."]),
 (outro(),["사람의 일을 다하고 하늘의 뜻을 기다리라는 말이 있죠.","댓글에 태어난 해를 남겨 주시면 확인해 드릴게요.","구독하고 다음 이야기도 함께하세요."]),
]
SUB=[ # on-screen subtitle text (same as narration, spoken numerals replaced)
]
def subtitle(im, text):
    im=im.copy().convert("RGBA"); ov=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    f=F(54); lines=[]; cur=""
    for ch in text:
        if d.textlength(cur+ch,font=f)>900 and ch!=" ": lines.append(cur); cur=ch
        else: cur+=ch
    lines.append(cur); h=len(lines)*76+50; y0=1500
    d.rounded_rectangle((60,y0,1020,y0+h),24,fill=(0,0,0,170))
    for i,l in enumerate(lines):
        bb=d.textbbox((0,0),l,font=f); d.text(((W-(bb[2]-bb[0]))/2,y0+25+i*76),l,font=f,fill=(255,255,255))
    return Image.alpha_composite(im,ov).convert("RGB")

os.makedirs("frames",exist_ok=True); os.makedirs("audio",exist_ok=True)
segs=[]; n=0
for si,(img,lines) in enumerate(SCENES):
    for li,t in enumerate(lines):
        wav=f"audio/{n:02d}.wav"; dur=say(t,wav,rate=125,pitch=50)+0.35
        subtitle(img,t).save(f"frames/{n:02d}.png"); segs.append((n,dur)); n+=1
with open("list.txt","w") as f:
    for n,dur in segs: f.write(f"file 'frames/{n:02d}.png'\nduration {dur:.3f}\n")
    f.write(f"file 'frames/{segs[-1][0]:02d}.png'\n")
with open("alist.txt","w") as f:
    for n,dur in segs: f.write(f"file 'audio/{n:02d}.wav'\n")
# pad each wav to its segment duration
for n,dur in segs:
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"audio/{n:02d}.wav","-af",f"apad=pad_dur=0.35","-t",f"{dur:.3f}",f"audio/p{n:02d}.wav"],check=True)
with open("alist.txt","w") as f:
    for n,dur in segs: f.write(f"file 'audio/p{n:02d}.wav'\n")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i","list.txt","-f","concat","-i","alist.txt","-vf","fps=30,format=yuv420p","-c:v","libx264","-c:a","aac","-b:a","128k","-shortest","part2.mp4"],check=True)
print("total", sum(d for _,d in segs))
