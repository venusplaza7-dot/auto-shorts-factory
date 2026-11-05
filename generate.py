import os, tempfile, random
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("=== 30 SEC GRAPHICS FACTORY V3 - VOICE FIXED ===")

# 30 sec scripts = 75-85 words each = 29-31 sec audio
scripts = [
    {
        "title": "STOP! $100K\nCHALLENGE!",
        "script": "Stop scrolling! This is the one hundred thousand dollar basketball challenge that broke the internet! A famous creator challenged a basketball star. If you beat him, you win one hundred grand! The first shot - missed! Second shot - missed! But the third shot? Nobody expected what happened next! The secret is how they edit to keep you watching till the end! Subscribe for the full breakdown!"
    },
    {
        "title": "VIRAL SECRET\nREVEALED!",
        "script": "This viral video got one hundred million views in twenty four hours! How? The secret is in the first three seconds! They use a hook that makes you stop scrolling! Then they add a countdown, suspense music, and a huge prize! If you can copy this formula, your Shorts will blow up too! Watch till the end for the bonus tip that nobody talks about! Follow for more viral secrets every day!"
    },
    {
        "title": "I WON\n$100,000?!",
        "script": "I tried the viral one hundred K challenge and this happened! Everyone said it is impossible! First I had to beat three challenges in a row! Basketball, football, and a puzzle! If I fail one, I lose everything! The pressure was insane! But I found a trick that the top creators use! And in the last ten seconds, I did something nobody expected! Comment your guess what happened right now!"
    }
]

data = random.choice(scripts)
title = data["title"]
script = data["script"]
print(f"Title: {title.replace(chr(10),' ')}")
print(f"Words: {len(script.split())}")

# 1. VOICE - Make 30 sec audio
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=script, lang='en', slow=False).save(tmp_mp3)

# Convert MP3 to WAV for reliable moviepy audio (fixes silent video bug)
tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
os.system(f"ffmpeg -y -i {tmp_mp3} {tmp_wav} -loglevel quiet")

if os.path.exists(tmp_wav) and os.path.getsize(tmp_wav) > 1000:
    audio = AudioFileClip(tmp_wav)
    print(f"Audio WAV: {audio.duration:.2f}s - TARGET 30 SEC!")
else:
    audio = AudioFileClip(tmp_mp3)
    print(f"Audio MP3: {audio.duration:.2f}s - TARGET 30 SEC!")

W, H = 1080, 1920

# 2. GRAPHICS - 4 colorful backgrounds changing every ~7 sec
colors = [(13,13,40), (40,10,30), (10,35,30), (35,25,10)]
clips = []
seg = audio.duration / len(colors)
for i, col in enumerate(colors):
    c = ColorClip(size=(W,H), color=col, duration=seg).set_start(i*seg)
    clips.append(c)

# 3. TEXT GRAPHICS with PIL (no ImageMagick needed)
def make_graphics(title_text, caption, size):
    img = Image.new('RGBA', size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 105)
        cap_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
    except:
        title_font = ImageFont.load_default()
        cap_font = title_font

    y = 350
    for line in title_text.split("\n"):
        bbox = draw.textbbox((0,0), line, font=title_font)
        w = bbox[2]-bbox[0]
        # shadow
        draw.text(((size[0]-w)//2 + 7, y+7), line, font=title_font, fill=(0,0,0,180))
        # main yellow/white
        fill = (255, 230, 0) if "!" in line else (255,255,255)
        draw.text(((size[0]-w)//2, y), line, font=title_font, fill=fill)
        y += 135

    # red bar
    draw.rounded_rectangle([120, y+15, size[0]-120, y+32], radius=10, fill=(255, 0, 80))

    # captions with black box
    y += 70
    words = caption.split()
    for chunk in [' '.join(words[i:i+7]) for i in range(0, 14, 7)][:2]:
        bbox = draw.textbbox((0,0), chunk, font=cap_font)
        w = bbox[2]-bbox[0]
        draw.rounded_rectangle([(size[0]-w)//2 - 18, y-6, (size[0]+w)//2 + 18, y+50], radius=14, fill=(0,0,0,200))
        draw.text(((size[0]-w)//2, y), chunk, font=cap_font, fill=(255,255,255))
        y += 68

    # graphic circles
    draw.ellipse([70, 1420, 270, 1620], fill=(255,0,80,110))
    draw.ellipse([W-270, 1470, W-70, 1670], fill=(0, 200, 255, 110))
    return np.array(img)

main_img = make_graphics(title, script[:110], (W,H))
txt_clip = ImageClip(main_img, duration=audio.duration)

# Final video with voice
video = CompositeVideoClip(clips + [txt_clip]).set_audio(audio)
tmp_video = "/tmp/short.mp4"
video.write_videofile(tmp_video, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None)
print(f"Video READY: {audio.duration:.2f}s - 3 SCENES with GRAPHICS!")

# 5. Upload
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
                "description": f"{script} #shorts #viral Original commentary, no copyrighted footage",
                "tags": ["shorts","viral","challenge"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(tmp_video, mimetype='video/mp4', resumable=True)
    )
    resp = req.execute()
    print(f"SUCCESS! 30 SEC SHORT: https://youtu.be/{resp['id']}")
else:
    print("Missing secrets - video made but not uploaded")
