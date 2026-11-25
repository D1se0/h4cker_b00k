# Armitage (interfaz grafica de metasploit)

`Armitage` es una interfaz grafica de `metasploit` que en vez de ser por terminal es mediante una interfaz grafica y no viene instalada en `kali`, por lo que vamos a instalarla:

```shell
sudo apt-get install armitage
```

Una vez instalado, iniciaremos el servicio de `postgresql`:

```shell
service postgresql start
```

Ahora para iniciar el software, pondremos simplemente `aemitage` y nos aparecera una ventana donde dejaremos por defecto las opciones ya que nos dice que donde esta la instancia de `metasploit` corriendo, le daremos simeplemnete a `Connect`.

<figure><img src="../../../../.gitbook/assets/image (49) (1).png" alt=""><figcaption></figcaption></figure>

Nos aparecera otro popup, en el que tendremos que dar a `Si`.

Una vez que ya haya cargado todo, nos aparecera un caudro en el que nos pedira nuestra IP de atacante `kali`, por lo que se la ponemos y le daremos a `Ok`.

Y con esto de forma visual, ya podriamos utilizarlo como si estuvieramos por linea de comandos, solo que con opciones visuales, tambien podremos ver las maquinas victimas, nuestra maquina atacante, con sus diferentes opciones, etc...

Por ejemplo si le damos click derecho a una maquina y nos vamos a la opcion `Scan` escanearia todos los puertos como si fuera un `nmap` mostrandolo por una mini terminal en la parte de abajo.

Si nos vamos como si fuera una ruta `relativa` de ficheros en la parte de la izquierda, nos vamos a un `exploit` y lo seleccionamos, podremos configurarlo con el `LHOST`, `RHOSTS`, etc... Para poder lanzarlo y verlo de forma grafica la explotacion de una maquina, pudiendo mandar comandos de forma grafica con las opciones o desde la mini terminal en la parte de abajo.
