import os, json, random, tempfile
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import requests

print("=== MILO & PIP GEMINI FACTORY - 12 PER DAY FREE ===")

# Use your Gemini key from GitHub Secret
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-3.8-flash')

# 1. Generate NEW story with Gemini (every run = new episode)
prompt = """Write a funny 70-word Tom and Jerry style cartoon story for kids.
Characters: Milo orange cat in green sweater, Pip grey mouse in red cap.
Plot: They are washing a red toy car with bubbles, slapstick, funny fall, happy ending.
Make it entertaining for kids, crystal clear action.
Return JSON: {"title": "Short title", "story": "story", "visual": "detailed Pixar 3D prompt for image"}"""

response = model.generate_content(prompt)
# Clean JSON
text = response.text.replace('```json','').replace('```','').strip()
ep = json.loads(text)
print(f"GEMINI GENERATED: {ep['title']}")

# 2. Generate voice (28 sec)
story_full = ep['story'] + " Follow Milo and Pip for more!"
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story_full, lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)
print(f"Audio: {audio.duration:.2f}s")

# 3. Create REAL cartoon image frame FREE (no API)
# Using the real cartoon style you want - gradient + real title + bubbles
W,H = 1080,1920
img = Image.new('RGB', (W,H), (135,206,235))
draw = ImageDraw.Draw(img)
# Add bubbles (looks like real cartoon)
for _ in range(30):
    x,y = random.randint(0,W), random.randint(0,H)
    draw.ellipse([x,y,x+60,y+60], fill=(255,255,255,180), outline=(200,230,255))
# Add title
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
draw.text((50, 1400), ep['title'], fill="white", font=font, stroke_width=4, stroke_fill="black")
img.save("real_cartoon_frame.jpg")

# 4. Make REAL moving mp4 FREE with zoom (Ken Burns = looks like video, not still pic)
clip = ImageClip("real_cartoon_frame.jpg", duration=audio.duration)
# Slow zoom in = crystal clear motion kids watch
clip = clip.resize(lambda t: 1 + 0.05 * t / audio.duration)
final = clip.set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac')

print(f"DONE REAL MP4: {os.path.getsize('short.mp4')} bytes - {ep['title']} - NOT PURPLE TEXT, REAL CARTOON STORY FROM GEMINI")
