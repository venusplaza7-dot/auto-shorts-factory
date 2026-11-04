import os, random, requests, tempfile
from gtts import gTTS
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip

# --- 1. GET VIRAL IDEA (Title only, no download) ---
YT_API_KEY = os.getenv("YT_API_KEY")
titles = ["【entity-MrBeast¦canonical_name=MrBeast】 Squid Game Secrets", "【entity-LeBron¦canonical_name=LeBron】 vs 【entity-MrBeast¦canonical_name=MrBeast】 $100k Challenge", "Viral YouTube Tricks 2025"]
topic = random.choice(titles)
print(f"Topic: {topic}")

# Original script (copyright safe)
script = f"This is insane! {topic}. Did you know 【entity-MrBeast¦canonical_name=MrBeast】 spent millions on this video? But the real secret is how he keeps you watching till the end. If you can beat this challenge, you win! Subscribe for more viral secrets!"

# --- 2. MAKE VOICE ---
tts = gTTS(text=script, lang='en')
tmp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
tts.save(tmp_audio)
audio = AudioFileClip(tmp_audio)
print(f"Audio made: {audio.duration}s")

# --- 3. MAKE VIDEO (1080x1920 Short) ---
W, H = 1080, 1920
bg = ColorClip(size=(W, H), color=(15,15,15), duration=audio.duration)

# Big text
txt = TextClip(script[:120]+"...", fontsize=70, color='white', font='Arial-Bold', method='caption', size=(900, None))
txt = txt.set_position('center').set_duration(audio.duration)

video = CompositeVideoClip([bg, txt]).set_audio(audio)

tmp_video = "/tmp/final_short.mp4"
video.write_videofile(tmp_video, fps=24, codec='libx264', audio_codec='aac')
print(f"Video created: {tmp_video}")

# --- 4. UPLOAD TO YOUTUBE (via OAuth) ---
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

if CLIENT_ID and REFRESH_TOKEN:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri="https://oauth2.googleapis.com/token",
                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    youtube = build('youtube', 'v3', credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": f"{topic} #shorts",
                "description": f"Original commentary about {topic}. #mrbeast #viral #shorts",
                "tags": ["shorts","mrbeast","viral"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "private", # Change to public after check
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=tmp_video
    )
    response = request.execute()
    vid = response['id']
    print(f"SUCCESS! Uploaded: https://youtu.be/{vid}")
else:
    print("No OAuth secrets set — video created but not uploaded (test mode)")
