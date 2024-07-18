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
        prompt: `Traduce el siguiente texto a español y devuelve solo la traduccion: ${texto}`,
    });
    return text.replace("\n", "");
}

export async function toTextEs(texto) {
    const { text } = await generateText({
        model: google("models/gemini-1.5-flash-latest"),
        maxTokens: 1000,
        system: "Eres un traductor de español a ingles profesional",
        prompt: `Traduce el siguiente texto a en/us y devuelve solo la traduccion: ${texto}`,
    });
    return text.replace("\n", "");
}

const uploadToCloudinary = async (fileBuffer, publicId) => {
    return new Promise((resolve, reject) => {
        const timestamp = Math.floor(new Date().getTime() / 1000); // Obtener timestamp actual en segundos

        cloudinary.uploader.upload_stream({
            public_id: publicId,
            resource_type: 'auto',
            timestamp: timestamp
        }, (error, result) => {
            if (error) {
                console.error(error);
                reject(error);
            } else {
                resolve(result);
            }
        }).end(fileBuffer);
    });
};
