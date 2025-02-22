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

# Funcionamiento de Kerberos

Vamos a ver el protocolo principal que se utiliza muchisimo en `Active Directory` llamado `Kerberos`.

El protocolo de `autenticacion` `Kerberos` fue desarrollado originalmente en el `MIT` para el proyecto `Athena` (`1983`). Los objetivos del proyecto incluian la integracion de:

* `SSO (Single Sign-on)`
* Soporte para sistemas de archivos de red
* Un entorno grafico unificado (`Desarrollaron X Windows`)
* Servicio de `convencion` de nombres (piense en `DNS`)

URL = [Athena Info](http://web.mit.edu/acs/athena.html)

> Kerberos y Microsoft Windows

En `Microsoft Windows` la `autenticacion` de usuarios y hosts basada en `dominio` se realiza a traves de `Kerberos`.

`Kerberos` v5 (`RFC1510`) se introdujo en `Windows Server 2000` y sustituyo a `NTLM` (`Windows NT LAN Manager`) como opcion de `autenticacion` por defecto.

`NTLM` se sigue utilizando como mecanismo de `autenticacion local` (equipos no unidos a un `dominio`)

`Kerberos` es el `protocolo de identidad` mas antiguo de uso comun en la actualidad

> ¿Como funciona `Kerberos`?

URL = [Kerberos Info](https://web.mit.edu/kerberos/www/dialogue.html)

<figure><img src="../../.gitbook/assets/image (108).png" alt=""><figcaption></figcaption></figure>

En esta pagina de arriba se comenta un dialogo entre 2 personas de como fue evolucionando la herramienta `Kerberos` hasta dia de hoy, en concreto estas 2 personas son los desarrolladores de `kerberos`.

### Escena 1 Kerberos Fundamentos

> Escena 1:

<figure><img src="../../.gitbook/assets/image (109).png" alt=""><figcaption></figcaption></figure>

Parte 2:

<figure><img src="../../.gitbook/assets/image (110).png" alt=""><figcaption></figcaption></figure>

En estos casos se plantea el tener varios servidor haciendo diferentes cosas en el que cualquier usuario pueda acceder a dicho servidor para que le proporcione lo que necesite, sin tener que conectarse todos los usuarios a un mismo servidor como se hacia antes.

### Escena 2 Kerberos Fundamentos

> Escena 2:

<figure><img src="../../.gitbook/assets/image (111).png" alt=""><figcaption></figcaption></figure>

Aqui lo que se esta comentando es que seria muy poco eficiente el echo de guardar todas las credenciales de los miles de usuarios en cada servidor cada uno teniendo una base de datos y si alguno cambiara la contraseña se tendria que cambiar de todas las bases de datos.

<figure><img src="../../.gitbook/assets/image (112).png" alt=""><figcaption></figcaption></figure>

Aqui lo que se esta planteando es que en vez de tener varias bases de datos con las credenciales tanto de los usuarios como de los servicios que corren en cada servidor, lo que se hara sera crear un sistema centralizado de base de datos dedicado unicamente a la autenticacion con dichas credenciales donde se almacenaran todas las credenciales de los usuarios y de los servicion llamada `AUTHENTICATION SERVICE` y estaran centralizado en una unica base de datos.

Y el esquema seria de la siguiente forma:

<figure><img src="../../.gitbook/assets/image (113).png" alt=""><figcaption></figcaption></figure>

Lo que se plantea aqui es que cuando el usuario quiera consumir un servicio bajo su nombre lo que se hara sera que el usuario enviara su nombre, contraseña y el servicio que quiere consumir al `servicio de autenticacion`, esta la compara con su nombre donde esta su contraseña y si coincide le pasa un cifrado que combina su nombre de usuario con la contraseña del servicio que quiere consumir de forma cifrada todo, este teniendo este `tiket` lo que hace es enviarlo al servicio y si es correcto el servicio el envia el archivo.

<figure><img src="../../.gitbook/assets/image (114).png" alt=""><figcaption></figcaption></figure>

Los problemas que plantea aqui sobre este sistema, es el echo de que si se descifrara mal o se cambiara alguna letra por error que pasaria y que si por ejemplo un atacante robara ese `tiket` y se hiciera pasar por dicho usuario la informacion iria para el atacante tambien cambiando el nombre del equipo por el del usuario para que todo coincida y le envie la informacion.

<figure><img src="../../.gitbook/assets/image (115).png" alt=""><figcaption></figcaption></figure>

Ahora lo que va hacer para solucionar mas o menos estos 2 problemas es que en vez de cifrar el usuario con la contraseña del servicio, lo que va hacer es cifrar el nombre de usuario, la direccion IP desde la maquina en la que se esta generando el `tiket` y el nombre del servicio.

<figure><img src="../../.gitbook/assets/image (116).png" alt=""><figcaption></figcaption></figure>

Lo que se comenta aqui es que el `tiket` se puede reutilizar para futuros logeos al servicio que se quiera consumir con tal solo haberse autenticado una vez, pero si se quiere consumir otro servicio se tiene que volver autenticar de nuevo para un nuevo `tiket` pongamos que hay cientos de servicios y tendriamos que autenticarnos en cientos de servicios en un mismo dia, seria una locura, pero a parte las credenciales que se le envia al servicio de autenticacion van por la red en plano, por lo que seria muy facil que fueran interceptadas, para solucionar estos problemas se planteo lo siguiente:

### Escena 3 Kerberos Fundamentos

> Escena 3:

<figure><img src="../../.gitbook/assets/image (117).png" alt=""><figcaption></figcaption></figure>

Lo que se va a incluir y a modificar aqui es que ahora tendremos un `Ticket-Granting Service` y una nueva figura que va a ser el `Ticket-Granting Ticket`.

Lo que el usuario ahora le envia son las credenciales en formato de `Key` al servicio de autenticacion, si son correctas este le responde con un `Ticket-Granting Ticket`, ahora cuando nos queramos autenticar antes un servicio se hara de la siguiente forma:

<figure><img src="../../.gitbook/assets/image (118).png" alt=""><figcaption></figcaption></figure>

Ahora si queremos obtener el ticket del servicio con el que nos queremos autenticar, vamos a enviarle ese `Ticket-Granting Ticket` el cual ya tiene las credenciales dentro en lugar de tener que meter nosotros las credenciales de forma manual y este `Ticket-Granting Ticket` se lo enviamos al `Ticket-Granting Service` este lo que va hacer es validar este `Ticket` con la clave que corresponda al usuario dentro de la base de datos, si es correcto este mismo le envia el `Ticket` de servicio que quiere consumir, el usuario envia el `Ticket` proporcionado al servicio que quiere consumir y este verifica que este todo correcto para enviarle el archivo o acceder al servicio, si quisieramos ir a otro servicio solo bastaria con enviar nuestro `Ticket-Granting Ticket` para que nos proporcione un nuevo `Ticket` de dicho servicio nuevo.

<figure><img src="../../.gitbook/assets/image (119).png" alt=""><figcaption></figcaption></figure>

Ahora lo que comenta es que esta todo bien, solo que todavia sigues enviando tus credenciales una primera vez en plano por la red, pero se plantea el siguiente esquema para solucionar esto:

<figure><img src="../../.gitbook/assets/image (120).png" alt=""><figcaption></figcaption></figure>

Cuando el usuario quiere obtener el `Ticket-Granting Ticket` lo primero que envia es su usuario al servicio de autenticacion este mismo va a comprobar si existe el usuario y como existe visualiza la clave privada que esta asociada a dicho usuario, por lo que este mismo servicio va a utilizar su misma clave privada para cifrara el `Ticket-Granting Ticket` que ha generado para dicho usuario, ahora lo que le manda el servicio de autenticacion es el paquete cifrado con la clave privada del usuario con el `Ticket-Granting Ticket` al usuario cuando el usuario recibe el paquete cifrado, coge su clave privada, descifra ese paquete y obtiene el `Ticket-Granting Ticket`.

<figure><img src="../../.gitbook/assets/image (121).png" alt=""><figcaption></figcaption></figure>

Lo que se plantea aqui es que si por ejemplo un usuario cierra sesion pero se dejo almacenados en el equipo los `Ticket-Granting Ticket` de los servicios que ha estado usando y viene otro usuario y se logea en la misma maquina, podra utilizar dichos servicios bajo el usuario del equipo, por lo que se plantea añadir 2 campos mas al `Ticket-Granting Ticket` el tiempo de vida que tendra ese `Ticket` y el `Timestamp` de cuando se creo el `Ticket`.

<figure><img src="../../.gitbook/assets/image (122).png" alt=""><figcaption></figcaption></figure>

Pero claro esta solucion es una solucion muy parcial, ya que si el tiempo de vida sigue estando valido cuando venga otro usuario se podra seguir utilizando hasta que caduque, por lo que se planteo otra solucion.

<figure><img src="../../.gitbook/assets/image (123).png" alt=""><figcaption></figcaption></figure>

### Escena 4 Kerberos Fundamentos

> Escena 4:

<figure><img src="../../.gitbook/assets/image (124).png" alt=""><figcaption></figcaption></figure>

Lo que mejora su sistema y este modelo de aqui es el `kerberos` de hoy en dia que se sigue utilizando hasta dia de hoy.

Este modelo incluye 2 estructuras nuevas una de `Athenticator`, incluye otra que es la clave privada para este `Ticket-Granting Service` y por ultimo incluye otro tipo de claves nuevas que se van a llamar `claves de sesion`.

Todo el procedimiento para obtener el `Ticket-Granting Ticket` es de la misma forma pero cuando genera el `Ticket-Granting Ticket` para el usuario coge la clave privada del usuario, genera una nueva `clave de sesion` y tambien coge la `clave` del `Ticket-Granting Service` para asi generar el `Ticket-Granting Ticket` con las cosas mencionadas como `clave de sesion` que acaba de generar, contiene el nombre de usuario, la direccion IP desde donde se esta haciendo, etc... Coge todos estos valores y lo cifra con la clave privada del `Ticket-Granting Service` la cual el usuario no conoce y a la vez va a crear un paquete aparte que contiene la `clave privada` el cual estara cifrado con la clave del usuario y le envia estas 2 cosas.

Cuando le llega al usuario lo unico que hace es descifrar la `clave privada` con la clave del usuario, lo que tendra sera la `clave privada` y el `ticket` el cual esta cifrado con la clave privada del `Ticket-Granting Service` el cual no conoce el usuario.

Ahora para obtener acceso algun servicio con estas cosas seria de la siguiente forma:

<figure><img src="../../.gitbook/assets/image (125).png" alt=""><figcaption></figcaption></figure>

Ahora lo que tendremos que hacer para obtener ese `Ticket-Granting Ticket` para dicho servicio, lo que entrara en juego ahora sera el `Authenticator` que es esto de aqui:

<figure><img src="../../.gitbook/assets/image (126).png" alt=""><figcaption></figcaption></figure>

Lo que contiene esto es nuestro nombre de usuario, la direccion IP y demas informacion... Pues lo que vamos hacer como usuario es `cifrar` con la `clave de sesion` que obtuvimos este `Authenticator`, ahora lo que se le tendra que enviar al `Ticket-Granting Service` sera el `Ticket-Granting Ticket` que tenemos mas el `Authenticator` `cifrado` con la `clave de sesion`, lo que hace este `Ticket-Granting Service` es que cuando recive todo esto descifra el `Ticket-Granting Ticket` que esta cifrado con la clave privada del `Ticket-Granting Service` y obtiene la `clave de sesion` que utiliza posteriormente para descifrar el `Authenticator` que ha enviado el usuario descifra este mismo y comprueba que el usuario que aparece en el `Ticket-Granting Ticket` que acaba de descrifrar con su clave privada y el que aparece con el `Authenticator` que aparece con la `clave de sesion` coincide y si coincide pasa la validacion y lo que va hacer sera crear un `Ticket` de servicio el cual quiere consumir y a parte tambien le creara una `clave de sesion` todo esto estara incluido en el `Ticket` de servicio y este `Ticket` de servicio estara cifrado con la clave privada del servicio y todo esto estar dentro de un paquete el cual estara cifrado con la `clave de sesion` que recupero cuando descifro el `Ticket-Granting Ticket` y que tambien tiene el usuario.

Entonces lo que envia al usuario es el `Ticket` de servicio cifrado mas el paquete cifrado que contiene la nueva `clave de sesion` generada por el `Ticket-Granting Service` para consumir ese servicio.

<figure><img src="../../.gitbook/assets/image (127).png" alt=""><figcaption></figcaption></figure>

Cuando todo esto le lleva al usuario lo que hara sera utilizar la antigua `clave de sesion` para descifrar el paquete que contiene la nueva `clave de sesion` para consumir el servicio y tendra el `Ticket` de servicio cifrada con la clave del servicio.

Entonces lo que va hacer el usuario es crear un nuevo `Authenticator` el cual va a cifrar con la `clave de sesion` nueva que le envio el `Ticket-Granting Service` para este servicio en concreto, entonces lo que va hacer el usuario para acceder al servicio sera enviarle como verificacion el `Ticket` de servicio mas el `Authenticator` cifrado con la `clave de sesion` del servicio.

Lo que va hacer este servicio cuando le llega la informacion es descifrar el `Ticket` de servicio con su clave privada de servicio que contiene una `clave de sesion` que le envio al usuario anteriormente entonces utiliza esta `clave de sesion` que contiene dentro para descifrar el `Authenticator` si la informacion que hay dentro del `Authenticator` coincide con la que hay en el `Ticket` de servicio puede validar que el usuario es quien tiene que ser por lo que le permite acceder al servicio.

<figure><img src="../../.gitbook/assets/image (128).png" alt=""><figcaption></figcaption></figure>

Para finalizar hay un paso adiccional y es que el servicio puede autenticar al usuario, pero el usuario no puede autenticar al servicio por lo que si por ejemplo un atacante se hace pasar por dicho servicio para quedarse con lo que envia el usuario, el usuario no sabra que es el servicio realmente, por lo que se plantea esta solucion.

Sigue el mismo proceso de antes, pero lo unico que cambia es que cuando el servicio ha descifrado todo y nos ha validado como usuario legitimo, lo que hace el servicio es autenticarse asi mismo todo esto lo guarda en un paquete y genera un `Timestamp` este paquete lo cifra con la misma `clave de sesion` que obtuvo del `Ticket` de servicio lo envia al usuario y como nosotros tenemos esa `clave de sesion` lo desciframos y si el descifrado es correcto sabemos que el servicio es el legitimo.
