---
icon: user-unlock
---

# Frameworks de postexplotación - Covenant

Voy a comentar algunos de los `Frameworks` que automatizan todas las tareas que hemos mencionado anteriormente, y eso hace que nos facilite la explotacion y el reconocimiento, pero tambien hay que tener cuidado ya que al ser muy facil de utilizar y que a parte lo estara utilizando muchisima gente, las herramientas de seguirdad y este tipo de `IDS` lo puede estar detectando, por lo que hay que tener mucho cuidado con este tipo de `Frameworks`.

### Empire

Un buen `framework` para `explotacion` y `postexplotacion` en `Windows` que en su momento fue el oficial y muy famoso es el siguiente:

URL = [Empire GitHub](https://github.com/EmpireProject/Empire)

Esta dedeicado al `PowerShell` para automatizar todo, pero el propio creador ya lo tiene archivado el proyecto y hace ya un tiempo que no se actualiza, por lo que todas las herraminetas de seguridad ya lo van a detectar y sera imposible de usar a no ser que se desactive las herramientas, pero esta bien que se conozca.

### Covenant

Pero hay un `framework` mucho mejor que ha surgido realtivamente hace poco que se llama `Covenant` y esta en el siguiente repositorio:

URL = [Covenant GitHub](https://github.com/cobbr/Covenant)

Esta escrito en `.NET` y para su instalacion tendremos que irnos en la seccion de `Wiki` y en la parte de `Installation`:

URL = [Instalacion Wiki Covenant](https://github.com/cobbr/Covenant/wiki/Installation-And-Startup)

Ahora nos iremos a nuestro `kali` y tendremos que clonar el repositorio.

```shell
git clone --recurse-submodules https://github.com/cobbr/Covenant
```

Una vez echo eso haremos lo siguiente, tendremos que compilar el codigo para que funcione.

```shell
cd /Covenant/Covenant
dotnet run
```

Echo esto despues de un rato no aparecera un mensaje en el que pone que esta alojado en la siguiente direccion:

```
URL = http://127.0.0.1:7443
```

Por lo que nos meteremos en la siguiente direccion, para asi visualizar la herramienta que esta levantada en dicho puerto.

#### Listener

En esta herramienta habra varias opciones entre ellas el estar a la escucha en la seccion de `Listener` para que este escuchando en un puerto en concreto como haciamos con `netcat`.

En esta parte tambien se puede configurar para que sea de `SSL` osea que vaya cifrada la conexion para que asi las herramientas de seguridad como los `IDS` si no estan haciendo un `BreackSSL` no sabran lo que esta pasando por la red por lo que seremos indetectables.

#### Launchers

En la seccion de `Launchers` podremos seleccionar los tipos de aplicaciones en la que queremos que este el codigo malicioso en la cual cuando se ejecute se creara una `reverse shell` en el puerto e `IP` especificados, facilitando mucho la intrusion y tenemos para elegir varios lenguajes de programacion, esto es parecido a los que hacemos con la herramienta `msfvenom`.

Tambien si dentro de esta seccion nos vamos a la pestaña `host` lo que hace es que en vez de ejecutar el troncho de linea que nos proporciona, lo podemos acortar haciendo la siguiente tecnica, esta herramienta se encargara de que nosotros tendremos el ejecutable, esta misma lo descarga en la maquina victima y seguidamente lo ejecuta pudiendo obtener diferentes comandos personalizados como si tuvieramos un `meterpreter` personalizando, teniendo muchisimas funcionalidades en el mismo.

Lo unico que tendremos que ejecutar en la maquina victima suponiendo que de alguna manera hemos conseguido poder ejecutarlo sera el comando que nos porporciona la herramienta para que se lo descargue de nuestra maquina y ejecute la aplicacion maliciosa.

#### Grunts

Una vez que el codigo se haya ejecutado y se haya creado una conexion `reversa` veremos en esta seccion las conexiones con las diferentes maquinas que tenemos activas para poder interactuar con ellas mediante una terminal.

En la pestaña de `Info` te proporciona toda la informacion de la maquina victima y ya despues en la pestaña de `Interact` podemos interactuar mediante una terminal que esta integrada en la propia herramienta.

Dentro de esta terminal la terminal que nos da tiene los comandos implementados por el propio `Covenant`, pero si lo queremos ejecutar de forma local en un `cmd` seria de la siguiente forma:

```
cmd "whoami"
```

Y esto se estaria ejecutando en un `cmd`.

**Comando SharpUp**

Con el comando `SharpUp` en la termianl de `Covenant` podremos ver como escalar privilegios en caso de que no los tuvieramos y si los tuvieramos podremos ver como auditar la maquina de forma sencilla y automatica.

**Comandos generales**

Tambien podremos utilizar el comando `mimikatz` sin necesidad de que este el `mimikatz` en la maquina victima, por lo que si queremos volcar la `SAM` y tenemos privilegios de administrador local, podremos hacerlo con el comando de `mimikatz` normal el cual ya nos viene por defecto para autocompletarlo.

Tambien podremos hacer un `Rubeus` que esta implementado en `Covenant` y podremos hacer un `dump` de los `tikets` y todo lo que hemos visto anteriormente de forma automatica poniendo por ejemplo:

```
Rubeus dump
```

Y esto nos mostrara el `dump` de lo que haciamos antes con la herramienta `Rubeus.exe`.

Y con esto tambien nos podriamos hacer un `Pass-The-Ticket` y realizar diversas tecnicas que nos facilita mucho esta terminal de `Covenant`.
