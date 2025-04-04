# Instalación aplicación Web vulnerable (Mutillidae II)

Estando dentro de `Ubuntu-Desktop`, nos iremos al siguiente link que os dejare donde se encuentra el repositorio oficial de `mutillidae`:

URL = [Mutillidae GitHub](https://github.com/webpwnized/mutillidae)

Aqui se podra encontrar toda la info sobre esta pagina vulnerable, proporcionandote pistas de algunas tecnicas para explotacion web, etc... Es una pagina muy completa la cual vamos a instalar seguidamente.

Abriremos una terminal y pondremos lo siguiente:

```shell
sudo apt update
```

Despues instalamos `apache2`:

```shell
sudo apt install apache2
```

Y vamos a iniciar el servicio, a la vez que vamos a ponerlo para que cada vez que se inicie la maquina se inicie `apache2` tambien.

```shell
systemctl start apache2
systemctl enable apache2
```

Pondremos lo siguiente:

```shell
sudo a2enmod rewrite
systemctl restart apache2
```

Ahora vamos a realizar unos cambios en `apache2` haciendo lo siguiente:

```shell
sudo nano /etc/apache2/apache2.conf

#Dentro del nano
<Directoy /var/www>
	Options Indexes FollowSymLinks
	AllowOverride All
	Require all granted
</Directoy>
```

En la linea de `AllowOverride` estara como `None` se lo cambiaremos a `All`.

Reiniciamos el servicio por si acaso:

```shell
systemctl restart apache2
```

Y ya tendriamos el servidor de `apache2` configurado correctamente.

Ahora instalaremos `PHP` y una libreria de `apache2` sobre `PHP`:

```shell
sudo apt install php libapache2-mod-php
```

Y con esto se nos instalara lo necesario para que interprete bien `PHP`.

Ahora vamos a instalar `mysql-server` y la dependencia de `PHP` respecto a `mysql`:

```shell
sudo apt install mysql-server php-mysql
```

Una vez instalado todas las dependencias, vamos a reiniciar los 2 servicios, por si acaso:

```shell
systemctl restart mysql
systemctl restart apache2
```

Ahora lo que vamos hacer es establecer una contraseña al usuario `root` en `mysql`, donde funcionara la aplicacion de `mutillidae`:

```shell
sudo mysql -u root
```

Dentro de la linea de comandos de `mysql` haremos lo siguiente:

```shell
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mutillidae';
```

Si vemos un `Query OK...` significa que todo fue correctamente.

Por lo que saldremos de la base de datos con `exit`, reiniciamos la base de datos de `mysql`.

```shell
systemctl restart mysql
```

Vamos a irnos a la carpeta donde vamos a instalar `mutillidae` que seria en:

```shell
cd /var/www/html
```

Antes de instalarlo, vamos a instalar algunas dependencias que puede requerir la instalacion:

```shell
sudo apt install php-curl php-mbstring php-xml
```

Y vamos a instalar una herramienta la cual nos permitira descargar el repositorio desde la terminal llamada `git`.

```shell
sudo apt install git
```

Ahora nos tendremos que ir al `github` de `mutillidae` y copiar el link, para descargarlo en nuestro `host`:

```shell
sudo git clone https://github.com/webpwnized/mutillidae.git
```

Reiniciaremos nuestro servicio de `apache2` para que se guarde todo correctamente:

```shell
systemctl restart apache2
```

Y nos iremos a la pagina de `mutillidae` desde el navegador web, poniendo lo siguiente:

```
URL = http://localhost/mutillidae
```

Nos va a dar un pequeño error por que no puede acceder a la base de datos `mysql`, pero solo le tendremos que dar donde pone `Click here`, le daremos a `Ok` y con esto ya tendriamos la pagina de `mutillidae` corriendo perfectamente y lista para nuestro `hacking etico`.

Y ahora desde nuestra maquina atacante podemos acceder a esta pagina poniendo la IP de la maquina de la pagina de `mutillidae` mas la ruta donde esta:

```
URL = http://<IP>/mutillidae
```
