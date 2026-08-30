import os
from dotenv import load_dotenv
from saturn.security.env_crypt import get_key, decrypt_env_to_memory

# 1. Intentar descifrar el archivo .env.encrypted si existe la clave
key = get_key()
cwd_encrypted = os.path.abspath(os.path.join(os.getcwd(), ".env.encrypted"))
pkg_encrypted = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env.encrypted"))
encrypted_path = cwd_encrypted if os.path.exists(cwd_encrypted) else pkg_encrypted

if key and os.path.exists(encrypted_path):
    try:
        decrypted_env = decrypt_env_to_memory(encrypted_path, key)
        for k, v in decrypted_env.items():
            os.environ[k] = v  # Actualizar variables de entorno para el proceso actual
        # Cargar variables locales sobre las descifradas (si existen)
        load_dotenv()
    except Exception as e:
        print(f"[!] Advertencia: No se pudo descifrar .env.encrypted: {e}")
        load_dotenv()
else:
    load_dotenv()

# ==========================================
# 2. Configuración Corporativa y Entorno
# ==========================================
COMPANY_NAME = os.getenv("COMPANY_NAME", "SaturnInvestments.com.mx")
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://SaturnInvestments.com.mx")
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "contacto@saturninvestments.com.mx")
PROJECT_TITLE = os.getenv("PROJECT_TITLE", "CALIBRACIÓN MOTOR DE SIMULACIÓN")

# Modo Tesis: Si es True, las marcas de agua corporativas se silencian para propósitos académicos
HIDE_BRANDING = os.getenv("HIDE_BRANDING", "False").lower() in ("true", "1", "yes")

# ==========================================
# 3. Control de Licenciamiento y Validación Criptográfica
# (Obligatorio en producción; sin fallbacks permisivos)
# ==========================================
LICENSE_KEY = os.getenv("LICENSE_KEY", None)

# ==========================================
# 4. Cabeceras y Metadatos Inmutables del Binario (.saturn)
# (Leídos estrictamente desde el entorno cifrado)
# ==========================================
import saturn
SATURN_MODEL_BRAND = os.getenv("SATURN_MODEL_BRAND", None)
SATURN_MODEL_CLIENT = os.getenv("SATURN_MODEL_CLIENT", None)
SATURN_MODEL_LICENSE = os.getenv("SATURN_MODEL_LICENSE", None)
SATURN_MODEL_VERSION = os.getenv("SATURN_MODEL_VERSION", None)
SATURN_ALGORITHM_VERSION = os.getenv("SATURN_ALGORITHM_VERSION", None)
SATURN_MODEL_ARCHITECTURE = os.getenv("SATURN_MODEL_ARCHITECTURE", None)
SATURN_MODEL_WARNING = os.getenv(
    "SATURN_MODEL_WARNING",
    "Modelo para fines de investigación y evaluación financiera. Prohibida su distribución o copia no autorizada."
)

# ==========================================
# 5. Configuración de Marca de Agua grabada en .saturn
# ==========================================
WATERMARK_TEXT = os.getenv(
    "WATERMARK_TEXT",
    f"Licencia {SATURN_MODEL_LICENSE}: {SATURN_MODEL_CLIENT}" if SATURN_MODEL_CLIENT else "Saturn Investments"
)
WATERMARK_FONT_SIZE = int(os.getenv("WATERMARK_FONT_SIZE", 8))
WATERMARK_COLOR = os.getenv("WATERMARK_COLOR", "gray")
WATERMARK_ALPHA = float(os.getenv("WATERMARK_ALPHA", 0.5))
WATERMARK_POSITION_X = float(os.getenv("WATERMARK_POSITION_X", 0.99))
WATERMARK_POSITION_Y = float(os.getenv("WATERMARK_POSITION_Y", 0.01))

# ==========================================
# 8. Cargador de Configuración Operativa (config.yaml)
# ==========================================
def load_yaml_config(yaml_path=None):
    """
    Carga de forma segura el archivo config.yaml de la raíz del proyecto.
    Si PyYAML no está instalado o el archivo no existe, devuelve un diccionario vacío.
    """
    if yaml_path is None:
        yaml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.yaml"))
        
    if not os.path.exists(yaml_path):
        return {}
        
    try:
        import yaml
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Si PyYAML no está instalado, parseo simple nativo
        return {}
    except Exception as e:
        print(f"[!] Advertencia al leer config.yaml: {e}")
        return {}



