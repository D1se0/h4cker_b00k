---
icon: radar
---

# Escaneo avanzado de puertos

Una vez que hayamos identificado el `host` al que queremos realizarle el escaneo de puertos, podremos hacerlo sin que `Snort` nos detecte de la siguiente forma:

```shell
sudo nmap -sS -n --top-ports 5 192.168.20.128
```

Con `--top-ports` especificamos que nos escanee los `5` puertos principales que tiene `nmap` en su lista, para asi generar menos trafico de red y no ser detectado por herramientas `IDS`.

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-03 03:25 EST
Nmap scan report for 192.168.20.128
Host is up (0.00072s latency).

PORT    STATE  SERVICE
21/tcp  open   ftp
22/tcp  open   ssh
23/tcp  closed telnet
80/tcp  open   http
443/tcp closed https
MAC Address: 00:0C:29:30:9B:3A (VMware)

Nmap done: 1 IP address (1 host up) scanned in 0.20 seconds
```
