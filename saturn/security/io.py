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

def save_saturn_model(filepath, model, license_type=None, client=None, version=None, algorithm_version=None, architecture=None, scaler_mean=None, scaler_std=None):
    """
    Exporta la topología y los pesos del modelo a un formato seguro .saturn.
    Inyecta metadatos corporativos, versionado, licenciamiento, marcas de agua
    y una FIRMA DIGITAL HMAC-SHA256 para prevenir alteraciones y transferencias ilegales.
    """
    # Forzar la extensión de la marca
    if not filepath.endswith('.saturn'):
        filepath += '.saturn'
        
    print(f"[*] Empaquetando red neuronal en: {filepath}")

    from saturn.config import (
        SATURN_MODEL_BRAND, SATURN_MODEL_CLIENT, SATURN_MODEL_LICENSE,
        SATURN_MODEL_WARNING, SATURN_MODEL_VERSION,
        SATURN_ALGORITHM_VERSION, SATURN_MODEL_ARCHITECTURE,
        WATERMARK_TEXT, WATERMARK_FONT_SIZE, WATERMARK_COLOR,
        WATERMARK_ALPHA, WATERMARK_POSITION_X, WATERMARK_POSITION_Y
    )
    from saturn.security.license_check import compute_weights_hash, generate_model_signature
    
    if license_type is None:
        license_type = SATURN_MODEL_LICENSE
    if client is None:
        client = SATURN_MODEL_CLIENT
    if version is None:
        version = SATURN_MODEL_VERSION
    if algorithm_version is None:
        algorithm_version = SATURN_ALGORITHM_VERSION
    if architecture is None:
        architecture = SATURN_MODEL_ARCHITECTURE

    # 1. Calcular integridad de los tensores y generar la Firma Criptográfica
    weights_hash = compute_weights_hash(model)
    signature_hmac = generate_model_signature(client, license_type, version, weights_hash)

    # Determinar resumen de capas real
    layers_flow = " -> ".join([layer.__class__.__name__ for layer in model.layers])

    # Abrir el archivo HDF5 para escritura binaria
    with h5py.File(filepath, 'w') as f:
        # 2. INYECCIÓN DE METADATOS, VERSIONADO Y FIRMA (Bloque de Seguridad)
        f.attrs['marca'] = str(SATURN_MODEL_BRAND)
        f.attrs['fecha_compilacion'] = str(datetime.datetime.now().isoformat())
        f.attrs['version_modelo'] = str(version)
        f.attrs['version_algoritmo'] = str(algorithm_version)
        f.attrs['arquitectura'] = str(architecture)
        f.attrs['flujo_capas'] = str(layers_flow)
        f.attrs['licencia'] = str(license_type)
        f.attrs['cliente'] = str(client)
        f.attrs['advertencia'] = str(SATURN_MODEL_WARNING)
        
        # Firma Criptográfica y Hash de Integridad
        f.attrs['weights_hash'] = str(weights_hash)
        f.attrs['signature_hmac'] = str(signature_hmac)
        
        # Inyección de Marca de Agua grabada
        f.attrs['watermark_text'] = str(WATERMARK_TEXT)
        f.attrs['watermark_font_size'] = int(WATERMARK_FONT_SIZE)
        f.attrs['watermark_color'] = str(WATERMARK_COLOR)
        f.attrs['watermark_alpha'] = float(WATERMARK_ALPHA)
        f.attrs['watermark_pos_x'] = float(WATERMARK_POSITION_X)
        f.attrs['watermark_pos_y'] = float(WATERMARK_POSITION_Y)
        
        # Guardar parámetros de estandarización si se proporcionan
        if scaler_mean is not None:
            f.create_dataset('scaler_mean', data=scaler_mean)
        if scaler_std is not None:
            f.create_dataset('scaler_std', data=scaler_std)
        
        # 3. GUARDADO DE TOPOLOGÍA Y PESOS (Elasticidades)
        for idx, layer in enumerate(model.layers):
            layer_group = f.create_group(f"layer_{idx}")
            layer_group.attrs['type'] = layer.__class__.__name__
            
            if hasattr(layer, 'weights') and hasattr(layer, 'bias'):
                layer_group.create_dataset('weights', data=layer.weights)
                layer_group.create_dataset('bias', data=layer.bias)
                
    print(f"    [OK] Red neuronal generada exitosamente (v{version} / engine v{algorithm_version})")
    print(f"    [OK] Metadatos de cliente sellados: '{client}' ({license_type})")
    print(f"    [SEC] Firma Digital HMAC-SHA256: {signature_hmac[:16]}... [SELLADA]")

def load_saturn_model(filepath, model_topology):
    """
    Carga un archivo .saturn al entorno de producción, valida la firma digital
    de integridad, verifica la licencia cruzada con .env.encrypted y reconstruye
    los pesos sinápticos en la topología proporcionada.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el artefacto {filepath}")

    # Leemos en formato binario
    with h5py.File(filepath, 'r') as f:
        metadata = {}
        for k, v in f.attrs.items():
            metadata[k] = v

        licencia = metadata.get('licencia', 'Desconocida')
        cliente = metadata.get('cliente', 'Desconocido')
        version_modelo = metadata.get('version_modelo', '1.0.0')
        version_algoritmo = metadata.get('version_algoritmo', 'Desconocida')
        
        # 1. Reconstrucción Matemática previa para verificación de tensores
        for idx, layer in enumerate(model_topology.layers):
            layer_group_name = f"layer_{idx}"
            if layer_group_name in f:
                if 'weights' in f[layer_group_name] and 'bias' in f[layer_group_name]:
                    layer.weights = f[layer_group_name]['weights'][:]
                    layer.bias = f[layer_group_name]['bias'][:]

        # 2. Validación de Integridad y Licencia Cruzada con el Entorno
        from saturn.utils.printout import print_saturn_banner
        from saturn.config import HIDE_BRANDING, LICENSE_KEY, SATURN_MODEL_CLIENT, SATURN_MODEL_LICENSE
        from saturn.security.license_check import compute_weights_hash, verify_model_integrity_and_license
        
        current_weights_hash = compute_weights_hash(model_topology)
        verify_model_integrity_and_license(
            metadata=metadata,
            current_weights_hash=current_weights_hash,
            env_client=SATURN_MODEL_CLIENT,
            env_license=SATURN_MODEL_LICENSE,
            env_license_key=LICENSE_KEY
        )
        
        if not HIDE_BRANDING:
            print_saturn_banner(licencia, cliente)
            print(f"[*] Modelo versión: {version_modelo} | Motor: saturn-engine v{version_algoritmo}")
            print(f"    [AUTH] Firma Digital Verificada: Integridad y Propiedad Confirmadas.")
                    
        # 3. Adherir metadatos y parámetros de estandarización al modelo
        model_topology.metadata = metadata
        if 'scaler_mean' in f and 'scaler_std' in f:
            model_topology.scaler_mean = f['scaler_mean'][:]
            model_topology.scaler_std = f['scaler_std'][:]
                    
    print("    [OK] Pesos sinápticos y filtros de régimen cargados exitosamente.")
    return model_topology
