# 🏆 Ejemplo real — Secur0

> 🔒 **CONFIDENCIAL — INFORMACIÓN REDACTADA**
> Este es un reporte real que envié, con el nombre del proyecto/repositorio y la ruta interna ocultados con efecto "rotulador negro" donde podían identificar a terceros. Se comparte solo como referencia de **formato y metodología**, no como PoC explotable.

**Plataforma:** Secur0
**Programa:** VDP público de <mark style="background-color:#000;color:#000;user-select:none">[Producto CRM — nombre redactado]</mark>
**Estado final:** Arreglado (`Fixed`)
**CVSS asignado:** 7.6 (Alto)

---

## Título

Contraseña por defecto hardcodeada en el alta de empleados (Hardcoded Default Password in Employee Onboarding)

## Descripción

El flujo estándar y documentado de alta de RRHH (`/rrhh/employee/create` → `POST /rrhh/employee/save`) **no tiene ningún campo de contraseña en su formulario**. Cada empleado creado a través de este flujo completamente normal recibe silenciosamente la contraseña hardcodeada `"changeme"`, sin que la aplicación notifique a quien hace el alta, sin correo de bienvenida, y sin forzar un cambio en el primer login.

```php
// EmployeeSaveController.php
$validated = $request->validate([
    'first_name' => 'required|string|max:255',
    'last_name'  => 'required|string|max:255',
    'email'      => 'required|email|unique:user,email',
    // ... sin ninguna regla para 'password'
]);
$validated['company_id'] = Auth::user()->company_id;
$validated['password'] = bcrypt($request->input('password', 'changeme')); // fallback hardcodeado
User::create($validated);
```

El formulario compartido por las vistas de creación y edición (`_form.blade.php`) confirma **cero coincidencias** para "password" — no hay ningún campo de contraseña en la interfaz. El `User` resultante es exactamente el mismo modelo usado para autenticación en toda la aplicación (`Auth::user()`), así que es una cuenta de login completamente funcional, no un registro inerte de RRHH.

**Confirmado de extremo a extremo**: se envió exactamente los campos que ofrece el formulario real (sin contraseña), se capturó el hash bcrypt generado por el propio servidor en su respuesta de error, se verificó programáticamente que equivale a `"changeme"`, se crackeó de forma independiente y "a ciegas" el mismo hash con John the Ripper + rockyou.txt en menos de 2 minutos, y finalmente se inició sesión en la cuenta resultante a través de la página de login normal.

## Tipo

Use of Hard-coded Credentials (CWE-798) / Weak Password Requirements (CWE-521)

## Prueba de concepto

1. Inicia sesión con cualquier cuenta con permisos de RRHH y abre `/rrhh/employee/create` — observa que no hay ningún campo de contraseña en la página.
2. Rellena y envía solo los campos que ofrece el formulario (nombre, apellidos, email, etc.) y guarda.
3. La contraseña de la cuenta del nuevo empleado es la cadena hardcodeada `"changeme"` — verificable con `password_verify("changeme", <hash almacenado>)` o crackeando el hash con cualquier herramienta estándar (confirmado con John the Ripper + rockyou.txt en menos de 2 minutos).
4. Cierra sesión y entra como el nuevo empleado usando su email y la contraseña `"changeme"` — el login funciona inmediatamente, sin que nadie haya establecido ni comunicado ninguna contraseña.
5. Confirma que la sesión está genuinamente autenticada (ej. una página protegida devuelve 403 "sin permiso" en lugar de 302 "inicia sesión").

Totalmente reproducible vía HTTP puro — comandos `curl` exactos y pasos de verificación/crackeo de hash disponibles en la sección de Payload del reporte original.

## Impacto

- Bypass total de autenticación para cada cuenta de empleado creada por el flujo estándar y nunca reasignada manualmente a una contraseña personalizada — es decir, **todas** las creadas por esta vía, ya que la interfaz no ofrece forma de establecer una.
- **No requiere ningún privilegio** para explotar una cuenta ya existente — solo su email, visible para cualquier compañero con permiso de "lectura RRHH" o adivinable por el patrón de correo corporativo.
- Confirmado como **crackeable por diccionario en menos de 2 minutos** contra una wordlist estándar (rockyou.txt) — no es una contraseña obscura.
- Los registros de empleado incluyen campos sensibles (IBAN, fecha de alta, relaciones de jefatura); el acceso posterior escala con los permisos que se le asignen después (crear-y-luego-asignar es una secuencia habitual en el mundo real).
- Ninguna señal dentro del sistema (cambio forzado, email de bienvenida/reseteo) avisa al empleado legítimo de que debe cambiar la contraseña por defecto — la ventana de exposición queda abierta indefinidamente.

## Información adicional y sugerencia de solución

**Causa raíz**: `EmployeeSaveController::save()` recurre a la cadena literal `"changeme"` cada vez que no hay un campo `password` en la petición — y la única interfaz que llama a este endpoint (el formulario de alta de RRHH) nunca envía uno, porque no tiene ningún campo de contraseña. No es una mala configuración puntual; es el único camino de código que ejecuta el producto tal y como se distribuye.

**Recomendación:**

1. Nunca usar como fallback una contraseña fija y hardcodeada. Alternativas: (a) añadir un campo de contraseña explícito al formulario de alta, o (b) generar una contraseña temporal aleatoria criptográficamente segura por usuario y entregarla fuera de banda (ej. un enlace de reseteo firmado y caducable por email) — nunca una constante compartida.
2. Forzar cambio de contraseña en el primer login para cualquier cuenta aprovisionada con una credencial generada por el sistema.
3. Añadir una comprobación mínima de fortaleza/entropía de contraseña que rechace `"changeme"` y palabras de diccionario similares aunque se introduzcan manualmente en el futuro.

## Alcance

<mark style="background-color:#000;color:#000;user-select:none">https://github.com/[organizacion]/[proyecto-crm]</mark>

## Endpoint

<mark style="background-color:#000;color:#000;user-select:none">https://[entorno-de-pruebas].local/rrhh/employee/save</mark>

---

> 📌 **Por qué este reporte funcionó bien**: no se quedó en "encontré una contraseña hardcodeada en el código". Se demostró el ciclo completo — desde el formulario real sin campo de contraseña, pasando por la extracción del hash generado por el propio servidor, hasta el login efectivo con esa cuenta — cerrando cualquier duda sobre si el hallazgo era solo teórico.
