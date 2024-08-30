FROM python:3.12-slim

WORKDIR /app_gradio

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg espeak

# Limpiar el caché de apt para reducir el tamaño de la imagen
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 7860

CMD ["python", "app_gradio.py"] 