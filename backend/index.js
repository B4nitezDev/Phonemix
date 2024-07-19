import express from "express";
import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import { body, validationResult } from 'express-validator';
import "dotenv/config";
import { router } from "./routes/routes.js";

const app = express();

app.use(helmet());
app.use(express.json());
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
    origin: 'http://localhost:4321',
    optionsSuccessStatus: 200
};

app.use(cors(corsOptions));

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 25,
    message: 'Too many requests from this IP, please try again later.'
});
app.use(limiter);

/*
app.use('/api/', [
    body('expected_text').trim().escape().isLength({ min: 1 }).withMessage('Expected text is required'),
    body('language_input').trim().escape().isIn(['en-us', 'en-gb', 'fr-fr', 'it', 'de', 'pt-pt', 'pt-br', 'es', 'es-la']).withMessage('Invalid input language'),
    body('language_output').trim().escape().isIn(['en-us', 'en-gb', 'fr-fr', 'it', 'de', 'pt-pt', 'pt-br', 'es', 'es-la']).withMessage('Invalid output language'),
    (req, res, next) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        next();
    },
    router
]);*/
app.use('/api/', router)

app.listen(process.env.PORT, () => {
    console.log(`Listen in port:${process.env.PORT}`);
});
