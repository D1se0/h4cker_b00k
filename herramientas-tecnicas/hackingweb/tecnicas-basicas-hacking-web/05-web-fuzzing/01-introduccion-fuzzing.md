# Fuzzing vs. fuerza bruta y herramientas

## Qué es el fuzzing

El fuzzing web es la técnica de probar sistemáticamente una aplicación con entradas inesperadas, mal formadas o simplemente variadas, observando cómo reacciona, con el objetivo de descubrir comportamientos que revelen vulnerabilidades o recursos ocultos.

## Fuzzing vs. fuerza bruta: la distinción

Aunque en el día a día se usan casi como sinónimos, hay un matiz conceptual:

- **Fuzzing**: espectro amplio. Se alimenta la aplicación con entradas variadas —datos mal formados, caracteres inválidos, combinaciones sin sentido— para observar reacciones inesperadas y descubrir fallos en el manejo de datos.
- **Fuerza bruta**: más específica. Prueba sistemáticamente todas las posibilidades para un valor concreto (una contraseña, un identificador), normalmente apoyándose en diccionarios predefinidos.

> Analogía: el fuzzing es lanzar de todo contra una puerta cerrada (llaves, un destornillador, lo que sea) para ver si algo la abre; la fuerza bruta es probar sistemáticamente cada llave de un llavero conocido hasta encontrar la correcta.

## Por qué el fuzzing es indispensable

- **Descubre vulnerabilidades ocultas** que las pruebas manuales tradicionales pasarían por alto, al provocar comportamientos inesperados con entradas anómalas.
- **Automatiza** la generación y el envío masivo de datos de prueba, liberando tiempo humano para el análisis.
- **Simula ataques reales**, permitiendo encontrar fallos antes de que lo haga un atacante.
- **Refuerza la validación de entrada**, exponiendo debilidades que derivan en SQLi, XSS y otras inyecciones.
- Puede integrarse en **pipelines CI/CD** para pruebas de seguridad continuas durante el desarrollo.

## Conceptos esenciales

| Concepto | Descripción | Ejemplo |
|---|---|---|
| **Wordlist** | Lista de palabras/valores usados como entrada de prueba | `admin`, `backup`, `login` |
| **Payload** | El dato concreto enviado en cada intento | `' OR 1=1 --` |
| **Response Analysis** | Comparar respuestas para detectar anomalías | `200 OK` esperado vs. `500` inesperado |
| **Fuzzer** | Herramienta que automatiza el proceso | `ffuf`, `wfuzz`, Burp Intruder |
| **Falso positivo** | El fuzzer marca algo como hallazgo sin serlo | Un `404` mal interpretado como válido |
| **Falso negativo** | Una vulnerabilidad real que el fuzzer no detecta | Un fallo lógico sutil no cubierto por la wordlist |
| **Scope** | Qué partes concretas de la app se están fuzzeando | Solo el login, o solo un endpoint de API |

## Herramientas de referencia

### ffuf (Fuzz Faster U Fool)

Escrito en Go, extremadamente rápido. La herramienta de referencia para enumeración de directorios/archivos, descubrimiento de parámetros y fuerza bruta.

```bash
go install github.com/ffuf/ffuf/v2@latest
```

### Gobuster

Rápido y sencillo, ideal tanto para principiantes como avanzados. Soporta descubrimiento de contenido, enumeración de subdominios DNS, y detección de contenido específico de WordPress.

```bash
go install github.com/OJ/gobuster/v3@latest
```

### FeroxBuster

Escrito en Rust, especializado en descubrimiento **recursivo** de contenido no enlazado. Más una herramienta de "navegación forzada" que un fuzzer de propósito general.

```bash
curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh | sudo bash -s $HOME/.local/bin
```

### wfuzz / wenum

`wenum` es el fork activamente mantenido de `wfuzz` (que ha quedado con menos mantenimiento), especialmente versátil para fuzzing de parámetros. Los comandos son intercambiables.

```bash
pipx install git+https://github.com/WebFuzzForge/wenum
pipx runpip wenum install setuptools
```

## Comparativa rápida

| Herramienta | Punto fuerte | Mejor para |
|---|---|---|
| `ffuf` | Velocidad, flexibilidad | Directorios, parámetros, fuzzing genérico |
| Gobuster | Simplicidad | Directorios, DNS, vhost |
| FeroxBuster | Recursión nativa | Descubrimiento profundo automatizado |
| wenum/wfuzz | Filtrado avanzado | Fuzzing de parámetros con lógica compleja |

No hay una única herramienta "mejor" para todo: en la práctica, conviene dominar al menos `ffuf` y una alternativa, ya que cada una tiene matices de sintaxis y rendimiento que se ajustan mejor a distintos escenarios.
