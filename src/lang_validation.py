from py3langid.langid import LanguageIdentifier, MODEL_FILE
from config.config import phonemize_config

# Inicializa el identificador de idioma
identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
identifier.set_languages(list(phonemize_config['lang_validation'].keys()))

def validate_language(text, expected_language):
    try:
        # Usa el identificador para clasificar el texto
        detected_language, _ = identifier.classify(text)
    except Exception as e:
        return False, f"Could not detect the language of the text. Error: {e}"
    
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
