import os, tempfile, random, math
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

print("=== V4 VIRAL PRO - ADDICTIVE GRAPHICS ===")

stories = [
    {
        "hook": "STOP! $100K\nON THE LINE!",
        "chapters": [
            ("The $100K\nChallenge!", "Stop scrolling! This is the one hundred thousand dollar challenge that broke the internet!"),
            ("3 Impossible\nTasks!", "You must beat three impossible tasks! Basketball, football, and a mind puzzle! Fail one and you lose everything!"),
            ("The Secret\nTwist!", "But I found the trick top creators use to win! Watch till the last ten seconds! Comment what you think happened!"),
        ],
        "full": "Stop scrolling! This is the one hundred thousand dollar basketball challenge that broke the internet! You must beat three impossible tasks! Basketball, football, and a mind puzzle! Fail one and you lose everything! The pressure was insane! But I found the trick top creators use to win! Watch till the last ten seconds! Comment what you think happened!"
    },
    {
        "hook": "THIS WENT\nVIRAL!",
        "chapters": [
            ("100M VIEWS\nIn 24H!", "This viral video got one hundred million views in twenty four hours! How?"),
            ("The 3 Sec\nHOOK!", "The secret is the first three seconds! A hook that makes you stop scrolling! Countdown plus prize!"),
            ("Copy This\nFORMULA!", "Copy this formula and your Shorts will blow up too! Watch till the end for the bonus tip nobody talks about!"),
        ],
        "full": "This viral video got one hundred million views in twenty four hours! How? The secret is the first three seconds! They use a hook that makes you stop scrolling! Then they add a countdown, suspense music, and a huge prize! If you can copy this formula, your Shorts will blow up too! Watch till the end for the bonus tip that nobody talks about! Follow for more viral secrets every day!"
    }
]

data = random.choice(stories)
hook = data["hook"]
chapters = data["chapters"]
full_script = data["full"]
print(f"Hook: {hook.replace(chr(10),' ')} | Words: {len(full_script.split())}")

# 1. VOICE - 30 sec
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=full_script, lang='en', slow=False).save(tmp_mp3)
tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
os.system(f"ffmpeg -y -i {tmp_mp3} {tmp_wav} -loglevel quiet")
audio = AudioFileClip(tmp_wav) if os.path.exists(tmp_wav) and os.path.getsize(tmp_wav)>1000 else AudioFileClip(tmp_mp3)
print(f"Audio: {audio.duration:.2f}s TARGET 30s")

W, H = 1080, 1920

# Helper: pro text image with shadow, outline, glow
def make_pro_image(title, subtitle, bg_style, time_factor):
    # Create gradient background
    img = Image.new('RGB', (W, H), (0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Gradient based on bg_style
    if bg_style == 0: # Dark blue -> purple
        for y in range(H):
            r = int(10 + (60-10)*y/H + math.sin(time_factor)*10)
            g = int(10 + (10-10)*y/H)
            b = int(40 + (90-40)*y/H)
            draw.line([(0,y),(W,y)], fill=(r,g,b))
    elif bg_style == 1: # Dark red -> orange
        for y in range(H):
            r = int(50 + (80-50)*y/H)
            g = int(10 + (40-10)*y/H)
            b = int(20)
            draw.line([(0,y),(W,y)], fill=(r,g,b))
    else: # Dark green -> teal
        for y in range(H):
            r = int(10)
            g = int(20 + (60-20)*y/H)
            b = int(30 + (50-30)*y/H)
            draw.line([(0,y),(W,y)], fill=(r,g,b))
    
    # Add floating blurred circles (bokeh effect)
    for _ in range(5):
        cx = int((W*0.5 + math.sin(time_factor*2+_)*200 + _*150) % W)
        cy = int((H*0.3 + math.cos(time_factor+_)*150 + _*200) % H)
        rad = 80 + _*20
        overlay = Image.new('RGBA', (W,H), (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=(255,255,255,30))
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=30))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 115)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font
        small_font = title_font

    # Pulsing scale effect
    scale = 1.0 + 0.05*math.sin(time_factor*3)
    
    # Title with heavy outline
    y = 380
    for line in title.split("\n"):
        bbox = draw.textbbox((0,0), line, font=title_font)
        w = bbox[2]-bbox[0]
        x = (W - w*scale)//2
        # Thick black outline
        for ox in [-5,-3,0,3,5]:
            for oy in [-5,-3,0,3,5]:
                draw.text((x+ox, y+oy), line, font=title_font, fill=(0,0,0))
        # Main text - gradient yellow to white
        fill = (255, 235, 0) if "!" in line or "$" in line else (255,255,255)
        draw.text((x, y), line, font=title_font, fill=fill)
        y += int(145*scale)

    # Red accent bar with glow
    draw.rounded_rectangle([100, y+15, W-100, y+38], radius=12, fill=(255, 30, 80))
    # Glow under bar
    glow = Image.new('RGBA', (W, 100), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle([100, 0, W-100, 23], radius=12, fill=(255,30,80,80))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=10))
    img.paste(Image.new('RGB', (W,100), (0,0,0)), (0, y+15), glow)
    
    y += 90
    # Subtitle with background pill
    words = subtitle.split()
    lines = [' '.join(words[i:i+6]) for i in range(0, min(12, len(words)), 6)][:2]
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=sub_font)
        w = bbox[2]-bbox[0]
        # Pill background
        draw.rounded_rectangle([(W-w)//2 - 25, y-8, (W+w)//2 + 25, y+52], radius=20, fill=(0,0,0,210))
        draw.text(((W-w)//2, y), line, font=sub_font, fill=(255,255,255))
        y += 68

    # Bottom CTA
    cta = "FOLLOW FOR PART 2!"
    bbox = draw.textbbox((0,0), cta, font=small_font)
    w = bbox[2]-bbox[0]
    draw.rounded_rectangle([(W-w)//2 - 15, H-180, (W+w)//2 + 15, H-140], radius=12, fill=(255,235,0))
    draw.text(((W-w)//2, H-178), cta, font=small_font, fill=(0,0,0))

    return np.array(img)

# 2. Build 3 chapters changing with script
chapter_duration = audio.duration / len(chapters)
clips = []

for i, (ch_title, ch_sub) in enumerate(chapters):
    start = i * chapter_duration
    # Create 30 frames of animation for this chapter (moving background)
    def make_frame(t):
        # t is relative to chapter start
        return make_pro_image(ch_title, ch_sub, i, t*2 + i)

    # Use 24 fps illusion: create image clip with changing texture via time
    # For speed, generate 1 image per chapter with time_factor = i
    img_arr = make_pro_image(ch_title, ch_sub, i, i*1.5)
    ic = ImageClip(img_arr, duration=chapter_duration).set_start(start)
    # Add zoom effect
    ic = ic.resize(lambda t: 1.0 + 0.08*t/chapter_duration)
    clips.append(ic)

# 3. Add progress bar (YouTube style)
def progress_img():
    img = Image.new('RGBA', (W, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0,0,W,16], radius=8, fill=(255,255,255,90))
    return img

prog_bg = ImageClip(np.array(Image.new('RGBA', (W,16), (0,0,0,0))), duration=audio.duration).set_position((0, H-16))

# Animated progress
def make_prog_frame(t):
    prog = t / audio.duration
    img = Image.new('RGBA', (W, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0,0,W,16], radius=8, fill=(255,255,255,90))
    d.rounded_rectangle([0,0,int(W*prog),16], radius=8, fill=(255,30,80))
    return np.array(img)

progress_clip = ImageClip(make_prog_frame, duration=audio.duration).set_position((0, H-16))

# Final composite
video = CompositeVideoClip(clips + [progress_clip]).set_audio(audio)
tmp_video = "/tmp/short.mp4"
video.write_videofile(tmp_video, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None)
print(f"Video READY: {audio.duration:.2f}s - {len(chapters)} CHAPTERS - PRO GRAPHICS!")

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
                "title": f"{hook.replace(chr(10),' ')} #shorts",
                "description": f"{full_script}\n\n#shorts #viral #challenge Original commentary, no copyrighted footage. Follow for Part 2!",
                "tags": ["shorts","viral","challenge","100k","mrbeast"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(tmp_video, mimetype='video/mp4', resumable=True)
    )
    resp = req.execute()
    print(f"SUCCESS! VIRAL PRO 30 SEC: https://youtu.be/{resp['id']}")
else:
    print("Missing secrets")
