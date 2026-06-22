# Consideraciones generales de endurecimiento

## El patrón común a todas las aplicaciones comunes

A lo largo de este bloque, WordPress, Joomla, Drupal, Tomcat, Jenkins, Nagios, Zabbix, Splunk, GitLab y otras plataformas comparten el mismo perfil de vulnerabilidades:

1. **Credenciales por defecto no cambiadas** — el vector de menor coste y mayor frecuencia de éxito.
2. **Versiones del core sin parchear** — exploits públicos para vulnerabilidades conocidas.
3. **Componentes adicionales desactualizados** — plugins, extensiones, módulos.
4. **Configuración insegura por defecto** — funcionalidades peligrosas habilitadas por conveniencia de instalación.
5. **Exposición innecesaria a internet** — herramientas internas accesibles desde fuera sin necesidad.

## Checklist de endurecimiento transversal

### En el momento de instalación

- [ ] Cambiar todas las credenciales por defecto antes de cualquier uso.
- [ ] Revisar la configuración de seguridad que la propia documentación recomienda modificar.
- [ ] Registrar exactamente qué versión se instaló y de qué componentes adicionales.
- [ ] Deshabilitar funcionalidades no necesarias desde el inicio (consolas de script, endpoints de debug, métodos HTTP innecesarios).

### Control de acceso

- [ ] ¿La aplicación necesita ser accesible desde internet? Si no, restringir por IP o colocar detrás de VPN.
- [ ] Añadir autenticación adicional a nivel de servidor web (HTTP Basic Auth adicional, autenticación de cliente) para paneles de administración especialmente sensibles.
- [ ] Usar el principio de mínimo privilegio en cuentas de servicio y credenciales que la aplicación almacena.

### Mantenimiento continuo

- [ ] Proceso de actualización regular — tanto del core como de componentes adicionales.
- [ ] Monitorización de avisos de seguridad del proveedor.
- [ ] Eliminación de componentes (plugins, extensiones, módulos) no activamente utilizados.
- [ ] Auditoría periódica de cuentas de usuario — eliminar cuentas inactivas.

### Configuración del servidor web

- [ ] Mensajes de error personalizados que no revelen la versión del software subyacente.
- [ ] Cabeceras de seguridad HTTP correctamente configuradas.
- [ ] HTTPS obligatorio con certificado válido.
- [ ] Solo los métodos HTTP estrictamente necesarios habilitados.

## El valor de los escáneres especializados por plataforma

Cada una de las plataformas trabajadas en este bloque tiene su herramienta de escaneo especializada:

| Plataforma | Herramienta |
|---|---|
| WordPress | WPScan |
| Joomla / Drupal | droopescan |
| Cualquier plataforma (CVEs genéricos) | Nuclei con templates específicos |
| Secretos en repositorios Git | truffleHog, gitleaks |
| Aplicaciones generales | nikto, Burp Suite Pro scanner |

Estas herramientas automatizan el reconocimiento y la identificación de vulnerabilidades conocidas — pero el razonamiento detrás de cada hallazgo requiere entender los conceptos trabajados en este bloque y en los anteriores de este temario.

## Cierre del bloque de Attacking Common Applications

Este bloque completa el panorama de aplicaciones concretas donde las vulnerabilidades conceptuales trabajadas a lo largo de todo el temario se manifiestan en la práctica: SQLi, XSS, IDOR, LFI, RCE, credenciales débiles, y configuraciones inseguras — todas en el contexto de plataformas reales ampliamente desplegadas. El siguiente y último bloque, *Bug Bounty Hunting Process*, cierra el temario con el proceso formal de cómo reportar estos hallazgos de forma profesional.
