# Fuzzing recursivo

## El problema de las estructuras anidadas

El fuzzing básico solo explora un nivel: si se descubre un directorio `/admin/`, hay que repetir manualmente el comando apuntando a `/admin/FUZZ` para ver qué hay dentro. En aplicaciones con estructuras de varios niveles de profundidad, repetir esto manualmente para cada directorio descubierto es tedioso e impráctico.

## Cómo funciona el fuzzing recursivo

1. **Fuzzing inicial**: se empieza en la raíz (`/FUZZ`), enviando peticiones según la wordlist.
2. **Descubrimiento y expansión**: cuando se encuentra un directorio válido (por ejemplo, una respuesta `301` para `/admin`), la herramienta crea automáticamente una nueva "rama" de fuzzing en `/admin/FUZZ`.
3. **Profundidad iterativa**: el proceso se repite para cada directorio descubierto, hasta alcanzar un límite de profundidad configurado o agotar las posibilidades.

Es, conceptualmente, una exploración en árbol: la raíz web es el tronco, cada directorio descubierto es una rama, y el fuzzer recorre sistemáticamente cada rama hasta sus hojas (archivos) o hasta el límite establecido.

## Por qué usarlo

- **Eficiencia**: automatiza por completo el descubrimiento en profundidad, sin intervención manual.
- **Exhaustividad**: reduce el riesgo de pasar por alto recursos enterrados varios niveles por debajo de la raíz.
- **Escalabilidad**: imprescindible en aplicaciones grandes donde la exploración manual nivel a nivel sería completamente inviable.

## Fuzzing recursivo con `ffuf`

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
     -ic -v -u http://10.10.10.5/FUZZ -e .html -recursion
```

- `-recursion`: activa el fuzzing recursivo — cada directorio descubierto dispara automáticamente un nuevo trabajo de fuzzing dentro de él.
- `-ic` (*ignore comments*): ignora líneas de la wordlist que empiezan por `#`, evitando que se traten como entradas válidas.
- `-v`: salida detallada (verbose), útil para seguir el progreso de cada rama explorada.

```
[Status: 301] http://10.10.10.5/level1 --> /level1/
[INFO] Adding a new job to the queue: http://10.10.10.5/level1/FUZZ
[Status: 200] http://10.10.10.5/level1/index.html
[Status: 301] http://10.10.10.5/level1/level2 --> /level1/level2/
[INFO] Adding a new job: http://10.10.10.5/level1/level2/FUZZ
```

Cada nuevo directorio descubierto genera automáticamente un nuevo "trabajo" en cola, sin que el operador tenga que intervenir.

## Controlando el alcance: responsabilidad operativa

El fuzzing recursivo puede multiplicar exponencialmente el número de peticiones enviadas, con riesgo real de sobrecargar el servidor objetivo o disparar mecanismos de defensa (rate limiting, bloqueo de IP). `ffuf` ofrece controles específicos para mitigarlo:

```bash
ffuf -w wordlist.txt -ic -u http://10.10.10.5/FUZZ -e .html \
     -recursion -recursion-depth 2 -rate 500
```

| Flag | Función |
|---|---|
| `-recursion-depth` | Límite máximo de niveles de profundidad a explorar |
| `-rate` | Peticiones por segundo, para no saturar el servidor |
| `-timeout` | Tiempo de espera por petición, evita bloqueos en objetivos que no responden |

## Cuándo merece la pena

El fuzzing recursivo es especialmente valioso cuando el reconocimiento previo (crawling, robots.txt, código fuente) ya sugiere una estructura jerárquica no trivial — por ejemplo, un `robots.txt` que menciona `/internal/` invita directamente a lanzar fuzzing recursivo desde esa ruta concreta, en lugar de hacerlo a ciegas desde la raíz completa del sitio, ahorrando tiempo y reduciendo el ruido generado contra el objetivo.
