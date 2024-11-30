# Nmap (SMB Enumeration)

El puerto `SMB` es uno de los servicios mas antiguos que existen ya que se utiliza mucho y a medida que ha ido pasando el tiempo ha sido un foco de ataques enorme, pero tambien ha ido evolucionando de versiones, por lo que veremos en mas profundidad como enumerar este tipo de servicio.

En este tipo de servicios generalmente se utiliza para la comparticion de archivos en una red (Recursos compartidos), donde puede estar alojado todo tipo de informacion desde informacion que es inutil, hasta informacion delicada, ya que muchos usuarios lo utilizan simplemente por comodidad y muchas veces hay informacion que no deberia de estar ahi, pero que nosotros como atacantes podemos aprovechar.

Por lo que vamos a escanear los puertos que estan sujetos a este servicio que serian el `139` y el `445`.

```shell
sudo nmap -v -sS -p 139,445 192.168.16.132
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 05:11 EST
Initiating ARP Ping Scan at 05:11
Scanning 192.168.16.132 [1 port]
Completed ARP Ping Scan at 05:11, 0.04s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:11
Completed Parallel DNS resolution of 1 host. at 05:11, 13.00s elapsed
Initiating SYN Stealth Scan at 05:11
Scanning 192.168.16.132 [2 ports]
Discovered open port 139/tcp on 192.168.16.132
Discovered open port 445/tcp on 192.168.16.132
Completed SYN Stealth Scan at 05:11, 1.12s elapsed (2 total ports)
Nmap scan report for 192.168.16.132
Host is up (0.00046s latency).

PORT    STATE SERVICE
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 14.27 seconds
           Raw packets sent: 4 (160B) | Rcvd: 3 (116B)
```

Por lo que vemos que para conexiones `TCP` estan los puertos abiertos.

La propia herramienta `nmap` en una ruta en concreto nos da scritps automatizados para nosotros poder enumerar, explotar, recopilar artefactos o recursos que se esten compartiendo en este caso mediante `SMB`, etc... Estos scripts son muy utiles para automatizar todo esto y en este caso para el servicio `SMB` poder utilizar los siguientes script para enumerar y posteriormente explotar vulnerabilidades.

Estos scripts se encuentran en la siguiente ruta:

```shell
cd /usr/share/nmap/scripts/
```

Si nosotros listamos los scripts que nos interesen, en este caso con `SMB`, lo podremos hacer de la siguiente forma:

```shell
ls smb*
```

Info:

```
 smb-brute.nse                    smb-enum-sessions.nse   smb-os-discovery.nse    smb-system-info.nse          smb-vuln-ms08-067.nse     smb-webexec-exploit.nse
 smb-double-pulsar-backdoor.nse   smb-enum-shares.nse     smb-print-text.nse      smb-vuln-conficker.nse       smb-vuln-ms10-054.nse     smb2-capabilities.nse
 smb-enum-domains.nse             smb-enum-users.nse      smb-protocols.nse       smb-vuln-cve-2017-7494.nse   smb-vuln-ms10-061.nse     smb2-security-mode.nse
 smb-enum-groups.nse              smb-flood.nse           smb-psexec.nse          smb-vuln-cve2009-3103.nse    smb-vuln-ms17-010.nse     smb2-time.nse
 smb-enum-processes.nse           smb-ls.nse              smb-security-mode.nse   smb-vuln-ms06-025.nse        smb-vuln-regsvc-dos.nse   smb2-vuln-uptime.nse
 smb-enum-services.nse            smb-mbenum.nse          smb-server-stats.nse    smb-vuln-ms07-029.nse        smb-vuln-webexec.nse
```

Veremos unos cuantos scripts.

Por ejemplo para utilizar uno de estos scripts en `nmap` podremos hacerlo de la siguiente forma:

Si por ejemplo queremos sacar mas informacion del sistema operativo con un script de `SMB` podremos hacerlo asi:

```shell
sudo nmap -v -sS -p 139,445 --script=smb-os-discovery 192.168.16.132
```

Y con esto lo que estamos haciendo es ejecutar ese script, bajo esos puertos de esa IP

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 05:20 EST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 05:20
Completed NSE at 05:20, 0.00s elapsed
Initiating ARP Ping Scan at 05:20
Scanning 192.168.16.132 [1 port]
Completed ARP Ping Scan at 05:20, 0.03s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:20
Completed Parallel DNS resolution of 1 host. at 05:20, 13.00s elapsed
Initiating SYN Stealth Scan at 05:20
Scanning 192.168.16.132 [2 ports]
Discovered open port 139/tcp on 192.168.16.132
Discovered open port 445/tcp on 192.168.16.132
Completed SYN Stealth Scan at 05:20, 1.12s elapsed (2 total ports)
NSE: Script scanning 192.168.16.132.
Initiating NSE at 05:20
Completed NSE at 05:20, 0.02s elapsed
Nmap scan report for 192.168.16.132
Host is up (0.00059s latency).

PORT    STATE SERVICE
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2008 R2 Standard 7601 Service Pack 1 (Windows Server 2008 R2 Standard 6.1)
|   OS CPE: cpe:/o:microsoft:windows_server_2008::sp1
|   Computer name: vagrant-2008R2
|   NetBIOS computer name: VAGRANT-2008R2\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-11-11T02:20:22-08:00

NSE: Script Post-scanning.
Initiating NSE at 05:20
Completed NSE at 05:20, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 14.33 seconds
           Raw packets sent: 4 (160B) | Rcvd: 3 (116B)
```

Y aqui nos especifica con el script que ciertamente es un `Windows Server 2008 R2 Standard` junto a mas informacion.

Si queremos identificar que carpetas compartidas esta exponiendo dicha maquina mediante el `SMB` podremos hacerlo con el siguiente script:

```shell
sudo nmap -v -sS -p 139,445 --script=smb-enum-shares 192.168.16.132
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 05:26 EST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 05:26
Completed NSE at 05:26, 0.00s elapsed
Initiating ARP Ping Scan at 05:26
Scanning 192.168.16.132 [1 port]
Completed ARP Ping Scan at 05:26, 0.05s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:26
Completed Parallel DNS resolution of 1 host. at 05:26, 13.00s elapsed
Initiating SYN Stealth Scan at 05:26
Scanning 192.168.16.132 [2 ports]
Discovered open port 445/tcp on 192.168.16.132
Discovered open port 139/tcp on 192.168.16.132
Completed SYN Stealth Scan at 05:26, 0.02s elapsed (2 total ports)
NSE: Script scanning 192.168.16.132.
Initiating NSE at 05:26
Completed NSE at 05:26, 0.79s elapsed
Nmap scan report for 192.168.16.132
Host is up (0.00032s latency).

PORT    STATE SERVICE
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

Host script results:
| smb-enum-shares: 
|   note: ERROR: Enumerating shares failed, guessing at common ones (NT_STATUS_ACCESS_DENIED)
|   account_used: <blank>
|   \\192.168.16.132\ADMIN$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\192.168.16.132\C$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\192.168.16.132\IPC$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: READ
|   \\192.168.16.132\USERS: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|_    Anonymous access: <none>

NSE: Script Post-scanning.
Initiating NSE at 05:26
Completed NSE at 05:26, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 14.01 seconds
           Raw packets sent: 3 (116B) | Rcvd: 3 (116B)
```

En este caso esta bien configurado la maquina, ya que no permite ver los recursos compartidos de forma anonima.

Si queremos listar usuarios mediante el `SMB` podremos hacerlo con el siguiente script:

```shell
sudo nmap -v -sS -p 139,445 --script=smb-enum-users 192.168.16.132
```

En este caso tambien estara bien configurado y no nos mostrara ningun usuario.
