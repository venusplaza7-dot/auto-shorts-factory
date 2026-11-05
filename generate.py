import random, json, os, time, tempfile
from PIL import Image, ImageDraw
import numpy as np
from moviepy.editor import *
from gtts import gTTS

# Load episodes
try:
    with open('episodes.json') as f:
        EPISODES = json.load(f)
except:
    EPISODES = [{"title": "Milo Balances Laundry Tower", "visual_prompt": "Milo orange cat balancing towels", "motion_prompt": "cat walking"}]

episode = random.choice(EPISODES)
print(f"EPISODE: {episode['title']}")

# Pro background (V12 style, no cat PNG needed)
W, H = 1080, 1920
def make_bg(c1, c2):
    img = Image.new('RGB', (W,H), c1)
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = int(c1[0] + (c2[0]-c1[0])*y/H)
        g = int(c1[1] + (c2[1]-c1[1])*y/H)
        b = int(c1[2] + (c2[2]-c1[2])*y/H)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    return np.array(img)

# Generate audio + video (fallback pro version until Kling is wired)
tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=episode['title'], lang='en').save(tmp_mp3)
audio = AudioFileClip(tmp_mp3)

bg = make_bg((12,12,28),(88,28,88))
bg_clip = ImageClip(bg, duration=audio.duration)

txt = TextClip(episode['title'], fontsize=80, color='yellow', font='DejaVu-Sans-Bold', stroke_color='black', stroke_width=4, method='caption', size=(900,600)).set_duration(audio.duration).set_position('center')

final = CompositeVideoClip([bg_clip, txt]).set_audio(audio)
final.write_videofile("short.mp4", fps=30, codec='libx264', audio_codec='aac')
print("short.mp4 READY for 12/day factory")
