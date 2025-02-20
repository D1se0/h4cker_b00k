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

# NMAP

Para hacer un `nmap` mas rapido que el tipico...

```shell
nmap -A <IP> -p-
```

Haremos lo siguiente ya que con este comando que se mostrara sera mucho mas rapido y sigiloso...

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP> -oG <FILE_NAME>
```

Con esto lo que hacemos es que nos escanee todos los puertos `-p-`, solo nos muestre los abiertos `--open`, lo haga por `TCP` y de forma sigilosa `-sS`, que escane `5000` puertos por segundo `--min-rate 5000`, que nos muestre un triple verbose por lo que nos vaya mostrando los puertos que vaya encontrando con todas estas caracteristicas en vez de tener que esperar hasta que termine `-vvv`, para que no nos aplique resolucion `DNS` `-n`, para desactivar la fase de descubrimiento de host y que sea mas rapido el proceso `-Pn` y para que toda esta informacion nos la guarde en un archivo de texto `-oG <FILE_NAME>`...

El formato con el que se exporta no es el mas bonito y para copiar solo los puertos que se muestran en el archivo de texto que se creo con `nmap` de forma rapida para posteriormente hacer una busqueda mas detallada de ellos, utilizaremos un script...

```python
#!/usr/bin/env python3

import re
import sys
import subprocess

def extract_ports(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found!")
        return

    # Extraer la dirección IP
    ip_match = re.search(r'^Host: ([\d\.]+)', content, re.MULTILINE)
    ip_address = ip_match.group(1) if ip_match else None

    if ip_address:
        print(f"\t[*] IP Address: {ip_address}")
    else:
        print("No IP address found or extraction failed.")
        return

    # Extraer los puertos abiertos
    ports = re.findall(r'(\d{1,5})/open', content)
    if ports:
        ports_str = ','.join(ports)
        print(f"\t[*] Open ports: {ports_str}")
    else:
        print("No ports found or extraction failed.")
        return

    # Verificar si xclip está instalado
    try:
        subprocess.run(['xclip', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("[*] xclip is not installed. Ports not copied to clipboard.")
        return

    # Copiar los puertos al portapapeles si xclip está disponible
    try:
        subprocess.run(['xclip', '-sel', 'clip'], input=ports_str.encode(), check=True)
        print("[*] Ports copied to clipboard")
    except subprocess.CalledProcessError as e:
        print(f"[*] Failed to copy ports to clipboard: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)
    
    extract_ports(sys.argv[1])
```

Ahora tendiendo los puertos copiados haremos un escaneo mas exhaustivo y generando un archivo con el contenido del mismo con el siguiente comando...

```shell
nmap -sCV -p<PORTS> <IP> -oN <FILE_NAME>
```

Si queremos utilizar un script con `nmap` de fuerza bruta para que vaya probando diversas rutas y que nos muestre solo las del estado codigo `200 OK` seria de la siguiente manera...

```shell
nmap --script http-enum -p<PORT> <TARGET> -oN <FILE_NAME>
```

