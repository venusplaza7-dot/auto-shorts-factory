import os, tempfile, random, math
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("=== V9.1 BEAUTIFUL FIXED ANTIALIAS BUG ===")

story = "Stop scrolling! This is the one hundred thousand dollar basketball challenge that broke the internet! You must beat three impossible tasks! Basketball, football, and a puzzle! Fail one and you lose everything! The pressure was insane! But I found the trick top creators use to win! Watch till the last ten seconds! Comment what you think happened! Follow for Part 2! Subscribe now!"
print(f"Words: {len(story.split())}")

# Voice
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story, lang='en', slow=False).save(tmp_mp3)
tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
os.system(f"ffmpeg -y -i {tmp_mp3} {tmp_wav} -loglevel quiet")
audio = AudioFileClip(tmp_wav) if os.path.exists(tmp_wav) and os.path.getsize(tmp_wav)>1000 else AudioFileClip(tmp_mp3)
print(f"Audio: {audio.duration:.2f}s")

W, H = 1080, 1920

def draw_blue_cat(pose="happy", size=600):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = size//2, size//2
    hood_colors = {"happy": (65,105,225), "thinking": (100,149,237), "shocked": (30,144,255), "pointing": (0,191,255)}
    hood = hood_colors.get(pose, (65,105,225))
    draw.ellipse([cx-180, cy-80, cx+180, cy+200], fill=hood)
    draw.polygon([(cx-140, cy-120), (cx-200, cy-200), (cx-80, cy-150)], fill=hood)
    draw.polygon([(cx+140, cy-120), (cx+200, cy-200), (cx+80, cy-150)], fill=hood)
    draw.polygon([(cx-130, cy-130), (cx-160, cy-170), (cx-90, cy-140)], fill=(255,200,200))
    draw.polygon([(cx+130, cy-130), (cx+160, cy-170), (cx+90, cy-140)], fill=(255,200,200))
    draw.ellipse([cx-130, cy-100, cx+130, cy+120], fill=(255,248,220))
    eye_y = cy - 20
    if pose == "thinking":
        draw.ellipse([cx-70, eye_y-10, cx-20, eye_y+20], fill=(0,0,0))
        draw.ellipse([cx+20, eye_y-15, cx+70, eye_y+15], fill=(0,0,0))
        draw.ellipse([cx-60, eye_y, cx-30, eye_y+10], fill=(255,255,255))
        draw.ellipse([cx+30, eye_y-5, cx+60, eye_y+5], fill=(255,255,255))
    elif pose == "shocked":
        draw.ellipse([cx-80, eye_y-20, cx-20, eye_y+30], fill=(255,255,255))
        draw.ellipse([cx+20, eye_y-20, cx+80, eye_y+30], fill=(255,255,255))
        draw.ellipse([cx-60, eye_y, cx-30, eye_y+20], fill=(0,0,0))
        draw.ellipse([cx+30, eye_y, cx+60, eye_y+20], fill=(0,0,0))
        draw.ellipse([cx-30, cy+40, cx+30, cy+80], fill=(0,0,0))
    else:
        draw.ellipse([cx-75, eye_y, cx-25, eye_y+25], fill=(0,0,0))
        draw.ellipse([cx+25, eye_y, cx+75, eye_y+25], fill=(0,0,0))
        draw.ellipse([cx-65, eye_y+5, cx-35, eye_y+15], fill=(255,255,255))
        draw.ellipse([cx+35, eye_y+5, cx+65, eye_y+15], fill=(255,255,255))
        if pose == "happy":
            draw.arc([cx-50, cy+20, cx+50, cy+70], 20, 160, fill=(0,0,0), width=6)
        else:
            draw.line([(cx-20, cy+50), (cx+20, cy+50)], fill=(0,0,0), width=4)
    draw.polygon([(cx-10, cy+15), (cx+10, cy+15), (cx, cy+30)], fill=(255,105,180))
    for dx in [-1, 1]:
        for wy in [cy+10, cy+25, cy+40]:
            draw.line([(cx+dx*40, wy), (cx+dx*110, wy)], fill=(0,0,0), width=3)
    return np.array(img)

def make_beautiful_bg(title, idx):
    img = Image.new('RGB', (W, H), (10,10,30))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(20 + idx*20 + (y/H)*60)
        g = int(15 + idx*10 + (y/H)*40)
        b = int(50 + idx*15 + (y/H)*80)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    for _ in range(25):
        x = random.randint(0,W)
        y = random.randint(0,H)
        s = random.randint(30,120)
        col = (random.randint(200,255), random.randint(180,255), random.randint(50,255))
        draw.ellipse([x-s, y-s, x+s, y+s], fill=col)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 115)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        emoji_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font
        emoji_font = title_font
    y = 280
    emojis = ["🔥","💰","😱","⚡"]
    for i, line in enumerate(title.split("\n")):
        bbox = draw.textbbox((0,0), line, font=title_font)
        w = bbox[2]-bbox[0]
        for ox in [-5,0,5]:
            for oy in [-5,0,5]:
                if ox!=0 or oy!=0:
                    draw.text(((W-w)//2+ox, y+oy), line, font=title_font, fill=(0,0,0))
        fill = (255,235,0) if i==0 else (255,255,255)
        draw.text(((W-w)//2, y), line, font=title_font, fill=fill)
        y += 150
    draw.text((W//2-40, y+20), emojis[idx % len(emojis)], font=emoji_font, fill=(255,255,255))
    y += 130
    draw.rounded_rectangle([80, y, W-80, y+16], radius=8, fill=(255,0,90))
    y += 45
    for chunk in ["VIRAL CHALLENGE","SECRET INSIDE"]:
        bbox = draw.textbbox((0,0), chunk, font=sub_font)
        w = bbox[2]-bbox[0]
        draw.rounded_rectangle([(W-w)//2-25, y-8, (W+w)//2+25, y+60], radius=20, fill=(0,0,0))
        draw.rounded_rectangle([(W-w)//2-25, y-8, (W+w)//2+25, y+60], radius=20, outline=(255,255,255), width=2)
        draw.text(((W-w)//2, y), chunk, font=sub_font, fill=(255,255,255))
        y += 80
    return np.array(img)

titles = ["STOP!\n$100K\nON LINE!", "3 TASKS\nYOU MUST\nWIN!", "SECRET\nTRICK\nREVEALED!", "COMMENT\nBELOW!"]
poses = ["shocked", "thinking", "pointing", "happy"]
clips = []
chapter_dur = audio.duration / len(titles)

for i, (title, pose) in enumerate(zip(titles, poses)):
    start = i * chapter_dur
    bg_img = make_beautiful_bg(title, i)
    bg_clip = ImageClip(bg_img, duration=chapter_dur).set_start(start)
    clips.append(bg_clip)
    cat_img = draw_blue_cat(pose, size=800)
    cat_clip = ImageClip(cat_img, duration=chapter_dur).set_start(start)
    # FIXED: NO lambda resize - static resize only!
    cat_clip = cat_clip.resize(width=680).set_position((W-720, H-900))
    clips.append(cat_clip)
    print(f"Cat {pose} added")

progress_bg = ColorClip(size=(W, 18), color=(255,255,255), duration=audio.duration).set_opacity(0.25).set_position((0, H-22))
progress_fill = ColorClip(size=(W, 18), color=(255,0,90), duration=audio.duration).set_position((0, H-22))
clips.append(progress_bg)
clips.append(progress_fill)

final = CompositeVideoClip(clips, size=(W,H)).set_audio(audio)
tmp_video="/tmp/short.mp4"
save_video="./short.mp4"
final.write_videofile(tmp_video,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None)
import shutil
shutil.copy(tmp_video, save_video)
print(f"BEAUTIFUL VIDEO READY: {audio.duration:.2f}s - {os.path.getsize(save_video)} bytes")

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
        req=youtube.videos().insert(part="snippet,status",body={"snippet":{"title":f"{titles[0].replace(chr(10),' ')} #shorts","description":f"{story} #shorts #viral Blue Cat","tags":["shorts","viral","bluecat"],"categoryId":"22"},"status":{"privacyStatus":"private","selfDeclaredMadeForKids":False}},media_body=MediaFileUpload(tmp_video,mimetype='video/mp4',resumable=True))
        resp=req.execute()
        print(f"SUCCESS! YOUTUBE: https://youtu.be/{resp['id']}")
    else:
        print("No secrets - saved for download")
except Exception as e:
    err=str(e)
    if "uploadLimitExceeded" in err or "exceeded" in err:
        print("YOUTUBE LIMIT HIT - VIDEO SAVED FOR DOWNLOAD!")
    else:
        print(f"Upload error: {e}")

print("DONE V9.1 BEAUTIFUL FIXED")
