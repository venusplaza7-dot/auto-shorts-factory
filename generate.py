from PIL import Image
Image.ANTIALIAS = Image.Resampling.LANCZOS

import json, random, tempfile
from gtts import gTTS
from moviepy.editor import *
from PIL import ImageDraw, ImageFont

with open('episodes.json') as f:
    ep = random.choice(json.load(f))

# Map title to real image
title = ep['title']
if "Laundry" in title:
    bg_path = "laundry.jpg"
elif "Groceries" in title:
    bg_path = "groceries.jpg"
elif "Dishes" in title:
    bg_path = "dishes.jpg"
else:
    bg_path = "laundry.jpg"

# ... same clean code but bg = Image.open(bg_path)
