from transformers import pipeline

_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
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

def summarize_sections(sections):
    summarizer = get_summarizer()
    section_summaries = {}

    for title, content in sections.items():
        title_lower = title.lower()

        # only important sections
        if not any(k in title_lower for k in IMPORTANT_SECTIONS):
            continue

        if len(content.split()) < 50:
            continue

        result = summarizer(
            content[:1500],
            max_length=120,
            min_length=60,
            do_sample=False
        )

        section_summaries[title] = result[0]["summary_text"]

    return section_summaries