import express from "express";
import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import { body, validationResult } from 'express-validator';
import "dotenv/config";
import { router } from "./routes/routes.js";
import mongoose from "mongoose";
import bodyParser from "body-parser";
import {User} from "./models/User.js";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

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

mongoose.connect("mongodb://mongo:mBeLxAEDmyHKlFfaFNRKurVuamoAZbWp@roundhouse.proxy.rlwy.net:23470", {
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

app.post('/register', async (req, res) => {
    const { username, email, password } = req.body;
    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return res.status(400).json({ error: 'El usuario ya existe' });
    }

    try {
        const newUser = new User({ username, email, password });
        await newUser.save();
        res.status(201).send({ message: 'User registered successfully' });
    } catch (error) {
        res.status(400).send({ error: 'Error registering user' });
    }
});

app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ error: 'Credenciales inválidas' });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ error: 'Credenciales inválidas' });
        }

        const token = jwt.sign({ id: user._id }, process.env.SEED_JWT, { expiresIn: '1h' });

        res.json({ token });
    } catch (error) {
        res.status(500).json({ error: 'Error al iniciar sesión' });
    }
});

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
