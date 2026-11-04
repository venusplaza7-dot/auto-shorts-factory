import os, tempfile, random
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip

print("=== FINAL FACTORY ===")

ideas = [
    "Beat the basketball challenge win 100 thousand dollars! What happened next shocked everyone!",
    "【entity-Squid Game¦canonical_name=Squid Game】 secrets revealed! How the biggest YouTuber keeps you watching till the end!",
    "I spent 50 hours in a crazy challenge and won!"
]
script = random.choice(ideas)
print(f"Script: {script}")

tmp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
gTTS(text=script, lang='en').save(tmp_audio)
audio = AudioFileClip(tmp_audio)
print(f"Audio duration: {audio.duration}")

bg = ColorClip(size=(1080,1920), color=(15,15,15), duration=audio.duration)
video = CompositeVideoClip([bg]).set_audio(audio)
tmp_video = "/tmp/short.mp4"
video.write_videofile(tmp_video, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', logger=None)
print(f"Video done: {tmp_video}")

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

if CLIENT_ID and REFRESH_TOKEN:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri="https://oauth2.googleapis.com/token",
                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        scopes=['https://www.googleapis.com/auth/youtube.upload'])
    youtube = build('youtube', 'v3', credentials=creds)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Viral Challenge Breakdown #shorts",
                "description": "Original commentary, no copyrighted footage #shorts",
                "tags": ["shorts","viral"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(tmp_video, mimetype='video/mp4', resumable=True)
    )
    resp = request.execute()
    print(f"SUCCESS! https://youtu.be/{resp['id']}")
else:
    print("Missing secrets - video made but not uploaded")
