# Tomcat: servidor de aplicaciones Java

Apache Tomcat es el servidor de aplicaciones Java más desplegado en entornos empresariales. Su Application Manager (`/manager/html`) es el vector de ataque más frecuente — si está accesible y protegido con credenciales débiles o por defecto, representa un acceso de alto impacto al servidor.

## Fingerprinting e identificación

```bash
# Inducir un error 404 que puede revelar la versión en el mensaje de error
curl http://objetivo:8080/recurso-inexistente

# Confirmar Tomcat leyendo la documentación expuesta
curl -s http://objetivo:8080/docs/ | grep Tomcat

# El manager y host-manager son las rutas de administración
http://objetivo:8080/manager/html
http://objetivo:8080/host-manager/html
```

La página de error por defecto de Tomcat muestra claramente la versión — el mismo principio de "los errores revelan información" trabajado en el bloque de *Introducción a Aplicaciones Web*.

## Archivos críticos de configuración

Si existe una vulnerabilidad de LFI (como la que podría ocurrir en una aplicación desplegada sobre Tomcat), los archivos más relevantes a intentar leer:

| Archivo | Contenido relevante |
|---|---|
| `WEB-INF/web.xml` | Configuración de la aplicación — puede revelar rutas y parámetros internos |
| `conf/tomcat-users.xml` | Credenciales de los usuarios del Manager — el archivo más crítico |

## Credenciales por defecto del Manager

El Manager de Tomcat usa HTTP Basic Auth. Las credenciales más comunes encontradas en instalaciones sin endurecer:

```
tomcat:tomcat
admin:admin
admin:password
tomcat:s3cret
manager:manager
```

Estas credenciales pueden estar en `conf/tomcat-users.xml`. Si no son las por defecto, puede ser necesario un ataque de fuerza bruta contra el endpoint de Basic Auth — exactamente el mismo vector trabajado en el bloque de *Login Brute Forcing* con Hydra contra HTTP Basic Auth.

## El impacto de acceso al Manager

Con acceso al Application Manager de Tomcat, es posible desplegar, iniciar, parar y eliminar aplicaciones web en el servidor. Este nivel de acceso es equivalente a ejecución de código en el servidor — la misma conclusión de alto impacto que en cualquier otro mecanismo de "deploy de código" con acceso privilegiado en el contexto de una auditoría.

En una PoC responsable, documentar el acceso con capturas de pantalla del Manager es suficiente para demostrar el impacto — sin necesidad de escalar hacia el despliegue de aplicaciones adicionales.

## Vulnerabilidades conocidas del core de Tomcat

Al igual que con los CMS, Tomcat tiene su propio historial de CVEs graves — incluyendo path traversal en el Manager, vulnerabilidades de deserialización, y problemas de AJP (el conector Apache JServ Protocol, que en configuraciones desactualizadas puede exponer el servidor a ataques sin autenticación). El [CVE-2020-1938 "Ghostcat"](https://nvd.nist.gov/vuln/detail/CVE-2020-1938) es un ejemplo notable: permitía leer archivos del servidor vía el conector AJP por defecto habilitado.

## Mitigación

- Deshabilitar el Manager y Host-Manager si no son necesarios; si lo son, restringir su acceso por IP.
- Cambiar las credenciales por defecto del Manager en la primera instalación.
- Deshabilitar el conector AJP si no se usa (muchos despliegues modernos no lo necesitan).
- Mantener Tomcat actualizado — especialmente crítico para vulnerabilidades de deserialización y path traversal.
- Configurar mensajes de error personalizados que no revelen la versión de Tomcat.
