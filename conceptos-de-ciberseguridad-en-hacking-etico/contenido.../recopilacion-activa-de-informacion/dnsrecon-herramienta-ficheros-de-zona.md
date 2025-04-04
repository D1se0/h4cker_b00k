---
icon: earth-oceania
---

# DNSRecon Herramienta (Ficheros de zona)

Si los servidores `DNS` de dicha organizacion estan mal configurados podremos obtener esos ficheros de zona, descargandonoslo mediante dicha herramienta, al lo que se le llama `Transferencia de zona`.

Si nos vamos a la pagina conocida `DNSdumpster` y metemos un dominio de prueba que esta preparado para este ataque llamado `zonetransfer.me`

Veremos que nos muestra bastante informacion, como los `Names Server`, `Correos`, etc... Pero en el fichero de zona cuando lo consigamos descargar, veremos que habra mucha mas informacion.

Para poder sacar esta informacion como si fuera desde la pagina pero en la terminal, lo podremos hacer de la siguiente forma:

> Para el que este utilizando mucho este tipo de herramientas `DNS` se recomienda instalar lo siguiente:

```shell
sudo apt-get install dnsutils
```

Con esto nos instala diferentes herramientas para poder utilizar al analizar temas relacionados con las `DNS`.

Por ejemplo herramientas como:

```
host
dig
nslookup
...
```

Pero en la que nos vamos a centrara dentro de todas estas herramientas es en la llamada `nslookup`.

Si ponemos lo siguiente:

```shell
nslookup
```

Nos meteremos en la linea de comandos de la herramienta, por lo que empezaremos a configurar sus respectivos para metros.

```shell
set type=ns
zonetransfer.me
```

Con `set type=ns` lo que hacemos es especificar que tipo de registro `DNS` quiero obtener, en este caso los `NS` (Name Server). A continuacion pondremos el dominio del cual queremos obtener dichos `NS`, en mi caso `zonetransfer.me`.

Y esto nos devolvera la informacion de los `Names Servers`.

```
Server:		192.168.5.2
Address:	192.168.5.2#53

Non-authoritative answer:
zonetransfer.me	nameserver = nsztm2.digi.ninja.
zonetransfer.me	nameserver = nsztm1.digi.ninja.

Authoritative answers can be found from:
nsztm2.digi.ninja	internet address = 34.225.33.2
```

Veremos que habra 2 `Names Servers` bajo ese dominio.

Por lo que ahora vamos a ver si nos envia los registros de las zona `DNS` probando de la siguiente forma:

```shell
set type=any
ls -d zonetransfer.me
```

Con `set type=any` lo que estamos haciendo es que nos envie todos los registros que contenga. Y para iniciar esta transferencia de zona lo que hacemos es poner `ls -d` y el dominio de la cual queremos extraer esos ficheros en mi caso `zonetransfer.me`

Pero en `kali` nos dira que el comando `ls` esta desactivado por medidas de seguridad, y en nuestro `host` en `windows` si hacemos esto mismo si nos dejara, pero si ponemos `set type=any` y `ls -d zonetransfer.me` nos dara como resultado `Unknow` por que no sabe de donde cogerlo, por lo que realmente habria que poner el `Name Server` bajo el que esta sujeto dicho dominio quedando de la siguiente forma:

```shell
set type=any
server nsztm1.digi.ninja
```

Info:

```
Servidor predeterminado:  nsztm1.digi.ninja
Address:  81.4.108.41
```

Y una vez echo esto, si ponemos el siguiente comando como estaba antes:

```shell
ls -d zonetransfer.me
```

Ahora si nos dara los ficheros de zona del que estabamos intentando extraer.

Info:

```
[nsztm1.digi.ninja]
 zonetransfer.me.               SOA    nsztm1.digi.ninja robin.digi.ninja. (2019100801 172800 900 1209600 3600)
 zonetransfer.me.               TXT             "google-site-verification=tyP28J7JAUHA9fw2sHXMgcCC0I6XBmmoVi04VlMewxA"

 zonetransfer.me.               MX     0    ASPMX.L.GOOGLE.COM
 zonetransfer.me.               MX     10   ALT1.ASPMX.L.GOOGLE.COM
 zonetransfer.me.               MX     10   ALT2.ASPMX.L.GOOGLE.COM
 zonetransfer.me.               MX     20   ASPMX2.GOOGLEMAIL.COM
 zonetransfer.me.               MX     20   ASPMX3.GOOGLEMAIL.COM
 zonetransfer.me.               MX     20   ASPMX4.GOOGLEMAIL.COM
 zonetransfer.me.               MX     20   ASPMX5.GOOGLEMAIL.COM
 zonetransfer.me.               A      5.196.105.14
 zonetransfer.me.               NS     nsztm1.digi.ninja
 zonetransfer.me.               NS     nsztm2.digi.ninja
 zonetransfer.me.               HINFO  Casio fx-700G  Windows XP
 _acme-challenge                TXT             "6Oa05hbUJ9xSsvYy7pApQvwCUSSGgxvrbdizjePEsZI"

 _sip._tcp                      SRV    priority=0, weight=0, port=5060, www.zonetransfer.me
 14.105.196.5.IN-ADDR.ARPA      PTR    www.zonetransfer.me
 asfdbauthdns                   AFSDB  1    asfdbbox.zonetransfer.me
 asfdbbox                       A      127.0.0.1
 asfdbvolume                    AFSDB  1    asfdbbox.zonetransfer.me
 canberra-office                A      202.14.81.230
 cmdexec                        TXT             "; ls"

 contact                        TXT             "Remember to call or email Pippa on +44 123 4567890 or pippa@zonetransfer.me when making DNS changes"

 dc-office                      A      143.228.181.132
 deadbeef                       AAAA   dead:beaf::
 dr                             29
 DZC                            TXT             "AbCdEfG"

 email                          35
 email                          A      74.125.206.26
 Hello                          TXT             "Hi to Josh and all his class"

 home                           A      127.0.0.1
 Info                           TXT             "ZoneTransfer.me service provided by Robin Wood - robin@digi.ninja. See http://digi.ninja/projects/zonetransferme.php for more information."

 internal                       NS     intns1.zonetransfer.me
 internal                       NS     intns2.zonetransfer.me
 intns1                         A      81.4.108.41
 intns2                         A      167.88.42.94
 office                         A      4.23.39.254
 ipv6actnow.org                 AAAA   2001:67c:2e8:11::c100:1332
 owa                            A      207.46.197.32
 robinwood                      TXT             "Robin Wood"

 rp                             RP     robin.zonetransfer.me  robinwood.zonetransfer.me
 sip                            35
 sqli                           TXT             "' or 1=1 --"

 sshock                         TXT             "() { :]}; echo ShellShocked"

 staging                        CNAME  www.sydneyoperahouse.com
 alltcpportsopen.firewall.test  A      127.0.0.1
 testing                        CNAME  www.zonetransfer.me
 vpn                            A      174.36.59.154
 www                            A      5.196.105.14
 xss                            TXT             "'><script>alert('Boo')</script>"

 zonetransfer.me.               SOA    nsztm1.digi.ninja robin.digi.ninja. (2019100801 172800 900 1209600 3600)
```

Con esto estariamos accediendo al fichero literar de zona de ese `Name Server` mostrando bastante mas informacion de lo que muestran otras paginas y pudiendo descubrir informacion bastante importante.

Pero para que todo esto funcione en `kali` podemos utilizar una herramienta llamada `dnsrecon` que ya viene instalada en `kali` por defecto.

Podremos hacerlo con un comando haciendo de forma automatica todo lo anterior con el siguiente comando:

```shell
dnsrecon -d zonetransfer.me -t axfr
```

Info:

```
[*] Checking for Zone Transfer for zonetransfer.me name servers
[*] Resolving SOA Record
[+] 	SOA nsztm1.digi.ninja 81.4.108.41
[*] Resolving NS Records
[*] NS Servers found:
[+] 	NS nsztm2.digi.ninja 34.225.33.2
[+] 	NS nsztm1.digi.ninja 81.4.108.41
[*] Removing any duplicate NS server IP Addresses...
[*]  
[*] Trying NS server 34.225.33.2
[+] 34.225.33.2 Has port 53 TCP Open
[+] Zone Transfer was successful!!
[*] 	SOA nsztm1.digi.ninja 81.4.108.41
[*] 	NS nsztm1.digi.ninja 81.4.108.41
[*] 	NS nsztm2.digi.ninja 34.225.33.2
[*] 	NS intns1.zonetransfer.me 81.4.108.41
[*] 	NS intns2.zonetransfer.me 52.91.28.78
[*] 	TXT google-site-verification=tyP28J7JAUHA9fw2sHXMgcCC0I6XBmmoVi04VlMewxA
[*] 	TXT 2acOp15rSxBpyF6L7TqnAoW8aI0vqMU5kpXQW7q4egc
[*] 	TXT 6Oa05hbUJ9xSsvYy7pApQvwCUSSGgxvrbdizjePEsZI
[*] 	TXT ; ls
[*] 	TXT Remember to call or email Pippa on +44 123 4567890 or pippa@zonetransfer.me when making DNS changes
[*] 	TXT AbCdEfG
[*] 	TXT Hi to Josh and all his class
[*] 	TXT ZoneTransfer.me service provided by Robin Wood - robin@digi.ninja. See http://digi.ninja/projects/zonetransferme.php for more information.
[*] 	TXT Robin Wood
[*] 	TXT ' or 1=1 --
[*] 	TXT () { :]}; echo ShellShocked
[*] 	TXT '><script>alert('Boo')</script>
[*] 	PTR www.zonetransfer.me 5.196.105.14
[*] 	MX @.zonetransfer.me ASPMX.L.GOOGLE.COM 74.125.133.26
[*] 	MX @.zonetransfer.me ASPMX.L.GOOGLE.COM 2a00:1450:400c:c0c::1a
[*] 	MX @.zonetransfer.me ALT1.ASPMX.L.GOOGLE.COM 142.250.153.26
[*] 	MX @.zonetransfer.me ALT1.ASPMX.L.GOOGLE.COM 2a00:1450:4013:c16::1b
[*] 	MX @.zonetransfer.me ALT2.ASPMX.L.GOOGLE.COM 142.251.9.27
[*] 	MX @.zonetransfer.me ALT2.ASPMX.L.GOOGLE.COM 2a00:1450:4025:c03::1a
[*] 	MX @.zonetransfer.me ASPMX2.GOOGLEMAIL.COM 142.250.153.26
[*] 	MX @.zonetransfer.me ASPMX2.GOOGLEMAIL.COM 2a00:1450:4013:c16::1b
[*] 	MX @.zonetransfer.me ASPMX3.GOOGLEMAIL.COM 142.251.9.26
[*] 	MX @.zonetransfer.me ASPMX3.GOOGLEMAIL.COM 2a00:1450:4025:c03::1b
[*] 	MX @.zonetransfer.me ASPMX4.GOOGLEMAIL.COM 142.250.150.27
[*] 	MX @.zonetransfer.me ASPMX4.GOOGLEMAIL.COM 2a00:1450:4010:c1c::1b
[*] 	MX @.zonetransfer.me ASPMX5.GOOGLEMAIL.COM 74.125.200.26
[*] 	MX @.zonetransfer.me ASPMX5.GOOGLEMAIL.COM 2404:6800:4003:c00::1b
[*] 	AAAA deadbeef.zonetransfer.me dead:beaf::
[*] 	AAAA ipv6actnow.org.zonetransfer.me 2001:67c:2e8:11::c100:1332
[*] 	A @.zonetransfer.me 5.196.105.14
[*] 	A asfdbbox.zonetransfer.me 127.0.0.1
[*] 	A canberra-office.zonetransfer.me 202.14.81.230
[*] 	A dc-office.zonetransfer.me 143.228.181.132
[*] 	A email.zonetransfer.me 74.125.206.26
[*] 	A home.zonetransfer.me 127.0.0.1
[*] 	A intns1.zonetransfer.me 81.4.108.41
[*] 	A intns2.zonetransfer.me 52.91.28.78
[*] 	A office.zonetransfer.me 4.23.39.254
[*] 	A owa.zonetransfer.me 207.46.197.32
[*] 	A alltcpportsopen.firewall.test.zonetransfer.me 127.0.0.1
[*] 	A vpn.zonetransfer.me 174.36.59.154
[*] 	A www.zonetransfer.me 5.196.105.14
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.73
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.27
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.68
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.10
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:7a00:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:7200:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:1400:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:e600:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:5a00:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:ca00:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:9800:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:8a00:7:60:4d00:93a1
[*] 	SRV _sip._tcp.zonetransfer.me www 5060 0 no_ip
[*] 	HINFO Casio fx-700G Windows XP
[*] 	RP robin robinwood
[*] 	AFSDB 1 asfdbbox
[*] 	AFSDB 1 asfdbbox
[*] 	LOC 53 20 56.558 N 1 38 33.526 W 0.00m
[*] 	NAPTR P 1 1  email.zonetransfer.me E2U+email
[*] 	NAPTR P 2 3 !^.*$!sip:customer-service@zonetransfer.me! . E2U+sip
[*]  
[*] Trying NS server 81.4.108.41
[+] 81.4.108.41 Has port 53 TCP Open
[+] Zone Transfer was successful!!
[*] 	SOA nsztm1.digi.ninja 81.4.108.41
[*] 	NS nsztm1.digi.ninja 81.4.108.41
[*] 	NS nsztm2.digi.ninja 34.225.33.2
[*] 	NS intns1.zonetransfer.me 81.4.108.41
[*] 	NS intns2.zonetransfer.me 52.91.28.78
[*] 	TXT google-site-verification=tyP28J7JAUHA9fw2sHXMgcCC0I6XBmmoVi04VlMewxA
[*] 	TXT 6Oa05hbUJ9xSsvYy7pApQvwCUSSGgxvrbdizjePEsZI
[*] 	TXT ; ls
[*] 	TXT Remember to call or email Pippa on +44 123 4567890 or pippa@zonetransfer.me when making DNS changes
[*] 	TXT AbCdEfG
[*] 	TXT Hi to Josh and all his class
[*] 	TXT ZoneTransfer.me service provided by Robin Wood - robin@digi.ninja. See http://digi.ninja/projects/zonetransferme.php for more information.
[*] 	TXT Robin Wood
[*] 	TXT ' or 1=1 --
[*] 	TXT () { :]}; echo ShellShocked
[*] 	TXT '><script>alert('Boo')</script>
[*] 	PTR www.zonetransfer.me 5.196.105.14
[*] 	MX @.zonetransfer.me ASPMX.L.GOOGLE.COM 74.125.133.26
[*] 	MX @.zonetransfer.me ASPMX.L.GOOGLE.COM 2a00:1450:400c:c0c::1a
[*] 	MX @.zonetransfer.me ALT1.ASPMX.L.GOOGLE.COM 142.250.153.26
[*] 	MX @.zonetransfer.me ALT1.ASPMX.L.GOOGLE.COM 2a00:1450:4013:c16::1b
[*] 	MX @.zonetransfer.me ALT2.ASPMX.L.GOOGLE.COM 142.251.9.27
[*] 	MX @.zonetransfer.me ALT2.ASPMX.L.GOOGLE.COM 2a00:1450:4025:c03::1a
[*] 	MX @.zonetransfer.me ASPMX2.GOOGLEMAIL.COM 142.250.153.26
[*] 	MX @.zonetransfer.me ASPMX2.GOOGLEMAIL.COM 2a00:1450:4013:c16::1b
[*] 	MX @.zonetransfer.me ASPMX3.GOOGLEMAIL.COM 142.251.9.26
[*] 	MX @.zonetransfer.me ASPMX3.GOOGLEMAIL.COM 2a00:1450:4025:c03::1b
[*] 	MX @.zonetransfer.me ASPMX4.GOOGLEMAIL.COM 142.250.150.27
[*] 	MX @.zonetransfer.me ASPMX4.GOOGLEMAIL.COM 2a00:1450:4010:c1c::1b
[*] 	MX @.zonetransfer.me ASPMX5.GOOGLEMAIL.COM 74.125.200.26
[*] 	MX @.zonetransfer.me ASPMX5.GOOGLEMAIL.COM 2404:6800:4003:c00::1b
[*] 	AAAA deadbeef.zonetransfer.me dead:beaf::
[*] 	AAAA ipv6actnow.org.zonetransfer.me 2001:67c:2e8:11::c100:1332
[*] 	A @.zonetransfer.me 5.196.105.14
[*] 	A asfdbbox.zonetransfer.me 127.0.0.1
[*] 	A canberra-office.zonetransfer.me 202.14.81.230
[*] 	A dc-office.zonetransfer.me 143.228.181.132
[*] 	A email.zonetransfer.me 74.125.206.26
[*] 	A home.zonetransfer.me 127.0.0.1
[*] 	A intns1.zonetransfer.me 81.4.108.41
[*] 	A intns2.zonetransfer.me 167.88.42.94
[*] 	A office.zonetransfer.me 4.23.39.254
[*] 	A owa.zonetransfer.me 207.46.197.32
[*] 	A alltcpportsopen.firewall.test.zonetransfer.me 127.0.0.1
[*] 	A vpn.zonetransfer.me 174.36.59.154
[*] 	A www.zonetransfer.me 5.196.105.14
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.10
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.68
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.27
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 18.154.48.73
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:8a00:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:9800:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:ca00:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:5a00:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:e600:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:1400:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:7200:7:60:4d00:93a1
[*] 	CNAME staging.zonetransfer.me www.sydneyoperahouse.com 2600:9000:24be:7a00:7:60:4d00:93a1
[*] 	SRV _sip._tcp.zonetransfer.me www 5060 0 no_ip
[*] 	HINFO Casio fx-700G Windows XP
[*] 	RP robin robinwood
[*] 	AFSDB 1 asfdbbox
[*] 	AFSDB 1 asfdbbox
[*] 	LOC 53 20 56.558 N 1 38 33.526 W 0.00m
[*] 	NAPTR P 1 1  email.zonetransfer.me E2U+email
[*] 	NAPTR P 2 3 !^.*$!sip:customer-service@zonetransfer.me! . E2U+sip
```

Y con esto ya habriamos sacado ese fichero de zona `DNS`.
