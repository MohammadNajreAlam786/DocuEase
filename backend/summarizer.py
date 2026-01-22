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


def merge_section_summaries(section_summaries):
    if not section_summaries:
        return "Document too short to summarize."

    summarizer = get_summarizer()
    combined = " ".join(section_summaries.values())

    result = summarizer(
        combined[:2000],
        max_length=160,
        min_length=80,
        do_sample=False
    )

    return result[0]["summary_text"]