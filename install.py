"""
install.py
Asistente de Inicialización y Verificación de Entorno para Saturn Network.
Diseñado para que el cliente final configure su entorno con un solo clic.

(c) SaturnInvestments.com.mx
"""
import os
import sys
import subprocess
import platform

# Asegurar compatibilidad UTF-8 en consola
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REQUIRED_PYTHON_MAJOR = 3
REQUIRED_PYTHON_MINOR_MIN = 9
REQUIRED_PYTHON_MINOR_MAX = 13
RECOMMENDED_PYTHON = "3.11"

def print_banner():
    print("\n=======================================================")
    print("      SATURN NETWORK - ASISTENTE DE INSTALACIÓN        ")
    print("            (c) SaturnInvestments.com.mx               ")
    print("=======================================================\n")

def check_python_version():
    """Verifica que la versión de Python sea compatible (3.9 - 3.13)."""
    major, minor, micro = sys.version_info[:3]
    current_ver = f"{major}.{minor}.{micro}"
    print(f"[*] Comprobando versión de Python: {current_ver} ({platform.system()} {platform.machine()})")
    
    if major != REQUIRED_PYTHON_MAJOR or minor < REQUIRED_PYTHON_MINOR_MIN or minor > REQUIRED_PYTHON_MINOR_MAX:
        print(f"\n❌ ERROR: Versión de Python no compatible: {current_ver}")
        print(f"   Saturn Network requiere Python entre {REQUIRED_PYTHON_MAJOR}.{REQUIRED_PYTHON_MINOR_MIN} y {REQUIRED_PYTHON_MAJOR}.{REQUIRED_PYTHON_MINOR_MAX} (Recomendado: {RECOMMENDED_PYTHON}).")
        print("   Por favor descargue la versión adecuada desde: https://www.python.org/downloads/\n")
        return False
    
    print(f"    [OK] Versión de Python compatible ({current_ver}).")
    return True

def check_security_files():
    """Comprueba la existencia de los archivos de autorización corporativa."""
    print("[*] Comprobando artefactos de seguridad corporativa...")
    encrypted_env = os.path.exists(".env.encrypted")
    env_key = os.path.exists(".env.key") or os.environ.get("SATURN_ENV_KEY") is not None
    
    if not encrypted_env:
        print("❌ ERROR: No se encontró el archivo de licencia sellada (.env.encrypted).")
        print("   Asegúrese de copiar todos los archivos entregados por Saturn Investments.")
        return False
        
    if not env_key:
        print("❌ ERROR: No se encontró la clave de descifrado (.env.key) ni la variable SATURN_ENV_KEY.")
        print("   Contacte a su administrador de Saturn Investments para obtener su credencial.")
        return False
        
    print("    [OK] Archivos de autorización y licencia detectados.")
    return True

def check_or_create_venv():
    """Verifica si existe un entorno virtual o asiste en su creación."""
    print("[*] Comprobando entorno de ejecución...")
    is_in_venv = sys.prefix != sys.base_prefix
    
    if is_in_venv:
        print(f"    [OK] Ejecutando dentro de un entorno virtual activo ({sys.prefix}).")
        return sys.executable
    
    venv_dir = os.path.join(os.getcwd(), "venv")
    if os.path.exists(venv_dir):
        print(f"    [OK] Entorno virtual local detectado en '{venv_dir}'.")
    else:
        print("    [!] No se detectó un entorno virtual activo.")
        ans = input("    ¿Desea crear un entorno virtual aislado automáticamente? [S/n]: ").strip().lower()
        if ans not in ("n", "no"):
            print("    [*] Creando entorno virtual 'venv'...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("    [OK] Entorno virtual creado exitosamente.")
            
    # Determinar ruta del ejecutable del venv
    if sys.platform.startswith("win"):
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")
        
    return venv_python if os.path.exists(venv_python) else sys.executable

def install_dependencies(python_bin):
    """Instala requirements.txt usando el ejecutable de Python determinado."""
    req_file = os.path.join(os.getcwd(), "requirements.txt")
    if not os.path.exists(req_file):
        print("❌ ERROR: No se encontró requirements.txt en el directorio actual.")
        return False
        
    print(f"[*] Instalando dependencias desde requirements.txt...")
    cmd = [python_bin, "-m", "pip", "install", "--upgrade", "pip"]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    cmd_req = [python_bin, "-m", "pip", "install", "-r", req_file]
    res = subprocess.run(cmd_req)
    
    if res.returncode != 0:
        print("❌ ERROR al instalar dependencias. Verifique su conexión a Internet o permisos.")
        return False
        
    print("    [OK] Todas las dependencias instaladas y verificadas.")
    return True

def run_system_diagnostic(python_bin):
    """Ejecuta una simulación rápida de prueba (smoke test) para confirmar el estado."""
    print("[*] Ejecutando diagnóstico de integridad y validación criptográfica...")
    sim_script = os.path.join(os.getcwd(), "scripts", "2_run_simulation.py")
    
    if not os.path.exists(sim_script):
        print("    [INFO] Instalación completa.")
        return True
        
    cmd_test = [python_bin, sim_script, "--scenarios", "100", "--days", "5"]
    res = subprocess.run(cmd_test, capture_output=True, text=True)
    
    if res.returncode == 0 and "Firma Digital Verificada" in res.stdout:
        print("    [OK] Autenticación y Motor de Simulación 100% operativos.")
        return True
    else:
        print(f"⚠️ Advertencia en la prueba diagnóstica:\n{res.stdout}\n{res.stderr}")
        return False

def main():
    print_banner()
    
    # 1. Comprobar Python
    if not check_python_version():
        sys.exit(1)
        
    # 2. Comprobar Seguridad
    if not check_security_files():
        sys.exit(1)
        
    # 3. Entorno Virtual
    python_bin = check_or_create_venv()
    
    # 4. Instalar Dependencias
    if not install_dependencies(python_bin):
        sys.exit(1)
        
    # 5. Diagnóstico de Integridad
    run_system_diagnostic(python_bin)
    
    print("\n=======================================================")
    print("🎉 ¡INSTALACIÓN Y CONFIGURACIÓN COMPLETADA CON ÉXITO!  ")
    print("=======================================================")
    print("\nPara ejecutar el motor de simulación:")
    if sys.platform.startswith("win") and os.path.exists("venv"):
        print("   .\\venv\\Scripts\\python.exe scripts/2_run_simulation.py")
    else:
        print("   python scripts/2_run_simulation.py")
    print("Para calibrar hiperparámetros, edite el archivo 'config.yaml'.\n")

if __name__ == "__main__":
    main()
