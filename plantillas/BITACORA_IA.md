# Bitácora de uso de IA

**Grupo:** <número> · **Integrantes:** Kevin Leonardo Chaparro Reyes, Valentina Muñoz Palma, Paula Margarita Triana Ancinez
**Herramientas usadas:** Deepseek

> Las tres secciones son obligatorias. **`## Rechazado` es la que se califica.**
> Una bitácora que solo lista prompts aceptados vale la mitad.

## Prompts

| # | Parte | Quién | Prompt (resumido si es largo) |
|---|-------|-------|-------------------------------|
| 1 | A | Deepseek | Configuración inicial del entorno: clonar repositorio, abrir VS Code con la carpeta `taller_corte1` como raíz, y activar entorno virtual. |
| 2 | A | Deepseek | Prueba de `endpoints`: comandos para probar `/health`, `/score`, `/historial`, `/siniestros/{id}`, `/exportar`, `/ping`, `/consulta-archivo`, `/servicio-externo`, `/calculo-pesado`. |
| 3 | A | Deepseek | Documentación de hallazgos: solicitud de ayuda para llenar la tabla de `HALLAZGOS.md` con el formato exacto del taller. |
| 4 | A | Deepseek | Corrección de defectos: cómo implementar `Pydantic`, cargar el modelo al inicio, manejar secretos con `.env`, y corregir `.gitignore`. |
| 5 | A | Deepseek | Gestión de dependencias: cómo fijar versiones en `requirements.txt` sin `pip freeze`, y cómo forzar `scikit-learn==1.7.2`. |
| 6 | A | Deepseek | Revisión de archivos adicionales: `config.py`, `utilidades.py`, `dominio.py`, `README.md` para identificar nuevos hallazgos. |
| 7 | A | Deepseek | Solicitud de comandos de evidencia para los hallazgos documentados (H1 a H10). |
| 8 | B | Deepseek | Corrección de restricciones B1-B9: cómo cumplir con cada una, incluyendo B8 (arranque de producción) y B9 (decoradores). |
| 9 | C | Deepseek | Clasificación de `endpoints` para la Parte C y ejecución de `medir.py`. |
| 10 | D | Deepseek | Auditoría de `ia_propuesta.py`: identificación de los tres defectos y correcciones. |
| 11 | D | Deepseek | Pruebas de `ia_propuesta.py`: comandos para probar cada defecto y evidencia de salidas. |
| 12 | B | Deepseek | Solución del error `State' object has no attribute 'modelo'` en pruebas con `pytest`. |
| 13 | B | Deepseek | Corrección del historial compartido entre instancias (atributo de clase vs instancia). |
| 14 | B | Deepseek | Uso de `pip-tools` con `requirements.in` para fijar versiones de dependencias. |
| 15 | B | Deepseek | Configuración de `.env` y modificación de `config.py` para leer variables de entorno. |
| 16 | B | Deepseek | Modificación del decorador `con_registro` en `utilidades.py` con `@functools.wraps` y `raise`. |
| 17 | B | Deepseek | Cambio del comando de arranque en `README` y bloque `if __name__ == "__main__"` para cumplir B8. |
| 18 | A | Deepseek | Resolución del error de política de ejecución en `PowerShell (PSSecurityException)`. |
| 19 | A | Deepseek | Prueba de casos límite: `siniestros/-1, siniestros/1.5, monto="", poliza=null`. |
| 20 | A | Deepseek | Corrección de los hallazgos H9 y H10 (antiguedad faltante y negativa) con `Pydantic`. |

## Aceptado

| # | Qué propuso la IA | Por qué lo aceptamos | Qué cambiamos antes de usarlo |
|---|-------------------|----------------------|-------------------------------|
| 1 | Añadir el endpoint `/health` en `main.py` con `@app.get("/health")`. | El taller exige explícitamente la existencia de este endpoint (restricción B7). | Se añadió `"version": app.version` en la respuesta para dar más información. |
| 2 | Usar `Pydantic` con `BaseModel` y `Field` para validar los campos de entrada en `/score`. | Cumple con las restricciones B2 y B5, eliminando validaciones manuales con `if` y `assert`. | Se definió `ScoreRequest` con los campos poliza, monto, antiguedad, siniestros_previos, todos obligatorios y con restricciones de rango `(gt=0, ge=0)`. |
| 3 | Usar `@asynccontextmanager` y `app.state.modelo` para cargar el modelo una sola vez al inicio. | Cumple con la restricción B6 y resuelve el error 500 que ocurría al cargar el modelo en cada petición. | Se implementó el lifespan y se eliminó la carga dentro del `handler /score`. |
| 4 | Ampliar el `.gitignore` para excluir `venv/`, `__pycache__/`, `datos/`, `.env`, `.vscode/`, `.DS_Store`, etc. | Cumple con la restricción B1 (reproducibilidad y seguridad), evitando subir archivos innecesarios o sensibles. | Se agregaron reglas adicionales como `*.swp`, `*.swo`, `*.log` y `Thumbs.db`. |
| 5 | Crear un archivo `.env` (ignorado por Git) y modificar `config.py` para leer `API_KEY` y `CLAVE_FIRMA` con `os.getenv()` y `load_dotenv()`. | Elimina la exposición de secretos en el código fuente, cumpliendo con B1. | Se mantuvo `UMBRAL_ALTO_RIESGO`, `RUTA_MODELO` y `RUTA_DATOS` en `config.py` por ser configuraciones no sensibles. |
| 6 | Usar `pip-tools` con `requirements.in` y `pip-compile` para fijar versiones de dependencias. | Garantiza la reproducibilidad del entorno (B1) y evita errores por versiones no especificadas. | Se forzó `scikit-learn==1.7.2` en `requirements.in` para eliminar la advertencia de compatibilidad con el modelo. |
| 7 | Modificar el decorador `con_registro` en `utilidades.py` añadiendo `@functools.wraps(func)` y reemplazando `return None` por `raise`. | Cumple con la restricción B9 y elimina la causa raíz de puntaje: null en errores inesperados. | No hubo cambios; se aplicó tal cual. |
| 8 | Cambiar el comando de arranque en `README` y el bloque `if __name__ == "__main__"` para cumplir con B8. | El taller exige que el arranque documentado sea de producción (sin `--reload` y con `--workers`). | Se añadió una nota en el `README` aclarando que `--reload` es solo para desarrollo. |
| 9 | Solución para el error `State' object has no attribute 'modelo'` en `pytest`: cargar el modelo directamente en `app.state` fuera del `lifespan`. | Permite que los tests de contrato encuentren el modelo sin ejecutar el `lifespan`. | Se mantuvo el `lifespan` para producción y se agregó la carga directa para pruebas. |
| 10 | Corrección del historial compartido: mover `historial` de atributo de clase a atributo de instancia en `dominio.py`. | Cumple con la restricción B4 y resuelve el test `test_el_historial_no_se_comparte_entre_instancias`. | Se modificó el `endpoint /historial` para devolver una lista vacía, ya que el historial ahora es por instancia. |
| 11 | Identificación de los tres defectos en `ia_propuesta.py` y propuesta de correcciones. | Permite completar la Parte D del taller con evidencia sólida. | Se documentaron los defectos en `DICTAMEN_IA.md` y se generó `ia_propuesta_corregida.py`. |
| 12 | Cambiar la política de ejecución de PowerShell con `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`. | Resuelve el error `PSSecurityException` al activar el entorno virtual. | No hubo cambios; se aplicó tal cual. |
| 13 | Prueba de casos límite: `siniestros/-1, siniestros/1.5, monto="", poliza=null`. | Permitió identificar que algunos casos ya devuelven 422 correctamente y no son defectos. | Se documentaron solo los que eran defectos reales (H9 y H10). |

## Rechazado

| # | Qué propuso la IA | Por qué lo rechazamos | Qué hicimos en su lugar |
|---|-------------------|-----------------------|-------------------------|
| 1 | Usar `curl http://localhost:8000/health` para probar endpoints en PowerShell. | En PowerShell, `curl` es un alias de `Invoke-WebRequest` y genera advertencias de seguridad. | Se usó `Invoke-WebRequest -UseBasicParsing` para tener control sobre el parseo. |
| 2 | Usar `pip freeze > requirements.txt` como solución definitiva para fijar versiones. | Incluye dependencias transitivas no deseadas y no permite separar dependencias directas de transitivas. | Se usó `pip-tools` con `requirements.in` para un control más fino y mantenible. |
| 3 | Editar directamente `requirements.txt` para cambiar la versión de `scikit-learn`. | Se prefería mantener la trazabilidad del cambio. | Se modificó `requirements.in` y se recompiló con `pip-compile`. |
| 4 | 	Ignorar la advertencia `InconsistentVersionWarning` de `scikit-learn`. | Aunque no es un error crítico, fijar la versión exacta elimina la advertencia y mejora la reproducibilidad. | Se forzó `scikit-learn==1.7.2` en `requirements.in`. |
| 5 | | | |
| 6 | | | |
| 7 | | | |
