# DocuEase 📄

DocuEase is an AI-powered document understanding system that allows users to upload documents and automatically generate:
- Clean summaries
- Section-wise summaries
- Keywords
- Multilingual support

## Tech Stack
- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- NLP Models: HuggingFace Transformers (DistilBART)

## Features
- PDF document upload
- Academic-style summaries
- Section-wise accordion summaries
- Keyword extraction
- Multilingual document support
- Light/Dark mode UI

## How to Run Locally

### Backend
```bash
cd backend
uvicorn main:app --reload
