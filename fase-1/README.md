# Fase 1: Limpieza y Exploración de Datos

En esta fase, se realiza la limpieza de los datos y la exploración inicial para entender su estructura, identificar posibles problemas de calidad y preparar los datos para el modelado.

## Descripción

En esta fase se utilizaron los siguientes pasos:

1. **Carga de los datos**
   
   Se cargaron los archivos `train.csv` y `test.csv` proporcionados, los cuales contienen características de diferentes tipos de hongos. Estos datos fueron extraídos del concurso de Kaggle.

2. **Exploración de los datos**

   Se exploraron los datos para detectar cualquier valor faltante, inconsistencias o valores atípicos que pudieran afectar el rendimiento del modelo. También se realizaron análisis descriptivos para entender las distribuciones y las relaciones entre las variables.

3. **Limpieza de los datos**

   Se eliminaron o imputaron los valores faltantes, se transformaron las variables categóricas en variables numéricas utilizando codificación (OneHotEncoder), y se normalizaron las características para mejorar la eficiencia del modelo.

4. **Entrenamiento del modelo**

   Usamos un modelo de clasificación basado en un enfoque de clasificación binaria para predecir si un hongo es venenoso o no.

## Instrucciones para ejecutar la fase 1

1. **Clonar el repositorio**

   Clona el repositorio del proyecto:

   ```bash
   git clone https://github.com/tu_usuario/proyecto-ml-hongos.git
