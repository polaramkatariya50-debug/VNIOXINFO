from PIL import Image

def image_to_pdf(img_path):
    pdf_path = img_path.replace(".png", ".pdf")
    Image.open(img_path).convert("RGB").save(pdf_path)
    return pdf_path
