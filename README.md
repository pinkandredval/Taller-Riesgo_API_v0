# Riesgo API v0 — Solución Taller Corte I

**Python para Desarrollo de APIs e IA · USTA · Estadística · 2026-II**

**Grupo:** <número>  
**Integrantes:** Kevin Leonardo Chaparro Reyes, Valentina Muñoz Palma, Paula Margarita Triana Ancinez

---

## Descripción

Este repositorio contiene la solución al **Taller del Corte I – "Riesgo API v0"**.

Partiendo de un servicio web deliberadamente mal construido, se realizaron las siguientes actividades:

- Diagnóstico de defectos del servicio (**Parte A**).
- Refactorización del código cumpliendo restricciones de entorno, HTTP, POO, validación con Pydantic, carga del modelo y arranque en producción (**Parte B**).
- Medición y decisión de la declaración síncrona/asíncrona de los endpoints según su perfil de carga (**Parte C**).
- Auditoría y corrección de una propuesta generada por IA (**Parte D**).
- Documentación del uso de IA mediante una bitácora (**Parte E**).

El resultado es un servicio REST funcional, reproducible y listo para producción, que expone un modelo de puntuación de siniestros.

---

## Integrantes

- Kevin Leonardo Chaparro Reyes
- Valentina Muñoz Palma
- Paula Margarita Triana Ancinez

---

## Requisitos

Todas las dependencias están fijadas en `requirements.txt` (generado con **pip-tools**).

---

# Instalación y ejecución paso a paso

Sigue estos comandos en tu terminal. Todos los archivos del proyecto están dentro de la carpeta `semilla/`, así que asegúrate de entrar allí después de clonar.

```bash
# 1. Clonar el repositorio (reemplaza la URL por la de tu grupo)
git clone <url-del-repositorio>
cd <repositorio>

# 2. Entrar a la carpeta donde está el código fuente
cd semilla
```

---

# Archivo .env (variables de entorno)

Este repositorio no incluye el archivo `.env` por seguridad (está en `.gitignore`).

Debes crearlo manualmente dentro de la carpeta `semilla/` (donde se encuentran `main.py` y `config.py`).

## Crear el archivo `.env`

1. Ve a la carpeta `semilla/`.
2. Crea un archivo llamado exactamente:

```text
.env
```

3. Copia y pega el contenido correspondiente a las variables de entorno definidas para el proyecto.
```bash
API_KEY=sk-riesgo-2026-9f3a1c7b4e21
CLAVE_FIRMA=aseguradora-santo-tomas-2026
```
> **Importante:** El archivo debe quedar ubicado en `semilla/.env`.

El módulo `config.py` utilizará `load_dotenv()` para cargar estas variables automáticamente cuando el servicio se inicie.

---


```bash

# 3. Crear y activar un entorno virtual
python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\activate

# En macOS / Linux:
source venv/bin/activate

# 4. Instalar las dependencias exactas
pip install -r requirements.txt

# 5. (Opcional) Verificar que los tests de contrato pasan
pytest tests/test_contrato.py -v

# 6. Arrancar el servicio en modo producción (sin --reload, con 4 workers)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

El servicio quedará escuchando en:

```text
http://localhost:8000
```

---

# Uso básico (ejemplos con curl)

Puedes probar los endpoints directamente desde la terminal o con herramientas como **Postman**.

## 1. Verificar salud del servicio

```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**

```json
{"status":"ok","version":"0.1.0"}
```

---

## 2. Solicitar una puntuación (caso válido)

```bash
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"poliza":"POL-2026-0413","monto":15000,"antiguedad":3,"siniestros_previos":0}'
```

**Respuesta (ejemplo):**

```json
{"poliza":"POL-2026-0413","puntaje":0.45,"alto_riesgo":false}
```

---

## 3. Solicitar con datos inválidos (debe devolver 422)

```bash
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"poliza":"","monto":-100,"antiguedad":-1,"siniestros_previos":0}'
```

**Respuesta esperada:** `422 Unprocessable Content` con detalles de validación.

---

## 4. Consultar historial de evaluaciones

```bash
curl http://localhost:8000/historial
```

---

## 5. Obtener un siniestro por ID (existente o no)

```bash
curl http://localhost:8000/siniestros/1
# existe → 200

curl http://localhost:8000/siniestros/999
# no existe → 404
```

---

## 6. Exportar todos los siniestros (JSON)

```bash
curl http://localhost:8000/exportar
```

---

## 7. Endpoints de perfil de carga (Parte C)

```bash
curl http://localhost:8000/ping
curl http://localhost:8000/consulta-archivo
curl http://localhost:8000/servicio-externo
curl http://localhost:8000/calculo-pesado
```

---

# Endpoints disponibles

| Método | Ruta | Descripción |
|----------|----------|----------|
| GET | `/health` | Verificación de salud |
| POST | `/score` | Calcula puntuación de riesgo (validación con Pydantic) |
| GET | `/historial` | Devuelve el historial de evaluaciones |
| GET | `/siniestros/{id}` | Obtiene un siniestro por ID (404 si no existe) |
| GET | `/exportar` | Exporta todos los siniestros en JSON |
| GET | `/ping` | Respuesta trivial (para mediciones) |
| GET | `/consulta-archivo` | Lee un archivo del disco (I/O) |
| GET | `/servicio-externo` | Simula una llamada externa (I/O) |
| GET | `/calculo-pesado` | Cálculo intensivo en CPU |

---

# Pruebas

El repositorio incluye una batería de pruebas de contrato en:

```text
tests/test_contrato.py
```

Para ejecutarlas (con el entorno virtual activado):

```bash
pytest tests/test_contrato.py -v
```

Todas deben pasar. No se ha modificado el archivo original para cumplir con la restricción del taller.

---

# Estructura de archivos (relevantes)

```text
taller_corte1/
├── plantillas/                      # Entregables de las partes A, C, D y E
│   ├── HALLAZGOS.md                 # Diagnóstico (Parte A) + interpretación (Parte C)
│   ├── DICTAMEN_IA.md               # Auditoría de ia_propuesta.py (Parte D)
│   ├── BITACORA_IA.md               # Bitácora de uso de IA (Parte E)
│   └── MEDICIONES.csv               # Resultados de las mediciones (Parte C)
│
└── semilla/                         # Código fuente del servicio
    ├── main.py                      # Punto de entrada, endpoints, lifespan
    ├── dominio.py                   # Lógica de negocio
    ├── utilidades.py                # Decorador con_registro (corregido)
    ├── config.py                    # Configuración (carga .env)
    ├── .env                         # Variables de entorno (NO versionado)
    ├── requirements.txt             # Dependencias fijadas
    ├── requirements.in              # Dependencias directas
    ├── .gitignore                   # Ignora venv, pycache, .env, etc.
    ├── modelo.pkl                   # Modelo serializado
    ├── datos/siniestros.csv         # Datos de siniestros
    ├── tests/test_contrato.py       # Pruebas de contrato
    ├── medir.py                     # Script para la Parte C
    ├── ia_propuesta.py              # Código original generado por IA
    ├── ia_propuesta_corregida.py    # Versión corregida (Parte D)
    └── README.md                    # Este archivo
```

---

# Notas sobre el entorno de producción

- El servicio se lanza con Uvicorn usando `--workers 4`.
- No se usa `--reload` en producción.
- El modelo se carga una sola vez al iniciar el servicio gracias al mecanismo de **lifespan**.
- Los secretos (`API_KEY`, `CLAVE_FIRMA`) se leen desde un archivo `.env` no versionado.
- Las respuestas de error utilizan códigos HTTP apropiados:
  - `200 OK`
  - `404 Not Found`
  - `422 Unprocessable Content`
  - `500 Internal Server Error`

---

## Última actualización

**Septiembre de 2026**
