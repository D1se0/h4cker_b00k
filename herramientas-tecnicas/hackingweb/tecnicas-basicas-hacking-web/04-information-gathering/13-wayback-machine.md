# Archivos web: Wayback Machine

## Viajando al pasado de un sitio web

La [Wayback Machine](https://web.archive.org/), mantenida por la organización sin ánimo de lucro Internet Archive, conserva instantáneas históricas de sitios web desde 1996. Permite consultar exactamente cómo lucía —y qué contenía— un dominio en un momento concreto del pasado, incluyendo HTML, CSS, JavaScript e imágenes completas, no solo texto indexado.

## Cómo funciona

1. **Rastreo**: bots automatizados navegan la web siguiendo enlaces, de forma similar a cualquier crawler, pero en lugar de solo indexar texto para búsqueda, **descargan copias completas** de cada página visitada.
2. **Archivado**: cada captura se almacena vinculada a una fecha y hora exacta, creando una instantánea histórica verificable.
3. **Acceso**: cualquier usuario puede introducir una URL y seleccionar una fecha para ver el sitio tal como era entonces, navegar instantáneas individuales, o buscar términos dentro del contenido archivado.

La frecuencia de archivado varía enormemente según la popularidad del sitio: algunos se capturan varias veces al día, otros apenas tienen un puñado de instantáneas en años. No todo el contenido de internet está cubierto — Internet Archive prioriza sitios de valor cultural, histórico o de investigación, y algunos propietarios pueden solicitar exclusión (sin garantía absoluta de que se respete retroactivamente).

## Por qué es tan valioso en reconocimiento

- **Descubrir activos olvidados**: páginas, directorios, subdominios o archivos antiguos que ya no son accesibles —o enlazados— en la versión actual del sitio, pero que podrían seguir existiendo en algún rincón del servidor.
- **Rastrear cambios y patrones**: comparar instantáneas en distintos momentos revela cómo ha evolucionado la estructura, el contenido, las tecnologías empleadas, y potencialmente vulnerabilidades que existieron (y quizás se corrigieron mal) en versiones anteriores.
- **Inteligencia general (OSINT)**: estrategias de marketing pasadas, empleados mencionados en versiones antiguas del sitio, decisiones tecnológicas históricas — todo contexto útil para construir un perfil completo del objetivo.
- **Reconocimiento completamente sigiloso**: consultar la Wayback Machine no genera ninguna interacción directa con la infraestructura del objetivo, por lo que es indetectable desde su perspectiva.

## Ejemplo de uso

Buscar la captura más antigua disponible de un dominio permite observar su forma original, a menudo reveladora de tecnologías, estructura o contenido que ya no existe en la versión actual:

```
https://web.archive.org/web/20170610042301*/ejemplo.com
```

Explorando capturas sucesivas, es posible reconstruir:

- Versiones anteriores de formularios de login (a veces con endpoints distintos a los actuales, todavía operativos en el backend).
- Rutas de administración mencionadas en versiones antiguas de menús de navegación.
- Productos, nombres de servicio o terminología interna usados en el pasado que pueden seguir siendo válidos como credenciales débiles, nombres de usuario, o términos de búsqueda dorking.
- Direcciones de correo de empleados mencionados en páginas de contacto o equipo que ya no aparecen en el sitio actual.

## Buenas prácticas

- Empezar siempre por la captura **más antigua disponible**, para entender el punto de partida del sitio.
- Revisar capturas en puntos significativos del histórico (cambios de diseño evidentes, picos de actividad conocidos) en lugar de revisar exhaustivamente cada instantánea disponible.
- Cruzar cualquier hallazgo —una ruta antigua, un nombre de archivo— con el estado **actual** del sitio: muchas veces una ruta "histórica" sigue siendo accesible aunque ya no esté enlazada desde ningún sitio visible.

La Wayback Machine es, en definitiva, una de las fuentes pasivas más infravaloradas del reconocimiento web: coste cero, riesgo cero, y un potencial de hallazgos que ninguna otra técnica de este bloque puede igualar en términos de profundidad histórica.
