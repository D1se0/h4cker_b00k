---
icon: right-left
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

# IDOR (Insecure Direct Object Reference)

## Practica de explotación `IDOR`

Vamos a poner que tenemos la siguiente pagina web:

> reset\_password.php

```php
<?php
$usersFile = 'users.txt';

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $username = $_POST['username'];
    $newPassword = $_POST['password'];

    if (file_exists($usersFile)) {
        $users = file($usersFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        $updated = false;
        foreach ($users as $index => $line) {
            list($user, $pass) = explode(":", trim($line));
            if ($user === $username) {
                $users[$index] = "$user:$newPassword";
                $updated = true;
            }
        }

        // Si se actualizó la contraseña en el archivo, se guarda y, si el usuario es 'carlos', se cambia la contraseña a nivel de sistema
        if ($updated) {
            file_put_contents($usersFile, implode("\n", $users));

            // Si el usuario es 'carlos', cambiar la contraseña a nivel de sistema
            if ($username === 'carlos') {
                // Ejecutamos el comando 'passwd' en el sistema para cambiar la contraseña del usuario 'carlos'
                $command = "echo 'carlos:$newPassword' | sudo chpasswd";
                exec($command, $output, $return_var);

                if ($return_var === 0) {
                    echo "<p class='success'>La contraseña para el usuario <strong>$username</strong> se ha cambiado correctamente.</p>";
                } else {
                    echo "<p class='error'>Hubo un error al intentar cambiar la contraseña a nivel del sistema.</p>";
                }
            } else {
                echo "<p class='success'>La contraseña para el usuario <strong>$username</strong> se ha cambiado correctamente.</p>";
            }
        } else {
            echo "<p class='error'>El usuario <strong>$username</strong> no existe.</p>";
        }
    } else {
        echo "<p class='error'>No se encontró la base de datos de usuarios.</p>";
    }
} else {
    $token = isset($_GET["temp-forgot-password-token"]) ? $_GET["temp-forgot-password-token"] : "";
    $username = isset($_GET["username"]) ? $_GET["username"] : "";
?>
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Restablecer Contraseña</title>
        <style>
            // <!-- STYLE_PAGE -->
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Restablecer tu contraseña</h2>
            <form action="reset_password.php?temp-forgot-password-token=<?php echo htmlspecialchars($token); ?>" method="post">
                <input type="hidden" name="username" value="<?php echo htmlspecialchars($username); ?>">

                <label for="password">Nueva Contraseña:</label>
                <input type="password" name="password" id="password" required>

                <input type="submit" value="Restablecer">
            </form>
        </div>
    </body>
    </html>
<?php
}
?>
```

> send\_password.php

```php
<?php
$usersFile = 'users.txt';
$message = ""; // Variable para mostrar mensajes de éxito o error

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Validar si la contraseña actual es correcta
    $isValidUser = false;

    if (file_exists($usersFile)) {
        $users = file($usersFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($users as $line) {
            list($user, $pass) = explode(":", trim($line));
            if ($user === $username && $pass === $password) {
                $isValidUser = true;
                break;
            }
        }
    }

    if ($isValidUser) {
        // Token dummy que no se valida posteriormente
        $token = "ABC123";
        $message = "<p class='success'>Se ha enviado un correo de restablecimiento (simulado).</p>";
        $message .= "<p>Contenido del correo: </p>";
        $message .= "<a href='reset_password.php?temp-forgot-password-token={$token}&username=" . urlencode($username) . "' class='link-reset'>Restablecer tu contraseña</a>";
    } else {
        $message = "<p class='error'>La contraseña actual es incorrecta.</p>";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enviar Restablecimiento de Contraseña</title>
    <style>
        // <!-- STYLE_PAGE -->
    </style>
</head>
<body>
    <div class="container">
        <h2>Enviar Correo de Restablecimiento</h2>

        <!-- Si hay mensajes (error o éxito), los mostramos -->
        <?php if ($message): ?>
            <div class="message-container">
                <?php echo $message; ?>
            </div>
        <?php else: ?>
            <!-- Formulario solo se muestra si no se ha enviado una solicitud -->
            <form action="send_reset.php" method="post">
                <label for="username">Usuario:</label>
                <input type="text" name="username" id="username" required>

                <label for="password">Contraseña Actual:</label>
                <input type="password" name="password" id="password" required>

                <input type="submit" value="Enviar Correo de Restablecimiento">
            </form>
        <?php endif; ?>

        <p class="back-link"><a href="login.php">¿Ya tienes cuenta? Inicia sesión</a></p>
    </div>
</body>
</html>
```

Vemos que en estos `2` archivos no valida que el usuario sea el legitimo a nivel de peticion, por lo que si se modifica alguna peticion con otra informacion, el servidor no lo valida y confia en lo que le llegue por lo que podremos cambiar la `password` del usuario `admin`.

Estando dentro de la pagina le daremos a `¿Olvidaste tu contraseña?` con las credenciales por defecto que viene en la pagina `user:user` poniendo eso, veremos que entraremos en una apartado en el que tendremos que poner la nueva contraseña para dicho usuario, pero en esta parte abriremos `BurpSuite` y capturaremos la peticion del cambio de contraseña, viendo algo asi:

```
POST /reset_password.php?temp-forgot-password-token=ABC123 HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 28
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/reset_password.php?temp-forgot-password-token=ABC123&username=user
Cookie: PHPSESSID=c81glfe7e77ol15a1ipcu83tfd
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=user&password=user1
```

Veremos que hay `2` campos, uno que es para el usuario y otro para la contraseña, el que nos interesa es el del usuario, cambiaremos `user` por `admin` para que se le cambie la contraseña a `admin`, enviaremos dicha peticion modificada y si volvemos a la pagina veremos lo siguiente:

```
La contraseña para el usuario admin se ha cambiado correctamente.
```

Ahora si probamos a iniciar sesion con el usuario `admin` veremos que nos deja, por lo que habremos aprovechado dicha vulnerabilidad.

## Explicación detallada `IDOR`

### **Vulnerabilidad IDOR (Insecure Direct Object Reference)**

#### **¿Qué es IDOR?**

**IDOR (Insecure Direct Object Reference)** es una vulnerabilidad de control de acceso que ocurre cuando un usuario puede acceder directamente a recursos o datos que no deberían estar disponibles para él, debido a la falta de validación adecuada en el backend.

El problema surge cuando una aplicación expone identificadores de objetos en la URL o en los parámetros de solicitud, permitiendo que un atacante modifique estos valores y acceda a información de otros usuarios sin la autorización adecuada.

***

### **Ejemplo de IDOR**

#### **Escenario Vulnerable**

Imagina un sistema de tickets de soporte donde cada usuario puede ver sus propias solicitudes de ayuda accediendo a una URL como esta:

```bash
https://soporte.com/ticket?id=1234
```

Si el usuario cambia manualmente el ID en la URL por otro número, como:

```bash
https://soporte.com/ticket?id=1235
```

Y obtiene acceso a un ticket que no le pertenece, entonces la aplicación es vulnerable a **IDOR** porque no verifica si el usuario tiene permisos para ver ese recurso.

***

### **Impactos de la vulnerabilidad IDOR**

1. **Fuga de información confidencial:** Un atacante puede acceder a datos privados de otros usuarios, como correos electrónicos, direcciones, facturas o documentos sensibles.
2. **Modificación de datos ajenos:** Si el IDOR no solo permite leer información, sino también modificarla, un atacante podría cambiar contraseñas, modificar registros o eliminar información crítica.
3. **Escalada de privilegios:** En algunos casos, si el atacante tiene acceso a identificadores de recursos administrativos, podría modificar su cuenta y obtener privilegios más altos.
4. **Robo de identidad y fraude:** Al acceder a datos personales, un atacante podría suplantar la identidad de otros usuarios o cometer fraudes financieros.

***

### **Payloads y Bypasses para IDOR**

Aquí tienes una tabla con ejemplos de **payloads y técnicas de bypass** utilizadas para explotar esta vulnerabilidad:

| **Descripción**                      | **Payload/Bypass**                                                              | **Explicación**                                                                       |
| ------------------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Cambio de ID en la URL**           | `https://web.com/perfil?id=1000` → `id=1001`                                    | Se cambia el ID manualmente en la URL para acceder a la cuenta de otro usuario.       |
| **Manipulación en parámetros POST**  | `id=1000` → `id=1001` en el cuerpo de una petición POST                         | Si el ID es enviado en una solicitud POST, se puede modificar en el request.          |
| **Cambio de ID en encabezados HTTP** | `X-User-ID: 1000` → `X-User-ID: 1001`                                           | Algunas aplicaciones usan encabezados personalizados para identificar usuarios.       |
| **Uso de técnicas de enumeración**   | `id=1`, `id=2`, `id=3`, `id=4`...                                               | Se prueban IDs secuenciales para encontrar datos expuestos.                           |
| **ID codificado en Base64**          | `id=MTIzNA==` (Base64 de 1234) → `MTIzNQ==` (1235)                              | Si los IDs están en Base64, se pueden decodificar, modificar y volver a codificar.    |
| **Uso de parámetros secundarios**    | `id=1000&role=admin`                                                            | Algunos sistemas permiten modificar roles o permisos mediante parámetros.             |
| **Cambio de método HTTP**            | `GET /user/1000` → `POST /user/1000`                                            | Si la API no valida correctamente el método HTTP, un atacante podría modificar datos. |
| **Sustitución de token de usuario**  | `Authorization: Bearer TOKEN1234` → `TOKEN1235`                                 | Si el token se basa en un identificador predecible, puede ser reemplazado.            |
| **Cambio en cookies**                | `userID=1000` → `userID=1001`                                                   | Algunas aplicaciones guardan el ID del usuario en cookies sin validación.             |
| **Uso de GraphQL**                   | `{ user(id: "1000") { name, email } }` → `{ user(id: "1001") { name, email } }` | GraphQL puede permitir acceso a datos no autorizados si no se valida correctamente.   |

***

### **Cómo prevenir la vulnerabilidad IDOR**

Para evitar esta vulnerabilidad, se deben implementar controles de acceso adecuados en el backend y evitar confiar en los datos enviados por el cliente.

#### **1. Validación de permisos en el servidor**

Nunca confíes en los datos proporcionados por el usuario. Antes de devolver información, verifica si el usuario tiene permiso para acceder a ese recurso.

**Ejemplo en PHP:**

```php
session_start();
$userId = $_SESSION['user_id'];
$requestedId = $_GET['id'];

$query = "SELECT * FROM tickets WHERE id = ? AND user_id = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param("ii", $requestedId, $userId);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows == 0) {
    die("Acceso denegado.");
}
```

#### **2. Uso de identificadores aleatorios y UUIDs**

Evita usar identificadores predecibles como números secuenciales. En su lugar, utiliza identificadores aleatorios o UUIDs:

```python
import uuid
user_id = uuid.uuid4()  # Genera un identificador aleatorio
```

#### **3. Autenticación y autorización adecuadas**

* Implementa control de acceso basado en roles (RBAC).
* Usa tokens de sesión seguros para identificar usuarios.
* Restringe el acceso a recursos mediante políticas en el backend.

#### **4. Registros y monitoreo**

* Registra intentos sospechosos de acceso a recursos.
* Implementa alertas cuando un usuario acceda a demasiados recursos en un corto periodo de tiempo.

#### **5. Protección en API REST y GraphQL**

* Usa middleware de autenticación para verificar cada solicitud.
* Implementa reglas de acceso a nivel de API para cada endpoint.

***

### **Conclusión**

La vulnerabilidad **IDOR** es una de las fallas más comunes y peligrosas en aplicaciones web. Si una aplicación no valida correctamente los permisos antes de otorgar acceso a un recurso, un atacante puede aprovecharse de esta falla para obtener información sensible, modificar datos o incluso escalar privilegios.

Para mitigar esta vulnerabilidad, es crucial validar los permisos en el servidor, utilizar identificadores aleatorios, implementar controles de acceso y monitorear actividades sospechosas.
