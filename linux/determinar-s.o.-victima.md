---
icon: brake-warning
---

# Determinar S.O. (Victima)

Para determinar el S.O. de una maquina tendremos que fijarnos en el numero de `TTL` cuando se hace un `ping`...

```shell
ping -C 1 <VICTIM_IP>
```

Con esto enviaremos un paquete a la maquina victima y sabremos si responde con el mismo paquete, por lo que sabremos que nos hace `ping` y que podriamos interactuar con la misma...

```shell
ping -C 1 <VICTIM_IP> -R
```

Con eso podremos ver de manera mas detallada el proceso que hace el paquete desde nuestra `IP` hasta la suya...

De las dos manera podremos ver la opcion donde pone `ttl=` el numero que ponga ahi podremos determinal si es una maquina `Linux` o `Windows` ya que se diferencian con que la de `Linux` tiene un `ttl` de hasta `64` y las de `Windows` tienen un `ttl` de hasta `128` y para automatizar todo esto con utilizar el siguiente script en `python` nos lo dira directamente...

```python
#!/usr/bin/python3
#coding: utf-8

import re, sys, subprocess
from termcolor import colored

# python3 wichSystem.py <IP>

if len(sys.argv) != 2:
    print("\n[!] Uso: python3 " + sys.argv[0] + " <direccion-ip>\n")
    sys.exit(1)

def get_ttl(ip_address):
    # Usar el comando ping con -c 1 para un solo ping
    proc = subprocess.Popen("ping -c 1 %s" % ip_address, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    
    # Verificar si hubo un error
    if proc.returncode != 0:
        print(colored("\n[!] Error al hacer ping a la dirección IP\n", 'red'))
        sys.exit(1)
    
    # Convertir la salida a cadena y buscar el valor TTL usando una expresión regular
    out = out.decode('utf-8')
    ttl_value = re.search(r'ttl=(\d+)', out)
    
    # Verificar si se encontró el TTL en la salida
    if ttl_value:
        return ttl_value.group(1)
    else:
        print(colored("\n[!] No se pudo obtener el TTL de la respuesta del ping\n", 'red'))
        sys.exit(1)

def get_os(ttl):
    ttl = int(ttl)

    if ttl >= 0 and ttl <= 64:
        return "Linux"
    elif ttl >= 65 and ttl <= 128:
        return "Windows"
    else:
        return "Not Found"

if __name__ == '__main__':
    ip_address = sys.argv[1]

    ttl = get_ttl(ip_address)
    os_name = colored(get_os(ttl), 'blue')
    print(colored("\n[+] %s (ttl -> %s): %s\n" % (ip_address, ttl, os_name), 'yellow'))
```

