---
icon: file-signature
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

# Controles de seguridad en un entorno real

Si por ejemplo hemos conseguido encontrar la `IP` publica del servidor web real, ya que lo tiene habilitado y es una mala practica que muchas empresas siguen siguiendo, podremos realizar un escaneo de puerto esta vez de forma real si que el `balanceador de carga` nos apantalle dichos puertos o dicha informacion:

```shell
nmap -sV <Public_IP>
```

Info:

<figure><img src="../../.gitbook/assets/image (74).png" alt=""><figcaption></figcaption></figure>

Muchas veces podremos ver en la `VERSION` de `SSH` que nos aparecera `TCP Wrapped` y es como un pequeño `firewall` que paraceran en casi todas las instancia de `AWS` que ya vienen por defecto para proteger dicho puerto en tal caso de que estuvieramos haciendo esto mismo, pero es raro que nos este apareciendo la version del `SSH`.

Para poder `Bypassear` esto mismo, podremos realizar un escaneo un poco mas personalizado con `netcat` de la siguiente forma:

```shell
netcat -v <Public_IP> 22
```

Info:

<figure><img src="../../.gitbook/assets/image (75).png" alt=""><figcaption></figcaption></figure>

Y ya vemos como nos salta el `banner` del servidor `SSH` pudiendo identificar la `version` real del puerto.

Si un buen administrador del servidor web configurara de forma correcta todo esto, en vez de permitir que cualquiera se pueda conectar a los puertos `80` y `22` desde cualquier `IP` de esta forma en el `grupo de seguridad`:

<figure><img src="../../.gitbook/assets/image (76).png" alt=""><figcaption></figcaption></figure>

Aqui estamos permitiendo el acceso a `80` y `22` desde unicamente el grupo de seguridad `LB-SG`, por lo que ya no cualquier persona puede realizar esto escaneos que estabamos haciendo antes.

Lo que esta sucediendo aqui es que solamente va a permitir solicitudes a los servidores web desde unicamente el `balanceador de carga` por lo que aunque tengamos la `IP` publica del servidor web, no podremos realizar dichas peticiones para intentar sacar informacion.

En esta parte lo unico que nos quedaria seria realizar `hacking web` para poder identificar fallos de seguridad del mismo.

Pero igualmente, puede tener un `WAF` la aplicacion web protegiendo ese tipo de peticiones o cortando ese tipo de tecnicas de `hacking` como vimos anteriormente.
