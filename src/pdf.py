""" This module provides functions to extract text from PDF files using OCR. """

import os
import PyPDF2
import pytesseract  # type: ignore
import requests
from pdf2image import convert_from_path


def download_tesseract_lang_data(lang):
    """Download Tesseract language data if not already present."""
    tessdata_dir = os.path.join(os.getenv("TESSDATA_PREFIX", ""), "tessdata")
    if not os.path.exists(tessdata_dir):
        os.makedirs(tessdata_dir)

    lang_file = os.path.join(tessdata_dir, f"{lang}.traineddata")
    if not os.path.exists(lang_file):
        url = f"https://github.com/tesseract-ocr/tessdata_best/raw/main/{lang}.traineddata"
        r = requests.get(url, timeout=5000)
        with open(lang_file, "wb") as f:
            f.write(r.content)


def extract_text_and_images(input_pdf_path, dpi=300, lang="por") -> list[str] | None:
    """Extracts text from a PDF using tesseract OCR."""
    for l in lang.split("+"):
        download_tesseract_lang_data(l)
    # Convert PDF to images
    try:
        cache_file = os.path.splitext(input_pdf_path)[0] + "_ocr_cache.txt"
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_content = f.read().strip()
                if cached_content:
                    return cached_content.split("\n\n")
            except Exception as e:
                print("Failed to read cache, proceeding with OCR:", e)
        images = convert_from_path(input_pdf_path, dpi=dpi)
    except Exception as e:
        print("An error occurred while converting PDF to images:", e)
        print("Ensure Poppler is installed and added to PATH.")
        return None
    ocr_text_list = []
    for image in images:
        # Perform OCR on the image
        ocr_text = pytesseract.image_to_string(image, lang=lang)
        ocr_text_list.append(ocr_text.strip())
    cache_file = os.path.splitext(input_pdf_path)[0] + "_ocr_cache.txt"
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write("\n\n".join(ocr_text_list))
    except Exception as e:
        print("Failed to save cache:", e)
    return ocr_text_list


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
