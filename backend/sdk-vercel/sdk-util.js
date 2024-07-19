import {generateText} from "ai";
import {createGoogleGenerativeAI} from "@ai-sdk/google";

const google = createGoogleGenerativeAI({
    apiKey: process.env.API_KEY,
});

export async function Translate(textTranslate, language_input, language_output) {
    const { text } = await generateText({
        model: google("models/gemini-1.5-flash-latest"),
        maxTokens: 614,
        system: `You are a professional translator from ${language_input} to ${language_output}`,
        prompt: `Translate the following text to ${language_output} and return only the translation: ${textTranslate}`,
    });
    return text.replace("\n", "");
}

export async function OptionalText(textExpected,language_input, language_output) {
    const {text} = await generateText({
        model: google("models/gemini-1.5-flash-latest"),
        maxTokens: 614,
        system:  `You are a professional translator from ${language_input} to ${language_output}`,
        prompt: `Give me 2 translations, one formal and one informal, of the following text ${textExpected} in this language ${language_output} and just return the translation`,
    })
    console.log(text)
    return cleanText(text)
}

function cleanText(inputText) {
    // Regex patterns to match the formal and informal translations
    const formalPattern = /## Formal Translation:\s*> ([^#]*)/;
    const informalPattern = /## Informal Translation:\s*> ([^#]*)/;

    // Extract the formal translation
    const formalMatch = inputText.match(formalPattern);
    const formalTranslation = formalMatch ? formalMatch[1].trim() : '';

    // Extract the informal translation
    const informalMatch = inputText.match(informalPattern);
    const informalTranslation = informalMatch ? informalMatch[1].trim() : '';

    // Combine the translations into a single result
    return { formalTranslation, informalTranslation}
}
