---
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

# Gobuster y Seclists

La herramienta `Gobuster` esta no solo dedicada al descubrimiento de directorios mediante fuerza bruta lo que se le denomina `URIs`, si no, que tambien realiza un reconocimiento de `Subdominios DNS`, `Virtual Hosts Names` y `Open Amazon S3 buckets`.

URL = [Gobuster GitHub](https://github.com/OJ/gobuster)

Tendremos que instalar la herramienta ya que no viene por defecto.

```shell
sudo apt install gobuster
```

Para utilizar la herramienta y no limitarnos en tema de diccionarios de palabras, vamos a utilizar un repositorio donde englomera muchisimos diccionarios de palabras para lo que sea de diferentes tamaños y que es uno de los mas famosos que hay en `GitHub` llamado `SecLists`:

URL = [GitHub SecLists](https://github.com/danielmiessler/SecLists)

Podremos pasarnos todos esos diccionarios a nuestro `kali` instalando el `seclists` de la siguiente forma:

```shell
sudo apt install seclists
```

Ahora si nos vamos a la siguiente ruta, veremos que los tendremos ahi todos los diccionarios.

```
PATH = /usr/share/seclists/
```

Ahora para utilizar `gobuster` y ponerlo a prueba con nuestra maquina que instalamos anteriormente, lo haremos de la siguiente forma:

```shell
gobuster dir -u http://192.168.5.211:8080/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
```

Con el `dir` lo que hacemos es indicarle que queremos hacer fuerza bruta en `URLs`. Con el `-u` le indicamos la direccion `URL` en la que queremos realizar fuerza bruta, lo que haya despues de la `/`. Con el `-w` le indicamos el diccionario de palabras que queremos utilizar para esa fuerza bruta.

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.211:8080/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 301) [Size: 321] [--> http://192.168.5.211:8080/images/]
/documents            (Status: 301) [Size: 324] [--> http://192.168.5.211:8080/documents/]
/apps                 (Status: 301) [Size: 319] [--> http://192.168.5.211:8080/apps/]
/admin                (Status: 301) [Size: 320] [--> http://192.168.5.211:8080/admin/]
/portal               (Status: 200) [Size: 5396]
/db                   (Status: 301) [Size: 317] [--> http://192.168.5.211:8080/db/]
/bugs                 (Status: 200) [Size: 7858]
/js                   (Status: 301) [Size: 317] [--> http://192.168.5.211:8080/js/]
/message              (Status: 200) [Size: 28]
/robots               (Status: 200) [Size: 167]
/fonts                (Status: 301) [Size: 320] [--> http://192.168.5.211:8080/fonts/]
/666                  (Status: 200) [Size: 112]
/soap                 (Status: 301) [Size: 319] [--> http://192.168.5.211:8080/soap/]
/passwords            (Status: 301) [Size: 324] [--> http://192.168.5.211:8080/passwords/]
/stylesheets          (Status: 301) [Size: 326] [--> http://192.168.5.211:8080/stylesheets/]
Progress: 87664 / 87665 (100.00%)
===============================================================
Finished
===============================================================
```

Con esto lo que estamos viendo son directorios que ha descubierto en la pagina los cuales podremos recorrer para ver lo que parezcan mas interesantes.

Ahora si queremos buscar esas palabras pero tambien con extensiones por si encontrara algo con dicha extension seria de la siguiente forma:

```shell
 gobuster dir -u http://192.168.5.211:8080/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -x html,php,txt -t 100
```

Con el `-x` especificamos las extensiones de cada palabra para que se lo implemente. Con el `-t` especificamos los `hilos` que queremos que utilice para que vaya mas rapido.

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.211:8080/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/login.php            (Status: 200) [Size: 4013]
/security.php         (Status: 302) [Size: 0] [--> login.php]
/info.php             (Status: 200) [Size: 3426]
/documents            (Status: 301) [Size: 324] [--> http://192.168.5.211:8080/documents/]
/apps                 (Status: 301) [Size: 319] [--> http://192.168.5.211:8080/apps/]
/admin                (Status: 301) [Size: 320] [--> http://192.168.5.211:8080/admin/]
/training.php         (Status: 200) [Size: 3843]
/portal.php           (Status: 302) [Size: 0] [--> login.php]
/portal               (Status: 200) [Size: 5396]
/images               (Status: 301) [Size: 321] [--> http://192.168.5.211:8080/images/]
/index.php            (Status: 302) [Size: 0] [--> portal.php]
/test.php             (Status: 200) [Size: 0]
/credits.php          (Status: 302) [Size: 0] [--> login.php]
/install.php          (Status: 200) [Size: 2270]
/.php                 (Status: 403) [Size: 286]
/db                   (Status: 301) [Size: 317] [--> http://192.168.5.211:8080/db/]
/bugs.txt             (Status: 200) [Size: 7858]
/bugs                 (Status: 200) [Size: 7858]
/js                   (Status: 301) [Size: 317] [--> http://192.168.5.211:8080/js/]
/update.php           (Status: 200) [Size: 0]
/.html                (Status: 403) [Size: 287]
/message.txt          (Status: 200) [Size: 28]
/message              (Status: 200) [Size: 28]
/logout.php           (Status: 302) [Size: 0] [--> login.php]
/connect.php          (Status: 200) [Size: 0]
/robots.txt           (Status: 200) [Size: 167]
/robots               (Status: 200) [Size: 167]
/fonts                (Status: 301) [Size: 320] [--> http://192.168.5.211:8080/fonts/]
/666                  (Status: 200) [Size: 112]
/captcha.php          (Status: 302) [Size: 0] [--> login.php]
/soap                 (Status: 301) [Size: 319] [--> http://192.168.5.211:8080/soap/]
/passwords            (Status: 301) [Size: 324] [--> http://192.168.5.211:8080/passwords/]
/aim.php              (Status: 200) [Size: 9958]
/secret.php           (Status: 302) [Size: 0] [--> login.php]
/reset.php            (Status: 302) [Size: 0] [--> login.php]
/backdoor.php         (Status: 200) [Size: 333]
/lang_en.php          (Status: 200) [Size: 61]
/stylesheets          (Status: 301) [Size: 326] [--> http://192.168.5.211:8080/stylesheets/]
/.html                (Status: 403) [Size: 287]
/.php                 (Status: 403) [Size: 286]
/top_security.php     (Status: 200) [Size: 2208]
/phpinfo.php          (Status: 200) [Size: 78569]
/lang_fr.php          (Status: 200) [Size: 65]
/selections.php       (Status: 200) [Size: 0]
Progress: 350656 / 350660 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que ahora nos saco mucha mas informacion que antes, por lo que ya podremos explorar dichos directorios y archivos de la `URL`.
