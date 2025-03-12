---
icon: book-skull
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

# Evil-winrm

Si la herramienta no esta instalada...

```shell
gem install evil-winrm
```

Teniendo unas credenciales para conectarnos mediante esta herramienta, haremos lo siguiente...

```shell
evil-winrm -i <IP> -u '<USER>' -p '<PASSWORD>'
```

Si todo esto ha funcionado, tendriamos una shell interactiva dentro del servidor y se habria vulnerado (Ya digo es como un `ssh` de linux, pero en `Windows`)

