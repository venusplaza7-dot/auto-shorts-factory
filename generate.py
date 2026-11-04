import os, requests
from moviepy.editor import *
from gtts import gTTS

PEXELS_KEY = os.getenv('PEXELS_API_KEY')
YT_KEY = os.getenv('YT_API_KEY')

def get_trending_titles():
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=US&maxResults=3&key={YT_KEY}"
    data = requests.get(url).json()
    return [item['snippet']['title'] for item in data['items']]

def rewrite_script(original):
    # COPYRIGHT SAFE: We never use original video, only rewrite idea
    return f"Breaking down: {original}. This went viral because... Here's my analysis and what actually happened..."

def get_stock_video(query="basketball"):
    headers = {"Authorization": PEXELS_KEY}
    r = requests.get(f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait", headers=headers)
    video_url = r.json()['videos'][0]['video_files'][0]['link']
    video_data = requests.get(video_url).content
    with open('/tmp/stock.mp4','wb') as f: f.write(video_data)
    return '/tmp/stock.mp4'

def make_short(script, stock_path, output):
    # Voice
    tts = gTTS(script, lang='en')
    tts.save('/tmp/voice.mp3')
    audio = AudioFileClip('/tmp/voice.mp3')
    
    # Video: 9:16 stock + text
    clip = VideoFileClip(stock_path).subclip(0, audio.duration)
    clip = clip.resize(height=1920).crop(width=1080, x_center=clip.w/2)
    txt = TextClip(script[:80]+"...", fontsize=60, color='white', stroke_color='black', stroke_width=2, method='caption', size=(900,None)).set_duration(audio.duration).set_position('center')
    final = CompositeVideoClip([clip, txt]).set_audio(audio)
    final.write_videofile(output, fps=24)

# MAIN LOOP - GitHub Action runs this
for title in get_trending_titles():
    script = rewrite_script(title)
    stock = get_stock_video("basketball")
    make_short(script, stock, f"/tmp/{title[:10]}.mp4")
    # Then call your /api/upload endpoint to post
