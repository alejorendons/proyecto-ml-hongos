# 🍄 Clasificador de Hongos – Fase 2

Este repositorio contiene los scripts finales para entrenar y predecir la clasificación de hongos usando un pipeline de machine learning con `scikit-learn` y `XGBoost`.

## 🧾 Requisitos

- Tener instalado Docker en tu sistema
- Contar con los archivos de datos dentro de la carpeta local `data/` (ejemplo: `train.csv`, `test.csv`)
- Una terminal para ejecutar comandos (PowerShell, CMD, o similar)

## 🚀 Cómo empezar

Sigue estos pasos después de clonar el repositorio:

### 1. Clonar el repositorio

Esto producirá:
```bash
git clone https://github.com/alejorendons/proyecto-ml-hongos.git
cd fase-2
```

### 2. Construir la imagen de Docker
Esto crea un entorno aislado con todas las dependencias instaladas, dentro de la carpeta fase-2 abrel terminal y ejecuta el siguiente comando:
```bash
docker build -t mushroom-model .
```
### 3. Ejecutar el contenedor Docker con los volúmenes montados
Esto monta tus carpetas locales data/ y artifacts/ dentro del contenedor, luego ejecuta:
```bash
docker run -it --rm -v "${PWD}/data:/app/data" -v "${PWD}/artifacts:/app/artifacts" --name mushroom-container mushroom-model
```
### 4. Entrenar el modelo
Dentro del contenedor, ejecuta:
```bash
python train.py
```
### 5. Realizar predicciones
Después del entrenamiento, puedes predecir con un archivo de prueba (ejemplo: data/test.csv) con el siguiente comando:
```bash
python predict.py data/test.csv
```
📁 Archivos generados
Modelo entrenado: artifacts/model_package.joblib

Predicciones: predictions.csv (en el directorio raíz)

### 6. Salir del contenedor
Para finalizar escribe el siguiente comando:
```bash
Exit
```





