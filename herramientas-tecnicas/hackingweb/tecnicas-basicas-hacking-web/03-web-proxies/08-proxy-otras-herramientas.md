# Proxificando otras herramientas

## Más allá del navegador

El proxy de intercepción no está limitado a tráfico generado por un navegador. Cualquier herramienta de línea de comandos, script, o aplicación de escritorio que realice peticiones HTTP puede enrutarse a través de Burp o ZAP, permitiendo inspeccionar exactamente qué envían y reciben — algo especialmente valioso al depurar exploits propios, módulos de Metasploit, o herramientas de terceros cuyo comportamiento interno no está documentado con claridad.

> **Nota de rendimiento**: enrutar tráfico a través de un proxy de intercepción introduce latencia notable. Conviene activarlo solo mientras se necesita investigar, no como configuración permanente para uso normal de las herramientas.

## proxychains

[`proxychains`](https://github.com/haad/proxychains) es una utilidad de Linux que fuerza el tráfico de red de cualquier herramienta de línea de comandos a través de un proxy especificado, sin que la herramienta necesite soporte nativo de proxy.

### Configuración

Editar `/etc/proxychains.conf`, comentar la línea por defecto (normalmente SOCKS) y añadir:

```
http 127.0.0.1 8080
```

### Uso

```bash
proxychains -q curl http://10.10.10.5
```

El flag `-q` activa el modo silencioso, suprimiendo los mensajes de estado de conexión de `proxychains` en la terminal, dejando solo la salida de la herramienta proxificada. Tras ejecutar el comando, la petición debería aparecer en el historial del proxy web, confirmando que el enrutamiento funciona correctamente.

Esta técnica funciona con prácticamente cualquier herramienta de línea de comandos: escáneres, scripts personalizados, clientes HTTP alternativos, etc.

## Metasploit

Los módulos de Metasploit también pueden enrutarse a través de un proxy, lo cual resulta muy útil para depurar exactamente qué petición está enviando un módulo concreto, o para verificar manualmente una respuesta antes de confiar en el resultado reportado por el propio módulo.

```bash
msfconsole

msf6 > use auxiliary/scanner/http/robots_txt
msf6 auxiliary(scanner/http/robots_txt) > set PROXIES HTTP:127.0.0.1:8080
msf6 auxiliary(scanner/http/robots_txt) > set RHOST 10.10.10.5
msf6 auxiliary(scanner/http/robots_txt) > set RPORT 80
msf6 auxiliary(scanner/http/robots_txt) > run
```

Tras la ejecución, el historial del proxy debería mostrar la(s) petición(es) realizadas por el módulo, permitiendo inspeccionar cabeceras, método, cuerpo y la respuesta completa del servidor — información que la salida resumida de Metasploit en consola no siempre expone con el mismo nivel de detalle.

## Por qué esta capacidad es tan valiosa

Más allá de la comodidad de depuración, proxificar herramientas externas tiene una utilidad estratégica: permite **verificar de forma independiente** lo que una herramienta automatizada afirma estar haciendo. Es una buena práctica de auditoría no confiar ciegamente en el resultado reportado por un escáner o exploit sin haber observado al menos una vez la petición y respuesta reales — los falsos positivos y falsos negativos son comunes en herramientas automatizadas, y tener la capacidad de inspeccionar el tráfico subyacente es la forma más fiable de confirmarlos o descartarlos.
