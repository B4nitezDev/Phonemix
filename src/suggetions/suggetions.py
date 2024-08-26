import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

def suggetion_generate(textInput, language_output):
    response = model.generate_content("Give me 2 translations, one formal and one informal, of the following text: " +
                                    textInput +
                                    ". in this language" +
                                    language_output +                                     
                                    " and just return the translation"
                                  )
    
    return response.text
