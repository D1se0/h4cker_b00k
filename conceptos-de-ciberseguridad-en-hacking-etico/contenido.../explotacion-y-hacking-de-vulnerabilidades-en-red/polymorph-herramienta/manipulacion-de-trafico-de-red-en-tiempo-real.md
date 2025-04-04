# Manipulación de trafico de red en tiempo real

Lo que vamos hacer es modificar el trafico de red, los paquetes de red originales que se estan intercambiando entre los 2 `nodos` legitimos de la red.

No solamente vamos a mandar paquetes falsos, si no que vamos a modificar los paquetes originales para que la informacion que contienen sea diferente de manera que podamos engañar alguno de los puntos de la conexion.

> NOTA IMPORTANTE:

Esta serie de tecnicas que vamos a ver es de un nivel bastante avanzado y es muy complejo de entender, ya que vamos hacerlo todo a muy bajo nivel, en el campo de la red.

La herramienta que vamos a utilizar para hacer esto se llama `Polymorph` y esta en el siguiente link:

URL = [Polymorph GitHub](https://github.com/shramos/polymorph)

Para instalarlo, pondremos los siguiente comandos:

```shell
sudo su
sudo apt update
sudo apt install build-essential python3-dev libnetfilter-queue-dev tshark tcpdump python3-pip wireshark git
pip3 install git+https://github.com/kti/python-netfilterqueue
pip3 install polymorph
```

Una vez que ya este instalada, solamente tendremos que poner lo siguiente para acceder a dicha herramienta que tendra su propia linea de comandos:

```shell
polymorph
```

Info:

```

 ██████╗  ██████╗ ██╗  ██╗   ██╗███╗   ███╗ ██████╗ ██████╗ ██████╗ ██╗  ██╗
 ██╔══██╗██╔═══██╗██║  ╚██╗ ██╔╝████╗ ████║██╔═══██╗██╔══██╗██╔══██╗██║  ██║
 ██████╔╝██║   ██║██║   ╚████╔╝ ██╔████╔██║██║   ██║██████╔╝██████╔╝███████║
 ██╔═══╝ ██║   ██║██║    ╚██╔╝  ██║╚██╔╝██║██║   ██║██╔══██╗██╔═══╝ ██╔══██║
 ██║     ╚██████╔╝███████╗██║   ██║ ╚═╝ ██║╚██████╔╝██║  ██║██║     ██║  ██║
 ╚═╝      ╚═════╝ ╚══════╝╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝
                                                < Santiago Hernandez Ramos >

PH >
```

Lo que primero haremos con esta herramienta sera capturar un paquete de red, dicha herramienta lo que hara sera generar una "plantilla" donde nosotros podremos modificar dicho paquete de red donde podremos ejecutar funciones de codigo en `python` sobre los nuevos paquetes de red que se esten intercambiando entre 2 maquinas, de manera que nosotros podamos modificar su contenido a nuestro gusto.
