import {generateText} from "ai";
import {createGoogleGenerativeAI} from "@ai-sdk/google";

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