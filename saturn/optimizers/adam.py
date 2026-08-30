"""
adam.py
Optimizador de Estimación de Momento Adaptativo (Adam).
Mecanismo de convergencia acelerada para series temporales financieras ruidosas.

(c) SaturnInvestments.com.mx
"""
import numpy as np

class Adam:
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        """
        Inicializa los hiperparámetros del optimizador.
        """
        self.learning_rate = learning_rate
        self.beta1 = beta1       # Decaimiento para el primer momento (media)
        self.beta2 = beta2       # Decaimiento para el segundo momento (varianza no centrada)
        self.epsilon = epsilon   # Constante de estabilidad numérica
        
        # Diccionarios para almacenar la memoria de los gradientes por capa
        self.m = {} 
        self.v = {}
        self.t = 0  # Contador de iteraciones (pasos de tiempo)

    def update(self, layer_id, weights, bias, dW, dB):
        """
        Ejecuta la actualización paramétrica de las elasticidades (pesos) 
        usando la memoria adaptativa de Adam.
        """
        # Inicializar el estado de la capa si es la primera vez que se ve
        if layer_id not in self.m:
            self.m[layer_id] = {'W': np.zeros_like(weights), 'B': np.zeros_like(bias)}
            self.v[layer_id] = {'W': np.zeros_like(weights), 'B': np.zeros_like(bias)}
            
        self.t += 1

        # 1. Actualización de los primeros momentos sesgados (Media de los gradientes)
        self.m[layer_id]['W'] = self.beta1 * self.m[layer_id]['W'] + (1 - self.beta1) * dW
        self.m[layer_id]['B'] = self.beta1 * self.m[layer_id]['B'] + (1 - self.beta1) * dB
        
        # 2. Actualización de los segundos momentos sesgados (Varianza de los gradientes)
        self.v[layer_id]['W'] = self.beta2 * self.v[layer_id]['W'] + (1 - self.beta2) * (dW ** 2)
        self.v[layer_id]['B'] = self.beta2 * self.v[layer_id]['B'] + (1 - self.beta2) * (dB ** 2)
        
        # 3. Corrección de sesgo (Bias correction)
        m_W_hat = self.m[layer_id]['W'] / (1 - self.beta1 ** self.t)
        m_B_hat = self.m[layer_id]['B'] / (1 - self.beta1 ** self.t)
        
        v_W_hat = self.v[layer_id]['W'] / (1 - self.beta2 ** self.t)
        v_B_hat = self.v[layer_id]['B'] / (1 - self.beta2 ** self.t)
        
        # 4. Actualización final de los pesos y sesgos
        weights -= self.learning_rate * m_W_hat / (np.sqrt(v_W_hat) + self.epsilon)
        bias -= self.learning_rate * m_B_hat / (np.sqrt(v_B_hat) + self.epsilon)
        
        return weights, bias