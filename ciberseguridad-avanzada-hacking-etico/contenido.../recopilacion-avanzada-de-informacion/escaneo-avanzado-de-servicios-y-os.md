---
icon: bell-concierge
---

# Escaneo avanzado de servicios y OS

Una vez identificado el `host` con los puertos que contiene, lo que podremos hacer es con un script de `nmap` identificar la informacion de cada puerto sin ser detectado por las herramientas de `IDS`.

```shell
sudo nmap -sV -n -p21,22,80 192.168.20.128
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-04 04:22 EST
Nmap scan report for 192.168.20.128
Host is up (0.00044s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.2
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
MAC Address: 00:0C:29:30:9B:3A (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.52 seconds
```

Ahora si queremos realizar un escaneo de forma silenciosa, para detectar que sistema operativo es, podremos hacerlo de la siguiente forma:

```shell
sudo nmap -O -n -p22,80 --scan-delay 5 192.168.20.128
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-04 04:24 EST
Nmap scan report for 192.168.20.128
Host is up (0.00042s latency).

PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:0C:29:30:9B:3A (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.56 seconds
```
