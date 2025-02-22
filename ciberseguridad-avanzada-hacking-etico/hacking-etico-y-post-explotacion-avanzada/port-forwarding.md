---
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

# Port Forwarding

En lo que consiste esta tecnica es que una conexion en internet a nuestro `Router` concretamente a un puerto de nuestro `Router` se redirija a un puerto de uno de los sistema que se encuentran en nuestra red local, de esta manera podemos establecer una conexion desde internet a una maquina que se encuentra en una red local.

Vamos a encender las `2` maquinas `Windows` que son las `WS01` y `WS02`, vamos a realizar una conexion reversa con la maquina `WS02` con `metasploit` para obtener un `meterpreter`.

Una vez que lo hayamos obtenido, vamos a imaginar que tenemos un servicio corriendo vulnerable en la maquina llamada `WS02` con la que tenemos la `reverse shell`, ya que hemos podido obtener acceso a dicha maquina de una forma o de otra con un `meterpreter`, pero ese servicio tiene limitaciones ya que esta controlado por un `firewall` local, algo que es muy frecuente.

Para poder emular ese servicio corriendo vulnerable en `Windows` vamos a instalar `netcat` para poder emularlo de la siguiente forma:

URL = [Download Netcat](https://nmap.org/ncat/)

Pinchamos en `here` para que se nos descargue el `ZIP` y una vez que nos lo hayamos descargado, nos lo pasamos a la maquina `WS02`, tendremos que descomprimir el `ZIP`, si nos lo detecta como un `malware` desactivamos el antivirus y seguimos con el proceso, abriremos una `PowerShell` y nos iremos dentro de la carpeta descomprimida para poder ejecutar el `netcat`.

```powershell
cd .\Desktop\
cd .\ncat-portable-5.59BETA1\
.\ncat.exe -lvp 23
```

Por ejemplo si ejecutamos eso, estamos simulando tener un puerto abierto en el `23` como si fuera vulnerable.

Nos saldra si queremos `Permitir` o `Cancelar` el que sea accesible a redes publicas esta escucha, en este caso le daremos a `Cancelar` ya que en una organizacion real, esto estara todo en local y no podra ser accesible de forma externa.

Info:

```
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Listening on 0.0.0.0:23
```

Si nosotros intentamos conectarnos con `netcat` desde nuestro `kali` no va a funcionar, ya que nuestro `firewall` de `Windows` esta bloqueando todas las conexiones entrantes de forma externa para que dicho servicio no se exponga en la red, de ahi la necesidad de tener que realizar un `Port Forwarding` con la `shell reversa` que tenemos.

Pongamos que hemos descubierto que el servicio que corre en el puerto `23` tiene una vulnerabilidad y tenemos un script para explotarla, pero no lo podremos hacer de forma externa, y como tenemos una `shell` con la maquina `WS02` podremos realizar dicha tecnica para poder explotarlo de forma interna.

Teniendo el `meterpreter` de `metasploit` lo que haremos sera lo siguiente:

```shell
portfwd add -l 135 -p 23 -r 192.168.5.209
```

Lo que estamos haciendo con el `add` es añadir en el puerto `135` que sabemos que esta abierto, por que si no la maquina no funciona en `Windows` la tecnica del `Port Forwarding`.

Con el `-l` especificamos el puerto que queremos utilizar, que tiene que estar activo en la maquina victima.

Con el `-p` especificamos que nos canalice el puerto `135` del puerto que queremos hacer conexion en este caso el puerto `23` desde nuestro `host`, por lo que cuando nosotros enviemos informacion se la estaremos enviando al puerto `135` pero este lo canaliza y se la envia al `23`.

Con el `-r` especificamos la maquina victima.

Para poder ver que puertos tiene activo la maquina victima para ponerlo en el `-l`, sera de la siguiente forma:

```shell
sudo nmap -sS -n 192.168.5.209
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-10 06:01 EST
Nmap scan report for 192.168.5.209
Host is up (0.00046s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:0C:29:B6:61:8B (VMware)

Nmap done: 1 IP address (1 host up) scanned in 4.34 seconds
```

Info (Comando `portfwd`):

```
[*] Forward TCP relay created: (local) :135 -> (remote) 192.168.5.209:23
```

Ahora si realizamos lo siguiente:

```shell
netcat 127.0.0.1 135
```

Lo que estamos haciendo es que nos estamos conectando de forma local en nuestro `host` en el puerto que le especificamos de la `135` pero cuando enviemos dicha informacion por ahi, lo que hara sera canalizarlo y enviarlo al puerto `23` de la maquina victima.

Escribimos lo siguiente:

```
hola
que tal
adios
```

Y si nos vamos a la maquina victima y vemos el `PowerShell` donde estaba a la escucha con ese puerto activado del `23` que desde fuera no dejaba hacer esta conexion...

```
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Listening on 0.0.0.0:23
Ncat: Connection from 192.168.5.209:49562.
hola
que tal
adios
```

Por lo que vemos ha funcionado de forma correcta, pero si en este caso el puerto esta en la maquina `WS01` y tenemos una `shell` en `WS02`, lo que podemos hacer es la misma tecnica anterior, pero con la `IP` de la maquina `WS01` de la siguiente forma:

Primero eliminaremos `portfwd` el anterior:

```shell
portfwd delete -i 1
```

Y ahora lo configuraremos para la maquina `WS01`:

```shell
portfwd add -l 135 -p 23 -r 192.168.5.208
```

Y con esto ya lo tendriamos canalizado a la maquina `WS01`.
