---
icon: key-skeleton
---

# Privilege Escalation

### Escaneo de Privilegios y Capacidades

#### Binarios SUID

```bash
find / -type f -perm -4000 -ls 2>/dev/null
```

* Busca archivos con bit SUID activo
* `-perm -4000`: Permisos SUID (Set User ID)
* `2>/dev/null`: Oculta errores de permisos

#### Capacidades Linux

```bash
getcap -r / 2>/dev/null
```

* Busca binarios con capacidades especiales
* `-r`: Recursivo desde directorio raíz
* Capacidades permiten privilegios sin SUID

### Escaneo Automatizado

#### LinPEAS (Privilege Escalation Awesome Script)

```bash
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

* Script de enumeración automática
* Detecta vectores de escalada de privilegios
* Chequea configuraciones inseguras
