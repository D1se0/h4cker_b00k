# BONUS (Explotando un fallo de seguridad en Windows 10)

En el protocolo llamado `registro remoto` de `Windows` no implementa medidas de seguridad como por ejemplo el cifrado o el firmado de la informacion, por lo tanto era susceptible de ser modificado en tiempo real.

El registro de una maquina `Windows` es un almacen jerarquico de informacion que tiene desde informacion de configuracion de aplicaciones que se encuentran en espacio de usuario hasta parametros de configuracion de otros modulos, por ejemplo del sistema operativo, pero a demas de esto tambien se encuentran algunas claves de este registro donde podemos encontrar rutas a diferentes binarios que se ejecutan por ejemplo cuando el sistema opertivo se reinicia, cuando el sistema operativo se inicia, ejecuta una serie de aplicaciones en el `Startup` del sistema operativo y esas aplicaciones vienen definidas en el registro de la maquina.

Por lo que si nosotros tenemos la capacidad de poder escribir o manipular en cualquier parte del registro de `Windows` esto tiene las consecuencias de que vamos a ser capaces de ejecutar codigo de manera remota en esa maquina `Windows`.

Tendremos que encender 2 maquinas `Windows` mas la de `kali`, entre ellas `Windows 10` y `Windows Server 2008 Metasploitable`.

> NOTA

Tambien se podria con 2 maquinas `Windows` totalmente normales.

Abriremos la herramienta `polymorph` en `kali` y envenenaremos la red con el `ARP Spoofing`:

```shell
spoof -t 192.168.16.138 -g 192.168.16.137
```

Si nos vamos a la maquina `Windows 10`, tendremos que irnos a los registros de la siguiente forma, pulsaremos `Windows + R` y escribiremos `regedit`.

Lo que vamos hacer con la tecnica es lo que haya establecido el administrador se lo vamos a modificar en la clave de una rama del registro de una maquina remota.

Para ello tendremos que acceder de forma remota al registro, para empezar la maquina tiene que tener corriendo un servicio que es el servicio de registro remoto. (`Remote Registre`)

Pero en maquinas como `Windows Server` es muy comun ver estos servicios corriendo, ya que se suelen utilizar mucho.

Por lo que vamos a modificar de forma remota los registros de la maquina `Windows Server` desde la maquina `Windows 10`.

Desde el propio `regedit` de `Windows 10` podemos darle a `File` -> `Connect Network Registry...` y nos aparecera esto:

<figure><img src="../../../../.gitbook/assets/image (132) (1).png" alt=""><figcaption></figcaption></figure>

Y en la parte de `Escriba el nombre de objeto paar seleccionar` pondremos la IP de la maquina `Windows Server 2008`:

<figure><img src="../../../../.gitbook/assets/image (133) (1).png" alt=""><figcaption></figcaption></figure>

Le damos `Aceptar` y al cavo de unos segundos nos aparecera un recuadro para meter las credenciales de la maquina `Windows Server` que seria:

```
User: vagrant
Pass: vagrant
```

Una vez que nos hayamos conectado, veremos esto:

<figure><img src="../../../../.gitbook/assets/image (134) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que si nosotros por ejemplo entramos en `HKEY_USERS` -> `S-1-5-18` -> pulsamos `Control Panel` (Por ejemplo) -> hacemos doble click en el registro `(Default) REG_SZ` y lo establecemos su `data` en `testvalue` viendose algo asi:

<figure><img src="../../../../.gitbook/assets/image (135) (1).png" alt=""><figcaption></figcaption></figure>

Si nos vamos ahora a la maquina `Windows Server` y en el `regedit` nos vamos a la misma ubicacion donde hemos cambiado ese registro.

`HKEY_USERS` -> `S-1-5-18` -> `Control Panel` -> `(Default) REG_SZ` este registro lo veremos con la `data` como `testvalue` por lo que funciono correctamente y se cambia desde una maquina a otra.

<figure><img src="../../../../.gitbook/assets/image (136) (1).png" alt=""><figcaption></figcaption></figure>

Todos estos paquetes se mandan mediante el protocolo `WINREG`, por lo que se capturamos con `wireshark` el trafico de red y lo filtramos por dicho protocolo, podremos ver todos los paquetes que se han intercambiado.

Pero hay un paquete en concreto que es el que nos interesa el llamado `SetValue request` que suele aparecer abajo del todo, es el que lleva toda la informacion que nosotros estamos estableciendo en una clave concreta, si nos vamos al contenido del paquete vemos que tiene varias capas de red, pero entre ellas esta la llamada `Remote Registry Service, SetValue` que es la que nos interesa y si abrimos dicha capa vemos que tenemos abajo del todo una llamada `Long Frame` que es el valor que nosotros estabamos estableciendo a dicha clave de registro.

Y como vemos la informacion no va cifrada, va en texto plano, se puede leer.

El campo que identifica dicho paquete se le llama `opnum` y en este caso esta con el valor `22`.

Llendonos a la herramienta `polymorph` en `kali` vamos a empezar a capturar paquetes del protocolo `winreg`:

```shell
capture -f winreg
```

Nos volvemos al `windows` y cerramos `regedit` y lo volvemos abrir, nos volvemos a conectar y volvemos a modificar el mismo registro.

Una vez echo esto, volvemos a `kali` y pausaremos la captura, por lo que nos dira `polymorph` que capturo entorno a `259` paquetes.

Vamos abrirlo con `wireshark` llendonos abajo del todo normalmente es el penultimo paquete donde pone `SetValue request` entonces sabiendo que es el penultimo en `wireshark` en la herramienta `polymorph` pondremos `show` y seleccionaremos el penultimo numero que en mi caso es el `258`:

```shell
template 258
```

Si hacemos un `show` de dicho paquete, veremos toda la informacion del mismo.

Hay muchas veces que `polymorph` no te detecta como campo el texto que se esta intercambiando entre los registros, por lo que no te lo va a mostrara directamente en la herramienta, pero si nosotros ejecutamos el siguiente comando:

```
dump
```

Podremos ver que nos vuelca todos los `bytes` de este paquete y aqui si que podremos ver la cadena de texto de la informacion que se ha enviado.

Y esta cadena de `bytes` en la herramienta se asocia en el protocolo `DCERPC` en la seccion de `FT_HEX payload_stub_data=` podremos ver una cadena de `hexadecimal` el cual se asocia con el `dump` que hemos echo, solo tendriamos que detectar en `hexadecimal` cual es el valor que se esta intercambiando que ya te lo dice en el propio `dump`.

Ahora vamos acceder a la capa `winreg`:

```shell
layer winreg
```

Y si hacemos `show` solo nos aparecera la informacion de la capa `winreg` de dicho paquete.

Y aqui vamos a crear un campo:

```shell
field -a winreg_value
```

Cuando le demos a `ENTER` nos dira `polymorph` que le especifiquemos el `byte` de comienzo donde queremos añadir esto que seria donde esta la informacion que se esta intercambiando `testvalue` en nuestro caso, para seleccionar desde que `byte` a que `byte` comienza y termina, si nos vamos a `wireshark` y seleccionamos el paquete en la informacion del paquete donde esta la `data` del registro que se esta intercambiando, abajo a la derecha aparece un numero seguido de un `-` con otro numero y esos serian los `bytes` en mi caso seria `278-305`.

Pero nosotros queremos coger la primera letras que seria la `t` y la ultima que seria la `e`, por lo que habria que contar hasta la `t` en mi caso seria el `282` y hasta la letra `e` seria en el `300`, por lo que le diremos a `polymorph` el primer `byte` seria el `282` y cuando nos vuleva a pedir intoducir otro numero sera el `byte` en el que termina que en mi caso seria el `300` aproximadamente.

Despues nos dira de que queremos que sea el tipo de campo, en nuestro caso de `bytes` por lo que elegiremos el `4`.

Y con esto ya nos habria agregado el campo, por lo que si le damos a `show` veremos nuestro nuevo campo llamado `winreg_value`.

Ahora nos iremos atras con `back`, por lo que crearemos una funcion que modifique este tipo de paquetes y aprovechar el campo que acabamos de crear para referenciarlo y modificar su valor.

```shell
functions -a winreg_set_value -e nano

#Dentro del nano

def winreg_set_value(packet)
	try:
		if packet['DCERPC']['opnum'] == 22
			packet['WINREG']['winreg_value'] = b'a\x00t\x00t\x00a\x00c\x00k\x00e\x00r\x00r\x00'
		print("Paquete Set Value modificado!!!")
		return packet
	except:
		return packet
```

Lo que estamos haciendo aqui es modificar el contenido del valor del registro de la cadena de `testvalue` a la de `attackerr`.

Tambien hacemos una especie de seguridad para que no de un error y con otros paquetes de red, por si coincidiera el caso de este tipo de protocolo poniendo el `Try` y `except`.

Una vez que hayamos terminado, lo guardamos todo y nos pondremos a interceptar los paquetes:

```shell
intercept
```

Ahora en la maquina `Windows` modificaremos el valor de `testvalue` por otra vez `testvalue`, poner el mismo valor.

Si nos vamos a la maquina `Windows Server` y pinchamos en otro registro y volvemos al mismo para recargarlo, veremos que el valor que se ha puesto es el de `attackerr` en vez de el de `testvalue`.

Y si nos vamos a la maquina `kali` veremos lo siguiente:

```
Paquete Set Value modificado!!!
```

Por lo que se ejecuto todo correctamente.

Y con este mismo metodo no solo podemos manipular ese campo, si no, todos los campos, incluidos los que abren las claves, pudiendo engañar al administrador y asi que ponga una clave que nosotros queramos en vez de la que ponga el administrador.

Y toda esta informacion de como se hace todo este tipo de tecnica esta recogida en el siguiente link:

URL = [Tecnica Info Extra Winregmitm](https://github.com/shramos/winregmitm)
