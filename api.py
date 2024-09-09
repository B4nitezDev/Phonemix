from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.phonemix import pronunciation_feedback
from src.lang_validation import validate_language
from src.suggestions.suggestions import suggestion_generate
from config.config import phonemize_config
import uvicorn
from src.accent_feedback.set_model import load_model, choice_device
from src.accent_feedback.inference import make_prediction, preprocess_audio, move_to_device, load_audio, resample_audio, get_predicted_accent
from src.accent_feedback.feedback_items import generate_accent_feedback

app = FastAPI()

# Configurar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo y configurar el dispositivo
model, processor = load_model("model-wav2vec2-accent-classification")
device = choice_device(model)

class ValidationRequest(BaseModel):
    expected_text: str
    language: str

@app.get("/")
async def home():
    return {"message": "Welcome to Phonemix API"}

@app.post("/lang_validation")
async def lang_validation(request: ValidationRequest):
    is_valid, validation_message = validate_language(request.expected_text, request.language)
    if not is_valid:
        return {"validation_message": validation_message}
    return {"validation_message": ""}

@app.post("/get_feedback")
async def get_feedback(language: str = Form(...), text: str = Form(...), audio: UploadFile = File(...)):
    try:
        # Guarda temporalmente el archivo de audio
        audio_file_path = f"/tmp/{audio.filename}"
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(await audio.read())
        
        # Obtén el feedback detallado
        transcribed_text, user_phonemes, correct_phonemes, detailed_feedback, audio_base64 = pronunciation_feedback(
            language, text, audio_file_path
        )
        suggestions = suggestion_generate(text, language)
        
        return {
            "transcribed_text": transcribed_text,
            "user_phonemes": user_phonemes,
            "correct_phonemes": correct_phonemes,
            "detailed_feedback": detailed_feedback,
            "expected_audio": audio_base64,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_accent")
async def predict_accent(language: str = Form(...), text: str = Form(...), audio: UploadFile = File(...)):
    try:
        # Guarda temporalmente el archivo de audio
        audio_file_path = f"/tmp/{audio.filename}"
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(await audio.read())

        # Procesar el audio
        waveform, sample_rate = load_audio(audio_file_path)
        waveform = resample_audio(waveform, sample_rate, processor.feature_extractor.sampling_rate)
        max_length = int(processor.feature_extractor.sampling_rate * 10)
        inputs = preprocess_audio(waveform, processor.feature_extractor.sampling_rate, processor, max_length)
        
        # Realizar la predicción
        inputs = move_to_device(inputs, device)
        predicted_class_id = make_prediction(model, inputs, device)
        predicted_accent = get_predicted_accent(predicted_class_id, {0: 'us', 1: 'england'})
        
        # Comparar el acento predicho con el acento esperado
        if predicted_accent == language:
            return {"message": "La pronunciación está bien!"}
        else:
            # Generar feedback sobre el acento si no coincide
            feedback_items = generate_accent_feedback(text, predicted_accent, language)
            return {
                "predicted_accent": predicted_accent,
                "feedback_items": feedback_items
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/supported_languages")
async def supported_languages():
    try:
        lang_choices = list(phonemize_config['language_map_sr'].keys())
        return lang_choices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Inicia la API con uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
