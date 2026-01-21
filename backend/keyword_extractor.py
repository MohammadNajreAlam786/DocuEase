from keybert import KeyBERT

kw_model = KeyBERT()

def extract_keywords(text):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=8
    )

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw, _ in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)

    return unique_keywords
