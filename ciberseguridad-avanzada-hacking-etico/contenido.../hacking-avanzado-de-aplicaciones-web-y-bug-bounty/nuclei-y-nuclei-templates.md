---
icon: radiation
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

# Nuclei y Nuclei Templates

La herramienta `nuclei` es muy famosa a dia de hoy para encontrara diferentes vulnerabilidades web, ya que utiliza una plantilla con una gran comunidad con diferentes vulnerabilidades que se han econtrado hasta dia de hoy probando cada una de ellas, la introduccion de como crear nuestra propia plantilla para colaborar en formato `YAM` esta en el siguiente link:

URL = [Templates Guide Nuclei](https://docs.projectdiscovery.io/templates/introduction)

El repositorio oficial es el siguiente:

URL = [Nuclei GitHub](https://github.com/projectdiscovery/nuclei)

Esta herramienta como comente antes utiliza diversas plantillas de la comunidad creadas en `YAM` las cuales contiene rutas o vulnerabilidades va a probar en la pagina web que le pasemos como parametro, en el repositorio estan ordenados pro años y por tipo de vulnerabilidades para que podamos ver la estructura de la vulnerabilidad, es una herramienta muy util para este ambito.

La herramienta no viene por defecto en `kali` por lo que tendremos que instalarla de la siguiente forma:

```shell
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

Echo esto tendremos instalada la herramienta, si es verdad que puede tardar un poco, ahora una vez instalada instalaremos los `templates` de la herramienta.

```shell
nuclei --update-templates
```

Info:

```
                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.3.8

                projectdiscovery.io

[INF] nuclei-templates are not installed, installing...
[INF] Successfully installed nuclei-templates at /home/kali/nuclei-templates
[INF] No new updates found for nuclei templates
```

Ahora vamos a testear la herramienta contra un objetivo de la maquina que tenemos levantada de antes.

```shell
nuclei -u http://192.168.5.211:8080 -ni 
```

Con el `-u` especificamos el target donde queremos escanear. Con el `-ni` especificamos que no nos haga una resolucion `DNS` para que asi no tarde tanto.

Si lo dejamos asi va a utilizar todas las plantillas que haya actualmente para hacer la prueba de vulnerabilidades contra el `target`, pero si le ponemos el parametro `-t` especificamos que plantillas queremos que utilice o que grupo de plantillas y con el `-l` podremos especificar un listado de `targets` como `subdominios, dominios, IP's, etc...` que queramos que utilice.

Info:

```
                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.3.8

                projectdiscovery.io

[WRN] Found 2 templates with runtime error (use -validate flag for further examination)
[INF] Current nuclei version: v3.3.8 (latest)
[INF] Current nuclei-templates version: v10.1.2 (latest)
[WRN] Scan results upload to cloud is disabled.
[INF] New templates added in latest release: 52
[INF] Templates loaded for current scan: 7654
[INF] Executing 7274 signed templates from projectdiscovery/nuclei-templates
[WRN] Loading 380 unsigned templates for scan. Use with caution.
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 1693 (Reduced 1591 Requests)
[phpinfo-files] [http] [low] http://192.168.5.211:8080/phpinfo.php ["5.5.9"] [paths="/phpinfo.php"]
[waf-detect:apachegeneric] [http] [info] http://192.168.5.211:8080
[form-detection] [http] [info] http://192.168.5.211:8080/login.php
[robots-txt] [http] [info] http://192.168.5.211:8080/robots.txt
[tech-detect:google-font-api] [http] [info] http://192.168.5.211:8080/login.php
[tech-detect:php] [http] [info] http://192.168.5.211:8080/login.php
[tech-detect:php] [http] [info] http://192.168.5.211:8080/portal.php
[tech-detect:php] [http] [info] http://192.168.5.211:8080
[robots-txt-endpoint] [http] [info] http://192.168.5.211:8080/robots.txt
[old-copyright] [http] [info] http://192.168.5.211:8080/login.php ["&copy; 2014"]
[http-missing-security-headers:strict-transport-security] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:x-content-type-options] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:cross-origin-embedder-policy] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:cross-origin-resource-policy] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:referrer-policy] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:clear-site-data] [http] [info] http://192.168.5.211:8080/login.php                                                                                            
[http-missing-security-headers:cross-origin-opener-policy] [http] [info] http://192.168.5.211:8080/login.php                                                                                 
[http-missing-security-headers:content-security-policy] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:permissions-policy] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:x-frame-options] [http] [info] http://192.168.5.211:8080/login.php
[http-missing-security-headers:x-permitted-cross-domain-policies] [http] [info] http://192.168.5.211:8080/login.php
[web-config] [http] [info] http://192.168.5.211:8080/web.config
```

Vemos que nos saca mucha informacion, pero no solo sirve para las paginas web, si no que tambien se puede contra un `host` pudiendo sacar diferentes vulnerabilidades que pueda tener en los puertos u otro tipo de cosas a nivel de red.

```shell
nuclei -u 192.168.5.211 -ni 
```

Info:

```
                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.3.8

                projectdiscovery.io

[WRN] Found 2 templates with runtime error (use -validate flag for further examination)
[INF] Current nuclei version: v3.3.8 (latest)
[INF] Current nuclei-templates version: v10.1.2 (latest)
[WRN] Scan results upload to cloud is disabled.
[INF] New templates added in latest release: 52
[INF] Templates loaded for current scan: 7654
[INF] Executing 7274 signed templates from projectdiscovery/nuclei-templates
[WRN] Loading 380 unsigned templates for scan. Use with caution.
[INF] Targets loaded for current scan: 1
[INF] Running httpx on input host
[INF] Found 1 URL from httpx
[INF] Templates clustered: 1693 (Reduced 1591 Requests)
[waf-detect:apachegeneric] [http] [info] http://192.168.5.211
[options-method] [http] [info] http://192.168.5.211 ["GET,POST,OPTIONS,HEAD"]
[apache-detect] [http] [info] http://192.168.5.211 ["Apache/2.4.29 (Ubuntu)"]
[old-copyright] [http] [info] http://192.168.5.211 ["\u00a9 2021"]
[http-missing-security-headers:strict-transport-security] [http] [info] http://192.168.5.211
[http-missing-security-headers:content-security-policy] [http] [info] http://192.168.5.211
[http-missing-security-headers:x-content-type-options] [http] [info] http://192.168.5.211
[http-missing-security-headers:x-permitted-cross-domain-policies] [http] [info] http://192.168.5.211
[http-missing-security-headers:cross-origin-opener-policy] [http] [info] http://192.168.5.211
[http-missing-security-headers:permissions-policy] [http] [info] http://192.168.5.211
[http-missing-security-headers:x-frame-options] [http] [info] http://192.168.5.211
[http-missing-security-headers:referrer-policy] [http] [info] http://192.168.5.211
[http-missing-security-headers:clear-site-data] [http] [info] http://192.168.5.211
[http-missing-security-headers:cross-origin-embedder-policy] [http] [info] http://192.168.5.211
[http-missing-security-headers:cross-origin-resource-policy] [http] [info] http://192.168.5.211
```

Y ya con esto podremos utilizarlo para cualquier cosa, es una herramienta bastante buena y util, que podremos utilizar en cualquier parte.
