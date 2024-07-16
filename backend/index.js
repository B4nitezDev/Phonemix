import express from "express";
import cors from "cors";
import morgan from "morgan";
import "dotenv/config";
import multer from 'multer';
import {router} from "./routes/routes.js";

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));
app.use(cors());

app.use('/api/', router)

app.listen(process.env.PORT, () => {
    console.log(`Listen in port:${process.env.PORT}`);
});
