import os, json, random, tempfile, math
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import *
import numpy as np

print("=== MILO & PIP V15 - 12 PER DAY FACTORY ===")

# Load episode
try:
    with open('episodes.json', 'r') as f:
        episodes = json.load(f)
    ep = random.choice(episodes)
except:
    ep = {"title": "Milo Balances Laundry Tower", "story": "Milo tries to carry laundry tower and wobbles."}

title_text = ep['title']
story_text = ep['story'] + " Follow for next episode! Comment what happens next!"
print(f"EPISODE: {title_text}")

# Audio - 25-30 sec long
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story_text, lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)
print(f"Audio duration: {audio.duration:.2f}s - Perfect for Shorts")

W, H = 1080, 1920

def make_pro_bg():
    colors = [((12,12,28),(88,28,88)), ((15,25,45),(20,55,80)), ((28,12,20),(90,30,35))]
    c1, c2 = random.choice(colors)
    img = Image.new('RGB', (W, H), c1)
    draw = ImageDraw.Draw(img, 'RGBA')
    for y in range(H):
        r = int(c1[0] + (c2[0]-c1[0])*y/H)
        g = int(c1[1] + (c2[1]-c1[1])*y/H)
        b = int(c1[2] + (c2[2]-c1[2])*y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # light leaks
    draw.ellipse([-200,-200,600,600], fill=(255,255,255,10))
    draw.ellipse([W-400,H-600,W+300,H+100], fill=(255,200,50,12))
    return np.array(img)

# Build clips
bg_img = make_pro_bg()
bg_clip = ImageClip(bg_img, duration=audio.duration)
bg_clip = bg_clip.resize(lambda t: 1.0 + 0.05*t/audio.duration)

# Title with pop animation - 28 sec episode style
try:
    title_clip = TextClip(title_text, fontsize=90, color='yellow', font='DejaVu-Sans-Bold', stroke_color='black', stroke_width=6, method='caption', size=(900,400)).set_duration(audio.duration)
except:
    title_clip = TextClip(title_text, fontsize=90, color='yellow', method='caption', size=(900,400)).set_duration(audio.duration)

title_clip = title_clip.set_position(('center', 350)).resize(lambda t: 0.9 + 0.2*min(1, t*3))

# Badge
badge = TextClip("MILO & PIP SERIES", fontsize=38, color='white', bg_color='black', font='DejaVu-Sans-Bold').set_duration(audio.duration).set_position(('center', 900))

# Progress bar - animated
progress_bg = ColorClip(size=(W, 14), color=(255,255,255), duration=audio.duration).set_opacity(0.2).set_position((0, H-18))
progress_fill = ColorClip(size=(W, 14), color=(255,50,80), duration=audio.duration).set_position((0, H-18))
progress_fill = progress_fill.resize(lambda t: (int(W * (t / audio.duration)), 14))

final = CompositeVideoClip([bg_clip, title_clip, badge, progress_bg, progress_fill]).set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac', preset='ultrafast', threads=4)

print(f"DONE: short.mp4 ready - {os.path.getsize('short.mp4')} bytes - {audio.duration:.2f}s long")

# YouTube Upload
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
REFRESH = os.getenv("GOOGLE_REFRESH_TOKEN")
if CLIENT_ID and REFRESH:
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
        creds = Credentials(None, refresh_token=REFRESH, token_uri="https://oauth2.googleapis.com/token", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scopes=['https://www.googleapis.com/auth/youtube.upload'])
        youtube = build('youtube','v3', credentials=creds)
        req = youtube.videos().insert(part="snippet,status", body={"snippet":{"title":f"{title_text} #shorts","description":f"{story_text} #shorts #cat #cartoon #milopip","tags":["shorts","cat","cartoon","miloandpip"],"categoryId":"22"},"status":{"privacyStatus":"public","selfDeclaredMadeForKids":False}}, media_body=MediaFileUpload("short.mp4", mimetype='video/mp4', resumable=True))
        resp = req.execute()
        print(f"UPLOADED: https://youtu.be/{resp['id']}")
    except Exception as e:
        print(f"Upload skip: {e}")
else:
    print("No YouTube secrets - saved locally for download")
