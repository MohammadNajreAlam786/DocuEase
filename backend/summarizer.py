from transformers import pipeline

# Lightweight + fast model (free-tier safe)
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1
)

def summarize_text(text):
    text = text[:1200]  # extra safety
    result = summarizer(
        text,
        max_length=130,
        min_length=50,
        do_sample=False
    )
    return result[0]["summary_text"]
