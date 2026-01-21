from keybert import KeyBERT
import spacy

kw_model = KeyBERT()
nlp = spacy.load("en_core_web_sm")

def normalize_keyword(kw):
    doc = nlp(kw.lower())
    return " ".join(
        token.lemma_
        for token in doc
        if token.pos_ in {"NOUN", "PROPN"}
    )

def extract_keywords(text, top_n=10):
    if not text or len(text.split()) < 30:
        return []

    raw_keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        use_mmr=True,
        diversity=0.7,
        top_n=top_n * 2  # extract more → filter better
    )

    seen = set()
    final_keywords = []

    for kw, _ in raw_keywords:
        normalized = normalize_keyword(kw)

        if not normalized:
            continue

        if normalized not in seen:
            seen.add(normalized)
            final_keywords.append(normalized.title())

        if len(final_keywords) >= top_n:
            break

    return final_keywords
