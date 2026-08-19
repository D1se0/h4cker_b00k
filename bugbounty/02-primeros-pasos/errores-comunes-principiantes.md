---
icon: lightbulb-exclamation-on
---

# Errores comunes de principiante

Una lista honesta de fallos típicos (muchos los he cometido yo también) para que los evites desde el primer día.

## 🚫 Errores de metodología

* **No leer el scope y las reglas del programa antes de empezar.** Te puede llevar a reportar algo out-of-scope (rechazo automático) o, peor, a hacer algo que no estaba permitido.
* **Usar escáneres automáticos "a saco" sin permiso explícito.** Muchos programas prohíben herramientas de escaneo masivo/DoS-like. Si tienes dudas, pregunta o revisa las reglas.
* **Tocar datos de usuarios reales "solo para confirmar".** Nunca. Siempre cuentas y datos propios/inventados. Es la diferencia entre investigación legítima y un problema legal.
* **No reproducir el bug dos veces antes de reportar.** A veces un comportamiento raro es un fallo puntual de red, no una vulnerabilidad real.
* **Reportar sin haber entendido bien el impacto real.** Ver [Mentalidad y metodología](mentalidad-y-metodologia.md#️-impacto--diferencia-de-código-de-estado).

## 🚫 Errores de reporte

* **Título vago**: "Hay un fallo de seguridad" no dice nada. Sé específico: tipo de vulnerabilidad + endpoint + impacto en una línea.
* **Pasos de reproducción incompletos o que asumen conocimiento previo.** Si un triager que no conoce tu setup no puede seguir tus pasos exactamente, vas a recibir un "Need more info" (y con razón).
* **No incluir capturas o vídeo.** El texto solo, sin evidencia visual, genera dudas y ralentiza el triage.
* **Mezclar varias vulnerabilidades distintas en un solo reporte** ("y además encontré esto otro..."). Cada vulnerabilidad, su propio reporte.
* **Sobrevalorar la severidad.** Pedir un CVSS Crítico para algo que realmente es Medio hace que el triager empiece la conversación a la defensiva. Sé honesto y argumenta con la calculadora.
* **Responder tarde o de forma cortante cuando piden más información.** Recuerda que "Need more info" no es un rechazo, es una oportunidad de defender mejor tu hallazgo.

## 🚫 Errores de actitud

* **Frustrarte y "quemar" un programa con reportes de baja calidad** después de un rechazo. Cada reporte flojo afecta a tu reputación en la plataforma.
* **No aceptar un "N/A" razonado.** A veces el equipo tiene contexto que tú no tienes (por ejemplo, ese endpoint es intencionalmente público). Pregunta con educación si no lo entiendes, no discutas por discutir.
* **Compararte constantemente con hunters con años de experiencia.** La curva de aprendizaje es real, todo el mundo empezó sin encontrar nada.
* **No aprovechar los rechazos.** Un "N/A" bien explicado te enseña más sobre cómo funciona el sistema que un reporte aceptado a la primera.
