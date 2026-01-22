from transformers import pipeline

# -------------------------------------------------
# Lazy-loaded summarizer (CRITICAL for free tier)
# -------------------------------------------------
_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        print("Loading summarization model...")
        _summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            device=-1
        )
    return _summarizer


IMPORTANT_SECTIONS = (
    "abstract",
    "introduction",
    "methodology",
    "proposed",
    "system",
    "results",
    "discussion",
    "conclusion"
)

# -------------------------------------------------
# Section-wise summarization
# -------------------------------------------------
def summarize_sections(sections):
    summarizer = get_summarizer()
    section_summaries = {}

    for title, content in sections.items():
        title_lower = title.lower()

        if not any(key in title_lower for key in IMPORTANT_SECTIONS):
            continue

        if len(content.split()) < 50:
            continue

        try:
            result = summarizer(
                content[:1500],
                max_length=120,
                min_length=50,
                do_sample=False
            )
            section_summaries[title] = result[0]["summary_text"]
        except Exception as e:
            print(f"Section '{title}' failed:", e)

    return section_summaries


# -------------------------------------------------
# Merge section summaries into final summary
# -------------------------------------------------
def merge_section_summaries(section_summaries):
    if not section_summaries:
        return "The document does not contain enough structured content to generate a summary."

    summarizer = get_summarizer()
    combined = " ".join(section_summaries.values())

    try:
        result = summarizer(
            combined[:1800],
            max_length=150,
            min_length=80,
            do_sample=False
        )
        return result[0]["summary_text"]
    except Exception as e:
        print("Final summary failed:", e)
        return combined[:400]
