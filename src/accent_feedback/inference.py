import torch
import torchaudio

def load_audio(audio_path):
    waveform, sample_rate = torchaudio.load(audio_path)
    return waveform, sample_rate

def resample_audio(waveform, original_sample_rate, target_sample_rate):
    if original_sample_rate != target_sample_rate:
        resampler = torchaudio.transforms.Resample(original_sample_rate, target_sample_rate)
        waveform = resampler(waveform)
    return waveform

def preprocess_audio(waveform, sample_rate, processor, max_length):
    inputs = processor(
        waveform.squeeze().numpy(),
        sampling_rate=sample_rate,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=max_length
    )
    return inputs

def move_to_device(inputs, device):
    return {k: v.to(device) for k, v in inputs.items()}

def make_prediction(model, inputs, device):
    model.eval()
    model.to(device)  # Mueve el modelo al dispositivo
    inputs = move_to_device(inputs, device)  # Mueve los inputs al dispositivo
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=-1).item()
    return predicted_class_id

def get_predicted_accent(predicted_class_id, id2label):
    return id2label[predicted_class_id]