FROM python:3.11-slim

WORKDIR /app

# Copiar scripts y dependencias
COPY api/requirements.txt .
COPY api/train.py .
COPY api/predict.py .
COPY api/apirest.py .
COPY client.py .

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Crear directorios necesarios
RUN mkdir -p /app/data /app/artifacts

# Puerto expuesto para la API
EXPOSE 5000

# Comando para iniciar la API
CMD ["python", "apirest.py"]