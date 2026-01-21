from transformers import pipeline

_translator = None

def get_translator(src, tgt):
    global _translator
    if _translator is None:
        model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        _translator = pipeline("translation", model=model_name)
    return _translator


def translate_text(text, src_lang, tgt_lang):
    translator = get_translator(src_lang, tgt_lang)

    chunks = [text[i:i+400] for i in range(0, len(text), 400)]
    translated = []

    for chunk in chunks:
        result = translator(chunk)
        translated.append(result[0]["translation_text"])

    return " ".join(translated)