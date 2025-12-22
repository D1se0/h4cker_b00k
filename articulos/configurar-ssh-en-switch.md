---
icon: shuffle
layout:
  width: default
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
  metadata:
    visible: true
---

# Configurar SSH en Switch

Primero tendremos que conectarnos mediante un `SERIAL` al puerto de `Consola` del `Switch`, hecho esto tendremos que abrir nuestra aplicación `PuTTY` y conectarnos mediante `Serial` poniendo el puerto correcto, para identificar que `COM` es lo podremos mirara desde `Windows` en el `Administrador de dispositivos` bajamos abajo del todo y desplegamos la opción llamada `Ports (COM & LPT)` dentro de esta veremos el numero.

Pensemos que es el `COM3`, en el `PuTTY` tendremos que poner `COM3` y darle a conectar, hecho esto veremos un prompt.

```
switch:
```

Aquí tendremos que ejecutar `enable` para que nos meta de forma privilegiada al `switch` pudiendo configurar el mismo.

```
switch: enable
```

Info:

```
switch#
```

## Configurar IP al Switch

Ahora que vemos ese `#` sabemos que estamos de forma `privilegiada`, primero tendremos que configurarle una `IP` al `switch` de esta forma:

```
switch# configure terminal
switch(config)# interface vlan1
switch(config)# ip address 192.168.1.10  255.255.255.0
switch(config)# no shutdown
switch(config)# end
switch#
```

La `IP` podremos poner la que "queramos" para darle un rango, pero este mismo luego lo tendremos que configurar en nuestro `PC`.

## Configurar usuario al Switch

Ahora vamos a configurarle un usuario al `switch`.

```
switch# configure terminal
switch(config)# username user secret password
switch(config)# line vty 0 15
switch(config)# login local
switch(config)# transport input ssh
switch(config)# end
switch#
```

## Configurar usuario SSH

Ahora vamos a configurar el `SSH` para que el usuario se pueda conectar por `SSH` de esta forma:

```
switch# configure terminal
switch(config)# hostname name
switch(config)# enable password 1234
switch(config)# ip domain-name cisco.com
switch(config)# crypto key generate rsa
<LE DAMOS A ENTER>...
switch(config)# line vty 0 15
switch(config)# password 1234
switch(config)# login
switch(config)# transport input ssh
switch(config)# end
switch# 
```

Con esto ya tendremos el `SSH` configurado, pero siempre suele dar un fallo en tema de versiones de `SSH` ya que actualmente estamos por la versión `3` de `SSH` y la que se pone por defecto en el `switch` es la versión `2` por lo que habría una incompatibilidad cuando nos conectemos, para solucionar esto vamos a realizar la siguiente configuración.

```
switch# configure terminal
switch(config)# ip ssh time-out 30
switch(config)# ip ssh authentication-retries 3
switch(config)# ip ssh version 2
<NOS PEDIRA QUE ESTABLEZCAMOS DE NUEVO UN RSA>...
switch(config)# crypto key generate rsa
<ESCRIBIMOS "yes">...
<ESTABLECEMOS "768" bits>...
switch(config)# end
switch#
```

Para que todo esto se guarde en memoria vamos a escribir `write memory` y hecho esto ya podremos desconectar el cable `serial` del `PC`.

## Acceso por SSH mediante PC

Vamos a coger un cable de red por ejemplo un `Ethernet` (`RJ45`), lo conectaremos al `PC` y en el otro extremo lo conectamos a un puerto dentro del rango de la `VLAN1` que hayamos establecido, por ejemplo lo conectaremos en el primero puerto libre en este caso.

Después desde el `PC` tendremos que irnos a la configuración del `Ethernet` y darle a `Editar`, dentro de este menú estableceremos en `IPv4` la `IP` `192.168.1.100` por ejemplo, pero que este dentro del rango establecido en el `Switch`, como mascara de red pondremos `255.255.255.0`, para el `gateway` pondremos `192.168.1.254` y como servidores `DNS` ponemos los de `google` por ejemplo `8.8.8.8` o `8.8.4.4`.

Hecho esta configuración le daremos a guardar, abriremos una terminal de `CMD` y pondremos.

```cmd
ping 192.168.1.10
```

Para ver si tenemos `ping` con el `switch`, el primer `ping` siempre falla ya que en sus tablas de `ARP` no tiene nuestra dirección `MAC` pero si volvemos hacer un segundo `ping` veremos que si esta funcionando.

Ahora desde la aplicación de `PuTTY` le daremos a la opción de `SSH` y pondremos la `IP` del `switch` que es `192.168.1.10`, le daremos a `conectar` y nos saldrá que tenemos que `acptar` la conexión por llamarlo de alguna forma, le damos `aceptar` y veremos una terminal en el que tenemos que meter el usuario y contraseña que establecimos anteriormente.

```
User: user
Pass: password
```

Metiendo esas credenciales tendremos que obtener acceso al `switch` directamente, viendo el prompt `switch:`.
