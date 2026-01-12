from fpdf import FPDF

def image_to_pdf(img_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(img_path, x=10, y=10, w=190)
    path = img_path.replace(".png",".pdf")
    pdf.output(path)
    return path
