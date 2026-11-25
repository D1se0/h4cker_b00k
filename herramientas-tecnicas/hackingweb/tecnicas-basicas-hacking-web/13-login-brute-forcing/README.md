# Login Brute Forcing

Cuando ninguna vulnerabilidad de inyección está disponible, atacar directamente el mecanismo de autenticación —probando sistemáticamente credenciales hasta encontrar una combinación válida— sigue siendo una de las técnicas más efectivas en pentesting. Este bloque cubre los fundamentos de la seguridad de contraseñas, los distintos tipos de ataque de fuerza bruta, y el uso práctico de las dos herramientas de referencia para automatizar este proceso: **Hydra** y **Medusa**, tanto contra autenticación HTTP básica como contra formularios de login y otros servicios de red.

## Contenido

1. [Fundamentos de la seguridad de contraseñas](01-fundamentos-contrasenas.md)
2. [Tipos de ataques de fuerza bruta](02-tipos-fuerza-bruta.md)
3. [Ataques de diccionario](03-ataques-diccionario.md)
4. [Ataques híbridos](04-ataques-hibridos.md)
5. [Hydra: fundamentos y sintaxis](05-hydra-fundamentos.md)
6. [Hydra contra autenticación HTTP básica](06-hydra-http-basica.md)
7. [Hydra contra formularios de login](07-hydra-formularios.md)
8. [Medusa: fundamentos](08-medusa-fundamentos.md)
9. [Medusa contra servicios web](09-medusa-servicios-web.md)
10. [Construyendo listas de palabras personalizadas](10-listas-personalizadas.md)

## Por qué este bloque importa

Por muy bien protegida que esté una aplicación frente a inyecciones, su mecanismo de autenticación sigue siendo, en la práctica, uno de los puntos más atacados — y uno de los más descuidados, ya que mitigar fuerza bruta requiere medidas activas (límites de intentos, bloqueo de cuentas, CAPTCHA) que muchas aplicaciones no implementan correctamente o de forma incompleta.
