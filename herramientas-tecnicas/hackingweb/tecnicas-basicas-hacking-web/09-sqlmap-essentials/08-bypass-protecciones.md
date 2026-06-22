# Sorteando protecciones de aplicaciones web

> Este apartado describe mecanismos que SQLMap incorpora para continuar una auditoría **autorizada** cuando la aplicación objetivo implementa controles anti-automatización legítimos. Conocerlos es tan relevante para quien hace pentesting como para quien diseña esos mismos controles desde la perspectiva defensiva.

## Tokens anti-CSRF

Muchas aplicaciones incluyen un token único por sesión o petición (visto en el bloque de *Introducción a Aplicaciones Web*, en el apartado de CSRF) que, además de proteger contra falsificación de peticiones, dificulta incidentalmente la automatización: cada petición necesita un token "fresco" extraído de la respuesta anterior.

```bash
sqlmap -u "http://objetivo.htb/" --data="id=1&csrf-token=WfF1szMU..." --csrf-token="csrf-token"
```

SQLMap analiza automáticamente cada respuesta en busca de un nuevo valor de token y lo reutiliza en la siguiente petición. Incluso sin especificar `--csrf-token` explícitamente, si detecta un parámetro con un nombre sugerente (`csrf`, `xsrf`, `token`), preguntará si se desea activar esta actualización automática.

## Valores únicos por petición (sin relación con CSRF)

Algunas aplicaciones exigen que un parámetro concreto sea siempre distinto en cada petición, como medida anti-replay sencilla:

```bash
sqlmap -u "http://objetivo.htb/?id=1&rp=29125" --randomize=rp --batch
```

`--randomize` genera un valor aleatorio distinto para ese parámetro en cada petición enviada.

## Parámetros calculados (hash derivado de otro valor)

Cuando un parámetro debe contener, por ejemplo, el hash MD5 de otro:

```bash
sqlmap -u "http://objetivo.htb/?id=1&h=c4ca4238a0b923820dcc509a6f75849b" \
  --eval="import hashlib; h=hashlib.md5(id).hexdigest()"
```

`--eval` ejecuta código Python arbitrario justo antes de enviar cada petición, permitiendo calcular dinámicamente cualquier valor dependiente de otros parámetros — una forma controlada de extender el comportamiento de SQLMap sin modificar su código fuente.

## Enrutando el tráfico a través de un proxy

```bash
sqlmap ... --proxy="socks4://127.0.0.1:9050"
sqlmap ... --proxy-file=lista_proxies.txt
sqlmap ... --tor --check-tor
```

`--tor` enruta automáticamente a través de la red Tor si está correctamente configurada en local; `--check-tor` verifica contra `check.torproject.org` que el enrutamiento es efectivo antes de proceder. En auditorías profesionales, esto suele ser relevante más por necesidad operativa (evitar bloqueos temporales por volumen de peticiones contra un objetivo autorizado) que por anonimato propiamente dicho.

## Detección y manejo de WAF

Como parte de sus pruebas iniciales, SQLMap envía una sonda deliberadamente "ruidosa" con un nombre de parámetro inexistente, para comprobar si existe algún WAF/IPS interpuesto. Si la respuesta cambia sustancialmente (por ejemplo, un `406 Not Acceptable` típico de ModSecurity), SQLMap usa la librería [identYwaf](https://github.com/stamparm/identYwaf) para intentar identificar el producto concreto entre un catálogo de firmas conocidas.

```bash
sqlmap ... --skip-waf   # omite esta comprobación, generando menos ruido si ya se sabe que no hay WAF
```

## Scripts de manipulación (`tamper`)

Los scripts `tamper` son pequeños módulos en Python que transforman el payload justo antes de enviarlo, pensados para sortear filtros de entrada poco sofisticados:

| Script | Transformación |
|---|---|
| `space2comment` | Sustituye espacios por comentarios SQL `/**/` |
| `randomcase` | Alterna mayúsculas/minúsculas en palabras clave (`SELECT` → `SeleCt`) |
| `between` | Sustituye `>` por `NOT BETWEEN 0 AND #`, y `=` por `BETWEEN # AND #` |
| `base64encode` | Codifica el payload completo en Base64 |
| `charencode` | Codificación porcentual de cada carácter |

```bash
sqlmap ... --tamper=between,randomcase
sqlmap --list-tampers   # catálogo completo disponible
```

Los scripts se encadenan en el orden especificado, respetando una prioridad interna predefinida para evitar que se interfieran entre sí cuando varios modifican la sintaxis SQL del payload.

## Otras técnicas de evasión

- **`--chunked`**: divide el cuerpo de la petición POST en fragmentos (*Transfer-Encoding: chunked*), de forma que palabras clave SQL en listas negras simples queden repartidas entre fragmentos.
- **HTTP Parameter Pollution (HPP)**: divide el payload entre múltiples valores del mismo nombre de parámetro (`?id=1&id=UNION&id=SELECT...`), aprovechando que algunas plataformas backend (notablemente ASP/ASP.NET clásico) concatenan automáticamente todos los valores recibidos para ese nombre.

## La lección de fondo, desde ambas perspectivas

Desde el lado ofensivo, estas técnicas existen porque las protecciones perimetrales (WAF, anti-CSRF, listas negras de palabras clave) son, por diseño, **mitigaciones de superficie** — no corrigen la causa raíz (entrada sin parametrizar) vista en el bloque anterior. Desde el lado defensivo, esta misma observación es la justificación de por qué un WAF nunca debe ser la única línea de defensa: las consultas parametrizadas siguen siendo, con diferencia, la mitigación estructuralmente más sólida, exactamente como se concluyó en el apartado de mitigación del bloque de *SQL Injection Fundamentals*.
