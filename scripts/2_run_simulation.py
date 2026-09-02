r"""
2_run_simulation.py
Motor de Prospectiva y Simulación de Escenarios (Monte Carlo + Neural Tensor).
Generación de Fan Chart (Cono de Incertidumbre).
(c) SaturnInvestments.com.mx
"""
import os
import sys
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from saturn.core.model import SaturnModel
from saturn.core.layers import Dense
from saturn.core.activations import Tanh, ReLU
from saturn.security.io import load_saturn_model
from saturn.utils.data_parser import load_financial_csv
from saturn.config import COMPANY_NAME, HIDE_BRANDING, load_yaml_config
from saturn.utils.visuals import apply_watermark

def main():
    # 1. Cargar configuración desde config.yaml si existe
    yaml_cfg = load_yaml_config()
    sim_cfg = yaml_cfg.get("simulation", {})
    data_cfg = yaml_cfg.get("data", {})
    stress_ranges = sim_cfg.get("stress_ranges", {})

    cfg_input_file = data_cfg.get("input_file", os.path.join("data", "input", "tmec_historico.csv"))
    cfg_model_name = sim_cfg.get("model_name", yaml_cfg.get("training", {}).get("model_name", "motor_tmec_v1"))
    if not cfg_model_name.endswith(".saturn"):
        cfg_model_name = f"{cfg_model_name}.saturn"
        
    cfg_scenarios = sim_cfg.get("scenarios", 5000)
    cfg_horizon = sim_cfg.get("horizon_days", 30)
    cfg_noise = sim_cfg.get("stochastic_noise", 0.15)
    cfg_spot = sim_cfg.get("spot", None)
    
    banxico_default = stress_ranges.get("banxico", [None, None])
    fed_default = stress_ranges.get("fed", [None, None])
    vix_default = stress_ranges.get("vix", [None, None])

    parser = argparse.ArgumentParser(description="Motor Operativo de Simulación - Stress Testing")
    parser.add_argument("--spot", type=float, default=cfg_spot, help=f"Precio spot inicial del USD/MXN. Defecto: {cfg_spot or 'Último histórico'}")
    parser.add_argument("--scenarios", type=int, default=cfg_scenarios, help=f"Número de trayectorias Monte Carlo. Defecto: {cfg_scenarios}")
    parser.add_argument("--days", type=int, default=cfg_horizon, help=f"Horizonte prospectivo en días hábiles. Defecto: {cfg_horizon}")
    parser.add_argument("--input-file", type=str, default=cfg_input_file, help=f"Ruta al archivo CSV de entrada. Defecto: {cfg_input_file}")
    parser.add_argument("--model-name", type=str, default=cfg_model_name, help=f"Nombre del archivo de modelo .saturn. Defecto: {cfg_model_name}")
    
    # Rangos para Análisis Combinatorio (Grid Search)
    parser.add_argument("--banxico_min", type=float, default=banxico_default[0], help=f"Límite inferior Banxico (%). Defecto: {banxico_default[0]}")
    parser.add_argument("--banxico_max", type=float, default=banxico_default[1], help=f"Límite superior Banxico (%). Defecto: {banxico_default[1]}")
    parser.add_argument("--fed_min", type=float, default=fed_default[0], help=f"Límite inferior Fed (%). Defecto: {fed_default[0]}")
    parser.add_argument("--fed_max", type=float, default=fed_default[1], help=f"Límite superior Fed (%). Defecto: {fed_default[1]}")
    parser.add_argument("--vix_min", type=float, default=vix_default[0], help=f"Límite inferior VIX. Defecto: {vix_default[0]}")
    parser.add_argument("--vix_max", type=float, default=vix_default[1], help=f"Límite superior VIX. Defecto: {vix_default[1]}")
    
    args = parser.parse_args()

    print("\n")
    print("==================================================")
    print(" INICIANDO MOTOR OPERATIVO DE SIMULACIÓN")
    print("==================================================\n")

    # 1. OBTENER PARÁMETROS DE ESTANDARIZACIÓN (Z-Score)
    print("[1/6] Analizando contexto macroeconómico base")
    csv_path = args.input_file
    x_train_raw, y_train = load_financial_csv(csv_path, target_col_index=-1)
    num_features = x_train_raw.shape[1]
    
    x_mean = np.mean(x_train_raw, axis=0)
    x_std = np.std(x_train_raw, axis=0)
    print(f"    [OK] Datos históricos procesados. Estandarización de {num_features} variables lista.")

    # 2. CARGAR EL MODELO YA ENTRENADO (.saturn)
    model_name = args.model_name
    if not model_name.endswith(".saturn"):
        model_name = f"{model_name}.saturn"
    model_path = os.path.join("data", "output", "models", model_name)
    print(f"[2/6] Cargando Red Neuronal ({model_name})")
    
    oraculo = SaturnModel()
    oraculo.add(Dense(num_features, 16))
    oraculo.add(Tanh())
    oraculo.add(Dense(16, 8))
    oraculo.add(ReLU())
    oraculo.add(Dense(8, 1))

    oraculo = load_saturn_model(model_path, oraculo)
    print("    [OK] Arquitectura Feed-Forward (Perceptrón Multicapa) y pesos sinápticos ensamblados.")

    # 3. GENERADOR SINTÉTICO: MONTE CARLO MULTI-PASO (Random Walk)
    print("[3/6] Configurando Hiperparámetros de Análisis Combinatorio (Grid Search)")
    num_escenarios = args.scenarios
    horizonte_dias = args.days
    
    escenario_base = x_train_raw[-1, :, 0]
    desviacion_historica = x_std[:, 0]
    
    if args.spot is not None:
        precio_spot_actual = args.spot
        print(f"    [INFO] Usando precio SPOT personalizado (What-If): {precio_spot_actual:.4f}")
    else:
        precio_spot_actual = y_train[-1][0][0]
        print(f"    [INFO] Usando precio SPOT histórico (Defecto): {precio_spot_actual:.4f}")

    # Inicializar matriz base: Todos los escenarios inician iguales al último día histórico
    estado_actual = np.tile(escenario_base, (num_escenarios, 1))
    
    # Inyectar límites combinatorios de Estrés si fueron proporcionados
    if args.banxico_min is not None and args.banxico_max is not None:
        print(f"   [INFO] Muestreo uniforme Banxico entre {args.banxico_min}% y {args.banxico_max}%")
        estado_actual[:, 0] = np.random.uniform(args.banxico_min, args.banxico_max, num_escenarios)
        
    if args.fed_min is not None and args.fed_max is not None:
        print(f"   [INFO] Muestreo uniforme Fed entre {args.fed_min}% y {args.fed_max}%")
        estado_actual[:, 1] = np.random.uniform(args.fed_min, args.fed_max, num_escenarios)
        
    if args.vix_min is not None and args.vix_max is not None:
        print(f"   [INFO] Muestreo uniforme Índice VIX entre {args.vix_min} y {args.vix_max}")
        estado_actual[:, 2] = np.random.uniform(args.vix_min, args.vix_max, num_escenarios)
        
    # Autocalcular diferencial de tasas si existen al menos 2 columnas
    if num_features >= 5:
        estado_actual[:, 4] = estado_actual[:, 0] - estado_actual[:, 1]
    
    print("[4/6] Ejecutando simulación prospectiva de variables")
    print(f"    [INFO] Proyectando {num_escenarios} trayectorias con evolución estocástica a {horizonte_dias} días.")
    
    trayectorias_usd_mxn = np.zeros((num_escenarios, horizonte_dias))
    for t in range(horizonte_dias):
        # Ruido gaussiano basado en volatilidad histórica
        ruido = np.random.normal(loc=0.0, scale=1.0, size=(num_escenarios, num_features))
        estado_actual = estado_actual + (ruido * desviacion_historica * cfg_noise) 
        
        # Estandarización y Forward Pass
        estado_actual_z = (estado_actual - x_mean[:, 0]) / (x_std[:, 0] + 1e-8)
        x_tensor = estado_actual_z.reshape(num_escenarios, num_features, 1)
        proyecciones_tensor = oraculo.predict(x_tensor)
        trayectorias_usd_mxn[:, t] = np.array([val[0][0] for val in proyecciones_tensor])
        proyecciones_tensor = oraculo.predict(x_tensor)
        trayectorias_usd_mxn[:, t] = np.array([val[0][0] for val in proyecciones_tensor])

    print("[5/6] Extrayendo fronteras probabilísticas y cuantificando riesgo de cola")
    dias = np.arange(1, horizonte_dias + 1)
    
    p5 = np.percentile(trayectorias_usd_mxn, 5, axis=0)   
    p25 = np.percentile(trayectorias_usd_mxn, 25, axis=0)
    p50 = np.percentile(trayectorias_usd_mxn, 50, axis=0) 
    p75 = np.percentile(trayectorias_usd_mxn, 75, axis=0)
    p95 = np.percentile(trayectorias_usd_mxn, 95, axis=0) 

    dias_plot = np.insert(dias, 0, 0)
    p5_plot = np.insert(p5, 0, precio_spot_actual)
    p25_plot = np.insert(p25, 0, precio_spot_actual)
    p50_plot = np.insert(p50, 0, precio_spot_actual)
    p75_plot = np.insert(p75, 0, precio_spot_actual)
    p95_plot = np.insert(p95, 0, precio_spot_actual)

    print("   [OK] Techo de Riesgo (Smax) y Piso Técnico (Smin) calculados.")

    # 4. EXPORTACIÓN DE RESULTADOS (CSV)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(os.path.join("data", "output", "simulations"), exist_ok=True)
    csv_fronteras_out = os.path.join("data", "output", "simulations", f"fronteras_riesgo_{timestamp}.csv")
    datos_fronteras = np.column_stack((dias_plot, p5_plot, p25_plot, p50_plot, p75_plot, p95_plot))
    np.savetxt(csv_fronteras_out, datos_fronteras, delimiter=",",
               header="Dia_Prospectivo,Smin_P5,P25,Consenso_P50,P75,Smax_P95", comments='')
               
    csv_distribucion_out = os.path.join("data", "output", "simulations", f"distribucion_dia_30_{timestamp}.csv")
    np.savetxt(csv_distribucion_out, trayectorias_usd_mxn[:, -1], delimiter=",",
               header="Proyeccion_USD_MXN_Dia_30", comments='')

    # 5. GENERACIÓN DE GRÁFICOS (Visuals / Fan Chart)
    print("[6/6] Renderizando Inteligencia Visual Directiva")
    plot_out = os.path.join("data", "output", "simulations", f"abanico_estres_{timestamp}.png")
    
    plt.figure(figsize=(12, 7))
    plt.fill_between(dias_plot, p5_plot, p95_plot, color='#d9272e', alpha=0.2, label='Incertidumbre Extrema (P5-P95)')
    plt.fill_between(dias_plot, p25_plot, p75_plot, color='#d9272e', alpha=0.4, label='Rango Intercuartil (P25-P75)')
    plt.plot(dias_plot, p50_plot, color='darkred', linewidth=2, linestyle='-', label='Consenso Algorítmico (Mediana)')
    plt.axhline(y=precio_spot_actual, color='black', linestyle='--', linewidth=1.5, label=f'Spot Actual ({precio_spot_actual:.4f})')

    plt.title('Fan Chart: Cono de Incertidumbre Geopolítica USD/MXN (30 días)', fontsize=14, fontweight='bold')
    plt.xlabel('Horizonte Prospectivo (Días Hábiles)', fontsize=12)
    plt.ylabel('Cotización USD/MXN Proyectada', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left')
    
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    # Aplicar marca de agua proveniente del binario .saturn
    model_meta = getattr(oraculo, 'metadata', None)
    apply_watermark(metadata=model_meta)

    plt.savefig(plot_out, dpi=300)
    plt.close()

    # GENERACIÓN DEL HISTOGRAMA (Distribución Final Día 30)
    plot_hist_out = os.path.join("data", "output", "simulations", f"distribucion_dia_30_{timestamp}.png")
    plt.figure(figsize=(10, 6))
    plt.hist(trayectorias_usd_mxn[:, -1], bins=60, color='#004b87', alpha=0.8, edgecolor='black')
    plt.title(f'Distribución Probabilística de Estrés Cambiario (Día {horizonte_dias})', fontsize=14, fontweight='bold')
    plt.xlabel('Proyección del Tipo de Cambio USD/MXN', fontsize=12)
    plt.ylabel('Frecuencia de Escenarios', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.axvline(p50[-1], color='darkred', linestyle='dashed', linewidth=2, label=f'Consenso: {p50[-1]:.4f}')
    plt.axvline(p95[-1], color='red', linestyle='dotted', linewidth=2, label=f'Techo P95: {p95[-1]:.4f}')
    plt.axvline(p5[-1], color='green', linestyle='dotted', linewidth=2, label=f'Piso P5: {p5[-1]:.4f}')
    
    plt.legend()
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    apply_watermark(metadata=model_meta)
    
    plt.savefig(plot_hist_out, dpi=300)
    plt.close()
    
    print(f"\n[OK] SIMULACIÓN PROSPECTIVA Y CONO DE ESTRÉS CONCLUIDOS EXITOSAMENTE.")
    print(f"[OUT] Matriz fronteras: {csv_fronteras_out}")
    print(f"[OUT] Fan Chart:        {plot_out}")
    print(f"[OUT] Histograma:       {plot_hist_out}\n")

if __name__ == "__main__":
    main()