---
icon: album-collection-circle-plus
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

# Recopilación de información en un entorno real

`Amazon` en su propia nube tendra unas normas respecto al `petesting` sobre sus servidores, aunque sean nuestros, solo podremos realizar ciertos ataques, los demas ataques que diga `amazon` que no se pueden realizar seran `ilegales`, por lo que hay que tener mucho cuidado con eso, la siguiente informacion se encuentra en este link:

URL = [Info pentesting amazon](https://aws.amazon.com/es/security/penetration-testing/)

Una vez sabiendo esto, realizaremos los siguientes escaneos basicos y utilizando herramientas basicas, ya que si profundizamos mas podemos sobreecargar un poco los servidores de `amazon` y eso costaria dinero en nuestra cuenta, por lo que tambien hay que tener cuidado con eso, pero imaginemos que una empresa nos dice que probemos su servidor web dandonos solamente un link de su servidor web `DNS`, lo que podremos hacer es investigar la web de primeras y despues podremos utilizar `kali` para realizar lo siguiente:

```shell
ping <LINK_WEB>
```

Pero veremos que no nos funciona el `ping` ya que el servidor esta limitado a solamente peticiones `HTTP` en el grupo de seguridad que le implementamos:

<figure><img src="../../.gitbook/assets/image (66).png" alt=""><figcaption></figcaption></figure>

Si nosotros por ejemplo editamos ese grupo y añadimos la siguiente regla:

<figure><img src="../../.gitbook/assets/image (67).png" alt=""><figcaption></figcaption></figure>

Vemos que estamos añadiendo una regla mas que es permitir el trafico de `ICMP` en cualquier direccion `IP`, con esto si podremos realizar un `ping`, pero rara vez las organizaciones tienen estas reglas.

<figure><img src="../../.gitbook/assets/image (68).png" alt=""><figcaption></figcaption></figure>

Pero bueno en este caso lo dejaremos como estaba antes sin la regla de `ICMP`, pero no nos tenemos que limitar solo a comprobar realizando un `ping` ya que muchas veces pueden tener capado eso mismo.

Si realizamos un `escaneo` con la herramienta `nmap`:

```shell
nmap -sn <LINK_WEB>
```

Info:

<figure><img src="../../.gitbook/assets/image (69).png" alt=""><figcaption></figcaption></figure>

Vemos que consiguio realizar un `reverse DNS` y nos esta encontrando otro `link` en el que se esta conectando el primero, que si entramos en el veremos que nos lleva a la misma aplicacion, pero tampoco es algo muy relevante, solo veremos que tiene otra `IP` asociado a el.

`nmap` en este caso funciono ya que a parte de utilizar trafico `ICMP` tambien realiza otra serie de peticiones que llaman al puerto `80` y `443` (`HTTP` y `HTTPS`).

Si nosotros queremos realizar un escaneo de puertos al `servidro web`:

```shell
sudo nmap -sS <LINK_WEB>
```

Info:

<figure><img src="../../.gitbook/assets/image (70).png" alt=""><figcaption></figcaption></figure>

Podemos deducir que solo contiene un puerto `80` pero eso no es verdad, ya que tambien tiene un `SSH`, solo que estamos escaneando el `balanceador de carga` y no el servidor real.

Si nosotros realizamos un escaneo para saber mas informacion como la version del puerto, etc... Y en la version del puerto aparece `filtered` sera por que hay alguna herramienta de seguridad por en medio que esta cortando ese tarfico de red para poder identificarlo, pero en este caso podremos sacar la info:

```shell
nmap -sV <LINK_WEB>
```

Info:

<figure><img src="../../.gitbook/assets/image (71).png" alt=""><figcaption></figcaption></figure>

Si nosotros queremos identificar el `S.O.` donde esta corriendo ese servidor web, lo haremos de la siguiente forma:

```shell
sudo nmap -O <LINK_WEB>
```

Info:

<figure><img src="../../.gitbook/assets/image (72).png" alt=""><figcaption></figcaption></figure>

Aqui vemos que esta sucediendo algo muy raro y es que nos lo esta detectando como un tipo de `Phone` o un `WAP`, cosa que eso no es real y podemos deducir que hay alguna herramienta que esta apantallando dicha informacion.

Por lo que podremos sospechar de diversas cosas, pero entre ellas de que pueda tener un `balanceador de carga` por en medio, por lo que vamos a comprobarlo con la siguiente herramienta:

```shell
lbd <LINK_WEB>
```

Info:

<figure><img src="../../.gitbook/assets/image (73).png" alt=""><figcaption></figcaption></figure>

Por lo que estamos observando efectivamente nos encontramos bajo un `balanceador de carga`, llegados a este punto tendremos que entrar en paginas como `Shodan` o este tipo de paginas en las que intentar buscar informacion por malas configuraciones o viendo su huella historica de que en algun momento no estuviera con un `balanceador` y poder observar la `IP` publica que tenia para de ahi poder realizar el escaneo y los ataques bajo esa `IP`.
