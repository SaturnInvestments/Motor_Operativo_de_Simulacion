"""
license_check.py
Motor de validación criptográfica y control de licenciamiento comercial.
Diseñado para ser compilado y ofuscado mediante Cython (.so / .pyd).

(c) SaturnInvestments.com.mx
"""
import hashlib
from saturn.utils.printout import print_security_warning

class LicenseViolationError(Exception):
    """Excepción corporativa para violaciones de propiedad intelectual."""
    pass

def _generate_expected_hash(client_name):
    """
    Genera el hash criptográfico esperado para un cliente.
    (En producción, esta función permanece ofuscada en código C).
    """
    # Sal criptográfica privada de Saturn Investments (Nunca se expone)
    secret_salt = "Saturn_Master_Key_2026_Strict"
    
    # Se genera una firma única combinando el nombre del cliente y la sal
    payload = f"{client_name}_{secret_salt}".encode('utf-8')
    return hashlib.sha256(payload).hexdigest()

def verify_enterprise_key(client_name, provided_key):
    """
    Verifica matemáticamente si la llave proporcionada es auténtica.
    """
    if not provided_key:
        return False
        
    expected_key = _generate_expected_hash(client_name)
    
    # Compara la llave insertada por la empresa con la llave matemática real
    return provided_key == expected_key

def enforce_license_policy(license_type, client_name, provided_key=None):
    """
    Filtro de seguridad principal. Se invoca obligatoriamente al cargar un .saturn.
    """
    # 1. VÍA LIBRE: Uso Académico / Open Source
    if "AGPLv3" in license_type or "Académica" in license_type:
        # Se permite la ejecución libre (el banner académico protegerá la marca)
        return True
        
    # 2. VÍA RESTRINGIDA: Uso Corporativo / Enterprise
    if "Enterprise" in license_type:
        is_valid = verify_enterprise_key(client_name, provided_key)
        
        if is_valid:
            return True
        else:
            # Despliega la advertencia corporativa y destruye el proceso
            from saturn.config import COMPANY_WEBSITE
            print_security_warning()
            raise LicenseViolationError(
                f"Llave criptográfica inválida o ausente para el cliente '{client_name}'. "
                f"Adquiera una licencia comercial en {COMPANY_WEBSITE}"
            )
            
    # 3. VÍA BLOQUEADA: Archivo corrupto o hackeado
    print_security_warning()
    raise LicenseViolationError("Estructura de licencia corrupta o alterada.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "generate":
        client_name = sys.argv[2]
        key = _generate_expected_hash(client_name)
        print(f"\n=======================================================")
        print(f"[KEY] GENERADOR DE LICENCIAS SATURN ENTERPRISE")
        print(f"=======================================================")
        print(f"Cliente: {client_name}")
        print(f"Llave:   {key}")
        print(f"=======================================================\n")
    else:
        print("\nUso: python -m saturn.security.license_check generate \"Nombre del Cliente\"\n")