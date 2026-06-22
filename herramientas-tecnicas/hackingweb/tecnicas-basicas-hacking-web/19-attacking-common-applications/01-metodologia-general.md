# Preparación y metodología general

## Por qué las aplicaciones comunes son objetivos prioritarios

Las aplicaciones empresariales ampliamente desplegadas (WordPress, Tomcat, Jenkins, Nagios, etc.) comparten una característica que las convierte en objetivos especialmente relevantes en auditorías externas: **sus vulnerabilidades son públicas, bien documentadas, y frecuentemente explotadas**. Un CVE en WordPress afecta a millones de instalaciones simultáneamente; un Tomcat con credenciales por defecto es un hallazgo casi garantizado en entornos corporativos que no siguen un proceso de endurecimiento sistemático.

## El proceso de reconocimiento de aplicaciones

Antes de auditar cualquier aplicación concreta, el primer paso es identificar qué hay en el entorno objetivo. El mismo proceso de *Information Gathering* trabajado en el bloque correspondiente se aplica aquí con un foco específico en descubrir qué aplicaciones conocidas están en uso.

### Escaneo inicial y toma de capturas

Herramientas como **EyeWitness** y **aquatone** automatizan la toma de capturas de pantalla de todas las interfaces web encontradas durante un escaneo de red, permitiendo identificar visualmente qué aplicaciones están desplegadas antes de interactuar con ninguna individualmente:

```bash
# Primero, exportar nmap a XML
nmap -sV -oX scan.xml 10.10.10.0/24

# EyeWitness toma capturas de todas las interfaces HTTP/HTTPS encontradas
eyewitness -x scan.xml --web

# aquatone, alternativa popular
cat urls.txt | aquatone
```

El resultado es una galería visual que permite identificar de un vistazo interfaces de login de WordPress, Tomcat, Jenkins, paneles de administración, y otras aplicaciones conocidas — reduciendo significativamente el tiempo de reconocimiento manual.

### Señales de fingerprinting por aplicación

| Aplicación | Señales características |
|---|---|
| WordPress | `/wp-admin/`, `/wp-content/`, cabecera `X-Pingback`, `generator` en el HTML |
| Joomla | `/administrator/`, `Joomla` en cabeceras o HTML |
| Drupal | `/node/`, `X-Generator: Drupal` |
| Tomcat | Página de error con logo de Apache Tomcat, `/manager/html` |
| Jenkins | `/jenkins/`, interfaz característica, cabecera `X-Jenkins` |
| GitLab | `/users/sign_in`, interfaz GitLab |

## Estructura del proceso de auditoría por aplicación

Para cada aplicación identificada, el proceso sigue siempre el mismo esquema:

1. **Identificar la versión exacta** — las vulnerabilidades son frecuentemente específicas de versión.
2. **Buscar CVEs conocidos** para esa versión — exactamente la misma técnica de fingerprinting + búsqueda de CVEs trabajada en el bloque de *Introducción a Aplicaciones Web*.
3. **Comprobar credenciales por defecto** — antes de cualquier otro ataque, el paso de menor coste y mayor rendimiento potencial.
4. **Enumerar componentes adicionales** (plugins, temas, módulos) — a menudo más vulnerables que la aplicación base.
5. **Auditar la configuración** — configuraciones inseguras que la propia documentación del producto desaconseja.

## Documentación durante la auditoría

La estructura recomendada para mantener notas organizadas durante una auditoría de aplicaciones comunes:

```
Pentesting - Cliente X
├── Scope (IPs, rangos, URLs autorizadas, fechas)
├── Contactos del cliente
├── Credenciales de prueba
├── Reconocimiento
│   ├── Escaneos nmap
│   └── Hosts activos
├── Descubrimiento de aplicaciones
│   └── Hosts interesantes por aplicación
└── Explotación
    └── Por host: hallazgo, PoC, remediación recomendada
```

Una documentación ordenada desde el inicio de la auditoría evita perder el rastro de hallazgos y facilita enormemente la redacción del informe final — tema que se desarrolla en el bloque de *Bug Bounty Hunting Process*.
