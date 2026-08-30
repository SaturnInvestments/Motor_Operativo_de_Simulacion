# Saturn Network - Motor Operativo de Simulación Financiera

Saturn Network es un framework neuronal secuencial de análisis combinatorio y simulación de estrés macroeconómico cambiario (Stress Testing USD/MXN) diseñado para calibración y prospectiva financiera mediante simulaciones de Monte Carlo y Tensor Neuronal.

El proyecto cuenta con un esquema de licenciamiento dual (Académico AGPLv3 / Comercial Enterprise) y soporte para variables de entorno cifradas estilo Laravel.

---

## 📋 Características Principales

- **Cifrado de Entorno**: Cifrado AES-256 en memoria para proteger variables y claves de producción sin exponerlas en GitHub.
- **Validación Criptográfica de Licencias**: El motor requiere una validación matemática de clave comercial para modelos con licencia corporativa.
- **Inteligencia Visual Directiva**: Generación automática de gráficos *Fan Chart* (cono de incertidumbre de estrés cambiario) e histogramas con marcas de agua completamente configurables.
- **Historial de Simulaciones**: Salidas de simulación autogestionadas con marcas de tiempo cronológicas (`YYYYMMDD_HHMMSS`) para evitar sobreescrituras accidentales.

---

## 🛠️ Requisitos e Instalación

### 1. Clonar el repositorio y acceder a la carpeta
```bash
git clone <url-del-repositorio>
cd motor_operativo_de_simulacion/saturn-network
```

### 2. Crear y activar el entorno virtual (Python >= 3.8)
En Windows:
```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🔒 Gestión del Entorno Cifrado (.env.encrypted)

Para subir el proyecto a producción de manera segura sin exponer credenciales en GitHub, se utiliza un sistema de variables cifradas.

### Cifrar el archivo `.env`
Genera el archivo cifrado `.env.encrypted` y crea una clave local en `.env.key` (excluida de Git):
```bash
python -m saturn.security.env_crypt encrypt
```
> [!IMPORTANT]
> En tu servidor de producción, define la variable de entorno de sistema `SATURN_ENV_KEY` con el valor de la clave generada para que la aplicación descifre las variables directamente en memoria sin requerir el archivo `.env` físico.

### Descifrar `.env.encrypted` a `.env` (Desarrollo)
```bash
python -m saturn.security.env_crypt decrypt
```

---

## 🚀 Guía de Ejecución

El flujo operativo se divide en tres fases principales:

### Fase 1: Ingesta e Histórico de Datos
Los datos macroeconómicos del T-MEC deben encontrarse en el archivo `data/input/tmec_historico.csv` (se incluye una plantilla histórica).

### Fase 2: Calibración y Entrenamiento del Modelo
Ajusta los pesos sinápticos de la red secuencial utilizando datos históricos:
```bash
python scripts/1_train_model.py
```
*Este comando genera el archivo del modelo en `data/output/models/motor_tmec_v1.saturn` e inyecta la firma de licencia correspondiente.*

### Fase 3: Simulación de Estrés y Prospectiva (What-If)
Corre la simulación de escenarios de Monte Carlo basándose en variables macroeconómicas estresadas:
```bash
python scripts/2_run_simulation.py
```

#### Parámetros adicionales para Grid Search:
- `--spot <valor>`: Especifica un precio Spot USD/MXN personalizado para la simulación.
- `--banxico_min <val> --banxico_max <val>`: Tasa de interés de Banxico estresada.
- `--fed_min <val> --fed_max <val>`: Tasa de la Reserva Federal.
- `--vix_min <val> --vix_max <val>`: Niveles del índice VIX de volatilidad.

Ejemplo:
```bash
python scripts/2_run_simulation.py --spot 19.50 --banxico_min 10.0 --banxico_max 11.5
```

---

## 🔑 Generación de Licencias Comerciales (Enterprise)

Para autorizar la carga de modelos corporativos de clientes, puedes generar llaves de validación criptográfica desde la CLI usando la sal interna:
```bash
python -m saturn.security.license_check generate "Nombre del Cliente Completo"
```
Inyecta la clave generada en la variable `LICENSE_KEY` del entorno (dentro de tu `.env` o descifrado en producción).

---

## ⚖️ Licencia

Este proyecto está bajo la Licencia **GNU Affero General Public License v3.0 (AGPLv3)** para fines educativos y de investigación académica. El uso comercial o corporativo requiere de una licencia Enterprise provista por Saturn Investments.
