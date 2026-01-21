from transformers import pipeline

# 🚀 Faster distilled summarization model
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1
)

IMPORTANT_SECTIONS = (
    "abstract",
    "introduction",
    "methodology",
    "method",
    "proposed",
    "system",
    "results",
    "discussion",
    "conclusion"
)

# ---------- ADAPTIVE LENGTH CONTROL ----------
def adaptive_lengths(text, max_cap=160):
    words = len(text.split())
    max_len = min(max_cap, max(50, int(words * 0.55)))
    min_len = max(25, int(words * 0.25))
    return max_len, min_len


# ---------- SECTION-AWARE SUMMARY ----------
def summarize_sections(sections):
    section_summaries = {}

    for title, content in sections.items():
        title_lower = title.lower()

        if not any(key in title_lower for key in IMPORTANT_SECTIONS):
            continue

        if len(content.split()) < 40:
            continue

        try:
            max_len, min_len = adaptive_lengths(content)

            result = summarizer(
                content[:1600],   # smaller context = faster
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )

            section_summaries[title] = result[0]["summary_text"]

        except Exception as e:
            print(f"Section '{title}' failed:", e)

    return section_summaries


# ---------- MERGE IMPORTANT SECTION SUMMARIES ----------
def merge_section_summaries(section_summaries):
    if not section_summaries:
        return (
            "The document does not contain enough structured content "
            "to generate a meaningful summary."
        )

    combined = " ".join(section_summaries.values())

    try:
        max_len, min_len = adaptive_lengths(combined, max_cap=200)

        result = summarizer(
            combined[:1800],
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        return result[0]["summary_text"]

    except Exception as e:
        print("Final merge failed:", e)
        return combined[:400]
