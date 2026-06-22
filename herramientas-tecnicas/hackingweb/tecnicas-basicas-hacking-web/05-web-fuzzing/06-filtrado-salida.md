# Filtrado de la salida de fuzzing

## El problema: demasiado ruido

Una sesión de fuzzing contra una wordlist de varios miles de entradas puede generar cientos de "hallazgos" — muchos de ellos respuestas idénticas sin ningún interés (páginas de error genéricas, redirecciones estándar). Sin un buen filtrado, encontrar la aguja en el pajar es casi tan difícil como no haber fuzzeado nada.

Todas las herramientas principales ofrecen mecanismos de filtrado robustos, basados en las mismas señales: código de estado, tamaño de respuesta, número de palabras/líneas, y expresiones regulares sobre el contenido.

## Gobuster

| Flag | Función |
|---|---|
| `-s` (include) | Incluir solo respuestas con los códigos de estado indicados |
| `-b` (exclude) | Excluir respuestas con los códigos indicados |
| `--exclude-length` | Excluir respuestas de una longitud de contenido específica |

```bash
gobuster dir -u http://ejemplo.com/ -w wordlist.txt -s 200,301 --exclude-length 0
```

> `-s` y `-b` solo están disponibles en el modo `dir`.

## ffuf

| Flag | Función |
|---|---|
| `-mc` (match code) | Incluir solo respuestas con códigos de estado indicados |
| `-fc` (filter code) | Excluir respuestas con códigos indicados |
| `-fs` (filter size) | Excluir respuestas de un tamaño/rango específico |
| `-ms` (match size) | Incluir solo respuestas de un tamaño/rango específico |
| `-fw` (filter words) | Excluir respuestas con un número de palabras específico |
| `-mw` (match words) | Incluir solo respuestas con un número de palabras específico |
| `-fl` / `-ml` | Igual que `-fw`/`-mw` pero contando líneas |
| `-mt` (match time) | Incluir solo respuestas que cumplan una condición de tiempo de respuesta |

```bash
# Solo 200, descartando un tamaño de respuesta de relleno conocido
ffuf -u http://ejemplo.com/FUZZ -w wordlist.txt -mc 200 -fs 1234

# Excluir varios códigos de error comunes
ffuf -u http://ejemplo.com/FUZZ -w wordlist.txt -fc 404,401,302

# Buscar respuestas anómalamente lentas (>500ms), candidatas a inyección ciega
ffuf -u http://ejemplo.com/FUZZ -w wordlist.txt -mt ">500"
```

Por defecto, `ffuf` ya filtra para mostrar únicamente `200-299, 301, 302, 307, 401, 403, 405, 500` — un buen punto de partida que conviene ajustar según el objetivo concreto.

## wenum (fork mantenido de wfuzz)

| Flag | Función |
|---|---|
| `--hc` (hide code) | Excluir códigos de estado |
| `--sc` (show code) | Incluir solo códigos de estado |
| `--hl` / `--sl` | Ocultar/mostrar por número de líneas |
| `--hw` / `--sw` | Ocultar/mostrar por número de palabras |
| `--hs` / `--ss` | Ocultar/mostrar por tamaño |
| `--hr` / `--sr` | Ocultar/mostrar según coincidencia de **regex** en el cuerpo |
| `--filter` / `--hard-filter` | Filtro genérico — `--hard-filter` además impide que otros plugins procesen lo filtrado |

```bash
# Solo éxitos y redirecciones
wenum -w wordlist.txt --sc 200,301,302 -u https://ejemplo.com/FUZZ

# Ocultar errores comunes
wenum -w wordlist.txt --hc 404,400,500 -u https://ejemplo.com/FUZZ

# Buscar contenido que mencione "admin" o "password"
wenum -w wordlist.txt --sr "admin\|password" -u https://ejemplo.com/FUZZ
```

El filtrado por **regex** (`--hr`/`--sr`) es particularmente potente: permite aislar respuestas que contienen (o no) un patrón textual concreto, independientemente de su código de estado o tamaño — útil, por ejemplo, para localizar mensajes de error de base de datos específicos durante un fuzzing orientado a detectar inyección SQL.

## Estrategia práctica de filtrado iterativo

1. **Lanzar sin filtros** (o con los filtros por defecto de la herramienta) para tener una visión general.
2. **Identificar el "ruido base"**: la respuesta más repetida suele corresponder al comportamiento "normal" ante una entrada inválida (un `404` consistente, o un `200` con una página de error genérica de tamaño fijo).
3. **Filtrar ese ruido explícitamente** (por código, tamaño o número de palabras) y relanzar.
4. **Repetir** el proceso si tras el primer filtrado sigue habiendo demasiado volumen — a menudo aparece un segundo patrón de ruido que conviene filtrar también.

Esta iteración progresiva —filtrar, observar qué queda, refinar— es mucho más eficaz que intentar adivinar de antemano el filtro "perfecto": en la práctica, casi nunca se sabe con certeza qué aspecto tendrá una respuesta interesante antes de haber visto al menos una vez cómo responde la aplicación a entradas tanto válidas como inválidas.
