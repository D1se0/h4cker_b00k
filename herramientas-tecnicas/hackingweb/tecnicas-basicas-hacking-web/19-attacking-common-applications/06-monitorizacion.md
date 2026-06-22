# Herramientas de monitorización (Nagios, Zabbix, Splunk)

Las herramientas de monitorización de infraestructura tienen acceso privilegiado a información de todos los sistemas que supervisan — métricas, logs, estado de servicios, credenciales de conexión a agentes remotos. Comprometer una herramienta de monitorización puede revelar la arquitectura completa de la red interna y las credenciales de acceso a múltiples sistemas.

## Nagios

Nagios es uno de los sistemas de monitorización más antiguos y extendidos en entornos Linux. Se despliega típicamente en el puerto 80/443 con un prefijo `/nagios/`.

**Fingerprinting:**
```bash
http://objetivo/nagios/
curl -s http://objetivo/nagios/ | grep -i "nagios"
```

**Vectores frecuentes:**
- Credenciales por defecto: `nagiosadmin:nagiosadmin` o `admin:admin`
- Versiones antiguas sin parchear con vulnerabilidades de RCE documentadas (Nagios XI especialmente tiene un historial de CVEs graves)
- Exposición de configuración que revela IPs y credenciales de sistemas monitorizados

## Zabbix

Zabbix es una alternativa popular a Nagios, con una interfaz web más moderna. Puerto por defecto: 80/443.

**Fingerprinting:**
```bash
http://objetivo/zabbix/
curl -s http://objetivo/ | grep -i "zabbix"
```

**Vectores frecuentes:**
- Credenciales por defecto: `Admin:zabbix` (con A mayúscula)
- Con acceso de administrador, Zabbix permite ejecutar scripts en los agentes monitorizados — equivalente a ejecución remota de comandos en todos los sistemas monitorizados
- Vulnerabilidades de SQLi e RCE en versiones antiguas

## Splunk

Splunk es la plataforma de SIEM (Security Information and Event Management) más extendida. Gestiona logs de seguridad de toda la infraestructura, lo que hace que comprometer Splunk equivalga a tener visibilidad completa de toda la actividad de la red — incluyendo alertas de seguridad, logs de autenticación, y a menudo credenciales en texto plano en los propios logs ingestados.

**Fingerprinting:**
```bash
# Puertos típicos de Splunk
nmap -sV -p 8000,8089 objetivo
# 8000: interfaz web
# 8089: API REST de Splunk

http://objetivo:8000/
```

**Vectores frecuentes:**
- En versiones antiguas de Splunk (antes de 6.x), la instalación no requería contraseña — acceso anónimo total
- Credenciales por defecto: `admin:changeme`
- Con acceso de administrador, Splunk permite ejecutar "búsquedas" que pueden incluir comandos del sistema (`|script`, `|runshellscript`) — similar a la Script Console de Jenkins
- Acceso a todos los logs ingestados, que pueden contener credenciales, tokens, y datos sensibles de toda la infraestructura

## El patrón común a las tres herramientas

Nagios, Zabbix, y Splunk comparten el mismo perfil de riesgo:

1. **Acceso privilegiado a la infraestructura por diseño** — necesitan ver todos los sistemas para monitorizar, lo que convierte su compromiso en un vector de escalada masiva.
2. **Credenciales por defecto frecuentes** — herramientas que se instalan como "infraestructura de soporte" suelen recibir menos atención de seguridad que las aplicaciones de negocio.
3. **Capacidad de ejecución de código en sistemas remotos** — la funcionalidad de "ejecutar scripts en agentes" es la misma que cualquier vector de RCE, con la diferencia de que los agentes son los sistemas monitorizados.

## Mitigación

- Cambiar credenciales por defecto inmediatamente tras la instalación.
- Restringir acceso por IP — estas herramientas no deberían ser accesibles desde internet.
- Mantener versiones actualizadas — especialmente Nagios XI y Splunk tienen historiales de CVEs graves.
- Aplicar el principio de mínimo privilegio en las credenciales que estas herramientas usan para conectarse a los agentes.
- Auditar qué datos sensibles se ingestan en Splunk — credenciales en logs son un vector de filtración frecuente.
