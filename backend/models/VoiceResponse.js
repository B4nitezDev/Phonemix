import mongoose from 'mongoose'
const Schema = mongoose.Schema

const VoiceResponseSchema = new Schema({
    audioExpected: {type: String},
    expectedPhonemes: { type: String },
    feedback: { type: String },
    optionalText: {formalTranslation: { type: String }, informalTranslation: { type: String } },
    textExpected: { type: String },
    textUser: { type: String },
    userPhonemes: { type: String },
})

export const VoiceResponse = mongoose.model('VoiceResponse', VoiceResponseSchema)