---
icon: circle-nodes
---

# Fragmentación de paquetes con Nmap

En la siguiente pagina oficial de `nmap` estara un link en la que hay diferentes parametros con la herramienta `nmap` para la evasion de herramientas de seguridad como `firewall's` o `IDS's` a la hora de realizar un escaneo:

URL = [Nmap bypass-firewalls-ids](https://nmap.org/book/man-bypass-firewalls-ids.html)

Si nosotros queremos partir los paquetes por `bytes` a la hora de realizar un escaneo de algun puerto, podremos hacerlo, ya que un paquete por defecto viene con `20 bytes` y si ponemos el parametro `-f` sin especificar nada, nos lo fragmentaria en paquetes de `8 bytes` para despues reeordenarlos y asi obtener el paquete original una vez finalizado el escaneo, `Snort` puede detectar este tipo de escaneos tambien de desfragmentacion y framentacion, ya que es muy tipico en ataques de `denegacion de servicio` los cuales se le envian al servidor paquetes fragmentados para que el mismo los recomponga y eso hacer perder mucho recursos del sistema, pero para realizar un escaneo de este tipo seria de la siguiente forma:

```shell
sudo nmap -sS -n -f -p80 192.168.20.128
```

Si nosotros queremos especificarle que nos mande paquetes de `16 bytes` en vez de de `8 bytes` para que asi `Snort` o este tipo de herramientas no nos detecte, seria de la siguiente forma:

```shell
sudo nmap -sS -n -ff -p80 192.168.20.128
```

Añadimos otra `f` mas para especificar la suma de los `bytes` que esto `ff = 8+8 = 16`.

Si nosotros le queremos decir otro tipo de longitud podremos hacerlo con el parametro `-mtu` pero tiene que ser mayor a `8` y multiplo de `8`.

```shell
sudo nmap -sS -n -mtu 24 -p80 192.168.20.128
```

En este caso estamos fragmentando los paquetes en `24 bytes` sin ser detectados por `Snort`.
