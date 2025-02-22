# Instalación Nessus

Nos tendriamos que ir a la siguiente pagina:

URL = [Download Nessus](https://es-la.tenable.com/products/nessus/nessus-essentials)

Nos tendriamos que registrar, una vez que nos registremos nos llevara a un apartado en el que nos permitira descargarnos `Nessus`, por lo que le daremos a `Descargar`, esto nos llevara a todos los tipos de descarga que hay en `Nessus` para cada sistema operativo, nosotros le daremos al llamado `Linux - Debian - amd64`, le daremos a `Download` y se nos emepezara a descargar, sera un fichero de extension `.deb`.

Una vez descargado, abriremos una terminal y para instalarlo pondremos lo siguiente:

```shell
mv ../Downloads/Nessus-10.8.3-debian10_amd64.deb .
apt install ./Nessus-10.8.3-debian10_amd64.deb
```

Echo esto, ya lo tendriamos instalado, por lo que iniciaremos el demonio (proceso):

```shell
systemctl start nessusd.service
```

Y en el navegador, en la barra de URL pondremos lo siguiente:

```
URL = https://localhost:8834/
```

Aceptamos el riesgo y le daremos a continuar, por lo que nos llevara a la pagina de `Nessus`.

<figure><img src="../../../.gitbook/assets/image (32) (1).png" alt=""><figcaption></figcaption></figure>

Una vez que se instales todos los `plugins` nos aparecera la interfaz de `Nessus` nos pedira que introduzcamos una IP para empezar el primer escaneo, pero le daremos a `Close` y si nos vamos a `New Scan` veremos todos los `plugins` que hay para realizar escaneos.

<figure><img src="../../../.gitbook/assets/image (33) (1).png" alt=""><figcaption></figcaption></figure>
