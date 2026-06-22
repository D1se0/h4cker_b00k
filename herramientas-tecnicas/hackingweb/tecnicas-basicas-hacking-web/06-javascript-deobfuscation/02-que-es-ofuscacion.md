# Qué es la ofuscación de código

## Definición

La ofuscación es el proceso de reescribir un programa de forma que su **comportamiento técnico se mantenga intacto**, pero su lectura por parte de un humano se vuelva extremadamente difícil. No es lo mismo que cifrado: el código ofuscado sigue siendo código ejecutable directamente, sin necesidad de ninguna clave para "revertirlo" antes de ejecutarse — solo resulta difícil de **entender**, no de **ejecutar**.

Una herramienta de ofuscación típica convierte el código en una especie de diccionario interno (palabras y símbolos numerados), reconstruyendo el programa original "sobre la marcha" durante la ejecución, consultando ese diccionario en cada paso.

## Por qué JavaScript es el terreno preferido de la ofuscación

Lenguajes como Python o PHP suelen ejecutarse **en el servidor**: el código fuente nunca llega al usuario final, solo el resultado de su ejecución. JavaScript, en cambio, se ejecuta predominantemente **en el cliente**: el código se envía completo, en texto plano, y es el propio navegador del usuario quien lo interpreta. Esto significa que **cualquiera puede leer el JavaScript de cualquier página** simplemente mirando el código fuente — razón de peso por la que la ofuscación es tan habitual específicamente en este lenguaje.

## Casos de uso de la ofuscación

### Legítimos

- **Proteger propiedad intelectual**: dificultar que terceros copien o reutilicen la lógica original sin permiso.
- **Dificultar la ingeniería inversa** de mecanismos de validación o lógica de negocio sensible del lado del cliente.

> **Advertencia importante**: implementar autenticación o cifrado **del lado del cliente** nunca es una buena práctica de seguridad, por mucho que el código esté ofuscado — el cliente siempre es un entorno no confiable, y la ofuscación solo añade fricción, no seguridad real. Cualquier control que importe debe vivir en el servidor.

### Maliciosos

El uso más extendido de la ofuscación, con diferencia, es **evadir la detección**: atacantes y autores de malware ofuscan deliberadamente sus scripts para dificultar que sistemas de detección y prevención de intrusiones (IDS/IPS), antivirus, o analistas humanos identifiquen rápidamente su comportamiento real.

## Cómo se ofusca el código en la práctica

La ofuscación raras veces se hace a mano: existen numerosas herramientas automatizadas para cada lenguaje, desde servicios web gratuitos hasta ofuscadores propios desarrollados por organizaciones de ciberdelincuencia precisamente para dificultar todavía más el trabajo de quienes intentan analizar su código.

## Por qué esto importa para un analista/pentester

Saber identificar y revertir ofuscación es una habilidad transversal que aparece en varios contextos profesionales:

- **Análisis de malware**: gran parte del malware basado en web (droppers, *phishing kits*, *skimmers* de tarjetas de crédito) usa JavaScript ofuscado para ocultar su payload real.
- **Auditoría de aplicaciones web**: funcionalidad no documentada, lógica de validación, o endpoints internos a menudo se "esconden" ofuscando el JavaScript que los referencia, en lugar de protegerlos correctamente en el backend.
- **Ejercicios de equipo rojo/azul**: entender rápidamente qué hace un script sospechoso es esencial tanto para construir un ataque (rojo) como para responder a un incidente (azul).

Los siguientes apartados de este bloque recorren, de menor a mayor complejidad, las técnicas de ofuscación más comunes — minificación, *packing*, y técnicas avanzadas — antes de pasar a las herramientas y el proceso de desofuscación.
