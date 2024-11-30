# Command Injection

Vamos a empezar por `command injection` nos iremos a `OWASP 2017` -> `Cross-Site-Scripting (XSS)` -> `Reflected (First Order)` -> `DNS Lookup`

`Command Injection` se va a basar basicamente en una injeccion de codigo, lo que pasa es que el contexto de esta injeccion va a ser un comando que se va a ejecutar en el sistema operativo del web server.

Cuando nosotros creemos que en una pagina hay un campo en el que cuando introducimos algun comando o alguna funcion que tiene la pagina como en este caso de la pagina `Mutillidae` que te hace un `DNS Lookup` cuando metemos un dominio o IP, podemos pensar que esto se esta ejecutando en el servidor y por dentro se esta ejecutando la herramienta `dnslookup` para que se pueda ejecutar ese comando, por lo que nosotros pdoremos aprovechar esto si no esta bien sanitizada la pagina para poder concatenar comandos y poder ejecutar lo que queremos.

Lo que haremos para probar esto seria poner lo siguiente:

```shell
Hostname/IP: www.google.com; cat /etc/passwd
```

Y podremos ver algo asi:

<figure><img src="../../../.gitbook/assets/image (108).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos funciona correctamente.
