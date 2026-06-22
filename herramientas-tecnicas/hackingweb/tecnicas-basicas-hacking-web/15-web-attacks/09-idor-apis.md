# IDOR en APIs

## Por qué las APIs son un terreno especialmente fértil para IDOR

Las APIs REST exponen endpoints que realizan operaciones CRUD sobre objetos con identificadores explícitos en la propia ruta o el cuerpo de la petición. Esto hace que los parámetros de identificación sean mucho más visibles y directamente manipulables que en una aplicación web tradicional donde los identificadores a veces quedan ocultos en formularios HTML.

## El patrón típico: API con identificadores expuestos

Una API de gestión de empleados puede tener endpoints como:

```
GET  /profile/api.php/profile/1      → leer perfil del empleado 1
PUT  /profile/api.php/profile/1      → actualizar perfil del empleado 1
POST /profile/api.php/profile/       → crear nuevo empleado
DELETE /profile/api.php/profile/1   → eliminar empleado 1
```

Al capturar la petición de actualización de perfil con un proxy de intercepción, el cuerpo JSON puede revelar campos que la interfaz visual nunca muestra:

```json
{
    "uid": 1,
    "uuid": "40f5888b67c748df7efba008e7c2f9d2",
    "role": "employee",
    "full_name": "Amy Lindon",
    "email": "a_lindon@employees.htb",
    "about": "..."
}
```

La presencia de campos como `role` en el cuerpo de la petición cliente es una señal de alarma inmediata: si el servidor confía en ese valor para determinar el privilegio del usuario, en lugar de derivarlo del estado de sesión autenticado en el backend, es potencialmente manipulable.

## La metodología de prueba sistemática en APIs

Para cada endpoint descubierto, conviene probar:

**1. Cambiar el identificador propio por el de otro usuario**

```
GET /profile/api.php/profile/2   (siendo yo el usuario 1)
```

Si devuelve los datos del empleado 2 → IDOR de lectura confirmado.

**2. Intentar modificar datos de otro usuario**

```
PUT /profile/api.php/profile/2
{"uid": 2, "email": "atacante@mail.com"}
```

Si el servidor actualiza el perfil del empleado 2 → IDOR de escritura confirmado.

**3. Intentar invocar funciones reservadas a privilegios superiores**

```
POST /profile/api.php/profile/
{"role": "admin", "full_name": "Nuevo Admin"}
```

Si crea el usuario con rol admin → IDOR de escalada de privilegios.

**4. Intentar modificar el rol en la petición de actualización**

```json
{"uid": 1, "role": "admin", "full_name": "..."}
```

Si el servidor acepta el cambio de rol → el control de acceso está delegado al cliente.

## Por qué fallar en algunos intentos no significa que no haya IDOR

Una API puede tener control de acceso para algunas operaciones pero no para otras. El ejemplo del apartado anterior ilustra esto: la API comparaba `uid` del cuerpo con el endpoint y rechazaba el intento de modificar datos de otro usuario (comprobación correcta), pero la operación de **lectura** (`GET`) podía carecer de esa misma comprobación — devolviendo libremente los datos de cualquier empleado, incluyendo los campos `uuid` que después se necesitarían para intentar otras operaciones.

Esta asimetría — control de acceso en escritura pero no en lectura, o viceversa — es exactamente el tipo de inconsistencia que solo se detecta probando sistemáticamente **todos los verbos** sobre **todos los endpoints**, no asumiendo que porque una operación esté protegida, las demás también lo están.

## Conectando con el encadenamiento

En el escenario descrito, leer los datos de otro usuario vía GET (IDOR de información) puede revelar su `uuid` — un valor que se necesitaría para, en un segundo paso, modificar sus datos (IDOR de función). Esto es exactamente el "encadenamiento de vulnerabilidades IDOR" que se trata en el siguiente apartado.
