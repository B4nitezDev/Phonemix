import express from "express";
import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import {userRouter} from "./routes/user.js";
import * as dotenv from "dotenv";
import { router } from "./routes/routes.js";
import mongoose from "mongoose";
import bodyParser from "body-parser";

dotenv.config()

const app = express();

app.use(helmet());
app.use(express.json());
app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));

/*
    Produccion:
    const corsOptions = {
    origin: 'https://phonemix.vercel.app',
    optionsSuccessStatus: 200
};
*/

/* Develop*/
const corsOptions = {
    origin: '*',
    optionsSuccessStatus: 200
};

app.use(cors(corsOptions));

mongoose.connect(process.env.DB_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then(() => {
    console.log('Connected to MongoDB');
}).catch((error) => {
    console.error('Connection error:', error.message);
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
});

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 25,
    message: 'Too many requests from this IP, please try again later.'
});
app.use(limiter);

app.use('/api/', router)
app.use('/api/user', userRouter)

app.listen(process.env.PORT, () => {
    console.log(`Listen in port:${process.env.PORT}`);
});
