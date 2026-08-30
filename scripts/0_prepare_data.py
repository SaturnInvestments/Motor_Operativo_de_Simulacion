import pandas as pd
import os

def main():
    # Rutas a los archivos
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    daily_file = os.path.join(base_dir, 'input', 'base_diario.csv')
    monthly_file = os.path.join(base_dir, 'input', 'base_mensual.csv')
    output_file = os.path.join(base_dir, 'input', 'tmec_historico.csv')

    print("Cargando datos...")
    df_daily = pd.read_csv(daily_file)
    df_monthly = pd.read_csv(monthly_file)

    # 1. Estandarización de Fechas
    df_daily['date'] = pd.to_datetime(df_daily['date'], format='%d/%m/%Y')
    df_monthly['date'] = pd.to_datetime(df_monthly['date'], format='%Y-%m-%d')

    # Seleccionar las columnas de interés de la base mensual
    cols_to_keep = ['date', 'remesas_mdd', 'diferencial_tasas', 'remesas_z', 'remesas_var_anual_pct']
    df_monthly_filtered = df_monthly[cols_to_keep]

    # 2. Fusión de los Datos (Merge)
    # Left join usando la fecha
    df_merged = pd.merge(df_daily, df_monthly_filtered, on='date', how='left')
    df_merged = df_merged.sort_values('date')

    # 3. Aplicación de Forward Fill (ffill)
    cols_to_ffill = ['remesas_mdd', 'diferencial_tasas', 'remesas_z', 'remesas_var_anual_pct']
    df_merged[cols_to_ffill] = df_merged[cols_to_ffill].ffill()

    # 4. Limpieza Final y Eliminación de Fechas
    # Eliminar filas (días iniciales) que quedaron con NaN antes del primer dato mensual
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
    df_final.to_csv(output_file, index=False)
    
    print(f"\nProceso completado.")
    print(f"Archivo guardado en: {output_file}")
    print(f"Forma final del dataset: {df_final.shape}")
    print(f"Columnas incluidas: {df_final.columns.tolist()}")

if __name__ == '__main__':
    main()
