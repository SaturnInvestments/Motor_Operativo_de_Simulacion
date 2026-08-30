"""
test_load.py
Script para validar la lectura de metadatos y licenciamiento 
de los archivos .saturn.

(c) SaturnInvestments.com.mx
"""
import os
import sys

# Forzar a Python a reconocer la carpeta padre si se ejecuta directamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from saturn.security.io import load_saturn_model

def main():
    print("Iniciando sistema de lectura de Saturn Network...\n")
    
    # Ruta del archivo que acabamos de generar en la prueba anterior
    # Ajustamos la ruta asumiendo que se guardó en la raíz (saturn-network)
    archivo_modelo = os.path.join(os.path.dirname(__file__), '..', 'riesgo_tmec.saturn')
    
    try:
        # Intentamos cargar el modelo y leer sus metadatos de seguridad
        load_saturn_model(archivo_modelo)
        
        print("✅ Verificación de seguridad concluida. El modelo está listo para recibir datos.")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo_modelo}")
    except Exception as e:
        print(f"❌ Error crítico al leer el archivo .saturn: {e}")

if __name__ == "__main__":
    main()