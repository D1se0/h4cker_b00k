# Bypass de autenticación con manipulación de verbos

## El escenario: autenticación HTTP básica que no cubre todos los verbos

Imaginemos un panel de administración en `/admin/reset.php` protegido por autenticación HTTP básica. Al intentar acceder con `GET` aparece una ventana de login (`401 Unauthorized`). Al cambiar a `POST`, el servidor también pide autenticación — confirma que la configuración cubre ambos verbos habituales.

Pero, ¿y `HEAD`? Una petición `HEAD` es funcionalmente idéntica a `GET` — ejecuta la misma lógica en el servidor, solo que devuelve la respuesta sin cuerpo. Si la configuración de `<Limit>` del servidor solo lista `GET` y `POST`, `HEAD` queda fuera de esa restricción y se procesa sin exigir credenciales.

## Verificando qué verbos acepta el servidor

```bash
curl -i -X OPTIONS http://objetivo/admin/reset.php

HTTP/1.1 200 OK
Allow: POST,OPTIONS,HEAD,GET
```

La cabecera `Allow:` confirma que el servidor acepta `HEAD` — candidato inmediato para probar el bypass.

## El bypass en acción

```bash
curl -i -X HEAD http://objetivo/admin/reset.php
```

Si la respuesta es `200 OK` (o cualquier código distinto de `401`) sin solicitar credenciales, la manipulación de verbo ha eludido la autenticación. La funcionalidad del endpoint se ejecutó aunque no se proporcionaran credenciales — con `HEAD` la respuesta no incluye cuerpo, pero la acción en el servidor (en este caso, un reset) sí se realizó.

También vale la pena probar otros verbos aceptados que no estén en el bloque `<Limit>`:

```bash
curl -i -X DELETE http://objetivo/admin/reset.php
curl -i -X PATCH  http://objetivo/admin/reset.php
```

## Configuraciones vulnerables en distintos servidores web

| Servidor | Configuración vulnerable | Por qué falla |
|---|---|---|
| Apache | `<Limit GET POST>` | No cubre HEAD, PUT, DELETE, etc. |
| Tomcat | `<http-method>GET</http-method>` en `web.xml` | Idéntica lógica de cobertura parcial |
| ASP.NET | `<verbs>GET,POST</verbs>` en `web.config` | Idéntica lógica |

La causa raíz es siempre la misma: la lista de verbos restringidos en el control de autenticación es incompleta respecto al conjunto de verbos que el servidor acepta realmente.

## Mitigación

- Usar directivas que cubran **todos los verbos** no permitidos, no solo los esperados:
  - Apache: `<LimitExcept GET POST>` (más seguro — deniega todo excepto lo explícitamente permitido)
  - O bien, deshabilitar en el servidor todos los verbos no necesarios para la aplicación

El apartado de prevención al final de esta sección desarrolla en detalle las configuraciones correctas para cada servidor.
