import os, tempfile, random, math
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import ImageDraw, ImageFont
import numpy as np

print("=== V11 ANIMATED BLUE CAT PERFORMING - MOVING CHARACTER ===")

story = "Stop scrolling! This is the one hundred thousand dollar challenge that broke the internet! You must beat three impossible tasks! Basketball, football, and a puzzle! Fail one and you lose everything! The pressure was insane! But I found the trick top creators use to win! Watch till the last ten seconds! Comment what you think happened! Follow for Part 2! Subscribe now!"

tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story, lang='en', slow=False).save(tmp_mp3)
tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
os.system(f"ffmpeg -y -i {tmp_mp3} {tmp_wav} -loglevel quiet")
audio = AudioFileClip(tmp_wav) if os.path.exists(tmp_wav) and os.path.getsize(tmp_wav)>1000 else AudioFileClip(tmp_mp3)
print(f"Audio: {audio.duration:.2f}s")

W, H = 1080, 1920

def make_cinematic_bg(title, idx):
    img = Image.new('RGB', (W, H), (10,10,25))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        base = [(12,12,28), (25,15,40), (20,25,50), (35,20,35)][idx % 4]
        r = int(base[0] + (y/H)*35)
        g = int(base[1] + (y/H)*25)
        b = int(base[2] + (y/H)*55)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Vignette
    for i in range(120):
        alpha = int(80 * (1 - i/120))
        draw.rectangle([0, i, W, i+1], fill=(0,0,0))
        draw.rectangle([0, H-120+i, W, H-120+i+1], fill=(0,0,0))
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font
    y = 180
    for j, line in enumerate(title.split("\n")):
        bbox = draw.textbbox((0,0), line, font=title_font)
        w = bbox[2]-bbox[0]
        for ox in [-6,-4,0,4,6]:
            for oy in [-6,-4,0,4,6]:
                if abs(ox)+abs(oy) > 1:
                    draw.text(((W-w)//2+ox, y+oy), line, font=title_font, fill=(0,0,0))
        fill = (255,225,0) if j==0 else (255,255,255)
        draw.text(((W-w)//2, y), line, font=title_font, fill=fill)
        y += 170
    draw.rounded_rectangle([60, y+20, W-60, y+30], radius=5, fill=(255,30,80))
    y += 80
    for chunk in ["VIRAL CHALLENGE"]:
        bbox = draw.textbbox((0,0), chunk, font=sub_font)
        w = bbox[2]-bbox[0]
        draw.rounded_rectangle([(W-w)//2-30, y-10, (W+w)//2+30, y+65], radius=25, fill=(0,0,0))
        draw.text(((W-w)//2, y), chunk, font=sub_font, fill=(255,255,255))
        y += 85
    return np.array(img)

titles = ["STOP!\n$100K\nON LINE!", "3 TASKS\nMUST WIN!", "SECRET\nREVEALED!", "COMMENT!"]
cat_map = {
    0: ["assets/blue_cat_shocked_pro.png", "blue_cat_shocked_pro.png", "/mnt/data/blue_cat_shocked_pro.png"],
    1: ["assets/blue_cat_thinking_pro.png", "blue_cat_thinking_pro.png", "/mnt/data/blue_cat_thinking_pro.png"],
    2: ["assets/blue_cat_happy_pro.png", "blue_cat_happy_pro.png", "/mnt/data/blue_cat_happy_pro.png"],
    3: ["assets/blue_cat_happy_pro.png", "blue_cat_happy_pro.png", "/mnt/data/blue_cat_happy_pro.png"],
}
def find_cat(idx):
    for p in cat_map[idx]:
        if os.path.exists(p):
            return p
    for paths in cat_map.values():
        for p in paths:
            if os.path.exists(p):
                return p
    return None

clips = []
chapter_dur = audio.duration / len(titles)

for i, title in enumerate(titles):
    start = i * chapter_dur
    bg_img = make_cinematic_bg(title, i)
    bg_clip = ImageClip(bg_img, duration=chapter_dur).set_start(start)
    bg_clip = bg_clip.resize(lambda t: 1.02 + 0.03*(t/chapter_dur))
    clips.append(bg_clip)

    cat_path = find_cat(i)
    if cat_path:
        try:
            cat_clip = ImageClip(cat_path, duration=chapter_dur).set_start(start)
            # ANIMATED PERFORMING CHARACTER!
            if i == 0:  # SHOCKED - SHAKE + POP
                cat_clip = cat_clip.resize(lambda t: 0.85 + 0.15*abs(math.sin(t*8))).set_position(lambda t: (W-900 + math.sin(t*12)*30, H-1150 + math.cos(t*10)*20))
            elif i == 1:  # THINKING - TILT + BOUNCE
                cat_clip = cat_clip.resize(lambda t: 0.9 + 0.05*math.sin(t*2)).set_position(lambda t: (W-920 + math.sin(t*1.5)*15, H-1160 + math.sin(t*2.2)*25))
            elif i == 2:  # POINTING - JUMP + POINT
                cat_clip = cat_clip.resize(lambda t: 0.85 + 0.2*max(0, math.sin(t*3))).set_position(lambda t: (W-950, H-1150 - abs(math.sin(t*3))*80))
            else:  # HAPPY - DANCE!
                cat_clip = cat_clip.resize(lambda t: 0.9 + 0.1*abs(math.sin(t*4))).set_position(lambda t: (W-900 + math.sin(t*5)*40, H-1150 + math.cos(t*4)*30))
            clips.append(cat_clip)
            print(f"ANIMATED CAT {i}: {cat_path} performing!")
        except Exception as e:
            print(f"Cat fail {cat_path}: {e}")
    else:
        print(f"No cat {i}")

progress_bg = ColorClip(size=(W, 14), color=(255,255,255), duration=audio.duration).set_opacity(0.2).set_position((0, H-18))
progress_fill = ColorClip(size=(W, 14), color=(255,50,80), duration=audio.duration).set_position((0, H-18))
clips.append(progress_bg)
clips.append(progress_fill)

final = CompositeVideoClip(clips, size=(W,H)).set_audio(audio)
tmp_video="/tmp/short.mp4"
save_video="./short.mp4"
final.write_videofile(tmp_video,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None)
import shutil
shutil.copy(tmp_video, save_video)
print(f"ANIMATED VIDEO READY: {audio.duration:.2f}s - {os.path.getsize(save_video)} bytes")

CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
REFRESH_TOKEN=os.getenv("GOOGLE_REFRESH_TOKEN")
try:
    if CLIENT_ID and REFRESH_TOKEN:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
        creds=Credentials(None,refresh_token=REFRESH_TOKEN,token_uri="https://oauth2.googleapis.com/token",client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scopes=['https://www.googleapis.com/auth/youtube.upload'])
        youtube=build('youtube','v3',credentials=creds)
        req=youtube.videos().insert(part="snippet,status",body={"snippet":{"title":f"{titles[0].replace(chr(10),' ')} #shorts","description":f"{story} #shorts #viral Animated Blue Cat","tags":["shorts","viral","bluecat"],"categoryId":"22"},"status":{"privacyStatus":"private","selfDeclaredMadeForKids":False}},media_body=MediaFileUpload(tmp_video,mimetype='video/mp4',resumable=True))
        resp=req.execute()
        print(f"SUCCESS! ANIMATED: https://youtu.be/{resp['id']}")
    else:
        print("No secrets")
except Exception as e:
    err=str(e)
    if "uploadLimitExceeded" in err or "exceeded" in err:
        print("YOUTUBE LIMIT HIT - VIDEO SAVED FOR DOWNLOAD!")
    else:
        print(f"Upload err: {e}")

print("DONE V11 ANIMATED PERFORMING")
