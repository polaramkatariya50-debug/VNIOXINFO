from PIL import Image

def image_to_pdf(img_path):
    pdf = img_path.replace(".png", ".pdf")
    Image.open(img_path).convert("RGB").save(pdf, "PDF", resolution=300.0)
    return pdf
