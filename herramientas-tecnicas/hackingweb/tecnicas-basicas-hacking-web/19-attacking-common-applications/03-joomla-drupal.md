# Joomla y Drupal

## Joomla

Joomla es el segundo CMS más extendido tras WordPress. Sigue el mismo patrón de auditoría: identificar la versión, buscar CVEs conocidos, y comprobar credenciales por defecto en el panel de administración.

### Fingerprinting

```bash
# Detectar Joomla por cabeceras o contenido HTML
curl -s http://objetivo/ | grep Joomla

# Identificar versión desde el README
curl -s http://objetivo/README.txt | head -n 5

# Versión exacta desde el manifiesto XML (más fiable)
curl -s http://objetivo/administrator/manifests/files/joomla.xml | xmllint --format -
```

El panel de administración siempre está en `/administrator/` — accesible por defecto sin ninguna protección adicional.

### droopescan — escaneo automatizado

```bash
pip3 install droopescan

# Escanear instalación de Joomla
droopescan scan joomla --url http://objetivo/
```

`droopescan` detecta la versión, componentes instalados, y los cruza con vulnerabilidades conocidas — el equivalente de WPScan para Joomla (y también soporta Drupal).

### Vectores frecuentes

- **Componentes (extensiones) desactualizados**: igual que WordPress con sus plugins — el ecosistema de extensiones de Joomla tiene un historial de vulnerabilidades importantes en componentes populares.
- **Panel de administración expuesto**: `/administrator/` accesible sin protección adicional. Credenciales débiles o por defecto permiten acceso total.
- **Versiones antiguas del core**: Joomla tiene un historial de vulnerabilidades graves en versiones sin parchear — SQLi, RCE, y escalada de privilegios.

### Mitigación

- Actualizar Joomla y todas las extensiones instaladas regularmente.
- Restringir acceso a `/administrator/` por IP o con autenticación adicional a nivel de servidor web.
- Usar contraseñas fuertes y 2FA para cuentas administrativas.
- Deshabilitar o eliminar extensiones no utilizadas.

---

## Drupal

Drupal es el CMS más usado en entornos gubernamentales y grandes organizaciones por su énfasis en seguridad y flexibilidad — pero sus vulnerabilidades ("Drupalgeddon", "Drupalgeddon2") han demostrado que incluso el CMS más "serio" puede tener fallos críticos en el core.

### Fingerprinting

```bash
# Detectar Drupal
curl -s http://objetivo/ | grep -i "drupal"
curl -s http://objetivo/CHANGELOG.txt | head -20  # revela versión
curl -s http://objetivo/core/CHANGELOG.txt         # Drupal 8+

# droopescan también soporta Drupal
droopescan scan drupal --url http://objetivo/
```

### Vectores frecuentes

- **Vulnerabilidades del core sin parchear**: las Drupalgeddon (CVE-2014-3704, CVE-2018-7600, CVE-2019-6340) afectaron a instalaciones masivas con RCE explotable de forma trivial. Si la versión está sin parchear, la búsqueda del CVE exacto es el primer paso.
- **Módulos contrib desactualizados**: igual que plugins/componentes en WordPress y Joomla.
- **Exposición de `/update.php`**: la página de actualización de Drupal puede ser accesible sin autenticación en algunas configuraciones.

### Mitigación

- Actualizaciones del core mediante el sistema oficial de Drupal — las actualizaciones de seguridad se marcan explícitamente.
- Proteger `/update.php` y otras rutas de administración.
- Revisar y actualizar módulos contrib con la misma prioridad que el core.

---

## El patrón común a todos los CMS

WordPress, Joomla, y Drupal comparten la misma arquitectura de riesgo:

1. **Core actualizado pero componentes no** — la mayoría de compromisos reales vienen del ecosistema de extensiones, no del core en sí.
2. **Panel de administración expuesto por defecto** — sin protección adicional a nivel de servidor.
3. **Historial de CVEs conocidos** — vulnerar una instalación antigua con un exploit público documentado es trivial si no se ha parcheado.
4. **Credenciales débiles o por defecto** — administradores que nunca cambiaron las credenciales de instalación inicial.

La metodología de auditoría es idéntica para los tres: fingerprinting de versión → búsqueda de CVEs → comprobación de credenciales → enumeración de componentes → auditoría de configuración.
