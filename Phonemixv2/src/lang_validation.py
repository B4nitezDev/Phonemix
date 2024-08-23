from langdetect import detect, LangDetectException
from config.config import phonemize_config

def validate_language(text, expected_language):
    try:
        detected_language = detect(text)
    except LangDetectException:
        return False, "Could not detect the language of the text."
    
    languages = phonemize_config['lang_validation']
    
    # Verifica si el idioma esperado está en el mapeo
    if expected_language not in [code for codes in languages.values() for code in codes]:
        return False, "Unsupported language."

    # Verifica si el idioma detectado está en el mapeo
    if detected_language not in languages:
        return False, f"Detected language not supported: {detected_language}"

    # Compara si el idioma detectado es uno de los esperados
    if expected_language in languages[detected_language]:
        return True, "The text matches the expected language."
    else:
        return False, f"The text is in {languages[detected_language][0]}, but {expected_language} was expected."
