---
icon: flatbread
layout:
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
---

# Preparación del entorno vulnerable

Para hacer nuestras prubeas nos descargaremos una maquina laboratorio de `VulnHub` que es con el que vamos a estar practicando mucho, ya que entran varias cosas impoprtantes y variadas para practicar lo que queremos hacer.

URL = [VulnHub LAB Download](https://www.vulnhub.com/entry/vulnerable-pentesting-lab-environment-1,737/)

Una vez descargada la descomprimimos y la importaremos a `VMWare` para poderla utilizar.

En la propia maquina nos porporcionara las credenciales del `Administrador` y los puertos en los que esta corriendo cada una de las aplicaciones:

<figure><img src="../../.gitbook/assets/image (180).png" alt=""><figcaption></figcaption></figure>

Ahora la iniciaremos, meteremos las credeciales que nos propociona y una vez dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (181).png" alt=""><figcaption></figcaption></figure>

Ahora en nuestro `kali` veremos que `IP` le ha dado a nuestra maquina de la siguiente forma:

```shell
sudo nmap -sS -n 192.168.5.0/24
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-28 03:19 EST
Nmap scan report for 192.168.5.1
Host is up (0.00098s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:50:56:C0:00:08 (VMware)

Nmap scan report for 192.168.5.2
Host is up (0.000056s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
53/tcp open  domain
MAC Address: 00:50:56:F5:72:77 (VMware)

Nmap scan report for 192.168.5.211
Host is up (0.00053s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE
80/tcp   open  http
3000/tcp open  ppp
8080/tcp open  http-proxy
8800/tcp open  sunwebadmin
8899/tcp open  ospf-lite
MAC Address: 00:0C:29:71:73:31 (VMware)

Nmap scan report for 192.168.5.254
Host is up (0.00012s latency).
All 1000 scanned ports on 192.168.5.254 are in ignored states.
Not shown: 1000 filtered tcp ports (no-response)
MAC Address: 00:50:56:FF:9B:11 (VMware)

Nmap scan report for 192.168.5.205
Host is up (0.0000070s latency).
All 1000 scanned ports on 192.168.5.205 are in ignored states.
Not shown: 1000 closed tcp ports (reset)

Nmap done: 256 IP addresses (5 hosts up) scanned in 7.86 seconds
```

Vemos que le ha dado la `192.168.5.211`, por lo que si habrimos el navegador y probamos a meter uno de los puertos en los que esta corriendo una pagina web en este caso `Mutillidae` de la siguiente forma:

```
URL = http://192.168.5.211:1336/
```

Veremos que efectivamente estaremos dentro de la pagina de `Mutillidae`.

Pero vamos a irnos a la siguiente direccion `IP` para instalarnos una configuracion de pagina web:

```
URL = http://192.168.5.211:8080/install.php
```

Dentro de aqui le daremos a `Click here`, dandole ahi veremos que se instalo correctamente ya que veremos el siguiente mensaje:

```
bWAPP has been installed successfully!
```

Nos iremos a `New User` y rellenaremos la informacion de un usuario para crearlo.

```
Login: santiago
Password: 1234
E-mail: test@test.com
Secret: test
```

Y le daremos a `Create`, esto nos creara el usuario y le daremos a `Login` para logearnos con las mismas credenciales que hemos creado, una vez echo eso veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (182).png" alt=""><figcaption></figcaption></figure>

Y en los demas puertos veremos diferentes paginas web en las cuales seran vulnerables unas mas dificiles que otras.
