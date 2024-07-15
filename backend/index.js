import { createGoogleGenerativeAI } from "@ai-sdk/google";
import { generateText } from "ai";
import express from "express";
import cors from "cors";
import morgan from "morgan";
import "dotenv/config";

const google = createGoogleGenerativeAI({
  apiKey: process.env.API_KEY,
});

export async function toTextEn(texto) {
  const { text } = await generateText({
    model: google("models/gemini-1.5-flash-latest"),
    maxTokens: 614,
    system: "Eres un traductor de ingles a español profesional",
    prompt: `Traduce el siguiente texto a español: ${texto}`,
  });
  return text.replace("## ", "");
}

export async function toTextEs(texto) {
  const { text } = await generateText({
    model: google("models/gemini-1.5-flash-latest"),
    maxTokens: 614,
    system: "Eres un traductor de español a ingles profesional",
    prompt: `Traduce el siguiente texto a ingles: ${texto}`,
  });
  return text.replace("** ", "");
}

export async function textToSpeech(text) {
  const model = google('models/gemini-pro')

  const { text } = await generateText({
    model: model,
  })
}

export function clearResponse(data) {
    const regex = /(\d+): '([^']+)'/g;
    const phonemes = [];
    let match;
    let finish = ''
    
    while ((match = regex.exec(data)) !== null) {
        phonemes.push({ index: parseInt(match[1]), phoneme: match[2] });
    }
    
    phonemes.map(f=> {
        finish += f.phoneme;
    } )
    
    return finish;
}
/* 
 * Example: 
  * const phonemes = "Fonemas transcritos: 0: 'a' 1: 'ɪ' 2: ' ' 3: 'w' 4: 'ɑ' 5: 'ː' 6: 'n' 7: 't' 8: ' ' 9: 't' 10: 'ə' 11: 'b' 12: 'i' 13: ' ' 14: 'ð' 15: 'ə' 16: ' ' 17: 't' 18: 'ʃ' 19: 'æ' 20: 'm' 21: 'p' 22: 'i' 23: 'ə' 24: 'n' 25: ' ' 26: 'ʌ' 27: 'v' 28: 'ð' 29: 'ɪ' 30: ' ' 31: 'ɐ' 32: 'm' 33: 'ɛ' 34: 'ɹ' 35: 'ɪ' 36: 'k' 37: 'ə' 38: 'n' 39: ' ' 40: 'k' 41: 'ʌ' 42: 'p' 43: ' ' 44: 'ɐ' 45: 'ɡ' 46: 'ɛ' 47: 'n' 48: ' ' 49: 'ɪ' 50: 'n' 51: 'ð' 52: 'ə' 53: ' ' 54: 'l' 55: 'æ' 56: 's' 57: 't' 58: ' ' 59: 'd' 60: 'i' 61: ' ' 62: 'm' 63: 'ɚ' 64: 'ɹ' 65: 'i' 66: 'ː' 67: 'ə' 68: 'z' 69: ' ' 70: 'm' 71: 'æ' 72: 't' 73: 'ʃ' 74: ' '"
  * const phonemes_finish = clearResponse(phonemes)
  * console.log(phonemes_finish)
 *
*/

const app = express();

app.get('/', async(req, res) => {
  res.status(200).send('Phonemix Listen')
})

/*
 ? Body:
 *  file: @Type FileType
 *  text: @Type String
 *  language: @Type string
 */
app.post("/phonemix", async (req, res) => {
  const { file, text, lenguage } = req.body;

  if ((!file, !text, !lenguage)) {
    res.status(400).json({
      message: "Body incomplete",
    });
  }

  let textExpected;

  lenguage == "es"
    ? (textExpected = await toTextEs(text))
    : (textExpected = await toTextEn(text));

  const URL_PHONEMIX = 'http://localhost:8000/api/'

  const body = { file, textExpected, lenguage};

  const response = await fetch(URL_PHONEMIX, {
    method: 'POST',
    body: JSON.stringify(body)
  })

  const data = response.json();
  const userAudio = data.user_audio;
  const feedback = data.feedback;
  const clearPhonemesUser = clearResponse(data.user_phonemes)
  const clearPhonemesExpected = clearResponse(data.expected_phonemes)

  res.status(200).json({result: data})
});

app.listen(process.env.PORT, () => {
  console.log(`Listen in port:${process.env.PORT}`);
});
 