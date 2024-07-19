import subprocess
import os
import speech_recognition as sr
from config.config import phonemize_config


def convert_audio(input_file, output_file):
    """
    Convert audio file to desired format using ffmpeg.
    
    Parameters:
    - input_file (str): Path to the input audio file.
    - output_file (str): Path to the output audio file.
    """
    command = ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', output_file, '-y']
    subprocess.run(command, check=True)

def transcribe_audio(audio_file, language=phonemize_config['default_language_sr']):
    """
    Transcribe audio to text using Google's speech recognition service, 
    adjusting the language based on phoneme settings.
    
    Parameters:
    - audio_file (str): Path to the audio file.
    - language (str): Language setting for phoneme transcription.
    
    Returns:
    - str: Transcribed text or error message.
    """
    temp_file = '/tmp/temp_converted_audio.wav'
    try:
        # Convert the audio file
        convert_audio(audio_file, temp_file)

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_file) as source:
            audio_data = recognizer.record(source)
            language = phonemize_config['language_map_sr'].get(language, phonemize_config['default_language_sr'])
            try:
                return recognizer.recognize_google(audio_data, language=language)
            except sr.UnknownValueError:
                return phonemize_config['unknownvaluerror']
            except sr.RequestError:
                return phonemize_config['requesterror']
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
