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

# Seguridad y Computación en la nube (AWS)

Ahora para controlar tanto la conectividad entrante pero tambien saliente, lo que vamos a configurar va a ser un `firewall`, si nos vamos en la seccion de `Security` -> `Security Groups` -> `Create Security Groups` -> lo llamaremos `APPWEB-SG`, en la descripcion tendremos que poner `allow HTTP and SSH` (Esto se hace para permitir el trafico `HTTP` y despues tambien el trafico `SSH`), seleccionamos la `VPC` llamada `WEBAPP-VPC`, ahora tendremos que configurar una serie de `reglas` -> `Add rule` -> seleccionamos en `Type` el `HTTP`, despues en `Source` seleccionamos `Anywhere-IPv4`, despues añadiremos otra `regla` el `Type` sera `SSH` y seleccionaremos en `Source` la misma regla `Anywhere-IPv4` -> `Create Security Groups`

Y con esto ya tendremos esto creado, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (46).png" alt=""><figcaption></figcaption></figure>

Crearemos otro `Security Groups` de la misma forma, pero a este le llamaremos `BD-SG`, pondremos en la descripcion `Allow MySQL acces`, seleccionamos `WEBAPP-VPC`, añadiremos una `regla`, el tipo sera `MYSQL/Aurora` y en el `source` en la barra de busqueda, pondremos el `APPWEB-SG` para que solo tenga acceso a nivel de los `2` servidores y no de forma externa.

<figure><img src="../../.gitbook/assets/image (47).png" alt=""><figcaption></figcaption></figure>

Y con esto ya lo tendremos creado todo, pero vamos a crear otro `Security Groups` que se llame `LB-SG` (Para el `Load Balancer`), en la descripcion pondremos `Allow HTTP`, seleccionaremos `WEBAPP-VPC`, añadiremos una regla en la que el tipo sera `HTTP` y en el `source` seleccionaremos `Anywhere-IPv4`.

Este `balanceador` sera el que reciba las peticiones de los usuarios y este mismo decidira a cual de los `2` servidores transmitirles dicha peticion, como medida de seguridad.

Ahora vamos a crear los servidores, y el servicion de computacion en la nube que tiene `amazon` se llama `EC2`, por lo que lo buscaremos y lo seleccionaremos:

<figure><img src="../../.gitbook/assets/image (48).png" alt=""><figcaption></figcaption></figure>

Seleccionaremos `Instances (running)` -> `Launch instances` -> seleccionaremos la primera `Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type ...` -> `Select` -> elegimos el tipo `Family: t2, Type: t2.micro, ...` -> `Next: Configure Instances Details` -> en `network` seleccionaremos `WEBAPP-VPC`, en `Subred` seleccionamos `Subred Publica 1`, pondremos en `Enable` la parte de `Auto-assign Public IP`, por ultimo nos bajamos abajo y en la parte de `User data` en el recuadro de texto tendremos que poner el siguiente codigo en `bash`:

```bash
#!/bin/bash  
yum -y install httpd php mysql php-mysql  
  
case $(ps -p 1 -o comm | tail -1) in  
systemd) systemctl enable --now httpd ;;  
init) chkconfig httpd on; service httpd start ;;  
*) echo "Error starting httpd (OS not using init or systemd)." 2>&1  
esac  
  
if [ ! -f /var/www/html/bootcamp-app.tar.gz ]; then  
cd /var/www/html  
wget https://s3.amazonaws.com/immersionday-labs/bootcamp-app.tar  
tar xvf bootcamp-app.tar  
chown apache:root /var/www/html/rds.conf.php  
fi  
yum -y update
```

Esto lo que hace es que descarga la pagina web, la monta en `/var/www/html` para que el servidor web la pueda consumir, le da los permisos necesarios, etc...

<figure><img src="../../.gitbook/assets/image (49).png" alt=""><figcaption></figcaption></figure>

Ahora le damos a `Next: Add Storage` -> `Next: Add Tags` -> `Next: Configure Security Group` -> en la parte de `Assign a security group` seleccionamos `Select an existing security group` y seleccionamos `APPWEB-SG` -> `Review and Launch` -> `Launch` -> ahora nos aparecera una mini ventanita ya que anteriormente dijimos que podiamos acceder a traves de `SSH` y tendremos que configurar una `clave privada` (`RSA`) de `SSH`, seleccionaremos `Create a new key pair`, en la seccion de `Key pair name` pondremos `APPSERVER1-keypair` -> `Download Key Pair` (Esto lo que hace es descargarnos las `claves privada/publica` del `SSH`) -> `Launch Instances`.

<figure><img src="../../.gitbook/assets/image (50).png" alt=""><figcaption></figcaption></figure>

Y con esto ya tendremos creado el `servidor 1`:

<figure><img src="../../.gitbook/assets/image (51).png" alt=""><figcaption></figcaption></figure>

Nos iremos a `instancias` y cambiaremos el nombre al servidor ya que viene por defecto el nombre de `ec2` y lo cambiaremos por `WEBSERVER1`

Ahora lo que vamos hacer es crear otro segundo servidor identico al primero con el objetivo de que el `balanceador de carga` distribuya las peticiones que se le hace con los `2` servidores, por si fallara uno, que el otro lo reespalde.

Si ahora nosotros nos vamos al primer servidor y vemos la `IP` publica que tiene:

<figure><img src="../../.gitbook/assets/image (52).png" alt=""><figcaption></figcaption></figure>

Esa `IP` la pegamos en una `URL` de internet, veremos la pagina web que hemos desplegado de forma correcta.

<figure><img src="../../.gitbook/assets/image (53).png" alt=""><figcaption></figcaption></figure>

Veremos que carga todo correctamente, ahi tiene una opcion llamada `RDS` que es para conectarnos a la base de datos, pero que veremos despues:

<figure><img src="../../.gitbook/assets/image (54).png" alt=""><figcaption></figcaption></figure>

Ahora vamos a crear el segundo servidor de forma exacta al primero que hemos creado, pero con la unica diferencia de que en la parte de `Subred` seleccionaremos `Subred Publica 2` y cuando llegamos a la parte de la `clave privada` de `SSH` pondremos esto:

<figure><img src="../../.gitbook/assets/image (55).png" alt=""><figcaption></figcaption></figure>

Y con esto ya tendremos los `2` servidores listos, nombraremos este segundo servidor como `WEBSERVER2`:

<figure><img src="../../.gitbook/assets/image (56).png" alt=""><figcaption></figcaption></figure>
