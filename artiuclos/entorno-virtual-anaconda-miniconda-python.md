---
icon: python
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

# Entorno virtual Anaconda/Miniconda Python

En algunos casos algunas herramientas de `github` o de cualquier otra plataforma, que esten echas con `python` en este caso pueden dar error dependiendo de la version de `python` que soporte dicha herramienta, por lo que esta herramienta llamada `Conda` crea un entorno virtual en el que nosotros podremos especificar que tipo de version de `python` queremos que tenga dicho entorno para asi poder ejecutar la herramienta dentro de ese entorno virtual, es muy util para herramientas de `python` las cuales estan desactualizadas o que queramos utilizar alguna version anterior que ya no tenga soporte con el `python3`, para realizar todo esto haremos lo siguiente:

Primero nos descargaremos la herramientas de `Conda`:

```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Seguidamente la ejecutaremos:

```shell
bash Miniconda3-latest-Linux-x86_64.sh
```

Nos pedira una serie de opciones, pero recomiendo dejarlo todo por defecto, dandole a `ENTER` y escribiendo `yes` cuando te lo pida.

Una vez instalada, si abrimos una nueva terminal veremos que en el `prompt` de nuestro usuario estara en la parte izquierda `(base)` lo que significa que se instalo correctamente, pero esto lo podremos desactivar de la siguiente forma:

```shell
conda config --set auto_activate_base false
```

Ahora si abrimos otra terminal, ya no nos deberia de aparecer eso.

Ahora crearemos el entorno virtual con la herramienta de `conda` especificando que tipo de version de `python` queremos, por ejemplo si necesitamos utilizar un `python2.7` lo podremos hacer de la siguiente forma:

```shell
conda create -n test_env pip python=2.7
```

Con el parametro `-n` especificamos el nombre que le queremos dar al entorno virtual.

Con ese comando ya lo abriamos creado, ahora para activar el entorno y entrar dentro del mismo, lo haremos con el siguiente comando:

```shell
conda activate test_env
```

Y en el `prompt` aparecera `(test_env)` por lo que nos indica que estamos dentro del entorno de `conda` que hemos creado.

Con esto ya tendremos el `python2.7` y podremos instalar los requisitos de dicha herramienta o lo que queramos.

Una vez que ya queramos salir del entorno, pondremos lo siguiente:

```shell
conda deactivate
```

Y ya veremos como nuestro `prompt` vuelve a la normalidad.
