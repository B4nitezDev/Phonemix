import express from 'express';
import {User} from "../models/User.js";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

export const userRouter = express.Router();


userRouter.post('/register', async (req, res) => {
    const { username, email, password } = req.body;

    console.log(username, email, password)
    try {
        const newUser = new User({ username, email, password });
        console.log(newUser)
        await newUser.save();
        res.status(201).send({ message: 'User registered successfully' });
    } catch (error) {
        res.status(400).send({ error: 'Error registering user' });
    }
});

userRouter.post('/login', async (req, res) => {
    const { email, password } = req.body;

    console.log(email)
    // Validate email and password
    if (typeof email !== 'string' || typeof password !== 'string') {
        return res.status(400).json({ error: 'Email and password must be strings' });
    }

    try {
        const user = await User.findOne({ email: email }).exec();

        if (!user) {
            return res.status(400).json({ error: 'Invalid credentials' });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ error: 'Invalid credentials' });
        }

        const token = jwt.sign({ id: user._id }, process.env.SEED_JWT, { expiresIn: '1h' });

        res.json({ token });
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: 'Error logging in' });
    }
});