import torch
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2Processor

def initialize_model_and_processor(model_path):
    model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path)
    processor = Wav2Vec2Processor.from_pretrained(model_path)
    return model, processor

def setup_device(model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return device
