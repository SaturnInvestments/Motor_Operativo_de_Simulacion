"""
env_crypt.py
Servicio de cifrado y descifrado de variables de entorno para Saturn Network (estilo Laravel).
Permite proteger secretos de producción en archivos cifrados no legibles.

(c) SaturnInvestments.com.mx
"""
import os
import sys
import argparse
from cryptography.fernet import Fernet

def get_key():
    """
    Obtiene la clave de cifrado desde la variable de entorno o desde el archivo local .env.key.
    """
    # 1. Intentar desde variable de entorno
    key = os.environ.get("SATURN_ENV_KEY")
    if key:
        return key.strip().encode()

    # 2. Intentar desde archivo .env.key
    key_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env.key"))
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read().strip()
    
    return None

def encrypt_env(env_path, encrypted_path, key=None):
    """
    Cifra el archivo .env y lo guarda en .env.encrypted.
    """
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"No se encontró el archivo original {env_path}")

    if not key:
        key = Fernet.generate_key()
        # Guardar en .env.key
        key_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env.key"))
        with open(key_file, "wb") as f:
            f.write(key)
        print(f"[KEY] Nueva clave generada y guardada en: {key_file}")
        print(f"[INFO] Asegurate de guardar esta clave de forma segura en produccion (SATURN_ENV_KEY):")
        print(f"   {key.decode()}\n")

    fernet = Fernet(key)
    with open(env_path, "rb") as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    print(f"[OK] Archivo cifrado exitosamente en: {encrypted_path}")
    return key

def decrypt_env_to_memory(encrypted_path, key):
    """
    Descifra .env.encrypted en memoria y devuelve un diccionario de variables de entorno.
    """
    if not os.path.exists(encrypted_path):
        raise FileNotFoundError(f"No se encontró el archivo cifrado {encrypted_path}")

    fernet = Fernet(key)
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
    
    # Parsear las líneas del env descifrado
    env_vars = {}
    for line in decrypted_data.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            # Limpiar comillas si existen
            v = v.strip().strip("'").strip('"')
            env_vars[k.strip()] = v
            
    return env_vars

def decrypt_env_to_file(encrypted_path, env_path, key):
    """
    Descifra .env.encrypted y lo escribe de vuelta al archivo .env.
    """
    if not os.path.exists(encrypted_path):
        raise FileNotFoundError(f"No se encontró el archivo cifrado {encrypted_path}")

    fernet = Fernet(key)
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    with open(env_path, "wb") as f:
        f.write(decrypted_data)

    print(f"[OK] Archivo descifrado exitosamente y guardado en: {env_path}")

def main():
    parser = argparse.ArgumentParser(description="Gestor de cifrado de variables de entorno (.env) para Saturn Network")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando encrypt
    subparsers.add_parser("encrypt", help="Cifra el archivo .env actual")
    
    # Subcomando decrypt
    subparsers.add_parser("decrypt", help="Descifra .env.encrypted al archivo .env")

    args = parser.parse_args()

    # Rutas por defecto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env_path = os.path.join(base_dir, ".env")
    encrypted_path = os.path.join(base_dir, ".env.encrypted")

    if args.command == "encrypt":
        key = get_key()
        encrypt_env(env_path, encrypted_path, key)
    elif args.command == "decrypt":
        key = get_key()
        if not key:
            print("❌ Error: No se encontró la clave de cifrado. Define SATURN_ENV_KEY o crea el archivo .env.key.")
            sys.exit(1)
        decrypt_env_to_file(encrypted_path, env_path, key)

if __name__ == "__main__":
    main()
