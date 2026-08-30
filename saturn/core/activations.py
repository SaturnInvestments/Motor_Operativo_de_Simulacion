import numpy as np
from saturn.core.layers import Layer

class Activation(Layer):
    """
    Clase base abstracta para los Filtros de Regímenes de Mercado.
    Hereda de Layer porque las activaciones también procesan datos
    hacia adelante y transmiten gradientes hacia atrás, pero sin 
    pesos sinápticos propios.
    
    (c) SaturnInvestments.com.mx - Licencia Dual
    """
    def __init__(self, activation_function, activation_derivative):
        super().__init__()
        self.activation = activation_function
        self.activation_derivative = activation_derivative

    def forward(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward(self, output_gradient, learning_rate):
        # El gradiente de entrada es el gradiente de salida multiplicado 
        # (element-wise) por la derivada de la función de activación.
        # La tasa de aprendizaje no se usa aquí porque no hay pesos que actualizar.
        return output_gradient * self.activation_derivative(self.input)


class Tanh(Activation):
    """
    Filtro de Tangente Hiperbólica (Rango -1 a 1).
    Financieramente, modela fluctuaciones acotadas, simulando escenarios 
    donde el banco central (Banxico) interviene para frenar depreciaciones 
    o apreciaciones excesivas, creando un régimen de mercado de reversión a la media.
    """
    def __init__(self):
        # Función Tanh: np.tanh(x)
        tanh = lambda x: np.tanh(x)
        # Derivada de Tanh: 1 - tanh(x)^2
        tanh_prime = lambda x: 1 - np.tanh(x) ** 2
        
        super().__init__(tanh, tanh_prime)


class ReLU(Activation):
    """
    Filtro de Rectificación Lineal (Rectified Linear Unit).
    Financieramente, modela "pisos técnicos" o umbrales de riesgo asimétrico.
    Si el choque macroeconómico (x) es negativo, el mercado no reacciona (0).
    Si supera el umbral de pánico (x > 0), el riesgo se transmite de manera íntegra.
    """
    def __init__(self):
        # Función ReLU: max(0, x)
        relu = lambda x: np.maximum(0, x)
        # Derivada de ReLU: 1 si x > 0, 0 en otro caso
        relu_prime = lambda x: np.where(x > 0, 1, 0)
        
        super().__init__(relu, relu_prime)
