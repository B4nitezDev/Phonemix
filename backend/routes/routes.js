import express, {text} from 'express';
import multer from "multer";
import {toTextEn, toTextEs} from "../sdk-vercel/sdk-util.js";
import {FormData, File} from 'formdata-node';
import fetch from "node-fetch";
export const router = express.Router();
import fs from 'fs';
import Readable  from 'stream';

const storage = multer.memoryStorage();

const upload = multer({ dest: 'uploads/' });

router.get('/', (req, res) => {
    res.status(200).send('Phonemix Listen');
});

router.post("/phonemix", upload.single('file'), async (req, res) => {
    if (!req.file || !req.body.expected_text || !req.body.language) {
        return res.status(400).json({ message: "Body incomplete" });
    }

    const file = req.file;

    const { expected_text, language } = req.body;

    const formData = new FormData();
    const fileData = fs.readFileSync(file.path);
    const fileBlob = new File([fileData], file.originalname, { type: file.mimetype });

    formData.append('file', fileBlob);

    let textExpected;

    if (language === "es") {
        textExpected = await toTextEs(expected_text);
    } else {
        textExpected = await toTextEn(expected_text);
    }

    formData.append('expected_text', expected_text)
    formData.append('language', language);

    try {
        const response = await fetch('http://ec2-52-8-119-197.us-west-1.compute.amazonaws.com:8000/feedback', {
            method: 'POST',
            body: formData
        })

        console.log(await response.json());
        res.send(textExpected).status(200);
    } catch (e) {
        console.error(e.message);
        res.status(500).json({ error: "Internal Server Error" });
    }
});
