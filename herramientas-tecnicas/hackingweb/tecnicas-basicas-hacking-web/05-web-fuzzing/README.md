# Web Fuzzing

El *fuzzing* es la técnica que convierte el reconocimiento de "lo que se ve" en el descubrimiento de "lo que está oculto pero accesible": directorios sin enlazar, archivos de backup olvidados, parámetros no documentados, virtual hosts internos, endpoints de API sin publicar. Este bloque cubre las herramientas de referencia (`ffuf`, Gobuster, FeroxBuster, wfuzz/wenum), las técnicas de fuzzing de directorios, parámetros, virtual hosts y subdominios, cómo filtrar el ruido de los resultados, cómo validar responsablemente un hallazgo, y cómo aplicar todo esto al fuzzing específico de APIs web.

## Contenido

1. [Fuzzing vs. fuerza bruta y herramientas](01-introduccion-fuzzing.md)
2. [Fuzzing de directorios y archivos](02-fuzzing-directorios.md)
3. [Fuzzing recursivo](03-fuzzing-recursivo.md)
4. [Fuzzing de parámetros y valores](04-fuzzing-parametros.md)
5. [Fuzzing de virtual hosts y subdominios](05-fuzzing-vhosts-subdominios.md)
6. [Filtrado de la salida de fuzzing](06-filtrado-salida.md)
7. [Validación responsable de hallazgos](07-validacion-hallazgos.md)
8. [Fuzzing de APIs web](08-fuzzing-apis.md)

## Por qué este bloque importa

La diferencia entre un pentester que solo encuentra lo "evidente" y uno que encuentra hallazgos reales suele estar exactamente aquí: en la disciplina de fuzzear sistemáticamente cada superficie posible (directorios, parámetros, hosts, endpoints de API) en lugar de limitarse a lo que la interfaz visible muestra. Las herramientas que se cubren aquí se usarán constantemente en el resto del temario, desde Command Injection hasta API Attacks.
