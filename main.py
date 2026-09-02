"""
main.py
Orquestador Central y Punto de Entrada Unificado: Saturn Network.
Experiencia Zero-Setup: Auto-inicialización de entorno virtual y menú interactivo.

(c) SaturnInvestments.com.mx
"""
import os
import sys
import subprocess
import platform

# Asegurar compatibilidad de codificación en consola
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

def get_venv_python():
    """Retorna la ruta al ejecutable de Python del entorno virtual."""
    if sys.platform.startswith("win"):
        return os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
    return os.path.join(BASE_DIR, "venv", "bin", "python")

def is_running_in_venv():
    """Comprueba si el proceso actual se está ejecutando dentro de un entorno virtual."""
    return sys.prefix != sys.base_prefix

def find_compatible_python():
    """Selecciona un intérprete de Python óptimo (3.11 / 3.10) para máxima compatibilidad binaria."""
    if (sys.version_info.major, sys.version_info.minor) in ((3, 11), (3, 10)):
        return sys.executable
    if sys.platform.startswith("win"):
        try:
            res = subprocess.run(["py", "-3.11", "-c", "import sys; print(sys.executable)"], capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(res.stdout.strip()):
                return res.stdout.strip()
        except Exception:
            pass
    return sys.executable

def bootstrap_environment():
    """Garantiza la existencia del entorno virtual y sus dependencias (Zero-Setup)."""
    venv_python = get_venv_python()
    
    if not os.path.exists(venv_python):
        print("\n" + "=" * 69)
        print("    MOTOR OPERATIVO DE SIMULACIÓN FINANCIERA by SATURN INVESTMENTS   ")
        print("    www.SaturnInvestments.com.mx")
        print("=" * 69 + "\n")
        print("[*] Configurando entorno virtual aislado por primera vez...")
        
        base_python = find_compatible_python()
        
        # 1. Crear venv
        subprocess.run([base_python, "-m", "venv", os.path.join(BASE_DIR, "venv")], check=True)
        print("    [OK] Entorno virtual 'venv' creado.")
        
        # 2. Instalar dependencias
        req_file = os.path.join(BASE_DIR, "requirements.txt")
        if os.path.exists(req_file):
            print("[*] Instalando dependencias requeridas (requirements.txt)...")
            subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run([venv_python, "-m", "pip", "install", "-r", req_file], check=True)
            print("    [OK] Dependencias instaladas exitosamente.\n")

    return venv_python

def ensure_venv_trampoline():
    """Si no estamos dentro del venv, nos relanzamos usando el Python del venv."""
    if not is_running_in_venv():
        venv_python = bootstrap_environment()
        if os.path.exists(venv_python) and venv_python != sys.executable:
            # Relanzar el proceso usando el intérprete del entorno virtual
            cmd = [venv_python] + sys.argv
            sys.exit(subprocess.call(cmd))

# Ejecutar trampoline de inmediato antes de cargar módulos pesados
ensure_venv_trampoline()

# Cargar utilidades de configuración de Saturn
from saturn.config import load_yaml_config

def print_header():
    print("\n" + "=" * 69)
    print("    MOTOR OPERATIVO DE SIMULACIÓN FINANCIERA by SATURN INVESTMENTS   ")
    print("    www.SaturnInvestments.com.mx")
    print("=" * 69 + "\n")

def prompt_param(message, default_val):
    """Solicita un parámetro al usuario mostrando el valor por defecto. En modo no interactivo toma el defecto."""
    if not sys.stdin.isatty():
        print(f"  • {message} [Defecto: {default_val}]")
        return default_val
    user_val = input(f"  • {message} [Defecto: {default_val}]: ").strip()
    return user_val if user_val else default_val

def run_prepare_data(yaml_cfg):
    print("\n--- [INGESTA Y PREPROCESAMIENTO DE DATOS] ---")
    data_cfg = yaml_cfg.get("data", {})
    def_daily = "data/input/base_diario.csv"
    def_monthly = "data/input/base_mensual.csv"
    def_output = data_cfg.get("input_file", "data/input/tmec_historico.csv")
    
    daily_file = prompt_param("Ruta de series diarias CSV", def_daily)
    monthly_file = prompt_param("Ruta de series mensuales CSV", def_monthly)
    output_file = prompt_param("Ruta de salida procesada", def_output)
    
    venv_python = get_venv_python() if not is_running_in_venv() else sys.executable
    script_path = os.path.join(BASE_DIR, "scripts", "0_prepare_data.py")
    
    cmd = [venv_python, script_path, "--daily", daily_file, "--monthly", monthly_file, "--output", output_file]
    print(f"\n[*] Ejecutando: python scripts/0_prepare_data.py --daily {daily_file} --monthly {monthly_file} --output {output_file}\n")
    subprocess.run(cmd)

def run_train_model(yaml_cfg):
    print("\n--- [CALIBRACIÓN Y ENTRENAMIENTO DE RED NEURONAL] ---")
    train_cfg = yaml_cfg.get("training", {})
    def_epochs = train_cfg.get("epochs", 1000)
    def_interval = train_cfg.get("interval", 200)
    def_model_name = train_cfg.get("model_name", "motor_tmec_v1")
    
    epochs = prompt_param("Épocas de entrenamiento", str(def_epochs))
    interval = prompt_param("Intervalo de reporte de pérdida", str(def_interval))
    model_name = prompt_param("Nombre del artefacto compilado (.saturn)", def_model_name)
    
    venv_python = get_venv_python() if not is_running_in_venv() else sys.executable
    script_path = os.path.join(BASE_DIR, "scripts", "1_train_model.py")
    
    cmd = [venv_python, script_path, "--epochs", epochs, "--interval", interval, "--model-name", model_name]
    print(f"\n[*] Ejecutando: python scripts/1_train_model.py --epochs {epochs} --interval {interval} --model-name {model_name}\n")
    subprocess.run(cmd)

def run_forecast_simulation(yaml_cfg):
    print("\n--- [GENERAR FORECAST Y CONOS DE ESTRÉS (MOTOR NEURONAL)] ---")
    sim_cfg = yaml_cfg.get("simulation", {})
    def_scenarios = sim_cfg.get("num_scenarios", 5000)
    def_days = sim_cfg.get("horizon_days", 30)
    
    scenarios = prompt_param("Número de trayectorias proyectadas", str(def_scenarios))
    days = prompt_param("Horizonte de proyección en días hábiles", str(def_days))
    spot_price = prompt_param("Precio SPOT inicial USD/MXN (vacio = histórico)", "")
    
    venv_python = get_venv_python() if not is_running_in_venv() else sys.executable
    script_path = os.path.join(BASE_DIR, "scripts", "2_run_simulation.py")
    
    cmd = [venv_python, script_path, "--scenarios", scenarios, "--days", days]
    if spot_price:
        cmd.extend(["--spot", spot_price])
        
    print(f"\n[*] Ejecutando: python scripts/2_run_simulation.py --scenarios {scenarios} --days {days}\n")
    subprocess.run(cmd)

def open_terminal_with_venv():
    """Abre una sub-terminal interactiva con el entorno virtual activo."""
    print("\n[*] Abriendo sesión de terminal con el entorno virtual activado...")
    print("    Escriba 'exit' para regresar a este menú cuando termine.\n")
    
    env = os.environ.copy()
    venv_dir = os.path.join(BASE_DIR, "venv")
    
    if sys.platform.startswith("win"):
        venv_scripts = os.path.join(venv_dir, "Scripts")
        env["PATH"] = f"{venv_scripts};{env.get('PATH', '')}"
        env["VIRTUAL_ENV"] = venv_dir
        subprocess.run(["powershell.exe", "-NoExit", "-Command", f"Write-Host 'Entorno virtual activo en {venv_dir}' -ForegroundColor Green"], env=env)
    else:
        venv_bin = os.path.join(venv_dir, "bin")
        env["PATH"] = f"{venv_bin}:{env.get('PATH', '')}"
        env["VIRTUAL_ENV"] = venv_dir
        shell = env.get("SHELL", "/bin/bash")
        subprocess.run([shell], env=env)

def main():
    yaml_cfg = load_yaml_config()
    
    # Manejo de flags directos por CLI si se proporcionan
    if len(sys.argv) > 1:
        flag = sys.argv[1].lower()
        if flag in ("--simulate", "-s", "--forecast", "-f"):
            run_forecast_simulation(yaml_cfg)
            return
        elif flag in ("--train", "-t"):
            run_train_model(yaml_cfg)
            return
        elif flag in ("--prepare", "-p"):
            run_prepare_data(yaml_cfg)
            return
        elif flag in ("--help", "-h"):
            print("Uso: python main.py [opciones]")
            print("  --forecast, -f, --simulate, -s : Ejecutar forecast y conos de estrés")
            print("  --train, -t                   : Calibrar y entrenar red neuronal")
            print("  --prepare, -p                 : Ingesta y preprocesamiento de datos")
            return

    while True:
        print_header()
        print("GUÍA DE OPERACIONES DISPONIBLES:")
        print("  [1] 📥 Ingesta y Preprocesamiento de Datos (0_prepare_data.py)")
        print("      -> Valida y estandariza series de tiempo macroeconómicas (T-MEC).\n")
        print("  [2] 🧠 Calibrar / Entrenar Red Neuronal (1_train_model.py)")
        print("      -> Ajusta pesos sinápticos y sella el artefacto binario .saturn.\n")
        print("  [3] 📊 Generar Forecast y Conos de Estrés (2_run_simulation.py)")
        print("      -> Proyecta trayectorias, calcula fronteras y genera Fan Charts.\n")
        print("  [4] 💻 Abrir Terminal Interactiva (con entorno virtual activado)")
        print("  [5] 🚪 Salir")
        print("=" * 70)
        
        opcion = input("Seleccione una opción [1-5] (Defecto: 3): ").strip()
        if not opcion:
            opcion = "3"
            
        if opcion == "1":
            run_prepare_data(yaml_cfg)
        elif opcion == "2":
            run_train_model(yaml_cfg)
        elif opcion == "3":
            run_forecast_simulation(yaml_cfg)
        elif opcion == "4":
            open_terminal_with_venv()
        elif opcion == "5":
            print("\n👋 Gracias por utilizar SATURN INVESTMENTS. Sesión finalizada.")
            break
        else:
            print("\n❌ Opción no válida. Por favor seleccione un número del 1 al 5.")
            
        try:
            input("\nPresione [ENTER] para volver al menú principal...")
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    main()
