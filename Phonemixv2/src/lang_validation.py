from langdetect import detect, LangDetectException
from config.config import phonemize_config

def validate_language(text, expected_language):
    try:
        detected_language = detect(text)
    except LangDetectException:
        return False, "Could not detect the language of the text."
    
    languages = phonemize_config['lang_validation']
    if not expected_language == None:
        expected_language = expected_language.lower()
    
    if expected_language not in languages.values():
        return False, "Unsupported language."

    if detected_language not in languages:
        return False, f"Detected language not supported: {detected_language}"

    if languages[detected_language] == expected_language:
        return True, "The text matches the expected language."
    else:
        return False, f"The text is in {languages[detected_language]}, but {expected_language} was expected."
