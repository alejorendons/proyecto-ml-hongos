# Usa una imagen base de Python.
FROM python:3.11-slim

# Establece el directorio de trabajo.
WORKDIR /app

# Copia todos los archivos y carpetas del proyecto.
COPY . .

# Instala las dependencias desde la ruta correcta.
RUN pip install --no-cache-dir -r api/requirements.txt

# Expone el puerto 5000, que es el que usa tu script apirest.py.
EXPOSE 5000

CMD ["python", "api/apirest.py"]
