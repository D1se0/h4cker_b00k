# Fundamentos del reconocimiento web

## Qué es y por qué es la primera fase

El reconocimiento web es el proceso sistemático de recopilar información sobre un objetivo antes de intentar cualquier explotación. Es la fase de *Information Gathering* dentro de cualquier metodología de pentesting, y condiciona todo lo que viene después: no se puede atacar lo que no se ha descubierto.

Los objetivos principales del reconocimiento son:

- **Identificar activos**: descubrir todos los componentes públicamente accesibles del objetivo — páginas, subdominios, direcciones IP, tecnologías empleadas.
- **Descubrir información oculta**: localizar datos sensibles expuestos por descuido — backups, archivos de configuración, documentación interna.
- **Analizar la superficie de ataque**: evaluar tecnologías, configuraciones y posibles puntos de entrada para la explotación.
- **Recopilar inteligencia**: información reutilizable para fases posteriores, como personal clave, correos electrónicos, o patrones de comportamiento explotables en ingeniería social.

## Reconocimiento activo vs. pasivo

La distinción fundamental en cualquier fase de recon es si se interactúa directamente con la infraestructura del objetivo o no.

### Reconocimiento activo

Implica interacción directa con los sistemas del objetivo: escaneo de puertos, escaneo de vulnerabilidades, fuerza bruta de subdominios, *banner grabbing*, *web spidering*. Aporta información más completa y verificada, pero conlleva un riesgo de detección considerablemente mayor — estas interacciones pueden quedar registradas en logs y disparar alertas de sistemas de detección de intrusiones (IDS/IPS) o firewalls.

| Técnica | Riesgo de detección |
|---|---|
| Escaneo de puertos | Alto |
| Escaneo de vulnerabilidades | Alto |
| Mapeo de red | Medio-Alto |
| *Banner grabbing* | Bajo |
| *OS fingerprinting* | Bajo |
| Enumeración de servicios | Bajo |
| *Web spidering* | Bajo-Medio |

### Reconocimiento pasivo

Se basa exclusivamente en información ya disponible públicamente, sin interactuar directamente con los sistemas del objetivo: consultas a motores de búsqueda, WHOIS, análisis de registros DNS públicos, archivos web históricos, redes sociales, repositorios de código público. El riesgo de detección es prácticamente nulo, ya que toda la actividad se dirige a terceros (registradores, motores de búsqueda, archivos públicos), no al objetivo directamente.

| Técnica | Riesgo de detección |
|---|---|
| Consultas a motores de búsqueda | Muy bajo |
| Consultas WHOIS | Muy bajo |
| Análisis DNS | Muy bajo |
| Archivos web (Wayback Machine) | Muy bajo |
| Análisis de redes sociales | Muy bajo |
| Repositorios de código | Muy bajo |

## La estrategia correcta: combinar ambos enfoques

Ninguno de los dos enfoques es suficiente por sí solo. El reconocimiento pasivo es más sigiloso pero limitado a lo que ya es público; el activo es más completo pero arriesga revelar la presencia del auditor antes de tiempo. En la práctica, una metodología sólida empieza siempre por agotar las fuentes pasivas —que no cuestan nada en términos de riesgo— antes de pasar a técnicas activas, reservando estas últimas para llenar los huecos que el reconocimiento pasivo no pudo cubrir.

Este orden no es casual: cuanta más información se reúna pasivamente, más dirigido y eficiente puede ser el reconocimiento activo posterior, reduciendo el "ruido" generado contra el objetivo.

A lo largo de este bloque se recorren, en este mismo orden lógico, las técnicas y herramientas fundamentales: empezando por WHOIS y DNS (mayormente pasivas), pasando por descubrimiento de subdominios y virtual hosts (con componentes activos y pasivos), hasta fingerprinting, crawling y automatización del proceso completo.
