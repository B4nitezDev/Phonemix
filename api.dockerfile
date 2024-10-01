FROM python:3.12-slim

WORKDIR /api

COPY api_requirements.txt .

RUN pip install --no-cache-dir -r api_requirements.txt

RUN apt-get update && apt-get install -y ffmpeg espeak

# Limpiar el caché de apt para reducir el tamaño de la imagen
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"] 