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

# Identificación de contenido - Dirbuster

Vamos a utilizar una de las herramientas posiblemente mas conocidas que hay en este descubrimiento de recursos o directorios web, pero que bajo mi opinion no es la mejor opcion, la encontraremos en el siguiente repositorio:

URL = [Dirbuster GitHub](https://github.com/KajanM/DirBuster)

Despues de explicar un poco esta herramienta pasaremos de la misma seccion pero con otra herramienta que es una de las mas utilizadas y que esa si es la que mas utilizo.

Esta herramienta viene por defecto en `kali`, por lo que vamos a probar a utilizarla de la siguiente forma:

```shell
dirbuster -u http://<IP>:8899/
```

Lo que esta realizando aqui es una serie de `fuerza bruta` con el diccionario que le pasemos probando cada una de las palabras por si alguna de ellas existiera con su codigo de pagina (`200, 403, 500, etc...`) pero es una tecnica muy intrusiva, por lo que no es muy recomendable paar entornos reales.

<figure><img src="../../.gitbook/assets/image (183).png" alt=""><figcaption></figcaption></figure>

Si le damos a `Start` empezara el proceso, cuando termina podremos generar un reporte de lo que ha encontrado pudiendo investigarlo por nuestra cuenta en la propia `URL`.

<figure><img src="../../.gitbook/assets/image (184).png" alt=""><figcaption></figcaption></figure>

El propio `kali` ya te viene implementado los diccionarios de palabras que puedes probar a utilizar con la herramienta en la siguiente ruta.

```shell
ls -la /usr/share/wordlists/dirbuster/
```

Info:

```
total 7592
drwxr-xr-x 2 root root    4096 Nov 30 07:24 .
drwxr-xr-x 4 root root    4096 Nov 30 07:24 ..
-rw-r--r-- 1 root root   71638 Feb 27  2009 apache-user-enum-1.0.txt
-rw-r--r-- 1 root root   90418 Feb 27  2009 apache-user-enum-2.0.txt
-rw-r--r-- 1 root root  546618 Feb 27  2009 directories.jbrofuzz
-rw-r--r-- 1 root root 1802668 Feb 27  2009 directory-list-1.0.txt
-rw-r--r-- 1 root root 1980043 Feb 27  2009 directory-list-2.3-medium.txt
-rw-r--r-- 1 root root  725439 Feb 27  2009 directory-list-2.3-small.txt
-rw-r--r-- 1 root root 1849676 Feb 27  2009 directory-list-lowercase-2.3-medium.txt
-rw-r--r-- 1 root root  676768 Feb 27  2009 directory-list-lowercase-2.3-small.txt
```
