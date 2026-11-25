# Information Gathering — Reconocimiento Web

Antes de poder atacar nada, hay que saber qué hay ahí fuera. El reconocimiento (*recon*) es la fase que construye el mapa completo de la superficie de ataque de un objetivo: qué dominios y subdominios existen, qué tecnologías corren por debajo, qué archivos e información quedaron expuestos por descuido, y qué rastro histórico ha dejado el objetivo en la web a lo largo del tiempo.

Este bloque cubre WHOIS, DNS y enumeración de subdominios, virtual hosts, registros de transparencia de certificados, fingerprinting de tecnologías, crawling, robots.txt, URIs `.well-known`, dorking en motores de búsqueda, archivos web históricos (Wayback Machine) y automatización del proceso completo.

## Contenido

1. [Fundamentos del reconocimiento web](01-introduccion-recon.md)
2. [WHOIS](02-whois.md)
3. [DNS: conceptos y registros](03-dns-fundamentos.md)
4. [Herramientas DNS: dig y consultas](04-herramientas-dns.md)
5. [Enumeración de subdominios](05-enumeracion-subdominios.md)
6. [Transferencia de zona DNS](06-transferencia-zona.md)
7. [Virtual Hosts](07-virtual-hosts.md)
8. [Registros de Transparencia de Certificados (CT logs)](08-ct-logs.md)
9. [Fingerprinting de tecnologías](09-fingerprinting.md)
10. [Crawling y robots.txt](10-crawling-robots.md)
11. [URIs .well-known](11-well-known-uris.md)
12. [Google Dorking y motores de búsqueda](12-google-dorking.md)
13. [Archivos web: Wayback Machine](13-wayback-machine.md)
14. [Automatización del reconocimiento](14-automatizacion-recon.md)

## Por qué este bloque importa

La calidad del reconocimiento determina directamente la calidad de todo lo que viene después. Un subdominio de desarrollo olvidado, un archivo de backup expuesto, o una cabecera que revela una versión vulnerable pueden ahorrar horas de trabajo de explotación — o directamente ser la única vía de entrada viable a un objetivo bien protegido en su superficie principal.
