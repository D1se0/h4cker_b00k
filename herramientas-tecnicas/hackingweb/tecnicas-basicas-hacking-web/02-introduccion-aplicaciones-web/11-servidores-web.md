# Servidores web (Apache, Nginx, IIS)

## Qué hace un servidor web

Un servidor web es el software que se ejecuta en el servidor backend y gestiona todo el tráfico HTTP/HTTPS: recibe peticiones de los clientes, las enruta hacia el recurso o script correspondiente, y devuelve la respuesta con el código de estado adecuado. Normalmente escucha en los puertos 80 (HTTP) y 443 (HTTPS).

```bash
curl -I https://academy.hackthebox.com

HTTP/2 200
date: Tue, 15 Dec 2026 19:54:29 GMT
content-type: text/html; charset=UTF-8
```

El servidor web es responsable de devolver los códigos de estado vistos en el bloque de *Web Requests* (`200`, `301`/`302`, `400`, `401`, `403`, `404`, `405`, `500`, `502`, `504`...) en función de cómo procese cada petición.

## Apache (httpd)

El servidor web más extendido en internet, presente en aproximadamente un 40% de los sitios web según distintas mediciones. Viene preinstalado en la mayoría de distribuciones Linux y también está disponible para Windows y macOS.

Características relevantes:

- Se usa habitualmente junto a **PHP**, aunque también soporta `.NET`, Python, Perl, e incluso scripts del sistema operativo a través de **CGI**.
- Es modular: se pueden instalar módulos adicionales para extender su funcionalidad (por ejemplo, `mod_php` para servir PHP).
- Es de código abierto, ampliamente documentado y mantenido con actualizaciones de seguridad frecuentes.
- Configuración descentralizada habitual mediante archivos `.htaccess` por directorio — un punto de interés en auditorías, ya que configuraciones incorrectas ahí pueden filtrar información o desactivar protecciones sin que se note a simple vista.

## Nginx

El segundo servidor web más usado, con presencia especialmente fuerte entre los sitios de mayor tráfico mundial (cerca del 60% de los 100.000 sitios más visitados, según diversas mediciones). Su diseño asíncrono le permite atender un volumen elevado de conexiones concurrentes con un consumo de memoria y CPU comparativamente bajo, lo que lo hace especialmente popular como proxy inverso y balanceador de carga, además de servidor web tradicional.

Es también gratuito y de código abierto.

## IIS (Internet Information Services)

Desarrollado y mantenido por Microsoft, se ejecuta principalmente sobre Windows Server. Es la opción natural para alojar aplicaciones desarrolladas sobre el framework .NET, aunque también puede servir contenido en PHP u otros lenguajes, así como otros protocolos (FTP).

Una característica distintiva es su integración nativa con **Active Directory**, incluyendo `Windows Authentication`, que permite a los usuarios autenticarse automáticamente usando sus credenciales de dominio sin un login explícito — relevante en pentesting interno de entornos corporativos basados en Windows.

## Otros servidores relevantes

- **Apache Tomcat**: orientado a aplicaciones Java (servlets, JSP). Se trata en detalle en el bloque de *Attacking Common Applications*.
- **Node.js** (a través de frameworks como Express): sirve aplicaciones donde tanto frontend como backend están escritos en JavaScript.

## Fingerprinting de servidores web

Identificar qué servidor web (y, idealmente, qué versión) está sirviendo una aplicación es uno de los primeros pasos de reconocimiento en cualquier auditoría:

```bash
curl -I https://objetivo.com
```

La cabecera `Server` suele revelarlo directamente (`Server: Apache/2.4.41 (Ubuntu)`), aunque administradores cautelosos pueden ocultar o falsear esta cabecera. En esos casos, existen técnicas de fingerprinting más finas basadas en comportamientos específicos de cada servidor (manejo de cabeceras no estándar, formato exacto de páginas de error, orden de cabeceras en la respuesta), que se abordan en detalle en el bloque de *Information Gathering*.

Conocer el servidor web concreto también orienta la búsqueda de vulnerabilidades públicas conocidas para esa versión específica — tema que se desarrolla en el siguiente apartado de este bloque.
