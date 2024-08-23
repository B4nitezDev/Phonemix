import gradio as gr
from src.phonemize.analyzer import get_phonemes
from src.phonemize.transcriber import transcribe_audio
from src.phonemix import provide_detailed_feedback
from src.t2s.t2s import text_to_speech
from src.lang_validation import validate_language
from pydub import AudioSegment
import os

def pronunciation_feedback(language, expected_text, file_path):
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
            feedback,
            expected_audio_file
        )

    except ValueError as e:
        return str(e), None, None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return "An unexpected error occurred.", None, None, None, None, None

# Crear la interfaz de Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Phonemix: Pronunciation Feedback Tool")

    text_input = gr.State("")
    text_validate_boolean = gr.State(False)

    def validate_text_in_real_time(expected_text, language):
        is_valid, validation_message = validate_language(expected_text, language)
        if not is_valid:
            return gr.Markdown(f"<span style='color: red;'>{validation_message}</span>")
        return gr.Markdown("")

    with gr.Row():
        native_language_input = gr.Dropdown(
            label="Your native language", 
            choices=["es", "es-la", "pt-pt", "pt-br", "de", "it", "fr-fr", "en-gb", "en-us"]
        )
        language_input = gr.Dropdown(
            label="What language do you want to speak?", 
            choices=["es", "es-la", "pt-pt", "pt-br", "de", "it", "fr-fr", "en-gb", "en-us"]
        )

        with gr.Column():
            text_input = gr.Textbox(label="What do you want to say?")
            validation_message_output = gr.Markdown("")
        
        audio_input = gr.Audio(label="Speak out loud", type="filepath")

    text_input.change(
        validate_text_in_real_time, 
        inputs=[text_input, language_input], 
        outputs=validation_message_output,
        every=2  # Valida cada 2 segundos
    )

    transcribed_text_output = gr.Textbox(label="You say this")
    user_phonemes_output = gr.Textbox(label="Your Phonemes")
    correct_phonemes_output = gr.Textbox(label="Correct Phonemes")
    expected_audio_output = gr.Audio(label="Correct Audio", type="filepath")

    feedback_button = gr.Button("Get Feedback")

    feedback_button.click(
        pronunciation_feedback,
        inputs=[language_input, text_input, audio_input],
        outputs=[
            transcribed_text_output,
            user_phonemes_output, 
            correct_phonemes_output, 
            expected_audio_output
        ]
    )

demo.launch(server_name="ec2-52-8-119-197.us-west-1.compute.amazonaws.com", server_port=8000)
