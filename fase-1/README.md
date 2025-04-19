# Proyecto ML: Clasificación de Hongos (Venenosos/No Venenosos)

## Fase 1: Limpieza y Exploración de Datos

### Descripción
En esta fase se realiza la limpieza de datos y exploración inicial para entender su estructura, identificar problemas de calidad y preparar los datos para el modelado, siguiendo estos pasos:

1. **Carga de los datos**  
   - Archivos `train.csv` y `test.csv` del concurso Kaggle  
   - 22 características morfológicas de hongos  

2. **Exploración de los datos**  
   - Detección de valores faltantes/inconsistencias  
   - Análisis de distribuciones y relaciones entre variables  
   - Visualización de correlaciones  

3. **Limpieza de los datos**  
   - Imputación de valores faltantes  
   - Transformación de variables categóricas (OneHotEncoder)  
   - Normalización de características  
   - Eliminación de outliers con Isolation Forest  

4. **Entrenamiento del modelo**  
   - Modelo XGBoost con optimización de hiperparámetros  
   - Clasificación binaria (venenoso/no venenoso)  
   - Mejor score MCC: 0.9847  

### Resultados Generados
- Modelo entrenado: `artifacts/model_package.joblib`  
- Predicciones: `fase-1/submission.csv`  

---

## Instrucciones de Ejecución

### Requisitos previos
1. **Git LFS** (para manejo de archivos grandes):
   ```bash
   # Windows: Descargar de https://git-lfs.com
   # MacOS: brew install git-lfs
   # Linux: sudo apt-get install git-lfs
2. Ejecutar el notebook Jupyter ps4e8-data-cleaning-and-eda-of-mushrooms.ipynb
3. Ejecutar todas las celdas del notebook en orden
