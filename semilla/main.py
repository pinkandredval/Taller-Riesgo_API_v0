"""
riesgo-api-v0 — Servicio de puntuación de siniestros.
Aseguradora Santo Tomás · prototipo interno.
"""
import pickle
import time
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException 
from pydantic import BaseModel, Field, field_validator, ConfigDict

import config
from dominio import EvaluadorRiesgo, RepositorioSiniestros

BASE = Path(__file__).parent

# ===== Carga del modelo UNA SOLA VEZ al arrancar =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta cuando el servidor arranca
    with open(BASE / config.RUTA_MODELO, "rb") as fh:
        app.state.modelo = pickle.load(fh)
    app.state.repositorio = RepositorioSiniestros(BASE / config.RUTA_DATOS)
    app.state.historial = []
    print("Modelo cargado al inicio")
    yield
    # (Opcional) lo que quieras hacer al apagar
    print("Apagando servidor...")

app = FastAPI(title="Riesgo API", version="0.1.0", lifespan=lifespan)

# ===== MODELO DE VALIDACIÓN CON PYDANTIC =====
class ScoreRequest(BaseModel):
    poliza: str = Field(..., min_length=1, description="Número de póliza")
    monto: float = Field(..., gt=0, description="Monto del siniestro (>0)")
    antiguedad: int = Field(..., ge=0, description="Antigüedad en años (>=0)")
    siniestros_previos: int = Field(..., ge=0, description="Siniestros previos (>=0)")

    # --- NUEVO: VALIDADOR PARA NORMALIZAR LA PÓLIZA ---
    @field_validator('poliza')
    @classmethod
    def normalizar_poliza(cls, v: str) -> str:
        """Elimina espacios al inicio/final y convierte a mayúsculas."""
        return v.strip().upper()

# ===== MODELOS DE SALIDA (RESPUESTAS) =====
class EvaluacionItem(BaseModel):
    """Elemento individual del historial de evaluaciones."""
    poliza: str
    puntaje: float | None

class HistorialResponse(BaseModel):
    """Respuesta del endpoint /historial."""
    evaluaciones: list[EvaluacionItem]

class ScoreResponse(BaseModel):
    """Respuesta del endpoint /score."""
    poliza: str
    puntaje: float | None
    alto_riesgo: bool

class HealthResponse(BaseModel):
    """Respuesta del endpoint /health."""
    status: str
    version: str

class SiniestroResponse(BaseModel):
    """Respuesta del endpoint /siniestros/{id}."""
    id: str
    poliza: str
    monto: str
    fecha: str
    model_config = ConfigDict(extra='allow')  # Permite columnas extra del CSV

class PingResponse(BaseModel):
    """Respuesta del endpoint /ping."""
    pong: bool

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de verificación de salud del servicio."""
    return {"status": "ok", "version": app.version}

@app.post("/score", response_model=ScoreResponse)
async def score(data: ScoreRequest, request: Request):  # ← Cambio: payload: dict → data: ScoreRequest
    # El modelo ya está cargado en memoria, lo recuperamos de app.state
    modelo = request.app.state.modelo

    evaluador = EvaluadorRiesgo(data.poliza)
    puntaje = evaluador.puntuar(modelo,  data.model_dump())  # ← Convertimos el modelo a dict
    evaluador.anotar(puntaje)

    request.app.state.historial.append({
        "poliza": data.poliza,
        "puntaje": puntaje
    })
    return {
        "poliza": data.poliza,
        "puntaje": puntaje,
        "alto_riesgo": evaluador.es_alto_riesgo(puntaje),
    }


@app.get("/historial", response_model=HistorialResponse)
async def historial(request: Request):
    return {"evaluaciones":  request.app.state.historial}


@app.get("/siniestros/{id_siniestro}", response_model=SiniestroResponse)
async def siniestro(id_siniestro: int, request: Request):
    fila = request.app.state.repositorio.buscar_por_id(id_siniestro)
    if fila is None:
        raise HTTPException(status_code=404, detail=f"no existe el siniestro {id_siniestro}")
    return fila


@app.get("/exportar", response_model=list[SiniestroResponse])
async def exportar(request: Request):
    datos = request.app.state.repositorio.cargar_todos()
    return datos

# --- Endpoints de perfil de carga -----------------------------------------

@app.get("/ping", response_model=PingResponse)
async def ping():
    return {"pong": True}


@app.get("/consulta-archivo")
async def consulta_archivo():
    contenido = (BASE / config.RUTA_DATOS).read_text(encoding="utf-8")
    return {"lineas": len(contenido.splitlines())}


@app.get("/servicio-externo")
async def servicio_externo():
    time.sleep(0.3)
    return {"tarifa_referencia": 1.18}


@app.get("/calculo-pesado")
async def calculo_pesado():
    total = 0.0
    for i in range(3_000_000):
        total += (i % 7) ** 0.5
    return {"total": round(total, 2)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
