from gtts import gTTS
from io import BytesIO
from config.config import phonemize_config

def text_to_speech(text, language=phonemize_config['default_language']):
    """
    Convert text to speech using gTTS.
    
    Parameters:
    - text (str): The text to be converted to speech.
    - language (str): Language code for the speech synthesis.
    
    Returns:
    - BytesIO: Audio file in memory.
    """
    # Ajustar el código de idioma si es necesario
    language = phonemize_config['language_map_t2s'].get(language, phonemize_config['default_language'])

    # Dividir el código de idioma para obtener el TLD
    lang_split = language.split('-')
    lang = lang_split[0]
    tld = phonemize_config['tld_map_t2s'].get(lang_split[1], phonemize_config['default_tld']) if len(lang_split) > 1 else phonemize_config['default_tld']

    # Crear un objeto gTTS con el TLD correcto
    tts = gTTS(text=text, lang=lang, tld=tld)

    # Usar BytesIO para guardar el archivo de audio en memoria
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)  # Mover el cursor al principio del stream

    return mp3_fp
