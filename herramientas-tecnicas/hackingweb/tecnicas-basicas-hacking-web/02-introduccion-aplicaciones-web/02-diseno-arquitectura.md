# Diseño y arquitectura de aplicaciones web

No existen dos aplicaciones web construidas exactamente igual. Cada organización diseña su infraestructura según sus necesidades de escala, presupuesto y tolerancia al riesgo. Entender los patrones arquitectónicos más comunes ayuda a anticipar, durante una auditoría, qué impacto puede tener comprometer un componente concreto.

La estructura de una aplicación web se puede analizar en tres niveles:

| Categoría | Qué describe |
|---|---|
| Infraestructura | Cómo se distribuyen físicamente los componentes (servidores, bases de datos). |
| Componentes | Las piezas funcionales que la conforman: interfaz, cliente, servidor. |
| Arquitectura | Cómo se relacionan esos componentes entre sí. |

## Modelos de infraestructura

### Cliente-servidor (el modelo base)

Un único servidor aloja la aplicación y la sirve a cualquier cliente que la solicite. El frontend se ejecuta e interpreta en el navegador; el backend corre y se procesa en el servidor. Es el modelo conceptual sobre el que se construyen todos los demás.

### Un solo servidor

Toda la aplicación —incluida la base de datos— vive en una única máquina. Es la opción más sencilla de desplegar, pero también la más arriesgada desde el punto de vista de seguridad: **todos los huevos en la misma cesta**. Si se compromete ese servidor (por cualquier vulnerabilidad, en cualquier componente alojado), se compromete absolutamente todo: aplicación, datos y disponibilidad. Y si el servidor cae, toda la aplicación deja de estar disponible.

### Muchos servidores, una base de datos

La base de datos se separa en su propio servidor, accesible por uno o varios servidores de aplicación. Esto introduce **segmentación**: comprometer el servidor web no implica automáticamente comprometer el servidor de base de datos (y viceversa), siempre que existan controles de acceso adecuados entre ambos. Es un patrón habitual cuando varias aplicaciones (por ejemplo, una principal y una réplica de respaldo) necesitan compartir los mismos datos.

### Muchos servidores, muchas bases de datos

Extiende el modelo anterior: cada aplicación tiene su propia base de datos, accesible únicamente por ella (más, opcionalmente, acceso a datos compartidos). Es el modelo más robusto en términos de seguridad y resiliencia, ya que limita el "radio de explosión" de cualquier vulnerabilidad a un único par aplicación-base de datos, y favorece la redundancia ante caídas. A cambio, es más complejo de implementar y operar (requiere balanceadores de carga, sincronización, etc.).

Más allá de estos cuatro modelos clásicos, existen arquitecturas modernas como las **serverless** (funciones ejecutadas bajo demanda en proveedores cloud, sin gestión directa de servidores) y los **microservicios** (descritos más abajo).

## Componentes de una aplicación web

Independientemente del modelo de infraestructura elegido, toda aplicación web se descompone en:

1. **Cliente**: navegador o cualquier consumidor de la API.
2. **Servidor**: a su vez compuesto por:
   - Servidor web (gestiona las conexiones HTTP)
   - Lógica de la aplicación (el código de negocio)
   - Base de datos
3. **Servicios**: integraciones de terceros o microservicios internos.
4. **Funciones**: en arquitecturas serverless, unidades de cómputo bajo demanda.

## Arquitectura de tres capas

Es habitual describir la arquitectura interna de una aplicación en tres capas lógicas (independientemente de cómo se distribuyan físicamente):

| Capa | Función |
|---|---|
| **Presentación** | Lo que el usuario ve e interactúa: HTML, CSS, JavaScript renderizados en el navegador. |
| **Aplicación** | Procesa cada petición: valida autorización, aplica lógica de negocio, decide qué datos devolver. |
| **Datos** | Determina dónde y cómo se almacenan/recuperan los datos necesarios. |

## Microservicios

Un microservicio es un componente independiente, normalmente responsable de una única tarea de negocio bien delimitada (registro, búsqueda, pagos, valoraciones, reseñas...). Cada microservicio puede desarrollarse en un lenguaje distinto y desplegarse de forma independiente, comunicándose con el resto mediante peticiones —típicamente *stateless*: cada petición es independiente y no depende de un estado compartido en memoria entre microservicios.

Ventajas habituales: agilidad de desarrollo, escalabilidad selectiva (escalar solo el componente que recibe más carga), despliegues independientes, reutilización de código y mayor resiliencia (la caída de un microservicio no tiene por qué tumbar toda la aplicación).

Desde la perspectiva de seguridad, los microservicios añaden superficie de ataque (más endpoints, más comunicación interna que proteger) pero también limitan el impacto de cada vulnerabilidad individual si están correctamente segmentados.

## Serverless

Proveedores cloud (AWS, GCP, Azure) ofrecen plataformas donde el código se ejecuta en respuesta a eventos, sin que el desarrollador tenga que aprovisionar ni gestionar servidores directamente — el proveedor se encarga del escalado, parcheo y disponibilidad de la infraestructura subyacente. Esto traslada parte de la responsabilidad de seguridad (a nivel de sistema operativo y red) al proveedor, pero la lógica de aplicación sigue siendo responsabilidad de quien la desarrolla, y sigue siendo susceptible a las mismas clases de vulnerabilidades (inyección, control de acceso roto, etc.).

## Por qué la arquitectura importa en una auditoría

Muchas vulnerabilidades no son errores de programación puntuales, sino **fallos de diseño**. Ejemplos típicos:

- Una aplicación implementa todas sus funciones de forma "segura" a nivel de código, pero **no implementa control de acceso basado en roles (RBAC)** a nivel de diseño — cualquier usuario autenticado puede invocar funciones administrativas porque nadie pensó en restringir esa capa.
- Tras comprometer un servidor de aplicación, no se encuentra la base de datos en la misma máquina — señal de que el diseño usa un modelo segmentado, lo que cambia por completo la estrategia de movimiento lateral necesaria para llegar a los datos.

Corregir un fallo de diseño suele ser mucho más costoso que corregir un bug de código, porque implica repensar cómo se relacionan los componentes entre sí — de ahí la importancia de incorporar seguridad desde las fases tempranas del diseño (*security by design*), y no solo como una capa de parches al final del desarrollo.
