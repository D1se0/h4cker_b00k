# Programa Remcos (Técnica RAT)

Este es un programa para controlar de forma remota cualquier equipo mediante un `.exe`, `.dll`, etc... Tiene varias extensiones, de por si la version gratuita ya tiene muchas opciones, pero la de pago, te permite un `keylogger` y demas cosas, con esto tiene el acceso total del sistema de la victima pudiendo hablar por un chat generado con la victima en el sistema, bloquearle el teclado y cualquier periferico, pudiendo activar la camara, microfono, etc... Es una herramienta muy util para auditorias de seguridad.

URL = [Download Remcos](https://breakingsecurity.net/remcos/)

Password ZIP = `BreakingSecurity.net`

Para poder utilizar esta herramienta, nos la descargaremos en ese link, seguidamente tendremos que desactivar el `Windows Defender` ya que nos lo pondra como un `malware` pero es una aplicacion legitima, ejecutaremos el `.exe` de `remcos` y se nos abrira una ventana donde podremos crear un ejecutable, elegiremos la extension, el nombre, que tipo de archivo queremos que sea, el empaquetado, etc... Una vez echo todo esto, nos iremos a `Build` donde contruiremos el ejecutable.

Una vez creado, se lo tendremos que pasar dicho ejecutable a la maquina victima, este lo tendra que ejecutar.

Una vez ejecutado, se nos creara una conexion a nuestro `workspace` de `remcos` pudiendo saber las `coordenadas` del equipo, saber tambien el sistema (`CPU, RAM, Disco Duro, etc...`), tambien podremos saber el pais, etc... Podremos saber practicamente todo, y a parte podremos ver a tiempo real lo que esta viendo el usuario y poder interactuar a tiempo real moviendole el raton, teclado, etc... Esto tiene una persistencia, por lo que si desconectamos y volvemos a conectar podremos obtener la conexion de nuevo.

Tambien hay una opcion donde se nos puede desplegar una consola de comandos en la que podremos interactuar en el equipo victima, pudiendo hacer por terminal lo que queramos.
