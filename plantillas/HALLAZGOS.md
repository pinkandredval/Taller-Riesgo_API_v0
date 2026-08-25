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
| H2 |` POST /score` finciona pero "puntaje":null | | | | ` $body = @{poliza="POL-2026-0413"; monto=15000; antiguedad=3} \| ConvertTo-Json ` <br><br> ` Invoke-WebRequest -UseBasicParsing -Method POST -Uri http://localhost:8000/score -Body $body -ContentType "application/json" `| ` StatusCode        : 200 ` <br><br> ` StatusDescription : OK ` <br><br> ` Content           : {"poliza":"POL-2026-0413","puntaje":null,"alto_riesgo":false} ` <br><br> ` RawContent        : HTTP/1.1 200 OK` <br><br> ` Content-Length: 61 ` <br><br> ` Content-Type: application/json ` <br><br> ` Date: Mon, 24 Aug 2026 02:25:52 GMT ` <br><br> ` Server: uvicorn ` <br><br> ` {"poliza":"POL-2026-0413","puntaje":null,"alto_riesgo":false} ` <br><br> ` Forms             : ` <br><br> ` Headers           : {[Content-Length, 61], [Content-Type, application/json], [Date, Mon, 24 Aug 2026 02:25:52 GMT], [Server, uvicorn]} ` <br><br> ` Images            : {} ` <br><br> ` InputFields       : {} ` <br><br> ` Links             : {} ` <br><br> ` ParsedHtml        : ` <br><br> ` RawContentLength  : 61 `| |
| H3 |` /historial ` | | | |` Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/historial `| ` StatusCode        : 200 ` <br><br> ` StatusDescription : OK ` <br><br> ` Content           : {"evaluaciones":[{"poliza":"POL-2026-0413","puntaje":null}]} ` <br><br> ` RawContent        : HTTP/1.1 200 OK ` <br><br> ` Content-Length: 60 `<br><br> ` Content-Type: application/json ` <br><br> ` Date: Mon, 24 Aug 2026 00:09:18 GMT ` <br><br> ` Server: uvicorn ` <br><br> ` {"evaluaciones":[{"poliza":"POL-2026-0413","puntaje":null}]} ` <br><br> ` Forms             : ` <br><br> `Headers           : {[Content-Length, 60], [Content-Type, application/json], [Date, Mon, 24 Aug 2026 00:09:18 GMT], [Server, uvicorn]} ` <br><br> ` Images            : {} ` <br><br> ` InputFields       : {} ` <br><br> ` Links             : {} ` <br><br> ` ParsedHtml        : ` <br><br> ` RawContentLength  : 60 `| |
| H4 |` /siniestros/999 ` <br><br> ` Devuelve 200 con {"error":"no existe el siniestro 999"} en lugar de 404 ` | | | |` Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/siniestros/999` |` StatusCode        :200 ` <br><br> ` StatusDescription :OK             ` <br><br> ` Content           : {"error":"no existe el siniestro 999"} ` <br><br> ` RawContent        : HTTP/1.1 200 OK ` <br><br> ` Content-Length: 38 ` <br><br> ` Content-Type: application/json ` <br><br> ` Date: Mon, 24 Aug 2026 01:30:04 GMT ` <br><br> ` Server: uvicorn ` <br><br> ` {"error":"no existe el siniestro 999"} `<br><br>` Forms            : ` <br><br> ` Headers           : {[Content-Length, 38], [Content-Type, application/json], [Date, Mon, 24 Aug 2026 01:30:04 GMT], [Server, uvicorn]} ` <br><br> ` Images            : {} ` <br><br> ` InputFields       : {} ` <br><br> ` Links             : {} ` <br><br> ` ParsedHtml        : ` <br><br> ` RawContentLength  : 38 ` | |
| H5 |` /exportar ` <br><br> ` Devuelve datos con octet-stream en lugar de JSON ` | | | | ` Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/exportar`|` StatusCode        :200 ` <br><br> ` StatusDescription : OK ` <br><br> ` Content           : {128, 4, 149, 198...}   ` <br><br> ` RawContent        : HTTP/1.1 200 OK ` <br><br> ` Content-Length: 22481 ` <br><br>`Content-Type: application/octet-stream`<br><br>`Date: Mon, 24 Aug 2026 01:42:35 GMT`<br><br>`Server: uvicorn`<br><br>`?.??W......]?(}?(?.id??.1??.poliza??POL-2026-0001??.monto??.158...`<br><br>`Headers           : {[Content-Length, 22481], [Content-Type, application/octet-stream], [Date, Mon, 24 Aug 2026 01:42:35 GMT], [Server, uvicorn]}`<br><br>`RawContentLength  : 22481` | |
| H6 | | | | | | | |
| H7 | | | | | | | |
| H8 | | | | | | | |
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
