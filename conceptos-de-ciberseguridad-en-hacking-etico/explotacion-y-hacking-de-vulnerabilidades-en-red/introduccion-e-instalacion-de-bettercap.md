# Introducción e instalación de Bettercap

Para obtener mas informacion de esta herramienta nos podremos ir a la pagina oficial de la herramienta en `GitHub` con el siguiente link:

URL = [Bettercap GitHub](https://github.com/bettercap/bettercap)

Esta herramienta no viene por defecto en `kali` por lo que la tendremos que instalar:

```shell
sudo apt-get install bettercap
```

Si ahora nosotros pusieramos `bettercap` entraremos dentro del entorno de linea de comandos de la propia herramienta:

<figure><img src="../../.gitbook/assets/image (119) (1).png" alt=""><figcaption></figcaption></figure>

Si ponemos `help` nos sacara la info de los modulos que hay:

<figure><img src="../../.gitbook/assets/image (120) (1).png" alt=""><figcaption></figcaption></figure>

Si por ejemplo queremos ver informacion de un modulo, podremos hacerlo poniendo:

```shell
help <MODULE>
```

> EJEMPLO:

```shell
help arp.spoof
```

Info:

```
arp.spoof (not running): Keep spoofing selected hosts on the network.

   arp.spoof on : Start ARP spoofer.
     arp.ban on : Start ARP spoofer in ban mode, meaning the target(s) connectivity will not work.
  arp.spoof off : Stop ARP spoofer.
    arp.ban off : Stop ARP spoofer.

  Parameters

    arp.spoof.fullduplex : If true, both the targets and the gateway will be attacked, otherwise only the target (if the router has ARP spoofing protections in place this will make the attack fail). (default=false)
      arp.spoof.internal : If true, local connections among computers of the network will be spoofed, otherwise only connections going to and coming from the external network. (default=false)
  arp.spoof.skip_restore : If set to true, targets arp cache won't be restored when spoofing is stopped. (default=false)
       arp.spoof.targets : Comma separated list of IP addresses, MAC addresses or aliases to spoof, also supports nmap style IP ranges. (default=<entire subnet>)
     arp.spoof.whitelist : Comma separated list of IP addresses, MAC addresses or aliases to skip while spoofing. (default=)
```

Podremos ver la informacion del modulo en cuestion.
