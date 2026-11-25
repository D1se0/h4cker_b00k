---
icon: globe-pointer
---

# Fuzzing Web

### Fuzzing de Directorios y Archivos

#### Gobuster

```bash
gobuster dir -u http://<IP> -w <WORDLIST> -x php,html,txt -t 100 -k -r
```

* `-u`: URL objetivo
* `-w`: Wordlist para fuzzing
* `-x`: Extensiones de archivo a buscar
* `-t`: Número de hilos concurrentes
* `-k`: Ignorar certificados SSL
* `-r`: Seguir redirecciones

#### Dirb

```bash
dirb https://<IP>:<PORT>/ <WORDLIST>
```

* Escanea directorios web usando wordlists predefinidas
* Soporta SSL/TLS automáticamente

#### FFuf (Fuzz Faster U Fool)

```bash
ffuf -u http://<IP>/file.php\?FUZZ\=/etc/passwd -w <WORDLIST> -fs <SIZE>
```

* `-u`: URL con marcador FUZZ
* `-w`: Wordlist
* `-fs`: Filtrar por tamaño de respuesta

```bash
ffuf -u http://domain.local/ -w <WORDLIST> -H "Host: FUZZ.domain.local" -fs <SIZE>
```

* `-H`: Header personalizado con fuzzing
* Útil para virtual host discovery
