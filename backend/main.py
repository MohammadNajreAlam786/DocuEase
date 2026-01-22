# main.py
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_text_from_pdf
from summarizer import summarize_sections, merge_section_summaries
from keyword_extractor import extract_keywords
from utils import extract_sections
from utils import detect_language
from translator import translate_text

app = FastAPI()

app.state.document_chunks = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile):
    # 1. Extract text
    text = extract_text_from_pdf(file.file)

    # 🚨 HARD LIMIT for free tier (IMPORTANT)
    MAX_CHARS = 6000
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]


    # 2. Detect language
    original_language = detect_language(text[:1000])

    # 3. Translate to English if needed
    if original_language != "en":
        text_en = translate_text(text, original_language, "en")
    else:
        text_en = text

    # 4. Extract sections
    sections = extract_sections(text_en)

    # 5. Section-wise summaries (IMPORTANT SECTIONS ONLY)
    #section_summaries_en = summarize_sections(sections)
    # 6. Merge into final academic-style summary
    #final_summary_en = merge_section_summaries(section_summaries_en)
    section_summaries_en = {}
    final_summary_en = merge_section_summaries(
        {"Document Summary": text_en[:1500]}
    )

    # 7. Translate back if needed
    if original_language != "en":
        final_summary = translate_text(final_summary_en, "en", original_language)
        section_summaries = {
            title: translate_text(content, "en", original_language)
            for title, content in section_summaries_en.items()
        }
    else:
        final_summary = final_summary_en
        section_summaries = section_summaries_en

    # 8. Keywords (from final summary)
    keywords = extract_keywords(final_summary)

    return {
        "language": original_language,
        "summary": final_summary,
        "section_summaries": section_summaries,
        "keywords": keywords
    }