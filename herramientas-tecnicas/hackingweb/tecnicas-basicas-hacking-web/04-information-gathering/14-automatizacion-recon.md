# Automatización del reconocimiento

## Por qué automatizar

Repetir manualmente cada técnica vista en este bloque —WHOIS, DNS, subdominios, CT logs, fingerprinting, crawling— contra cada nuevo objetivo es lento y propenso a omisiones. La automatización aporta:

- **Eficiencia**: tareas repetitivas resueltas en una fracción del tiempo, liberando capacidad para el análisis y la toma de decisiones (que sigue siendo, y seguirá siendo, una tarea humana).
- **Escalabilidad**: cubrir múltiples dominios o un alcance amplio sin que el esfuerzo crezca linealmente.
- **Consistencia**: resultados reproducibles, sin el riesgo de "olvidar" un paso de la metodología bajo presión de tiempo.
- **Cobertura integral**: orquestar en un único flujo enumeración DNS, descubrimiento de subdominios, rastreo, escaneo de puertos, etc.
- **Integración**: conectar de forma fluida la salida del reconocimiento con las fases posteriores de evaluación y explotación.

## Frameworks de reconocimiento

| Framework | Enfoque |
|---|---|
| **FinalRecon** | Herramienta Python modular: cabeceras, WHOIS, certificados SSL, crawling, DNS, subdominios, fuzzing de directorios, Wayback Machine — todo en una única herramienta |
| **Recon-ng** | Framework modular en Python, con módulos para DNS, subdominios, escaneo de puertos e incluso explotación de vulnerabilidades conocidas |
| **theHarvester** | Especializado en recopilar correos, subdominios, hosts y banners desde múltiples fuentes OSINT (motores de búsqueda, servidores de claves PGP, Shodan) |
| **SpiderFoot** | Automatización de inteligencia de código abierto, integrando numerosas fuentes de datos en un único flujo |
| **OSINT Framework** | No es una herramienta en sí, sino un catálogo organizado de recursos y herramientas OSINT por categoría — útil como punto de partida cuando no se sabe qué herramienta concreta usar para un dato específico |

## FinalRecon en detalle

Cubre, en una sola herramienta, prácticamente todo lo visto en este bloque:

- **Header Information**: detalles del servidor y posibles configuraciones inseguras.
- **Whois Lookup**: registro de dominio y contactos.
- **SSL Certificate Information**: validez, emisor, detalles del certificado.
- **Crawler**: extracción de enlaces internos/externos, recursos JS/CSS, imágenes, `robots.txt`, `sitemap.xml`.
- **DNS Enumeration**: más de 40 tipos de registros, incluyendo DMARC para evaluar seguridad del correo.
- **Subdomain Enumeration**: combina crt.sh, AnubisDB, ThreatMiner, CertSpotter, y APIs de terceros (Facebook, VirusTotal, Shodan, BeVigil).
- **Directory Enumeration**: fuzzing con wordlists y extensiones personalizables.
- **Wayback Machine**: URLs históricas de los últimos años.

```bash
git clone https://github.com/thewhiteh4t/FinalRecon.git
cd FinalRecon
pip3 install -r requirements.txt
chmod +x ./finalrecon.py

./finalrecon.py --full --url https://ejemplo.com
```

El flag `--full` ejecuta todos los módulos en cadena, generando un perfil de reconocimiento completo en una sola ejecución — el punto de partida ideal al enfrentarse a un objetivo nuevo, antes de profundizar manualmente en los hallazgos más prometedores.

## Cómo encaja la automatización en una metodología real

La automatización **no sustituye** el análisis manual ni el criterio humano — acelera la fase de recopilación bruta de datos, pero la interpretación y correlación de esos datos (la parte que realmente encuentra vulnerabilidades, como se vio en el apartado de *crawling*) sigue requiriendo revisión activa.

Un flujo de trabajo razonable:

1. **Lanzar un framework de automatización completo** (FinalRecon, Recon-ng) contra el objetivo para obtener una base amplia rápidamente.
2. **Revisar manualmente** los resultados más prometedores: subdominios con nombres sugerentes (`dev`, `staging`, `internal`, `old`), archivos sensibles detectados, tecnologías con versiones desactualizadas.
3. **Completar con técnicas dirigidas** donde la automatización se quedó corta: fuzzing manual con wordlists personalizadas basadas en patrones ya observados, consultas dorking específicas, exploración manual de capturas de Wayback Machine en fechas relevantes.
4. **Documentar todo** de forma estructurada — el reconocimiento que no se registra se pierde, y es habitual tener que volver sobre estos datos en fases posteriores de la auditoría.

Este enfoque combinado —automatización amplia + revisión y profundización manual dirigida— es el que mejor balance ofrece entre cobertura, profundidad y tiempo invertido, y es la base sobre la que se construyen todas las técnicas de explotación que se tratan en los bloques siguientes de este temario.
