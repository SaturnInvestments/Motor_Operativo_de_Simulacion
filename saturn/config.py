import os
from dotenv import load_dotenv
from saturn.security.env_crypt import get_key, decrypt_env_to_memory

# 1. Intentar descifrar el archivo .env.encrypted si existe la clave
key = get_key()
encrypted_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env.encrypted"))

if key and os.path.exists(encrypted_path):
    try:
        decrypted_env = decrypt_env_to_memory(encrypted_path, key)
        for k, v in decrypted_env.items():
            os.environ.setdefault(k, v)
        # Cargar variables locales sobre las descifradas (si existen)
        load_dotenv()
    except Exception as e:
        print(f"[!] Advertencia: No se pudo descifrar .env.encrypted: {e}")
        load_dotenv()
else:
    load_dotenv()

COMPANY_NAME = os.getenv("COMPANY_NAME", "SaturnInvestments.com.mx")
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://SaturnInvestments.com.mx")
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "contacto@saturninvestments.com.mx")

PROJECT_TITLE = os.getenv("PROJECT_TITLE", "CALIBRACIÓN SATURN NETWORK")
DEFAULT_CLIENT = os.getenv("DEFAULT_CLIENT", "Cliente Genérico")
MODEL_EXPORT_NAME = os.getenv("MODEL_EXPORT_NAME", "motor_v1")
TRAIN_EPOCHS = int(os.getenv("TRAIN_EPOCHS", 150))
TRAIN_EPOCHS_INTERVAL_PRINT = int(os.getenv("TRAIN_EPOCHS_INTERVAL_PRINT", 10))

# MODO TESIS: Si es "True", las marcas de agua y mensajes de branding genéricos se ocultan
HIDE_BRANDING = os.getenv("HIDE_BRANDING", "False").lower() in ("true", "1", "yes")

# ==========================================
# Control de Licenciamiento y Seguridad
# ==========================================
LICENSE_TYPE = os.getenv("LICENSE_TYPE", "AGPLv3 (Académica)")
LICENSE_KEY = os.getenv("LICENSE_KEY", "")

# ==========================================
# Configuración de Marca de Agua en Gráficos
# ==========================================
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", "Proyecto de Investigación Académica" if HIDE_BRANDING else COMPANY_NAME)
WATERMARK_FONT_SIZE = int(os.getenv("WATERMARK_FONT_SIZE", 8))
WATERMARK_COLOR = os.getenv("WATERMARK_COLOR", "gray")
WATERMARK_ALPHA = float(os.getenv("WATERMARK_ALPHA", 0.5))
WATERMARK_POSITION_X = float(os.getenv("WATERMARK_POSITION_X", 0.99))
WATERMARK_POSITION_Y = float(os.getenv("WATERMARK_POSITION_Y", 0.01))

# ==========================================
# Cabeceras y Metadatos del archivo .saturn
# ==========================================
SATURN_MODEL_BRAND = os.getenv("SATURN_MODEL_BRAND", "Proyecto de Investigación Académica" if HIDE_BRANDING else COMPANY_NAME)
SATURN_MODEL_WARNING = os.getenv("SATURN_MODEL_WARNING", "Modelo para fines académicos y de investigación." if HIDE_BRANDING else f"El uso corporativo requiere licencia comercial. Contacte a {COMPANY_NAME}.")

