# Fingerprinting de tecnologías

## Qué es y por qué es tan rentable

El *fingerprinting* (identificación de huella digital) consiste en determinar qué tecnologías concretas —servidor web, lenguaje de backend, framework, CMS, librerías de frontend, sistema operativo— sustentan una aplicación. Es, junto con la enumeración de subdominios, una de las técnicas con mejor relación esfuerzo/valor del reconocimiento: identificar correctamente la pila tecnológica permite:

- **Dirigir el ataque**: centrar esfuerzos en vulnerabilidades y exploits conocidos para esas tecnologías concretas, en lugar de probar a ciegas.
- **Detectar configuraciones incorrectas**: versiones desactualizadas, configuraciones por defecto sin endurecer, componentes con vulnerabilidades públicas conocidas.
- **Priorizar objetivos**: ante varios sistemas, identificar primero cuáles ejecutan software con mayor probabilidad de ser vulnerable.
- **Construir un perfil completo**: combinado con el resto del reconocimiento, da una imagen integral de la postura de seguridad del objetivo.

## Técnicas de fingerprinting

| Técnica | En qué consiste |
|---|---|
| **Banner grabbing** | Leer directamente los banners que muestran servicios y servidores — versión de software incluida. |
| **Análisis de cabeceras HTTP** | `Server` suele revelar el servidor web; `X-Powered-By` puede delatar el lenguaje/framework. |
| **Sondeo de respuestas específicas** | Enviar peticiones diseñadas a propósito para provocar respuestas (mensajes de error, comportamientos) característicos de tecnologías concretas. |
| **Análisis de contenido de página** | Comentarios de copyright, rutas de recursos (`wp-content/`, `/sites/default/`), patrones de nomenclatura de archivos. |

## Herramientas

| Herramienta | Tipo | Notas |
|---|---|---|
| **Wappalyzer** | Extensión de navegador / servicio web | Identifica CMS, frameworks, analítica, y mucho más de un vistazo |
| **BuiltWith** | Servicio web | Informes detallados, con planes de pago para mayor profundidad |
| **WhatWeb** | Línea de comandos | Amplia base de datos de firmas |
| **Nmap** (con NSE) | Línea de comandos | Identificación de servicios/SO, scripts especializados |
| **Netcraft** | Servicio web | Incluye reportes de hosting y seguridad |
| **wafw00f** | Línea de comandos | Específica para detectar la presencia (y tipo) de un WAF |

## Banner grabbing manual con `curl`

```bash
curl -I ejemplo.com

HTTP/1.1 301 Moved Permanently
Server: Apache/2.4.41 (Ubuntu)
Location: https://ejemplo.com/
```

Siguiendo la cadena de redirecciones suele revelar capas adicionales:

```bash
curl -I https://ejemplo.com

HTTP/1.1 301 Moved Permanently
Server: Apache/2.4.41 (Ubuntu)
X-Redirect-By: WordPress
Location: https://www.ejemplo.com/
```

`X-Redirect-By: WordPress` confirma de forma directa el CMS subyacente, sin necesidad de ninguna herramienta adicional. Profundizando un nivel más:

```bash
curl -I https://www.ejemplo.com

HTTP/1.1 200 OK
Server: Apache/2.4.41 (Ubuntu)
Link: <https://www.ejemplo.com/index.php/wp-json/>; rel="https://api.w.org/"
```

La presencia de `wp-json` en una cabecera `Link` es otra señal característica e inequívoca de WordPress (a través de su API REST integrada), reforzando la identificación.

## Detección de WAF con `wafw00f`

Antes de profundizar en fingerprinting activo o, más adelante, en pruebas de explotación, conviene comprobar si existe un **Web Application Firewall (WAF)** delante de la aplicación: un WAF puede bloquear o alterar las sondas de fingerprinting, generando falsos negativos o respuestas engañosas si no se tiene en cuenta su presencia.

```bash
pip3 install git+https://github.com/EnableSecurity/wafw00f
wafw00f ejemplo.com
```

Si se detecta un WAF, conviene ajustar las expectativas: las técnicas de evasión de filtros que se ven en bloques posteriores (Command Injection, SQL Injection) pasan a ser relevantes incluso en fases tempranas de reconocimiento activo.

## De la identificación a la explotación

Una vez identificada con precisión la tecnología y, si es posible, su número de versión exacto, el siguiente paso lógico —tratado en el bloque de *Introducción a Aplicaciones Web*, apartado de vulnerabilidades públicas— es buscar CVEs y exploits conocidos para esa combinación concreta. El fingerprinting es, en este sentido, el puente directo entre el reconocimiento puro y el inicio de la fase de explotación.
