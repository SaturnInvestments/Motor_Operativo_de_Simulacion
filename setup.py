"""
setup.py
Script de instalación, construcción y empaquetado para Saturn Network.

(c) SaturnInvestments.com.mx
"""
import os
from setuptools import setup, find_packages

# Lee de manera segura el README para la descripción larga si existe
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_desc = f.read()
except FileNotFoundError:
    long_desc = "Motor Operativo de Simulación Financiera no lineal basado en tensores y modelos de agregación de riesgo cambiario."

# Obtener la versión de forma segura
version = "1.0.0"
init_path = os.path.join(here, 'saturn', '__init__.py')
if os.path.exists(init_path):
    with open(init_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                version = line.split('=')[1].strip().strip('"').strip("'")
                break

setup(
    name="saturn-network",
    version=version,
    author="Nicolás Daniel Gaucín Neria - Saturn Investments",
    author_email="contacto@saturninvestments.com.mx",
    description="Framework neuronal de análisis combinatorio y simulación de estrés cambiario.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://SaturnInvestments.com.mx",
    
    # Busca e incluye automáticamente la carpeta 'saturn' y sus submódulos
    packages=find_packages(include=['saturn', 'saturn.*']),
    
    # Dependencias estrictas que definimos en requirements.txt
    install_requires=[
        "numpy==1.26.4",
        "h5py==3.11.0",
        "Cython==3.0.10"
    ],
    
    # Metadatos para el ecosistema de Python
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License", # Refleja el modelo de Licencia Dual
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    
    # Versión mínima de Python recomendada para operaciones matriciales
    python_requires=">=3.8",
)