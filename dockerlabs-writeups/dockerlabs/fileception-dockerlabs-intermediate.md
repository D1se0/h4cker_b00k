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

# Fileception DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip fileception.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh fileception.tar
```

Info:

```
Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-24 06:38 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000028s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 172.17.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rwxrw-rw-    1 ftp      ftp         75372 Apr 27 02:17 hello_peter.jpg [NSE: writeable]
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 61:8f:91:89:a7:0b:8e:17:b7:dd:38:e0:00:04:59:47 (ECDSA)
|_  256 8a:15:29:13:ec:aa:f6:20:ca:c8:80:14:56:05:ec:3b (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.83 seconds
```

Vemos que hay un `FTP` que permite el login de `anonymous` por lo que haremos lo siguiente.

## FTP

```shell
ftp anonymous@<IP>
```

Una vez dentro veremos lo siguiente.

```
dr-xr-xr-x    1 ftp      ftp          4096 Apr 27 02:19 .
dr-xr-xr-x    1 ftp      ftp          4096 Apr 27 02:19 ..
-rwxrw-rw-    1 ftp      ftp         75372 Apr 27 02:17 hello_peter.jpg
```

Por lo que nos lo descargamos de la siguiente forma.

```shell
get hello_peter.jpg
```

Una vez hecho esto nos salimos y si intentamos extraer datos no servira de mucho, por lo que lo dejaremos aparcado.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 11137]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que no hay gran cosa.

Pero si inspeccionamos la pagina de `apache2` veremos lo siguiente.

```html
<!-- 
¡Hola, Peter!

¿Te acuerdas los libros que te presté de esteganografía? ¿A que estaban buenísimos?

Aquí te dejo una clave que usaras sabiamente en el momento justo. Por favor, no seas tan obvio, la vida no se trata de fuerza bruta.

@UX=h?T9oMA7]7hA7]:YE+*g/GAhM4

Solo te comento, recuerdo que usé este método porque casi nadie lo usa... o si. Lamentablemente, a mi también se me olvido. Solo recuerdo que era base
-->
```

Vemos que esta en `Base85` que decodificado diria lo siguiente:

```
base_85_decoded_password
```

Vemos que puede ser una contraseña para extraer datos de la imagen de la siguiente forma.

## Steghide

```shell
steghide extract -sf hello_peter.jpg
```

Info:

```
Enter passphrase: 
wrote extracted data to "you_find_me.txt".
```

Vemos que nos extrae un archivo que si lo leemos pone lo siguiente.

```
Hola, Peter!

Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook! Ook?  Ook. Ook?  Ook. Ook.  Ook. Ook?  Ook. Ook.  Ook. Ook. 
Ook. Ook.  Ook. Ook?  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook?  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.
Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook? Ook.  Ook? Ook.  Ook? Ook.  Ook? Ook.  Ook! Ook!  Ook? Ook!  Ook. Ook?  Ook. Ook?  Ook. Ook?  Ook! Ook!  Ook! Ook!  Ook! Ook
!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook.  Ook. Ook?  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Oo
k.  Ook! Ook.  Ook? Ook.  Ook! Ook!  Ook! Ook.  Ook! Ook.  Ook. Ook.  Ook! Ook.  Ook. Ook?  Ook! Ook.  Ook? Ook.  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! Ook!  Ook! O
ok!  Ook! Ook!  Ook! Ook.  Ook. Ook.  Ook! Ook.  Ook. Ook?  Ook! Ook.  Ook! Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. Ook.  Ook. 
Ook.  Ook. Ook.  Ook. Ook.  Ook! Ook.  Ook! Ook.  Ook? Ook.  Ook! Ook!  Ook! Ook.  Ook. Ook.  Ook! Ook.
```

Pone este texto que esta codificado en `Brainfuck` decodificado diria lo siguiente.

```
9h889h23hhss2
```

Esto puede ser la contraseña de `peter` para el `ssh`.

## SSH

```shell
ssh peter@<IP>
```

Si metemos esa contraseña estaremos dentro y si leemos el mensaje que hay en la `/home`.

## Escalate user octopus

```shell
cat nota_importante.txt
```

Info:

```
NO REINICIES EL SISTEMA!!

HAY UN ARCHIVO IMPORTANTE EN TMP
```

Por lo que nos iremos a `/tmp`.

```
total 28
drwxrwxrwt 1 root   root    4096 Aug 24 12:34 .
drwxr-xr-x 1 root   root    4096 Aug 24 12:34 ..
-rw-r--r-- 1 ubuntu ubuntu 14558 Apr 27 03:38 importante_octopus.odt
-rw-r--r-- 1 root   root     114 Apr 27 02:20 recuerdos_del_sysadmin.txt
```

Si leemos `recuerdos_del_sysadmin.txt` veremos lo siguiente.

```
Cuando era niño recuerdo que, a los videos, para pasarlos de flv a mp4, solo cambiaba la extensión. Que iluso.
```

Como no podemos hacer mucho con ese archivo en la maquina nos la pasaremos a nuestro equipo host.

```shell
python3 -m http.server 7777
```

abrimos un servidor de `python3` y desde el host nos lo descargamos.

```shell
wget http://<IP>:7777/importante_octopus.odt
```

Una vez hecho esto paramos el servidor de `python3` y ya lo tendriamos en nuestro host.

Si lo pasamos de `.odt` a `.zip` veremos que funciona y que descomprime muchas cosas.

### unzip

```shell
mv importante_octopus.odt importante_octopus.zip
```

Si lo descomprimimos.

```shell
unzip importante_octopus.zip
```

Info:

```
Archive:  importante_octopus.zip
   creating: Configurations2/accelerator/
   creating: Configurations2/floater/
   creating: Configurations2/images/Bitmaps/
   creating: Configurations2/menubar/
   creating: Configurations2/popupmenu/
   creating: Configurations2/progressbar/
   creating: Configurations2/statusbar/
   creating: Configurations2/toolbar/
   creating: Configurations2/toolpanel/
  inflating: META-INF/manifest.xml   
 extracting: Thumbnails/thumbnail.png  
  inflating: content.xml             
  inflating: leerme.xml              
  inflating: manifest.rdf            
  inflating: meta.xml                
 extracting: mimetype                
  inflating: settings.xml            
  inflating: styles.xml 
```

Si leemos el archivo `leerme.xml` veremos lo siguiente:

```
Decirle a Peter que me pase el odt de mis anécdotas, en caso de que se me olviden mis credenciales de administrador... Él no sabe de Esteganografía, nunca sé lo imaginaria esto.

usuario: octopus
password: ODBoMjM4MGgzNHVvdW8zaDQ=
```

Por lo que vemos esa es la contraseña del usuario `octopus` en `Base64` que decodificado es lo siguiente.

```
80h2380h34uouo3h4
```

Si nos vamos al `ssh` de nuevo y cambiamos al usuario `octopus` veremos que funciona.

```shell
su octopus
```

## Escalate Privilege

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for octopus on e12e56f13138:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User octopus may run the following commands on e12e56f13138:
    (ALL) NOPASSWD: ALL
    (ALL : ALL) ALL
```

Por lo que podremos hacer `sudo su` para ser directamente `root`.

```shell
sudo su
```

Metemos la contraseña y ya seremos `root`.
