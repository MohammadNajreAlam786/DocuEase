from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from utils import extract_text_from_pdf
from summarizer import summarize_text
from keyword_extractor import extract_keywords

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend (Vercel)
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "DocuEase backend running"}

@app.post("/upload")
async def upload(file: UploadFile):
    text = extract_text_from_pdf(file.file)

    # HARD LIMIT to avoid memory crash
    text = text[:2000]

    summary = summarize_text(text)
    keywords = extract_keywords(summary)

    return {
        "summary": summary,
        "keywords": keywords
    }
