---
icon: audible
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

# Auditando la infraestructura interna

Si por ejemplo nosotros dejamos la configuracion del grupo de seguridad como la teniamos antes en la que cualquier usuario desde internet pueda conectarse por `SSH` y por `HTTP`, lo que estamos haciendo es echar a perder toda la seguridad de nuestro servidor web, aunque tengamos un `WAF` que este en mitad de la comunicacion entre un balanceador de carga y el servidor web, si nosotros dejamos esa mala configuracion nosotros como atacantes podremos aprovechar eso sin necesidad de pasar por ese `WAF`, por lo que podremos realizar un `Bypass` del mismo.

Ya que si descubrimos la direccion `IP` publica de uno de los servidores web, podremos acceder a el directamente sin pasar por el `WAF` o el balanceador, y podremos atacarlo directamente.

Si por ejemplo conseguimos acceder de forma remota mediante `SSH` al servidor de la nube de `amazon` de la organizacion, ya que esta habilitado para ello como una mala configuracion, ya eso seria una parte que tendriamos que poner en el informe que estemos realizando, vamos a simular que hemos entrado poniendo lo siguiente:

```shell
chmod 400 <KEY.pem>
ssh -i "<KEY.pem>" ec2-user@<IP>
```

Info:

<figure><img src="../../../.gitbook/assets/image (77).png" alt=""><figcaption></figcaption></figure>

Y con esto ya estariamos logeados dentro del servidor de la nube de `amazon`, por lo que paar hacer un reconocimiento del `host` de forma interna, instalaremos `nmap` de la siguiente forma:

```shell
sudo yum install nmap
```

Pero esto puede hacer saltar algunas alertas de seguridad en el servidor, ya que estamos instalando una herramienta, por lo que podria ser un poco ruidoso, pero mas adelante veremos algunas otras tecnicas para que sea mas silencioso sin necesidad de instalar ninguna herramienta.

Una vez que hayamos instalado `nmap` haremos lo siguiente:

```shell
nmap -sn 10.0.0.0/24
```

Info:

<figure><img src="../../../.gitbook/assets/image (78).png" alt=""><figcaption></figcaption></figure>

Y vemos que hay otro `host` levantado, vamos ha realizar un escaneo de puertos:

```shell
sudo nmap -sS 10.0.0.245
```

Info:

<figure><img src="../../../.gitbook/assets/image (79).png" alt=""><figcaption></figcaption></figure>

Y vemos que solamente tiene el puerto `80` levantado, por lo que podemos deducir que puede ser el `balanceador de carga`.

Pero lo que esta haciendo `nmap` es realizar un escaneo de los puertos `(Protocolo) ICMP, 80 y 443` por lo que claramente que si hay un base de datos detras no va a responder, tendremos que realizar lo siguiente:

```shell
sudo nmap -sS -p 3306 10.0.0.0/24
```

Con esto lo que estamos haciendo es realizar un escaneo del puerto `MySQL` de todos los `host` de la red.

Info:

<figure><img src="../../../.gitbook/assets/image (80).png" alt=""><figcaption></figcaption></figure>

Y vemos que nos esta encontrando unos cuantos, por lo que ya tendremos varios vectores de entrada.

Pero si vemos en uno de esos `hosts` esta abierto concretamente el de `10.0.0.10`, por lo que ya podriamos investigar a ver como acceder a dicha base de datos.
