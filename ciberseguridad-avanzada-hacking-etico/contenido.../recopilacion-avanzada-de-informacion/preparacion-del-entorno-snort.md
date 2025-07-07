---
icon: pig
---

# Preparación del entorno - Snort

Vamos a crear una red virtual con `VMWare` para meter en la misma red virtual todas las maquinas que vayamos a ir `hackeando` o haciendole pruebas de penetracion, incluida la del `kali`.

Nos iremos en `VMWare` -> `Edit` -> `Virtual Network Editor...` -> `Change Settings` -> `Add Network...` -> seleccionamos `VMnet3` -> `Ok` -> en la parte de `Subnet IP` lo pondremos como `192.168.20.0` -> `Apply` -> `Ok`.

Una vez que ya hayamos configurado toda la red virtual en `Host Only` haremos lo siguiente:

Nos vamos a la maquina `Tr0ll: 1` seleccionamos `Edit Virtual Machine Settings` -> `Network Adapter` -> `Custom: Specific virtual network` -> seleccionamos `VMnet3 (Host-only)`.

Iniciaremos la maquina dandole a `Power...` y seguidamente mientras se inicia la maquina, descargaremos la herramienta de seguridad llamada `Snort`.

Este `software` es un `IDS` bastante ponente el cual se encarga principalmente de detectar actividad maliciosa en trafico de red, generalmente este tipo de herramientas se colocan en un punto de la infraestructura tecnologica por donde pasa el trafico de red que se intercambia por los sistemas que queremos monitorizar, en nuestro caso nuestro punto central va a ser nuestra maquina `host`.

Si nosotros en nuestro `windows` abrimos `powershell` y ejecutamos:

```powershell
ipconfig
```

Vamos a ver que tenemos creado nuestra red virtual de `VMWare` que creamos anteriormente el `VMnet3`:

```
Adaptador de Ethernet VMware Network Adapter VMnet3:

   Sufijo DNS específico para la conexión. . :
   Vínculo: dirección IPv6 local. . . : fe80::ef:b5c0:32f7:5d45%56
   Dirección IPv4. . . . . . . . . . . . . . : 192.168.20.1
   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
   Puerta de enlace predeterminada . . . . . :
```

Y vemos que nuestra maquina `host` esta actuando como un `router` virtual.

```
192.168.20.1
```

Ya que la `.1` suele estar destinada al `router` que es la que se va a encargar de distribuir el trafico entre los diferentes dispositivos que esten conectados a su red, en nuestro caso lo hace la maquina `host`, por lo que si nosotros instalamos `Snort` dentro de nuestra maquina `host` lo que vamos a poder hacer es monitorizar todo el trafico que se intercambie entre las maquinas virtuales.

Con esto podremos ver como aplicar medidas para evadir la deteccion de este tipo de herramientas de seguridad que nos vamos a encontrar en cualquier entorno profesional.

Vamos a descargarnos la herramienta de `Snort`:

URL = [Download Snort](https://www.snort.org/downloads)

Una vez que se nos haya instalado, cuando le demos a `close` nos pondra el siguiente mensaje:

<figure><img src="../../../.gitbook/assets/image (205).png" alt=""><figcaption></figcaption></figure>

El cual nos dice que se instalo todo correctamente, pero que para poder interceptar los datos de una maquina a otra necesitara una libreria llamada `Npcap` que pertenece a `nmap`, por lo que nos iremos a la siguiente pagina:

URL = [Download Npcap](https://npcap.com)

Una vez que hayamos ejecutado el instalador e instalado todo, tendremos que irnos a la siguiente ruta de `windows`:

```
C:\Snort\etc
```

Aqui dentro veremos varios archivos entre ellos uno llamado `snort.conf` este le tendremos que reemplazar por una configuracion ya profesional que tendremos que descargar en el siguiente link:

URL = [Download snort.conf](https://drive.google.com/file/d/1W86rglBka9NAejS7Rx6lyymuV_2GFWKJ/view?usp=sharing)

Y este archivo lo pegaremos en esa ruta reemplazandolo, seguidamente nos descargaremos las reglas configuradas de `Snort` tambien en un `.zip`:

URL = [Download rules\_snort.zip](https://drive.google.com/file/d/1ozf_4fV2d8pGEeDGvY38jCt_fVnflwTv/view?usp=sharing)

Y tendremos que descomprimir la carpeta ZIP, nos dejara una carpeta llamada `rules`, pues el contenido de la misma los `75` archivos los pegaremos en la siguiente ruta:

```
C:\Snort\rules
```

Una vez echo todo esto, ya tendriamos a punto nuestro `software`.

> NOTA IMPORTANTE:

Si por ejemplo pusisteis una direccion distinta que no fuera la `192.168.20.0` por ejemplo la `192.168.50.0` tendreis que actualizarlo en el archivo `snort.conf` en la siguiente seccion:

```
# Setup the network addresses you are protecting
ipvar HOME_NET 192.168.20.0/24
```

Cuando tengamos ya todo, iniciaremos nuestro `kali` y le meteremos en la red de `VMnet3` como hicimos con la anterior maquina.

Ahora cuando tengamos las 2 maquinas desplegadas y queramos capturar todo el trafico con `Snort` ejecutaremos lo siguiente en nuestra `powershell` en `windows`.

```powershell
cd C:\Snort\bin
.\snort.exe -W
```

Con `-W` vemos las interfaces de red que tenemos disponibles.

```

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.20-WIN64 GRE (Build 82)
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014-2022 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using PCRE version: 8.10 2010-06-25
           Using ZLIB version: 1.2.11

Index   Physical Address        IP Address      Device Name     Description
-----   ----------------        ----------      -----------     -----------
    5   00:50:56:C0:00:03       192.168.20.1    \Device\NPF_{736F6191-9B39-452D-88A0-F2EA055C35F4}      VMware Virtual Ethernet Adapter for VMnet3
```

La que nos interesa es la de `VMnet3` vemos que en mi caso esta asignado con el numero `5` por lo que haremos lo siguiente:

```powershell
.\snort.exe -i 5 -A console -c C:\Snort\etc\snort.conf
```

Con el `-i` especificamos el numero de la interfaz que queremos monitorizar Con el `-A` especificamos que las alertas nos la muestre por consola Con el `-c` especificamos que utilice el fichero de configuracion que implementamos anteriormente

```
        --== Initialization Complete ==--

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.20-WIN64 GRE (Build 82)
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014-2022 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using PCRE version: 8.10 2010-06-25
           Using ZLIB version: 1.2.11

           Rules Engine: SF_SNORT_DETECTION_ENGINE  Version 3.2  <Build 1>
           Preprocessor Object: SF_SSLPP  Version 1.1  <Build 4>
           Preprocessor Object: SF_SSH  Version 1.1  <Build 3>
           Preprocessor Object: SF_SMTP  Version 1.1  <Build 9>
           Preprocessor Object: SF_SIP  Version 1.1  <Build 1>
           Preprocessor Object: SF_SDF  Version 1.1  <Build 1>
           Preprocessor Object: SF_REPUTATION  Version 1.1  <Build 1>
           Preprocessor Object: SF_POP  Version 1.0  <Build 1>
           Preprocessor Object: SF_MODBUS  Version 1.1  <Build 1>
           Preprocessor Object: SF_IMAP  Version 1.0  <Build 1>
           Preprocessor Object: SF_GTP  Version 1.1  <Build 1>
           Preprocessor Object: SF_FTPTELNET  Version 1.2  <Build 13>
           Preprocessor Object: SF_DNS  Version 1.1  <Build 4>
           Preprocessor Object: SF_DNP3  Version 1.1  <Build 1>
           Preprocessor Object: SF_DCERPC2  Version 1.0  <Build 3>
Commencing packet processing (pid=26680)
```

Como veremos `Snort` ya esta monitorizando la interfaz de red.

Vamos a ver si realmente esta capturando todo el trafico de red de la siguiente forma, nos iremos a `kali` y haremos un escaneo simple con `nmap` para ver que IP tiene la maquina `tr0ll`:

```shell
sudo nmap -sS -n 192.168.20.0/24
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-02 10:39 EST
Nmap scan report for 192.168.20.1
Host is up (0.00058s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:60:52:F0:01:08 (VMware)

Nmap scan report for 192.168.20.128
Host is up (0.0013s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:0C:29:30:9B:3A (VMware)

Nmap scan report for 192.168.20.254
Host is up (0.00010s latency).
All 1000 scanned ports on 192.168.20.254 are in ignored states.
Not shown: 1000 filtered tcp ports (no-response)
MAC Address: 00:50:56:FC:E5:23 (VMware)

Nmap scan report for 192.168.20.129
Host is up (0.0000060s latency).
All 1000 scanned ports on 192.168.20.129 are in ignored states.
Not shown: 1000 closed tcp ports (reset)

Nmap done: 256 IP addresses (4 hosts up) scanned in 8.29 seconds
```

Vemos que el scaneo fue bien, pero si nos vamos al `PowerShell` veremos lo siguiente:

```
01/02-16:39:53.553598  [**] [122:3:1] (portscan) TCP Portsweep [**] [Classification: Attempted Information Leak] [Priority: 2] {PROTO:255} 192.168.20.129 -> 192.168.20.128
01/02-16:39:53.553598  [**] [122:1:1] (portscan) TCP Portscan [**] [Classification: Attempted Information Leak] [Priority: 2] {PROTO:255} 192.168.20.129 -> 192.168.20.128
01/02-16:39:53.626276  [**] [1:1418:11] SNMP request tcp [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33239 -> 192.168.20.128:161
01/02-16:39:53.639718  [**] [1:1421:11] SNMP AgentX/tcp request [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33239 -> 192.168.20.128:705
01/02-16:39:57.510741  [**] [1:1418:11] SNMP request tcp [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33239 -> 192.168.20.1:161
01/02-16:39:57.611109  [**] [1:1418:11] SNMP request tcp [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33241 -> 192.168.20.1:161
01/02-16:39:58.011336  [**] [1:1418:11] SNMP request tcp [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33239 -> 192.168.20.254:161
01/02-16:39:58.113809  [**] [1:1418:11] SNMP request tcp [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33241 -> 192.168.20.254:161
01/02-16:39:58.218401  [**] [1:1421:11] SNMP AgentX/tcp request [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33239 -> 192.168.20.1:705
01/02-16:39:58.319278  [**] [1:1421:11] SNMP AgentX/tcp request [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33241 -> 192.168.20.1:705
01/02-16:39:58.690677  [**] [1:1421:11] SNMP AgentX/tcp request [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33239 -> 192.168.20.254:705
01/02-16:39:58.790996  [**] [1:1421:11] SNMP AgentX/tcp request [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.20.129:33241 -> 192.168.20.254:705
```

Vemos que `Snort` nos ha capturado el scaneo que hemos realizado y nos lo clasifica de esta forma:

```
01/02-16:39:53.553598  [**] [122:3:1] (portscan) TCP Portsweep [**] [Classification: Attempted Information Leak] [Priority: 2] {PROTO:255} 192.168.20.129 -> 192.168.20.128
```

Con un `(portscan)`, basicamente un escaneo de puertos, con la direccion `IP` de entrada y la de destino.

Mas adelante veremos a como `Bypassear` estas medidas de seguridad para que no seamos detectados por herramientas como estas.
