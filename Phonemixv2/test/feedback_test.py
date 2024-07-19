import requests

url = "http://ec2-52-8-119-197.us-west-1.compute.amazonaws.com:8000/feedback/"
audio_file_path = "test/chesca_modded_1.wav"
expected_text = "bueno estaba escuchando un podcast"
language = "es"  # Cambia esto al idioma que estás usando, por ejemplo, "en" para inglés

# Abre el archivo de audio en modo binario
with open(audio_file_path, "rb") as audio_file:
    # Prepara los archivos y datos para enviar en la solicitud
    files = {"file": audio_file}
    data = {
        "expected_text": expected_text,
        "language": language
    }

    # Envía la solicitud POST a la API
    response = requests.post(url, files=files, data=data)

# Imprime la respuesta de la API
print(response.status_code)
print(response.json())
