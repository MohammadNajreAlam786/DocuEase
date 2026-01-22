from transformers import pipeline

# Cache translators so they load only once
TRANSLATORS = {}

def get_translator(src_lang, tgt_lang):
    key = f"{src_lang}-{tgt_lang}"

    if key not in TRANSLATORS:
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"

        TRANSLATORS[key] = pipeline(
            "translation",
            model=model_name,
            device=-1  # CPU only (IMPORTANT for Render)
        )

    return TRANSLATORS[key]


def translate_text(text, src_lang, tgt_lang):
    # Short-circuit if same language
    if src_lang == tgt_lang:
        return text

    translator = get_translator(src_lang, tgt_lang)

    # Chunk text to avoid OOM
    chunks = [text[i:i + 400] for i in range(0, len(text), 400)]
    translated = []

    for chunk in chunks:
        try:
            result = translator(chunk)
            translated.append(result[0]["translation_text"])
        except Exception as e:
            print("Translation error:", e)
            translated.append(chunk)  # fallback

    return " ".join(translated)