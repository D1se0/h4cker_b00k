---
icon: pineapple
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

# Hacking WiFi (Wifi Pineapple Mark VII)

## Introducción

Vamos a ver como podriamos con un `WiFi Pineapple Mark VII` poder capturar el `Handshake` de una red wifi y posteriormente desde un `Kali` crackear dicho `Handshake` para poder obtener la contraseña del wifi en cuestion.

## Creación WiFi de testeo

En primero lugar vamos a crearnos una red wifi propia para simular todo este ataque y tenerlo en un entorno controlado, primero crearemos ese `AP` desde nuestro `WiFi Pineapple` asignandole alguna contraseña debil.

<figure><img src="../../.gitbook/assets/Pasted image 20251220194845.png" alt=""><figcaption></figcaption></figure>

Le daremos al boton `Enable` para que este activa esta red `WiFi` y posteriormente le daremos a `Save` para guardar los cambios tal cual se ven en la captura.

## Escaneo de redes wifi

Despues nos iremos a un apartado donde podremos realizar un escaneo de redes.

<figure><img src="../../.gitbook/assets/Pasted image 20251220195038.png" alt=""><figcaption></figcaption></figure>

Dentro de esta seccion vamos a `habilitar` la opcion de `Scan` para que empiece el escaneo, pero antes seleccionaremos la opcion llamada `Continuous` para que este continuamente escaneando redes y asi nos aparezcan los `SSID` junto a la demas informacion, seleccionando la red wifi que queremos `hackear` en mi caso la llamada `WIFI_DISEO`...

<figure><img src="../../.gitbook/assets/Pasted image 20251220195056.png" alt=""><figcaption></figcaption></figure>

Veremos que se nos despliega una serie de opciones, vamos a seleccionar el boton llamado `Deauthenticate All Clients`, pero antes de darle a este boton le daremos al llamado `Capture WPA Handshakes` para que este a la escucha de dicha captura.

<figure><img src="../../.gitbook/assets/Pasted image 20251220195241.png" alt=""><figcaption></figcaption></figure>

## Captura de Handshake de WIFI\_DISEO

Una vez teniendolo activo, ahora si le daremos al boton `Deauthenticate All Clients` para que cualquier cliente que este en dicha red wifi le expulse y esto lo que hara sera que el dispositivo se conecte de forma automatica a la misma red wifi forzando asi una captura de `Handshake`, echo esto, al rato podremos ver esta notificacion.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-20 1951017.png" alt=""><figcaption></figcaption></figure>

Significa que hemos capturado un `Handshake` de alguna red wifi, si entramos dentro del apartado de `Handshakes` capturados...

> Archivo PCAP (Full)

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-20 1957281.png" alt=""><figcaption></figcaption></figure>

> Archivo Hashcat (Full)

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-20 2001019.png" alt=""><figcaption></figcaption></figure>

Veremos que podemos tener `2` tipos junto con su `BSSID` que corresponde a la del `WIFI_DISEO`, estos tipos se pueden clasificar en un formato de `.pcap` para examinarlo con `wireshark` o en formato `hashcat` para poder crackear el `hash` directamente con la herramienta `hashcat`, en este caso la mas efectiva es la del formato `hashcat` y tiene que tener el `Handshake` todos los ticks que son los pasos que tiene que pasar de `autenticacion`, si hay alguno con una `X` entonces no nos serviria, en este caso se capturo de forma correcta.

## Crackeo de Handshake (Hashcat)

Vamos a pasar al `Kali` con el archivo de `hashcat` y probaremos a `crackearlo` de esta forma:

```shell
hashcat -m 22000 00_13_37_BE_EF_00_CE_C5_00_BB_6D_EA_full.22000 -a 0 <WORDLIST> -O -w 3
```

Info:

```
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, SPIR-V, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
====================================================================================================================================================
* Device #1: cpu-sandybridge-13th Gen Intel(R) Core(TM) i7-13620H, 2058/4181 MB (1024 MB allocatable), 8MCU

Kernel /usr/share/hashcat/OpenCL/m22000-optimized.cl:
Optimized kernel requested, but not available or not required
Falling back to pure kernel

Minimum password length supported by kernel: 8
Maximum password length supported by kernel: 63

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Single-Hash
* Single-Salt
* Slow-Hash-SIMD-LOOP

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 2 MB

Dictionary cache built:
* Filename..: dic.txt
* Passwords.: 8
* Bytes.....: 60
* Keyspace..: 8
* Runtime...: 0 secs

The wordlist or mask that you are using is too small.
This means that hashcat cannot use the full parallel power of your device(s).
Unless you supply more work, your cracking speed will drop.
For tips on supplying more work, see: https://hashcat.net/faq/morework

Approaching final keyspace - workload adjusted.           

c51a686b131cbc6bec67a128b81e73ae:001337beef00:cec500bb6dea:WIFI_DISEO:diseo12345a
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 22000 (WPA-PBKDF2-PMKID+EAPOL)
Hash.Target......: handshake
Time.Started.....: Sat Dec 20 17:21:25 2025 (1 sec)
Time.Estimated...: Sat Dec 20 17:21:26 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (dic.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:       17 H/s (0.92ms) @ Accel:512 Loops:1024 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 8/8 (100.00%)
Rejected.........: 5/8 (62.50%)
Restore.Point....: 0/8 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: diseo12345 -> root12345
Hardware.Mon.#1..: Util: 13%

Started: Sat Dec 20 17:21:00 2025
Stopped: Sat Dec 20 17:21:26 2025
```

Despues de unos minutos utilizando un diccionario correspondiente podremos ver que ha funcionado y hemos podido obtener la contraseña de la `red` wifi de `WIFI_DISEO` de forma correcta.
