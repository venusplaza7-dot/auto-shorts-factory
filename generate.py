# MUST BE FIRST - FIXES PILLOW 11 + MOVIEPY 1.0.3
from PIL import Image
Image.ANTIALIAS = Image.Resampling.LANCZOS

import json, random, tempfile
from gtts import gTTS
from moviepy.editor import *
from PIL import ImageDraw, ImageFont

print("=== MILO & PIP - NO RESIZE GLITCH - FINAL ===")

with open('episodes.json') as f:
    ep = random.choice(json.load(f))

title = ep.get('title', 'Milo Does Laundry Again')
story = ep.get('story', 'Milo tries laundry again but puts too many clothes in the washing machine. Bubbles fly everywhere. Pip gets sucked into a T-shirt. Clothes fly out and land on Milos head.')

print(f"EP: {title}")

# Voice
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story + " Follow Milo and Pip!", lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)

# Clean frame - like your 0.0s but NO distortion
W,H = 1080,1920
img = Image.new('RGB', (W,H), (135,206,235))
draw = ImageDraw.Draw(img)
for _ in range(40):
    x,y = random.randint(0,W), random.randint(0,H)
    draw.ellipse([x,y,x+50,y+50], fill=(255,255,255,200))

# FIXED TEXT - wrapped, not stretching
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
# Wrap title so it doesn't cut off
words = title.split()
lines = []
line = ""
for w in words:
    if len(line + " " + w) < 20:
        line += " " + w
    else:
        lines.append(line)
        line = w
lines.append(line)
y = 1300
for l in lines:
    draw.text((60, y), l.strip(), fill="white", font=font, stroke_width=3, stroke_fill="black")
    y += 85

img.save("clean_frame.jpg")

# NO RESIZE LAMBDA - STATIC = NO GLITCH
clip = ImageClip("clean_frame.jpg", duration=audio.duration)
final = clip.set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac')

print(f"DONE CLEAN - NO LINES - {audio.duration:.1f}s")
