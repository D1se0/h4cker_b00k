# Extraviado DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip extraviado.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh extraviado.tar
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

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-13 10:34 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000026s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 cc:d2:9b:60:14:16:27:b3:b9:f8:79:10:df:a1:f3:24 (ECDSA)
|_  256 37:a2:b2:b2:26:f2:07:d1:83:7a:ff:98:8d:91:77:37 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.51 seconds
```

Si inspeccionamos la pagina al final de todo veremos lo siguiente:

```
#.........................................................................................................ZGFuaWVsYQ== : Zm9jYXJvamE=
```

Por lo que vemos esta en `Base64` y si lo decodificamos...

```
daniela:focaroja
```

Vemos que son unas credenciales, por lo que nos conectaremos por `SSH`.

## SSH

```shell
ssh daniela@<IP>
```

Metemos como contraseña `focaroja` y estaremos dentro con dicho usuario.

## Escalate user diego

Si leemos el siguiente fichero:

```shell
cat .secreto/passdiego
```

Info:

```
YmFsbGVuYW5lZ3Jh
```

Si lo decodificamos de `Base64` veremos lo siguiente:

```
ballenanegra
```

Por lo que haremos lo siguiente:

```shell
su diego
```

Metemos como contraseña `ballenanegra` y veremos que somos dicho usuario.

## Escalate Privileges

Si leemos el sigueinte archivo:

```shell
cat /home/diego/.local/share/.-
```

Info:

```
password de root

En un mundo de hielo, me muevo sin prisa,
con un pelaje que brilla, como la brisa.
No soy un rey, pero en cuentos soy fiel,
de un color inusual, como el cielo y el mar
tambien.
Soy amigo de los ni~nos, en historias de
ensue~no.
Quien soy, que en el frio encuentro mi due~no?
```

El acertijo es `osoazul` a parte de que sigue la misma mecanica de contraseñas, por lo que si hacemos lo siguiente:

```shell
su root
```

Metemos como contraseña `osoazul` veremos que seremos `root`.
