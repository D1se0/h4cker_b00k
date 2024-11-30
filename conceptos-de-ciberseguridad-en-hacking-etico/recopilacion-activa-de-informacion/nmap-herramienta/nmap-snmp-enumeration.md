# Nmap (SNMP enumeration)

Si nosotros intentamos ejecutar este comando en el puerto `161` que es donde esta alojado el servicio de `SNMP` mediante `TCP`:

```shell
sudo nmap -v -sS -p161 192.168.16.132
```

Veremos que esta `closed` por que lo estamos haciendo mediante `TCP` ya que el servicio `SNMP` esta por `UDP` por lo que tendremos que realizar lo siguiente:

```shell
sudo nmap -v -sU -p161 192.168.16.132
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 05:38 EST
Initiating ARP Ping Scan at 05:38
Scanning 192.168.16.132 [1 port]
Completed ARP Ping Scan at 05:38, 0.04s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:38
Completed Parallel DNS resolution of 1 host. at 05:38, 13.00s elapsed
Initiating UDP Scan at 05:38
Scanning 192.168.16.132 [1 port]
Discovered open port 161/udp on 192.168.16.132
Completed UDP Scan at 05:38, 0.10s elapsed (1 total ports)
Nmap scan report for 192.168.16.132
Host is up (0.0019s latency).

PORT    STATE SERVICE
161/udp open  snmp
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 13.28 seconds
           Raw packets sent: 3 (195B) | Rcvd: 2 (113B)
```

Y aqui veremos que por `UDP` si esta `open`.

Con los scripts de `nmap` podemos recolectar informacion de este servidor, es mas, este servicio actualmente en muchas ocasiones esta mal configurado y se puede obtener mucha informacion de el, no se sabe por que, pero muchas emrpesas u organizaciones bastantes suelen tener este servicio mal configurado y de ahi se puede obtener mucha informacion incluso la intrusion del mismo.

Con el script `snmp-win32-software` se puede obtener informacion del sistema, mas las versiones de algunos procesos que se esten ejecutando en dicha maquina, pero por ejemplo veamos si esta mal configurado y nos deja enumerar usuarios.

```shell
sudo nmap -v -sU -p161 --script=snmp-win32-users 192.168.16.132
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 05:46 EST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 05:46
Completed NSE at 05:46, 0.00s elapsed
Initiating ARP Ping Scan at 05:46
Scanning 192.168.16.132 [1 port]
Completed ARP Ping Scan at 05:46, 0.04s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:46
Completed Parallel DNS resolution of 1 host. at 05:46, 13.01s elapsed
Initiating UDP Scan at 05:46
Scanning 192.168.16.132 [1 port]
Discovered open port 161/udp on 192.168.16.132
Completed UDP Scan at 05:46, 0.09s elapsed (1 total ports)
NSE: Script scanning 192.168.16.132.
Initiating NSE at 05:46
Completed NSE at 05:46, 0.02s elapsed
Nmap scan report for 192.168.16.132
Host is up (0.00053s latency).

PORT    STATE SERVICE
161/udp open  snmp
| snmp-win32-users: 
|   Administrator
|   Guest
|   anakin_skywalker
|   artoo_detoo
|   ben_kenobi
|   boba_fett
|   c_three_pio
|   chewbacca
|   darth_vader
|   greedo
|   han_solo
|   jabba_hutt
|   jarjar_binks
|   kylo_ren
|   lando_calrissian
|   leia_organa
|   luke_skywalker
|   sshd
|   sshd_server
|_  vagrant
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

NSE: Script Post-scanning.
Initiating NSE at 05:46
Completed NSE at 05:46, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 13.31 seconds
           Raw packets sent: 3 (195B) | Rcvd: 2 (113B)
```

Y en este caso si nos muestra los usuario, cuando en el servicio `SMB` mediante `TCP` no nos dejaba por que estaba bien configurado y en este si nos deja por que esta mal configurado.

Si queremos ver los procesos que se estan ejecutando en ese momento de la maquina, se podria hacer con el siguiente script:

```shell
sudo nmap -v -sU -p161 --script=snmp-processes 192.168.16.132
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 05:48 EST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 05:48
Completed NSE at 05:48, 0.00s elapsed
Initiating ARP Ping Scan at 05:48
Scanning 192.168.16.132 [1 port]
Completed ARP Ping Scan at 05:48, 0.05s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:48
Completed Parallel DNS resolution of 1 host. at 05:48, 13.00s elapsed
Initiating UDP Scan at 05:48
Scanning 192.168.16.132 [1 port]
Discovered open port 161/udp on 192.168.16.132
Completed UDP Scan at 05:48, 0.10s elapsed (1 total ports)
NSE: Script scanning 192.168.16.132.
Initiating NSE at 05:48
Completed NSE at 05:48, 0.30s elapsed
Nmap scan report for 192.168.16.132
Host is up (0.00050s latency).

PORT    STATE SERVICE
161/udp open  snmp
| snmp-processes: 
|   1: 
|     Name: System Idle Process
|   4: 
|     Name: System
|   232: 
|     Name: smss.exe
|     Path: \SystemRoot\System32\
|   336: 
|     Name: csrss.exe
|     Path: %SystemRoot%\system32\
|     Params: ObjectDirectory=\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:User
|   340: 
|     Name: svchost.exe
|   380: 
|     Name: wininit.exe
|   396: 
|     Name: csrss.exe
|     Path: %SystemRoot%\system32\
|     Params: ObjectDirectory=\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:User
|   444: 
|     Name: services.exe
|     Path: C:\Windows\system32\
|   476: 
|     Name: lsass.exe
|     Path: C:\Windows\system32\
|   484: 
|     Name: winlogon.exe
|   492: 
|     Name: lsm.exe
|     Path: C:\Windows\system32\
|   612: 
|     Name: svchost.exe
|   696: 
|     Name: svchost.exe
|   780: 
|     Name: svchost.exe
|   828: 
|     Name: svchost.exe
|   880: 
|     Name: svchost.exe
|   920: 
|     Name: svchost.exe
|   960: 
|     Name: svchost.exe
|   1072: 
|     Name: spoolsv.exe
|   1116: 
|     Name: svchost.exe
|   1144: 
|     Name: wrapper.exe
|   1304: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   1312: 
|     Name: domain1Service.exe
|   1376: 
|     Name: elasticsearch-service-x64.exe
|     Path: C:\Program Files\elasticsearch-1.1.1\bin\
|     Params:  //RS//elasticsearch-service-x64
|   1384: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   1416: 
|     Name: svchost.exe
|   1440: 
|     Name: jenkins.exe
|   1484: 
|     Name: cmd.exe
|     Params: /c ""C:/glassfish/glassfish4/glassfish/lib/nadmin.bat"  start-domain --watchdog --domaindir C:\\glassfish\\glassfish4\\glassfish
|   1504: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   1552: 
|     Name: java.exe
|     Params:  -jar "C:\glassfish\glassfish4\glassfish\lib\..\modules\admin-cli.jar" start-domain --watchdog --domaindir C:\\glassfish\\glassf
|   1568: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   1612: 
|     Name: java.exe
|   1724: 
|     Name: jmx.exe
|   1752: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   1864: 
|     Name: dcnotificationserver.exe
|   1924: 
|     Name: dcserverhttpd.exe
|   2020: 
|     Name: dcrotatelogs.exe
|     Path: C:\ManageEngine\DesktopCentral_Server\apache\bin\
|     Params: -l C:/ManageEngine/DesktopCentral_Server/logs/apache_errorlog_%Y-%m-%d-%H_%M.txt 5M
|   2040: 
|     Name: java.exe
|     Path: C:\Program Files (x86)\Common Files\Oracle\Java\javapath\
|     Params:  -jar "C:\Program Files\jenkins\jenkins.war" --httpPort=8484
|   2056: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   2104: 
|     Name: dcserverhttpd.exe
|     Path: C:\ManageEngine\DesktopCentral_Server\apache\bin\
|     Params: -d C:/ManageEngine/DesktopCentral_Server/apache
|   2112: 
|     Name: cygrunsrv.exe
|     Path: C:\Program Files\OpenSSH\bin\
|   2160: 
|     Name: cmd.exe
|     Path: C:\Windows\system32\
|     Params:   /c "C:\Program Files\jmx\start_jmx.bat"
|   2184: 
|     Name: java.exe
|     Path: C:\openjdk6\openjdk-1.6.0-unofficial-b27-windows-amd64\jre\bin\
|     Params:   -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1617 -Dcom.sun.management.jmxremote.authenticate=false -Dco
|   2204: 
|     Name: taskhost.exe
|   2324: 
|     Name: svchost.exe
|   2340: 
|     Name: dcrotatelogs.exe
|     Path: C:\ManageEngine\DesktopCentral_Server\apache\bin\
|     Params: -l C:/ManageEngine/DesktopCentral_Server/logs/apache_errorlog_%Y-%m-%d-%H_%M.txt 5M
|   2348: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   2356: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   2384: 
|     Name: sshd.exe
|     Path: C:\Program Files\OpenSSH\usr\sbin\
|   2448: 
|     Name: snmp.exe
|     Path: C:\Windows\System32\
|   3268: 
|     Name: tomcat8.exe
|     Path: C:\Program Files\Apache Software Foundation\tomcat\apache-tomcat-8.0.33\bin\
|     Params:  //RS//Tomcat8
|   3300: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   3396: 
|     Name: VGAuthService.exe
|     Path: C:\Program Files\VMware\VMware Tools\VMware VGAuth\
|   3524: 
|     Name: vmtoolsd.exe
|     Path: C:\Program Files\VMware\VMware Tools\
|   3572: 
|     Name: httpd.exe
|   3676: 
|     Name: svchost.exe
|     Path: C:\Windows\system32\
|     Params: -k iissvcs
|   3716: 
|     Name: wlms.exe
|     Path: C:\Windows\system32\wlms\
|   3884: 
|     Name: httpd.exe
|     Path: C:\wamp\bin\apache\apache2.2.21\bin\
|     Params: -d C:/wamp/bin/apache/Apache2.2.21
|   4236: 
|     Name: java.exe
|   4252: 
|     Name: conhost.exe
|     Path: \??\C:\Windows\system32\
|   4468: 
|     Name: sppsvc.exe
|   4524: 
|     Name: svchost.exe
|   4596: 
|     Name: svchost.exe
|   4760: 
|     Name: WmiPrvSE.exe
|   4796: 
|     Name: dllhost.exe
|   4916: 
|     Name: vmtoolsd.exe
|     Path: C:\Program Files\VMware\VMware Tools\
|     Params:  -n vmusr
|   4924: 
|     Name: DesktopCentral.exe
|     Path: C:\ManageEngine\DesktopCentral_Server\bin\
|     Params:  
|   4996: 
|     Name: explorer.exe
|     Path: C:\Windows\
|   5112: 
|     Name: msdtc.exe
|   6112: 
|_    Name: svchost.exe
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

NSE: Script Post-scanning.
Initiating NSE at 05:48
Completed NSE at 05:48, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 13.64 seconds
           Raw packets sent: 3 (195B) | Rcvd: 2 (113B)
```

Y como veremos aqui nos esta mostrando todos los procesos que se estan corriendo en la maquina victima (`windows`).

Tambien se podria ver las conexiones con las cuales esta maquina esta conectandose, para asi poder falsificarnos por dicha conexion y que nos de informacion o poder explotarla con `snmp-netstat` y mas script con los que se puede sacar mas informacion.
