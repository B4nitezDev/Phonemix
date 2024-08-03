# Pronunciation Feedback API

This project aims to provide pronunciation feedback using phoneme analysis and detailed feedback. The project is hosted with the model deployed on AWS and the web application running on Railway.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Usage](#usage)
- [Endpoints](#endpoints)

## Overview

The Pronunciation Feedback API converts speech to text, analyzes phonemes, and provides detailed feedback on pronunciation. The project uses various tools and libraries to process and analyze audio, convert text to phonemes, and generate feedback.

## Features

- **Audio Transcription**: Converts audio files to text using Google's speech recognition service.
- **Phoneme Conversion**: Converts text to phonemes for detailed analysis.
- **Levenshtein Distance Calculation**: Provides detailed operations needed to correct pronunciation.
- **Language Validation**: Ensures the input text matches the expected language.
- **FastAPI**: Serves as the backend framework.
- **CORS Support**: Allows cross-origin requests from specified origins.

## Architecture

- **AWS**: Hosts the core model for phoneme analysis.
- **Railway**: Deploys the FastAPI web application.
- **Phonemizer**: Converts text to phonemes.
- **SpeechRecognition**: Transcribes audio files.
- **Pydub**: Processes and normalizes audio files.
- **LangDetect**: Detects the language of input text.

## Usage

1. **Run the API**:
    ```sh
    uvicorn app:app --reload
    ```

2. **Access the API**:
    Open your browser and navigate to `http://localhost:8000`.

## Endpoints

### `GET /`

Returns a welcome message.

### `POST /feedback/`

Provides pronunciation feedback for the uploaded audio file.

- **Parameters**:
    - `file`: Audio file (required)
    - `expected_text`: The expected text (required)
    - `language`: The language of the text (required)

- **Response**:
    - `user_text`: Transcribed text from the audio
    - `user_phonemes`: Phonemes of the transcribed text
    - `expected_phonemes`: Phonemes of the expected text
    - `feedback`: Detailed feedback on pronunciation
    - `expected_audio`: Base64-encoded audio of the expected pronunciation

### `GET /langvalidation/`

Validates if the input text matches the expected language.

- **Parameters**:
    - `expected_text`: The text to validate (required)
    - `language`: The expected language (required)

- **Response**:
    - `status`: Validation status
    - `message`: Validation message
