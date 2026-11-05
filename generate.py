import os, json, random, tempfile
from google import genai
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

print("=== MILO & PIP AUTO-MODEL FACTORY ===")

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = """Write a funny 70-word 【entity-Tom and Jerry¦canonical_name=Tom and Jerry】 style cartoon story for kids.
Characters: Milo orange cat in green sweater, Pip grey mouse in red cap.
Plot: They are washing a red toy car with bubbles, slapstick, funny fall, happy ending.
Return ONLY JSON: {"title": "Short title", "story": "story text"}"""

# Try every model Google has - one will work
models_to_try = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-001",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-002"
]

ep = None
for model_name in models_to_try:
    try:
        print(f"Trying model: {model_name}")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        text = response.text.replace('```json','').replace('```','').strip()
        ep = json.loads(text)
        print(f"WORKING MODEL FOUND: {model_name} -> {ep['title']}")
        break
    except Exception as e:
        print(f"Model {model_name} failed: {e}")
        continue

if not ep:
    raise Exception("All Gemini models failed - check GOOGLE_API_KEY")

# Voice
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=ep['story'] + " Follow Milo and Pip!", lang='en', slow=False).save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)

# Real cartoon frame
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
