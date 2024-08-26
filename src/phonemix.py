from src.phonemize.analyzer import levenshtein_detailed, print_phonemes_with_indices
from .phonemize.transcriber import transcribe_audio
from .t2s.t2s import text_to_speech
from .phonemize.analyzer import get_phonemes
from pydub import AudioSegment
import os

def provide_detailed_feedback(user_phonemes, correct_phonemes):
    """ Generate detailed feedback for phoneme corrections. """
    operations = levenshtein_detailed(user_phonemes, correct_phonemes)
    user_phonemes_indices = print_phonemes_with_indices(user_phonemes)
    correct_phonemes_indices = print_phonemes_with_indices(correct_phonemes)
    feedback_lines = [
        "Fonemas transcritos: " + user_phonemes_indices,
        "\nFonemas correctos: " + correct_phonemes_indices,
        "\nOperaciones necesarias:\n" + "\n".join(operations) if operations else "No se requieren cambios, la pronunciación es correcta."
    ]
    return "\n".join(feedback_lines)


def pronunciation_feedback(language, expected_text, file_path):
    try:
        # Transcribir el archivo de audio y obtener fonemas
        transcribed_text = transcribe_audio(file_path, language)
        user_phonemes = get_phonemes(transcribed_text, language)

        # Generar el audio esperado como un archivo
        expected_audio_stream = text_to_speech(expected_text, language)
        expected_audio = AudioSegment.from_file(expected_audio_stream)
        expected_audio_file = "/tmp/expected_audio.wav"
        expected_audio.export(expected_audio_file, format="wav")

        # Obtener los fonemas correctos
        correct_phonemes = get_phonemes(expected_text, language)

        # Generar retroalimentación
        feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)
        
        return (
            transcribed_text, 
            user_phonemes, 
            correct_phonemes, 
            feedback,
            expected_audio_file
        )

    except ValueError as e:
        return str(e), None, None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return "An unexpected error occurred.", None, None, None, None, None
