import express, { text } from 'express';
import multer from "multer";
import { Translate } from "../sdk-vercel/sdk-util.js";
import { FormData, File } from 'formdata-node';
import fetch from "node-fetch";
export const router = express.Router();
import path from 'node:path';
import fs from 'node:fs';
import { v2 as cloudinary } from 'cloudinary';
import 'dotenv/config'
import * as uuid from 'uuid';

import {fileURLToPath} from 'url';

const __filename = fileURLToPath(import.meta.url);

// 👇️ "/home/john/Desktop/javascript"
const __dirname = path.dirname(__filename);

// Configuración de Cloudinary
cloudinary.config({
    cloud_name: process.env.CLOUD_NAME,
    api_key: process.env.API_KEY_CLOUD,
    api_secret: process.env.API_SECRET_CLOUD
});

const uploadFunction = async (filePath) => {
    const options = {
        use_filename: true,
        unique_filename: false,
        overwrite: true,
        resource_type: 'auto',
        //format: 'mp3'
    };

    try {
        const result = await cloudinary.uploader.upload(filePath, { resource_type: "video" }, (error, result) => {
            if (error) {
                console.error('Error al subir el archivo:', error);
            } else {
                console.log('Archivo subido exitosamente:', result);
            }
        });
        console.log(result);
        return result.secure_url;
    } catch (error) {
        console.error(error);
    }
}


// Función para decodificar base64 de audio y guardar archivo
function decodeBase64Audio(base64String, outputFilePath) {
    const base64Data = base64String.replace(/^data:audio\/\w+;base64,/, '');
    const audioBuffer = Buffer.from(base64Data, 'base64');
    fs.writeFileSync(outputFilePath, audioBuffer);
    return audioBuffer;
}

// Configuración de Multer
const storage = multer.memoryStorage();
const upload = multer({ storage });

router.get('/', (req, res) => {
    res.status(200).send('Phonemix Listen');
});

router.post('/phonemix', upload.single('file'), async (req, res) => {
    if (!req.file || !req.body.expected_text || !req.body.language_output, !req.body.language_input) {
        return res.status(400).json({ message: 'Body incomplete' });
    }

    const file = req.file;
    const { expected_text, language_output, language_input } = req.body;

    const languages = [
        {key: "en-us", value: "ingles americano"},
        {key: "en-gb", value:"ingles britanico"},
        {key: "fr-fr", value: "frances"},
        {key: "it", value: "italiano"},
        {key: "de", value: "aleman"},
        {key: "pt-pt", value: "portugues de portugal"},
        {key: "pt-br", value: "portugues de brasil"},
        {key: "es", value: "español de españa"},
        {key: "es-la", value: "español de latinoamerica"}
    ]

    const isValidLanguageInput = languages.some(language => language.key === language_input);
    const isValidLanguageOutput = languages.some(language => language.key === language_output);

    if (!isValidLanguageInput || !isValidLanguageOutput) {
        return res.status(400).json({ message: 'Invalid language input or output' });
    }

    try {
        let textExpected = await Translate(expected_text, language_input, language_output);

        // Preparación de datos para la solicitud a AWS
        const formData = new FormData();
        const fileBlob = new File([file.buffer], `${file.originalname}.${new Date().getTime()}`, { type: file.mimetype });

        formData.append('file', fileBlob);
        formData.append('expected_text', textExpected);
        formData.append('language', language_output);

        // Realización de la solicitud a AWS
        const awsResponse = await fetch('http://ec2-52-8-119-197.us-west-1.compute.amazonaws.com:8000/feedback', {
            method: 'POST',
            body: formData
        });

        if (!awsResponse.ok) {
            throw new Error('Error fetching audio data from AWS');
        }

        const awsData = await awsResponse.json();
        const base64Audio = awsData.expected_audio;

        if (!base64Audio) {
            return res.status(400).json({ message: 'Invalid audio data from AWS' });
        }

        // Guardar archivo decodificado de AWS
        const outputDir = path.join(__dirname, 'temp');
        fs.mkdirSync(outputDir, { recursive: true });

        const awsFilePath = path.join(outputDir, `aws_audio_${uuid.v4()}.mp3`);
        const audioBuffer = decodeBase64Audio(base64Audio, awsFilePath);

        // Normaliza la ruta del archivo para Cloudinary
        const publicId = `aws_audio_${uuid.v4()}.mp3`;

        const awsUploadResult = await uploadFunction(awsFilePath)

        console.log(textExpected)
        const response = {
            //awsUploadedUrl: awsUploadResult.secure_url,
            textExpected,
            textUser: awsData.user_text,
            userPhonemes: awsData.user_phonemes,
            expectedPhonemes: awsData.expected_phonemes,
            feedback: awsData.feedback,
            audioExpected: awsUploadResult
        };

        // Enviar respuesta al cliente
        res.status(200).json(response);

        // Limpiar archivos temporales (opcional, dependiendo de tus necesidades)
        fs.unlinkSync(awsFilePath);

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});