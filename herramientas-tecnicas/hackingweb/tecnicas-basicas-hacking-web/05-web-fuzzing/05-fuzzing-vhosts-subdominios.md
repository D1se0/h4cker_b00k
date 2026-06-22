# Fuzzing de virtual hosts y subdominios

> Este apartado complementa lo visto en el bloque de *Information Gathering* (apartados de *Virtual Hosts* y *Enumeración de subdominios*), centrándose ahora en la mecánica práctica con Gobuster.

## Repaso rápido: vhost vs. subdominio

| Aspecto | Virtual Host | Subdominio |
|---|---|---|
| Identificación | Cabecera `Host` en la petición HTTP | Registro DNS apuntando a una IP |
| Propósito | Servir múltiples sitios desde un único servidor | Organizar secciones/servicios de un dominio |
| Riesgo típico | Vhosts mal configurados exponen apps internas | *Subdomain takeover* si el DNS apunta a un recurso ya no controlado |

## Fuzzing de virtual hosts con Gobuster

```bash
echo "10.10.10.5 ejemplo.htb" | sudo tee -a /etc/hosts

gobuster vhost -u http://ejemplo.htb:81 \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  --append-domain
```

- `gobuster vhost`: activa el modo de fuzzing de virtual hosts.
- `-u`: URL base del servidor objetivo.
- `-w`: wordlist de nombres candidatos.
- `--append-domain`: construye cada candidato como `palabra.ejemplo.htb`, añadiendo el dominio base — imprescindible en versiones recientes de Gobuster para que el `Host` enviado sea un nombre completo válido.

```
Found: admin.ejemplo.htb:81 Status: 200 [Size: 100]
```

Un código `200` (frente a, por ejemplo, `400` para hosts inexistentes que el servidor rechaza directamente) indica un virtual host real y accesible — exactamente la misma lógica de comparación de respuestas vista en el apartado de fuzzing de parámetros.

> Antes de empezar, hay que añadir manualmente una entrada al archivo `/etc/hosts` apuntando el dominio base hacia la IP del servidor objetivo — de lo contrario, la herramienta no podría siquiera resolver la URL base sobre la que construir cada candidato de `Host`.

## Fuzzing de subdominios con Gobuster

```bash
gobuster dns -d ejemplo.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

- `gobuster dns`: activa el modo de fuzzing DNS.
- `-d`: dominio objetivo.
- `-w`: wordlist de nombres de subdominio candidatos.

Internamente, Gobuster construye cada candidato (`palabra.ejemplo.com`) e intenta resolverlo vía DNS; si resuelve a una IP, se considera válido y se reporta.

## Por qué practicar ambos modos con la misma herramienta

Dominar Gobuster en sus distintos modos (`dir`, `dns`, `vhost`, y también `fuzz` para casos genéricos) evita tener que cambiar constantemente de herramienta según el tipo de fuzzing necesario en cada fase de la auditoría — la sintaxis se mantiene consistente, solo cambia el modo y el objetivo de la sustitución.

## Riesgos de seguridad asociados

- **Virtual hosts mal configurados**: pueden exponer aplicaciones internas (paneles de administración, entornos de desarrollo) que el equipo asumía protegidos por "no estar enlazados", cuando en realidad son perfectamente accesibles conociendo el nombre exacto.
- **Subdomain takeover**: si un registro DNS apunta a un recurso externo (por ejemplo, un servicio cloud) que ya no está en uso ni reclamado, un atacante puede registrar ese mismo recurso y tomar control efectivo del subdominio — un vector cada vez más común con la proliferación de servicios cloud que se desaprovisionan sin limpiar el DNS asociado.

Combinar el fuzzing activo descrito aquí con las fuentes pasivas vistas en *Information Gathering* (CT logs especialmente) sigue siendo la estrategia más completa: las fuentes pasivas revelan nombres reales sin coste de sigilo, y el fuzzing activo cubre los huecos que esas fuentes no alcanzan a mostrar.
