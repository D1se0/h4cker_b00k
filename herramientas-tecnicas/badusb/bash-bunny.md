---
icon: rabbit
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

# Bash Bunny

Aparentemente es un pendrive que se utiliza mucho en el hacking y es el favorito de los hackers, ya que puede hacer diversas cosas, desde fuera parece un simple pendrive, pero en su interior cuenta con un `Sistema Operativo Linux`, `Procesador de 4 nucleos`, `CHIP SSD de hasta 8GB` y `512MB/1GB de memoria RAM`.

Dispone tambien de `Bluetooth` para hacer conexiones remotas hacia el dispositivo.

Tiene una LED en la parte inferior para notificarnos en cada momento como se encuentra nuestro ataque y es totalmente programable tambien.

Tiene un boton en la parte lateral de deslizamiento con 3 opciones de deslizamiento y estas sirven para cargar diferentes `payloads` dependiendo en la posicion en la que se lo dejemos.

## <mark style="color:purple;">Funciones del boton</mark>

Si dejamos el boton en el modo 3 (Por defecto) lo estariamos dejando en `Modo Armamento` que sirve para que cuando lo conectes al PC actue como una simple `unidad de almacenamiento` la cual se utilizara para guardar nuestros `payloads`.

Dentro del pendrive hay diversas carpetas donde `loot` es la carpeta donde se volcara la informacion extraida dependiendo de lo que hayamos configurado, la carpeta `payloads` contendra muchas cargas utiles, como `Reverse Shell`, `Phishing`, `recoleccion de datos`, etc... para todo tipo de sistemas operativos y tambien habra 2 carpetas llamadas `Switch1` y `Switch2`, las cuales haran referencia a los 2 botones del pendrive.

## <mark style="color:purple;">Payload de recolección (Ejemplo)</mark>

Nos iremos al directorio `Library` y aqui es donde estan las diferentes tecnicas, escogeremos en este caso la carpeta `recon` (para recolectar informacion del sistema victima o de las carpetas que queramos), picharemos en el primero llamado `-BB-ADV-Recon` y utilizaremos el script llamado `ADV-Recon.ps1` (Esta en `Power Shell`) y tambien tendremos que coger el archivo `payload.txt`, estos 2 archivos se cogen por el simple hecho hacer todo el reconocimiento del equipo.

Haremos `Ctrl+C` a los 2 archivos y los pegaremos (`Ctrl+V`) en la carpeta llamada `Switch1` para que cuando dejemos el `boton 1` del pendrive se ejecute ese script al introducirlo en el PC.

Ahora solo tendremos que desconectarlo del nuestro PC Atacante y conectarlo con el `Boton 1` al PC Victima.

### Funcion una vez conectado al PC Victima

Automaticamente se ejecutaria el script en cuestion de segundos y ya se habria cargado toda la informacion de lo que haga el script en nuestro pendrive, ya digo, en cuestion de segundos, cuando salte el mensaje de `Script done` podremos quitar el pendrive.

Ahora pondremos el pendrive `Bash Bunny` en el `Boton 3` para poderlo meter en nuestro PC Atacante y ver la informacion recolectada en la siguiente carpeta, nos vamos a la carpeta `loot` y dentro se nos habra creado una carpeta llamada `ADV-Recon` donde habra volvado toda la informacion del PC Victima, y dentro de la misma habra otra carpeta que se llamara como el nombre que se le haya puesto al equipo, ya que el script coge el nombre del equipo y te crea la carpeta con dicho nombre donde estara la informacion del equipo victima.

Y dentro del mismo habra un `.txt` que es un `log` de toda la informacion del equipo sensible en forma de texto.

## <mark style="color:purple;">Payload de exfiltración (Ejemplo)</mark>

Si con la tecnica anterior hemos descubierto alguna ruta de carpetas interesante para poder descargarnos algun archivo de la misma, podremos utilizar un script de `exfiltracion` para podernos pasar varios archivos de la maquina victima a la maquina atacante.

Nos iremos a la carpeta `library`, dentro de ella nos iremos a `exfiltration`, despues nos iremos a `Powershell_TCP_Extractor` y nos abriremos el archivo de `powershell` que habra que retocar llamado `copyMoveData.ps1`.

Dentro del script cambiaremos la IP que tendremos que poner nuestra IP de atacante donde quiero que me lleguen todos los archivos y el puerto por el que tengo configurado mi servidor a la escucha para que me lleguen los archivos de la maquina victima y la extension de los archivos que queremos que busque el script como por ejemplo `.txt, .kdbx, etc...` en la seccion de `edit include to specify filetypes...` y despues decir por el directorio donde queremos que realice la busqueda, como en el anterior script sabemos que directorio es pondremos ese mismo nombre en la seccion correspondiente del script, el script ya pilla automaticamente el nombre del equipo por lo que pondremos algo como `Desktop` en la seccion de `$ENV:UserProfile\Desktop` de esta manera.

Una vez hecho todo lo anterior copiaremos los 3 archivos llamados `copyMoveData.ps1`, `d.cmd` y `payload.txt`, los moveremos a la carpeta `Switch2` por ejemplo y los pegaremos en esa carpeta.

Ahora seria el mismo proceso de antes, desconectarlo del equipo Atacante, cambiar al `Boton2` y conectarlo al equipo Victima.

Y estando en nuestro equipo Atacante con el siguiente comando:

```shell
nc -lvnp <PORT> > datos.zip
```

Cuando se ejecute el script en la maquina victima, nos llegara toda la informacion a nuestra maquina atacante.

## <mark style="color:purple;">Payload Sticky Key (Ejemplo)</mark>

Pongamos que el equipo Victima siempre bloquea Windows estando en la pantalla de login pero si por un momento tenemos el equipo desbloqueado podremos aprovechar con el pendrive `Bash Bunny` la tecnica de `Sticky Key` para que si se bloqueara en un futuro poder pasar este login de forma rapida abriendonos una terminal autenticada como administrador y pudiendo cambiar la contraseña del usuario.

Estando en el `Boton3` del pendrive, lo introduciremos en nuestro equipo Atacante y nos iremos a la siguiente carpeta llamada `library`, despues a `execution`, nos iremos a `StickyBunny` y dentro de la carpeta copiaremos el archivo llamado `payload.txt`, lo pegaremos en la carpeta `Switch1` habiendo borrado lo anterior.

Una vez echo esto desconectaremos el pendrive, lo cambiaremos al `Boton1` y lo conectaremos al equipo Victima y en cuestion de segundos se habria completado todo el proceso.

Si se bloqueara de nuevo el equipo Victima, pulsando 5 veces la tecla `Shift` se nos habrira una terminal en la que podremos cambiar el password al usuario y poder entrar.

## <mark style="color:purple;">Payload Credentials (Ejemplo)</mark>

Con este pendrive tambien se puede robar las credenciales de un usuario de la siguiente forma.

Conectado el pendrive con el `Boton3` al equipo Atacante, nos iremos a la carpeta `library`, despues a la carpeta `Credentials`, de ahi nos vamos a `-BB-Credz-Plz` y dentro del mismo nos copiaremos 2 archivos llamados `Credz-Plz.ps1` y `payload.txt`, lo pegaremos en la carpeta llamada `Switch1` habiendo borrado lo anterior.

Si desconectamos el pendrive del equipo y lo ponemos en el `Boton1`, y lo conectamos en el equipo Victima, se nos cargara un script especial, en el que aparecera una ventana pequeña donde se mostrara el nombre de usuario del equipo y un campo de contraseña, donde la victima insertara la contraseña, ya que si lo intentar cerrar se volvera abrir en forma de bucle y cuando inserta 2 veces la contraseña, se detiene y es cuando podremos extraer el pendrive ponerlo en el `Boton3` y conectarlo en nuestro equipo Atacante.

Si nos vamos a la carpeta `loot` tendremos una carpeta llamada `Credz-Plz`, que dentro de ella estara otra carpeta con el nombre del equipo y dentro de la misma, estara un archivo `.txt` que contendra las credenciales que se metieron en la maquina Victima junto a la informacion del usuario, dominio, etc...

## <mark style="color:purple;">Payload phishing (Ejemplo)</mark>

Poniendo el pendrive en el `Boton3`, lo conectamos en nuestro equipo Atacante, nos vamos al carpeta `library`, de ahi a la carpeta `phishing`, dentro de ella habra muchas tecnicas, pero entre ellas elegiremos la carpeta `windows10_fakelogonscreen` y copiaremos los 2 recursos llamados `payload.txt` y `phishing_files`, lo pegaremos en la carpeta llamada `Switch1` borrando todo lo anterior.

Ahora lo desconectaremos del equipo Atacante y poniendolo en el `Boton1` lo conectaremos en el equipo Victima.

> NOTA

Este script lo que hace es que simulara un login en el que el usuario victima introducira las credenciales y esto nos llegara a un servidor que tengamos nosotros en la maquina Atacante.

Una vez que conectemos el pendrive en la maquina Victima en cuestion de segundos, montara una especie de `HTML` simulando el login de Windows con el nombre de usuario del equipo y se aumentara en un `F11` para que parezca que es el verdadero login de Windows.

Y cuando el usuario introduzca el password, viajara hasta mi servidor, que se podra hacer de muchas formas como por ejemplo con el siguiente comando:

```shell
php -S 0.0.0.0:4646
```

Una vez que lo recibamos, podremos hacer `Ctrl+C` para cerrar el servidor y pondremos el siguiente comando para leer su contenido.

```shell
cat <NAME>_loot.log
```

Esto nos dara informacion de la IP, los navegadores, el nombre de usuario y la contraseña que introdujo.

Y la plantilla se puede cambiar a la que mas guste programandote una propia si se quisiera.

## <mark style="color:purple;">Payload Remote\_access (Ejemplo)</mark>

Si queremos tener una consola interactiva desde nuestro equipo Atacante a la del equipo Victima haremos lo siguiente.

Con el pendrive en el `Boton3` lo conectamos en nuestro equipo Atacante y nos vamos a la carpeta llamada `library`, despues a `remote_access`, dentro de la misma a `WindowsPersistentReverseShell` y dentro copiaremos 3 archivos llamados `payload.txt`, `persistence.vbs` y `run.ps1`, pegaremos todo esto en la carpeta llamada `Seitch1` borrando todo lo anterior.

> NOTA

Esta tecnica es muy eficiente ya que estaremos creando una persistencia, por lo que si se nos fuera la consola o pasara algo, podremos volver a ganar acceso sin que este el pendrive o cuando queramos para siempre.

Ahora desconectamos el pendrive del equipo Atacante, lo ponemos con el `Boton1` y lo conectamos en el equipo Victima, en cuestion de segundos se ejecutaria el script y estando a la escucha en nuestra maquina Atacante se nos crearia una shell interactiva al equipo Victima.

```shell
rlwrap nc -nlvp 4646
```

Si perdieramos la shell, solamente tendremos que volver a poner ese comando y volveremos a ganar acceso al sistema.

Esto tambien se podria utilizar para hacerlo mediante metasploit, con otros scripts.

## <mark style="color:purple;">Resumen</mark>

Con esta herramienta se pueden hacer muchas cosas, esto esta muy bien para utilizarlo en forma de pentesting o para hacer pruebas en entornos controlados y protegernos frente a estas herramientas.
