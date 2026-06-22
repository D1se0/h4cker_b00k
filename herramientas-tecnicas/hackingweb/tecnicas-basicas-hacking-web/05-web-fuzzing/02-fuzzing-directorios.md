# Fuzzing de directorios y archivos

## Qué se busca

Toda aplicación tiende a acumular recursos que no están enlazados desde la interfaz visible: backups, archivos de configuración, logs, entornos de desarrollo, paneles administrativos, funcionalidades no documentadas. Ninguno de ellos aparece navegando normalmente — solo se descubren probando sistemáticamente posibles rutas.

Categorías típicas de hallazgos:

- **Datos sensibles**: backups, configuraciones, logs con credenciales.
- **Contenido desactualizado**: versiones antiguas de scripts, potencialmente vulnerables a exploits conocidos.
- **Recursos de desarrollo**: entornos de staging, paneles admin reutilizados de pruebas.
- **Funcionalidad oculta**: endpoints no documentados con comportamiento inesperado.

Estas áreas suelen recibir **menos escrutinio de seguridad** que el resto de la aplicación, precisamente por no estar pensadas para ser descubiertas — lo que las convierte en objetivos prioritarios.

## Wordlists

La calidad de una sesión de fuzzing depende directamente de la wordlist usada. **SecLists** ([github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists)) es la colección de referencia, con listas específicas para cada propósito.

> En PwnBox/Kali, suele estar en `/usr/share/seclists/` (minúsculas); en otras distribuciones puede variar la capitalización — comprobar la ruta si un comando no encuentra el archivo.

| Wordlist | Cuándo usarla |
|---|---|
| `Discovery/Web-Content/common.txt` | Punto de partida rápido, propósito general |
| `Discovery/Web-Content/directory-list-2.3-medium.txt` | Cobertura más amplia, centrada en directorios |
| `Discovery/Web-Content/raft-large-directories.txt` | Campañas exhaustivas |
| `Discovery/Web-Content/big.txt` | Cobertura muy amplia, directorios y archivos combinados |

## Fuzzing básico con `ffuf`

El marcador `FUZZ` en la URL indica dónde se sustituirá cada entrada de la wordlist:

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
     -u http://10.10.10.5/FUZZ
```

Por cada palabra de la lista, `ffuf` construye una petición (`http://10.10.10.5/admin`, `http://10.10.10.5/backup`...) y analiza la respuesta (código de estado, tamaño) para decidir si es relevante.

```
w2ksvrus    [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 0ms]
```

Un `301` (redirección, típico cuando se accede a un directorio sin la barra final) confirma que ese recurso existe.

## Buscando archivos con extensión

```bash
ffuf -w wordlist.txt -u http://10.10.10.5/FUZZ -e .php,.bak,.txt,.html
```

`-e` añade automáticamente cada extensión especificada a cada palabra de la wordlist, multiplicando la cobertura sin necesidad de mantener wordlists separadas por extensión.

## Por qué este paso es tan rentable

El fuzzing de directorios y archivos suele tener una de las mejores relaciones esfuerzo/resultado de toda la metodología de pentesting: requiere poco conocimiento previo de la aplicación, se automatiza completamente, y con relativa frecuencia revela hallazgos de alto impacto (credenciales en backups, código fuente expuesto, paneles administrativos sin proteger) que de otro modo pasarían completamente desapercibidos. Es, junto al reconocimiento DNS visto en el bloque anterior, uno de los primeros pasos activos en cualquier auditoría web.
