import asyncio
from typing import Optional, List, Union

from pydantic import BaseModel, Field, field_validator


class SolicitudPuntuacion(BaseModel):
    """Datos de entrada para puntuar una póliza."""

    poliza: str = Field(min_length=8, max_length=20)
    correo_analista: str = Field(
        pattern=r"^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,3}$"
    )
    monto: float = Field(gt=0)
    antiguedad: int = Field(ge=0, le=60)
    siniestros_previos: int = Field(ge=0)
    observaciones: Optional[str] = Field(default=None, max_length=200)

    @field_validator("monto")
    @classmethod
    def redondear_monto(cls, v: float) -> float:
        """Redondea el monto a dos decimales para evitar ruido de coma flotante."""
        return round(v, 2)  # ← CORRECCIÓN 2: devuelve el valor redondeado


class RespuestaPuntuacion(BaseModel):
    """Resultado de la evaluación."""

    poliza: str
    puntaje: float = Field(ge=0.0, le=1.0)
    alto_riesgo: bool


async def _puntuar(solicitud: SolicitudPuntuacion) -> float:
    """Consulta el servicio externo de scoring y devuelve la probabilidad."""
    await asyncio.sleep(0.2)  # ← CORRECCIÓN 1: asyncio.sleep en lugar de time.sleep
    base = 0.18 * solicitud.siniestros_previos - 0.01 * solicitud.antiguedad
    return max(0.0, min(1.0, 0.4 + base))


async def evaluar_lote(solicitudes: List[SolicitudPuntuacion]) -> List[Union[float, Exception]]:
    """
    Evalúa un lote de solicitudes de forma concurrente.
    Retorna una lista con los resultados o excepciones por cada solicitud.
    """
    # CORRECCIÓN 3: validación de entrada
    if not isinstance(solicitudes, list):
        raise TypeError("solicitudes debe ser una lista")
    if not solicitudes:
        return []

    # CORRECCIÓN 3: usar return_exceptions=True para manejar fallos individuales
    resultados = await asyncio.gather(
        *[_puntuar(s) for s in solicitudes],
        return_exceptions=True
    )
    return resultados
