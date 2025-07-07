---
icon: gauge-max
---

# Control de velocidad de escaneo con Nmap

Con estas tecnicas lo que podemos hacer es controlar el tiempo y el rendimiento del escaneo de `nmap` para que podamos ser mas silenciosos a la hora de realizar dicho escaneo.

Nosotros podemos hacer que vaya con un `dedlay` de unos segundos por cada paquete que se envia de la siguiente forma:

```shell
sudo nmap -sS -n --scan-delay 1 192.168.20.128
```

Y esto va a tardar 1 segundo entre cada paquete que se envie.

`nmap` de normal escanea con una velocidad `-T3` que con este parametro se especifica como de agresivo queremos que sea el escaneo, cuanto mas alto el numero mas rapido ira, pero mas expuestos estaremos, el maximo es el `-T5` y cuanto menos sea el numero mas lento ira, pero mas seguro sera.

```shell
sudo nmap -sS -n -T5 192.168.20.128
```

Esto hara un escaneo muy rapido, pero poco seguro.

```shell
sudo nmap -sS -n -T0 192.168.20.128
```

Este sin embargo hara un escaneo mas lento, pero mas seguro (Se le llama el `Escaneo Paranoico`).

> NOTA:

Una curiosidad de `nmap` es que si esta en mitad de un escaneo procesandose y le damos a la tecla `r` nos pondra en la terminal el porcentaje de como va el escaneo, para saber cuanto puede llegara a tardar.

Lo que vamos hacer para ser indetectable en casi cualquier `IDS` que se este ejecutando, es crear un pequeño script de `bash` para poder realizar un escaneo de forma segura, pero que no tarde tanto como en los casos anteriores.

> scan\_advanced.sh

```bash
#!/bin/bash

for i in {0..30..2}; do; sudo nmap -sS -p$(($i+1))-$(($i+2)) -n 192.168.20.128; sleep 40; done;
```

Si aun asi nos siguen detectando, podremos cambiar el `sleep` y aumentarlo entorno a lo que la herramienta `IDS` no detecte.
