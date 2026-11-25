---
icon: sensor-triangle-exclamation
---

# Introducción a la evasión de defensas

> Aviso importante

El contenido de este tema esta creado `exclusivamente` con fines `educativos`.

El uso de varias de estas `tecnicas` y herramientas contra un objetivo sin un consentimiento previo es `ilegal`.

No me hago responsable de ningun mal uso de las `tecnicas` y/o herramientas presentadas en este tema.

Utiliza todas estas `tecnicas` con responsabilidad y dentro de un ejercicio de `hacking etico` donde se haya establecido un `contrato previamente`.

> Static signature analysis

Se fundamento en el concepto de `lista negra`.

Cuando un `nuevo malware` es identificado, los analistas crean una `firma` para detectarlo.

Las firmas suelen basarse en los primeros `bytes` del binario para identificarlo.

El problema de este enfoque es que no puede `detectar` nuevo `malware` o `modificaciones sobre malware` existente.

> Static heuristic analysis

Se fundamenta en el concepto de `lista negra`.

Se crean reglas que `verifican` patrones que normalmente se encuentran en `malware`.

Estos patrones `involucran` artefactos como `llamadas al sistema`, `procesos`, `escrituras en memoria`...

Permiten identificar `malware` nuevo o modificado.

> Dynamic analysis

Cuando se escanea un `malware`, se ejecuta en un `entorno virtual` durante un periodo de tiempo.

Se combina con las `tecnicas` anteriores y permite detectar `malware` nuevo, `modificado` o que se encuentra `cifrado`.

Consume mucho mas tiempo y recursos que las `tecnicas` anteriores y no suele realizarse a no ser que se indique `explicitamente`.

> Tipos de herramientas de seguridad

* `Red`
  * Balanceadores de carga
  * WAF (Web Application Firewall)
  * Network Firewall
  * IDS/IPS
  * NDR (Network Detection and Response)
  * Sistemas de deteccion de anomalias
  * ...
* Endpoint
  * Antivirus
  * EDR (Endpoint Detection and Response)
  * DLP (Data Loss Prevention)
  * HIDS
  * Local Firewall
  * ...
