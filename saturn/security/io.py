"""
io.py
Módulo de entrada/salida y serialización de modelos con inyección de metadatos.
(c) SaturnInvestments.com.mx
"""
import h5py
import datetime
import os

# Importamos nuestro gestor centralizado de branding
from saturn.utils.printout import print_saturn_banner

def save_saturn_model(filepath, model, license_type=None, client=None):
    """
    Exporta la topología y los pesos del modelo a un formato seguro .saturn.
    Inyecta metadatos corporativos y de licenciamiento directamente en el binario.
    """
    # Forzar la extensión de la marca
    if not filepath.endswith('.saturn'):
        filepath += '.saturn'
        
    print(f"[*] Empaquetando red neuronal en: {filepath}")

    from saturn.config import LICENSE_TYPE, DEFAULT_CLIENT, SATURN_MODEL_BRAND, SATURN_MODEL_WARNING
    
    if license_type is None:
        license_type = LICENSE_TYPE
    if client is None:
        client = DEFAULT_CLIENT

    # Abrir el archivo HDF5 para escritura binaria
    with h5py.File(filepath, 'w') as f:
        # 1. INYECCIÓN DE METADATOS Y LICENCIA (Bloque de Seguridad)
        f.attrs['marca'] = SATURN_MODEL_BRAND
        f.attrs['fecha_compilacion'] = str(datetime.datetime.now())
        f.attrs['licencia'] = license_type
        f.attrs['cliente'] = client
        f.attrs['advertencia'] = SATURN_MODEL_WARNING
        
        # 2. GUARDADO DE TOPOLOGÍA Y PESOS (Elasticidades)
        for idx, layer in enumerate(model.layers):
            layer_group = f.create_group(f"layer_{idx}")
            layer_group.attrs['type'] = layer.__class__.__name__
            
            if hasattr(layer, 'weights') and hasattr(layer, 'bias'):
                layer_group.create_dataset('weights', data=layer.weights)
                layer_group.create_dataset('bias', data=layer.bias)
                
    print(f"    [OK] Red neuronal generada exitosamente")

def load_saturn_model(filepath, model_topology):
    """
    Carga un archivo .saturn al entorno de producción, valida la licencia
    y reconstruye los pesos sinápticos en la topología proporcionada.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el artefacto {filepath}")

    # Leemos en formato binario
    with h5py.File(filepath, 'r') as f:
        licencia = f.attrs.get('licencia', 'Desconocida')
        cliente = f.attrs.get('cliente', 'Desconocido')
        
        # 1. Filtro de Seguridad Visual y Validación
        from saturn.utils.printout import print_saturn_banner
        from saturn.config import HIDE_BRANDING, LICENSE_KEY
        from saturn.security.license_check import enforce_license_policy
        
        # Validar la política de licenciamiento
        enforce_license_policy(licencia, cliente, provided_key=LICENSE_KEY)
        
        if not HIDE_BRANDING:
            print_saturn_banner(licencia, cliente)
        
        # 2. Reconstrucción Matemática (Inyección de Tensores)
        for idx, layer in enumerate(model_topology.layers):
            layer_group_name = f"layer_{idx}"
            if layer_group_name in f:
                # Si la capa tiene pesos guardados (es un Dense), los cargamos
                if 'weights' in f[layer_group_name] and 'bias' in f[layer_group_name]:
                    layer.weights = f[layer_group_name]['weights'][:]
                    layer.bias = f[layer_group_name]['bias'][:]
                    
    print("    [OK] Pesos sinápticos y filtros de régimen cargados exitosamente.")
    return model_topology
