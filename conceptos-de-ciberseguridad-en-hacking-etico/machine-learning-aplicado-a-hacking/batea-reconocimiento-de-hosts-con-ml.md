# BATEA (Reconocimiento de hosts con ML)

> ERROR DE INSTALACIÓN BATEA

Para instalar BATEA en un entorno virtual de Anaconda/Miniconda, puedes seguir los siguientes pasos:

1. Crea un nuevo entorno virtual en anaconda/miniconda: `conda create -n batea_env pip python=3.7`
2. Activa el entorno: `conda activate batea_env`
3. Accede a la carpeta de `batea` que has descargado
4. Instala los paquetes externos (**no uses pip3**): `pip install -r requirements.txt`
5. Instala batea: `pip install -e .`
6. Ejecuta batea introduciendo el comando `batea` dos veces en la terminal.

Con esto debería funcionar correctamente.

La herramienta para descargarla la obtendremos del siguiente link:

URL = [BATEA GitHub](https://github.com/delvelabs/batea)

Lo que va hacer esta herramienta es clasificar en base a un ranking de que es mas interesante continuar investigando del punto de vista del `hacking ético`, para realizar esta clasificacion `BATEA` utiliza una serie de tecnicas de `Machine Learning` y concretamente se basa en un algoritmo que se denomina `Isolation Forest` (Algoritmo de deteccion de anomalias).

Por ejemplo nosotros realizamos un escaneo de servicios o de `hosts` en este caso con `nmap` y el `output` es lo que le tendremos que proporcionar a esta herramienta para que coja todos los `hosts` que ha descubierto con sus servicios y realice un ranking, es decir, una clasificacion de cuales de esos `hosts` tiene mas interes desde el punto de vista de seguridad para comenzar analizar.

Por lo que vamos a instalar la herramienta de la siguiente forma:

```shell
git clone https://github.com/delvelabs/batea.git
cd batea/
```

Y ahora tendremos que realizar los siguientes pasos:

```shell
python3 setup.py sdist
pip3 install -r requirements.txt
pip3 install -e .
```

Y ahora si ponemos `batea`, tendremos que ver esto:

```
Empty report, can't predict. 
Quitting
```

Ya que no le hemos pasado nada, pero para ver que funciona.

Por lo que vamos arrancar las maquinas de los anteriores ejercicios como por ejemplo:

```
Metasploitable3-Ubuntu
Metasploitable3-WindowsServer2008
Ubuntu-Mutillidae
Windows 10
```

Las maquinas mas vulnerables en este caso serian las 2 `metasploitables`, que tendrian las siguientes IP's:

```
Windows = 192.168.5.185
Ubuntu = 192.168.5.183
```

Activaremos esas y realizaremos un escaneo con `nmap` de la siguiente forma:

```shell
nmap -O -sV 192.168.5.0/24 -oX output.xml
```

Una vez que tengamos el fichero, haremos lo siguiente:

```shell
batea -n 2 output.xml
```

Con el parametro `-n` especificamos el numero de resultados que queremos que nos aparezca o que nos proporcione `batea` respecto al nivel de vulnerabilidad que tenga el `host`.

Info:

```
{
    "report_info": [
        {
            "number_of_hosts": 8,
            "features": [
                "ip_octet_0",
                "ip_octet_1",
                "ip_octet_2",
                "ip_octet_3",
                "port_count",
                "open_port_count",
                "low_port_count",
                "tcp_port_count",
                "named_service_count",
                "software_banner_count",
                "max_banner_length",
                "is_windows",
                "is_linux",
                "http_server_count",
                "database_count",
                "windows_domain_admin_count",
                "windows_domain_member_count",
                "port_entropy",
                "hostname_length",
                "hostname_entropy"
            ]
        }
    ],
    "host_info": [
        {
            "rank": "1",
            "host": "192.168.5.185"
        },
        {
            "rank": "2",
            "host": "192.168.5.183"
        }
    ]
}
```

Como estamos observando aqui, nos esta inidicando 2 `host` los cuales nos recomienda priorizar por el nivel de vulnerabilidad que tienen, y son las 2 `metasploitables` por lo que se esta ejecutando todo de forma correcta.
