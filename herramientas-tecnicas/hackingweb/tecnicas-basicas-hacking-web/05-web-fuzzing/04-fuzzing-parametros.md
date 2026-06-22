# Fuzzing de parámetros y valores

## Por qué fuzzear parámetros, no solo rutas

Hasta ahora se ha buscado *dónde* existen recursos (directorios, archivos). El fuzzing de parámetros responde a una pregunta distinta: una vez localizado un endpoint, **¿qué parámetros acepta y qué valores espera?** Esto es crítico porque muchas vulnerabilidades —SQLi, XSS, IDOR, manipulación de lógica de negocio— solo se manifiestan a través de un parámetro concreto que ni siquiera aparece en la interfaz visible.

## GET: parámetros visibles

```
https://ejemplo.com/search?query=fuzzing&category=security
```

Visibles directamente en la URL, separados por `&`. Por su naturaleza pública (quedan en historial, logs, `Referer`), se usan típicamente para operaciones que no deberían modificar estado en el servidor — búsquedas, filtros, paginación.

## POST: parámetros en el cuerpo

Viajan en el cuerpo de la petición, no en la URL — el método preferido para datos sensibles (credenciales, información personal) y para operaciones que sí modifican estado.

## Dos tipos de fuzzing de parámetros

### 1. Descubrir el *nombre* del parámetro

Cuando no se conoce qué parámetros acepta un endpoint (sin documentación, sin ejemplos visibles en el frontend):

```bash
ffuf -u http://10.10.10.5/get.php?FUZZ=valor \
     -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
     -fc 404
```

Aquí `FUZZ` reemplaza el **nombre** del parámetro, no su valor — se está probando si existe un parámetro llamado `id`, `user`, `debug`, `redirect`, etc.

### 2. Descubrir el *valor* válido de un parámetro conocido

Una vez se conoce el nombre del parámetro (por ejemplo, `x`), pero no qué valores acepta:

```bash
ffuf -u 'http://10.10.10.5/get.php?x=FUZZ' \
     -w wordlist.txt -mc 200
```

```
[Status: 200, Size: 25] FUZZ: OA_HTML
```

Aquí `FUZZ` reemplaza el **valor**, iterando hasta encontrar uno que el servidor acepte (en lugar de devolver, por ejemplo, una página de error genérica para valores inválidos).

## Fuzzing de POST con `ffuf`

```bash
ffuf -u http://10.10.10.5/post.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "y=FUZZ" \
     -w wordlist.txt -mc 200
```

- `-X POST`: fuerza el método.
- `-H`: añade la cabecera de tipo de contenido necesaria para que el servidor interprete correctamente el cuerpo.
- `-d "y=FUZZ"`: el cuerpo de la petición, con `FUZZ` en la posición del valor que se quiere descubrir.

## Reconociendo el patrón de "respuesta de éxito"

La clave del fuzzing de parámetros es identificar qué distingue una respuesta "válida" de una "inválida" — no siempre es tan evidente como un código `200` vs `404`. Puede ser:

- Una diferencia de **tamaño** de respuesta significativa.
- Un **código de estado distinto** al patrón mayoritario (la mayoría de valores fallidos devuelven `400`, pero uno concreto devuelve `200`).
- Un **mensaje de error distinto** (genérico vs. específico, que puede filtrar información sobre la lógica interna).
- Un **tiempo de respuesta anómalo**, indicativo de un procesamiento distinto en el backend (relevante, por ejemplo, en técnicas de inyección ciega que se verán en el bloque de *SQL Injection*).

En entornos de prueba controlados es habitual que el valor correcto destaque de forma obvia; en aplicaciones reales, suele requerir comparar cuidadosamente las respuestas y, a menudo, combinar varios filtros simultáneamente (visto en detalle en el apartado de filtrado de este mismo bloque) para aislar la señal real entre el ruido.

## Conectando con el resto del temario

El fuzzing de parámetros es la puerta de entrada práctica a casi todas las clases de inyección que se cubren más adelante: una vez se sabe que un parámetro existe y qué tipo de valor espera, el siguiente paso natural es sustituir ese valor por payloads de prueba (comillas para SQLi, operadores de shell para Command Injection, HTML/JS para XSS) y observar cómo reacciona el backend — exactamente el mismo flujo de trabajo, aplicado con un objetivo distinto en cada bloque posterior.
