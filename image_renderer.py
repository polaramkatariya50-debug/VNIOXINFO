from PIL import Image, ImageDraw, ImageFont
import textwrap, os, re, hashlib
from config import *

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
CACHE_DIR = "/tmp/osint_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def mask_sensitive(text):
    if not ENABLE_BLUR:
        return text
    patterns = [
        r"\b\d{10}\b",
        r"\b\d{12}\b",
        r"\b\d{13,16}\b",
        r"\b\d{5}-\d{7}-\d\b",
    ]
    for p in patterns:
        text = re.sub(p, "████████", text)
    return text

def text_to_image(text):
    text = mask_sensitive(text)
    key = hashlib.md5(text.encode()).hexdigest()
    path = f"{CACHE_DIR}/{key}.png"
    if CACHE_ENABLED and os.path.exists(path):
        return path

    bg = "#0d1117" if THEME == "dark" else "#ffffff"
    fg = "#c9d1d9" if THEME == "dark" else "#000000"

    try:
        font = ImageFont.truetype(FONT_PATH, 18)
    except:
        font = ImageFont.load_default()

    lines = []
    for l in text.split("\n"):
        lines += textwrap.wrap(l, 95) or [""]

    width = 1200
    line_h = 24
    height = 30 + line_h * len(lines) + 40

    img = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(img)

    y = 20
    for l in lines:
        d.text((20, y), l, font=font, fill=fg)
        y += line_h

    if ENABLE_WATERMARK:
        d.text((width-360, height-30), WATERMARK_TEXT, font=font, fill="#777777")

    img.save(path)
    return path
