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

# AS-REQ Roasting

Esta tecnica consiste en que cuando nosotros hacemos una conexion con el `AS-REQ` una primera vez con el nombre de usuario, el `AS` quiere una `Preautenticacion` teniendole que enviar un `Timestamp` de forma cifrada con nuestra `clave privada` para que lo verifique el `AS`, pues con esta tecnica lo que haremos sera interceptar ese paquete del `timestap` que esta cifrado con la `clave privada` del usuario y crackearla de forma offline para sacarle la contraseña a dicho usuario.

Lo que vamos hacer primeramente es abrir `Wireshark` para ver todas las peticiones a nivel de red, filtrarlo por `kerberos` y reiniciaremos la maquina `empleado2`, una vez echo esto y estando en la parte de inicio de sesion, le daremos a `Otro usuario`, y nos logearemos con el usuario `Administrador` como si un administrador estuviera accediendo mediante otro equipo, cosa que suele ser comun ver.

Pondremos las siguientes credenciales:

<figure><img src="../../.gitbook/assets/image (142).png" alt=""><figcaption></figcaption></figure>

Le daremos a iniciar sesion con el `Administrador` mientras estamos capturando con `Wireshark`, una vez que estemos en el escritorio, pararemos de capturar con `Wireshark` y veremos todo esto:

<figure><img src="../../.gitbook/assets/image (143).png" alt=""><figcaption></figcaption></figure>

Vemos que nos capturo bastante informacion sobre `kerberos` y la autenticacion.

Si nos vamos a un `AS-REQ` el primero en concreto:

<figure><img src="../../.gitbook/assets/image (144).png" alt=""><figcaption></figcaption></figure>

Y vemos sus datos a nivel de red en la parte de abajo, desplegamos un poco la informacion de `kerberos` en concreto el `cname` que es el que nos interesa para saber sobre que usuario es y vemos lo siguiente:

<figure><img src="../../.gitbook/assets/image (145).png" alt=""><figcaption></figcaption></figure>

Vemos que es sobre el usuario `Administrador`, si seguimos bajando en los paquetes de datos, vemos que `AS` necesita una `Preautenticacion` como mencione anteriormente y el siguiente paquete es el paquete cifrado con la `clave privada` del usuario en este caso `Administrador`:

<figure><img src="../../.gitbook/assets/image (146).png" alt=""><figcaption></figcaption></figure>

Si le damos a ese segundo `AS-REQ` sera el paquete con el `timestamp` cifrada con la `clave privada` del `Administrador` el cual nos va a interesar obtener.

Nos vamos a ir a la parte de la informacion del paquete donde pone `padata-type: ... TIMESTAMP...` y cogeremos el valor donde pone `cipher: ...`:

<figure><img src="../../.gitbook/assets/image (147).png" alt=""><figcaption></figcaption></figure>

Que esa sera la clave que nos interesa, en mi caso seria esta:

```
788868b4ee00b4045b005c736c3448299b6a2df8f86a797f4b5d54dc1e7a7d8c7a18f42068bff33492b5993176bbf57e5364aa167f5094d7
```

Para copiarla, le daremos click derecho -> `Copy` -> `Value`.

Vemos que esta cifrado en `AES256`, por lo que necesitaremos otra cosa a parte de ese `hash` que hemos obtenido, que seria el `salt`, esto lo podremos obtener en la siguiente respuesta que le hacer el `AS-REP`.

<figure><img src="../../.gitbook/assets/image (148).png" alt=""><figcaption></figcaption></figure>

Y si nos vamos a la informacion, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (149).png" alt=""><figcaption></figcaption></figure>

Ahi estamos viendo el `salt` con el que esta cifrado, por lo que copiaremos de la misma forma los valores como hicimos antes y obtendremos algo asi:

```
WIN-VTVIM0M8QM9Administrator
```

Ahora lo que vamos a intentar es `crackear` este `hash` con este `salt`, por lo que en este caso podremos utilizar `john` o `hashcat`, en mi caso utilizare `john`, en la siguiente pagina podremos ver los diferentes formatos que hay para poder `crackear` con `hashcat`:

URL = [Hashcat Wiki](https://hashcat.net/wiki/doku.php?id=example_hashes)

Si nos metemos en la pagina nos interesara el siguiente formato:

<figure><img src="../../.gitbook/assets/image (150).png" alt=""><figcaption></figcaption></figure>

Que el ejemplo seria algo asi:

```
$krb5pa$18$hashcat$HASHCATDOMAIN.COM$96c289009b05181bfd32062962740b1b1ce5f74eb12e0266cde74e81094661addab08c0c1a178882c91a0ed89ae4e0e68d2820b9cce69770
```

Entonces donde pone `$hashcat` seria el nombre de usuario, donde pone `$HASHCATDOMAIN.COM` seria el dominio de `Windows Server`, todo lo demas seria el `hash` de la `clave privada` del usuario, pero el `salt` creo que no lo soporta en este caso, por eso vamos a utilizar `john` ya que es mas sencillo de utilizar tambien.

Pero el `hash` de ejemplo de arriba nos sirve para preparar el formato para `john` por lo que el archivo del `hash` tiene que quedar algo tal que asi:

> hash

```
$krb5pa$18$Administrator$CORP.LOCAL$WIN-VTVIM0M8QM9Administrator$788868b4ee00b4045b005c736c3448299b6a2df8f86a797f4b5d54dc1e7a7d8c7a18f42068bff33492b5993176bbf57e5364aa167f5094d7
```

Lo unico que tenemos que añadir es el `$<SALT>` entre el `$<DOMINIO>` y el `$<HASH>`.

Ahora lo vamos a `crackear` utilizando `john` de la siguiente forma:

```shell
john hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5pa-sha1, Kerberos 5 AS-REQ Pre-Auth etype 17/18 [PBKDF2-SHA1 128/128 AVX 4x])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Passw0rd         (?)     
1g 0:00:00:01 DONE 2/3 (2025-01-15 04:00) 0.8474g/s 5206p/s 5206c/s 5206C/s Stephani..Open
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Y como vemos lo ha conseguido `crackear` por lo que sabremos que la contraseña del `Administrador` es `Passw0rd`.
