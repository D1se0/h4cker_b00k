---
icon: globe-wifi
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

# Identificación de tecnologías web - WhatWeb y WebAnalyzer

Primero empecemos con la herramienta de `Whatweb` que la podremos encontrar en el siguiente repositorio de `GitHub`:

URL = [Whatweb GitHub](https://github.com/urbanadventurer/WhatWeb)

Con esta herramienta lo que podremos hacer sera analizar una pagina web, ya sea mediante una `IP`, dominio, subdominio, etc... Va analizar la tecnologia que se implementa en dicha pagina web, a parte de ver que librerias se esta utilizando, posibles errores para aprovechar, etc.. Con unos `1800` plugins los cuales vienen incorporados en la herramienta, sobre todo es muy utilizada para ver versiones de `software` y asi posteriormente ver si hubiera algun exploit asociado a dicha version.

Viene por defecto en `kali`, por lo que si abrimos una terminal y para probarla utilizaremos la maquina que nos descargamos anteriormente la llamada `VPLE`:

```shell
whatweb http://192.168.5.211:8899/
```

Info:

```
http://192.168.5.211:8899/ [200 OK] Apache[2.4.7], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.7 (Ubuntu)], IP[192.168.5.211], JQuery, Script, Title[Security Ninja]
```

Si queremos algo de forma mas detallada podremos ponerle el `-v` de la siguiente forma:

```shell
whatweb -v http://192.168.5.211:8899/
```

Pero si queremos que no utilice el modo silencioso y que realice mas peticiones de forma activa a la pagina para que nos de mucha mas informacion, podremos ponerle el nivel `4`:

```shell
whatweb -a 4 http://192.168.5.211:8899/
```

Y esto lo que hara sera generar mucho trafico de red, pero te dara una informacion muy detallada y exacta de lo que esta corriendo en esa pagina web, versiones, etc...

Luego esta la otra herramienta llamada `WebAnalyzer` que es como `Whatweb` pero menos indetectable ya que se suele utilizar menos:

URL = [WebAnalyzer GitHub](https://github.com/rverton/webanalyze)

Esta herramienta no viene instalada en `kali`, lo que hace es la misma funcion que `whatweb` pero te detalla mucho mas la informacion y de forma mejor estructurada, es una herramienta bastante buena.

```shell
go install github.com/rverton/webanalyze/cmd/webanalyze@latest
wget https://raw.githubusercontent.com/rverton/webanalyze/master/technologies.json
```

Y con esto ya tendremos instalada la herramienta.

```shell
webanalyze -host http://192.168.5.211:8899/
```

Info:

```
 :: webanalyze        : v0.3.9
 :: workers           : 4
 :: technologies      : technologies.json
 :: crawl count       : 0
 :: search subdomains : true
 :: follow redirects  : false

http://192.168.5.211:8899/ (0.0s):
    Apache HTTP Server, 2.4.7 (Web servers)
    Ubuntu,  (Operating systems)
```

Vemos que en nada de tiempo nos muestra la informacion de la pagina web.
