import os
import sys
import argparse
import numpy as np

# Asegurar rutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from saturn.config import (
    PROJECT_TITLE, SATURN_MODEL_CLIENT, SATURN_MODEL_LICENSE,
    load_yaml_config
)
from saturn.core.model import SaturnModel
from saturn.core.layers import Dense
from saturn.core.activations import Tanh, ReLU
from saturn.optimizers.losses import mse, mse_prime
from saturn.security.io import save_saturn_model
from saturn.utils.visuals import plot_loss_curve, plot_predictions
from saturn.utils.data_parser import load_financial_csv

def main():
    # 1. Cargar configuración desde config.yaml si existe
    yaml_cfg = load_yaml_config()
    train_cfg = yaml_cfg.get("training", {})
    data_cfg = yaml_cfg.get("data", {})

    cfg_epochs = train_cfg.get("epochs", 1000)
    cfg_interval = train_cfg.get("interval", 200)
    cfg_learning_rate = train_cfg.get("learning_rate", 0.005)
    cfg_model_name = train_cfg.get("model_name", "motor_tmec_v1")
    cfg_input_file = data_cfg.get("input_file", os.path.join("data", "input", "tmec_historico.csv"))

    parser = argparse.ArgumentParser(description="Calibración y Entrenamiento del Motor Neuronal")
    parser.add_argument("--epochs", type=int, default=cfg_epochs, help=f"Número de iteraciones de entrenamiento. Defecto: {cfg_epochs}")
    parser.add_argument("--interval", type=int, default=cfg_interval, help=f"Intervalo de impresión de pérdida en consola. Defecto: {cfg_interval}")
    parser.add_argument("--lr", type=float, default=cfg_learning_rate, help=f"Tasa de aprendizaje (learning rate). Defecto: {cfg_learning_rate}")
    parser.add_argument("--model-name", type=str, default=cfg_model_name, help=f"Nombre del archivo compilado de salida. Defecto: {cfg_model_name}")
    parser.add_argument("--input-file", type=str, default=cfg_input_file, help=f"Ruta al dataset histórico CSV. Defecto: {cfg_input_file}")
    parser.add_argument("--client", type=str, default=SATURN_MODEL_CLIENT, help=f"Entidad o cliente asignado al artefacto. Defecto: '{SATURN_MODEL_CLIENT}'")
    
    args = parser.parse_args()

    print('\n')
    print("==================================================")
    print(f"[START] {PROJECT_TITLE}")
    print("==================================================\n")

    # 2. INGESTA DE DATOS REALES
    csv_path = args.input_file
    
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: No se encontró {csv_path}. Asegúrate de exportar tu archivo ahí.")
        return
    
    x_train_raw, y_train = load_financial_csv(csv_path, target_col_index=-1)
    num_features = x_train_raw.shape[1]

    # 2. Estandarización Z-Score
    print(f"[*] Estandarizando {num_features} variables independientes (Z-score)")
    x_mean = np.mean(x_train_raw, axis=0)
    x_std = np.std(x_train_raw, axis=0)
    
    x_train = (x_train_raw - x_mean) / (x_std + 1e-8)

    # 3. ARQUITECTURA DEL MOTOR OPERATIVO
    modelo = SaturnModel()
    
    # Capa de entrada (dinámica según num_features) y primera capa oculta (16 neuronas)
    modelo.add(Dense(num_features, 16)) 
    modelo.add(Tanh())       
    
    # Capa oculta de abstracción de riesgo
    modelo.add(Dense(16, 8)) 
    modelo.add(ReLU())       
    
    # Capa de salida (1 predicción: USD/MXN)
    modelo.add(Dense(8, 1))  

    modelo.compile(mse, mse_prime)

    # 4. ENTRENAMIENTO
    print(f"[*] Iniciando entrenamiento de red neuronal con datos históricos ({args.epochs} épocas, lr={args.lr})")
    historial_error = modelo.fit(x_train, y_train, epochs=args.epochs, learning_rate=args.lr, print_interval=args.interval)

    # 5. GENERACIÓN DEL ECOSISTEMA VISUAL
    print("[*] Generando panel de control gráfico:")
    plot_loss_curve(historial_error)
    
    predicciones = modelo.predict(x_train)
    plot_predictions(y_train, predicciones)

    # 6. EXPORTACIÓN DEL MODELO SERIALIZADO
    print("[*] Exportando red neuronal (.saturn)")
    model_path = os.path.join("data", "output", "models", args.model_name)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    save_saturn_model(
        filepath=model_path,
        model=modelo,
        license_type=SATURN_MODEL_LICENSE,
        client=args.client,
        scaler_mean=x_mean,
        scaler_std=x_std
    )
    
    print("\n[OK] ENTRENAMIENTO DE LA RED NEURONAL COMPLETADA CON ÉXITO.")

if __name__ == "__main__":
    main()