import requests

# Ejemplo de llamada a /predict
def predict_from_csv(file_path):
    url = "http://localhost:5000/predict"
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    return response.json()

# Ejemplo de llamada a /train
def train_with_csv(file_path):
    url = "http://localhost:5000/train"
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    return response.json()

# Uso
if __name__ == '__main__':
    print("Predicción:", predict_from_csv('data/test.csv'))
    print("Entrenamiento:", train_with_csv('data/train.csv'))