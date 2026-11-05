import os, json, random, tempfile
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import *
import numpy as np

print("=== MILO & PIP V15 FINAL - 12 PER DAY ===")
try:
    with open('episodes.json') as f:
        episodes = json.load(f)
    ep = random.choice(episodes)
except:
    ep = {"title": "Milo Balances Laundry Tower", "story": "Milo the cat tries to carry laundry."}

story_text = ep['story'] + " Follow for next episode!"
title_text = ep['title']
print(f"EP: {title_text}")

tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story_text, lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)
print(f"Audio: {audio.duration:.2f}s")

W, H = 1080, 1920

def make_frame(text):
    img = Image.new('RGB', (W, H), (15,15,35))
    draw = ImageDraw.Draw(img)
    # gradient
    for y in range(H):
        r = int(15 + y/H*70)
        g = int(15 + y/H*20)
        b = int(35 + y/H*50)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # text - PIL not TextClip!
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font_big = ImageFont.load_default()
        font_small = font_big
    # wrap title
    draw.text((80, 350), text, font=font_big, fill=(255,235,0), stroke_width=4, stroke_fill=(0,0,0))
    draw.rectangle([80, 900, 1000, 908], fill=(255,50,80))
    draw.text((80, 950), "MILO & PIP SERIES", font=font_small, fill=(255,255,255))
    return np.array(img)

frame = make_frame(title_text)
bg_clip = ImageClip(frame, duration=audio.duration)
bg_clip = bg_clip.resize(lambda t: 1.0 + 0.04*t/audio.duration)

progress_bg = ColorClip(size=(W, 14), color=(255,255,255), duration=audio.duration).set_opacity(0.2).set_position((0, H-18))
progress_fill = ColorClip(size=(W, 14), color=(255,50,80), duration=audio.duration).set_position((0, H-18))
progress_fill = progress_fill.resize(lambda t: (int(W * (t / audio.duration)), 14))

final = CompositeVideoClip([bg_clip, progress_bg, progress_fill]).set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
print(f"DONE short.mp4 {os.path.getsize('short.mp4')} bytes")

# YouTube upload if secrets exist
if os.getenv("GOOGLE_REFRESH_TOKEN"):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        creds = Credentials(None, refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"), token_uri="https://oauth2.googleapis.com/token", client_id=os.getenv("GOOGLE_CLIENT_ID"), client_secret=os.getenv("GOOGLE_CLIENT_SECRET"), scopes=['https://www.googleapis.com/auth/youtube.upload'])
        youtube = build('youtube','v3', credentials=creds)
        req = youtube.videos().insert(part="snippet,status", body={"snippet":{"title":f"{title_text} #shorts","description":f"{story_text} #shorts #miloandpip","tags":["shorts","cartoon"],"categoryId":"22"},"status":{"privacyStatus":"public","selfDeclaredMadeForKids":False}}, media_body=MediaFileUpload("short.mp4", mimetype='video/mp4', resumable=True))
        resp = req.execute()
        print(f"UPLOADED https://youtu.be/{resp['id']}")
    except Exception as e:
        print(f"Upload skipped: {e}")
