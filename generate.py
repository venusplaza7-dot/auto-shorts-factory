from PIL import Image
Image.ANTIALIAS = Image.Resampling.LANCZOS

import tempfile
from gtts import gTTS
from moviepy.editor import *

# Your 5 sec REAL MOVIE from PixVerse
movie_5sec = VideoFileClip("pizza_movie_real.mp4")  # your 5 sec explosion

# Your story (70 words = 28 sec audio)
story = "Milo tries to make giant pizza but dough gets stuck to ceiling. It stretches and stretches and then BOOM flour explosion everywhere. Milo covered in flour, Pip covered in sauce. What a pizza disaster. Follow Milo and Pip for more!"

tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=story, lang='en').save(tmp)
audio = AudioFileClip(tmp)  # 28 sec

# LOOP 5 sec movie to 28 sec = REAL MOVIE for full Shorts
movie_28sec = movie_5sec.loop(duration=audio.duration)
final = movie_28sec.set_audio(audio)
final.write_videofile("short.mp4", fps=30)

print(f"5 sec -> 28 sec MOVIE DONE - Kids watch full 28 sec!")
