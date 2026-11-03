
import requests, os
from moviepy.editor import *
from gtts import gTTS

# 1. FIND VIRAL TOPICS (without downloading copyrighted video)
# We use YouTube API to get TRENDING TITLES only
def get_viral_ideas():
    YT_API_KEY = os.getenv("YT_API_KEY")
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=US&maxResults=10&key={YT_API_KEY}"
    data = requests.get(url).json()
    # Example: "Beat 【entity-LeBron¦canonical_name=LeBron】 In Basketball, Win $100,000"
    return [item['snippet']['title'] for item in data['items']]

# 2. REWRITE AS ORIGINAL SCRIPT (This is what makes it copyright-safe)
# Using OpenAI / Groq free API
def rewrite_script(original_title):
    # You are NOT copying the video. You are making commentary.
    prompt = f"""
    Original viral title: {original_title}
    Write a 25-second YouTube Shorts script.
    Style: Fast-paced, shocking, commentary.
    Example: "【entity-MrBeast¦canonical_name=MrBeast】 just challenged 【entity-LeBron¦canonical_name=LeBron】 James to a 1v1 for 100k...
    Here's what happened and why LeBron almost lost..."
    Make it original, add your own opinion. No copy-paste.
    """
    # Call OpenAI API here
    return "【entity-MrBeast¦canonical_name=MrBeast】 just challenged 【entity-LeBron¦canonical_name=LeBron】 for $100,000... and 【entity-LeBron¦canonical_name=LeBron】 said 'I'm no 【entity-Steph Curry¦canonical_name=Steph Curry】'... Here's why this 1-minute shootout shocked everyone..."

# 3. BUILD VIDEO FROM STOCK + AI (No copyrighted footage)
def build_short(script_text, output_path):
    # a) Voiceover
    tts = gTTS(text=script_text, lang='en', tld='us')
    tts.save("voice.mp3")
    
    # b) Stock footage - Pexels API (copyright free)
    # Search: basketball, 【entity-lebron¦canonical_name=LeBron】, 【entity-mrbeast¦canonical_name=MrBeast】 style
    # Download free vertical videos from Pexels
    
    # c) Create 9:16 video
    audioclip = AudioFileClip("voice.mp3")
    # Use stock clips or AI images
    videoclip = ColorClip(size=(1080, 1920), color=(0,0,0), duration=audioclip.duration)
    txt = TextClip(script_text, fontsize=60, color='white', method='caption', size=(900, None)).set_duration(audioclip.duration).set_position('center')
    
    final = CompositeVideoClip([videoclip, txt]).set_audio(audioclip)
    final.write_videofile(output_path, fps=24)

# MAIN
for title in get_viral_ideas()[:3]:
    script = rewrite_script(title)
    build_short(script, f"output/{title[:20]}.mp4")
