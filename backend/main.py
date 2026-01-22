from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from utils import extract_text_from_pdf
from keyword_extractor import extract_keywords
from summarizer import get_summarizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "DocuEase backend running"}

@app.post("/upload")
async def upload(file: UploadFile):
    # Extract text
    text = extract_text_from_pdf(file.file)

    # HARD LIMIT for Render free tier
    text = text[:2000]

    summarizer = get_summarizer()
    result = summarizer(
        text,
        max_length=140,
        min_length=70,
        do_sample=False
    )

    summary = result[0]["summary_text"]
    keywords = extract_keywords(summary)

    return {
        "summary": summary,
        "keywords": keywords
    }