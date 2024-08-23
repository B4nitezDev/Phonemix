import gradio as gr
from src.phonemize.analyzer import get_phonemes
from src.phonemize.transcriber import transcribe_audio
from src.phonemix import provide_detailed_feedback
from src.t2s.t2s import text_to_speech
from src.lang_validation import validate_language
from pydub import AudioSegment
import os

def pronunciation_feedback(native_language, language, expected_text, file_path):

    try:
        # Convertir el archivo subido a formato PCM WAV usando pydub
        audio_segment = AudioSegment.from_file(file_path)
        audio_file = f"/tmp/{os.path.basename(file_path)}.wav"
        audio_segment.export(audio_file, format="wav")

        # Transcribir el archivo de audio y obtener fonemas
        transcribed_text = transcribe_audio(audio_file, language)
        user_phonemes = get_phonemes(transcribed_text, language)

        # Generar el audio esperado como un archivo
        expected_audio_stream = text_to_speech(expected_text, language)
        expected_audio = AudioSegment.from_file(expected_audio_stream)
        expected_audio_file = "/tmp/expected_audio.wav"
        expected_audio.export(expected_audio_file, format="wav")

        correct_phonemes = get_phonemes(expected_text, language)

        # Generar retroalimentación
        feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)

        # Limpiar archivo temporal
        os.remove(audio_file)

        return (
            transcribed_text, 
            expected_text, 
            user_phonemes, 
            correct_phonemes, 
            file_path, 
            expected_audio_file
        )

    except ValueError as e:
        return str(e), None, None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return "An unexpected error occurred.", None, None, None, None, None

# Crear la interfaz de Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Pronunciation Feedback Tool")

    text_input = gr.State("")

    def validate_text_in_real_time(expected_text, language):
        is_valid, validation_message = validate_language(expected_text, language)
        return validation_message if not is_valid else ""

    with gr.Row():
        native_language_input = gr.Dropdown(
            label="Tu idioma Nativo", 
            choices=["es", "es-la", "pt-pt", "pt-br", "de", "it", "fr-fr", "en-gb", "en-us"]
        )
        language_input = gr.Dropdown(
            label="En qué idioma quieres hablar", 
            choices=["es", "es-la", "pt-pt", "pt-br", "de", "it", "fr-fr", "en-gb", "en-us"]
        )
        text_input = gr.Textbox(label="Qué quieres decir")
        audio_input = gr.Audio(label="Dilo en voz alta", type="filepath")
        validation_message_output = gr.Textbox(label="Validación del texto", interactive=False)


    text_input.change(
        validate_text_in_real_time, 
        inputs=[text_input, language_input], 
        outputs=validation_message_output,
        every=2  # Valida cada 2 segundos
    )

    transcribed_text_output = gr.Textbox(label="El texto del audio del usuario")
    expected_text_output = gr.Textbox(label="Texto correcto")
    user_phonemes_output = gr.Textbox(label="Phonemas del usuario")
    correct_phonemes_output = gr.Textbox(label="Phonemas correctos")
    expected_audio_output = gr.Audio(label="Audio esperado", type="filepath")

    feedback_button = gr.Button("Obtener Retroalimentación")

    feedback_button.click(
        pronunciation_feedback,
        inputs=[native_language_input, language_input, text_input, audio_input],
        outputs=[
            transcribed_text_output, 
            expected_text_output, 
            user_phonemes_output, 
            correct_phonemes_output, 
            audio_input, 
            expected_audio_output
        ]
    )

demo.launch(share=True)
