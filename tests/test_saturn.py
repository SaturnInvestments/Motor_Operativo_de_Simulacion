"""
test_saturn.py
Script de Prueba de Integración para Saturn Network.
Simulación de Riesgo Cambiario T-MEC (USD/MXN).

(c) SaturnInvestments.com.mx
"""
import os
import sys
import numpy as np

# Asegurar importación del paquete saturn
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from saturn.core.model import SaturnModel
from saturn.core.layers import Dense
from saturn.core.activations import Tanh, ReLU
from saturn.optimizers.losses import mse, mse_prime
from saturn.security.io import save_saturn_model

def main():
    print("Iniciando entorno de pruebas de Saturn Network...")

    # 1. PREPARACIÓN DE DATOS (Fines Pedagógicos)
    # X_train: [Diferencial Banxico-Fed, Volatilidad T-MEC (EPU), Remesas Normalizadas]
    # Y_train: [Cotización Proyectada USD/MXN Normalizada]
    # Forma de los datos: (muestras, columnas, 1) para operaciones matriciales
    x_train = np.array([
        [[0.05], [0.2], [0.8]],  # Escenario 1: Estabilidad
        [[0.02], [0.9], [0.6]],  # Escenario 2: Fricción Arancelaria
        [[0.06], [0.1], [0.9]],  # Escenario 3: Nearshoring Óptimo
        [[-0.01], [0.8], [0.5]]  # Escenario 4: Fuga de Capitales
    ])
    
    y_train = np.array([
        [[18.50]], 
        [[20.10]], 
        [[17.90]], 
        [[21.00]]
    ])

    # 2. ARQUITECTURA DEL MODELO (Instanciación)
    modelo = SaturnModel()
    
    # Capa de Entrada y Primera Capa Oculta (3 variables de entrada -> 5 neuronas)
    modelo.add(Dense(3, 5))
    modelo.add(Tanh())  # Filtro de Régimen: Absorción de mercado
    
    # Capa Oculta Profunda (5 neuronas -> 4 neuronas)
    modelo.add(Dense(5, 4))
    modelo.add(ReLU())  # Filtro de Régimen: Pisos técnicos
    
    # Capa de Salida (4 neuronas -> 1 predicción: USD/MXN)
    modelo.add(Dense(4, 1))

    # 3. COMPILACIÓN Y CALIBRACIÓN
    modelo.compile(mse, mse_prime)
    
    print("\nIniciando Calibración Histórica Continua...")
    # Entrenamos por 1000 iteraciones (épocas) con una tasa de aprendizaje de 0.01
    modelo.fit(x_train, y_train, epochs=1000, learning_rate=0.01, print_interval=200)

    # 4. PRUEBA DE INFERENCIA (What-If)
    print("\nEjecutando Inferencia de Prueba (Predicción final sobre los datos):")
    predicciones = modelo.predict(x_train)
    for i, pred in enumerate(predicciones):
        print(f"Escenario {i+1} | Real: {y_train[i][0][0]:.2f} | Proyectado: {pred[0][0]:.2f}")

    # 5. EMPAQUETADO CORPORATIVO
    print("\nProcesando exportación de seguridad...")
    save_saturn_model(
        filepath="riesgo_tmec",
        model=modelo,
        license_type="Enterprise (Full Capabilities)",
        client="Tesorería Corporativa Alpha"
    )

if __name__ == "__main__":
    main()