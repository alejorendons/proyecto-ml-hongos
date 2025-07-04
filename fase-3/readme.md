# 🍄 Clasificador de Hongos – Fase 3: API REST

Este repositorio contiene la fase final del proyecto, donde el modelo de machine learning se despliega como una API REST interactiva utilizando Flask y Gunicorn, todo dentro de un contenedor Docker.

## 🧾 Requisitos

* Tener **Docker Desktop** instalado y en ejecución en tu sistema.
* Una terminal de comandos como PowerShell, CMD o Bash.
* Tener todos los archivos del proyecto (`Dockerfile`, `apirest.py`, `train.py`, etc.) en la misma carpeta.
* Una subcarpeta llamada `data` que contenga el archivo `train.csv`.

## 🚀 Cómo Empezar

Sigue estos pasos para construir, entrenar y ejecutar la API.
###  Clonar el repositorio

Esto producirá:
```bash
git clone https://github.com/alejorendons/proyecto-ml-hongos.git
cd fase-3
```

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

### 3. Reiniciar y Ejecutar el Servidor de la API

Este flujo de trabajo detiene cualquier versión anterior del contenedor y lo inicia de nuevo para asegurar que se carguen todos los cambios.
```bash
# Detener y eliminar el contenedor anterior para evitar conflictos
docker stop mushroom-api 2>$null
docker rm mushroom-api 2>$null

# Iniciar el nuevo contenedor con el servidor de la API en segundo plano
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
curl.exe -X POST -F "file=@data/test.csv" http://localhost:5000/predict
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
