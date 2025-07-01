# train.py
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler,
    OrdinalEncoder,
    FunctionTransformer,
    LabelEncoder
)
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier

# ------------------------------
# 📁 1. Cargar y limpiar datos
# ------------------------------
data_path = Path("data/train.csv")
df = pd.read_csv(data_path)

# Eliminar columna 'id' si existe
if 'id' in df.columns:
    df.drop(columns=['id'], inplace=True)

# ------------------------------
# 🔄 2. Separar target
# ------------------------------
target_column = 'class'
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df[target_column])

# ------------------------------
# ✨ 3. Limpieza: columnas
# ------------------------------
categorical_columns = df.select_dtypes(include=['object']).columns.drop(target_column)
numerical_columns = df.select_dtypes(exclude=['object']).columns.drop(target_column, errors='ignore')

# Reemplazar categorías poco frecuentes en cada columna categórica
def replace_infrequent_categories(df, column, threshold=70):
    value_counts = df[column].value_counts()
    infrequent = value_counts[value_counts <= threshold].index
    df[column] = df[column].apply(lambda x: "Unknown" if x in infrequent else x)
    return df

for col in categorical_columns:
    df = replace_infrequent_categories(df, col)

# Imputar valores faltantes
# Numéricas → mediana
df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].median())

# Categóricas → 'Unknown'
df[categorical_columns] = df[categorical_columns].fillna('Unknown')

# Convertir categóricas a tipo category
df[categorical_columns] = df[categorical_columns].astype('category')

# Eliminar duplicados
df = df.drop_duplicates()
y = y[:len(df)]  # asegurar alineación

# ------------------------------
# ⚙️ 4. Crear pipelines
# ------------------------------
import numpy as np

def to_float32(x):
    return x.astype(np.float32)


numerical_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('to_float32', FunctionTransformer(to_float32))
])

categorical_pipeline = Pipeline([
    ('ordinal', OrdinalEncoder(
        dtype=np.int32,
        handle_unknown='use_encoded_value',
        unknown_value=-1
    ))
])

preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_columns),
    ('cat', categorical_pipeline, categorical_columns)
])

X_preprocessed = preprocessor.fit_transform(df)

# ------------------------------
# 🧹 5. Outlier Removal
# ------------------------------
isolation_forest = IsolationForest(contamination=0.024, random_state=58)
outlier_labels = isolation_forest.fit_predict(X_preprocessed)
non_outliers = outlier_labels != -1

X_clean = X_preprocessed[non_outliers]
y_clean = y[non_outliers]

# ------------------------------
# 🤖 6. Entrenar modelo
# ------------------------------
best_params = {
    'colsample_bytree': 0.43786552283911356,
    'learning_rate': 0.027640232910206706,
    'max_depth': 15,
    'min_child_weight': 8,
    'n_estimators': 456,
    'subsample': 0.9379640997273687
}

model = XGBClassifier(**best_params, use_label_encoder=False, random_state=58)
model.fit(X_clean, y_clean)

# ------------------------------
# 💾 7. Guardar modelo
# ------------------------------
artifacts_dir = Path("artifacts")
artifacts_dir.mkdir(exist_ok=True)

joblib.dump({
    'model': model,
    'preprocessor': preprocessor,
    'label_encoder': label_encoder
}, artifacts_dir / "model_package.joblib")

print("✅ Entrenamiento completado y modelo guardado en 'artifacts/model_package.joblib'")
