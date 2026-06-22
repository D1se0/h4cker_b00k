---
icon: webhook
layout:
  width: default
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
  tags:
    visible: true
  actions:
    visible: true
---

# 01-protocolo-http

## El protocolo HTTP

### Qué es y para qué sirve

HTTP (_HyperText Transfer Protocol_) es el protocolo de nivel de aplicación que hace posible la World Wide Web. Cuando hablamos de "nivel de aplicación" nos referimos a que vive en la capa más alta del modelo de comunicación en red: por debajo de HTTP hay TCP/IP encargándose de que los paquetes lleguen a su destino, pero HTTP es el que define _qué se dice_ y _cómo se estructura_ la conversación entre un cliente y un servidor.

La palabra "hypertext" no es casualidad: el protocolo nació para transportar documentos que contienen enlaces a otros documentos, formando la "telaraña" (web) que conocemos. Cada vez que el navegador pide una página, una imagen, un script o cualquier recurso, lo hace mediante una petición HTTP.

El modelo es siempre el mismo: **cliente-servidor**. El cliente (un navegador, `curl`, una app móvil, un script en Python) inicia la comunicación pidiendo un recurso; el servidor lo procesa y devuelve una respuesta. Por defecto, HTTP usa el puerto **80**, aunque cualquier servidor puede configurarse para escuchar en otro puerto distinto (algo muy común al auditar aplicaciones desplegadas en entornos de pruebas o CTFs).

### La URL como puerta de entrada

Para pedir un recurso necesitamos identificarlo de forma única. Eso es lo que hace una URL (_Uniform Resource Locator_), construida sobre un FQDN (_Fully Qualified Domain Name_) como `www.ejemplo.com`.

Una URL se descompone en varias partes, y entender cada una es clave porque, como pentester, cada componente es una superficie potencial de ataque:

| Componente   | Ejemplo               | Qué hace                                                                                                                         |
| ------------ | --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Scheme       | `http://`, `https://` | Indica el protocolo. Termina en `://`.                                                                                           |
| User Info    | `admin:password@`     | Credenciales embebidas en la URL, separadas por `:` y terminadas en `@`. Históricamente usado para autenticación básica vía URL. |
| Host         | `ejemplo.com`         | Dominio o IP del servidor que aloja el recurso.                                                                                  |
| Port         | `:8080`               | Puerto TCP de escucha. Si se omite, se asume 80 (HTTP) o 443 (HTTPS).                                                            |
| Path         | `/panel/admin.php`    | Ruta al recurso concreto dentro del servidor.                                                                                    |
| Query String | `?id=5&debug=true`    | Parámetros enviados al servidor, empiezan con `?` y se separan con `&`.                                                          |
| Fragment     | `#seccion2`           | Procesado solo por el navegador, nunca llega al servidor. Sirve para saltar a una sección de la página.                          |

Solo el _scheme_ y el _host_ son estrictamente obligatorios; todo lo demás es opcional y depende del recurso al que se quiera acceder. Esta estructura es importante para un pentester porque la _query string_ y el _path_ son los puntos de entrada más habituales para probar inyecciones, manipular parámetros o descubrir rutas ocultas.

### Cómo se desarrolla una petición HTTP de principio a fin

Cuando escribes una URL en el navegador ocurre una secuencia de eventos que conviene tener clara:

1. **Resolución DNS**: el navegador necesita la IP asociada al dominio, así que consulta primero el archivo local `/etc/hosts` (en Linux/macOS) y, si no encuentra coincidencia, pregunta a un servidor DNS configurado en el sistema.
2. **Conexión TCP**: una vez se conoce la IP, el cliente establece una conexión TCP contra el puerto correspondiente (80 por defecto en HTTP).
3. **Envío de la petición**: el navegador envía una petición `GET` solicitando la ruta `/` (raíz) si no se especificó otra cosa.
4. **Procesamiento en el servidor**: el servidor recibe la petición, normalmente devuelve el archivo índice configurado (`index.html`, `index.php`, etc.).
5. **Respuesta**: el servidor responde con un código de estado (por ejemplo `200 OK`) y el contenido solicitado.
6. **Renderizado**: el navegador interpreta el HTML/CSS/JS recibido y lo muestra.

Como pentester, este flujo es relevante porque el archivo `/etc/hosts` puede usarse manualmente para forzar la resolución de un dominio hacia una IP concreta —algo muy habitual en laboratorios y CTFs donde se trabaja con _virtual hosts_ que no están publicados en DNS público. Basta con añadir una línea con el formato `IP nombre_de_dominio` a ese archivo.

### `curl`: la navaja suiza del pentester web

Mientras que un navegador interpreta y renderiza HTML/CSS/JS, **`curl`** (_Client URL_) es una herramienta de línea de comandos que envía la petición y muestra la respuesta en crudo, sin procesarla. Esto la convierte en la herramienta ideal para pentesting, scripting y automatización: es rápida, scriptable y no introduce ningún comportamiento añadido por el navegador (como ejecutar JavaScript).

#### Petición básica

```bash
curl http://ejemplo.com
```

Esto envía una petición GET y vuelca el cuerpo de la respuesta (normalmente HTML) directamente en la terminal, tal cual lo envía el servidor.

#### Guardar la respuesta en un archivo

```bash
curl -O http://ejemplo.com/index.html   # guarda con el nombre remoto
curl -o salida.html http://ejemplo.com/ # guarda con nombre propio
```

`-O` (mayúscula) conserva el nombre de archivo remoto; `-o` (minúscula) permite elegir el nombre local.

#### Modo silencioso

Por defecto, `curl` imprime una barra de progreso y estadísticas de transferencia. En scripts esto es ruido innecesario:

```bash
curl -s -O http://ejemplo.com/index.html
```

#### Consultar la ayuda

```bash
curl -h          # ayuda resumida
curl --help all   # ayuda completa
man curl          # manual completo
```

### Por qué esto importa en una auditoría

Dominar `curl` desde el primer momento tiene una razón práctica: en una auditoría real (o en un CTF) no siempre vamos a tener un navegador disponible, y aunque lo tengamos, automatizar peticiones repetitivas (probar 50 payloads distintos, por ejemplo) es mucho más rápido desde la terminal. Además, `curl` no ejecuta JavaScript ni aplica ninguna lógica de "protección" del lado del cliente, por lo que vemos exactamente lo que el servidor envía, sin filtros añadidos por el navegador.

> **Ejemplo de caso real**: una aplicación puede exponer un endpoint como `/download.php` que no está enlazado desde ninguna parte visible de la web, pero que sigue siendo accesible directamente. Un escaneo de directorios (que veremos en el bloque de _Web Fuzzing_) descubre esa ruta, y con un simple `curl http://objetivo/download.php` podemos comprobar qué devuelve sin necesidad de interactuar con la interfaz gráfica.
