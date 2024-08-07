import express, { response, text } from "express";
import multer from "multer";
import { Translate, OptionalText } from "../sdk-vercel/sdk-util.js";
import qs from 'qs'
import { FormData, File } from "formdata-node";
import fetch from "node-fetch";
import axios from 'axios'
export const router = express.Router();
import path from "node:path";
import fs from "node:fs";
import "dotenv/config";
import * as uuid from "uuid";
import { uploadFunction } from "../cloudinary/cloudinary.js";
import { decodeBase64Audio } from "../utils/decode64.js";
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
  console.log(language, expected_text);
  let local_url =
    "http://ec2-52-8-119-197.us-west-1.compute.amazonaws.com:8000/langvalidation";

  return fetch(
    `${local_url}/?language=${language}&expected_text=${expected_text}`,
    {
      method: "GET",
    }
  )
    .then(async (result) => {
      //console.info('result: ', await result.json)
      const data = await result.json();
      res.status(200).json({ data });
    })
    .catch((error) => {
      console.error("error: " + error);
      res.status(500).send(error.message)
    });

  //console.info(await response.json());

  //return response.json();
});

router.post("/phonemix", upload.single("file"), async (req, res) => {
  if (
    (!req.file || !req.body.expected_text || !req.body.language_output,
    !req.body.language_input)
  ) {
    return res.status(400).json({ message: "Body incomplete" });
  }

  const file = req.file;
  const { expected_text, language_output, language_input } = req.body;

  console.info(file);

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

    //const formData = new FormData();
 //   const fileBuffer = new ArrayBuffer();
   // console.log(file.buffer)
   // fileBuffer.push(file.buffer)


function toArrayBuffer(buffer) {
  const arrayBuffer = new ArrayBuffer(buffer.length);
  const view = new Uint8Array(arrayBuffer);
  for (let i = 0; i < buffer.length; ++i) {
    view[i] = buffer[i];
  }
  return arrayBuffer;
}

    const fileBuffer = toArrayBuffer(file.buffer)

    const fileBlob = new File(
      fileBuffer,
      `${file.originalname}.${new Date().getTime()}`
    );


    //console.info(fileBlob, textExpected, language_output)


    //formData.append("file", fileBlob);
    //formData.append("expected_text", textExpected);
    //formData.append("language", language_output);

    const url_deploy =
      "http://ec2-52-8-119-197.us-west-1.compute.amazonaws.com:8000/feedback";
    const url_local = "http://localhost:8000/feedback";

console.info(fileBlob)

//console.info(formData);

  const data = {
    file: fileBlob,
    expected_text: textExpected,
    language: language_output
  }

   const options = {
     method: 'POST',
     headers: { 'content-type': 'application/x-www-form-urlencoded' },
     data: qs.stringify(data),
     url: url_deploy
   }

   console.log(options)

    const awsResponse = await axios(options);

  //  console.log(awsResponse);

    if (!awsResponse.ok) {
      throw new Error("Error fetching audio data from AWS");
    }

    const awsData = await awsResponse.json();
    const base64Audio = awsData.expected_audio;

    if (!base64Audio) {
      return res.status(400).json({ message: "Invalid audio data from AWS" });
    }

    const ResponseOptional = await OptionalText(
      expected_text,
      language_input,
      language_input
    );

    const outputDir = path.join(__dirname, "temp");
    fs.mkdirSync(outputDir, { recursive: true });

    const awsFilePath = path.join(outputDir, `aws_audio_${uuid.v4()}.mp3`);
    const awsUploadResult = await uploadFunction(awsFilePath);

    console.log(ResponseOptional);

    if (!req.header.Authorization) {
      const response = {
        //awsUploadedUrl: awsUploadResult.secure_url,
        textExpected,
        textUser: awsData.user_text,
        userPhonemes: awsData.user_phonemes,
        expectedPhonemes: awsData.expected_phonemes,
        feedback: awsData.feedback,
        audioExpected: awsUploadResult,
        optionalText: ResponseOptional,
      };

      res.status(200).json(response);
    }

    const newVoiceResponse = await new VoiceResponse(response);
    fs.unlinkSync(awsFilePath);
    await newVoiceResponse.save();
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});
