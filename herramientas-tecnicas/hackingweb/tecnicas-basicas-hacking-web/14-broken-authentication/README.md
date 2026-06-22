# Broken Authentication

Mientras que el bloque anterior se centró en atacar la robustez de las credenciales mediante fuerza bruta, este bloque amplía el alcance a fallos **estructurales** en la propia lógica de autenticación de una aplicación: enumeración de usuarios, debilidades en tokens de restablecimiento de contraseña, fuerza bruta de 2FA, credenciales por defecto olvidadas, bypass de autenticación mediante acceso directo o manipulación de parámetros, y ataques contra los tokens de sesión que mantienen a un usuario autenticado.

## Contenido

1. [Qué es la autenticación](01-que-es-autenticacion.md)
2. [Clasificación de ataques a la autenticación](02-ataques-autenticacion.md)
3. [Enumeración de usuarios](03-enumeracion-usuarios.md)
4. [Fuerza bruta de contraseñas en profundidad](04-fuerza-bruta-contrasenas.md)
5. [Fuerza bruta de tokens de restablecimiento de contraseña](05-fuerza-bruta-tokens-reset.md)
6. [Fuerza bruta de códigos 2FA](06-fuerza-bruta-2fa.md)
7. [Protección débil contra fuerza bruta](07-proteccion-debil-fuerza-bruta.md)
8. [Credenciales por defecto](08-credenciales-por-defecto.md)
9. [Restablecimiento de contraseña vulnerable](09-restablecimiento-vulnerable.md)
10. [Bypass de autenticación por acceso directo](10-bypass-acceso-directo.md)
11. [Bypass de autenticación por modificación de parámetros](11-bypass-modificacion-parametros.md)
12. [Ataques a tokens de sesión](12-ataques-tokens-sesion.md)
13. [Ataques de sesión adicionales](13-ataques-sesion-adicionales.md)

## Por qué este bloque importa

La autenticación es la primera línea de defensa de cualquier aplicación — y, precisamente por eso, uno de los componentes donde un fallo de diseño tiene el impacto más directo: un bypass exitoso no requiere ninguna otra vulnerabilidad adicional para otorgar acceso completo a una cuenta, o a toda la aplicación.
