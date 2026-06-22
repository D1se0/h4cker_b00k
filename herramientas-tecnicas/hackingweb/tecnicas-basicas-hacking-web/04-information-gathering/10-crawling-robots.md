# Crawling y robots.txt

## Qué es un rastreador (crawler/spider)

Un rastreador web es un proceso automatizado que navega sistemáticamente la web siguiendo enlaces de página en página, extrayendo y registrando información a medida que avanza — el mismo principio que usan los motores de búsqueda para indexar internet, aplicado aquí con fines de reconocimiento.

El funcionamiento básico: el rastreador parte de una **URL semilla**, obtiene su contenido, extrae todos los enlaces que contiene, los añade a una cola, y repite el proceso con cada uno de ellos.

## Estrategias de rastreo

| Estrategia | Prioriza | Útil para |
|---|---|---|
| **Breadth-first** (anchura) | Explorar todos los enlaces de un nivel antes de profundizar | Obtener una visión general rápida de la estructura completa |
| **Depth-first** (profundidad) | Seguir una ruta de enlaces hasta el final antes de retroceder | Explorar a fondo una sección concreta del sitio |

## Qué extrae un buen rastreador

- **Enlaces internos y externos**: construyen el mapa de la aplicación y revelan relaciones con dominios de terceros.
- **Comentarios**: en blogs, foros, secciones interactivas — pueden filtrar detalles internos sin que el usuario lo perciba.
- **Metadatos**: títulos, descripciones, autores, fechas — información de contexto valiosa.
- **Archivos sensibles**: backups (`.bak`, `.old`), configuraciones (`web.config`, `settings.php`), logs (`error_log`) — candidatos directos a contener credenciales, claves de API, o fragmentos de código fuente.

## La importancia del contexto: conectar hallazgos aislados

Un dato suelto rara vez es significativo por sí solo. El valor real del rastreo aparece al **correlacionar** hallazgos: una lista de enlaces que, examinada con calma, revela que varias URLs apuntan al mismo directorio (`/files/`); visitar ese directorio manualmente confirma que el *listado de directorio* está habilitado, exponiendo backups y documentos internos. Ese hallazgo crítico nunca habría aparecido analizando cada enlace de forma aislada — solo se hace visible al construir la imagen completa.

## robots.txt: el mapa que el propio sitio entrega

`robots.txt` es un archivo de texto plano en la raíz del dominio (`ejemplo.com/robots.txt`) que indica a los rastreadores qué partes del sitio pueden o no visitar, siguiendo el Estándar de Exclusión de Robots.

```
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /public/

User-agent: Googlebot
Crawl-delay: 10

Sitemap: https://ejemplo.com/sitemap.xml
```

| Directiva | Función |
|---|---|
| `User-agent` | A qué bot se aplican las reglas siguientes (`*` = todos) |
| `Disallow` | Rutas que el bot no debería rastrear |
| `Allow` | Excepción explícita dentro de una regla `Disallow` más amplia |
| `Crawl-delay` | Segundos de espera entre peticiones sucesivas |
| `Sitemap` | URL del mapa del sitio XML |

### La paradoja de robots.txt para un pentester

`robots.txt` está pensado para **proteger** ciertas rutas de la indexación pública en motores de búsqueda — pero, irónicamente, es también el lugar donde el propio sitio **revela voluntariamente** qué rutas considera lo bastante sensibles como para querer ocultarlas. Un bot malicioso (o un pentester) puede simplemente ignorar las directivas y visitar directamente esas rutas "prohibidas" — el archivo no impone ninguna restricción técnica real, solo una convención de buena fe que únicamente respetan los rastreadores legítimos.

Del ejemplo anterior se puede inferir directamente: existe un panel de administración en `/admin/` y contenido privado en `/private/` — información valiosa obtenida sin enviar una sola petición más allá de consultar el propio `robots.txt`.

> **Nota ética y legal**: aunque ignorar `robots.txt` es técnicamente trivial, sigue siendo importante operar dentro del alcance autorizado de cualquier auditoría. El valor de `robots.txt` en reconocimiento es la **información** que revela sobre la estructura del sitio, no una autorización para actuar sin límites.

## Herramientas de rastreo

| Herramienta | Notas |
|---|---|
| **Burp Suite Spider** | Integrado en el proxy, ideal combinado con el resto del flujo de trabajo (visto en el bloque de *Web Proxies*) |
| **OWASP ZAP Spider** | Equivalente gratuito, incluye variante Ajax Spider para SPAs |
| **Scrapy** (Python) | Framework completo para rastreadores personalizados, altamente configurable |
| **Apache Nutch** | Rastreador a gran escala, más orientado a proyectos masivos |

### Ejemplo con Scrapy: `ReconSpider`

```bash
pip3 install scrapy
python3 ReconSpider.py http://ejemplo.com
```

El resultado se guarda en `results.json`, estructurado por categorías:

```json
{
    "emails": ["contacto@ejemplo.com", "..."],
    "links": ["https://...", "..."],
    "external_files": ["https://ejemplo.com/wp-content/uploads/doc.pdf"],
    "js_files": ["https://ejemplo.com/wp-includes/js/jquery.js"],
    "images": ["..."],
    "comments": ["<!-- #masthead -->"]
}
```

Esta salida estructurada es exactamente el tipo de material que conviene revisar manualmente con calma: correos electrónicos para construir listas de usuarios, archivos JS para analizar lógica de frontend (relevante en el bloque de *JavaScript Deobfuscation*), y comentarios HTML que pueden contener pistas olvidadas — la misma idea que se vio en el bloque de *Introducción a Aplicaciones Web* sobre exposición de datos sensibles, ahora aplicada de forma sistemática y automatizada a todo un dominio.

## Buenas prácticas

- Obtener siempre autorización antes de rastrear de forma extensa o intrusiva.
- Respetar `Crawl-delay` cuando se especifica, para no sobrecargar el servidor objetivo.
- Combinar el rastreo con el resto de técnicas pasivas vistas en este bloque (CT logs, motores de búsqueda) para maximizar cobertura sin necesidad de fuerza bruta agresiva.
