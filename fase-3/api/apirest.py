from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
from werkzeug.utils import secure_filename
import threading

import numpy as np

def to_float32(x):
    return x.astype(np.float32)

app = Flask(__name__)

# Cargar modelo al iniciar
model_package = joblib.load('/app/artifacts/model_package.joblib')
model = model_package['model']
preprocessor = model_package['preprocessor']
label_encoder = model_package['label_encoder']

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para predicciones: espera un CSV o JSON con los datos."""
    if 'file' not in request.files:
        return jsonify({"error": "No se proporcionó archivo"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Archivo vacío"}), 400
    
    try:
        # Leer datos (CSV o JSON)
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_json(file)
        
        # Preprocesar y predecir
        df_processed = preprocessor.transform(df)
        y_pred = model.predict(df_processed)
        y_pred_decoded = label_encoder.inverse_transform(y_pred)
        
        return jsonify({"predictions": y_pred_decoded.tolist()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train', methods=['POST'])
def train():
    """Endpoint para reentrenar el modelo (usa un CSV con datos nuevos)."""
    if 'file' not in request.files:
        return jsonify({"error": "No se proporcionó archivo"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Archivo vacío"}), 400
    
    try:
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        filepath = os.path.join('/app/data', filename)
        file.save(filepath)
        
        # Lanzar entrenamiento en segundo plano (para no bloquear la API)
        def train_async():
            os.system(f"python /app/train.py")
        
        threading.Thread(target=train_async).start()
        return jsonify({"message": "Entrenamiento iniciado en segundo plano"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)