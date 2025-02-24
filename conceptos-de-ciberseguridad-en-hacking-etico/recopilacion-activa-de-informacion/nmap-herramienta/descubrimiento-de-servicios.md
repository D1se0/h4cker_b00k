---
icon: usps
---

# Descubrimiento de servicios

Para nosotros poder descubrir un servicio con su version en un determinado puerto o en varios puertos de un `host` o de varios `hosts` podemos hacerlo con el siguiente comando:

```shell
sudo nmap -sV 192.168.16.129 -p 21
```

Con `-sV` especificamos que nos de informacion adiccional del servicio, la version, etc... Que esta corriendo en dicho puerto.

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 04:12 EST
Nmap scan report for 192.168.16.129
Host is up (0.00043s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.5
MAC Address: 00:0C:29:29:E7:FF (VMware)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.31 seconds
```

Por lo que vemos hemos descubierto que en el puerto `21` hay un servicio `ftp` con la version `ProFTPD 1.3.5` por lo que con esto podriamos encontrar algun exploit o vulnerabilidad de dicha version.

Si ahora queremos exportar los datos de los `hosts` que esten activos mas sus servicios y versiones en un fichero `XML` con estilo dentro de un segmento de red en un rango determinado por nosotros, podremos hacerlo de la siguiente forma:

```shell
sudo nmap -v --reason -sV -oX servicios.xml --stylesheet="https://svn.nmap.org/nmap/docs/nmap.xsl" 192.168.16.125-135
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 04:21 EST
NSE: Loaded 46 scripts for scanning.
Initiating ARP Ping Scan at 04:21
Scanning 10 hosts [1 port/host]
Completed ARP Ping Scan at 04:21, 1.22s elapsed (10 total hosts)
Initiating Parallel DNS resolution of 2 hosts. at 04:21
Completed Parallel DNS resolution of 2 hosts. at 04:21, 13.00s elapsed
Nmap scan report for 192.168.16.125 [host down, received no-response]
Nmap scan report for 192.168.16.126 [host down, received no-response]
Nmap scan report for 192.168.16.127 [host down, received no-response]
Nmap scan report for 192.168.16.130 [host down, received no-response]
Nmap scan report for 192.168.16.131 [host down, received no-response]
Nmap scan report for 192.168.16.133 [host down, received no-response]
Nmap scan report for 192.168.16.134 [host down, received no-response]
Nmap scan report for 192.168.16.135 [host down, received no-response]
Initiating Parallel DNS resolution of 1 host. at 04:21
Completed Parallel DNS resolution of 1 host. at 04:22, 13.00s elapsed
Initiating SYN Stealth Scan at 04:22
Scanning 2 hosts [1000 ports/host]
Discovered open port 3306/tcp on 192.168.16.129
Discovered open port 3389/tcp on 192.168.16.132
Discovered open port 21/tcp on 192.168.16.132
Discovered open port 139/tcp on 192.168.16.132
Discovered open port 21/tcp on 192.168.16.129
Discovered open port 8080/tcp on 192.168.16.132
Discovered open port 22/tcp on 192.168.16.132
Discovered open port 445/tcp on 192.168.16.132
Discovered open port 8080/tcp on 192.168.16.129
Discovered open port 80/tcp on 192.168.16.132
Discovered open port 135/tcp on 192.168.16.132
Discovered open port 22/tcp on 192.168.16.129
Discovered open port 445/tcp on 192.168.16.129
Discovered open port 49152/tcp on 192.168.16.132
Discovered open port 49155/tcp on 192.168.16.132
Increasing send delay for 192.168.16.132 from 0 to 5 due to 57 out of 188 dropped probes since last increase.
Discovered open port 8383/tcp on 192.168.16.132
Discovered open port 80/tcp on 192.168.16.129
Discovered open port 49157/tcp on 192.168.16.132
Discovered open port 9200/tcp on 192.168.16.132
Discovered open port 8181/tcp on 192.168.16.132
Discovered open port 4848/tcp on 192.168.16.132
Discovered open port 8009/tcp on 192.168.16.132
Discovered open port 49156/tcp on 192.168.16.132
Discovered open port 49154/tcp on 192.168.16.132
Discovered open port 631/tcp on 192.168.16.129
Completed SYN Stealth Scan against 192.168.16.129 in 6.10s (1 host left)
Discovered open port 49153/tcp on 192.168.16.132
Discovered open port 7676/tcp on 192.168.16.132
Completed SYN Stealth Scan at 04:22, 7.84s elapsed (2000 total ports)
Initiating Service scan at 04:22
Scanning 27 services on 2 hosts
Completed Service scan at 04:24, 103.68s elapsed (27 services on 2 hosts)
NSE: Script scanning 2 hosts.
Initiating NSE at 04:24
Completed NSE at 04:24, 8.09s elapsed
Initiating NSE at 04:24
Completed NSE at 04:24, 4.13s elapsed
Nmap scan report for 192.168.16.129
Host is up, received arp-response (0.00038s latency).
Not shown: 991 filtered tcp ports (no-response)
PORT     STATE  SERVICE     REASON         VERSION
21/tcp   open   ftp         syn-ack ttl 64 ProFTPD 1.3.5
22/tcp   open   ssh         syn-ack ttl 64 OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open   http        syn-ack ttl 64 Apache httpd 2.4.7
445/tcp  open   netbios-ssn syn-ack ttl 64 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
631/tcp  open   ipp         syn-ack ttl 64 CUPS 1.7
3000/tcp closed ppp         reset ttl 64
3306/tcp open   mysql       syn-ack ttl 64 MySQL (unauthorized)
8080/tcp open   http        syn-ack ttl 64 Jetty 8.1.7.v20120910
8181/tcp closed intermapper reset ttl 64
MAC Address: 00:0C:29:29:E7:FF (VMware)
Service Info: Hosts: 127.0.0.1, UBUNTU; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Nmap scan report for 192.168.16.132
Host is up, received arp-response (0.00029s latency).
Not shown: 980 closed tcp ports (reset)
PORT      STATE SERVICE              REASON          VERSION
21/tcp    open  ftp                  syn-ack ttl 128 Microsoft ftpd
22/tcp    open  ssh                  syn-ack ttl 128 OpenSSH 7.1 (protocol 2.0)
80/tcp    open  http                 syn-ack ttl 128 Microsoft IIS httpd 7.5
135/tcp   open  msrpc                syn-ack ttl 128 Microsoft Windows RPC
139/tcp   open  netbios-ssn          syn-ack ttl 128 Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds         syn-ack ttl 128 Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  tcpwrapped           syn-ack ttl 128
4848/tcp  open  ssl/http             syn-ack ttl 128 Oracle GlassFish 4.0 (Servlet 3.1; JSP 2.3; Java 1.8)
7676/tcp  open  java-message-service syn-ack ttl 128 Java Message Service 301
8009/tcp  open  ajp13                syn-ack ttl 128 Apache Jserv (Protocol v1.3)
8080/tcp  open  http                 syn-ack ttl 128 Sun GlassFish Open Source Edition  4.0
8181/tcp  open  ssl/intermapper?     syn-ack ttl 128
8383/tcp  open  http                 syn-ack ttl 128 Apache httpd
9200/tcp  open  wap-wsp?             syn-ack ttl 128
49152/tcp open  msrpc                syn-ack ttl 128 Microsoft Windows RPC
49153/tcp open  msrpc                syn-ack ttl 128 Microsoft Windows RPC
49154/tcp open  msrpc                syn-ack ttl 128 Microsoft Windows RPC
49155/tcp open  msrpc                syn-ack ttl 128 Microsoft Windows RPC
49156/tcp open  java-rmi             syn-ack ttl 128 Java RMI
49157/tcp open  tcpwrapped           syn-ack ttl 128
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port8181-TCP:V=7.94SVN%T=SSL%I=7%D=11/11%Time=6731CCED%P=x86_64-pc-linu
SF:x-gnu%r(RTSPRequest,76,"HTTP/1\.1\x20505\x20HTTP\x20Version\x20Not\x20S
SF:upported\r\nDate:\x20Mon,\x2011\x20Nov\x202024\x2009:22:52\x20GMT\r\nCo
SF:nnection:\x20close\r\nContent-Length:\x200\r\n\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9200-TCP:V=7.94SVN%I=7%D=11/11%Time=6731CCD7%P=x86_64-pc-linux-gnu%
SF:r(GetRequest,18C,"HTTP/1\.0\x20200\x20OK\r\nContent-Type:\x20applicatio
SF:n/json;\x20charset=UTF-8\r\nContent-Length:\x20309\r\n\r\n{\r\n\x20\x20
SF:\"status\"\x20:\x20200,\r\n\x20\x20\"name\"\x20:\x20\"Maha\x20Yogi\",\r
SF:\n\x20\x20\"version\"\x20:\x20{\r\n\x20\x20\x20\x20\"number\"\x20:\x20\
SF:"1\.1\.1\",\r\n\x20\x20\x20\x20\"build_hash\"\x20:\x20\"f1585f096d3f398
SF:5e73456debdc1a0745f512bbc\",\r\n\x20\x20\x20\x20\"build_timestamp\"\x20
SF::\x20\"2014-04-16T14:27:12Z\",\r\n\x20\x20\x20\x20\"build_snapshot\"\x2
SF:0:\x20false,\r\n\x20\x20\x20\x20\"lucene_version\"\x20:\x20\"4\.7\"\r\n
SF:\x20\x20},\r\n\x20\x20\"tagline\"\x20:\x20\"You\x20Know,\x20for\x20Sear
SF:ch\"\r\n}\n")%r(HTTPOptions,4F,"HTTP/1\.0\x20200\x20OK\r\nContent-Type:
SF:\x20text/plain;\x20charset=UTF-8\r\nContent-Length:\x200\r\n\r\n")%r(RT
SF:SPRequest,4F,"HTTP/1\.1\x20200\x20OK\r\nContent-Type:\x20text/plain;\x2
SF:0charset=UTF-8\r\nContent-Length:\x200\r\n\r\n")%r(FourOhFourRequest,A9
SF:,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x2
SF:0charset=UTF-8\r\nContent-Length:\x2080\r\n\r\nNo\x20handler\x20found\x
SF:20for\x20uri\x20\[/nice%20ports%2C/Tri%6Eity\.txt%2ebak\]\x20and\x20met
SF:hod\x20\[GET\]")%r(SIPOptions,4F,"HTTP/1\.1\x20200\x20OK\r\nContent-Typ
SF:e:\x20text/plain;\x20charset=UTF-8\r\nContent-Length:\x200\r\n\r\n");
MAC Address: 00:0C:29:EC:1E:B9 (VMware)
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Initiating SYN Stealth Scan at 04:24
Scanning 192.168.16.128 [1000 ports]
Completed SYN Stealth Scan at 04:24, 0.02s elapsed (1000 total ports)
Initiating Service scan at 04:24
NSE: Script scanning 192.168.16.128.
Initiating NSE at 04:24
Completed NSE at 04:24, 0.00s elapsed
Initiating NSE at 04:24
Completed NSE at 04:24, 0.00s elapsed
Nmap scan report for 192.168.16.128
Host is up, received localhost-response (0.0000060s latency).
All 1000 scanned ports on 192.168.16.128 are in ignored states.
Not shown: 1000 closed tcp ports (reset)

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 11 IP addresses (3 hosts up) scanned in 151.28 seconds
           Raw packets sent: 4071 (178.836KB) | Rcvd: 3013 (124.604KB)
```

Y con esto nos dara toda la informacion que obtuvimos anteriormente con dicho comando, pero esta vez con las versiones y servicios que hay corriendo en los diferentes `hosts` y con un fichero `XML`.

<figure><img src="../../../.gitbook/assets/image (28) (1).png" alt=""><figcaption></figcaption></figure>

Esta tecnica si es verdad que es muchisimo mas intrusiva que las demas.
