"""
riesgo-api-v0 — Servicio de puntuación de siniestros.
Aseguradora Santo Tomás · prototipo interno.
"""
import pickle
import time
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException 
from pydantic import BaseModel, Field

import config
from dominio import EvaluadorRiesgo, buscar_siniestro, cargar_siniestros

BASE = Path(__file__).parent

# ===== Carga del modelo UNA SOLA VEZ al arrancar =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta cuando el servidor arranca
    with open(BASE / config.RUTA_MODELO, "rb") as fh:
        app.state.modelo = pickle.load(fh)
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

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio."""
    return {"status": "ok", "version": app.version}

@app.post("/score")
async def score(data: ScoreRequest, request: Request):  # ← Cambio: payload: dict → data: ScoreRequest
    # El modelo ya está cargado en memoria, lo recuperamos de app.state
    modelo = request.app.state.modelo

    evaluador = EvaluadorRiesgo(data.poliza)
    puntaje = evaluador.puntuar(modelo, data.dict())  # ← Convertimos el modelo a dict
    evaluador.anotar(puntaje)

    return {
        "poliza": data.poliza,
        "puntaje": puntaje,
        "alto_riesgo": evaluador.es_alto_riesgo(puntaje),
    }


@app.get("/historial")
async def historial():
    return {"evaluaciones": EvaluadorRiesgo.historial}


@app.get("/siniestros/{id_siniestro}")
async def siniestro(id_siniestro: int):
    fila = buscar_siniestro(id_siniestro)
    if fila is None:
        raise HTTPException(status_code=404, detail=f"no existe el siniestro {id_siniestro}")
    return fila


@app.get("/exportar")
async def exportar():
    datos = cargar_siniestros()
    return datos

# --- Endpoints de perfil de carga -----------------------------------------

@app.get("/ping")
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
