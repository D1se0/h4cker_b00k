# WHOIS

## Qué es

WHOIS es un protocolo de consulta-respuesta que permite acceder a bases de datos públicas con información sobre recursos registrados de internet: principalmente nombres de dominio, pero también bloques de direcciones IP y sistemas autónomos. Funciona, en esencia, como una guía telefónica pública de quién es responsable de cada recurso en línea.

```bash
whois ejemplo.com
```

Un registro WHOIS típico incluye:

- **Domain Name**: el dominio consultado.
- **Registrar**: la empresa donde se registró (GoDaddy, Namecheap, etc.).
- **Registrant/Administrative/Technical Contact**: personas u organizaciones responsables del dominio a distintos niveles.
- **Creation/Expiration Date**: fechas de registro y caducidad.
- **Name Servers**: servidores que resuelven el dominio a una IP.

## Por qué importa en reconocimiento web

Los datos WHOIS aportan valor en varios frentes:

- **Identificar personal clave**: nombres, correos y teléfonos de quienes administran el dominio — información reutilizable en campañas de ingeniería social o phishing dirigido.
- **Descubrir infraestructura de red**: los servidores de nombres y direcciones IP asociadas dan pistas sobre el proveedor de hosting y la arquitectura general.
- **Análisis histórico**: servicios que mantienen históricos WHOIS permiten rastrear cambios de propiedad o de infraestructura a lo largo del tiempo, revelando la evolución de la presencia digital del objetivo.

## Casos de uso prácticos

### Investigación de phishing

Ante un correo sospechoso que enlaza a un dominio desconocido, una consulta WHOIS rápida puede revelar señales de alarma: fecha de registro muy reciente (días, no años), información del registrante oculta tras un servicio de privacidad, o servidores de nombres asociados a proveedores de hosting conocidos por alojar actividad maliciosa. La combinación de estos factores es un fuerte indicador de campaña de phishing.

### Análisis de malware / infraestructura C2

Al analizar un dominio asociado a un servidor de mando y control (C2), el registro WHOIS puede mostrar patrones característicos: registrante usando un proveedor de correo gratuito y anónimo, ubicación geográfica de alto riesgo, o un registrador con historial laxo frente al abuso — pistas que ayudan a perfilar la infraestructura del atacante y a notificar al proveedor de hosting correspondiente.

### Inteligencia de amenazas

Analizar el WHOIS de múltiples dominios usados por un mismo grupo de amenaza a lo largo del tiempo puede revelar patrones: registros agrupados poco antes de campañas de ataque, alias reutilizados, servidores de nombres compartidos entre dominios — todo ello alimenta un perfil de tácticas, técnicas y procedimientos (TTPs) del actor, útil para construir indicadores de compromiso (IOCs).

## Uso práctico

```bash
sudo apt install whois -y

whois facebook.com
```

```
Domain Name: FACEBOOK.COM
Registrar: RegistrarSafe, LLC
Creation Date: 1997-03-29
Registry Expiry Date: 2033-03-30
Registrant Organization: Meta Platforms, Inc.
Name Server: A.NS.FACEBOOK.COM
Name Server: B.NS.FACEBOOK.COM
```

Una antigüedad de registro considerable, servidores de nombres propios del dominio, y todos los estados de protección activados (`clientTransferProhibited`, etc.) son señales típicas de un dominio legítimo y bien establecido — el contraste con un dominio de phishing recién creado, sin estos atributos, suele ser evidente.

## Limitaciones y evolución reciente

Desde la entrada en vigor del **RGPD/GDPR** en 2018, gran parte de la información personal de los registrantes (especialmente en dominios de particulares o pequeñas empresas europeas) aparece oculta tras servicios de privacidad, reduciendo la utilidad de WHOIS para identificar personal concreto. Por ello, WHOIS rara vez es suficiente por sí solo para identificar empleados individuales o vulnerabilidades específicas — su verdadero valor aparece al **combinarlo** con otras técnicas de reconocimiento (DNS, motores de búsqueda, redes sociales) para construir una imagen completa de la huella digital del objetivo.

> **Evolución del protocolo**: el sucesor moderno de WHOIS es **RDAP** (*Registration Data Access Protocol*), que ofrece un acceso más estructurado (JSON en lugar de texto libre) y con mejor soporte para políticas de privacidad por diseño.
