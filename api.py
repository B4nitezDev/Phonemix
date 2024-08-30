from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.phonemix import pronunciation_feedback
from src.lang_validation import validate_language
from src.suggestions.suggestions import suggestion_generate
from config.config import phonemize_config
import uvicorn

app = FastAPI()

# Configurar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes. Puedes restringir esto a dominios específicos.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.). Puedes restringirlo si es necesario.
    allow_headers=["*"],  # Permite todos los encabezados. Puedes restringirlo si es necesario.
)

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

    
@app.get("/supported_languages")
async def supported_languages():
    try:
        lang_choices = phonemize_config['lang_choices']
        return lang_choices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Inicia la API con uvicorn
# uvicorn main:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
