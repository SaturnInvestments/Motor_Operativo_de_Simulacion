# Motor Operativo de Simulación Financiera

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Architecture: Tensor Sequential](https://img.shields.io/badge/Architecture-Tensor%20Sequential%20ML-orange.svg)](#-arquitectura-tecnológica)
[![Explainable AI](https://img.shields.io/badge/XAI-Shapley%20Values-purple.svg)](#-explicabilidad-directiva-xai)

Este **Motor Operativo de Simulación** es un framework basado en inteligencia artificial y redes neuronales secuenciales, diseñado para la gestión de tesorería y evaluación de riesgos financieros. Se enfoca particularmente en la cotización del par peso mexicano frente al dólar estadounidense (**USD/MXN**), modelando la incertidumbre macroeconómica y geopolítica inherente al Tratado entre México, Estados Unidos y Canadá (**T-MEC**).

A diferencia de los modelos econométricos tradicionales de inferencia estática, esta arquitectura no busca adivinar un "tipo de cambio futuro determinista", sino que **cartografía el riesgo** mediante simulaciones combinatorias masivas y tensores matemáticos. El resultado es una herramienta de Inteligencia Visual Directiva (Fan Charts y valores SHAP) que asiste a comités de finanzas en la toma de decisiones para proteger márgenes operativos y justificar coberturas cambiarias.

---

## 📋 Tabla de Contenido

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Características Principales](#-características-principales)
- [Requisitos e Instalación](#️-requisitos-e-instalación)
- [Flujo Operativo (Scripts)](#-flujo-operativo-scripts)
  - [Módulo 0: Ingesta y Preparación](#módulo-0-ingesta-y-preparación-de-datos)
  - [Módulo 1: Calibración y Encapsulamiento](#módulo-1-calibración-de-red-neuronal-y-encapsulamiento)
  - [Módulo 2: Simulación y Cobertura](#módulo-2-simulación-de-estrés-geopolítico-y-cobertura)
- [Explicabilidad Directiva (XAI)](#-explicabilidad-directiva-xai)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Referencias Destacadas](#-referencias-destacadas)

---

## 📖 Acerca del Proyecto

El desarrollo de este ecosistema parte de la premisa fundamental de que *"el algoritmo de IA no reemplaza el criterio del financiero, sino que cuantifica las relaciones causa-efecto"*. Todo el marco teórico, justificación econométrica y diseño algorítmico de este proyecto están fundamentados en la investigación plasmada en el documento **"Inteligencia_Artificial_Explicable_para_la_Optimizacion_de_la_Gestion_de_Tesoreria_y_Riesgos_Financieros.pdf"** *(próximamente a ser publicado)*.

El modelo filtra variables predictoras en cuatro dimensiones estructurales:
1. **Carry Trade**: Diferenciales de política monetaria (Banxico vs. Fed) y spreads de deuda soberana.
2. **Ecosistema T-MEC**: Balanza comercial manufacturera y flujos de Inversión Extranjera Directa (IED) por *nearshoring*.
3. **Incertidumbre Geopolítica**: Índices de incertidumbre de política económica (EPU), volatilidad implícita (VIX) y variables categóricas de fricción diplomática.
4. **Macroeconomía Real**: Diferenciales inflacionarios e indicadores de actividad industrial.

Mediante filtros de regímenes de mercado (funciones de activación hiperbólicas y rectificadas), el sistema es capaz de diferenciar el ruido diario de las verdaderas crisis estructurales que detonan ventas de pánico.

---

## 🌟 Características Principales

- 🧠 **Arquitectura Tensor Sequential**: Una red interactiva de agregación de factores de riesgo con filtros de no-linealidad que simulan los "pisos técnicos" y la "memoria estocástica" del mercado cambiario.
- 📉 **Inteligencia Visual Directiva**: Generación de *Fan Charts* (Conos de Incertidumbre) que exponen de forma clara el "techo de riesgo" y el "piso técnico" a los directivos.
- 🔍 **Atribución Causal (XAI)**: Descomposición exacta del impacto de cada variable económica en el pronóstico final utilizando Teoría de Juegos Cooperativos (*Shapley Values*).
- 🛡️ **Inmutabilidad Causal**: Tras el entrenamiento, el conocimiento financiero se compila en un archivo serializado `.saturn` agnóstico a la tecnología, evitando la descalibración durante las pruebas de estrés corporativas.

---

## 🛠️ Requisitos e Instalación

### Prerrequisitos del Sistema
- **Sistema Operativo**: Windows 10/11, macOS o distribuciones Linux (Ubuntu/Debian).
- **Python**: Versión 3.8 o superior (se recomiendan versiones de 64-bits para un manejo eficiente de tensores).
- Memoria RAM mínima recomendada de 8 GB para operaciones de simulación estocástica.

### Proceso de Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/SaturnInvestments/Motor_Operativo_de_Simulacion.git
cd Motor_Operativo_de_Simulacion
```

2. **Crear y activar un entorno virtual**:

*En Windows (PowerShell):*
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*En Linux / macOS:*
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar las dependencias matemáticas y operativas**:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración Operativa (`config.yaml`)

El proyecto cuenta con un archivo centralizado **[`config.yaml`](file:///c:/projects/software/saturn_github/motor_operativo_de_simulacion/config.yaml)** en la raíz. Si ejecutas los scripts sin parámetros por consola, el motor tomará automáticamente los valores definidos en este archivo:

```yaml
data:
  input_file: "data/input/tmec_historico.csv"

training:
  epochs: 1000
  interval: 200
  learning_rate: 0.005
  model_name: "motor_tmec_v1"

simulation:
  scenarios: 5000
  horizon_days: 30
  stochastic_noise: 0.15
  spot: null               # Si es null, toma el último valor histórico
  stress_ranges:
    banxico: [10.0, 11.5]
    fed: [5.0, 5.5]
    vix: [15.0, 35.0]
```

---

## 🚀 Flujo Operativo (Scripts)

El ecosistema transforma el caos macroeconómico en inteligencia accionable a través de tres fases estrictas:

### Módulo 0: Ingesta y Preparación de Datos
**Ejecución:** `python scripts/0_prepare_data.py`

Sincroniza y estructura la inteligencia de mercado. **Los datos base deben depositarse en formato `.csv` dentro de la ruta `data/input/`** (por ejemplo, `tmec_historico.csv`). Las series de tiempo requeridas incluyen: Tasa de interés Banxico, Tasa de la Reserva Federal (Fed), Índice VIX, Índice de Incertidumbre de Política Económica (EPU), flujos comerciales y la cotización histórica USD/MXN. *(La selección rigurosa y justificación econométrica de estas variables se detalla a profundidad en "Inteligencia_Artificial_Explicable_para_la_Optimizacion_de_la_Gestion_de_Tesoreria_y_Riesgos_Financieros.pdf").*

- **Homologación de frecuencias mixtas**: Alinea matemáticamente series de tiempo diarias (VIX, TIIE) con variables mensuales o trimestrales (Remesas, IED), arrastrando el último dato conocido.
- **Estandarización (Z-Score)**: Comprime las variables absolutas a una escala normalizada (media cero y varianza unitaria) para evitar que variables como la masa monetaria "cieguen" al modelo frente a variaciones de tasas de interés.
- **Estabilización de varianza**: Aplicación de transformaciones logarítmicas y diferencias marginales basadas en pruebas de raíz unitaria (Dickey-Fuller) para evitar regresiones espurias.

### Módulo 1: Calibración de Red Neuronal y Encapsulamiento
**Ejecución:** `python scripts/1_train_model.py`

Realiza una auditoría histórica automatizada donde el algoritmo revisa iteraciones pasadas de datos macroeconómicos:
- **Calibración por costo financiero**: Ajusta las sensibilidades internas mediante la minimización del Error Cuadrático Medio, penalizando exponencialmente desviaciones graves (simulando los quiebres de caja).
- **Encapsulamiento Cuantitativo e Inmutabilidad**: Detiene el aprendizaje deliberadamente al alcanzar madurez algorítmica y serializa la topología, pesos y metadatos de versión en un archivo `motor_tmec_v1.saturn`.

**Parámetros configurables en CLI:**
| Parámetro | Tipo | Descripción | Defecto |
| :--- | :--- | :--- | :--- |
| `--epochs` | Int | Número de épocas / iteraciones de optimización | `1000` |
| `--interval` | Int | Frecuencia de impresión en consola | `200` |
| `--model-name` | String | Nombre del archivo binario serializado resultante | `motor_tmec_v1` |
| `--client` | String | Nombre de la entidad o cliente corporativo | `Cliente Genérico` |

*Ejemplo de ejecución personalizada:*
```bash
python scripts/1_train_model.py --epochs 1500 --interval 100 --model-name motor_tmec_v2
```

### Módulo 2: Simulación de Estrés Geopolítico y Cobertura
**Ejecución:** `python scripts/2_run_simulation.py`

"Despierta" el modelo encapsulado para realizar análisis combinatorios frente a escenarios extremos (Grid Search dinámico):
- Inyecta fluctuaciones estadísticas masivas (ruido gaussiano) sobre variables exógenas, generando miles de realidades macroeconómicas paralelas para un horizonte temporal futuro (e.g., 30 días).

**Parámetros configurables en CLI:**
| Parámetro | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `--spot` | Float | Tipo de cambio Spot USD/MXN base actual | `--spot 19.50` |
| `--banxico_min` / `--banxico_max` | Float | Rango de tasa de interés Banxico estresada | `--banxico_min 10.0 --banxico_max 11.5` |
| `--fed_min` / `--fed_max` | Float | Rango de tasa objetivo de la Reserva Federal | `--fed_min 4.75 --fed_max 5.50` |
| `--vix_min` / `--vix_max` | Float | Rango de volatilidad del índice VIX global | `--vix_min 15.0 --vix_max 35.0` |

*Ejemplo de ejecución con parámetros:*
```bash
python scripts/2_run_simulation.py --spot 19.50 --banxico_min 10.0 --banxico_max 11.5 --fed_min 5.0 --fed_max 5.5
```

- **Salidas Visuales**:
  - `abanico_estres.png`: El **Cono de Incertidumbre**, delimitado por un techo de riesgo ($P_{95}$) y un piso técnico ($P_{5}$).
  - `distribucion_dia_30.png`: Un histograma probabilístico detallando la frecuencia de escenarios cambiarios.

---

## 🧠 Explicabilidad Directiva (XAI)

Para vencer el problema de la "caja negra", el Motor Operativo de Simulación integra una disección financiera apoyada en los **Valores SHAP** (*Shapley Additive exPlanations*). La demostración y especificación matemática de esta capa de atribución causal se desglosa ampliamente en el manuscrito de investigación **"Inteligencia_Artificial_Explicable_para_la_Optimizacion_de_la_Gestion_de_Tesoreria_y_Riesgos_Financieros.pdf"**. 

Si el sistema emite una alerta de depreciación hacia 20.50 MXN/USD, la capa XAI intercepta la predicción y audita la causalidad: *e.g., 65% del movimiento se debe a un pico en el Índice de Incertidumbre T-MEC, 25% por diferencial de tasas Banxico-Fed, y un efecto mitigador del -10% derivado de un flujo resiliente de remesas.*

Esto provee una justificación fiduciaria directa ante los consejos de administración.

---

## 🤝 Contribución

Este proyecto fomenta la adopción de algoritmos avanzados en la planeación financiera corporativa, promoviendo la transición de sistemas estáticos a ecosistemas basados en inteligencia artificial explicable.

Para contribuir:
1. Haz un *Fork* del proyecto.
2. Crea una rama para tu característica (`git checkout -b feature/NuevaSimulacion`).
3. Haz un *Commit* de tus cambios (`git commit -m 'Añadir nueva variable de estrés'`).
4. Haz un *Push* a la rama (`git push origin feature/NuevaSimulacion`).
5. Abre un *Pull Request*.

---

## ⚖️ Licencia

Este proyecto se distribuye bajo un modelo de **Licenciamiento Dual**:

1. **Uso Académico y de Investigación**: [GNU Affero General Public License v3.0 (AGPLv3)](./LICENSE_AGPLv3).
2. **Uso Comercial / Corporativo**: Requiere una licencia comercial Enterprise autorizada por Saturn Investments. Para licenciamiento corporativo o soporte institucional, contactar a `contacto@saturninvestments.com.mx`.

---

## 📚 Referencias Destacadas

*Basado en el marco teórico y bibliográfico del proyecto de investigación subyacente:*
- **Aguayo, C., Gaucín Neria, N. D., & Morales Castro, A.** (2026). *"Inteligencia artificial explicable para la optimización de la gestión de tesorería y riesgos financieros"* (documento de investigación; *publicación pendiente*).
- Baker, S. R., Bloom, N., & Davis, S. J. (2016). *Measuring economic policy uncertainty*.
- Lundberg, S. M., & Lee, S.-I. (2017). *A unified approach to interpreting model predictions* (SHAP).
- Shapley, L. S. (1953). *A value for n-person games*.
- Sims, C. A. (1980). *Macroeconomics and reality*.