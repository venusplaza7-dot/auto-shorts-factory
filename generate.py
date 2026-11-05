import os, json, random, tempfile
from google import genai
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

print("=== MILO & PIP NEW GENAI PACKAGE ===")

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = """Write a funny 70-word 【entity-Tom and Jerry¦canonical_name=Tom and Jerry】 style cartoon story for kids.
Characters: Milo orange cat in green sweater, Pip grey mouse in red cap.
Plot: They are washing a red toy car with bubbles, slapstick, funny fall, happy ending.
Return ONLY JSON: {"title": "Short title", "story": "story text"}"""

response = client.models.generate_content(
    model="gemini-3.8-flash-lite",
    contents=prompt
)
text = response.text.replace('```json','').replace('```','').strip()
ep = json.loads(text)
print(f"GENERATED: {ep['title']}")

# Voice + moving cartoon (same as before)
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=ep['story'] + " Follow Milo and Pip!", lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)

W,H = 1080,1920
img = Image.new('RGB', (W,H), (135,206,235))
draw = ImageDraw.Draw(img)
for _ in range(30):
    x,y = random.randint(0,W), random.randint(0,H)
    draw.ellipse([x,y,x+60,y+60], fill=(255,255,255,180), outline=(200,230,255))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
draw.text((50, 1400), ep['title'][:30], fill="white", font=font, stroke_width=4, stroke_fill="black")
img.save("real_cartoon_frame.jpg")

clip = ImageClip("real_cartoon_frame.jpg", duration=audio.duration)
clip = clip.resize(lambda t: 1 + 0.05 * t / audio.duration)
final = clip.set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac')

print(f"DONE {os.path.getsize('short.mp4')} bytes - {ep['title']}")
