# Pesidious (Mutaciones con Deep Learning)

Lo primero para descargar la herramienta nos tendremos que ir a su repositorio, que estara en el siguiente link:

URL = [Pesidious GitHub](https://github.com/CyberForce/Pesidious)

Lo que hace esta herramienta es coger el `malware` que nosotros le pasamos, realizan transformaciones y lo convierte en un fichero nuevo, por lo que hace que no sea detectable para los antivirus, teniendo una `backdoor` dentro.

Esta herramienta es bastante complicada de instalar, por lo que puede dar muchos problemas, pero si fuera asi solamente tendremos que buscar en internet como solucionar dichos problemas y asi sucesivamente, en este caso vamos abordar generalmente los errores que pueden haber solucionandolo para que funcione en el 90% de los casos cambiando algunos ficheros que lleva la herramienta, primero tendremos que descargarnos su repositorio:

```shell
git clone https://github.com/CyberForce/Pesidious.git
cd Pesidious/
```

Despues haremos lo siguiente:

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
```

Ejecutado esto, le daremos a `ENTER` cuando nos lo pida para que lo añada.

Una vez echo esto nos dejara instalar `python3.6` de la siguiente forma:

```shell
sudo apt-get install python3.6
```

Y ahora instalaremos `pip` de esta manera:

```shell
curl https://bootstrap.pypa.io/get-pip.py | sudo -H python3.6
```

Ahora dentro del directorio de la herramienta, tendremos que modificar un fichero.

Tendremos que hacer lo siguiente:

```shell
nano pip_requirements/requirements.txt

#Dentro del nano
Pygments==2.6.0
```

Tendremos que editar esa seccion de ahi para dejarla en `2.6.0`.

Y ahora si podremos ejecutar lo siguiente:

```shell
python3.6 -m pip install -r pip_requirements/requirements.txt
```

Y con esto ya estaria todo instalado, por lo que tendremos que pasarnos la aplicacion que anteriormente nos habiamos `backdoorizado` al `Ubuntu` para poder usarlo con esta herramienta, pero lo tendremos que meter en una carpeta la cual podemos llamarlo como queramos, en mi caso la llamare `putty`.

Si nosotros queremos saber cuanto porcentaje tendria un antivirus en detectarnos nuestro `malware` podremos hacerlo con el siguiente modulo de esta herramienta:

```shell
python3.6 classifier.py -d ../putty
```

Y ya aqui te mostraria la informacion clasificandolo por tipo de `malware`, el porcentaje, etc... En este caso da un 92% de probabilidades de que lo detecte un antivirus.

Por lo que vamos a mutarlo, para que se baje bastante el porcentaje de que no lo detecte un antivirus de la siguiente forma:

```shell
python3.6 mutate.py -d ../putty
```

Y esto se pondra a cambiarlo, mutarlo, etc... Tardara un poco, pero cuando haya terminado podremos ver que nos ha creado una ruta con el archivo mutado:

```
Mutated_malware/mutated_puttyX.exe
```

Ahora si lo volvemos a clasificar de la siguiente forma:

```shell
python3.6 classifier.py -d Mutated_malware
```

Podremos ver que ahora nos pone que es de tipo `Benign` (Por lo que lo detecta como bueno) y que tiene un 50% de probabilidades de que lo puedan detectar, por lo que hemos conseguido reducirlo un 50% el echo de que nos lo puedan detectar.

Ahora solo habria que probarlo en un `windows` que si lo probamos no nos lo detectara un antivirus.
