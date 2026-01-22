from keybert import KeyBERT

_kw_model = None

def get_kw_model():
    global _kw_model
    if _kw_model is None:
        _kw_model = KeyBERT()
    return _kw_model

def extract_keywords(text):
    kw_model = get_kw_model()
    keywords = kw_model.extract_keywords(text, top_n=8)
    return list(dict.fromkeys([kw[0] for kw in keywords]))