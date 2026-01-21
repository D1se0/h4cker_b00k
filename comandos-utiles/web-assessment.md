---
icon: bomb
---

# Web Assessment

#### Dirbuster

```bash
dirbuster -u http://<IP>:<PORT>/
```

Herramienta GUI para fuzzing de directorios, automáticamente prueba combinaciones comunes.

#### Nikto (Escáner Web)

```bash
nikto -h http://<IP> -C all
```

* `-h`: Host objetivo
* `-C all`: Mostrar todos los chequeos
* Detecta vulnerabilidades web comunes
* Incluye checks de configuración insegura
