---
icon: fish-fins
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

# Nikto y Skipfish

Alguna otra alternativa que podriamos probar seran estas herramientas llamadas `Nikto` y `Skipfish` que tambien soon muy buenas para encontrar vulnerabilidades web.

`Nikto` viene por defecto en `kali`, esta herramienta es muy sencillita de utilizar, si por ejemplo queremos investigar la siguiente `URL`, haremos lo siguiente:

```shell
nikto -h http://192.168.5.211:8080 -o report.html -Format html
```

Lo que hacemos con `-o` es generar un reporte de lo que encuentre. Con el `-Format` es el formato que queremos para el reporte en mi caso `HTML`.

Info:

```
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          192.168.5.211
+ Target Hostname:    192.168.5.211
+ Target Port:        8080
+ Start Time:         2025-01-31 04:49:28 (GMT-5)
---------------------------------------------------------------------------
+ Server: Apache/2.4.7 (Ubuntu)
+ /: Retrieved x-powered-by header: PHP/5.5.9-1ubuntu4.14.
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ Root page / redirects to: portal.php
+ /passwords/: Directory indexing found.
+ /robots.txt: Entry '/passwords/' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /documents/: Directory indexing found.
+ /robots.txt: Entry '/documents/' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /robots.txt: Entry '/admin/' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /images/: Directory indexing found.
+ /robots.txt: Entry '/images/' is returned a non-forbidden or redirect HTTP code (200). See: https://portswigger.net/kb/issues/00600600_robots-txt-file
+ /robots.txt: contains 5 entries which should be manually viewed. See: https://developer.mozilla.org/en-US/docs/Glossary/Robots.txt
+ Apache/2.4.7 appears to be outdated (current is at least Apache/2.4.54). Apache 2.2.34 is the EOL for the 2.x branch.
+ /login.php: Cookie PHPSESSID created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /web.config: ASP config file is accessible.
+ /test.php?%3CSCRIPT%3Ealert('Vulnerable')%3C%2FSCRIPT%3E=x: OmniHTTPD's test.php is vulnerable to Cross Site Scripting (XSS). See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-1455
+ /phpinfo.php: Output from the phpinfo() function was found.
+ /admin/: This might be interesting.
+ /apps/: Directory indexing found.
+ /apps/: This might be interesting.
+ /db/: Directory indexing found.
+ /db/: This might be interesting.
+ /passwords/: This might be interesting.
+ /stylesheets/: Directory indexing found.
+ /stylesheets/: This might be interesting.
+ /admin/index.php: This might be interesting: has been seen in web logs from an unknown scanner.
+ /phpinfo.php: PHP is installed, and a test script which runs phpinfo() was found. This gives a lot of system information. See: CWE-552
+ /admin/phpinfo.php: Output from the phpinfo() function was found.
+ /admin/phpinfo.php: Immobilier allows phpinfo() to be run. See: https://vulners.com/osvdb/OSVDB:35877
+ /config.inc: DotBr 0.1 configuration file includes usernames and passwords. See: OSVDB-5092
+ /update.php: Cookie admin created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /update.php: Cookie movie_genre created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /update.php: Cookie secret created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /update.php: Cookie top_security created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /update.php: Cookie top_security_nossl created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /update.php: Cookie top_security_ssl created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /install.php: install.php file found.
+ /icons/README: Apache default file found. See: https://www.vntweb.co.uk/apache-restricting-access-to-iconsreadme/
+ /login.php: Admin login page/section found.
+ /test.php: This might be interesting.
+ 8913 requests: 0 error(s) and 39 item(s) reported on remote host
+ End Time:           2025-01-31 04:49:49 (GMT-5) (21 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Vemos que nos muestra mucha informacion aqui, pero si ahora abrimos el archivo que nos genero de la siguiente forma:

```shell
sudo open report.html
```

<figure><img src="../../.gitbook/assets/image (262).png" alt=""><figcaption></figcaption></figure>

Veremos que que nos muestra mucha mas informacion de forma que es mas visual que en la terminal, por lo que ya seria investigar.

Despues podremos ver la otra herramienta llamada `Skipfish` que tambien esta por defecto en `kali`.

```shell
skipfish -o report http://192.168.5.211:8080
```

Info:

```
skipfish version 2.10b by lcamtuf@google.com                                            
                                                                                                                                                                                            
  - 192.168.5.211 -                                                                     
                                                                                                                                                                                            
Scan statistics:                                                                   
                                                                                                                                                                                            
      Scan time : 0:00:05.893                                                       
  HTTP requests : 18305 (3105.7/s), 31913 kB in, 4495 kB out (6177.2 kB/s)         
    Compression : 2428 kB in, 9913 kB out (60.6% gain)                             
    HTTP faults : 0 net errors, 0 proto errors, 0 retried, 0 drops                    
 TCP handshakes : 197 total (92.9 req/conn)                                           
     TCP faults : 0 failures, 0 timeouts, 11 purged                                
 External links : 384 skipped                                                        
   Reqs pending : 0                                                                
                                                                                                                                                                                            
Database statistics:                                                               
                                                                                                                                                                                            
         Pivots : 79 total, 76 done (96.20%)                                       
    In progress : 0 pending, 0 init, 0 attacks, 3 dict                             
  Missing nodes : 8 spotted                                                        
     Node types : 1 serv, 8 dir, 50 file, 7 pinfo, 1 unkn, 12 par, 0 vall           
   Issues found : 31 info, 0 warn, 1 low, 0 medium, 0 high impact                  
      Dict size : 78 words (78 new), 9 extensions, 256 candidates                  
     Signatures : 77 total                                                         
                                                                                                                                                                                            
[+] Copying static resources...                                                    
[+] Sorting and annotating crawl nodes: 79                                         
[+] Looking for duplicate entries: 79                                              
[+] Counting unique nodes: 60                                                      
[+] Saving pivot data for third-party tools...                                     
[+] Writing scan description...                                                    
[+] Writing crawl tree: 79                                                         
[+] Generating summary views...                                                    
[+] Report saved to 'report/index.html' [0x9fa0d1ed].                              
[+] This was a great day for science! 
```

Y con esto veremos que nos genero correctamente el reporte encontrando varias cosas, vamos abrir el reporte:

```shell
sudo open report/index.html
```

Info:

<figure><img src="../../.gitbook/assets/image (263).png" alt=""><figcaption></figcaption></figure>

Vemos que nos lo muestra muchisimo mejor que `nikto` por lo que son dos herramientas muy buenas para encontrar vulenrabilidades web.
