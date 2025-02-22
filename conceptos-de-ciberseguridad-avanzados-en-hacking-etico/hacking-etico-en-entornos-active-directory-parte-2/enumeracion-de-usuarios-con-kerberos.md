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

# Enumeración de usuarios con Kerberos

Vamos a utilizar una aplicacion para realizar esta tecnica que no viene instalada por defecto en `kali` que se llama `Kerbrute`.

URL = [Kerbrute GitHub](https://github.com/ropnop/kerbrute)

Pero antes tendremos que instalar lo necesario para que esta herramienta pueda funcionar.

```shell
sudo apt install golang
```

Ya que esta herramienta esta creada en `Go`.

Ahora tendremos que modificar un momento nuestro fichero de `.zsh` para activar la ruta donde se va a ejecutar las aplicaciones que estan en `Go`.

```shell
sudo nano ~/.zshrc

#Dentro del nano
#Vamos añadir las siguiente lineas abajo del todo

export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
```

Lo guardamos y haremos lo siguiente:

```shell
source ~/.zshrc
```

Esto lo hacemos para cargar la configuracion que hemos añadido, para que se actualice basicamente.

Ahora si podremos instalar la herramienta de la siguiente forma:

```shell
go install github.com/ropnop/kerbrute@latest
```

Info:

```
go: downloading github.com/ropnop/kerbrute v1.0.3
go: downloading github.com/op/go-logging v0.0.0-20160315200505-970db520ece7
go: downloading github.com/spf13/cobra v0.0.5
go: downloading github.com/ropnop/gokrb5 v7.2.1-0.20190226233023-10e0941da4e2+incompatible
go: downloading github.com/spf13/pflag v1.0.5
go: downloading github.com/jcmturner/gofork v1.0.0
go: downloading gopkg.in/jcmturner/dnsutils.v1 v1.0.1
go: downloading github.com/hashicorp/go-uuid v1.0.1
go: downloading golang.org/x/crypto v0.0.0-20191107222254-f4817d981bb6
go: downloading gopkg.in/jcmturner/rpc.v1 v1.1.0
go: downloading gopkg.in/jcmturner/aescts.v1 v1.0.1
```

Por lo que vemos se instalo correctamente, ahora si ejecutamos el siguiente comando para saber si esta bien instalado:

```shell
kerbrute -h
```

Veremos que nos muestra la informacion de la herramienta.

Para enumerar usuarios en el dominio y saber cuales existen y cuales no, podremos hacerlo de la siguiente forma, pero antes tendremos que obtener un listado de usuarios para realizar esa fuerza bruta.

Podremos obtenerlo de internet, de diccionarios por `GitHub`, etc... En este caso vamos a crear uno que sea dedicado al dominio para ver como nos encunetra los usuarios.

> users.txt

```
anatoli.vaz
empleado1
empleado2
empleado3
angelika.shelly
empleado4
empleado5
```

Guardamos el listado y ejecutamos la herramienta de la siguiente forma:

```shell
kerbrute userenum -d corp.local --dc 192.168.5.5 users.txt
```

Info:

```

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 01/14/25 - Ronnie Flathers @ropnop

2025/01/14 04:36:05 >  Using KDC(s):
2025/01/14 04:36:05 >   192.168.5.5:88

2025/01/14 04:36:05 >  [+] VALID USERNAME:       empleado1@corp.local
2025/01/14 04:36:05 >  [+] VALID USERNAME:       empleado2@corp.local
2025/01/14 04:36:05 >  [+] VALID USERNAME:       angelika.shelly@corp.local
2025/01/14 04:36:05 >  Done! Tested 7 usernames (3 valid) in 0.007 seconds
```

Y vemos que nos encontro 3 usuarios validos.

Esto funciona de la siguiente manera, la herramienta esta enviando el nombre de usuario al `AS-REQ` y este verifica si el nombre es valido para forjar el `Ticket`, pero cuando ve que es valido necesita un `Preverificacion` y nos da el codigo `225` pero cuando el nombre no es valido nos de el error `134`, por lo que la herramienta solo se queda con los codigos `225` que son los que han validado el usuario el `AS`.
