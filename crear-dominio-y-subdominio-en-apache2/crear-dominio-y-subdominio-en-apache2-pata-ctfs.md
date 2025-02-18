---
icon: network-wired
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

# Crear Dominio y Subdominio en apache2

## <mark style="color:purple;">Dominio con apache2</mark>

Primero vamos a crear los archivos correspondientes paso a paso para que esto funcione.

Vamos a crear el archivo de configuracion del dominio llamandolo en mi caso `mi_dominio`.

```shell
sudo nano /etc/apache2/sites-available/mi_dominio.conf

#Dentro del nano
<VirtualHost *:80>
    ServerName mi_dominio.local
    DocumentRoot /var/www/mi_dominio

    <Directory /var/www/mi_dominio>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/mi_dominio_error.log
    CustomLog ${APACHE_LOG_DIR}/mi_dominio_access.log combined
</VirtualHost>
```

Ahi especificamos dentro del nano como queremos que sea nuestro dominio y donde queremos que este dicha carpeta, en mi caso todo sera dentro de `/www` las carpetas para que no haya confusiones.

Crearemos la carpeta del dominio con un `index.html` en su interior para ver que funciona.

```shell
sudo mkdir -p /var/www/mi_dominio
echo "<html><body><h1>Bienvenido a mi dominio</h1></body></html>" | sudo tee /var/www/mi_dominio/index.html
```

Despues habilitamos el dominio de la siguiente manera.

```shell
sudo a2ensite mi_dominio.conf
```

Antes de reiniciar el `apache2` haremos que les redirija al dominio directamente para que no les redirija al `index.html` del que viene por defecto en `/www/html/`, haciendo lo siguiente.

```shell
sudo nano /etc/apache2/sites-available/000-default-ip.conf

#Dentro del nano
<VirtualHost *:80>
    # Este VirtualHost captura cualquier solicitud hecha directamente a la IP
    ServerName default
    DocumentRoot /var/www/html

    # Redirige todas las solicitudes a tu dominio principal
    Redirect permanent / http://mi_dominio.local/
</VirtualHost>
```

Y ahi especificamos que sea a ese dominio que nosotros tenemos creado, por lo que cada vez que metan la IP les redirigira a nuestro dominio creado con nuestro `index`.

Lo establecemos para que funcione.

```shell
sudo a2ensite 000-default-ip.conf
```

Y por precaucion desactivaremos el que te redirija al `/html/` que viene por defecto en `apache2`.

```shell
sudo a2dissite 000-default.conf
```

Ahora si reiniciamos el `apache2`.

```shell
service apache2 restart
```

Si ahora lo comprobamos con la siguiente URL, tendria que redirigirnos al dominio en cuestion y para poder ver el contenido de la pagina web del dominio tendremos que editar el archivo `hosts` de la siguiente forma.

```
URL = http://<IP>/
```

```shell
nano /etc/hosts

#Dentro del nano
<IP>       mi_dominio.local
```

Lo guardamos y ahora si deberiamos de ver su contenido.

## <mark style="color:purple;">Subdominio con apache2</mark>

El proceso sera similar al anterior, crearemos el archivo de configuracion que tendra el subdominio.

```shell
sudo nano /etc/apache2/sites-available/subdominio.mi_dominio.conf

#Dentro del nano
<VirtualHost *:80>
    ServerName subdominio.mi_dominio.local
    DocumentRoot /var/www/subdominio

    <Directory /var/www/subdominio>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/subdominio_error.log
    CustomLog ${APACHE_LOG_DIR}/subdominio_access.log combined
</VirtualHost>
```

Aqui lo adaptaremos a nuestras necesidades y crearemos la carpeta en la que pusimos que va a estar nuestro subdominio, para que cuando pongamos nuestro subdominio nos redirija a ese `index.html`.

```shell
sudo mkdir -p /var/www/subdominio
echo "<html><body><h1>Bienvenido al subdominio</h1></body></html>" | sudo tee /var/www/subdominio/index.html
```

Una vez creado todo lo anterior, habilitaremos el subdominio de la siguiente forma.

```shell
sudo a2ensite subdominio.mi_dominio.conf
```

Y reiniciaremos el `apache2` de la siguiente forma.

```shell
service apache2 restart
```

Ahora lo comprobaremos poniendo nuestro subdominio en el archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>       mi_dominio.local subdominio.mi_dominio.local
```

Lo guardamos y si ponemos en la URL el subdominio tendria que aparecernos la pagina web del subdominio.

```
URL = http://subdominio.mi_dominio.local/
```
