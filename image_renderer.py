from PIL import Image, ImageDraw, ImageFont
import uuid

def text_to_image(text):
    img = Image.new("RGB", (1200, 2000), "black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    draw.multiline_text((20,20), text, fill="white", font=font)

    path = f"/tmp/{uuid.uuid4().hex}.png"
    img.save(path)
    return path
