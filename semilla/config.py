import os
from dotenv import load_dotenv

# Carga las variables del archivo .env (ubicado en la misma carpeta)
load_dotenv()

# Lee del entorno, y si no existe, usa un valor por defecto 
API_KEY = os.getenv("API_KEY")
CLAVE_FIRMA = os.getenv("CLAVE_FIRMA")

UMBRAL_ALTO_RIESGO = 0.7
RUTA_MODELO = "modelo.pkl"
RUTA_DATOS = "datos/siniestros.csv"

