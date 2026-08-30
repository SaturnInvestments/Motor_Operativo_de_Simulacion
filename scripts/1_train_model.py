import os
import sys
import numpy as np

# Asegurar rutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from saturn.config import PROJECT_TITLE, MODEL_EXPORT_NAME, DEFAULT_CLIENT, TRAIN_EPOCHS, TRAIN_EPOCHS_INTERVAL_PRINT

from saturn.core.model import SaturnModel
from saturn.core.layers import Dense
from saturn.core.activations import Tanh, ReLU
from saturn.optimizers.losses import mse, mse_prime
from saturn.security.io import save_saturn_model
from saturn.utils.visuals import plot_loss_curve, plot_predictions
from saturn.utils.data_parser import load_financial_csv

def main():
    print('\n')
    print("==================================================")
    print(f"[START] {PROJECT_TITLE}")
    print("==================================================\n")

    # 1. INGESTA DE DATOS REALES
    # Asume que guardaste el excel exactamente en esta ruta
    csv_path = "data/input/tmec_historico.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: No se encontró {csv_path}. Asegúrate de exportar tu Excel ahí.")
        return
    
    x_train_raw, y_train = load_financial_csv(csv_path, target_col_index=-1)

    # 2. Estandarización Z-Score
    print("[*] Estandarizando variables independientes (Z-score)")
    # x_train_raw tiene forma (muestras, variables, 1)
    x_mean = np.mean(x_train_raw, axis=0)
    x_std = np.std(x_train_raw, axis=0)
    
    # Restamos la media y dividimos por la desviación estándar (sumamos 1e-8 para evitar división por cero)
    x_train = (x_train_raw - x_mean) / (x_std + 1e-8)

    # 3. ARQUITECTURA DEL MOTOR OPERATIVO
    modelo = SaturnModel()
    
    # Capa de entrada (7 variables macroeconómicas) y primera capa oculta (16 neuronas)
    modelo.add(Dense(7, 16)) 
    modelo.add(Tanh())       
    
    # Capa oculta de abstracción de riesgo
    modelo.add(Dense(16, 8)) 
    modelo.add(ReLU())       
    
    # Capa de salida (1 predicción: USD/MXN)
    modelo.add(Dense(8, 1))  

    modelo.compile(mse, mse_prime)

    # 4. ENTRENAMIENTO
    print("[*] Iniciando entrenamiento de red neuronal con datos históricos")
    # Ajustamos a 150 épocas. Al ser 2291 registros diarios, cada época procesa mucha información.
    historial_error = modelo.fit(x_train, y_train, epochs=TRAIN_EPOCHS, learning_rate=0.005, print_interval=TRAIN_EPOCHS_INTERVAL_PRINT)

    # 5. GENERACIÓN DEL ECOSISTEMA VISUAL
    print("[*] Generando panel de control gráfico:")
    plot_loss_curve(historial_error)
    
    predicciones = modelo.predict(x_train)
    plot_predictions(y_train, predicciones)

    # 6. EXPORTACIÓN DEL MODELO SERIALIZADO
    print("[*] Exportando red neuronal (.saturn)")
    model_path = f"data/output/models/{MODEL_EXPORT_NAME}"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    save_saturn_model(
        filepath=model_path,
        model=modelo,
        license_type="Enterprise (Full Capabilities)",
        client=DEFAULT_CLIENT
    )
    
    print("\n[OK] ENTRENAMIENTO DE LA RED NEURONAL COMPLETADA CON ÉXITO.")

if __name__ == "__main__":
    main()