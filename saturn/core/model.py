import numpy as np
from saturn.utils.printout import print_epoch_progress

class SaturnModel:
    """
    Orquestador Principal de Saturn Network.
    Gestiona la arquitectura secuencial, el entrenamiento (Calibración Histórica)
    y la inferencia de simulaciones corporativas (What-If Scenarios).
    
    (c) SaturnInvestments.com.mx - Licencia Dual (AGPLv3 / Enterprise)
    """
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None
        self.history = []  # NUEVO: Almacenará la memoria del error

    def add(self, layer):
        """
        Agrega una Unidad de Agregación (Dense) o un Filtro de Régimen (Activation)
        a la topología de la red.
        """
        self.layers.append(layer)

    def compile(self, loss_function, loss_derivative):
        """
        Define la métrica de Minimización del Error de Pronóstico (Función de Pérdida).
        """
        self.loss = loss_function
        self.loss_prime = loss_derivative

    def predict(self, input_data):
        """
        Motor de Inferencia y Simulación (Forward Pass).
        Recibe una matriz combinatoria de escenarios macroeconómicos (tasas, T-MEC)
        y devuelve el cono de incertidumbre cambiaria proyectado.
        """
        # Dimensión de entrada dinámica para procesar lotes masivos (Batch Inference)
        samples = len(input_data)
        result = []

        # Ejecuta la simulación para cada escenario en la matriz
        for i in range(samples):
            # Propagación hacia adelante a través de todas las capas
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward(output)
            result.append(output)

        return result

    def fit(self, x_train, y_train, epochs, learning_rate, print_interval=100):
        """
        Proceso de Calibración Histórica Continua.
        """
        self.history = []  # Reiniciar el historial al iniciar el entrenamiento
        samples = len(x_train)

        for epoch in range(epochs):
            err = 0
            for j in range(samples):
                # 1. Forward Pass
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward(output)

                # 2. Computar el Error
                err += self.loss(y_train[j], output)

                # 3. Backward Pass
                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward(error, learning_rate)

            err /= samples
            self.history.append(err)  # NUEVO: Guardar el error de la época
            
            if (epoch + 1) % print_interval == 0:
                print_epoch_progress(epoch + 1, epochs, err)
                
        return self.history  # NUEVO: Devolver el historial al motor visual

    def save_to_saturn(self, filepath):
        """
        Empaqueta la topología, elasticidades y metadatos en un Motor Operativo de Simulación (.saturn).
        (La lógica criptográfica y de HDF5 se implementará en el módulo saturn/security/io.py)
        """
        # Aquí inyectaremos la llamada al módulo de seguridad e I/O
        print(f"Compilando Motor Operativo de Simulación en: {filepath}.saturn ...")
        pass
