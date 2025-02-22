# Análisis de vulnerabilidades con Nmap

Podemos utilizar los scripts de `namp` para hacer analisis de vulnerabilidades, en concreto los scripts llamados `vuln` por lo que si queremos hacer un escaneo de vulnerabilidades de una maquina de forma generica, pondremos el siguiente comando:

```shell
sudo nmap -v -sS --script=vuln 192.168.16.129
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-12 05:29 EST
NSE: Loaded 105 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 05:29
Completed NSE at 05:29, 0.00s elapsed
Initiating NSE at 05:29
Completed NSE at 05:29, 0.00s elapsed
Initiating ARP Ping Scan at 05:29
Scanning 192.168.16.129 [1 port]
Completed ARP Ping Scan at 05:29, 0.05s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 05:29
Completed Parallel DNS resolution of 1 host. at 05:29, 13.00s elapsed
Initiating SYN Stealth Scan at 05:29
Scanning 192.168.16.129 [1000 ports]
Discovered open port 111/tcp on 192.168.16.129
Discovered open port 80/tcp on 192.168.16.129
Discovered open port 22/tcp on 192.168.16.129
Discovered open port 21/tcp on 192.168.16.129
Discovered open port 3306/tcp on 192.168.16.129
Discovered open port 445/tcp on 192.168.16.129
Discovered open port 139/tcp on 192.168.16.129
Discovered open port 8080/tcp on 192.168.16.129
Discovered open port 631/tcp on 192.168.16.129
Discovered open port 6667/tcp on 192.168.16.129
Completed SYN Stealth Scan at 05:29, 0.05s elapsed (1000 total ports)
NSE: Script scanning 192.168.16.129.
Initiating NSE at 05:29
Completed NSE at 05:34, 316.64s elapsed
Initiating NSE at 05:34
Completed NSE at 05:34, 0.01s elapsed
Nmap scan report for 192.168.16.129
Host is up (0.00021s latency).
Not shown: 990 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
| http-fileupload-exploiter: 
|   
|_    Couldn't find a file-type field.
| http-dombased-xss: 
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=192.168.16.129
|   Found the following indications of potential DOM based XSS: 
|     
|     Source: eval("document.location.href = '"+b+"pos="+a.options[a.selectedIndex].value+"'")
|_    Pages: http://192.168.16.129:80/phpmyadmin/js/functions.js?ts=1365422810
| http-enum: 
|   /: Root directory w/ listing on 'apache/2.4.7 (ubuntu)'
|   /phpmyadmin/: phpMyAdmin
|_  /uploads/: Potentially interesting directory w/ listing on 'apache/2.4.7 (ubuntu)'
| http-slowloris-check: 
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|       Slowloris tries to keep many connections to the target web server open and hold
|       them open as long as possible.  It accomplishes this by opening connections to
|       the target web server and sending a partial request. By doing so, it starves
|       the http server's resources causing Denial Of Service.
|       
|     Disclosure date: 2009-09-17
|     References:
|       http://ha.ckers.org/slowloris/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6750
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-csrf: 
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=192.168.16.129
|   Found the following possible CSRF vulnerabilities: 
|     
|     Path: http://192.168.16.129:80/payroll_app.php
|     Form id: 
|     Form action: 
|     
|     Path: http://192.168.16.129:80/drupal/
|     Form id: user-login-form
|     Form action: /drupal/?q=node&destination=node
|     
|     Path: http://192.168.16.129:80/chat/
|     Form id: name
|_    Form action: index.php
| http-sql-injection: 
|   Possible sqli for queries:
|     http://192.168.16.129:80/?C=D%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=S%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=N%3BO%3DD%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=M%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=S%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=M%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=D%3BO%3DD%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=N%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=S%3BO%3DD%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=M%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=N%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=D%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=D%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=S%3BO%3DA%27%20OR%20sqlspider
|     http://192.168.16.129:80/?C=M%3BO%3DA%27%20OR%20sqlspider
|_    http://192.168.16.129:80/?C=N%3BO%3DA%27%20OR%20sqlspider
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
631/tcp  open  ipp
| http-slowloris-check: 
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|       Slowloris tries to keep many connections to the target web server open and hold
|       them open as long as possible.  It accomplishes this by opening connections to
|       the target web server and sending a partial request. By doing so, it starves
|       the http server's resources causing Denial Of Service.
|       
|     Disclosure date: 2009-09-17
|     References:
|       http://ha.ckers.org/slowloris/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6750
3306/tcp open  mysql
6667/tcp open  irc
|_irc-unrealircd-backdoor: Looks like trojaned version of unrealircd. See http://seclists.org/fulldisclosure/2010/Jun/277
| irc-botnet-channels: 
|_  ERROR: EOF
8080/tcp open  http-proxy
| http-slowloris-check: 
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|       Slowloris tries to keep many connections to the target web server open and hold
|       them open as long as possible.  It accomplishes this by opening connections to
|       the target web server and sending a partial request. By doing so, it starves
|       the http server's resources causing Denial Of Service.
|       
|     Disclosure date: 2009-09-17
|     References:
|       http://ha.ckers.org/slowloris/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6750
MAC Address: 00:0C:29:29:E7:FF (VMware)

Host script results:
| smb-vuln-regsvc-dos: 
|   VULNERABLE:
|   Service regsvc in Microsoft Windows systems vulnerable to denial of service
|     State: VULNERABLE
|       The service regsvc in Microsoft Windows 2000 systems is vulnerable to denial of service caused by a null deference
|       pointer. This script will crash the service if it is vulnerable. This vulnerability was discovered by Ron Bowes
|       while working on smb-enum-sessions.
|_          
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: false

NSE: Script Post-scanning.
Initiating NSE at 05:34
Completed NSE at 05:34, 0.00s elapsed
Initiating NSE at 05:34
Completed NSE at 05:34, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 330.04 seconds
           Raw packets sent: 1001 (44.028KB) | Rcvd: 1001 (40.068KB)
```

Normalmente `nmap` no es utilizado para escanear vulnerabilidades, ya que la informacion que te da es mucha por terminal y muchas veces es complicado de ver, ya que vemos que hay mcuhas vulneravilidades las que ha sacado, pero para entenderlo cuesta, por lo que podremos exportarlo a un fichero en el que se pueda ver mejor de la siguiente forma:

```shell
sudo nmap -v -sS -oX vulnerabilidades.xml --stylesheet="https://svn.nmap.org/nmap/docs/nmap.xsl" --script=vuln 192.168.16.129,132
```

Y esto lo que hara sera que toda esta informacion la exportara a un fichero `.xml` en el que se pueda visualizar mucho mejor, escaneando 2 `hosts` a la vez con el uso de una `,`(coma); viendose de tal forma:

<figure><img src="../../.gitbook/assets/image (31) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que de esta forma se pueden ver las vulnerabilidades de mucha mejor forma, pero igualmente este tipo de scripts no son 100% fiables, ya que habra algunas vulnerabilidades que no las sacara muy bien, pero para ello utilizaremos otro tipo de herramientas mas fiables.

Podemos hacer el mismo escaneo, pero en vez de hacerlo por `TCP` lo podremos hacer por `UDP` de la siguiente forma:

```shell
sudo nmap -v -sU -oX vulnerabilidades.xml --stylesheet="https://svn.nmap.org/nmap/docs/nmap.xsl" --script=vuln 192.168.16.129,132
```

Ya que lo mas probable es que nos muestre otro tipo de vulnerabilidades.
