# Prevención de IDOR

## El principio rector: control de acceso en el servidor, no en el cliente

IDOR no es un problema de "identificadores predecibles" — es un problema de **ausencia de control de acceso server-side**. Un identificador perfectamente visible y predecible, protegido por una verificación robusta en el backend, no crea IDOR. Un identificador opaco y aleatorio, sin ninguna verificación de permisos en el servidor, sí. La prevención actúa sobre ambas capas, pero el control de acceso es la fundamental.

## Capa 1: Control de acceso basado en roles (RBAC)

La aplicación debe verificar en **cada petición** que el usuario autenticado tiene permiso para acceder o modificar el objeto específico solicitado. La sesión del usuario (no ningún valor que venga en la propia petición) debe ser la única fuente de verdad sobre su identidad y rol.

```javascript
// Ejemplo conceptual de regla de acceso server-side
match /api/profile/{userId} {
    allow read, write: if user.isAuthenticated == true
        && (user.uid == userId      // el usuario accede a su propio perfil
            || user.role == 'admin'); // o es administrador
}
```

La comprobación compara el `userId` solicitado con el `uid` derivado del **token de sesión**, no con un `uid` que pudiera viajar en el cuerpo de la petición bajo control del cliente.

## Lo que NO es suficiente como control de acceso

- **Ocultar botones en el frontend** para roles sin permiso — la petición de API puede hacerse directamente sin pasar por la interfaz visual.
- **Confiar en parámetros del cliente** (`role=employee` en una cookie, `is_admin=true` en el cuerpo JSON) — cualquier valor que el cliente pueda modificar es un vector de manipulación.
- **Proteger el endpoint principal** pero olvidar endpoints alternativos equivalentes (p.ej., proteger la ruta HTML pero no la API JSON subyacente que sirve los mismos datos).

## Capa 2: Referencias de objetos robustas

Una vez que el control de acceso existe, usar identificadores no predecibles añade una capa adicional de defensa en profundidad — dificulta la enumeración aunque el control de acceso falle puntualmente.

### UUID v4 (la opción recomendada)

```
89c9b29b-d19f-4515-b2dd-abb6e693eb20
```

Un UUID v4 generado aleatoriamente tiene 122 bits de entropía — computacionalmente inviable de enumerar por fuerza bruta incluso con millones de intentos por segundo.

### Cómo mapearlo correctamente

```php
// Al crear un objeto, generar UUID y mapear a ID interno:
$uuid = generateUUID();
$db->query("INSERT INTO documents (uuid, user_id, ...) VALUES ('$uuid', $userId, ...)");

// Al recibir una petición con UUID:
$uuid = $_GET['id'];
$doc = $db->query("SELECT * FROM documents WHERE uuid='$uuid' AND user_id=$authenticatedUserId");
// La cláusula AND user_id verifica el control de acceso
```

La clave: el UUID es la referencia externa expuesta al cliente, pero el servidor siempre verifica además que ese UUID pertenece al usuario autenticado — ninguna de las dos capas es suficiente sola.

### Lo que no hay que hacer

- **Calcular hashes en el frontend** — si el algoritmo se expone en el JavaScript, cualquiera puede reproducirlo para otros valores.
- **Usar únicamente el UUID sin control de acceso** — un UUID dificulta la enumeración, pero si el servidor no verifica propiedad, alguien que obtenga un UUID por cualquier otro medio (IDOR de lectura, filtración en logs, etc.) puede seguir accediendo a ese objeto sin permiso.

## Checklist de prevención de IDOR

- [ ] ¿Cada endpoint verifica que el usuario autenticado tiene permiso sobre el objeto solicitado, no solo que tiene una sesión válida?
- [ ] ¿El rol y privilegios del usuario se derivan del token de sesión del servidor, no de valores enviados por el cliente en la petición?
- [ ] ¿Todos los verbos HTTP (GET, POST, PUT, DELETE) sobre cada endpoint tienen la misma verificación de control de acceso?
- [ ] ¿Las APIs internas y los endpoints "no enlazados desde la interfaz" tienen el mismo nivel de protección que los endpoints principales?
- [ ] ¿Los identificadores de objetos expuestos son no predecibles (UUID, hash con salt)?
- [ ] ¿Los hashes/identificadores se generan y mapean en el servidor, nunca en el cliente?
