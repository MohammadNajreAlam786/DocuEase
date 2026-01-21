import pdfplumber
import re
from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def chunk_text(text, max_words=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks

def extract_sections(text):
    sections = {}
    current_section = "Overview"
    sections[current_section] = ""

    lines = text.split("\n")

    for line in lines:
        clean = line.strip()

        # Detect headings (simple & effective)
        if (
    clean.isupper()
    or clean.lower().startswith((
        "introduction",
        "abstract",
        "methodology",
        "proposed",
        "system",
        "results",
        "discussion",
        "conclusion"
    ))
    or re.match(r"^\d+(\.\d+)*\s+", clean)
):

            current_section = clean.title()
            sections[current_section] = ""
        else:
            sections[current_section] += clean + " "

    return sections