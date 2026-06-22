# Qué son los proxies web y herramientas disponibles

## El problema que resuelven

Las aplicaciones web y móviles modernas dependen constantemente de comunicación con servidores backend: cada acción del usuario suele traducirse en una o varias peticiones HTTP. Auditar esa comunicación únicamente con `curl` o las DevTools del navegador es posible, pero limitado: no es cómodo modificar peticiones sobre la marcha, repetirlas con variaciones, ni automatizar pruebas sistemáticas sobre cientos de parámetros.

Un **proxy web de intercepción** resuelve esto colocándose literalmente en medio de la conversación: el navegador (o cualquier cliente) envía sus peticiones al proxy, el proxy las muestra (y opcionalmente las pausa para que se puedan modificar) antes de reenviarlas al servidor real, y hace lo mismo a la inversa con la respuesta. Es, en esencia, un ataque **Man-in-the-Middle (MitM)** consentido y controlado por el propio pentester contra su propio tráfico.

A diferencia de herramientas de captura de tráfico general como Wireshark (que analiza todo el tráfico de red a nivel de paquetes), un proxy web trabaja específicamente a nivel de aplicación, centrado en los puertos HTTP/HTTPS (80/443), lo que simplifica enormemente trabajar con peticiones web concretas.

## Usos de un proxy web

Aunque la función principal es capturar y modificar peticiones HTTP, un proxy de intercepción moderno integra muchas más capacidades:

- Escaneo de vulnerabilidades
- Fuzzing web
- Rastreo (*crawling*) automatizado del sitio
- Mapeo de la estructura completa de la aplicación
- Análisis detallado de peticiones
- Pruebas de configuración
- Asistencia en revisión de código

## Las dos herramientas de referencia

### Burp Suite

[Burp Suite](https://portswigger.net/burp) es el proxy web más extendido en pentesting profesional. Cuenta con una interfaz muy pulida, incluye un navegador Chromium integrado preconfigurado, y ofrece tanto una versión gratuita (**Community**) como una versión de pago (**Professional/Enterprise**).

Funcionalidades exclusivas de la versión de pago:

- Escáner activo de vulnerabilidades
- Burp Intruder sin límite de velocidad (la versión Community limita a 1 petición/segundo)
- Capacidad de cargar ciertas extensiones avanzadas

Para la mayoría de tareas de aprendizaje y pentesting básico/intermedio, la versión Community es suficiente; al avanzar hacia auditorías más exigentes, las funciones Pro aportan velocidad y automatización significativas.

### OWASP ZAP (Zed Attack Proxy)

[ZAP](https://www.zaproxy.org/) es un proyecto gratuito y de código abierto mantenido por la comunidad bajo el paraguas de OWASP. No tiene funciones de pago — todo lo que ofrece está disponible sin restricciones, lo que lo convierte en una alternativa atractiva cuando no se justifica (o no se dispone de) una licencia de Burp Pro. Su fuzzer, por ejemplo, no tiene límite de velocidad, a diferencia del Intruder gratuito de Burp.

### ¿Cuál elegir?

No es una decisión excluyente: en la práctica, muchos pentesters dominan ambas y eligen según el contexto. Burp suele preferirse por su ecosistema de extensiones (BApp Store) y su interfaz más refinada en flujos de trabajo intensivos; ZAP destaca cuando se necesita automatización sin límites de velocidad sin coste, o en entornos donde licenciar software de pago no es viable. Ambas están disponibles para Windows, macOS y Linux, y suelen venir preinstaladas en distribuciones de pentesting como Kali o Parrot OS.

## Instalación rápida

```bash
# Ambas herramientas requieren un entorno de ejecución Java (JRE)
java -jar burpsuite.jar
java -jar zap.jar
```

También se pueden iniciar con los comandos `burpsuite` o `zaproxy` si están instaladas mediante el gestor de paquetes del sistema, o desde el menú de aplicaciones.

Al iniciar Burp Community, solo se pueden crear **proyectos temporales** (sin opción de guardar progreso entre sesiones) — la persistencia de proyectos es una función de pago. ZAP, en cambio, permite elegir entre proyecto nuevo o temporal independientemente de la licencia.
