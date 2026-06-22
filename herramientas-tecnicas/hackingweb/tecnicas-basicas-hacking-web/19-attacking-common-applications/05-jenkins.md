# Jenkins: CI/CD

Jenkins es la plataforma de CI/CD (Integración Continua / Entrega Continua) más extendida en entornos empresariales. Por diseño, tiene acceso directo a repositorios de código, credenciales de despliegue, y en muchos casos al propio servidor de producción — lo que lo convierte en uno de los objetivos de mayor impacto en una red corporativa.

## Fingerprinting e identificación

```bash
# Acceso directo a la interfaz (puerto 8080 por defecto)
http://objetivo:8080/

# Señales características: cabecera X-Jenkins en respuestas HTTP
curl -I http://objetivo:8080/

# Ruta de configuración de seguridad — confirma Jenkins
http://objetivo:8080/configureSecurity/

# Nmap revela el servicio
nmap -sV -p 8080 objetivo
```

## Credenciales por defecto y acceso sin autenticación

En versiones antiguas de Jenkins, la instalación por defecto no requería autenticación — cualquier usuario anónimo podía acceder y ejecutar jobs. Versiones más recientes requieren configuración de seguridad durante la instalación, pero muchas instalaciones heredadas siguen sin ella.

Las credenciales por defecto más habituales:
```
admin:admin
admin:password
jenkins:jenkins
```

## El vector de mayor impacto: Script Console

El elemento de mayor riesgo de Jenkins es la **Script Console** (`/script`), disponible para administradores, que permite ejecutar código **Groovy** directamente en el servidor — con acceso completo al sistema de ficheros y al entorno de ejecución de Jenkins:

```
http://objetivo:8080/script
```

Un usuario con acceso al panel de administración tiene, a través de esta consola, capacidad de ejecución de código arbitrario en el servidor. Esto hace que el acceso al panel de administración de Jenkins sea equivalente, en términos de impacto, a la ejecución remota de código directa.

La PoC mínima responsable en una auditoría: ejecutar `println("hostname".execute().text)` o similar — suficiente para demostrar ejecución de código sin escalar a herramientas de post-explotación.

## Exposición de credenciales almacenadas

Jenkins almacena credenciales de sistemas externos (repositorios de código, servidores de despliegue, bases de datos) en su almacén de credenciales. Con acceso de administrador, estas credenciales pueden extraerse — representando un riesgo de compromiso en cascada hacia todos los sistemas integrados con Jenkins.

## CVEs históricos relevantes

Jenkins tiene un historial de vulnerabilidades graves en el core y en plugins populares — deserialización de Java (RCE sin autenticación), path traversal, SSRF, y XSS son categorías recurrentes. La [base de datos de seguridad de Jenkins](https://www.jenkins.io/security/advisories/) publica avisos regularmente.

## Mitigación

- Habilitar autenticación y autorización desde la instalación inicial — nunca dejar Jenkins accesible sin autenticación en ningún entorno.
- Restringir acceso al panel de administración por IP cuando sea posible.
- Deshabilitar la Script Console para usuarios no estrictamente necesarios.
- Mantener Jenkins y todos los plugins actualizados.
- Usar el principio de mínimo privilegio en las credenciales que Jenkins almacena.
- Segmentar la red para que Jenkins no tenga acceso innecesario a sistemas de producción.
