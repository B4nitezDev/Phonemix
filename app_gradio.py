import gradio as gr
from src.phonemix import pronunciation_feedback
from src.lang_validation import validate_language
from src.suggestions.suggestions import suggestion_generate
from config.config import phonemize_config

def validate_text_in_real_time(expected_text, language):
    is_valid, validation_message = validate_language(expected_text, language)
    if not is_valid:
        return f"<div style='color: red; min-height: 20px; max-height: 21px;'>{validation_message}</div>"
    return "<div style='min-height: 20px; max-height: 21px; max-width:60px;'>&nbsp;</div>"

def get_feedback(language, text, audio):
    transcribed_text, user_phonemes, correct_phonemes, detailed_feedback, expected_audio = pronunciation_feedback(language, text, audio)
    suggestions = suggestion_generate(text, language)
    return transcribed_text, user_phonemes, correct_phonemes, detailed_feedback, expected_audio, suggestions

with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("# 🌍 Phonemix: Pronunciation Feedback Tool")
        
    text_input = gr.State("")
    text_validate_boolean = gr.State(False)

    with gr.Row(elem_id="input_row"):
        native_language_input = gr.Dropdown(
            label="Your native language", 
            choices=phonemize_config['lang_choices']
        )
        language_input = gr.Dropdown(
            label="What language do you want to speak?", 
            choices=phonemize_config['lang_choices']
        )

        with gr.Column():
            text_input = gr.Textbox(label="What do you want to say?", max_lines=2)
            validation_message_output = gr.HTML("<div style='min-height:20px; max-height:21px;'>&nbsp;</div>") 
        
        audio_input = gr.Audio(label="Speak out loud", type="filepath", elem_id="audio_input")

    text_input.change(
        validate_text_in_real_time, 
        inputs=[text_input, language_input], 
        outputs=validation_message_output,
        every=2  # Valida cada 2 segundos
    )
    
    feedback_button = gr.Button("Get Feedback")
    
    transcribed_text_output = gr.Textbox(label="You said this")
    user_phonemes_output = gr.Textbox(label="Your Phonemes")
    correct_phonemes_output = gr.Textbox(label="Correct Phonemes")
    
    with gr.Row():
        with gr.Accordion(label="Show detailed feedback"):
            detailed_feedback_output = gr.Markdown()
    expected_audio_output = gr.Audio(label="Correct Audio", type="filepath")
    
    with gr.Column():
        gr.Markdown("## Suggestions")
        suggestions_output = gr.Markdown(label="Suggestions")

    feedback_button.click(
        get_feedback,
        inputs=[language_input, text_input, audio_input],
        outputs=[
            transcribed_text_output,
            user_phonemes_output, 
            correct_phonemes_output, 
            detailed_feedback_output,
            expected_audio_output,
            suggestions_output
        ]
    )

demo.css = """
#audio_input {
    max-height: 400px; /* Ajusta el tamaño del componente de audio para mantener estabilidad */
}

#input_row {
    height: 290px; /* Ajusta este valor según tus necesidades */
    overflow-y: auto; /* Permite el desplazamiento si el contenido es demasiado largo */
}
"""

demo.launch(server_name="0.0.0.0", server_port=7860)
