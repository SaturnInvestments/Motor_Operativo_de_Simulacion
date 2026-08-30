"""
license_check.py
Motor de validación criptográfica, control de licenciamiento y sellado de modelos.
Diseñado para ser compilado y ofuscado mediante Cython (.so / .pyd).

(c) SaturnInvestments.com.mx
"""
import hashlib
import hmac
from saturn.utils.printout import print_security_warning

class LicenseViolationError(Exception):
    """Excepción corporativa para violaciones de propiedad intelectual o licencias."""
    pass

class ModelTamperingError(Exception):
    """Excepción para modelos binarios alterados, corruptos o no autorizados."""
    pass

# Sal criptográfica privada del núcleo (Nunca se expone en código cliente)
SECRET_SALT = b"Saturn_Master_Cryptographic_Core_2026_Strict"

def generate_client_license_key(client_name):
    """
    Genera la clave HMAC de validación corporativa para un cliente específico.
    """
    if not client_name:
        raise ValueError("El nombre del cliente no puede estar vacío.")
    
    return hmac.new(
        SECRET_SALT,
        client_name.strip().encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def compute_weights_hash(model_or_layers):
    """
    Calcula un hash SHA-256 acumulado de todos los tensores de pesos y sesgos.
    Garantiza que nadie pueda alterar las elasticidades del modelo sin romper la firma.
    """
    hasher = hashlib.sha256()
    layers = getattr(model_or_layers, 'layers', model_or_layers)
    
    for layer in layers:
        if hasattr(layer, 'weights') and layer.weights is not None:
            hasher.update(layer.weights.tobytes())
        if hasattr(layer, 'bias') and layer.bias is not None:
            hasher.update(layer.bias.tobytes())
            
    return hasher.hexdigest()

def generate_model_signature(client_name, license_type, model_version, weights_hash):
    """
    Genera la firma digital HMAC del binario .saturn.
    Combina: Cliente + Licencia + Versión + Hash de Pesos + Sal Secreta.
    """
    payload = f"{client_name.strip()}|{license_type.strip()}|{model_version.strip()}|{weights_hash}".encode('utf-8')
    return hmac.new(SECRET_SALT, payload, hashlib.sha256).hexdigest()

def verify_model_integrity_and_license(metadata, current_weights_hash, env_client, env_license, env_license_key):
    """
    Filtro de seguridad estricto (Fail-Closed).
    1. Valida que el entorno esté autenticado.
    2. Comprueba que el archivo .saturn coincida con el cliente y licencia del entorno descifrado.
    3. Verifica que la firma digital HMAC del .saturn coincida exactamente.
    4. Comprueba que los pesos no hayan sido manipulados.
    """
    client_in_model = str(metadata.get('cliente', '')).strip()
    license_in_model = str(metadata.get('licencia', '')).strip()
    version_in_model = str(metadata.get('version_modelo', '')).strip()
    signature_in_model = str(metadata.get('signature_hmac', '')).strip()
    
    # 1. Validación de Vía Libre Académica (AGPLv3)
    if "AGPLv3" in license_in_model or "Académica" in license_in_model:
        return True

    # 2. Validación Corporativa (Enterprise)
    if "Enterprise" in license_in_model:
        # A) Validar que el entorno proporcione credenciales válidas
        if not env_client or not env_license_key:
            print_security_warning()
            raise LicenseViolationError(
                "Acceso Denegado: Se requiere un entorno corporativo autenticado (.env.encrypted) con credenciales válidas."
            )
            
        # B) Validar que el archivo .saturn pertenezca al cliente del entorno
        if client_in_model != env_client.strip():
            print_security_warning()
            raise LicenseViolationError(
                f"Violación de Seguridad: El artefacto binario (.saturn) está registrado para '{client_in_model}', "
                f"pero el entorno actual pertenece a '{env_client}'. Uso no autorizado."
            )
            
        # C) Validar la clave de licencia corporativa
        expected_license_key = generate_client_license_key(env_client)
        if env_license_key.strip() != expected_license_key:
            print_security_warning()
            raise LicenseViolationError(
                f"Llave de licencia corporativa inválida para el cliente '{env_client}'."
            )
            
        # D) Validar la Firma Digital del binario (.saturn) contra manipulación de pesos
        expected_signature = generate_model_signature(
            client_in_model, license_in_model, version_in_model, current_weights_hash
        )
        
        if signature_in_model != expected_signature:
            print_security_warning()
            raise ModelTamperingError(
                "Integridad Comprometida: La firma criptográfica del archivo .saturn no coincide. "
                "El modelo ha sido alterado, corrompido o transferido sin autorización."
            )
            
        return True

    # 3. Licencia Desconocida o Corrupta
    print_security_warning()
    raise LicenseViolationError("Estructura de licenciamiento no reconocida o manipulada.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "generate":
        client_name = sys.argv[2]
        key = generate_client_license_key(client_name)
        print(f"\n=======================================================")
        print(f"[KEY] GENERADOR DE LICENCIAS SATURN ENTERPRISE (HMAC-SHA256)")
        print(f"=======================================================")
        print(f"Cliente:     {client_name}")
        print(f"LICENSE_KEY: {key}")
        print(f"=======================================================\n")
    else:
        print("\nUso: python -m saturn.security.license_check generate \"Nombre del Cliente\"\n")