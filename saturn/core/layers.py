
import numpy as np

class Layer:
    """
    Clase base para la topología de red en Saturn Network.
    Toda capa (Unidad de Agregación) debe heredar de esta estructura
    y definir sus métodos de propagación hacia adelante (forward)
    y retropropagación de errores (backward).
    
    (c) SaturnInvestments.com.mx- Licencia Dual (AGPLv3 / Comercial)
    """
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input_data):
        raise NotImplementedError

    def backward(self, output_gradient, learning_rate):
        raise NotImplementedError


class Dense(Layer):
    """
    Capa Completamente Conectada (Dense Layer)
    Funciona como la Unidad de Agregación de Factores de Riesgo.
    """
    def __init__(self, input_size, output_size):
        """
        Inicialización de la capa con dimensiones específicas.
        
        Args:
            input_size (int): Cantidad de variables macroeconómicas de entrada (ej. tasas, inflación).
            output_size (int): Cantidad de neuronas (nodos de agregación) en esta capa.
        """
        super().__init__()
        
        # Inicialización de Pesos (Elasticidades) usando el método de Xavier/Glorot
        # Ideal para estabilizar la varianza en datos financieros no estandarizados al 100%.
        limite = np.sqrt(2.0 / (input_size + output_size))
        self.weights = np.random.uniform(-limite, limite, (output_size, input_size))
        
        # Inicialización del Sesgo (Prima de Riesgo Inercial) en ceros
        self.bias = np.zeros((output_size, 1))

    def forward(self, input_data):
        """
        Dinámica de Proyección Vectorial (Forward Pass).
        Ejecuta la operación matemática: Z = W * X + B
        """
        self.input = input_data
        
        # Producto punto entre la matriz de pesos y el vector de entrada + sesgo
        self.output = np.dot(self.weights, self.input) + self.bias
        return self.output

    def backward(self, output_gradient, learning_rate):
        """
        Calibración Histórica Continua (Backpropagation).
        Calcula las derivadas parciales y actualiza los parámetros internos.
        """
        # 1. Calcular el gradiente respecto a los pesos (dW) y el sesgo (dB)
        weights_gradient = np.dot(output_gradient, self.input.T)
        bias_gradient = np.sum(output_gradient, axis=1, keepdims=True)
        
        # 2. Calcular el gradiente que pasará a la capa anterior (dX)
        input_gradient = np.dot(self.weights.T, output_gradient)
        
        # 3. Optimización: Actualización paramétrica de Elasticidades
        # W_new = W_old - (tasa_aprendizaje * dW)
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * bias_gradient
        
        return input_gradient
