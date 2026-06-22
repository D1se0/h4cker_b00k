# Divulgación de archivos locales con XXE

## El flujo completo de explotación

### Paso 1: Identificar un formulario que envíe XML

El primer indicio es observar el cuerpo de la petición HTTP (usando las DevTools o un proxy de intercepción). Si los datos se transmiten en XML en lugar de `application/x-www-form-urlencoded` o JSON, hay superficie de ataque potencial.

### Paso 2: Confirmar que las entidades se procesan

Antes de intentar leer archivos, se confirma que el parser XML ejecuta sustituciones de entidades. Se define una entidad interna simple y se comprueba si su valor aparece en la respuesta:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [
  <!ENTITY test "XXE_CONFIRMED">
]>
<email>
  <from>&test;</from>
</email>
```

Si la respuesta refleja `XXE_CONFIRMED` en lugar de `&test;` como texto literal, el parser está procesando entidades — la vulnerabilidad está confirmada.

### Paso 3: Referenciar un archivo del sistema

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<email>
  <from>&xxe;</from>
</email>
```

Si el contenido de `/etc/passwd` aparece en la respuesta donde se esperaría ver el valor de `<from>`, la vulnerabilidad XXE está explotándose con éxito para leer archivos locales del servidor.

## Archivos de alto valor en sistemas Linux

| Archivo | Por qué es relevante |
|---|---|
| `/etc/passwd` | Lista de usuarios del sistema (sin contraseñas, pero útil para reconocimiento) |
| `/etc/hosts` | Mapa de hosts internos — puede revelar otros servidores en la red interna |
| Archivos de configuración de la aplicación (`config.php`, `.env`) | Credenciales de base de datos, claves de API |
| Claves SSH (`/home/usuario/.ssh/id_rsa`) | Si son legibles, permiten acceso directo al servidor |
| `/proc/self/environ` | Variables de entorno del proceso actual — a veces contiene rutas o credenciales |

## Leyendo archivos con caracteres especiales XML

Si el archivo contiene caracteres con significado especial en XML (`<`, `>`, `&`), la entidad externa puede fallar porque el parser los interpreta como sintaxis. Para archivos de código fuente PHP o HTML:

```xml
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">
```

El wrapper `php://filter` con el filtro `base64-encode` hace que el parser reciba una cadena Base64 limpia en lugar del contenido bruto con caracteres especiales — la respuesta contendrá el código fuente del archivo codificado en Base64, decodificable de forma trivial.

> Limitación: esta técnica solo funciona en aplicaciones PHP. Para otros frameworks existen enfoques alternativos, como la exfiltración ciega que se trata en el siguiente apartado.

## Por qué leer código fuente puede ser el hallazgo más valioso

Obtener el código fuente de la aplicación convierte una auditoría de caja negra en una de caja blanca de facto, permitiendo:

- Identificar otras vulnerabilidades en la lógica de la aplicación que serían invisibles desde fuera.
- Extraer credenciales hardcodeadas o claves de API en archivos de configuración.
- Entender exactamente cómo se implementa el control de acceso para buscar bypasses adicionales.

Es la misma idea trabajada en el bloque de *SQL Injection Fundamentals* cuando la lectura de archivos vía `LOAD_FILE()` permitía obtener el código fuente de la propia aplicación vulnerable.

## Atención: también funciona como SSRF

Usando `http://` en lugar de `file://`, XXE puede hacer que el servidor realice peticiones HTTP hacia URLs arbitrarias:

```xml
<!ENTITY xxe SYSTEM "http://servicio-interno/admin">
```

Este comportamiento es funcionalmente equivalente a SSRF (visto en el bloque de *Server-side Attacks*), pero a través del parser XML en lugar de un parámetro de URL. La superficie de ataque interna alcanzable es la misma.
