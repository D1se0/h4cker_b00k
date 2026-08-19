# 🏆 Ejemplos reales (anonimizados)

Esta sección contiene **reportes reales que he enviado**, uno por cada plataforma que uso, para que sirvan de referencia de formato, nivel de detalle y estilo de comunicación con los triagers.

> 🔒 **Aviso de anonimización**
>
> Todos los nombres de empresa, dominios reales, tokens completos, IPs y cualquier dato que pudiera identificar al programa o a un cliente real han sido **sustituidos u ocultados** con un efecto de "rotulador negro" (texto tachado con fondo negro). Estos ejemplos se comparten únicamente como referencia de **metodología y formato de reporte**, no como información explotable contra ningún sistema real.
>
> Los bloques ocultos se ven así: <mark style="background-color:#000000;color:#000000;user-select:none">información redactada</mark>

## 📄 Índice

* [YesWeHack — JWT hardcodeado en app Android](yeswehack-jwt-hardcodeado.md)
  Credenciales hardcodeadas (CWE-798) + bypass de autorización (CWE-639) en el bundle JS de una app Android, con un ejemplo real de cómo defender el impacto tras un "Need More Info".

* [Secur0 — Contraseña por defecto hardcodeada](secur0-password-hardcodeada.md)
  Contraseña hardcodeada en el flujo de alta de empleados de un CRM (CWE-798 / CWE-521), con verificación completa del hash y prueba de login.

* [Intigriti — IDOR en API de favoritos](intigriti-idor-favoritos.md)
  IDOR/BOLA (CWE-639) en una API de "guardados" que permite leer, añadir y borrar contenido de la lista de otro usuario.
