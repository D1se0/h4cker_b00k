# Credenciales por defecto

## El vector más simple, y a menudo el más efectivo

Muchas aplicaciones y dispositivos se configuran de fábrica con un usuario y contraseña predefinidos, pensados exclusivamente para el primer acceso tras la instalación. El problema, una vez más, no es técnico sino de proceso: si nadie las cambia tras la puesta en marcha, quedan exactamente igual de accesibles para un atacante que para el administrador legítimo. Por esta razón, la [Guía de Pruebas de Seguridad de OWASP](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials) incluye explícitamente la comprobación de credenciales por defecto como un paso estándar de cualquier auditoría de autenticación.

Este apartado retoma y amplía lo ya introducido en el bloque de *Login Brute Forcing*, centrándose ahora específicamente en **aplicaciones web** identificadas mediante fingerprinting (técnica desarrollada en el bloque de *Information Gathering*).

## Cómo se identifican credenciales por defecto durante una auditoría

1. **Identificar con precisión la aplicación y, si es posible, su versión** — mediante las técnicas de fingerprinting vistas en bloques anteriores (cabeceras HTTP, rutas características, comportamiento distintivo de la interfaz).
2. **Consultar bases de datos dedicadas a credenciales por defecto**, mantenidas precisamente para sistematizar este tipo de comprobación frente a un catálogo amplio de productos y dispositivos conocidos.
3. **Si no hay una entrada catalogada**, una búsqueda dirigida con el nombre exacto del producto suele ser suficiente: la documentación oficial de instalación de muchas aplicaciones de código abierto publica explícitamente las credenciales iniciales que el propio software asigna tras la instalación, precisamente para que el administrador sepa cómo acceder por primera vez y cambiarlas.

## Por qué este paso siempre debería intentarse primero

Comprobar credenciales por defecto conocidas tiene un coste casi nulo (una o dos peticiones) frente al beneficio potencial (acceso administrativo inmediato sin necesidad de ninguna otra vulnerabilidad). Por eso, en cualquier metodología de auditoría bien estructurada, esta comprobación precede sistemáticamente a cualquier intento de fuerza bruta más costoso — exactamente el mismo principio de "agotar primero lo de bajo coste y alta probabilidad" trabajado repetidamente a lo largo de este temario, desde el reconocimiento pasivo en *Information Gathering* hasta la comprobación de privilegios antes de intentar lectura de archivos en *SQL Injection Fundamentals*.

## Mitigación

- **Forzar el cambio de credenciales en el primer acceso**: la medida más robusta — la aplicación no debería permitir continuar usando el sistema con las credenciales de fábrica más allá de la configuración inicial.
- **Generar credenciales únicas por instalación**, en lugar de un valor fijo idéntico para todas las instalaciones del mismo software — eliminando por completo la posibilidad de que una lista pública de credenciales conocidas sea útil contra una instalación concreta.
- **Auditoría periódica de cuentas existentes**, comprobando de forma proactiva (y no solo en el momento de la instalación) que ninguna cuenta administrativa siga usando un valor por defecto documentado públicamente.

## Conectando con el resto del bloque

Las credenciales por defecto comparten con la enumeración de usuarios (apartado anterior) una misma característica: ambas son vulnerabilidades de **proceso**, no de criptografía ni de lógica compleja — fallan porque alguien olvidó un paso de configuración, no porque el mecanismo de autenticación en sí esté mal diseñado. El siguiente apartado examina un caso distinto: cuando el **diseño mismo** del mecanismo de restablecimiento de contraseña contiene un fallo lógico explotable, independientemente de si las credenciales actuales son fuertes o no.
