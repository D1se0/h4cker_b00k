---
icon: screencast
---

# ScreenCrab

Es un dispositivo que se utiliza pata capturar la pantalla de un equipo Victima, ya sea mediante capturas o video, pudiendo elegir la calidad de cada una de ellas, se hace la captura de una forma interna sin utilizar herramentas del sistema, por lo que es super sigiloso y nos afecta al sistema en tema de lentitud ni nada parecido.

> NOTA

Para que funcione y este alimentado el dispositivo, tendremos que tenerlo conectado en la ranura del `USB tipo C` a una toma de corriente.

## <mark style="color:purple;">Conexión/Configuración para que funcione</mark>

Lo que necesitaremos sera un cable `HDMI` extra del que ya venga en el monitor de la maquina victima, una `Micro SD` que conectaremos al dispositivo para que se guarde las capturas y los videos.

Conectando el `SD` al dispositivo y conectandolo a nuestro equipo Atacante, crearemos un archivo `.txt` en la `SD` poniendo los comandos que queremos que ejecute de captura de pantalla para el equipo victima, de primeras no habra nada en la `SD` pero cuando se le conecte, ya se crearan las respectivas carpetas y contenido del dispositivo.

Dentro del archivo `.txt` pondremos algo parecido a lo siguiente si queremos sacar capturas de pantalla en un intervalo de 5 segundos.

```txt
LED ON
CAPTURE_MODE IMAGE
CAPTURE_INTERVAL 5
STORAGE FILL
BUTTON EJECT
```

Ahora si conectamos el `HDMI` del equipo Victima al dispositivo con la `SD` ya incorporada y el segundo `HDMI` al dispositivo pero conectado al monitor Victima estara como estaba antes, pero en ese momento ya estaria ejecundose el dispositivo capturando todo como lo hayamos configurado.

Cuando lo desconectemos se parara o si presionamos un boton que tiene tambien lo hara, pero si lo desconectamos y lo dejamos como estaba antes, todo estara igual, pero cuando entremos dentro de la `SD` veremos que se añadieron varias cosas, entre ellas las que nos interesa es que donde nosotros pusimos el archivo `.txt` ahora se llamara `config` sin mas que es el que tendremos que modificar y todo se almacenara en la carpeta llamada `LOOT`.

Ahora si queremos grabar la pantalla en forma de video con intervalos de 30 segundos por cada video con una calidad maxima, pondremos lo siguiente.

```txt
LED ON
CAPTURE_MODE VIDEO
CAPTURE_INTERVAL 30
STORAGE FILL
BUTTON EJECT
VIDEO_BITRATE HIGH
```

Y solo tendremos que seguir el mismo proceso de antes.

### Antena del ScreenCrab

Se utiliza para que el dispositivo se pueda conectar a un `Punto de acceso` y desde ahi poder transmitir en tiempo real la pantalla de la Victima a un `C2 (Command And Control)` es un software que se tendra que descargar.

URL = [Pagina C2 Hack5](https://shop.hak5.org/products/c2?srsltid=AfmBOooq11iVSJiQPKTFs4pBW42xd7hNGAxxl2yBJzuG-uztcYpodbW2)

Y una vez descargado seria ejecutarlo en local en tu equipo Atacante.

```cmd
.\c2-3.2.0_amd64_windows.exe -listenip 0.0.0.0 -listenport 4646 -hostname <IP>
```

Y esto lo que hace es que en el equipo por dentro monta un servicio web con el que nos podremos conectar en internet con esa IP y puerto para visualizar lo que este llegando a tiempo real.

```
URL = localhost:4646
```

Y esto te llevara al software de `C2` por lo que nos tendremos que logear con nuestra cuenta y una vez hecho todo eso tendremos que añadir un dispositivo.

Dandole a `Add Device` nos abrira una ventana en la que tendremos que configurar la informacion del dispositivo que estemos creando (nombre, tipo de dispositivo, etc...):

```
Name = <NAME_DEVICE>
Device Type = Screen Crab
New Device Description = Screen Crab Demo
```

Le daremos a `Add Device` y esto nos añadira el dispositivo al sitio web.

Pinchando en el dispositivo, entraremos dentro del mismo, le daremos al boton `Setup` que nos descargara un archivo llamado `device.config` que sera el cual tendremos que pegar en la raiz de la `SD`, pero tambien tendremos que decir que se conecte el `ScreenCrab` a un punto de acceso para que esto funcione cambiando la configuracion del siguiente archivo llamado `config` que tendra que tener una estructura como esta:

```txt
WIFI_SSID "<NAME_WIFI>"
WIFI_PASS "<PASSWORD_WIFI>"
```

Ahora esta `SD` tendremos que meterlo en el `ScreenCrab`, conectarlo todo con sus `HDMI` del equipo Victima al `ScreenCrab` y del `ScreenCrab` al monitor Victima.

Cuando se conecte podremos ver en el equipo Atacante donde el sitio web en el dispositivo que creamos, vemos un pico de conexion en la seccion de `Uptime History`, el `Uptime` estara activo, al igual que el `Total Rx/Tx` y en `Online Clients` veremos un `1`.

Si nos vamos a la pestaña de `Configuration` veremos las opciones de captura y la pantalla del usuario Victima donde se estara capturando todo a tiempo real, pero para que sea mas rapido todo en la opcion llamada `Capture Intervale` lo establecemos en 5 segundos, Activamos la opcion llamada `Image Capture De-duplication` y si lo quieres en video se podra cambiar la opcion de `Capture Mode` en la opcion de `Video` en vez de `Still Image`.
