from fastapi import HTTPException
from src.phonemize.analyzer import levenshtein_detailed, print_phonemes_with_indices
from .phonemize.transcriber import transcribe_audio
from .t2s.t2s import text_to_speech
from .phonemize.analyzer import get_phonemes
from pydub import AudioSegment
import io
import base64

def provide_detailed_feedback(user_phonemes, correct_phonemes):
    """ Generate detailed feedback for phoneme corrections. """
    operations = levenshtein_detailed(user_phonemes, correct_phonemes)
    user_phonemes_indices = print_phonemes_with_indices(user_phonemes)
    correct_phonemes_indices = print_phonemes_with_indices(correct_phonemes)
    feedback_lines = [
        "Fonemas transcritos: " + user_phonemes_indices,
        "\nFonemas correctos: " + correct_phonemes_indices,
        "\nOperaciones necesarias:\n" + "\n".join(operations) if operations else "\nNo se requieren cambios, la pronunciación es correcta."
    ]
    return "\n".join(feedback_lines)

def pronunciation_feedback(language, expected_text, file_path):
    try:
        # Transcribir el archivo de audio y obtener fonemas
        transcribed_text = transcribe_audio(file_path, language)
        user_phonemes = get_phonemes(transcribed_text, language)

        # Generar el audio esperado como un stream en memoria
        expected_audio_stream = text_to_speech(expected_text, language)
        expected_audio = AudioSegment.from_file(expected_audio_stream)
        
        # Crear un buffer en memoria para el audio
        expected_audio_buffer = io.BytesIO()
        expected_audio.export(expected_audio_buffer, format="wav")
        expected_audio_buffer.seek(0)  # Resetea el puntero del buffer al inicio

        # Leer el contenido del buffer para codificarlo en base64
        expected_audio_data = expected_audio_buffer.read()

        # Codificar el buffer en base64
        expected_audio_base64 = base64.b64encode(expected_audio_data).decode('utf-8')

        # Obtener los fonemas correctos
        correct_phonemes = get_phonemes(expected_text, language)

        # Generar retroalimentación
        feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)
        
        return (
            transcribed_text, 
            user_phonemes, 
            correct_phonemes, 
            feedback,
            expected_audio_base64
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
