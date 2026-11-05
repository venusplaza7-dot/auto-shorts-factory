from PIL import Image
Image.ANTIALIAS = Image.Resampling.LANCZOS

import json, random, tempfile
from gtts import gTTS
from moviepy.editor import *
from PIL import ImageDraw, ImageFont

print("=== MILO & PIP REAL CARTOON - CLEAN NO GLITCH ===")

# For now use episodes.json - will be Milo Carries Groceries Tower etc
with open('episodes.json') as f:
    ep = random.choice(json.load(f))

title = ep.get('title', 'Milo Carries Groceries Tower')
story = ep.get('story', 'Milo tries to carry all grocery bags inside in one trip to be a hero. He stacks bags on head, arms, tail. Pip balances on top holding eggs. Can they get eggs to kitchen?')

tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story + " Follow Milo and Pip!", lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)

# USE REAL CARTOON IMAGE - not blue dots
# Save the car wash image I gave you as milo_real.jpg in repo
# Or generate new one with PixVerse Kling 4.0 (50 free/day) - your screenshot
try:
    bg = Image.open("milo_real.jpg").resize((1080,1920))
except:
    # Fallback - blue with bubbles (your current clean version)
    bg = Image.new('RGB', (1080,1920), (135,206,235))
    draw = ImageDraw.Draw(bg)
    for _ in range(40):
        x,y = random.randint(0,1080), random.randint(0,1920)
        draw.ellipse([x,y,x+50,y+50], fill=(255,255,255,200))

draw = ImageDraw.Draw(bg)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 65)
# Wrap title
words = title.split()
lines, line = [], ""
for w in words:
    if len(line + " " + w) < 22:
        line += " " + w
    else:
        lines.append(line); line = w
lines.append(line)
y = 1450
for l in lines:
    draw.text((50, y), l.strip(), fill="white", font=font, stroke_width=4, stroke_fill="black")
    y += 75

bg.save("frame.jpg")

clip = ImageClip("frame.jpg", duration=audio.duration)
final = clip.set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac')

print(f"DONE CLEAN REAL - {audio.duration:.1f}s - {title}")
