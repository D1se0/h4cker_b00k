---
icon: cloud-binary
---

# Herramienta Metagoofil

La primera herramienta que veremos sera la llamada `metagoofil` que encontraremos informacion en el siguiente repositorio de `GitHub`:

URL = [GitHub MetaGoofil](https://github.com/laramies/metagoofil)

No viene por defecto el `kali` pero si en los repositorios de descarga del mismo, por lo que la instalaremos:

```shell
sudo apt update
sudo apt-get install metagoofil
```

Y con esto habremos instalado la herramienta correctamente.

Para utilizar la herramienta sera muy sencillito, miraremos la ayuda con `-h` y si queremos buscar podremos hacerlo con el siguiente ejemplo:

```shell
metagoofil -d microsoft.com -l 10 -t pdf,doc,ppt -o /home/d1se0/Desktop
```

Esta herramienta solo busca en `google` cuando la `FOCA` busca en muchos mas sitios.

El parametro `-d` es para especificar el dominio, el `-l` es para limitar los resultados que encuentre, el `-t` es para especificar la extension de los archivos que queremos que busque y el `-o` el destino de donde queremos que se descarguen dichos archivos.

Y con esto lo que hara sera descargarnos todos los archivos especificados que encuentre en las busquedas que haga la herramienta, por lo que puede tardar un poco.

La propia herramienta de `metagoofil` no lleva nada incorporado paar extraer metadatos y volcarlos a un archivo, por lo que podremos combinarlo con otra herramienta llamada `exiftool`.

```shell
sudo apt-get install exiftool
```

Y con esto ya la habriamos instalado.

Para sacar todos los metadatos de los archivos que nos descargo `metagoofil` podremos hacerlo con el siguiente comando:

```shell
exiftool -r *.pdf | egrep -i "Author|Creator|Email|Producer|Template" | sort -u
```

Lo que hacemos aqui es recorrer todos los ficheros `PDF` filtrandolo por `Author|Creator|Email|Producer|Template` que es la informacion importante

Nos iriamos donde estan todos los `PDF's` y ejecutamos ese comando.

Y esto nos mostrara la informacion de forma filtrada de todos los metadatos de los archivos.

Seguidamente podremos hacer lo mismo pero con los archivos `doc` cambiando lo siguiente:

```shell
exiftool -r *.doc | egrep -i "Author|Creator|Email|Producer|Template" | sort -u
```

Y asi continuamente dependiendo de que extension de archivos hayamos elegido.
