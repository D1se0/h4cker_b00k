# Servidores back-end

## Qué es

El servidor back-end es el hardware y sistema operativo que aloja todos los componentes necesarios para ejecutar la aplicación: servidor web, base de datos, framework de desarrollo, y opcionalmente hipervisores, contenedores o un WAF (*Web Application Firewall*). Conceptualmente, se sitúa en la capa de acceso a datos de la arquitectura de tres capas vista anteriormente.

## "Stacks" o pilas tecnológicas habituales

Es muy común referirse a combinaciones específicas de sistema operativo, servidor web, base de datos y lenguaje mediante acrónimos:

| Stack | Componentes |
|---|---|
| **LAMP** | Linux, Apache, MySQL, PHP |
| **WAMP** | Windows, Apache, MySQL, PHP |
| **WINS** | Windows, IIS, .NET, SQL Server |
| **MAMP** | macOS, Apache, MySQL, PHP |
| **XAMPP** | Multiplataforma, Apache, MySQL, PHP/Perl |

### Por qué reconocer el stack es valioso en pentesting

Identificar el stack tecnológico de una aplicación —algo que se puede inferir de cabeceras HTTP (`Server`, `X-Powered-By`), extensiones de archivo (`.php`, `.aspx`, `.jsp`), mensajes de error característicos, o el comportamiento ante entradas específicas— permite anticipar:

- Qué clase de inyección es plausible (sintaxis SQL de MySQL vs. MSSQL vs. PostgreSQL son distintas).
- Qué vulnerabilidades públicas conocidas podrían aplicar a esa combinación concreta de versiones.
- Qué técnicas de explotación posteriores (por ejemplo, escritura de webshells, rutas de archivos típicas) son más probables.

## Hardware y escalabilidad

El rendimiento del servidor backend condiciona directamente la estabilidad y capacidad de respuesta de la aplicación. Para aplicaciones de gran escala, es habitual distribuir la carga entre varios servidores backend (balanceo de carga), o directamente usar infraestructura de centros de datos / proveedores cloud que ofrecen servidores virtuales bajo demanda, en lugar de depender de una única máquina física.

Desde una perspectiva ofensiva, un entorno con balanceo de carga puede complicar ciertos ataques (por ejemplo, condiciones de carrera que dependen de estado compartido entre instancias) pero también puede introducir inconsistencias explotables si la sincronización entre nodos no es perfecta (caché desactualizada, sesiones no compartidas correctamente entre instancias, etc.).
