# Usa una imagen base de Python oficial
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt .
COPY train.py .
COPY predict.py .

# Instala las dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Crea carpetas para datos y artefactos (opcional, pero recomendado)
RUN mkdir -p /app/data /app/artifacts

# Comando por defecto (puede ser una terminal interactiva)
CMD ["bash"]