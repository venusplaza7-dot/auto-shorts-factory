import os, json, random, tempfile
from PIL import Image
Image.ANTIALIAS = Image.LANCZOS if not hasattr(Image, 'ANTIALIAS') else Image.ANTIALIAS

from PIL import ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import *
import numpy as np

print("=== FINAL WORKING - NO RESIZE ===")

try:
    with open('episodes.json') as f:
        ep = random.choice(json.load(f))
except:
    ep = {"title": "Milo Balances Laundry Tower", "story": "Milo tries to carry laundry tower"}

story = ep['story'] + " Follow for next episode!"
title = ep['title']
print(f"EP: {title}")

tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story, lang='en', slow=False).save(tmp)
audio = AudioFileClip(tmp)
print(f"Duration: {audio.duration}s")

W, H = 1080, 1920

# Make one static image - NO RESIZE NEEDED
img = Image.new('RGB', (W, H), (18, 18, 40))
draw = ImageDraw.Draw(img)
for y in range(H):
    r = int(18 + y/H*60)
    g = int(18 + y/H*20)
    b = int(40 + y/H*60)
    draw.line([(0,y),(W,y)], fill=(r,g,b))

try:
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
except:
    f1 = ImageFont.load_default()
    f2 = f1

draw.text((80, 400), title, font=f1, fill=(255,230,0), stroke_width=4, stroke_fill=(0,0,0))
draw.text((80, 950), "MILO & PIP - 12 EPISODES PER DAY", font=f2, fill=(255,255,255))
draw.rectangle([0, H-14, W, H], fill=(255,50,80))

bg = ImageClip(np.array(img), duration=audio.duration)
final = bg.set_audio(audio)
final.write_videofile("short.mp4", fps=24, codec='libx264', audio_codec='aac', preset='ultrafast')

print(f"READY {os.path.getsize('short.mp4')} bytes - {audio.duration:.2f}s long - NO RESIZE ERROR")

# Upload
if os.getenv("GOOGLE_REFRESH_TOKEN"):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        creds = Credentials(None, refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"), token_uri="https://oauth2.googleapis.com/token", client_id=os.getenv("GOOGLE_CLIENT_ID"), client_secret=os.getenv("GOOGLE_CLIENT_SECRET"), scopes=['https://www.googleapis.com/auth/youtube.upload'])
        yt = build('youtube','v3', credentials=creds)
        req = yt.videos().insert(part="snippet,status", body={"snippet":{"title":f"{title} #shorts","description":f"{story} #shorts","categoryId":"22"},"status":{"privacyStatus":"public","selfDeclaredMadeForKids":False}}, media_body=MediaFileUpload("short.mp4", resumable=True))
        r = req.execute()
        print(f"UPLOADED https://youtu.be/{r['id']}")
    except Exception as e:
        print(f"Upload skip {e}")
