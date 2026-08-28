# Hallazgos — Parte A

**Grupo:** <número> · **Integrantes:** Kevin Leonardo Chaparro Reyes, Valentina Muñoz Palma, Paula Margarita Triana Ancinez

> No borren la fila de ejemplo hasta haber comprobado que su tabla se parsea.
> El formato es rígido: siete columnas, en este orden. Una tabla torcida se
> rechaza indicando la línea, no se «entiende igual».
>
> **Tuberías dentro de una celda:** si su comando lleva `|` —y varios lo llevarán,
> por `grep`, `head` o `jq`— escríbanlo `\|`. Sin escapar, Markdown lo lee como
> separador de columna y su fila pasa a tener ocho.

| ID | Síntoma observable | Causa | Módulo · Sección | SHA donde se observa | Comando de evidencia | Salida obtenida | Corrección aplicada |
|----|--------------------|-------|------------------|----------------------|----------------------|-----------------|---------------------|
| H0 | *(ejemplo de FORMATO, no un defecto de este repositorio)* `GET /ping` responde sin cabecera `Cache-Control` | El handler no declara política de caché | M2 · 2. El protocolo HTTP y la autenticación | `v0-semilla` | `curl -sI localhost:8000/ping \| grep -ci cache-control` | `0` | Se añade la cabecera en la respuesta |
| H1 |`GET /health` devuelve el error "detail":"Not Found"  | El endpoint `/health` no está definido en el código| |main.py | `curl http://localhost:8000/health`|`curl : {"detail":"Not Found"} ` <br><br> ` En línea: 1 Carácter: 1 ` <br><br> ` + curl http://localhost:8000/health ` <br><br> ` + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ` <br><br> ` + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:HttpWebRequest)[Invoke-WebRequest], WebException ` <br><br> ` + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShell.Commands.InvokeWebRequestCommand ` | agregar el siguiente codigo a main.py <br><br> `@app.get("/health")` <br><br> ` async def health_check(): ` <br><br> ` """Endpoint de verificación de salud del servicio.""" ` <br><br> `return {"status": "ok", "version": app.version}`|
<<<<<<< HEAD
| H2 |` POST /score` finciona pero "puntaje":null | | | | ` $body = @{poliza="POL-2026-0413"; monto=15000; antiguedad=3} \| ConvertTo-Json ` <br><br> ` Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json" `| ` StatusCode        : 200 ` <br><br> ` StatusDescription : OK ` <br><br> ` Content           : {"poliza":"POL-2026-0413","puntaje":null,"alto_riesgo":false} ` <br><br> ` RawContent        : HTTP/1.1 200 OK` <br><br> ` Content-Length: 61 ` <br><br> ` Content-Type: application/json ` <br><br> ` Date: Mon, 24 Aug 2026 02:25:52 GMT ` <br><br> ` Server: uvicorn ` <br><br> ` {"poliza":"POL-2026-0413","puntaje":null,"alto_riesgo":false} ` <br><br> ` Forms             : ` <br><br> ` Headers           : {[Content-Length, 61], [Content-Type, application/json], [Date, Mon, 24 Aug 2026 02:25:52 GMT], [Server, uvicorn]} ` <br><br> ` Images            : {} ` <br><br> ` InputFields       : {} ` <br><br> ` Links             : {} ` <br><br> ` ParsedHtml        : ` <br><br> ` RawContentLength  : 61 `| |
| H3 |` /historial ` | | | |` Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/historial `| ` StatusCode        : 200 ` <br><br> ` StatusDescription : OK ` <br><br> ` Content           : {"evaluaciones":[{"poliza":"POL-2026-0413","puntaje":null}]} ` <br><br> ` RawContent        : HTTP/1.1 200 OK ` <br><br> ` Content-Length: 60 `<br><br> ` Content-Type: application/json ` <br><br> ` Date: Mon, 24 Aug 2026 00:09:18 GMT ` <br><br> ` Server: uvicorn ` <br><br> ` {"evaluaciones":[{"poliza":"POL-2026-0413","puntaje":null}]} ` <br><br> ` Forms             : ` <br><br> `Headers           : {[Content-Length, 60], [Content-Type, application/json], [Date, Mon, 24 Aug 2026 00:09:18 GMT], [Server, uvicorn]} ` <br><br> ` Images            : {} ` <br><br> ` InputFields       : {} ` <br><br> ` Links             : {} ` <br><br> ` ParsedHtml        : ` <br><br> ` RawContentLength  : 60 `| |
| H4 |` /siniestros/999 ` <br><br> ` Devuelve 200 con {"error":"no existe el siniestro 999"} en lugar de 404 ` | | | |` Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/siniestros/999` |` StatusCode        :200 ` <br><br> ` StatusDescription :OK             ` <br><br> ` Content           : {"error":"no existe el siniestro 999"} ` <br><br> ` RawContent        : HTTP/1.1 200 OK ` <br><br> ` Content-Length: 38 ` <br><br> ` Content-Type: application/json ` <br><br> ` Date: Mon, 24 Aug 2026 01:30:04 GMT ` <br><br> ` Server: uvicorn ` <br><br> ` {"error":"no existe el siniestro 999"} `<br><br>` Forms            : ` <br><br> ` Headers           : {[Content-Length, 38], [Content-Type, application/json], [Date, Mon, 24 Aug 2026 01:30:04 GMT], [Server, uvicorn]} ` <br><br> ` Images            : {} ` <br><br> ` InputFields       : {} ` <br><br> ` Links             : {} ` <br><br> ` ParsedHtml        : ` <br><br> ` RawContentLength  : 38 ` | |
| H5 |` /exportar ` <br><br> ` Devuelve datos con octet-stream en lugar de JSON ` | | | | ` Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/exportar`|` StatusCode        :200 ` <br><br> ` StatusDescription : OK ` <br><br> ` Content           : {128, 4, 149, 198...}   ` <br><br> ` RawContent        : HTTP/1.1 200 OK ` <br><br> ` Content-Length: 22481 ` <br><br>`Content-Type: application/octet-stream`<br><br>`Date: Mon, 24 Aug 2026 01:42:35 GMT`<br><br>`Server: uvicorn`<br><br>`?.??W......]?(}?(?.id??.1??.poliza??POL-2026-0001??.monto??.158...`<br><br>`Headers           : {[Content-Length, 22481], [Content-Type, application/octet-stream], [Date, Mon, 24 Aug 2026 01:42:35 GMT], [Server, uvicorn]}`<br><br>`RawContentLength  : 22481` | |
| H6 | `POST /score` con datos válidos devuelve `"puntaje": null` | El modelo no se carga correctamente y el método `puntuar()` falla; se carga dentro del handler |  | `main.py` y `dominio.py` | `$body = @{poliza="POL-2026-0413"; monto=15000; antiguedad=3} \| ConvertTo-Json; Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json"` | `StatusCode: 200`<br><br>`StatusDescription : OK`<br><br>`Content: {"poliza":"POL-2026-0413"`<br><br>`"puntaje":null`<br><br>`"alto_riesgo":false}`<br><br>` RawContent        : HTTP/1.1 200 OK `<br><br>` Content-Length: 61 `<br><br>` Content-Type: application/json `<br><br>` Date: Thu, 27 Aug 2026 14:41:28 GMT `<br><br>` Server: uvicorn `<br><br>` {"poliza":"POL-2026-0413","puntaje":null,"alto_riesgo":false}` | Se verificó en `dominio.py` que el método `puntuar()` requiere el campo `"siniestros_previos"`, el cual faltaba en el body. Se corrigió el envío: `$body = @{poliza="POL-2026-0413"; monto=15000; antiguedad=3; siniestros_previos=0} \| ConvertTo-Json`. Además, se movió la carga del modelo (`pickle.load`) al inicio de `main.py` con bloque `try/except`, siguiendo la buena práctica de cargarlo una sola vez al levantar el servicio. |
| H7 | | | | | | | |
| H8 | | | | | | | |
=======
| H2 | `POST /score` con datos válidos devuelve `"puntaje": null` | El modelo no se carga correctamente y el método `puntuar()` falla; se carga dentro del handler || `main.py y dominio.py` | `$body = @{poliza="POL-2026-0413"; monto=15000; antiguedad=3} \| ConvertTo-Json; Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json"` | 
 `StatusCode: 200,StatusDescription : OK,Content: {"poliza":"POL-2026-0413","puntaje":null,"alto_riesgo":false},RawContent        : HTTP/1.1 200 OK ,Content-Length: 61 ,Content-Type: application/json , Date: Thu, 27 Aug 2026 14:41:28 GMT , Server: uvicorn, {"poliza":"POL-2026-0413","puntaje":null,"alto_riesgo":false} `| Se verifico en domimio.py los campos que necesita el método puntuar () y por lo tanto faltaba el campo "siniestros_previos" y cuando probamos lo hicimos con ese campo: 
 $body = @{                                                               
>>     poliza="POL-2026-0413"                                                   
>>     monto=15000                                                              
>>     antiguedad=3                                                             
>>     siniestros_previos=0   # ← Este campo es obligatorio para el modelo
>> } | ConvertTo-Json
>> 
>> Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json"
>> ademas se cargo el modelo al inicio en main.py como es la buena práctica ya que estaba en el handler:
>> try:
    with open(BASE / config.RUTA_MODELO, "rb") as fh:
        modelo = pickle.load(fh)
    print(f"Modelo cargado correctamente desde {config.RUTA_MODELO}")
except Exception as e:
    print(f"ERROR: No se pudo cargar el modelo: {e}")
    modelo = None|
| H3 | `POST /score` con falta del campo `poliza` devuelve `200` con `{"error":"falta el campo poliza"}` | Validación manual con `if`; no usa Pydantic ni códigos HTTP de error | M2 · Los códigos de estado HTTP son correctos y el error viaja en el estado | `v0-semilla` | `$body = @{monto=15000; antiguedad=3} \| ConvertTo-Json; Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json"` | `StatusCode: 200, Content: {"error":"falta el campo poliza"}` | Reemplazar validación manual por Pydantic; devolver `422 Unprocessable Content` |
| H4 | `GET /historial` devuelve `"puntaje": null` en el historial | El historial almacena el mismo `puntaje: null`; usa atributo de clase mutable | M3 · Programación orientada a objetos y clases | `v0-semilla` | `Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/historial` | `StatusCode: 200, Content: {"evaluaciones":[{"poliza":"POL-2026-0413","puntaje":null}]}` | Corregir cálculo del puntaje y mover historial a instancia o repositorio |
| H5 | `GET /siniestros/999` devuelve `200` con `{"error":"no existe el siniestro 999"}` | No se usa `404 Not Found` para recursos no encontrados | M2 · Los códigos de estado HTTP son correctos y el error viaja en el estado | `v0-semilla` | `Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/siniestros/999` | `StatusCode: 200, Content: {"error":"no existe el siniestro 999"}` | Lanzar `HTTPException(status_code=404, detail="Siniestro no encontrado")` |
| H6 | `GET /exportar` devuelve `Content-Type: application/octet-stream` con datos binarios | Se usa `pickle.dumps()` en lugar de JSON | M2 · Nada se serializa con pickle hacia el cliente | `v0-semilla` | `Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/exportar` | `StatusCode: 200, Content-Type: application/octet-stream, Content: (bytes)` | Cambiar a `return datos` (FastAPI lo convierte a JSON) |
| H7 | `POST /score` con `monto` negativo devuelve `500 Internal Server Error` | `assert payload["monto"] > 0` falla y lanza `AssertionError` | M2 · Los códigos de estado HTTP son correctos | `v0-semilla` | `$body = @{poliza="POL-2026-0413"; monto=-15000; antiguedad=3} \| ConvertTo-Json; Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json"` | `StatusCode: 500, Content: {"detail":"Internal Server Error"}` | Reemplazar `assert` por Pydantic con `Field(gt=0)`; devolver `422` |
| H8 | `POST /score` con `monto` como texto devuelve `422` con error de parsing | FastAPI no puede convertir string a número; el error es genérico | M4 · ValidationError → 422 | `v0-semilla` | `$body = @{poliza="POL-2026-0413"; monto="no es un número"; antiguedad=3} \| ConvertTo-Json; Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json"` | `StatusCode: 422, Content: {"detail":"There was an error parsing the body"}` | Usar Pydantic para validar tipos; el mensaje será más específico |
>>>>>>> f2aeac4e11d42fb9775e56c6ec0391775c7d773e
| H9 | | | | | | | |



**Reglas que se verifican automáticamente:**

- `Módulo · Sección` debe citar una lección que exista en los módulos 1 a 5, con el
  título tal como aparece en el menú lateral del material.
- **`SHA donde se observa`** es el commit donde el defecto todavía está: normalmente
  `v0-semilla`, la etiqueta del repositorio tal como se lo entregamos. El calificador hace
  *checkout* de ese commit para reproducir la evidencia. Si lo dejan en el commit final —donde
  ya está corregido— el comando no reproducirá nada y la fila no cuenta.
- `Comando de evidencia` se ejecuta ahí. Escríbanlo contra `localhost:8000`; el calificador
  sustituye el puerto por el que use.
- `Salida obtenida` es literal, copiada de su terminal. **Se compara con lo que salga de
  verdad**, así que una salida inventada se detecta.
- Entre 6 y 12 hallazgos. Una fila que no corresponda a un defecto real resta la mitad de lo
  que suma una correcta: el máximo se alcanza con precisión, no con volumen.

---

# Parte C — Interpretación de las mediciones

> Un párrafo por endpoint. Expliquen **los tiempos que ustedes obtuvieron**, no la
> teoría general. Si un resultado los sorprendió, dígan­lo: eso se premia.

## `/ping`

## `/consulta-archivo`

## `/servicio-externo`

## `/calculo-pesado`
