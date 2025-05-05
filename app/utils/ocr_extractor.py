from pdf2image import convert_from_path
import pytesseract

def extract_text_via_ocr(pdf_path: str) -> str:
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text
