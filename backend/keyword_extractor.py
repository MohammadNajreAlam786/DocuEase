from keybert import KeyBERT

kw_model = KeyBERT(model="all-MiniLM-L6-v2")

def extract_keywords(text):
    keywords = kw_model.extract_keywords(
        text,
        top_n=8,
        stop_words="english"
    )

    # remove duplicates & normalize
    unique = []
    for kw, _ in keywords:
        kw = kw.lower()
        if kw not in unique:
            unique.append(kw)

    return unique
