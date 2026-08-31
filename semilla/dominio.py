"""Lógica de dominio: evaluación de riesgo de pólizas."""
import csv
from pathlib import Path

import config
from utilidades import con_registro

BASE = Path(__file__).parent


class EvaluadorRiesgo:
    """Evalúa el riesgo de una póliza y guarda lo que ha evaluado."""
    umbral = config.UMBRAL_ALTO_RIESGO

    def __init__(self, poliza):
        self.poliza = poliza
        self.historial = []

    @con_registro
    def puntuar(self, modelo, payload):
        rasgos = [[
            payload["monto"],
            payload["antiguedad"],
            payload["siniestros_previos"],
        ]]
        return float(modelo.predict_proba(rasgos)[0][1])

    def anotar(self, puntaje):
        self.historial.append({"poliza": self.poliza, "puntaje": puntaje})

    def es_alto_riesgo(self, puntaje):
        return puntaje is not None and puntaje > self.umbral


###agregado para cumplir B4
class RepositorioSiniestros:
    """Repositorio para acceder a los datos de siniestros."""

    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv

    def cargar_todos(self):
        with open(self.ruta_csv, encoding="utf-8") as fh:
            return list(csv.DictReader(fh))

    def buscar_por_id(self, id_siniestro):
        for fila in self.cargar_todos():
            if fila["id"] == str(id_siniestro):
                return fila
        return None
