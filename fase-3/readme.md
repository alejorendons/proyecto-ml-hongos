# 🍄 Clasificador de Hongos – Fase 3: API REST

Este repositorio contiene la fase final del proyecto, donde el modelo de machine learning se despliega como una API REST interactiva utilizando Flask y Gunicorn, todo dentro de un contenedor Docker.

## 🧾 Requisitos

* Tener **Docker Desktop** instalado y en ejecución en tu sistema.
* Una terminal de comandos como PowerShell, CMD o Bash.
* Tener todos los archivos del proyecto (`Dockerfile`, `apirest.py`, `train.py`, etc.) en la misma carpeta.
* Una subcarpeta llamada `data` que contenga el archivo `train.csv`.

## 🚀 Cómo Empezar

Sigue estos pasos para construir, entrenar y ejecutar la API.

### 1. Construir la Imagen de Docker

Este comando empaqueta la aplicación de la API y todas sus dependencias en una imagen reutilizable llamada `mushroom-api`.

```bash
docker build -t mushroom-api .
```

### 2. Entrenar el Modelo

Antes de iniciar la API, es **crucial** generar el archivo del modelo. Este comando ejecuta el script de entrenamiento, que guardará `model_package.joblib` en una carpeta local llamada `artifacts`.

```bash
docker run --rm -v "${PWD}/data:/app/data" -v "${PWD}/artifacts:/app/artifacts" mushroom-api python train.py
```

### 3. Iniciar el Servidor de la API

Con el modelo ya creado, este comando inicia el servidor en segundo plano (`-d`). Los volúmenes (`-v`) son importantes para que el contenedor pueda leer el modelo que acabas de entrenar.

```bash
docker run -d --rm -p 5000:8000 --name mushroom-api -v "${PWD}/data:/app/data" -v "${PWD}/artifacts:/app/artifacts" mushroom-api
```
*La API estará disponible en `http://localhost:5000`.*

### 4. Probar los Endpoints

Puedes interactuar con la API de dos maneras:

#### A. Con el script `client.py` (Recomendado)

El cliente de Python prueba ambos endpoints de forma sencilla.

```bash
python client.py
```

#### B. Con `cURL` (Alternativa)

Puedes enviar una solicitud de predicción directamente desde la terminal.

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"cap-shape\": \"x\", \"cap-surface\": \"s\", \"cap-color\": \"n\", \"bruises\": \"t\", \"odor\": \"p\", \"gill-attachment\": \"f\", \"gill-spacing\": \"c\", \"gill-size\": \"n\", \"gill-color\": \"k\", \"stalk-shape\": \"e\", \"stalk-root\": \"e\", \"stalk-surface-above-ring\": \"s\", \"stalk-surface-below-ring\": \"s\", \"stalk-color-above-ring\": \"w\", \"stalk-color-below-ring\": \"w\", \"veil-type\": \"p\", \"veil-color\": \"w\", \"ring-number\": \"o\", \"ring-type\": \"p\", \"spore-print-color\": \"k\", \"population\": \"s\", \"habitat\": \"u\"}" http://localhost:5000/predict
```

### 5. Gestionar el Contenedor

* **Para ver los logs** del servidor en tiempo real y depurar:
    ```bash
    docker logs -f mushroom-api
    ```

* **Para detener el servidor** de la API:
    ```bash
    docker stop mushroom-api
    ```