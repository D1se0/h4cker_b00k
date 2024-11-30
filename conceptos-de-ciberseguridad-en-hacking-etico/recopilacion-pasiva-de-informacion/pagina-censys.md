# Pagina Censys

URL = [Pagina Censys](https://search.censys.io)

Cuando superar las 10 consultas te piden logearte, por lo que lo mejor es logearte desde un principio ya que es totalmente gratis.

Una de las herramientas que es muy util para combinarlo con `Censys` seria la llamada `zmap` que es como `nmap` pero mucho mejor optimizado para el escaneo de grandes volumenes de nodos en la red como por ejemplo podria ser `internet`, que a la vez tambien esta herramienta utiliza otra herramienta llamada `zgrab`.

URL = [Pagina de Zmap](https://zmap.io)

URL = [Pagina de GitHub de Zgrab](https://github.com/zmap/zgrab2)

Esta pagina `Censys` es muy parecida a `Shodan` ya que las busquedas siguen el mismo mecanismo y te muestra la informacion indexada de forma similar.

Pero en este buscador se puede buscar directamente por organizacion sin necesidad de proporcionarle un comando en concreto, igualmente tiene sus propios comandos de busqueda.

Por ejemplo si queremos buscar por una organizacion en concreto y un puerto en concreto respecto a esa organizacion, podremos hacerlo de la siguiente forma:

```
(youtube) AND protocols:"3389/rdp"
```

Por ejemplo aqui estamos buscando a `youtube` respecto al puerto `RDP` que es para el acceso a control remoto de un equipo, suele ser bastante jugoso para los hackers.
