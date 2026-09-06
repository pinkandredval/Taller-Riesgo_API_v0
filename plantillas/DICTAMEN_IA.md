# Dictamen sobre `ia_propuesta.py` — Parte D

**Grupo:** <número> · **Integrantes:** Kevin Leonardo Chaparro Reyes, Valentina Muñoz Palma, Paula Margarita Triana Ancinez

> Tres defectos. Las cuatro secciones de cada uno son obligatorias y se parsean.
> El peso está en **«Cómo lo comprobamos»**: afirmar que algo está mal no vale;
> demostrarlo, sí.

## Defecto 1

- **Qué está mal:** La función `_puntuar` está declarada como `async def`, pero usa `time.sleep(0.2)` para simular una demora de 0.2 segundos. Pero como está dentro de una función `async`, eso bloquea todo el proceso: mientras una solicitud espera, las demás no pueden avanzar.
- **Por qué es un defecto** (módulo · sección):Se supone que el sistema debe poder atender varias solicitudes al mismo tiempo (concurrencia). Pero con `time.sleep`, en la práctica se atienden una tras otra. Por ejemplo, si hay 5 solicitudes, el tiempo total es 5 × 0.2 = 1 segundo, en lugar de 0.2 segundos si se hicieran en paralelo. Esto se estudia en el módulo **M5 · Síncrono frente a asíncrono**.
- **Cómo lo comprobamos:** Hicimos una prueba con 5 solicitudes y tardó ~1.0 segundo. Eso confirma que se están ejecutando en serie.

```python
import asyncio, time; from ia_propuesta import evaluar_lote, SolicitudPuntuacion; s = [SolicitudPuntuacion(poliza=f'POL-2026-{i:02d}', correo_analista=f'{i}@b.com', monto=1000, antiguedad=5, siniestros_previos=1) for i in range(5)]; inicio = time.time(); asyncio.run(evaluar_lote(s)); fin = time.time(); print(f'{fin - inicio:.3f}s')
```

```
Tiempo 5 solicitudes: 1.009s
```

- **Corrección:** Cambiar `time.sleep(0.2)` por `await asyncio.sleep(0.2)` para que el sistema pueda atender otras tareas mientras espera.

## Defecto 2

- **Qué está mal:** En el modelo `SolicitudPuntuacion`, hay un validador que debería redondear el campo monto a dos decimales. Pero la función solo llama a `round()` y no devuelve el resultado. Como no devuelve nada, `Pydantic` guarda el campo como `None`.
- **Por qué es un defecto** (módulo · sección):El campo monto queda vacío (`None`) en lugar de tener el número redondeado. Esto puede generar errores más adelante porque el sistema espera un número válido. Además, no se cumple con el propósito del validador, que es limpiar los datos de entrada. Esto se relaciona con lo visto en **M4 · Validadores de campo**.
- **Cómo lo comprobamos:** Probamos a crear una solicitud con `monto=1000.123456789` y al imprimir el campo monto nos dio `None` en lugar de `1000.12`.

```python
from ia_propuesta import SolicitudPuntuacion; s = SolicitudPuntuacion(poliza='POL-2026-01', correo_analista='a@b.com', monto=1000.123456789, antiguedad=5, siniestros_previos=1); print(s.monto)
```

```
None
```

- **Corrección:** Agregar `return round(v, 2)` para que el validador devuelva el valor redondeado.

## Defecto 3

- **Qué está mal:** La función `evaluar_lote` no valida que `solicitudes` sea una lista no vacía de objetos `SolicitudPuntuacion`. Si una solicitud es inválida, toda la ejecución falla. Tampoco maneja errores de `_puntuar` de forma granular.
- **Por qué es un defecto** (módulo · sección):En un servicio de producción, una solicitud inválida no debe detener el procesamiento de todo el lote. Debe reportar los errores individuales y continuar con las demás. Esto contradice las buenas prácticas de robustez vistas en **M4 · Validación de DataFrames** y **M2 · Manejo de errores**.
- **Cómo lo comprobamos:** <br><br> - Al pasar una lista con una solicitud inválida (antiguedad negativa), se lanza `ValidationError` y no se procesa ninguna. <br><br> - Al pasar un string en lugar de un objeto, se lanza `AttributeError`. <br><br> - Al pasar `None`, se lanza `TypeError: 'NoneType' is not iterable`.

```python
## Prueba con solicitud inválida (antiguedad negativa) en el lote:
"import asyncio; from ia_propuesta import evaluar_lote, SolicitudPuntuacion; s1 = SolicitudPuntuacion(poliza='POL-2026-01', correo_analista='a@b.com', monto=1000, antiguedad=5, siniestros_previos=1); s2 = SolicitudPuntuacion(poliza='POL-2026-02', correo_analista='b@c.com', monto=2000, antiguedad=-3, siniestros_previos=0); asyncio.run(evaluar_lote([s1, s2]))"

## Prueba de pasar un string en lugar de una lista de objetos
"import asyncio; from ia_propuesta import evaluar_lote; asyncio.run(evaluar_lote(['no es un objeto']))"

## Prueba de pasar None en lugar de una lista
"import asyncio; from ia_propuesta import evaluar_lote; asyncio.run(evaluar_lote(None))"

```

```
## Salida de prueba con solicitud inválida (antiguedad negativa) en el lote:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\ACER\OneDrive\Documentos\universidad-programación\solución taller apis\Taller-Riesgo_API_v0\semilla\venv\Lib\site-packages\pydantic\main.py", line 263, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core._pydantic_core.ValidationError: 1 validation error for SolicitudPuntuacion
antiguedad
  Input should be greater than or equal to 0 [type=greater_than_equal, input_value=-3, input_type=int]
    For further information visit https://errors.pydantic.dev/2.13/v/greater_than_equal

## Salida de prueba de pasar un string en lugar de una lista de objetos
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\ACER\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\ACER\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ACER\AppData\Local\Programs\Python\Python311\Lib\asyncio\base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\ACER\OneDrive\Documentos\universidad-programación\solución taller apis\Taller-Riesgo_API_v0\semilla\ia_propuesta.py", line 54, in evaluar_lote
    return await asyncio.gather(*[_puntuar(s) for s in solicitudes])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ACER\OneDrive\Documentos\universidad-programación\solución taller apis\Taller-Riesgo_API_v0\semilla\ia_propuesta.py", line 48, in _puntuar
    base = 0.18 * solicitud.siniestros_previos - 0.01 * solicitud.antiguedad
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'siniestros_previos'

## Salida de pasar None en lugar de una lista
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\ACER\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\ACER\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ACER\AppData\Local\Programs\Python\Python311\Lib\asyncio\base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\ACER\OneDrive\Documentos\universidad-programación\solución taller apis\Taller-Riesgo_API_v0\semilla\ia_propuesta.py", line 54, in evaluar_lote
    return await asyncio.gather(*[_puntuar(s) for s in solicitudes])
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not iterable

```

- **Corrección:** Se modificó la función `evaluar_lote` en el archivo `ia_propuesta_corregida.py` para solucionar los problemas de validación y manejo de errores. Los cambios fueron los siguientes:

1. Validación del tipo de entrada:
Se agregó una verificación al inicio de la función para asegurar que solicitudes sea una lista. Si no lo es, se lanza un `TypeError` con un mensaje claro. Esto evita que el programa falle con errores como `AttributeError` o `TypeError` cuando se pasan datos incorrectos (como un `string` o `None`).

```python
if not isinstance(solicitudes, list):
    raise TypeError("solicitudes debe ser una lista")
```

2. Manejo de lista vacía:
Se agregó una verificación para que, si la lista está vacía, la función devuelva `[]` directamente, sin intentar ejecutar `asyncio.gather` sobre una lista vacía, lo que podría generar comportamientos inesperados.

```python
if not solicitudes:
    return []
```

3. Manejo de errores individuales con `return_exceptions=True`:
Se modificó la llamada a `asyncio.gather` para incluir el parámetro `return_exceptions=True`. Esto permite que, si una solicitud específica falla (por ejemplo, por un error de validación como antiguedad negativa), se capture la excepción y se devuelva como parte de los resultados, en lugar de detener todo el procesamiento del lote.

