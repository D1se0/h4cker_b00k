---
icon: spider-black-widow
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

# Fuzzing

## <mark style="color:purple;">Descubrir directorios</mark>

A parte de `Gobuster` tambien podemos utilizar una herramienta bastante mas potente llamada `wfuzz`...

```shell
wfuzz -c --hc=404 -t 200 -w <WORDLIST> http://<IP>/FUZZ
```

Con el `-c` estamos añadiendo color a la informacion que adquiramos, con `--hc=404` lo que hacemos es ocultar los codigos `404` ya que no nos interesan por que significa que no existen los directorios, con el `-t 200` lo que hacemos es realizar este escaneo con `200` hilos por lo que ira mas rapidos, como si hicieramos `200` tareas a la vez cada segundo...

Tambien podemos buscar por extensiones, en concreto con especificat haciendo lo siguiente...

```shell
wfuzz -c --hc=404 -t 200 -w <WORDLIST> http://<IP>/FUZZ.<EXTENSION>
```

> EJEMPLO

```shell
wfuzz -c --hc=404 -t 200 -w <WORDLIST> http://<IP>/FUZZ.php
```

Y en este caso te buscara a fuerza bruta los archivos que contengan `.php`...

### Crear 2 o mas directorios a la vez con `mkdir`

Entendiendo que los directorios `/home/user/` existen pero los siguientes no, lo que hara sera crear los directorios que detecte que no exsiste...

```shell
mkdir -p /home/user/example/example2
```

De esta manera se habrian creado 2 directorios a la vez llamados `/example/example2`...

## <mark style="color:purple;">Curl</mark>

Una de los principios basicos para utilizar la herramienta `curl` es cuando quieres hacer una peticion a una pagina web de manera que te lo muestre en terminal el contenido de la misma de forma simple, pero a veces se ve muy mal, por lo que utilizaremos el siguiente comando para que se vea mucho mejor...

```shell
curl -s -X GET "http://<IP>/" | htmlq -p | batcat -l html
```

Con esto lo que haremos sera solicitar la peticion a esa `IP` y que nos la muestre en terminal su contenido a la vez de que nos lo muestre en formato `html` y con el color propio del lenguaje de `html`...

Si por ejemplo nos interesa mas ver lo que hay entre `""` lo que haremos sera filtrar mediante el siguiente comando (Esto lo hacemos ya que normalmente los `css`,`js`, etc... estan entre `""`)

```shell
curl -s -X GET "http://<IP>/" | htmlq -p | batcat -l html | grep -oP '".*?"'
```

Y si queremos a parte filtrar todo eso por un nombre que nos interese buscar...

```shell
curl -s -X GET "http://<IP>/" | htmlq -p | batcat -l html | grep -oP '".*?"' | grep <NAME>\.
```

Tambien para que nos muestre las que no se repitan...

```shell
curl -s -X GET "http://<IP>/" | htmlq -p | batcat -l html | grep -oP '".*?"' | grep <NAME>\. | sort -u
```

Y esto nos mostrara en terminal el contenido filtrado de la pagina acorde a los que estemos buscando...

Generalmente en un `js` viene bien mirar ya que podemos encontrar en el propio codigo `subdominios` o `URL's` interesantes, por lo que si queremos filtrar alguna posible ruta distinta a la conocida por algun `js` encontrado haremos lo siguiente...

```shell
curl -s -X GET "http://<IP>/js/<NAME_JAVASCRIPT>.js"
```

Con esto solo te aparecera su contenido, pero si filtramos por lo que dije anteriormente...

```shell
curl -s -X GET "http://<IP>/js/<NAME_JAVASCRIPT>.js" | grep "\.<EXTENSION_URL>"
```

> EJEMPLO

```shell
curl -s -X GET "http://<IP>/js/<NAME_JAVASCRIPT>.js" | grep "\.htb"
```

o

```shell
curl -s -X GET "http://<IP>/js/<NAME_JAVASCRIPT>.js" | grep "\.com"
```

Y si por ejemplo queremos filtrar por el contenido entre `""` como hicimos anteriormente ya que puede ser contenido sensible y a parte por el comienzo de `http`, tambien seguido de que solo te aparezcan los que no esten repetidos, seria de la siguiente forma...

```shell
curl -s -X GET "http://<IP>/js/<NAME_JAVASCRIPT>.js" | grep -oP ".*?" | grep http | sort -u
```

