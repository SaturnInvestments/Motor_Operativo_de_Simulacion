
"""
printout.py
Módulo centralizado para la gestión de banners y branding corporativo.
(c) SaturnInvestments.com.mx
"""

from saturn.config import COMPANY_NAME, COMPANY_WEBSITE, HIDE_BRANDING

def print_saturn_banner(licencia="Desconocida", cliente="Desconocido"):
    """
    Imprime el banner oficial ineludible al cargar un archivo .saturn.
    """
    print(f"\n=======================================================")
    print(f"[START] INICIANDO MOTOR OPERATIVO DE SIMULACIÓN (.saturn)")
    if not HIDE_BRANDING:
        print(f"© {COMPANY_NAME} - Todos los derechos reservados")
    else:
        print("Proyecto de Investigación Académica")
    print(f"Licencia detectada: {licencia}")
    print(f"Cliente/Usuario: {cliente}")
    print(f"=======================================================\n")

def print_epoch_progress(epoch, total_epochs, loss_value):
    """
    Imprime el progreso del entrenamiento con la marca corporativa.
    """
    print(f"    Época {epoch}/{total_epochs} - Desviación cuadrática media: {loss_value:.6f}")

def print_security_warning():
    """
    Advertencia legal en caso de fallo de licencia.
    """
    print("\n[!] ADVERTENCIA DE SEGURIDAD Y LICENCIAMIENTO [!]")
    print("El uso comercial o corporativo de este framework requiere una licencia válida.")
    if not HIDE_BRANDING:
        print(f"Para adquirir la versión Enterprise, contacte a: {COMPANY_NAME} o {COMPANY_WEBSITE}")
    print("El proceso ha sido abortado por violación de licencia.\n")