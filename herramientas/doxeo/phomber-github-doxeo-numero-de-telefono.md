---
icon: mobile-notch
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

# Phomber GitHub (Doxeo Numero de Teléfono)

Es una herramienta de doxeo sobre numeros de telefono y mas opciones, pero esta especializado en numeros de telefono, de primeras hay que instalar los requerimientos y ya despues iniciarla, esta herramienta te proporciona informacion sobre dicho numero, diciendo la compañia, el pais, proporcionando links sobre que paginas esta registrado dicho numero y 2 paginas donde se puede ver mas informacion detallada sobre el numero, es una herramientas bastante buena para doxear un numero de telefono.

Lo primero que tendremos que hacer sera irnos a la siguiente pagina:

URL = [Phomber GitHub](https://github.com/s41r4j/phomber)

Despues copiaremos el link para clonarlo en nuestro kali.

```shell
git clone https://github.com/s41r4j/phomber.git
cd phomber/
```

A veces da errores de instalacion con `python3` por lo que crearemos un `enviroment` de `python3` para que se haga todo perfectamente.

```shell
python3 -m venv venv
source venv/bin/activate
venv\Scripts\activate
```

Una vez creado todo lo anterior, ahora si instalaremos lo necesario de la siguiente forma:

```shell
sudo apt install pipx
pip install pip-tools
pip-compile pyproject.toml
pip install -r requirements.txt
pip install poetry
poetry install
```

Terminado de instalar todo lo necesario, ahora si podremos iniciar la herramienta de la siguiente forma:

```shell
python3 phomber.py
```

Esto te metera en una especie de shell con la herramienta, si escribimos `help` podremos ver las opciones que ofrece la herramienta, pero en nuestro caso doxearemos un numero de telefono.

```shell
number <EXTENSION><NUMBER>
```

> EJEMPLO

```shell
number +34123456789
```

Y si lo ejecutamos nos pondra toda la informacion del numero de telefono (Informacion limitada), proporcionando links tambien para poder investigar mejor dicho numero de telefono.
