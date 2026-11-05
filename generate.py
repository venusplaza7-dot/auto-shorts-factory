import requests, os, time, json, random
from moviepy.editor import *

# 1. Pick episode
with open('episodes.json') as f:
    ep = random.choice(json.load(f))

# 2. Generate real cartoon image (or use your saved milo.png as ref)
# Use Stable Diffusion API or upload reference image to Kling

# 3. Call Kling to turn image -> REAL video (this is the key)
# This gives you crystal clear mp4 with motion
kl = requests.post("https://api.kling.com/v1/video",
  headers={"Authorization": f"Bearer {os.getenv('KLING_API_KEY')}"},
  json={"image": "base64_of_your_cartoon_image", "prompt": ep['video_prompt'], "duration": 5}
)
video_url = kl.json()['video_url']
# download video -> real_cartoon.mp4

# 4. Add audio + music + make 28 sec by looping / adding 2 clips
audio = AudioFileClip("voice.mp3") # from gTTS of ep['story']
video = VideoFileClip("real_cartoon.mp4").loop(duration=audio.duration)
final = video.set_audio(audio)
final.write_videofile("short.mp4", fps=30)
