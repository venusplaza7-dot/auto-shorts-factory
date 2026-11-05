import os, tempfile, random
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("=== V5 BLUE CAT CHARACTER FACTORY ===")

# Character: Blue Hoodie Cat
# Poses: thinking, pointing, happy, shocked

stories = [
    {
        "hook": "STOP! $100K\nON THE LINE!",
        "chapters": [
            ("THINKING", "Stop scrolling! This is the one hundred thousand dollar challenge that broke the internet!", "thinking"),
            ("POINTING", "You must beat three impossible tasks! Basketball, football, and a puzzle!", "pointing"),
            ("SHOCKED", "Fail one and you lose everything! But I found the secret trick! Watch till the end!", "shocked"),
            ("HAPPY", "Comment what you think happened! Follow for Part 2! Subscribe now!", "happy"),
        ],
        "full": "Stop scrolling! This is the one hundred thousand dollar basketball challenge that broke the internet! You must beat three impossible tasks! Basketball, football, and a puzzle! Fail one and you lose everything! The pressure was insane! But I found the trick top creators use to win! Watch till the last ten seconds! Comment what you think happened! Follow for Part 2!"
    }
]

data = random.choice(stories)
chapters = data["chapters"]
full_script = data["full"]
print(f"Full script words: {len(full_script.split())}")

# 1. Voice - 30 sec
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=full_script, lang='en', slow=False).save(tmp_mp3)
tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
os.system(f"ffmpeg -y -i {tmp_mp3} {tmp_wav} -loglevel quiet")
audio = AudioFileClip(tmp_wav) if os.path.exists(tmp_wav) and os.path.getsize(tmp_wav)>1000 else AudioFileClip(tmp_mp3)
print(f"Audio: {audio.duration:.2f}s")

W, H = 1080, 1920

# 2. Try to load cat images if they exist in assets/, else use colorful backgrounds
cat_files = {
    "thinking": "assets/cat_thinking_blue.webp",
    "pointing": "assets/cat_pointing_blue.webp",
    "happy": "assets/cat_happy_blue.webp",
    "shocked": "assets/cat_shocked_blue.webp",
}

def make_pro_background(ch_title, subtitle, color_idx, t):
    img = Image.new('RGB', (W,H), (15,15,35))
    draw = ImageDraw.Draw(img)
    # Gradient
    for y in range(H):
        r = int(15 + color_idx*10 + (y/H)*30)
        g = int(15 + color_idx*5 + (y/H)*20)
        b = int(40 + color_idx*10 + (y/H)*40)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 110)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font

    y = 250
    for line in ch_title.split("\n"):
        bbox = draw.textbbox((0,0), line, font=title_font)
        w = bbox[2]-bbox[0]
        for ox in [-4,0,4]:
            for oy in [-4,0,4]:
                draw.text(((W-w)//2+ox, y+oy), line, font=title_font, fill=(0,0,0))
        fill = (255,230,0) if "!" in line else (255,255,255)
        draw.text(((W-w)//2, y), line, font=title_font, fill=fill)
        y += 135

    draw.rounded_rectangle([100, y+10, W-100, y+28], radius=10, fill=(255,0,80))
    y += 60
    words = subtitle.split()
    for chunk in [' '.join(words[i:i+6]) for i in range(0, min(12, len(words)), 6)][:2]:
        bbox = draw.textbbox((0,0), chunk, font=sub_font)
        w = bbox[2]-bbox[0]
        draw.rounded_rectangle([(W-w)//2 -20, y-6, (W+w)//2+20, y+48], radius=15, fill=(0,0,0,200))
        draw.text(((W-w)//2, y), chunk, font=sub_font, fill=(255,255,255))
        y += 65
    return np.array(img)

# Build chapters
clips = []
chapter_duration = audio.duration / len(chapters)

for i, (ch_title, ch_sub, pose) in enumerate(chapters):
    start = i * chapter_duration
    # Background for chapter
    bg_img = make_pro_background(ch_title, ch_sub, i, i)
    bg_clip = ImageClip(bg_img, duration=chapter_duration).set_start(start)
    clips.append(bg_clip)
    
    # Try to add cat character if file exists
    cat_path = cat_files.get(pose)
    if os.path.exists(cat_path):
        try:
            # Cat at bottom right, big
            cat_clip = ImageClip(cat_path, duration=chapter_duration).set_start(start)
            cat_clip = cat_clip.resize(width=650).set_position((W-680, H-850))
            clips.append(cat_clip)
        except:
            pass

# Progress bar
def make_prog(t):
    prog = t / audio.duration
    img = Image.new('RGBA', (W, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0,0,W,16], radius=8, fill=(255,255,255,90))
    d.rounded_rectangle([0,0,int(W*prog),16], radius=8, fill=(255,0,80))
    return np.array(img)

progress = ImageClip(make_prog, duration=audio.duration).set_position((0, H-20))

final = CompositeVideoClip(clips + [progress]).set_audio(audio)
tmp_video = "/tmp/short.mp4"
final.write_videofile(tmp_video, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None)
print(f"Video READY: {audio.duration:.2f}s with BLUE CAT CHARACTER!")

# Upload
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
                "title": f"{chapters[0][0].replace(chr(10),' ')} #shorts",
                "description": f"{full_script} #shorts #viral Character: Blue Hoodie Cat",
                "tags": ["shorts","viral","bluecat","challenge"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(tmp_video, mimetype='video/mp4', resumable=True)
    )
    resp = req.execute()
    print(f"SUCCESS! BLUE CAT SHORT: https://youtu.be/{resp['id']}")
