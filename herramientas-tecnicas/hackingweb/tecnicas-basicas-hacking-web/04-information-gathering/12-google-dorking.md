# Google Dorking y motores de búsqueda

## El motor de búsqueda como herramienta OSINT

Más allá de responder consultas cotidianas, los motores de búsqueda indexan una porción enorme de la web pública — y esa indexación se puede explotar deliberadamente para descubrir información que el propietario del sitio nunca pretendió que fuera tan fácil de encontrar: documentos confidenciales, páginas de login sin enlazar, credenciales filtradas accidentalmente, mensajes de error con rutas internas.

A esta práctica se le llama **descubrimiento mediante motores de búsqueda** o recopilación de **OSINT** (*Open Source Intelligence*).

### Por qué es tan valioso

- **Información de fuente abierta**: completamente legal y ético, ya que se trabaja exclusivamente con contenido ya público.
- **Amplitud**: los motores indexan una fracción gigantesca de la web, ofreciendo un alcance que ninguna herramienta de fuerza bruta individual podría igualar.
- **Sin barrera técnica**: no requiere herramientas especializadas, solo conocer la sintaxis de operadores adecuada.
- **Coste cero**: completamente gratuito.

## Operadores de búsqueda esenciales

| Operador | Función | Ejemplo |
|---|---|---|
| `site:` | Limita resultados a un dominio | `site:ejemplo.com` |
| `inurl:` | Busca un término en la URL | `inurl:login` |
| `filetype:` | Filtra por tipo de archivo | `filetype:pdf` |
| `intitle:` | Busca un término en el título de la página | `intitle:"confidential"` |
| `intext:` | Busca un término en el cuerpo del texto | `intext:"password reset"` |
| `cache:` | Muestra la versión cacheada de una página | `cache:ejemplo.com` |
| `link:` | Páginas que enlazan a una URL concreta | `link:ejemplo.com` |
| `allintext:` | Todas las palabras especificadas deben aparecer en el texto | `allintext:admin password reset` |
| `allinurl:` | Todas las palabras deben aparecer en la URL | `allinurl:admin panel` |
| `AND` / `OR` / `NOT` | Operadores lógicos de combinación | `site:ejemplo.com AND (inurl:admin OR inurl:login)` |
| `-` | Excluye un término | `site:noticias.com -inurl:deportes` |
| `"..."` | Búsqueda de frase exacta | `"política de seguridad de la información"` |
| `*` | Comodín | `filetype:pdf manual de usuario*` |

## Google Dorking (Google Hacking)

Combinar estos operadores estratégicamente para descubrir información sensible o vulnerabilidades expuestas se conoce como **Google Dorking** (o *Google Hacking*). Algunos patrones clásicos:

```
site:ejemplo.com inurl:login
site:ejemplo.com (inurl:login OR inurl:admin)
site:ejemplo.com filetype:pdf
site:ejemplo.com intext:"index of /"
site:ejemplo.com ext:sql | ext:env | ext:log
```

La [Google Hacking Database (GHDB)](https://www.exploit-db.com/google-hacking-database) de Exploit-DB mantiene un catálogo extenso y actualizado de dorks categorizados por tipo de hallazgo (credenciales expuestas, archivos sensibles, mensajes de error, dispositivos vulnerables expuestos a internet, paneles de login, etc.) — una referencia obligada antes de improvisar consultas propias.

## Casos de uso prácticos

- **Localizar paneles de administración**: `site:ejemplo.com inurl:admin`
- **Documentos potencialmente sensibles**: `site:ejemplo.com filetype:xls OR filetype:pdf OR filetype:doc`
- **Mensajes de error con información de stack/rutas**: `site:ejemplo.com intext:"Warning: mysql_connect()"`
- **Archivos de configuración expuestos accidentalmente**: `site:ejemplo.com ext:env OR ext:config OR ext:ini`
- **Listados de directorio habilitados sin querer**: `site:ejemplo.com intitle:"index of /"`

## Limitaciones a tener en cuenta

No todo lo que existe en un sitio está indexado: páginas bloqueadas por `robots.txt` (aunque, como se vio en el apartado anterior, esto no impide el acceso directo, solo evita que el motor de búsqueda lo indexe), contenido tras autenticación, o simplemente páginas demasiado nuevas o de bajo tráfico que el rastreador del motor aún no ha visitado. El dorking complementa el resto de técnicas de este bloque — no las sustituye.

## Combinándolo con el resto del reconocimiento

Una sesión de dorking eficaz suele alimentarse de información ya recopilada en pasos anteriores: nombres de empleados obtenidos en redes sociales o WHOIS, nombres de subdominios descubiertos vía CT logs, tecnologías identificadas mediante fingerprinting — cada uno de estos datos puede convertirse en un término de búsqueda más específico y, por tanto, más productivo que un dork genérico aplicado a ciegas.
