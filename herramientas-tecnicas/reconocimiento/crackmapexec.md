---
icon: user-magnifying-glass
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

# Crackmapexec

Si tenemos unas credenciales que pueden ser validas las probamos con la siguiente herramienta al puerto de `smb`...

```shell
crackmapexec smb <IP> -u '<USER>' -p '<PASSWORD>'
```

Si nos salta con un resultado `[+]` y despues las credenciales separadas por `:` es que las credenciales son correctas, si no, serian incorrectas...

Para comprobar si definitivamente nos podemos conectar a la maquina con esas credenciales, probaremos el siguiente comando, que es solamente sustituyendo el parametro `smb` por el de `winrm`...

```shell
crackmapexec winrm <IP> -u '<USER>' -p '<PASSWORD>'
```

Si el resultado a parte de lo anteriormente dicho sale a la derecha de las credenciales el siguiente nombre de esta manera...

```
(Pwn3d!)
```

Significa que ya nos podremos conectar por `evil-winrm`...

Ya que despues para autenticarnos utilizariamos la herramienta `evil-winrm` que actua como un `ssh` en linux...

