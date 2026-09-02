import pandas as pd
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Ingesta y Preprocesamiento de Series Macroeconómicas T-MEC")
    parser.add_argument("--daily", type=str, default=os.path.join("data", "input", "base_diario.csv"), help="Ruta al CSV con series diarias")
    parser.add_argument("--monthly", type=str, default=os.path.join("data", "input", "base_mensual.csv"), help="Ruta al CSV con series mensuales")
    parser.add_argument("--output", type=str, default=os.path.join("data", "input", "tmec_historico.csv"), help="Ruta de salida del dataset preparado")
    args = parser.parse_args()

    daily_file = args.daily
    monthly_file = args.monthly
    output_file = args.output

    if not os.path.exists(daily_file):
        print(f"❌ ERROR: No se encontró el archivo de series diarias: {daily_file}")
        print("   Asegúrese de colocar 'base_diario.csv' en la carpeta data/input/.")
        return

    if not os.path.exists(monthly_file):
        print(f"❌ ERROR: No se encontró el archivo de series mensuales: {monthly_file}")
        print("   Asegúrese de colocar 'base_mensual.csv' en la carpeta data/input/.")
        return

    print("==================================================")
    print(" INGESTADOR DE DATOS MACROECONÓMICOS (T-MEC)")
    print("==================================================\n")
    print(f"[*] Cargando series diarias desde:  {daily_file}")
    print(f"[*] Cargando series mensuales desde: {monthly_file}")

    df_daily = pd.read_csv(daily_file)
    df_monthly = pd.read_csv(monthly_file)

    # 1. Estandarización de Fechas
    df_daily['date'] = pd.to_datetime(df_daily['date'], format='%d/%m/%Y', errors='coerce')
    df_monthly['date'] = pd.to_datetime(df_monthly['date'], format='%Y-%m-%d', errors='coerce')

    # Seleccionar las columnas de interés de la base mensual
    cols_to_keep = ['date', 'remesas_mdd', 'diferencial_tasas', 'remesas_z', 'remesas_var_anual_pct']
    existing_cols = [c for c in cols_to_keep if c in df_monthly.columns]
    df_monthly_filtered = df_monthly[existing_cols]

    # 2. Fusión de los Datos (Merge)
    # Left join usando la fecha
    df_merged = pd.merge(df_daily, df_monthly_filtered, on='date', how='left')
    df_merged = df_merged.sort_values('date')

    # 3. Aplicación de Forward Fill (ffill)
    cols_to_ffill = [c for c in existing_cols if c != 'date']
    df_merged[cols_to_ffill] = df_merged[cols_to_ffill].ffill()

    # 4. Limpieza Final y Eliminación de Fechas
    df_merged = df_merged.dropna()

    # Eliminar la columna 'date' para evitar ruido en la red neuronal
    df_final = df_merged.drop(columns=['date'])
    
    # Mover USD_MXN a la última posición (variable objetivo)
    cols = df_final.columns.tolist()
    if 'USD_MXN' in cols:
        cols.remove('USD_MXN')
        cols.append('USD_MXN')
        df_final = df_final[cols]

    # Guardar el resultado final
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    df_final.to_csv(output_file, index=False)
    
    print(f"\n[OK] Preprocesamiento y fusión de frecuencias concluido exitosamente.")
    print(f"     Archivo generado en: {output_file}")
    print(f"     Dimensiones del dataset: {df_final.shape[0]} muestras x {df_final.shape[1]} variables")
    print(f"     Columnas estructuradas: {', '.join(df_final.columns)}")

if __name__ == '__main__':
    main()
