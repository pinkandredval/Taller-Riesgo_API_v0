# Bitácora de uso de IA

**Grupo:** <número> · **Integrantes:** Kevin Leonardo Chaparro Reyes, Valentina Muñoz Palma, Paula Margarita Triana Ancinez
**Herramientas usadas:** Deepseek

> Las tres secciones son obligatorias. **`## Rechazado` es la que se califica.**
> Una bitácora que solo lista prompts aceptados vale la mitad.

## Prompts

| # | Parte | Quién | Prompt (resumido si es largo) |
|---|-------|-------|-------------------------------|
|  1 | A | Deepseek | ¿Cómo activo el entorno virtual si PowerShell bloquea la ejecución de scripts (`PSSecurityException`)? |
| 2 | A | Deepseek | ¿Qué comandos uso para probar los endpoints del servicio (`/health`, `/score`, `/historial`, `/siniestros/{id}`, `/exportar`, `/ping`, `/consulta-archivo`, `/servicio-externo`, `/calculo-pesado`) y documentar la evidencia en `HALLAZGOS.md`? |
|3 | A | Deepseek | ¿Cómo fijo las versiones de `requirements.txt` sin usar `pip freeze`, y cómo elimino la advertencia `InconsistentVersionWarning` de scikit-learn? |
| 4 | A | Deepseek | ¿Qué debe excluir el `.gitignore` para no subir `venv/`, `__pycache__/`, `datos/`, `.env`? |
| 5 | A | Deepseek | Casos límite (`siniestros/-1`, `siniestros/1.5`, `monto=""`, `poliza=null`): ¿cuáles son defectos reales (H9, H10) y cuáles ya funcionan bien? |
| 6 | B | Deepseek | ¿Cómo valido los campos de entrada de `/score` con Pydantic (`BaseModel`, `Field`) en lugar de `if`/`assert`?  |
| 7 | B | Deepseek | ¿Cómo evito que el modelo se cargue dentro del handler en cada petición?  |
| 8 | B | Deepseek | ¿Cómo manejo los secretos (`API_KEY`, `CLAVE_FIRMA`) sin dejarlos en el código fuente? |
|  9 | B | Deepseek | ¿Cómo corrijo que el decorador `con_registro` oculte la función original y devuelva `None` en errores inesperados? |
| 10 | B | Deepseek | ¿Cómo cambio el comando de arranque para cumplir B8 (sin `--reload`, con `--workers`)? |
| 11 | B | Deepseek | ¿Cómo soluciono el error `'State' object has no attribute 'modelo'` en `pytest` sin modificar `test_contrato.py`?|
|12 | B | Deepseek | ¿Cómo corrijo que el historial se comparta entre instancias de `EvaluadorRiesgo`? |
|  13 | B | Deepseek | ¿Hay código espagueti en `main.py`/`dominio.py` (sin contar la fusión de archivos, que se dejó para el final)? |
| 14 | C | Deepseek | Para el endpoint CPU-bound `/calculo-pesado`, ¿`def` simple o `async def` + `run_in_executor`? |
|  15 | D | Deepseek | Auditoría de `ia_propuesta.py`: identificar y confirmar (con `python -c`) los tres defectos de comportamiento.|
| 16 | D | Deepseek | ¿Es la regex de `correo_analista` (solo acepta TLD de 2-3 letras) un defecto a corregir en la Parte D?|


## Aceptado

| # | Qué propuso la IA | Por qué lo aceptamos | Qué cambiamos antes de usarlo |
|---|--------------------|-----------------------|-------------------------------|
| 2 | Añadir el endpoint `/health` en `main.py` con `@app.get("/health")`. | El taller exige explícitamente la existencia de este endpoint (restricción B7); se detectó al probar los endpoints y recibir 404. | Se añadió `"version": app.version` en la respuesta para dar más información. |
| 3 | Usar `pip-tools` con `requirements.in` y `pip-compile` para fijar versiones de dependencias. | Garantiza la reproducibilidad del entorno (B1) y evita errores por versiones no especificadas. | Se forzó `scikit-learn==1.7.2` en `requirements.in` para eliminar la advertencia de compatibilidad con el modelo. |
| 4 | Ampliar el `.gitignore` para excluir `venv/`, `__pycache__/`, `datos/`, `.env`, `.vscode/`, `.DS_Store`, etc. | Cumple con la restricción B1 (reproducibilidad y seguridad), evitando subir archivos innecesarios o sensibles. | Se agregaron reglas adicionales como `*.swp`, `*.swo`, `*.log` y `Thumbs.db`. |
| 5 | Usar `Field(ge=0)` y validadores de Pydantic para rechazar `antiguedad` negativa o faltante. | Corrige H9 y H10 de forma declarativa, sin `if` manuales. | Se documentaron solo los casos que eran defectos reales; otros casos límite probados ya devolvían 422 correctamente y no se tocaron. |
| 6 | Usar `Pydantic` con `BaseModel` y `Field` para validar los campos de entrada en `/score`. | Cumple con las restricciones B2 y B5, eliminando validaciones manuales con `if` y `assert`. | Se definió `ScoreRequest` con los campos poliza, monto, antiguedad, siniestros_previos, todos obligatorios y con restricciones de rango (`gt=0`, `ge=0`). |
| 7 | Usar `@asynccontextmanager` y `app.state.modelo` para cargar el modelo una sola vez al inicio. | Cumple con la restricción B6 y resuelve el error 500 que ocurría al cargar el modelo en cada petición; también corrigió una advertencia de que `@app.on_event("startup")` está en desuso en versiones recientes de FastAPI. | Se implementó el lifespan y se eliminó la carga dentro del handler `/score`. |
| 8 | Crear un archivo `.env` (ignorado por Git) y modificar `config.py` para leer `API_KEY` y `CLAVE_FIRMA` con `os.getenv()` y `load_dotenv()`. | Elimina la exposición de secretos en el código fuente, cumpliendo con B1. | Se mantuvo `UMBRAL_ALTO_RIESGO`, `RUTA_MODELO` y `RUTA_DATOS` en `config.py` por ser configuraciones no sensibles. |
| 9 | Modificar el decorador `con_registro` añadiendo `@functools.wraps(func)` y reemplazando `return None` por `raise`. | Cumple con la restricción B9 y elimina la causa raíz de `puntaje: null` en errores inesperados. | No hubo cambios; se aplicó tal cual. |
| 10 | Cambiar el comando de arranque en el `README` y el bloque `if __name__ == "__main__"` para cumplir con B8. | El taller exige que el arranque documentado sea de producción (sin `--reload` y con `--workers`). | Se añadió una nota en el README aclarando que `--reload` es solo para desarrollo. |
| 11 | Cargar el modelo, el repositorio y el historial directamente en `app.state` al final de `main.py` (verificando con `hasattr`) como respaldo cuando el `lifespan` no se ejecuta en `TestClient`. | Permite que los tests de contrato encuentren el modelo sin ejecutar el `lifespan` y sin tocar `test_contrato.py`. Sigue cumpliendo B6 porque la carga ocurre al iniciar la app, no en cada petición. | Se mantuvo el `lifespan` para producción y se agregó la carga directa solo como respaldo para pruebas; se documentó como hallazgo H16. |
| 12 | Mover `historial` de atributo de clase a atributo de instancia en `dominio.py`. | Cumple con la restricción B4 y resuelve el test `test_el_historial_no_se_comparte_entre_instancias`. | Se ajustó el endpoint `/historial` para devolver una lista vacía por defecto, ya que el historial ahora es por instancia. |
| 13 | Cachear el CSV en memoria: `RepositorioSiniestros` releía todo el archivo en cada `buscar_por_id()`, y el historial se guardaba duplicado (en `EvaluadorRiesgo.historial` y en `app.state.historial`). | Mejora el rendimiento (evita leer disco en cada búsqueda) y elimina una fuente de inconsistencia entre los dos historiales. | Se cargó el CSV una sola vez en `__init__` (`self.datos = self.cargar_todos()`) y `buscar_por_id` pasó a buscar en memoria. |
| 1 | Cambiar la política de ejecución de PowerShell con `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`. | Resuelve el error `PSSecurityException` al activar el entorno virtual. | No hubo cambios; se aplicó tal cual. |
| 15 | Identificación de los tres defectos en `ia_propuesta.py`: (1) `time.sleep()` bloqueante dentro de `async def _puntuar`, (2) el validador `redondear_monto` calcula `round(v, 2)` pero no lo retorna, y (3) `evaluar_lote` no maneja excepciones ni listas vacías en `asyncio.gather`. | Cada defecto se confirmó con una prueba puntual (`python -c ...`) antes de aceptarlo como tal. | Se generó `ia_propuesta_corregida.py` reemplazando `time.sleep` por `await asyncio.sleep`, agregando el `return` en el validador, y usando `asyncio.gather(..., return_exceptions=True)` con verificación de lista vacía. |


## Rechazado

| # | Qué propuso la IA | Por qué lo rechazamos | Qué hicimos en su lugar |
|---|-------------------|-----------------------|-------------------------|
| 2 | Usar `curl http://localhost:8000/...` para probar endpoints en PowerShell. | En PowerShell, `curl` es un alias de `Invoke-WebRequest` y genera advertencias/errores de parseo. | Se usó `Invoke-WebRequest -UseBasicParsing` para tener control sobre el parseo. |
| 3 | Usar `pip freeze > requirements.txt` como solución definitiva para fijar versiones. | Incluye dependencias transitivas no deseadas y no permite separar dependencias directas de transitivas. | Se usó `pip-tools` con `requirements.in` para un control más fino y mantenible.  |
| 3 | Editar directamente `requirements.txt` para cambiar la versión de scikit-learn. | Rompe la trazabilidad: `requirements.txt` es generado, no fuente de verdad. | Se modificó `requirements.in` y se recompiló con `pip-compile`. |
| 3 | Ignorar la advertencia `InconsistentVersionWarning` de scikit-learn. | Aunque no es un error crítico, fijar la versión exacta elimina la advertencia y mejora la reproducibilidad. | Se forzó `scikit-learn==1.7.2` en `requirements.in`.  |
| 11 | Modificar `test_contrato.py` para forzar la ejecución del `lifespan` durante los tests (y evitar así el parche de carga manual). | El taller prohíbe explícitamente modificar o borrar esos tests: se comprueba que el archivo llega intacto, así que alterarlo habría invalidado la entrega aunque el test "pasara". | Se dejó `test_contrato.py` intacto y se resolvió con la carga manual de `app.state` como respaldo |
| 14 | Usar `async def` con `run_in_executor` para el endpoint CPU-bound `/calculo-pesado`. | Al medir el rendimiento en la Parte C con concurrencia 1 y 20, `def` (dejando que los workers de Uvicorn manejen la concurrencia) dio mejor tiempo total que `async def` + executor; el executor añadía overhead sin beneficio real para una tarea puramente CPU-bound. | Se dejó el endpoint como `def` y se documentó la decisión con los tiempos medidos en `MEDICIONES.csv` y en la sección Parte C de `HALLAZGOS.md`. |
| 16 | Tratar la regex de `correo_analista` (solo acepta TLD de 2-3 letras, ej. rechaza `a@b.info`) como un defecto a corregir en la Parte D. | No es un error de comportamiento sino una restricción de diseño ya fijada en el contrato de `ia_propuesta.py`; la Parte D pide identificar exactamente los tres defectos de comportamiento reales, no ampliar la validación de correo. | Se dejó la regex tal cual venía y se documentaron únicamente los tres defectos de comportamiento confirmados con pruebas. |
