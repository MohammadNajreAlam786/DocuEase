from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from utils import extract_text_from_pdf, extract_sections
from keyword_extractor import extract_keywords
from summarizer import summarize_sections, merge_section_summaries

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
    # 1. Extract text
    text = extract_text_from_pdf(file.file)

    # 2. HARD LIMIT (VERY IMPORTANT for Render free tier)
    text = text[:3000]

    # 3. Extract sections
    sections = extract_sections(text)

    # 4. Section-wise summaries
    section_summaries = summarize_sections(sections)

    # 5. Final merged summary
    final_summary = merge_section_summaries(section_summaries)

    # 6. Keywords from final summary
    keywords = extract_keywords(final_summary)

    return {
        "summary": final_summary,
        "keywords": keywords
    }