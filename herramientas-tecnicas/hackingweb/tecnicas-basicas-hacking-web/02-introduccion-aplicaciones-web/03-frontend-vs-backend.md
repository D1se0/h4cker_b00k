# Front End vs. Back End

## La frontera entre lo que ve el cliente y lo que procesa el servidor

El desarrollo web suele dividirse en dos grandes disciplinas —frontend y backend— que, combinadas, forman el llamado desarrollo *full stack*. Comprender exactamente dónde está la frontera entre ambos es fundamental en pentesting, porque determina qué se puede inspeccionar libremente (todo el frontend, sin restricciones) y qué permanece oculto salvo que se logre acceso al servidor o se filtre de alguna forma (el backend).

## Front End

El frontend incluye todo lo que llega literalmente al navegador del cliente: HTML, CSS y JavaScript. Esto comprende el diseño visual (UI), la experiencia de usuario (UX), y toda la lógica que se ejecuta en el propio navegador.

Una característica clave: el código frontend debe funcionar de forma uniforme en **cualquier dispositivo, navegador y tamaño de pantalla**, a diferencia del backend, que normalmente se desarrolla para una plataforma o sistema operativo concreto.

### Implicación de seguridad fundamental

**Todo el código frontend es visible y manipulable por el cliente.** Esto incluye cualquier validación de formularios escrita en JavaScript, cualquier lógica de "ocultar" un botón según el rol del usuario, o cualquier comprobación que se haga exclusivamente en el navegador. Si la única barrera entre un usuario normal y una acción administrativa es una comprobación en JavaScript del lado del cliente, esa barrera es trivialmente evitable: basta con interactuar directamente con el endpoint del backend (vía `curl`, un proxy de intercepción, o la consola del navegador), sin pasar por la interfaz que oculta el botón.

> **Regla de oro**: cualquier validación o control de seguridad debe aplicarse siempre en el backend. Las validaciones en frontend son una mejora de experiencia de usuario (feedback inmediato sin esperar al servidor), nunca un mecanismo de seguridad real.

## Back End

El backend gestiona toda la funcionalidad "de verdad" de la aplicación: procesa peticiones, ejecuta lógica de negocio, interactúa con la base de datos, y devuelve una respuesta. Sin backend, una "aplicación web" no sería más que una colección de páginas estáticas sin ninguna interactividad real.

Se compone, típicamente, de cuatro elementos:

| Componente | Descripción |
|---|---|
| **Servidores backend** | El hardware/SO que aloja todo lo demás (Linux, Windows, o contenedores). |
| **Servidores web** | Gestionan las conexiones y peticiones HTTP (Apache, Nginx, IIS). |
| **Bases de datos** | Almacenan y recuperan los datos (MySQL, PostgreSQL, MongoDB, etc.). |
| **Frameworks de desarrollo** | El esqueleto sobre el que se construye la lógica de negocio (Laravel, Django, Express, ASP.NET, Spring). |

Cada uno de estos componentes puede aislarse en su propio servidor o contenedor (por ejemplo, usando Docker) para limitar el impacto si uno de ellos se ve comprometido — una práctica de segmentación que conecta directamente con lo visto en el apartado de arquitectura.

## Auditando frontend vs. backend: caja blanca y caja negra

| Aspecto | Frontend | Backend |
|---|---|---|
| Visibilidad | Total — código fuente accesible directamente desde el navegador | Ninguna por defecto — solo se observa el comportamiento externo |
| Tipo de pruebas típicas | Revisión de código (caja blanca) | Caja negra, salvo acceso al código fuente |

Cuando la aplicación es de código abierto, también es posible auditar el backend en modo caja blanca, descargando y revisando el código fuente directamente. Y ciertas vulnerabilidades —como la **inclusión de archivos locales (LFI)**, que veremos en detalle más adelante— pueden usarse precisamente para filtrar código fuente del backend desde fuera, abriendo la puerta a un análisis de caja blanca improvisado incluso en aplicaciones cerradas.

## Errores de desarrollo más comunes (y relevantes para un pentester)

Algunos de los fallos que con más frecuencia introducen los equipos de desarrollo, y que constituyen el caldo de cultivo de las vulnerabilidades del Top 10 de OWASP:

- Permitir que datos no validados lleguen a la base de datos.
- Implementar mecanismos de seguridad propios en lugar de usar librerías probadas y mantenidas.
- Tratar la seguridad como el último paso del desarrollo, en lugar de integrarla desde el diseño.
- Almacenar contraseñas en texto plano (o con algoritmos de hash débiles/sin *salt*).
- Confiar excesivamente en validaciones del lado del cliente.
- Permitir el paso de variables a través del *path* de la URL sin sanitización.
- Confiar ciegamente en código de terceros (dependencias, librerías, plugins) sin revisar su seguridad.
- Dejar credenciales o claves de acceso ("backdoors") hardcodeadas en el código.
- No validar/filtrar entradas que acaban en consultas SQL (inyección SQL).
- Permitir inclusión de archivos remotos sin restricción.
- No cifrar correctamente datos sensibles en tránsito o en reposo.

Estos errores son precisamente la base de las **10 vulnerabilidades principales de OWASP** (Control de acceso roto, Fallos criptográficos, Inyección, Diseño inseguro, Configuración de seguridad incorrecta, Componentes vulnerables, Fallos de identificación y autenticación, Fallos de integridad de software y datos, Fallos de registro y monitorización, y SSRF), que iremos viendo en detalle a lo largo de los siguientes bloques. Familiarizarse con esta lista desde el principio ayuda a contextualizar por qué cada técnica concreta que se estudia más adelante importa en el panorama general.
