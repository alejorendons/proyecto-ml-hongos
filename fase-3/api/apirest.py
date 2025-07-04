from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
from werkzeug.utils import secure_filename
import threading
import numpy as np

# --- Función Auxiliar ---
# Requerida si tu modelo fue entrenado con ella en el pipeline.
def to_float32(x):
    return x.astype(np.float32)

# --- Inicialización de la App ---
app = Flask(__name__)

# --- Carga del Modelo ---
# Se carga una sola vez al iniciar el servidor para eficiencia.
try:
    model_package = joblib.load('/app/artifacts/model_package.joblib')
    model = model_package['model']
    preprocessor = model_package['preprocessor']
    label_encoder = model_package['label_encoder']
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    model, preprocessor, label_encoder = None, None, None

# --- Endpoints de la API ---

@app.route('/')
def home():
    """Página de bienvenida para verificar que la API está en línea."""
    return jsonify({
        "message": "¡El servidor de la API de Hongos está en línea!",
        "endpoints": {
            "/predict": "POST, espera un archivo (CSV o JSON) para predecir.",
            "/train": "POST, espera un archivo CSV para iniciar el re-entrenamiento."
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para predicciones: espera un archivo CSV o JSON con los datos."""
    if not model:
        return jsonify({"error": "El modelo no está cargado. Revisa los logs del servidor."}), 500
        
    if 'file' not in request.files:
        return jsonify({"error": "No se proporcionó archivo en la solicitud."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío."}), 400
    
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
        return jsonify({"error": "No se proporcionó archivo en la solicitud."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío."}), 400
    
    try:
        # Para que train.py funcione, debemos guardar el archivo como 'train.csv'
        filepath = os.path.join('/app/data', 'train.csv')
        file.save(filepath)
        
        # Lanzar entrenamiento en segundo plano (para no bloquear la API)
        def train_async():
            # Llama al script train.py que lee /app/data/train.csv
            os.system("python /app/train.py")
        
        threading.Thread(target=train_async).start()
        return jsonify({"message": "Entrenamiento iniciado en segundo plano. El nuevo modelo estará disponible pronto."})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Este bloque se usa solo para pruebas locales, no en Docker con Gunicorn.
    app.run(host='0.0.0.0', port=5000)