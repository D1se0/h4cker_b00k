---
icon: route
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

# Identificación de subdominios - Subfinder, Sublist3r y Subbrute

La primera herramienta que veremos sera la de `Subfinder` esta herramienta busca de forma pasiva que eso es muy importante un `subdominio` desde ese dominio, ya que si tiene herramientas de seguridad y realizaramos fuerza bruta nos podrian detectar, pero esta herramienta lo hacer de forma pasiva con ayuda de la informacion de internet.

URL = [Subfinder GitHub](https://github.com/projectdiscovery/subfinder)

No viene por defecto en `kali` por lo que tendremos que instalarlo de la siguiente forma:

```shell
sudo apt install subfinder
```

Vamos hacer la prueba con una pagina muy conocida para realizar estos testeos llamado `hackthissite.org`, por lo que haremos lo siguiente:

### Subfinder

```shell
subfinder -d hackthissite.org 
```

Con el `-d` especificamos el dominio que queremos investigar.

Info:

```
               __    _____           __         
   _______  __/ /_  / __(_)___  ____/ /__  _____
  / ___/ / / / __ \/ /_/ / __ \/ __  / _ \/ ___/
 (__  ) /_/ / /_/ / __/ / / / / /_/ /  __/ /    
/____/\__,_/_.___/_/ /_/_/ /_/\__,_/\___/_/

                projectdiscovery.io

[INF] Current subfinder version v2.6.0 (outdated)
[INF] Loading provider config from the default location: /home/kali/.config/subfinder/provider-config.yaml
[INF] Enumerating subdomains for hackthissite.org
vm-200.outbound.firewall.hackthissite.org
mta-sts.hackthissite.org
www.hackthissite.org
ctf.hackthissite.org
speedtest2.hackthissite.org
irc-www.hackthissite.org
hackthissite.org
htsv4.hackthissite.org
lille.irc.hackthissite.org
vm-150.outbound.firewall.hackthissite.org
status-new.hackthissite.org
stats.hackthissite.org
status.hackthissite.org
h5ai.hackthissite.org
data.hackthissite.org
lille.irc-v6.hackthissite.org
new-irc.hackthissite.org
legal.hackthissite.org
v3stage.hackthissite.org
git.hackthissite.org
irc-wolf.hackthissite.org
vm-099.outbound.firewall.hackthissite.org
ns2.hackthissite.org
v3dev.hackthissite.org
www.irc.hackthissite.org
vm-050.outbound.firewall.hackthissite.org
daemon.hackthissite.org
shadow.hackthissite.org
wolf.irc-v6.hackthissite.org
wolf.irc.hackthissite.org
irc.hackthissite.org
api.hackthissite.org
mail.hackthissite.org
forums.hackthissite.org
pi.hackthissite.org
mirror.hackthissite.org
v3stage-cdn.hackthissite.org
irc-v6.hackthissite.org
irc-ipv6.hackthissite.org
staff.hackthissite.org
qdb.hackthissite.org
vm-005.outbound.firewall.hackthissite.org
jupiter.hackthissite.org
ns1.hackthissite.org
irc-hub.hackthissite.org
[INF] Found 45 subdomains for hackthissite.org in 16 seconds 531 milliseconds
```

Con esto veremos todos los `subdominios` que nos muestra de dicha pagina y todo esto sacado de fuetentes de internet y sin realizar ningun tipo de fuerza bruta hacia el dominio en concreto.

Pero si lo queremos tener todo en un fichero lo haremos de la siguiente forma.

```shell
subfinder -d hackthissite.org > output_subfinder.txt
```

Info:

```
[INF] Detected old /home/kali/.config/subfinder/config.yaml config file, trying to migrate providers to /home/kali/.config/subfinder/provider-config.yaml
[INF] Migration successful from /home/kali/.config/subfinder/config.yaml to /home/kali/.config/subfinder/provider-config.yaml.

               __    _____           __         
   _______  __/ /_  / __(_)___  ____/ /__  _____
  / ___/ / / / __ \/ /_/ / __ \/ __  / _ \/ ___/
 (__  ) /_/ / /_/ / __/ / / / / /_/ /  __/ /    
/____/\__,_/_.___/_/ /_/_/ /_/\__,_/\___/_/

                projectdiscovery.io

[INF] Current subfinder version v2.6.0 (outdated)
[INF] Loading provider config from /home/kali/.config/subfinder/provider-config.yaml
[INF] Enumerating subdomains for hackthissite.org
[INF] Found 45 subdomains for hackthissite.org in 3 seconds 289 milliseconds
```

### Sublist3r/Subbrute

La otra herramienta se denomina `sublist3r` que estaria en el siguiente repositorio.

URL = [Sublist3r GitHub](https://github.com/aboul3la/Sublist3r)

Pero dentro de ese repositorio tiene implementada otra herramienta mejor llamada `Subbrute` que se encontraria en la siguiente direccion:

URL = [Subbrute GitHub](https://github.com/TheRook/subbrute)

Tendremos que instalar `sublist3r` ya que no viene por defecto en `kali` de la siguiente forma:

```shell
sudo apt install sublist3r
```

Y se utilizaria de la siguiente forma.

```shell
sublist3r -d hackthissite.org -v
```

Info:

```

                 ____        _     _ _     _   _____
                / ___| _   _| |__ | (_)___| |_|___ / _ __
                \___ \| | | | '_ \| | / __| __| |_ \| '__|
                 ___) | |_| | |_) | | \__ \ |_ ___) | |
                |____/ \__,_|_.__/|_|_|___/\__|____/|_|

                # Coded By Ahmed Aboul-Ela - @aboul3la
    
[-] Enumerating subdomains now for hackthissite.org
[-] verbosity is enabled, will show the subdomains results in realtime
[-] Searching now in Baidu..
[-] Searching now in Yahoo..
[-] Searching now in Google..
[-] Searching now in Bing..
[-] Searching now in Ask..
[-] Searching now in Netcraft..
[-] Searching now in DNSdumpster..
[-] Searching now in Virustotal..
[-] Searching now in ThreatCrowd..
[-] Searching now in SSL Certificates..
[-] Searching now in PassiveDNS..
[!] Error: Virustotal probably now is blocking our requests
SSL Certificates: status.hackthissite.org
SSL Certificates: ctf.hackthissite.org
SSL Certificates: mail.hackthissite.org
SSL Certificates: lille.irc.hackthissite.org
SSL Certificates: irc.hackthissite.org
SSL Certificates: irc-v6.hackthissite.org
SSL Certificates: lille.irc-v6.hackthissite.org
SSL Certificates: h5ai.hackthissite.org
SSL Certificates: wolf.irc.hackthissite.org
SSL Certificates: wolf.irc-v6.hackthissite.org
SSL Certificates: www.hackthissite.org
SSL Certificates: www.irc.hackthissite.org
SSL Certificates: mta-sts.hackthissite.org
SSL Certificates: status-new.hackthissite.org
SSL Certificates: irc-ipv6.hackthissite.org
SSL Certificates: irc-wolf.hackthissite.org
SSL Certificates: new-irc.hackthissite.org
[-] Total Unique Subdomains Found: 17
www.hackthissite.org
ctf.hackthissite.org
h5ai.hackthissite.org
irc.hackthissite.org
www.irc.hackthissite.org
lille.irc.hackthissite.org
wolf.irc.hackthissite.org
irc-ipv6.hackthissite.org
irc-v6.hackthissite.org
lille.irc-v6.hackthissite.org
wolf.irc-v6.hackthissite.org
irc-wolf.hackthissite.org
mail.hackthissite.org
mta-sts.hackthissite.org
new-irc.hackthissite.org
status.hackthissite.org
status-new.hackthissite.org
```

Vemos que aqui nos ha encontrado solamente `17` cuando en `subfinder` nos encontro unos `62` subdominios, por eso es mucho mejor `subfinder`, ya que tambien tiene muchas mas fuentes de informacion en las que buscar.

Y para utilizar `subbrute` la podremos utilizar con la opcion `-b` en la herramienta, pero hay que tener cuidado, ya que esto si puede generar mucho trafico y ser detectados por herramientas de seguridad, es de las ultimas opciones que deberiamos hacer.

```shell
sublist3r -d hackthissite.org -v -b -o output_subbrute.txt
```

Info:

```

                 ____        _     _ _     _   _____
                / ___| _   _| |__ | (_)___| |_|___ / _ __
                \___ \| | | | '_ \| | / __| __| |_ \| '__|
                 ___) | |_| | |_) | | \__ \ |_ ___) | |
                |____/ \__,_|_.__/|_|_|___/\__|____/|_|

                # Coded By Ahmed Aboul-Ela - @aboul3la
    
[-] Enumerating subdomains now for hackthissite.org
[-] verbosity is enabled, will show the subdomains results in realtime
[-] Searching now in Baidu..
[-] Searching now in Yahoo..
[-] Searching now in Google..
[-] Searching now in Bing..
[-] Searching now in Ask..
[-] Searching now in Netcraft..
[-] Searching now in DNSdumpster..
[-] Searching now in Virustotal..
[-] Searching now in ThreatCrowd..
[-] Searching now in SSL Certificates..
[-] Searching now in PassiveDNS..
[!] Error: Virustotal probably now is blocking our requests
SSL Certificates: status.hackthissite.org
SSL Certificates: ctf.hackthissite.org
SSL Certificates: mail.hackthissite.org
SSL Certificates: lille.irc.hackthissite.org
SSL Certificates: irc.hackthissite.org
SSL Certificates: irc-v6.hackthissite.org
SSL Certificates: lille.irc-v6.hackthissite.org
SSL Certificates: h5ai.hackthissite.org
SSL Certificates: wolf.irc.hackthissite.org
SSL Certificates: wolf.irc-v6.hackthissite.org
SSL Certificates: www.hackthissite.org
SSL Certificates: www.irc.hackthissite.org
SSL Certificates: mta-sts.hackthissite.org
SSL Certificates: status-new.hackthissite.org
SSL Certificates: irc-ipv6.hackthissite.org
SSL Certificates: irc-wolf.hackthissite.org
SSL Certificates: new-irc.hackthissite.org
[-] Starting bruteforce module now using subbrute..
hackthissite.org
forum.hackthissite.org
api.hackthissite.org
stats.hackthissite.org
git.hackthissite.org
forums.hackthissite.org
```

Y esto nos hara el escaneo principal, mas los `subdominios` que vaya encontrando con fuerza bruta, pero lo pare ya que estaba tardando mucho.

### Subfinder API Key

Si nos volvemos a la herramienta `subfinder` podremos ver un apartado en `GitHub` el cual nos explica que podremos utilizar `API's` con la herramienta.

Esto lo podremos editar y ver, para implementar o no alguna `API` en el siguiente archivo de configuracion:

```shell
nano ~/.config/subfinder/config.yaml 
```

Dentro del archivo veremos lo siguiente:

```
# subfinder config file
# generated by https://github.com/projectdiscovery/goflags

# domains to find subdomains for
#domain: []

# file containing list of domains for subdomain discovery
#list: 

# specific sources to use for discovery (-s crtsh,github). use -ls to display all available sources.
#sources: []

# use only sources that can handle subdomains recursively (e.g. subdomain.domain.tld vs domain.tld)
#recursive: false

# use all sources for enumeration (slow)
#all: false

# sources to exclude from enumeration (-es alienvault,zoomeye)
#exclude-sources: []

# subdomain or list of subdomain to match (file or comma separated)
#match: []

#  subdomain or list of subdomain to filter (file or comma separated)
#filter: []

# maximum number of http requests to send per second
#rate-limit: 0

# number of concurrent goroutines for resolving (-active only)
#t: 10

# update subfinder to latest version
#update: false

# disable automatic subfinder update check
#disable-update-check: false

# file to write output to
#output: 

# write output in jsonl(ines) format
#json: false

# directory to write output (-dl only)
#output-dir: 

# include all sources in the output (-json only)
#collect-sources: false

# include host ip in output (-active only)
#ip: false

# flag config file
#config: /home/kali/.config/subfinder/config.yaml

# provider config file
#provider-config: /home/kali/.config/subfinder/provider-config.yaml

# comma separated list of resolvers to use
#r: []

# file containing list of resolvers to use
#rlist: 

# display active subdomains only
#active: false

# http proxy to use with subfinder
#proxy: 

# exclude ips from the list of domains
#exclude-ip: false

# show only subdomains in output
#silent: false

# show version of subfinder
#version: false

# show verbose output
#v: false

# disable color in output
#no-color: false

# list all available sources
#list-sources: false

# report source statistics
#stats: false

# seconds to wait before timing out
#timeout: 30

# minutes to wait for enumeration results
#max-time: 10%  
```

En esta parte le podremos implementar la pagina web, junto a la `API` para que busque tambien ahi los `subdominios`.

### Sublist3r Puertos

En la herramienta de `Sublist3r` podremos ver que puertos estan abiertos en los dominios que encuentre, solo que esto ya es un reconocimiento bastante activo, por lo que hay que tener cuidado.

```shell
sublist3r -d hackthissite.org -v -p 80,443
```

Con el `-p` especificamos los puertos que queremos que escanee en los `subdominios` que encuentre.
