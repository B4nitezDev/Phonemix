import gradio as gr
from src.phonemize.analyzer import get_phonemes
from src.phonemize.transcriber import transcribe_audio
from src.phonemix import provide_detailed_feedback
from src.t2s.t2s import text_to_speech
from src.lang_validation import validate_language
from io import BytesIO
from pydub import AudioSegment
import os

def pronunciation_feedback(file, expected_text, language):
    if not expected_text:
        return "Expected text is required."

    try:
        # Convert the uploaded file to an in-memory stream
        user_audio_stream = BytesIO(file.read())

        # Convert the audio to PCM WAV format using pydub
        audio_segment = AudioSegment.from_file(user_audio_stream)
        audio_file = f"/tmp/{file.name}.wav"
        audio_segment.export(audio_file, format="wav")

        # Transcribe the audio file and get phonemes
        transcribed_text = transcribe_audio(audio_file, language)
        user_phonemes = get_phonemes(transcribed_text, language)

        # Generate expected audio as a stream
        expected_audio_stream = text_to_speech(expected_text, language)
        expected_audio = AudioSegment.from_file(expected_audio_stream)
        expected_audio_file = "/tmp/expected_audio.wav"
        expected_audio.export(expected_audio_file, format="wav")

        correct_phonemes = get_phonemes(expected_text, language)

        # Generate feedback
        feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)

        # Clean up the temporary file
        os.remove(audio_file)

        return transcribed_text, user_phonemes, correct_phonemes, feedback, expected_audio_file

    except ValueError as e:
        return str(e)
    except Exception as e:
        print(f"Error: {e}")
        return "An unexpected error occurred."

def language_validation(expected_text, language):
    try:
        is_valid, validation_message = validate_language(expected_text, language)
        if not is_valid:
            return f"Validation Error: {validation_message}"
        return f"Validation Successful: The text matches the selected language ({language})."
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {str(e)}"

# Crear la interfaz de Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Pronunciation Feedback Tool")

    with gr.Tab("Feedback"):
        with gr.Row():
            audio_input = gr.Audio(label="Upload Audio File")
            text_input = gr.Textbox(label="Expected Text")
            lang_input = gr.Textbox(label="Language")
        transcribed_text_output = gr.Textbox(label="Transcribed Text")
        user_phonemes_output = gr.Textbox(label="User Phonemes")
        correct_phonemes_output = gr.Textbox(label="Expected Phonemes")
        feedback_output = gr.Textbox(label="Feedback")
        expected_audio_output = gr.Audio(label="Expected Audio")
        feedback_button = gr.Button("Get Feedback")

        feedback_button.click(
            pronunciation_feedback,
            inputs=[audio_input, text_input, lang_input],
            outputs=[
                transcribed_text_output, 
                user_phonemes_output, 
                correct_phonemes_output, 
                feedback_output, 
                expected_audio_output
            ]
        )

    with gr.Tab("Language Validation"):
        with gr.Row():
            validation_text_input = gr.Textbox(label="Expected Text")
            validation_lang_input = gr.Textbox(label="Language")
        validation_output = gr.Textbox(label="Validation Result")
        validation_button = gr.Button("Validate Language")

        validation_button.click(
            language_validation,
            inputs=[validation_text_input, validation_lang_input],
            outputs=validation_output
        )

demo.launch()
