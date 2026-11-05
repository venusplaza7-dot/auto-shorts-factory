import os, tempfile, random, traceback
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("=== V8 SAVE FOR DOWNLOAD - NO CRASH ===")

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

def make_bg(title, idx):
    img = Image.new('RGB', (W,H), (15,15,35))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(15 + idx*15 + (y/H)*35)
        g = int(15 + idx*5 + (y/H)*25)
        b = int(45 + idx*10 + (y/H)*45)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 105)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font
    y=350
    for line in title.split("\n"):
        bbox=draw.textbbox((0,0),line,font=title_font)
        w=bbox[2]-bbox[0]
        for ox in [-4,0,4]:
            for oy in [-4,0,4]:
                draw.text(((W-w)//2+ox,y+oy),line,font=title_font,fill=(0,0,0))
        fill=(255,230,0) if "!" in line or "$" in line else (255,255,255)
        draw.text(((W-w)//2,y),line,font=title_font,fill=fill)
        y+=140
    draw.rounded_rectangle([100,y+20,W-100,y+38],radius=10,fill=(255,0,80))
    y+=80
    for chunk in ["VIRAL CHALLENGE","SECRET REVEALED"]:
        bbox=draw.textbbox((0,0),chunk,font=sub_font)
        w=bbox[2]-bbox[0]
        draw.rounded_rectangle([(W-w)//2-20,y-6,(W+w)//2+20,y+50],radius=15,fill=(0,0,0))
        draw.text(((W-w)//2,y),chunk,font=sub_font,fill=(255,255,255))
        y+=70
    return np.array(img)

titles=["STOP!\n$100K ON LINE!","3 TASKS\nMUST WIN!","SECRET TRICK\nREVEALED!","COMMENT\nWHAT HAPPENED!"]
clips=[]
chapter_dur=audio.duration/len(titles)
for i,title in enumerate(titles):
    start=i*chapter_dur
    bg_img=make_bg(title,i)
    bg_clip=ImageClip(bg_img,duration=chapter_dur).set_start(start)
    clips.append(bg_clip)
    for pose_file in ["assets/cat_thinking_blue.webp","assets/cat_pointing_blue.webp","assets/cat_happy_blue.webp","assets/cat_shocked_blue.webp"]:
        if os.path.exists(pose_file):
            try:
                cat_clip=ImageClip(pose_file,duration=chapter_dur).set_start(start)
                cat_clip=cat_clip.resize(width=650).set_position((W-680,H-850))
                clips.append(cat_clip)
                break
            except: pass

progress_bg=ColorClip(size=(W,16),color=(255,255,255),duration=audio.duration).set_opacity(0.3).set_position((0,H-20))
progress_fill=ColorClip(size=(W,16),color=(255,0,80),duration=audio.duration).set_position((0,H-20))
clips.append(progress_bg)
clips.append(progress_fill)

final=CompositeVideoClip(clips).set_audio(audio)
# SAVE TO TWO PLACES - /tmp AND current dir for artifact
tmp_video="/tmp/short.mp4"
save_video="./short.mp4"
final.write_videofile(tmp_video,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',logger=None)
# Copy to repo dir for artifact
import shutil
shutil.copy(tmp_video, save_video)
print(f"VIDEO READY: {audio.duration:.2f}s - Saved to {save_video} - Size: {os.path.getsize(save_video)} bytes")

# Try upload - but DON'T crash if limit hit
CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN=os.getenv("GOOGLE_REFRESH_TOKEN")
try:
    if CLIENT_ID and REFRESH_TOKEN:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        creds=Credentials(None,refresh_token=REFRESH_TOKEN,token_uri="https://oauth2.googleapis.com/token",client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scopes=['https://www.googleapis.com/auth/youtube.upload'])
        youtube=build('youtube','v3',credentials=creds)
        req=youtube.videos().insert(part="snippet,status",body={"snippet":{"title":f"{titles[0].replace(chr(10),' ')} #shorts","description":f"{story} #shorts #viral Blue Cat","tags":["shorts","viral","bluecat"],"categoryId":"22"},"status":{"privacyStatus":"private","selfDeclaredMadeForKids":False}},media_body=MediaFileUpload(tmp_video,mimetype='video/mp4',resumable=True))
        resp=req.execute()
        print(f"SUCCESS! YOUTUBE UPLOAD: https://youtu.be/{resp['id']}")
    else:
        print("Missing secrets - video saved for download only")
except Exception as e:
    err_str=str(e)
    if "uploadLimitExceeded" in err_str or "exceeded the number" in err_str:
        print("="*60)
        print("YOUTUBE LIMIT HIT - BUT VIDEO IS SAVED!")
        print("Download video from GitHub Actions Artifacts:")
        print("Actions -> This run -> Artifacts -> short-video")
        print("Then upload manually to studio.youtube.com")
        print("="*60)
        # Don't exit with error - exit 0 so job is GREEN and artifact saved
    else:
        print(f"Upload error (not limit): {e}")
        traceback.print_exc()

print("DONE - VIDEO SAVED FOR DOWNLOAD")
