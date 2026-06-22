# Identificación de IDOR

## Dónde buscar referencias directas a objetos

El primer paso en cualquier auditoría de IDOR es identificar dónde la aplicación expone identificadores de objetos que podrían estar relacionados con datos específicos de un usuario. Los lugares más habituales:

### Parámetros de URL

```
GET /download.php?file_id=123
GET /profile.php?uid=5
GET /invoice?order_id=8821
```

Son el caso más obvio: el identificador es directamente visible en la barra de direcciones. Cualquier valor numérico o alfanumérico que parezca referirse a un objeto concreto de la base de datos merece comprobación.

### Cuerpo de peticiones POST/PUT/PATCH

```
POST /api/update_profile
{"uid": 183, "email": "nuevo@ejemplo.com"}
```

Menos visible que los parámetros de URL (no aparece en la barra de direcciones), pero igualmente manipulable con un proxy de intercepción — exactamente la misma técnica vista en el bloque de *Web Proxies*.

### Llamadas AJAX en el código JavaScript del frontend

El código JavaScript de la aplicación puede revelar llamadas a endpoints con referencias directas que la interfaz no hace visibles por diseño:

```javascript
function changeUserPassword() {
    $.ajax({
        url: "change_password.php",
        type: "post",
        data: {
            uid: user.uid,
            password: user.password,
            is_admin: is_admin
        }
    });
}
```

Si esta función existe en el JavaScript pero la interfaz nunca la invoca para usuarios sin privilegios, un auditor puede llamarla directamente (via consola del navegador, Repeater de Burp) con los parámetros de otro usuario — exactamente el mismo principio de "el frontend no protege nada por sí mismo" repetido desde el bloque de *Introducción a Aplicaciones Web*.

### Cookies y cabeceras HTTP

Aunque menos frecuente, algunos identificadores de objeto viajan en cookies o en cabeceras personalizadas — motivo por el que la revisión de cabeceras completas (no solo URL y cuerpo) debería ser parte de cualquier sesión de análisis con proxy de intercepción.

## Reconociendo el tipo de referencia

### Referencia numérica simple

El caso más directo: incrementar o decrementar el valor y comprobar si se devuelven datos de otro usuario.

```
?file_id=123 → ¿Y ?file_id=124?
?uid=5       → ¿Y ?uid=4?
```

### Referencia codificada (Base64, hex)

Un valor que parece random pero que reconocemos como codificación estándar. Decodificar, modificar, volver a codificar:

```bash
echo "ZmlsZV8xMjMucGRm" | base64 -d
# -> file_123.pdf

echo -n "file_124.pdf" | base64
# -> ZmlsZV8xMjQucGRm
# Probar: ?filename=ZmlsZV8xMjQucGRm
```

### Referencia hasheada (MD5, SHA1...)

Si la referencia es un hash, pero el código JavaScript revela con qué se calculó, puede ser reproducible:

```javascript
data: {filename: CryptoJS.MD5('file_1.pdf').toString()}
// -> c81e728d9d4c2f636f067f89cc14862c

// Para file_2.pdf:
// CryptoJS.MD5('file_2.pdf').toString() -> calculable en la consola del navegador
```

## Técnica de comparación entre roles

Una técnica más sistemática cuando se dispone de dos cuentas de distinto privilegio (o dos cuentas de usuario estándar):

1. Con la **cuenta A**, realizar una acción (p.ej., consultar el perfil) y registrar la petición completa.
2. Con la **cuenta B** (sesión distinta, diferente cookie), reproducir exactamente la misma petición — idealmente con los identificadores de la cuenta A.
3. Si el servidor devuelve los datos de A a B sin error, hay IDOR confirmado.

Esta técnica también es válida para detectar escalada de privilegios: si una función solo debería estar disponible para administradores, enviar la petición correspondiente desde una sesión de usuario estándar (con los mismos parámetros que usaría un admin) y verificar si el servidor la procesa igualmente, sin verificar el rol del usuario autenticado.

## La distinción entre "referencia expuesta" y "IDOR real"

Como se insistió en el apartado anterior: exponer un ID no es por sí solo una vulnerabilidad. La confirmación de IDOR requiere que **efectivamente se devuelvan datos de otro usuario** (o se ejecute una acción en nombre de otro) sin que el servidor haya verificado si el usuario autenticado tiene permiso. Una petición que devuelve `403 Forbidden` al intentar acceder a un recurso de otro usuario **no es IDOR**, aunque el ID sea completamente predecible — indica que el control de acceso está funcionando.
