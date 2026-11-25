---
icon: magnifying-glass
---

# Reconocimiento

#### WhatWeb (Fingerprinting Web)

```bash
whatweb http://<IP>
```

* Identifica tecnologías web
* Detecta CMS, frameworks, servidores
* Muestra versiones y plugins

#### Nikto (Escáner Web)

```bash
nikto -h http://<IP> -C all
```

* `-h`: Host objetivo
* `-C all`: Mostrar todos los chequeos
* Detecta vulnerabilidades web comunes
* Incluye checks de configuración insegura
