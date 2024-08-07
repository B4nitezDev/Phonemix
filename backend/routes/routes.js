import express from "express";
import multer from "multer";
import { Translate, OptionalText } from "../sdk-vercel/sdk-util.js";
import qs from 'qs';
import fetch from "node-fetch";
import axios from 'axios';
export const router = express.Router();
import path from "node:path";
import fs from "node:fs";
import "dotenv/config";
import * as uuid from "uuid";
import { uploadFunction } from "../cloudinary/cloudinary.js";
import { languageValidate } from "../utils/LanguageValidate.js";
import { VoiceResponse } from "../models/VoiceResponse.js";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const storage = multer.memoryStorage();
const upload = multer({ storage });

router.get("/", (req, res) => {
  res.status(200).send("Phonemix Listen");
});

router.get("/langvalidation", async (req, res) => {
  const { language, expected_text } = req.query;
  let local_url =
    "http://ec2-52-8-119-197.us-west-1.compute.amazonaws.com:8000/langvalidation";

  return fetch(
    `${local_url}/?language=${language}&expected_text=${expected_text}`,
    {
      method: "GET",
    }
  )
    .then(async (result) => {
      const data = await result.json();
      res.status(200).json({ data });
    })
    .catch((error) => {
      console.error("error: " + error);
      res.status(500).send(error.message)
    });
});

router.post("/phonemix", upload.single("file"), async (req, res) => {
  if (
    !req.file || !req.body.expected_text || !req.body.language_output || !req.body.language_input
  ) {
    return res.status(400).json({ message: "Body incomplete" });
  }

  const file = req.file;
  const { expected_text, language_output, language_input } = req.body;

  if (!languageValidate(language_input, language_output)) {
    return res
      .status(400)
      .json({ message: "Invalid language input or output" });
  }

  if (!file.buffer || file.buffer.length === 0) {
    return res.status(400).json({ message: "File is empty" });
  }

  try {
    let textExpected = await Translate(
      expected_text,
      language_input,
      language_output
    );

    // Convertir buffer a archivo
    const outputDir = path.join(__dirname, "temp");
    fs.mkdirSync(outputDir, { recursive: true });

    const audioFilePath = path.join(outputDir, `audio_${uuid.v4()}.wav`);
    fs.writeFileSync(audioFilePath, file.buffer);

    // Aquí puedes subir el archivo a tu servicio en la nube o procesarlo como necesites
    const awsUploadResult = await uploadFunction(audioFilePath);

    // Construir los datos para enviar a la API
    const formData = new FormData();
    formData.append("file", fs.createReadStream(audioFilePath));
    formData.append("expected_text", textExpected);
    formData.append("language", language_output);

    const url_deploy = "http://ec2-52-8-119-197.us-west-1.compute.amazonaws.com:8000/feedback";
    const url_local = "http://localhost:8000/feedback";

    const options = {
      method: 'POST',
      headers: formData.getHeaders(),
      data: formData,
      url: url_deploy
    };

    const awsResponse = await axios(options);
    const awsData = awsResponse.data;
    const base64Audio = awsData.expected_audio;

    if (!base64Audio) {
      return res.status(400).json({ message: "Invalid audio data from AWS" });
    }

    const ResponseOptional = await OptionalText(
      expected_text,
      language_input,
      language_input
    );

    // Guardar el archivo de audio esperado de AWS
    const awsFilePath = path.join(outputDir, `aws_audio_${uuid.v4()}.mp3`);
    const audioBuffer = Buffer.from(base64Audio, 'base64');
    fs.writeFileSync(awsFilePath, audioBuffer);
    const awsUploadResult = await uploadFunction(awsFilePath);

    const response = {
      textExpected,
      textUser: awsData.user_text,
      userPhonemes: awsData.user_phonemes,
      expectedPhonemes: awsData.expected_phonemes,
      feedback: awsData.feedback,
      audioExpected: awsUploadResult,
      optionalText: ResponseOptional,
    };

    res.status(200).json(response);

    // Limpieza de archivos temporales
    fs.unlinkSync(audioFilePath);
    fs.unlinkSync(awsFilePath);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});
