import fs from "node:fs";

export function decodeBase64Audio(base64String, outputFilePath) {
    const base64Data = base64String.replace(/^data:audio\/\w+;base64,/, '');
    const audioBuffer = Buffer.from(base64Data, 'base64');
    fs.writeFileSync(outputFilePath, audioBuffer);
    return audioBuffer;
}