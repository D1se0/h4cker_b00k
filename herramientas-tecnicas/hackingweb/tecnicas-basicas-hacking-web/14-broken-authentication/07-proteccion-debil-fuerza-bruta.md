# Protección débil contra fuerza bruta

## Las dos defensas estándar: límite de tasa y CAPTCHA

Tras ver, a lo largo de este bloque, varios escenarios donde la fuerza bruta resulta viable por debilidades en el espacio de búsqueda, conviene examinar las dos contramedidas más extendidas — y por qué, implementadas incorrectamente, pueden ofrecer una falsa sensación de seguridad.

## Límite de tasa (rate limiting)

Restringe cuántas peticiones puede realizar un mismo origen en una ventana de tiempo determinada, frustrando un ataque de fuerza bruta al hacerlo impracticablemente lento o bloqueándolo directamente tras cierto umbral de intentos fallidos.

### El problema de identificar correctamente "al atacante"

La eficacia de un límite de tasa depende por completo de identificar con precisión el origen real de cada petición — algo más complejo de lo que parece cuando existen proxies inversos, balanceadores de carga o cachés intermedias entre el cliente y el servidor de aplicación. En esos escenarios, la dirección IP que el servidor observa directamente pertenece al dispositivo intermedio, no al cliente original — por eso muchas implementaciones recurren a cabeceras HTTP como `X-Forwarded-For`, pensadas para transportar la IP real del cliente a través de esos intermediarios.

### Por qué confiar en esa cabecera sin más es un error de diseño

El problema de fondo es el mismo principio repetido constantemente a lo largo de este temario: **cualquier valor que el cliente pueda establecer libremente no debería tratarse como una fuente fiable de identidad**. La cabecera `X-Forwarded-For` es, por defecto, un valor que el propio cliente puede enviar con cualquier contenido arbitrario — si la lógica de limitación de tasa confía ciegamente en ella sin validación adicional (por ejemplo, sin comprobar que proviene realmente de un proxy de confianza conocido), un atacante puede variar ese valor en cada petición, haciendo que el sistema "vea" un origen distinto cada vez y nunca acumule suficientes intentos fallidos desde la misma fuente aparente como para activar el bloqueo.

Esta clase de fallo no es teórica: vulnerabilidades de este tipo —confiar en cabeceras controlables por el cliente para decisiones de seguridad— han sido documentadas en CVEs públicos reales, reforzando que se trata de un patrón de error genuino y recurrente, no un caso hipotético de laboratorio.

## CAPTCHA

Pensado para forzar interacción humana antes de procesar una petición sensible, dificultando que un script automatizado complete el flujo de ataque sin intervención manual.

### Cuándo un CAPTCHA falla por implementación

- **Filtrar la solución en la propia respuesta**: si, por error de implementación, el valor esperado del CAPTCHA viaja de alguna forma accesible en la respuesta del servidor (en lugar de validarse exclusivamente server-side contra un valor que nunca se expone al cliente), automatizar su resolución se vuelve trivial — el atacante simplemente lee el valor correcto de donde no debería estar expuesto.
- **CAPTCHA reutilizable**: si el mismo desafío puede resolverse una vez y reutilizarse en múltiples peticiones posteriores, pierde por completo su función de filtro por intento.
- **Ausencia de CAPTCHA en endpoints alternativos**: una aplicación puede proteger correctamente el formulario de login visible, pero olvidar aplicar la misma protección a un endpoint de API equivalente que realiza la misma función — el mismo patrón de "protección incompleta a través de las distintas superficies de la aplicación" señalado en el bloque de *File Upload Attacks* respecto a validación de archivos.

### Por qué el CAPTCHA, por sí solo, tampoco es una garantía absoluta

Más allá de errores de implementación, el avance de herramientas de resolución automatizada de CAPTCHA —incluyendo modelos de reconocimiento de imagen y voz cada vez más capaces— reduce progresivamente la fricción que un CAPTCHA impone a un atacante decidido. Esto no significa que el CAPTCHA carezca de valor (sigue elevando el coste y la complejidad del ataque), pero refuerza la misma idea de defensa en profundidad repetida en cada bloque de este temario: ninguna medida aislada debería considerarse suficiente por sí sola.

## La síntesis defensiva

Una protección robusta contra fuerza bruta combina, en lugar de depender de una única medida:

```
Límite de tasa basado en identificación fiable del origen (no en cabeceras controlables por el cliente sin validar)
  + CAPTCHA correctamente implementado (validación exclusivamente server-side, no reutilizable)
  + Bloqueo temporal o incremento progresivo de retraso tras intentos fallidos consecutivos
  + Aplicado de forma consistente en TODOS los endpoints equivalentes (formulario web, API, restablecimiento, 2FA)
```

## Cierre de la sección de fuerza bruta de este bloque

Con esto se completa el recorrido de los apartados de fuerza bruta de este bloque: enumeración de usuarios, fuerza bruta de contraseña, de tokens de restablecimiento, de códigos 2FA, y finalmente las protecciones (y sus fallos de implementación habituales) que deberían frenar todos los anteriores. El resto de este bloque se desplaza hacia un terreno distinto: vulnerabilidades de autenticación que no dependen de adivinar nada por fuerza bruta, sino de fallos lógicos directos en el diseño del mecanismo — credenciales por defecto, restablecimiento de contraseña mal diseñado, y bypass de autenticación.
