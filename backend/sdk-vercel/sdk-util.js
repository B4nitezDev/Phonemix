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
