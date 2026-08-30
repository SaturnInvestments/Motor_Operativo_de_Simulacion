"""
visuals.py
Motor de renderizado de gráficos y reportes para series temporales.
(c) SaturnInvestments.com.mx
"""
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para guardar imágenes sin requerir Tkinter
import matplotlib.pyplot as plt
import os
import datetime
from saturn.config import COMPANY_NAME, HIDE_BRANDING

def _ensure_dir(path):
    """Verifica que el directorio exista, si no, lo crea."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def apply_watermark(plt_ref=None, metadata=None):
    """
    Aplica la marca de agua configurada en el gráfico activo.
    Si se proporciona `metadata` (proveniente del archivo .saturn), se utilizan
    los valores sellados en el artefacto binario.
    """
    from saturn.config import (
        HIDE_BRANDING, WATERMARK_TEXT, WATERMARK_FONT_SIZE,
        WATERMARK_COLOR, WATERMARK_ALPHA, WATERMARK_POSITION_X, WATERMARK_POSITION_Y
    )
    if HIDE_BRANDING:
        return
        
    p_ref = plt_ref if plt_ref is not None else plt

    if metadata and isinstance(metadata, dict):
        text = metadata.get('watermark_text', metadata.get('cliente', WATERMARK_TEXT))
        font_size = int(metadata.get('watermark_font_size', WATERMARK_FONT_SIZE))
        color = metadata.get('watermark_color', WATERMARK_COLOR)
        alpha = float(metadata.get('watermark_alpha', WATERMARK_ALPHA))
        pos_x = float(metadata.get('watermark_pos_x', WATERMARK_POSITION_X))
        pos_y = float(metadata.get('watermark_pos_y', WATERMARK_POSITION_Y))
    else:
        text = WATERMARK_TEXT
        font_size = WATERMARK_FONT_SIZE
        color = WATERMARK_COLOR
        alpha = WATERMARK_ALPHA
        pos_x = WATERMARK_POSITION_X
        pos_y = WATERMARK_POSITION_Y

    # Auto-agregar fecha si es una firma de marca genérica
    if "{date}" in text:
        text = text.replace("{date}", datetime.datetime.now().strftime("%Y-%m-%d"))
    elif "©" in text or "Investigación" in text or "Saturn" in text or "Licencia" in text:
        text = f"{text} | {datetime.datetime.now().strftime('%Y-%m-%d')}"

    p_ref.figtext(
        pos_x,
        pos_y,
        text,
        horizontalalignment='right',
        fontsize=font_size,
        color=color,
        alpha=alpha
    )

def plot_loss_curve(loss_history, output_dir="data/output/plots/"):
    """
    Genera y guarda la gráfica de Convergencia del Modelo (Pérdida vs Épocas).
    """
    filepath = os.path.join(output_dir, "convergencia_entrenamiento.png")
    _ensure_dir(filepath)

    plt.figure(figsize=(10, 6))
    plt.plot(loss_history, color='#004b87', linewidth=2, label='Error Cuadrático Medio (MSE)')
    
    # Estilizado y Branding
    plt.title('Curva de Calibración Histórica Continua', fontsize=14, fontweight='bold')
    plt.xlabel('Épocas (Iteraciones)', fontsize=12)
    plt.ylabel('Magnitud del Error Financiero', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Marca de agua corporativa centralizada
    apply_watermark()

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)  # Resolución de alta calidad para tu tesis
    plt.close()
    
    print(f"    [PLOT] Gráfico de convergencia exportado en: {filepath}")

def plot_predictions(y_real, y_pred, output_dir="data/output/plots/"):
    """
    Genera y guarda la gráfica comparativa entre los datos reales del mercado 
    y la proyección del Motor Operativo de Simulación.
    """
    filepath = os.path.join(output_dir, "proyeccion_vs_realidad.png")
    _ensure_dir(filepath)

    # Aplanar los tensores para graficarlos fácilmente
    real_values = [val[0][0] for val in y_real]
    pred_values = [val[0][0] for val in y_pred]

    plt.figure(figsize=(10, 6))
    plt.plot(real_values, color='black', linewidth=2, label='Mercado Real (Banxico/Fed)')
    plt.plot(pred_values, color='#d9272e', linewidth=2, linestyle='dashed', label='Proyección del Motor Operativo de Simulación')
    
    # Estilizado y Branding
    plt.title('Simulación de Estrés Cambiario T-MEC', fontsize=14, fontweight='bold')
    plt.xlabel('Escenarios / Tiempo', fontsize=12)
    plt.ylabel('Cotización USD/MXN', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Marca de agua corporativa centralizada
    apply_watermark()

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()

    print(f"    [PLOT] Gráfico de simulación exportado en: {filepath}")