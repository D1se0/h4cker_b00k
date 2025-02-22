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

# Local Tunneling - LocalTunnel y Ngrok

Si nosotros de forma local queremos exponer un puerto, por ejemplo un servicio web del puerto `80` que este corriendo en nuestra maquina local, tendremos que hacerlo a traves del `router` de nuestra casa, lo que habria que hacer seria realizar en el `router` un `Port Forwarding` del puerto `80` para que cuando algun usuario en internet pregunte al `router` la conexion que quiera realizar este le rediriga al puerto `80` y el servicio web le responda al usuario que pregunto, exponiendo asi nuestro puerto `80` de forma local a internet.

Pero cuando estamos en una organizacion se hace de otra forma, ya que no vamos a coger el `router` y realizar un `Port Forwarding` a parte de que la organizacion tendra otras herramientas, tendremos que realizarlo de otra forma en un ejercicio de `hacking etico`.

Por lo que aqui es cuando entra en juego estas herramientas que realizan `tuneles locales` o `LocalTunnel`.

La herramienta mas utilizada y famosa para realizar esto es la llamada `ngrok` que tiene diferentes paquetes de pago, unos mas sofisticados que otros, solo que nos tendremos que registrar, registrar una cuenta y para realizar lo que queremos hacer ahora actualmente es de pago esa tecnica en concreto en esa herramienta, pero si queremos utilizar otra menos profesional, pero que es gratuita y no hace falta registrarse, seria la siguiente:

URL = [LocalTunnel GitHub](https://github.com/localtunnel/localtunnel)

Tendremos que instalarla de la siguiente forma:

```shell
sudo apt install npm
sudo npm install -g localtunnel
```

Una vez instalado todo vamos a iniciar el servicio de `apache2` en el puerto `80` que vendra una pagina web por defecto en `kali`, esto se hara de forma local:

```shell
systemctl start apache2
```

Ahora si nosotros queremos exponer este puerto del `apache2` del puerto `80` a internet con esta herramienta que hemos instalado, lo haremos de la siguiente forma:

```shell
lt -p 80
```

Info:

```
your url is: https://tricky-pants-smash.loca.lt
```

Esto lo que esta haciendo es crear una `URL` con una instancia que tiene `LocalTunnel` en su servidor, exponiendo tu servicio interno a internet, los usuarios de internet preguntaran a dicha `URL` y este nos la envia a nosotros a nuestro puerto local, nosotros le respondemos al servidor y este se lo envia al usuario que pregunto, esto es una forma de exponer un puerto local a internet sin que ninguna herramienta de seguridad de una organizacion lo bloquee.

Ahora si nosotros metemos esa `URL` desde cualquier parte del mundo, podremos conectarnos al puerto `80` local de la maquina `kali` en mi caso.
