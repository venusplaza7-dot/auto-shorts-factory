import os, tempfile, random
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("=== 30 SEC GRAPHICS FACTORY V2 - FIXED ===")

scripts = [
    {
        "title": "STOP! $100K\nCHALLENGE!",
        "script": "Stop scrolling! This is the $100,000 basketball challenge that broke the internet! A famous YouTuber challenged a basketball star. If you beat him, you win 100 grand! The first shot - missed! Second shot - missed! But the third shot? Nobody expected what happened next! The secret is how they edit to keep you watching till the end! Subscribe for the full breakdown!"
    },
    {
        "title": "VIRAL SECRET\nREVEALED!",
        "script": "This viral video got 100 million views in 24 hours! How? The secret is in the first 3 seconds! They use a hook that makes you stop scrolling! Then they add a countdown, suspense music, and a prize! If you can copy this formula, your Shorts will blow up too! Watch till the end for the bonus tip that nobody talks about! Follow for more viral secrets every day!"
    },
    {
        "title": "I WON\n$100,000?!",
        "script": "I tried the viral 100K challenge and this happened! Everyone said it's impossible! First I had to beat 3 challenges in a row! Basketball, football, and a puzzle! If I fail one, I lose everything! The pressure was insane! But I found a trick that the top creators use! And in the last 10 seconds, I did something nobody expected! Comment your guess what happened!"
    }
]

data = random.choice(scripts)
title = data["title"]
script = data["script"]
print(f"Title: {title}")
print(f"Words: {len(script.split())}")

tmp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=script, lang='en', slow=False).save(tmp_audio)
audio = AudioFileClip(tmp_audio)
print(f"Audio: {audio.duration}s - TARGET 30 SEC!")

W, H = 1080, 1920
colors = [(13,13,30), (30,10,40), (10,30,35), (35,15,15)]
clips = []
segment = audio.duration / len(colors)
for i, col in enumerate(colors):
    c = ColorClip(size=(W,H), color=col, duration=segment).set_start(i*segment)
    clips.append(c)

def make_graphics(text, sub_text, size):
    img = Image.new('RGBA', size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 110)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font

    y = 350
    for line in text.split('\n'):
        bbox = draw.textbbox((0,0), line, font=title_font)
        w = bbox[2]-bbox[0]
        draw.text(((size[0]-w)//2 + 6, y+6), line, font=title_font, fill=(0,0,0,180))
        draw.text(((size[0]-w)//2, y), line, font=title_font, fill=(255, 230, 0) if "!" in line else (255,255,255))
        y += 140

    draw.rounded_rectangle([120, y+10, size[0]-120, y+30], radius=10, fill=(255, 0, 80))
    y += 80
    words = sub_text.split()
    line1 = ' '.join(words[:7])
    line2 = ' '.join(words[7:14]) + "..."

    for txt in [line1, line2]:
        bbox = draw.textbbox((0,0), txt, font=sub_font)
        w = bbox[2]-bbox[0]
        draw.rounded_rectangle([(size[0]-w)//2 - 20, y-5, (size[0]+w)//2 + 20, y+55], radius=15, fill=(0,0,0,180))
        draw.text(((size[0]-w)//2, y), txt, font=sub_font, fill=(255,255,255))
        y += 75

    draw.ellipse([80, 1400, 280, 1600], fill=(255,0,80,120))
    draw.ellipse([W-280, 1450, W-80, 1650], fill=(0, 200, 255, 120))
    return np.array(img)

main_img = make_graphics(title, script[:100], (W,H))
txt_clip = ImageClip(main_img, duration=audio.duration)

# Simple static progress bar (FIXED - no function)
progress_bg = ColorClip(size=(W, 12), color=(255,255,255)).set_opacity(0.3).set_duration(audio.duration).set_position((0, H-60))
progress_fg = ColorClip(size=(W, 12), color=(255,0,80)).set_duration(audio.duration).set_position((0, H-60))

video = CompositeVideoClip(clips + [txt_clip, progress_bg, progress_fg]).set_audio(audio)
tmp_video = "/tmp/short.mp4"
video.write_videofile(tmp_video, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None)
print(f"Video READY: {audio.duration}s")

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

if CLIENT_ID and REFRESH_TOKEN:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri="https://oauth2.googleapis.com/token",
                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        scopes=['https://www.googleapis.com/auth/youtube.upload'])
    youtube = build('youtube', 'v3', credentials=creds)
    req = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": f"{title.replace(chr(10),' ')} #shorts",
                "description": f"{script} #shorts #viral",
                "tags": ["shorts","viral","challenge"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(tmp_video, mimetype='video/mp4', resumable=True)
    )
    resp = req.execute()
    print(f"SUCCESS! 30 SEC SHORT: https://youtu.be/{resp['id']}")
