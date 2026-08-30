import numpy as np

def mse(y_true, y_pred):
    """
    Error Cuadrático Medio (Mean Squared Error).
    Mide el costo financiero de la desviación del pronóstico cambiario.
    (c) SaturnInvestments.com.mx
    """
    return np.mean(np.power(y_true - y_pred, 2))

def mse_prime(y_true, y_pred):
    """
    Derivada del MSE.
    Inicia la cadena de retropropagación para ajustar las elasticidades.
    """
    return 2 * (y_pred - y_true) / y_true.size