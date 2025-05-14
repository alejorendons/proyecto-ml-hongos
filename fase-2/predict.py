import argparse
import pandas as pd
import joblib
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import KNNImputer
import os

import numpy as np

def to_float32(x):
    return x.astype(np.float32)


# Función para imputar los valores faltantes usando KNN
def knn_impute(df, n_neighbors=5):
    df_encoded = df.copy()
    for col in df_encoded.select_dtypes(include='object').columns:
        df_encoded[col] = df_encoded[col].astype('category').cat.codes
    knn_imputer = KNNImputer(n_neighbors=n_neighbors)
    df_imputed = pd.DataFrame(knn_imputer.fit_transform(df_encoded), columns=df_encoded.columns)
    for col in df.select_dtypes(include='object').columns:
        df_imputed[col] = df_imputed[col].round().astype(int).map(
            dict(enumerate(df[col].astype('category').cat.categories)))
    return df_imputed

# Preprocesamiento de datos, incluyendo la imputación y codificación ordinal
def preprocess_data(df, categorical_columns):
    df_imputed = knn_impute(df)
    ordinal_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    df_imputed[categorical_columns] = ordinal_encoder.fit_transform(df_imputed[categorical_columns].astype(str))
    return df_imputed

def main(csv_file):
    # Obtener la ruta del directorio actual
    current_directory = os.getcwd()
    
    # Cargar el modelo y el preprocesador guardados
    model_path = os.path.join(current_directory, 'artifacts', 'model_package.joblib')
    model_package = joblib.load(model_path)
    model = model_package['model']
    preprocessor = model_package['preprocessor']
    label_encoder = model_package['label_encoder']
    
    # Leer el archivo CSV de datos
    df = pd.read_csv(os.path.join(current_directory, csv_file))

    # Eliminar la columna 'id' si existe y almacenarla para el archivo de salida
    id_column = None
    if 'id' in df.columns:
        id_column = df['id']
        df = df.drop(columns=['id'])

    # Preprocesar datos usando el preprocesador guardado
    categorical_columns = df.select_dtypes(include=['object']).columns
    df_processed = preprocessor.transform(df)

    # Realizar predicciones
    y_pred = model.predict(df_processed)

    # Decodificar las etiquetas si es necesario
    y_pred_decoded = label_encoder.inverse_transform(y_pred)

    # Crear el archivo de salida con 'id' y 'prediction'
    if id_column is not None:
        output_df = pd.DataFrame({'id': id_column, 'prediction': y_pred_decoded})
    else:
        output_df = pd.DataFrame({'prediction': y_pred_decoded})

    # Guardar las predicciones en un archivo CSV
    output_file = os.path.join(current_directory, 'predictions.csv')
    output_df.to_csv(output_file, index=False)
    print(f'Predicciones guardadas en {output_file}')

# Definir la ejecución principal para argumentos de línea de comando
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predicción usando un modelo previamente almacenado.')
    parser.add_argument('csv_file', type=str, help='Nombre del archivo CSV de entrada.')
    args = parser.parse_args()
    main(args.csv_file)
