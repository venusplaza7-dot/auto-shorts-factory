import os, tempfile, random
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("=== FINAL FACTORY - VISUAL ===")

ideas = [
    ("Viral Challenge\nBreakdown", "Viral video secrets revealed! How top creators keep you watching till the end! The secret is the first 3 seconds!"),
    ("$100k Challenge!", "Beat the basketball challenge win 100 thousand dollars! What happened next shocked everyone!"),
    ("Secret Revealed!", "I spent 50 hours analyzing viral videos and found the formula!"),
]

title, script = random.choice(ideas)
print(f"Title: {title}")

# 1. Voice
tmp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=script, lang='en', slow=False).save(tmp_audio)
audio = AudioFileClip(tmp_audio)
print(f"Audio: {audio.duration}s")

W, H = 1080, 1920
# 2. Colorful background
bg = ColorClip(size=(W,H), color=(13, 13, 30), duration=audio.duration)

# 3. Create TEXT image with PIL (fast, no ImageMagick)
def make_text_image(text, size):
    img = Image.new('RGBA', size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Try to use bold font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
    except:
        font = ImageFont.load_default()
        small_font = font

    # Wrap text
    lines = text.split('\n')
    y = 500
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2]-bbox[0]
        draw.text(((size[0]-w)//2, y), line, font=font, fill=(255,255,255))
        y += 130
    # Add emoji style bar
    draw.rectangle([100, y+20, size[0]-100, y+30], fill=(255,0,80))
    return np.array(img)

txt_img = make_text_image(title, (W,H))
txt_clip = ImageClip(txt_img, duration=audio.duration).set_position('center')

# 4. Final video with text on top
video = CompositeVideoClip([bg, txt_clip]).set_audio(audio)
tmp_video = "/tmp/short.mp4"
video.write_videofile(tmp_video, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None)
print(f"Video done: {tmp_video}")

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
                "description": f"Original commentary: {script} #shorts #viral",
                "tags": ["shorts","viral","challenge"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(tmp_video, mimetype='video/mp4', resumable=True)
    )
    resp = req.execute()
    print(f"SUCCESS! https://youtu.be/{resp['id']}")
