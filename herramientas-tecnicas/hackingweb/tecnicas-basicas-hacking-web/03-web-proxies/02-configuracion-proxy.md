# Configuración del proxy y certificados

## Navegador preconfigurado vs. navegador propio

Tanto Burp como ZAP incluyen un **navegador preconfigurado** (basado en Chromium o Firefox respectivamente) con el proxy y el certificado CA ya instalados, lo que permite empezar a interceptar tráfico de inmediato sin configuración manual. Para la mayoría de tareas exploratorias, este navegador integrado es suficiente.

- **Burp**: `Proxy > Intercept > Open Browser`
- **ZAP**: icono del navegador en la barra superior

## Configurando un navegador propio (Firefox)

En auditorías más prolongadas suele preferirse usar el navegador habitual (con extensiones propias, sesiones guardadas, etc.). Para ello hay que apuntar manualmente el proxy de Firefox hacia el puerto de escucha de la herramienta (por defecto, `8080` en ambas):

1. Ir a las preferencias de proxy de Firefox y configurar un proxy manual `127.0.0.1:8080`.
2. Alternativamente, instalar la extensión **FoxyProxy**, que permite alternar rápidamente entre distintos perfiles de proxy con un clic, sin tener que editar las preferencias cada vez.

```
IP: 127.0.0.1
Puerto: 8080
Nombre: Burp / ZAP
```

> Si el puerto 8080 ya está en uso por otro proceso, la herramienta no podrá iniciar el listener y mostrará un error — se puede cambiar el puerto de escucha en `Proxy > Proxy settings > Proxy listeners` (Burp) o `Tools > Options > Network > Local Servers/Proxies` (ZAP), asegurándose de que el navegador apunte al mismo puerto elegido.

## Instalación del certificado CA

Cuando se intercepta tráfico HTTPS, el proxy necesita "romper" el cifrado extremo a extremo para poder leer y modificar el contenido: actúa generando un certificado propio sobre la marcha para cada dominio visitado, firmado por su propia autoridad certificadora (CA) interna. Para que el navegador confíe en esos certificados sin mostrar advertencias de seguridad en cada petición HTTPS, hay que **importar el certificado CA del proxy** como una autoridad de confianza.

### Burp

1. Con Burp seleccionado como proxy activo, navegar a `http://burp` desde el navegador.
2. Descargar el certificado haciendo clic en **CA Certificate**.

### ZAP

1. `Tools > Options > Network > Server Certificates`.
2. Clic en **Save** para exportar el certificado actual (o **Generate** para crear uno nuevo).

### Importar en Firefox

1. Ir a `about:preferences#privacy`, desplazarse hasta el final y clicar **View Certificates**.
2. Pestaña **Authorities** → **Import** → seleccionar el archivo de certificado descargado.
3. Marcar **Trust this CA to identify websites** (y opcionalmente, identificar usuarios de correo) → **Aceptar**.

Una vez instalado el certificado y configurado el proxy, todo el tráfico de ese navegador —HTTP y HTTPS— se enrutará a través de la herramienta elegida, lista para ser interceptado y analizado.

> **Nota de seguridad operativa**: instalar un certificado CA de confianza en el sistema es, en esencia, habilitar deliberadamente un MitM sobre el propio tráfico. Es perfectamente seguro hacerlo en un entorno de pruebas controlado por uno mismo, pero conviene desinstalar el certificado (o usar un perfil de navegador dedicado solo a pentesting) cuando ya no se necesite, para no dejar esa confianza activada de forma permanente.
