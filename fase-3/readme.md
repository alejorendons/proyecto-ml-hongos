# 🍄 Clasificador de Hongos – Fase 3: API REST
Este repositorio contiene la fase final del proyecto, donde el modelo de machine learning se despliega como una API REST interactiva utilizando Flask, todo dentro de un contenedor Docker autosuficiente.

## 🧾 Requisitos
Tener Docker Desktop instalado y en ejecución en tu sistema.

Una terminal de comandos como PowerShell, CMD o Bash.

Tener la estructura de carpetas final del proyecto, incluyendo:

La carpeta api con los scripts de Python.

La carpeta artifacts con el archivo model_package.joblib ya entrenado.

La carpeta data con train.csv y test.csv.

## 🚀 Cómo Empezar
Sigue estos pasos para construir la imagen y ejecutar la API. El Dockerfile está configurado para copiar todos los archivos necesarios, por lo que el proceso es muy directo.

###  1. Clonar el Repositorio (Paso Inicial)
Si estás empezando desde cero, clona el repositorio y navega a la carpeta de la fase 3.

Esto producirá:
```bash
git clone https://github.com/alejorendons/proyecto-ml-hongos.git
cd proyecto-ml-hongos/fase-3
```

### 2. Construir la Imagen de Docker

Este comando empaqueta toda la aplicación (código, modelo pre-entrenado y datos) en una imagen autosuficiente llamada mushroom-api.

```bash
docker build -t mushroom-api .
```

### 3. Iniciar el Servidor de la API

Ahora, ejecuta un contenedor a partir de la imagen que acabas de crear. No se necesitan volúmenes (-v) porque todos los archivos ya están dentro de la imagen

```bash
docker run -d --rm -p 5000:5000 --name mushroom-api mushroom-api
```

*La API estará disponible en `http://localhost:5000`.*

### 4. Probar los Endpoints

Puedes interactuar con la API de dos maneras:

#### A. Con el script `client.py` (Recomendado)

El cliente de Python prueba ambos endpoints de forma sencilla.

```bash
python client.py
```
Salida esperada:

```bash
Predicción: {'predictions': ['p', 'e', ...]}
Entrenamiento: {'message': 'Entrenamiento iniciado en segundo plano...'}
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
