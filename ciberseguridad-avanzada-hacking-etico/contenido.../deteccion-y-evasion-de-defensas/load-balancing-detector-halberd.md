---
icon: scale-balanced
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

# Load Balancing detector - halberd

Un balanceador de carga es lo que esta por delante de los servidores, el cual se utiliza para cuando los usuarios envian un gran numero de peticiones o una carga de datos mas grande, estos balanceadores distribuyen esa carga por los demas servidores para que no se lo coma uno todo entero y asi evite problemas en general.

Si nosotros intentamos enumerar los servicios de un servidor, pero tiene un balanceador de carga por delante, lo que vamos a enumerar seran los servicios del balanceador de carga en vez de el del servidor y esto no nos interesa, pero lo que si podremos hacer sera identificar si tiene un balanceador de carga de la siguiente forma:

```shell
lbd <DOMAIN>
```

> `ldb` es (`Load Balancing Detector`)

Si ejecutamos estos y en la parte llamada:

```
Checking for DNS-Loadbalancing
```

Pone `FOUND` significa que tiene un balanceador de carga, y nosotros podremos `Bypassear` este balanceador de carga.

Pero otra herramienta que tambien es muy buena para estos casos se denomina `halberd` y se encuentra en el siguiente repositorio:

URL = [halberd GitHub](https://github.com/jmbr/halberd)

Nos tendremos que clonar el repositorio de la siguiente forma:

```shell
git clone https://github.com/jmbr/halberd.git
cd halberd/
```

Ahora ejecutamos lo siguiente para que se nos instale de forma correcta.

```shell
sudo python2 setup.py install
```

Ahora si hacemos desde cualquier parte del sistema este comando:

```shell
halberd -h
```

Info:

```
Usage: halberd [OPTION]... URL

Discover web servers behind HTTP load balancers.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v, --verbose         explain what is being done
  -q, --quiet           run quietly
  -d, --debug           enable debugging information
  -t NUM, --time=NUM    time (in seconds) to spend scanning the target
  -p NUM, --parallelism=NUM
                        specify the number of parallel threads to use
  -u FILE, --urlfile=FILE
                        read URLs from FILE
  -o FILE, --out=FILE   write report to the specified file
  -a ADDR, --address=ADDR
                        specify address to scan
  -r FILE, --read=FILE  load clues from the specified file
  -w DIR, --write=DIR   save clues to the specified directory
  --config=FILE         use alternative configuration file
```

Veremos que funciona de forma correcta, por lo que haremos lo siguiente:

```shell
halberd <DOMAIN>
```

Y con esto lo que va ha realizar es hacer lo mismo que la anterior herramienta de `ldb` pero en este caso dara mas informacion como por ejemplo las `IP's` que estan corriendo dentras de dicho balanceador.

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Aqui nos muestra las direcciones `IP` pero de los balanceadores, la `IP` publica del servidor web real no se encuentra ahi, pero la unica forma de poder `Bypassear` esto seria intentando encontrar la direccion publica del servidor real y esto se puede conseguir utilizando tecnicas pasivas de recopilacion de informacion como por ejemplo utilizando `sodan`, `censis`, etc...
