---
icon: sensor-on
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

# WAF detector - wafw00f

Un `WAF` es un `firewall` que suelen tener las aplicaciones web en los servidores para poder filtrar todas esas posibles vulnerabilidades web como por ejemplo un `XSS`, `SQL Injection`, etc... Es un bloqueador de todo este tipo de trafico que nos puede impedir realizar diversas tecnicas de `hacking` a nivel web.

Para poder evadir este tipo de `WAF` podremos utilizar la siguiente herramienta bastante famosa:

URL = [wafw00f GitHub](https://github.com/EnableSecurity/wafw00f)

Esta herramienta es muy util para detectar que tipo de `WAF` tenemos por delante en un servidor web, a parte de que tiene implementadas las firmas para muchisimos proveedores.

Esta herramienta viene por defecto en `kali` y es muy sencillita de utilizar.

```shell
wafw00f <DOMAIN>
```

Info:

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

En este caso lo que estamos viendo es hacia un servidor de `AWS` en la nube de `amazon` y por lo que vemos lo detecto sin ningun problema.

Ahora una vez identificado este tipo de `WAF` vamos a ver como evadir este tipo de herramientas de seguridad.
