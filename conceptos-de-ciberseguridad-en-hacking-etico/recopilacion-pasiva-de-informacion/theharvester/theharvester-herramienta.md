# TheHarvester Herramienta

Es una herramienta bastante famosa la cual vamos a utilizar posteriormente, se encontraria en el siguiente repositorio de `GitHub`.

URL = [GitHub TheHarvester](https://github.com/laramies/theHarvester)

Esta herramienta nos proporciona informacion de algun dominio que queramos investigar, proporcionandole si queremos en la pagina en la que queremos que busque para que sea una busqueda mas exacta como por ejemplo que busque por `shodan` y despues que tipo de navegador queremos que utilice a la hora de que busque, es una herramienta muy completa y se utilizaria de la siguiente forma:

```shell
theHarvester -d microsoft.com -b baidu -l 100 
```

Con el `-d` especificamos el dominio al que queremos investigar. Con el `-b` especificamos la fuente donde queremos que haga la consulta del dominio. Con el `-l` especificamos un limite de resultados que nos aparezcan.

Por lo que si lo ejecutamos nos mostrara la informacion de las busquedas que ha realizado y los resultados que ha encontrado poniendonos todas las IP's , con los subdominios que tenga ese dominio, etc...

Al buscar por todo esto y sobre todo que nos muestre las IP's donde esta corriendo esos dominios, nos puede servir como un vector de entrada posteriormente.

Si queremos especficarle varias fuentes de navegadores a las que queremos que busque y que la herramienta lo permita lo podremos hacer de la siguiente forma:

```shell
theHarvester -d microsoft.com -b baidu,yahoo,duckduckgo,bing -l 100 
```

Con esto lo mas probable es que obtengamos mas resultados con diferentes navegadores, pero verlo en la terminal toda la informacion volcada es un poco caotico a la hora de analizarlo, por lo que podremos volcar toda la informacion en un fichero.

```shell
theHarvester -d microsoft.com -b baidu,yahoo,duckduckgo,bing -l 100 -f resultados
```

Con el `-f` especificamos que queremos volcarlo a un archivo toda la informacion obtenida.

Por lo que si ejecutamos esto se nos creara un fichero `.json` y `.xml` llamado `resultados` en el que estara toda la informacion obtenida de la busqueda.

Pero de esta herramienta, hay una version antigua que esta mucho mejor en la que se pueden buscar mas cosas, pero que la quitaron, por lo que vamos a descargar esa version de la siguiente forma.

Buscaremos en `google` "`miniconda download linux`", con esto lo que vamos hacer es que como la herramienta funciona con `linux` vamos a instalar por asi decirlo un entorno virtual dentro de nuestra maquina `kali` en la que instalemos esas dependencias antiguas de forma aislada, sin afectar a las dependencias modernas de nuestro `kali` en `python`.

Nos lo descargamos el `miniconda` en el siguiente link:

URL = [Download miniconda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)

Para instalarlo haremos lo siguiente:

```shell
bash Miniconda3-latest-Linux-x86_64.sh
```

Lo ejecutaremos y pulsaremos `ENTER` de nuevo para que se instale, despues pulsamos la `Q`, despues pondremos `yes` lo ejecutamos y pulsamos `ENTER` despues.

Con esto ya se estaria instalando la herramienta, una vez que se termine de instalar, tendremos que escribir `yes` y ejecutarlo, con esto ya estaria todo instalado correctamente.

Si abrimos una terminal nueva, tendremos que ver la palabra `(base)` a la izquierda del usuario o del prompt de la terminal, en tal caso de que no apareciera tendremos que hacer lo siguiente:

```shell
echo 'export PATH="$HOME/miniconda3/bin:$PATH" >> ~/.zshrc'
```

```shell
source miniconda3/bin/activate
```

Y con esto ya lo tendriamos 100%.

Si no queremos que nos aparezca eso de `(base)` a la izquierda, podremos ocultarlo de la siguiente forma:

```shell
conda config --set auto_activate_base false
```

Ahora tendremos que cerrar la terminal y volverla abrir, con esto ya veremos que se oculto correctamente.

Ahora vamos a crear el entorno virtual con `conda`.

```shell
conda create -n "old_harvester" python=3.8.0
```

Especificamos el nombre que le queremos dar con el `-n` y con `python` la version que queremos importar a ese entorno virtual.

Pulsaremos `ENTER` cuando se este instalando y aparezca `([y]/n)`, y con esto ya estaria instalado todo correctamente.

Y para entrar en el entorno o activarlo, simplemente tendremos que poner:

```shell
conda activate old_harvester
```

Para tenerlo todo mas ordenado vamos a crear una carpeta y acceder a ella estando en dicho entorno.

```shell
mkdir old_harvester
cd old_harvester/
```

Ahora tendremos que irnos a la siguiente link:

URL = [Version antigua de TheHarvester](https://github.com/laramies/theHarvester/archive/refs/tags/3.2.2.zip)

Lo descargaremos directamente con `wget`.

```shell
wget https://github.com/laramies/theHarvester/archive/refs/tags/3.2.2.zip
```

```shell
unzip 3.2.2.zip
```

```shell
rm 3.2.2.zip
cd theHarvester-3.2.2
```

Una vez descomprimido el archivo y estando dentro de ella tendremos que instalar las dependencias, por lo que lo haremos de la siguiente forma.

```shell
pip install -r requeriments/base.txt
```

Y ahora si hacemos...

```shell
python theHarvester.py -h
```

Podremos ver que ahora mismo se puede buscar en mas navegadores sin tener las limitaciones que teniamos en el actualizado.

Pero si cerramos la terminal nos sacara automaticamente del entorno virtual, por lo que para volver acceder a ese dicho entorno tendremos que poner lo siguiente:

```shell
cd old_harvester/
conda activate old_harvester
```

Y ahora si la podremos utilizar correctamente en este entorno virtual, por lo que buscaremos con `google` de la misma forma que hicimos anteriormente.

```shell
python theHarvester.py -d microsoft.com -b google -l 100 -f resultados2
```

Estos ficheros nos lo gardaria en formatos `.html` y `.xml`

Por lo que si queremos visualizar los resultados del `.html` lo podremos hacer de la siguiente forma:

```shell
firefox resultados2.html
```

Y con esto se nos abre el `firefox` con el `.html` de los resultados que volco al mismo y se podra observar que los resultados a la hora de visualizarlo en una pagina es mucho mejor para analizarlo todo.

Si por ejemplo queremos utilizar otro que no sea `googl` por ejemplo con `trello` que suele ser muy buena esa tambien, se haria de la siguiente forma:

```shell
python theHarvester.py -d microsoft.com -b trello -l 100 -f resultados2
```

Y esto nos mostrara muchisima informacion, ya que es un buscador en el cual se pueden encontrar credenciales o informacion muy sensible.

Y si queremos utilizar todos los buscadores de los que permite la herramienta, lo podremos hacer de la siguiente forma:

```shell
python theHarvester.py -d microsoft.com -b all -l 100 -f resultados2
```

Y esto plasmara la informacion de todos los buscadores que tiene la herramienta dando muchisima informacion.

Esta herramienta al realizar muchas peticiones, muchas veces se bloquea la IP para que no puedas realizar mas busquedas en algunos navegadores, esto se puede solucionar de la siguiente forma.
