# WordPress: reconocimiento y vectores comunes

WordPress alimenta más del 40% de los sitios web públicos — lo que lo convierte en el CMS más atacado del mundo por simple probabilidad. Su popularidad y su ecosistema extenso de plugins y temas son, simultáneamente, sus puntos de mayor riesgo.

## Identificación y fingerprinting

```bash
# Detectar si el sitio usa WordPress
curl -s http://objetivo/ | grep WordPress

# Identificar temas en uso (muchos temas desactualizados tienen vulnerabilidades)
curl -s http://objetivo/ | grep themes

# Identificar plugins instalados
curl -s http://objetivo/ | grep plugins

# Acceso directo al panel de administración (siempre expuesto por defecto)
http://objetivo/wp-admin/
http://objetivo/wp-login.php
```

## WPScan: la herramienta de referencia para WordPress

```bash
# Enumeración completa (versión, temas, plugins, usuarios)
sudo wpscan --url http://objetivo/ --enumerate

# Solo usuarios
sudo wpscan --url http://objetivo/ --enumerate u

# Solo plugins activos
sudo wpscan --url http://objetivo/ --enumerate ap

# Con API token (más datos de vulnerabilidades conocidas)
sudo wpscan --url http://objetivo/ --enumerate --api-token TU_TOKEN
```

WPScan cruza los plugins y temas encontrados con su base de datos de vulnerabilidades conocidas — exactamente el mismo principio de "fingerprinting + búsqueda de CVEs" trabajado en el bloque de *Information Gathering*.

## Vectores de ataque más frecuentes

### Plugins y temas desactualizados

La causa más habitual de compromisos de WordPress no es el core en sí (que se parchea regularmente y tiene actualizaciones automáticas disponibles), sino plugins y temas que los administradores olvidan actualizar. WPScan identifica las versiones instaladas y las cruza con vulnerabilidades conocidas — SQLi, XSS, LFI, y RCE en plugins populares son hallazgos frecuentes.

### Enumeración de usuarios

WordPress expone por defecto el endpoint `/?author=1`, que redirige al perfil del usuario con ID 1 — revelando su nombre de usuario. Esto facilita ataques de fuerza bruta dirigidos:

```
http://objetivo/?author=1  → redirect a /author/admin  (nombre de usuario: admin)
http://objetivo/?author=2  → redirect a /author/editor
```

También vía la API REST de WordPress:
```
http://objetivo/wp-json/wp/v2/users
```

### Fuerza bruta de credenciales

Con usuarios identificados, se puede lanzar fuerza bruta contra el login. El método `xmlrpc` usa la API XML-RPC de WordPress y permite múltiples intentos en una sola petición HTTP (el mismo principio de batching que se vio en el bloque de GraphQL):

```bash
sudo wpscan --password-attack xmlrpc \
            -t 20 \
            -U admin \
            -P /usr/share/wordlists/rockyou.txt \
            --url http://objetivo/
```

### Plugin/tema editor del panel de administración

Con acceso al panel de administración, WordPress incluye un editor de archivos de temas y plugins que permite modificar directamente archivos PHP — un vector directo de ejecución de código que muchas instalaciones no deshabilitan explícitamente.

## Mitigación

- Actualizar WordPress, plugins y temas regularmente — activar actualizaciones automáticas del core.
- Deshabilitar el editor de archivos desde `wp-config.php`: `define('DISALLOW_FILE_EDIT', true);`
- Renombrar o proteger `/wp-admin/` con autenticación adicional a nivel de servidor.
- Deshabilitar la enumeración de usuarios (`/?author=`) y el endpoint REST de usuarios no autenticado.
- Usar contraseñas fuertes y activar 2FA para cuentas administrativas.
- Deshabilitar XML-RPC si no se usa: `add_filter('xmlrpc_enabled', '__return_false');`
- Implementar un plugin de seguridad que incluya rate limiting en el login.
- Eliminar plugins y temas inactivos — incluso desactivados pueden ser un vector si tienen vulnerabilidades.
