from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_accent_feedback(phrase, predicted_accent, expected_accent):
    system = f'''Estás encargado de únicamente corregir o sugerir algún o algunos puntos en cuanto a pronunciacion de una frase en determinado acento del idioma ingles. 
                 Las respuestas deben ser extremadamente cortas y concisas. 
                 Con dar un máximo de 3 items como respuesta es más que suficiente. 
                 No debes responder de manera general, sino especifica haciendo referencia a la frase dada.
                 Un ejemplo de respuesta es: 1- "....." . 2- "....." . 3- ".....".
    '''
    prompt = f"Dame algún o algunos puntos para mejorar o incluso sugerencias de por qué el sistema detectó mi acento: '{predicted_accent}', y no llegué al acento esperado: '{expected_accent}', en la frase: '{phrase}'."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", "content": system
            },
            {
                "role": "user", "content": prompt 
            }
        ],
        temperature = 1
    )

    message = completion.choices[0].message.content
    return message