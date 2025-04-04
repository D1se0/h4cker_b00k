---
icon: server
---

# Registros o BBDD Whois

Este tipo de bases de datos, son cuando las empresas se dan de alta en algun cierto dominio o algo parecido a ello, es necesario que proporcionen informacion como, el nombre personal, correo, domicilio, etc... Y todo eso se queda registrado y se guardan en bases de datos llamadas `Whois`.

Para ello tenemos una herramienta en `kali` llamada `whois` la cual podremos utilizar para obtener informacion de esas bases de datos de un dominio en concreto o IP.

```shell
whois <DOMINIO/IP>
```

> Ejemplo:

```shell
whois vulnhub.com
```

Y aqui te mostraria informacion de las BBDD `whois` del registrador del dominio, mostraria mucha informacion dependiendo de como de protegido lo tenga, podriamos llegar a ver informacion sensible.

En españa actualmente este tipo de informacion suele estar muy protegida aunque busquemos en estas bases de datos, por las normativas de seguridad como por ejemplo `GDPR`, por lo que a lo mejor no encontraremos mucha informacion sensible que nos pueda ayudar a veces.

Pero en otros paises estas restricciones no existen por lo que si nos seria mas util esta herramienta.
