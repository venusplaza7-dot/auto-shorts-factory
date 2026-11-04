import os
from moviepy.editor import *
from gtts import gTTS

# No 【entity-Pexels¦canonical_name=Pexels】, No OpenAI, No Pixabay needed
def make_short():
    script = "MrBeast vs LeBron for $100k - shocking result. Here's my breakdown why LeBron almost lost this 1 minute shootout..."
    
    tts = gTTS(text=script, lang='en')
    tts.save('/tmp/voice.mp3')
    audio = AudioFileClip('/tmp/voice.mp3')
    
    # Just black background + text = no copyright, no API needed
    bg = ColorClip(size=(1080,1920), color=(10,10,10), duration=audio.duration)
    txt = TextClip(script, fontsize=60, color='white', method='caption', size=(900,None)).set_duration(audio.duration).set_position('center')
    
    final = CompositeVideoClip([bg, txt]).set_audio(audio)
    final.write_videofile('/tmp/final_short.mp4', fps=24)

make_short()
