"""
data_parser.py
Módulo de ingesta y preprocesamiento de series temporales financieras (CSV).
Transforma datos crudos en tensores matriciales para Saturn Network.

(c) SaturnInvestments.com.mx
"""
import numpy as np
import os

def load_financial_csv(filepath, target_col_index=-1, delimiter=',', skip_header=1):
    """
    Lee un archivo CSV financiero y separa las variables macroeconómicas (X)
    de la variable objetivo a proyectar (Y), como el tipo de cambio.

    Args:
        filepath (str): Ruta al archivo .csv (ej. data/input/tmec_historico.csv).
        target_col_index (int): Índice de la columna a predecir. Por defecto, la última (-1).
        delimiter (str): Separador del CSV.
        skip_header (int): Líneas a omitir (para saltar los nombres de columnas).

    Returns:
        tuple: (x_tensor, y_tensor) formateados tridimensionalmente para SaturnModel.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo de datos: {filepath}")

    print(f"[*] Importando datos desde: {filepath}")

    # Cargar el archivo CSV usando NumPy, ignorando valores no numéricos
    raw_data = np.genfromtxt(filepath, delimiter=delimiter, skip_header=skip_header)

    # Si hay valores faltantes (NaN), los rellenamos con la media de la columna
    # (Práctica común en series de tiempo para evitar que el gradiente explote)
    col_mean = np.nanmean(raw_data, axis=0)
    inds = np.where(np.isnan(raw_data))
    raw_data[inds] = np.take(col_mean, inds[1])

    # Separar variables independientes (X) y dependientes (Y)
    # Ejemplo: X = [Banxico, Fed, VIX, Remesas], Y = [USD/MXN]
    num_cols = raw_data.shape[1]
    
    # Creamos listas de índices para separar las columnas
    cols_x = [i for i in range(num_cols) if i != (target_col_index % num_cols)]
    
    x_data = raw_data[:, cols_x]
    y_data = raw_data[:, target_col_index]

    # Convertir a Tensores Tridimensionales (muestras, variables, 1)
    # Esto es crucial para que np.dot funcione correctamente en nuestras capas
    samples = x_data.shape[0]
    num_features = x_data.shape[1]
    
    x_tensor = x_data.reshape(samples, num_features, 1)
    y_tensor = y_data.reshape(samples, 1, 1)

    print(f"    [OK] Importación completa, Muestras procesadas: {samples}, Variables macro (X): {num_features}")
    return x_tensor, y_tensor