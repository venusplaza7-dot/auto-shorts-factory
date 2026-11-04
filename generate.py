# FINAL - Copyright Safe - No 【entity-MrBeast¦canonical_name=MrBeast】 footage used
# Creates original commentary Short from trending title
import os
from gtts import gTTS
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("=== SHORTS FACTORY V3 FINAL ===")

# === STEP 1: Generate script (copyright safe - original commentary) ===
# Later we will auto-scrape trending titles, for now using 【entity-MrBeast¦canonical_name=MrBeast】 example
original_viral_title = "Beat 【entity-LeBron¦canonical_name=LeBron】 In Basketball, Win $100,000 - MrBeast"
script = f"Breaking: {original_viral_title}. 【entity-LeBron¦canonical_name=LeBron】 said I'm no 【entity-Steph Curry¦canonical_name=Steph Curry】 but he almost lost this 1 minute shootout for 100k. Here's my breakdown of what actually happened and why it went viral."

print(f"Script: {script}")

# === STEP 2: Voiceover ===
print("Generating voice...")
tts = gTTS(text=script, lang='en', tld='com')
tts.save('/tmp/voice.mp3')
audio = AudioFileClip('/tmp/voice.mp3')
print(f"Voice duration: {audio.duration}s")

# === STEP 3: Create 9:16 video (no copyrighted footage) ===
print("Creating 9:16 video...")
bg = ColorClip(size=(1080, 1920), color=(10, 10, 10), duration=audio.duration)

# Big caption style like MrBeast Shorts
txt = TextClip(script, fontsize=65, color='white', stroke_color='black', 
               stroke_width=3, method='caption', size=(900, None))
txt = txt.set_duration(audio.duration).set_position('center')

final = CompositeVideoClip([bg, txt]).set_audio(audio)
output_path = '/tmp/final_short.mp4'
final.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', logger=None)
print(f"Video created: {output_path}")

# === STEP 4: Auto-upload to YouTube ===
print("Uploading to YouTube...")
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')

if not REFRESH_TOKEN:
    print("No REFRESH_TOKEN found - skipping upload (video saved in /tmp)")
else:
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=['https://www.googleapis.com/auth/youtube.upload']
    )
    youtube = build('youtube', 'v3', credentials=creds)
    
    request = youtube.videos().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': f"{original_viral_title} - My Reaction #shorts",
                'description': f"My original commentary on {original_viral_title}. No copyrighted footage used. Original analysis. #shorts #【entity-mrbeast¦canonical_name=MrBeast】 #【entity-lebron¦canonical_name=LeBron】",
                'tags': ['shorts', '【entity-mrbeast¦canonical_name=MrBeast】', '【entity-lebron¦canonical_name=LeBron】', 'reaction', 'commentary'],
                'categoryId': '22'
            },
            'status': {
                'privacyStatus': 'private',  # Change to 'public' after you test
                'selfDeclaredMadeForKids': False
            }
        },
        media_body=MediaFileUpload(output_path, mimetype='video/mp4', resumable=True)
    )
    response = request.execute()
    video_id = response['id']
    print(f"SUCCESS! Uploaded: https://youtu.be/{video_id}")
    print(f"Video is PRIVATE - Go to YouTube Studio to make it PUBLIC")

print("=== DONE ===")
