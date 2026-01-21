from transformers import pipeline

# Cache translators (important for performance)
TRANSLATORS = {}

def get_translator(src, tgt):
    key = f"{src}-{tgt}"
    if key not in TRANSLATORS:
        model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        TRANSLATORS[key] = pipeline("translation", model=model_name)
    return TRANSLATORS[key]


def translate_text(text, src_lang, tgt_lang):
    translator = get_translator(src_lang, tgt_lang)

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    translated = []

    for chunk in chunks:
        result = translator(chunk)
        translated.append(result[0]["translation_text"])

    return " ".join(translated)
