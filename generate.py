import os, json, random, tempfile
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

print("=== MILO & PIP FACTORY - GREEN BUILD NO API ===")

# Use local episodes - guaranteed green
with open('episodes.json') as f:
    episodes = json.load(f)
ep = random.choice(episodes)

title = ep.get('title', 'Milo Washes Car')
story = ep.get('story', 'Milo washes car with bubbles and Pip helps. Funny splash!')
print(f"EP: {title}")

# Voice
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story + " Follow Milo and Pip!", lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)
print(f"Audio {audio.duration:.2f}s")

# Cartoon frame with bubbles
W,H = 1080,1920
img = Image.new('RGB', (W,H), (135,206,235))
draw = ImageDraw.Draw(img)
for _ in range(30):
    x,y = random.randint(0,W), random.randint(0,H)
    draw.ellipse([x,y,x+60,y+60], fill=(255,255,255,180), outline=(200,230,255))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
draw.text((50, 1400), title[:30], fill="white", font=font, stroke_width=4, stroke_fill="black")
img.save("frame.jpg")

clip = ImageClip("frame.jpg", duration=audio.duration)
clip = clip.resize(lambda t: 1 + 0.05 * t / audio.duration)
final = clip.set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac')

print(f"DONE GREEN {os.path.getsize('short.mp4')} bytes")
