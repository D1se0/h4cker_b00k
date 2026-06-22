# Prevención de vulnerabilidades en la carga de archivos

## Por qué este apartado es el más importante de todo el bloque

Cada técnica vista hasta ahora —ausencia de validación, listas negras incompletas, confianza en metadatos declarados por el cliente, vectores secundarios como el nombre del archivo— comparte una misma raíz: la aplicación confía en algo que el usuario controla, sin verificarlo de forma independiente y robusta. Este apartado recopila las medidas que, combinadas, cierran cada uno de esos huecos.

## Capa 1: validación de extensión combinando lista blanca y lista negra

Aunque la lista blanca es, como se vio anteriormente, el enfoque estructuralmente más sólido, la recomendación práctica es **combinar ambas**: una lista blanca que defina explícitamente qué extensiones se aceptan, reforzada por una lista negra adicional que actúe como red de seguridad si, por cualquier descuido, la lista blanca llegara a aceptar algo no previsto (por ejemplo, un nombre de archivo con extensiones encadenadas).

```php
$fileName = basename($_FILES["uploadFile"]["name"]);

// Comprobación de lista negra: ¿aparece una extensión peligrosa en cualquier parte del nombre?
if (preg_match('/^.*\.ph(p|ps|ar|tml)/', $fileName)) {
    echo "Only images are allowed";
    die();
}

// Comprobación de lista blanca: ¿el nombre TERMINA con una extensión permitida?
if (!preg_match('/^.*\.(jpg|jpeg|png|gif)$/', $fileName)) {
    echo "Only images are allowed";
    die();
}
```

Nótese la diferencia conceptual entre ambas comprobaciones: la lista negra busca la extensión peligrosa **en cualquier posición** del nombre (cubriendo casos como `shell.php.jpg`), mientras que la lista blanca exige que el nombre **termine exactamente** con una de las extensiones permitidas — ninguna de las dos por sí sola cubre todos los casos, pero combinadas se refuerzan mutuamente.

Esta validación debe aplicarse **siempre en el servidor**; la validación de frontend puede mantenerse como complemento de experiencia de usuario (evita que usuarios legítimos suban accidentalmente un archivo incorrecto), pero nunca como sustituto de la comprobación real.

## Capa 2: validar también el contenido, no solo el nombre

Validar la extensión sin validar el contenido —o viceversa— deja exactamente los huecos descritos en los apartados anteriores de este bloque. Ambas comprobaciones deben aplicarse siempre juntas, y además deben **coincidir entre sí**:

```php
$fileName = basename($_FILES["uploadFile"]["name"]);
$contentType = $_FILES['uploadFile']['type'];
$MIMEtype = mime_content_type($_FILES['uploadFile']['tmp_name']);

// Lista blanca de extensión
if (!preg_match('/^.*\.png$/', $fileName)) {
    echo "Only PNG images are allowed";
    die();
}

// Verificación de contenido: tanto la cabecera declarada como el tipo MIME real deben coincidir
foreach (array($contentType, $MIMEtype) as $type) {
    if (!in_array($type, array('image/png'))) {
        echo "Only PNG images are allowed";
        die();
    }
}
```

La función `mime_content_type()` (o su equivalente en otros lenguajes) examina el contenido real del archivo —no lo que el cliente declaró— para determinar su tipo MIME efectivo, cerrando la brecha entre "lo que el nombre dice ser" y "lo que el archivo realmente es" señalada en apartados anteriores.

## Capa 3: nunca exponer directamente el directorio de subidas

Una de las medidas de mayor impacto: **no permitir acceso HTTP directo** al directorio donde se almacenan los archivos subidos. En su lugar, servir los archivos exclusivamente a través de un script intermediario controlado por la aplicación.

```
Petición directa a /uploads/archivo.ext  →  403 Forbidden
Petición a /download.php?id=123          →  el script valida y sirve el archivo
```

Este script intermediario debe implementar, como mínimo:

- **Comprobación de autorización**: verificar que el usuario autenticado tiene realmente derecho a acceder a ese archivo concreto — sin esta comprobación, se introduce una vulnerabilidad de **IDOR** (referencia directa a objetos insegura), tratada en detalle en el bloque de *Web Attacks*.
- **Validación estricta de rutas**: nunca construir la ruta del archivo a partir de entrada de usuario sin sanitizar, para evitar habilitar una vulnerabilidad de **inclusión de archivos locales (LFI)**, desarrollada en su propio bloque de este temario — limitando el acceso exclusivamente a una lista cerrada de directorios permitidos.
- **Cabeceras de seguridad apropiadas** al servir el archivo:

| Cabecera | Función |
|---|---|
| `Content-Disposition: attachment` | Fuerza la descarga del archivo en lugar de renderizarlo directamente en el navegador |
| `Content-Type` | Declara explícitamente el tipo MIME correcto, evitando ambigüedades |
| `X-Content-Type-Options: nosniff` | Impide que el navegador intente "adivinar" un tipo de contenido distinto al declarado — la misma cabecera vista en el bloque de *Web Requests* como mitigación general frente a XSS |

## Capa 4: anonimizar nombres de archivo

Renombrar cada archivo subido a un identificador aleatorio (en lugar de conservar el nombre original que proporcionó el usuario) y guardar la correspondencia entre nombre original y nombre almacenado en una base de datos aporta dos beneficios simultáneos:

1. **Elimina por completo el vector de inyección a través del nombre de archivo**, visto en el apartado anterior — si el nombre nunca se usa tal cual en ningún comando, consulta o página, no hay superficie de ataque que explotar a través de él.
2. **Dificulta la localización directa** de archivos subidos por terceros, reforzando la capa de control de acceso del script de descarga.

## Capa 5: aislamiento del almacenamiento

Almacenar los archivos subidos en un servidor, contenedor, o sistema de almacenamiento (como un bucket de almacenamiento en la nube) **independiente** del servidor de aplicación principal limita drásticamente el impacto de cualquier fallo: si, pese a todas las capas anteriores, se lograra ejecutar código a través de un archivo subido, ese compromiso quedaría contenido en un entorno separado, sin acceso directo al resto de la infraestructura de la aplicación.

Configuraciones a nivel de servidor web, como restringir explícitamente desde qué directorios puede leer una aplicación PHP (mediante directivas como `open_basedir`), refuerzan esta misma idea de contención incluso dentro de un único servidor.

## Capas adicionales de profundidad

| Medida | Por qué ayuda |
|---|---|
| Deshabilitar funciones de ejecución de comandos no usadas | Si la aplicación nunca necesita invocar `exec`, `system` o equivalentes, deshabilitarlas a nivel de configuración del lenguaje elimina por completo ese vector, incluso si una vulnerabilidad de carga permitiera depositar código que intentara usarlas |
| Desactivar la visualización de errores detallados | Errores de sistema o de servidor expuestos directamente al usuario pueden filtrar rutas internas, nombres de archivo, o fragmentos de código — la misma idea de minimizar la "exposición de datos sensibles" trabajada en el bloque de *Introducción a Aplicaciones Web* |
| Limitar el tamaño máximo de archivo | Mitiga ataques de denegación de servicio basados en archivos desproporcionadamente grandes |
| Mantener actualizadas las librerías de procesamiento | Cierra vulnerabilidades conocidas en componentes de terceros, como se discutió en el apartado anterior |
| Análisis antimalware de archivos subidos | Una capa adicional de detección, especialmente relevante si los archivos subidos se comparten posteriormente con otros usuarios |
| WAF como capa secundaria | Refuerzo adicional, nunca sustituto de las medidas anteriores — el mismo matiz repetido en cada bloque de este temario |

## La síntesis final: defensa en profundidad, una vez más

```
Lista blanca + lista negra de extensión (servidor, nunca solo frontend)
  + Verificación de contenido real (no solo metadatos declarados)
  + Almacenamiento fuera del alcance HTTP directo
  + Servido exclusivamente vía script controlado con autorización e IDOR/LFI prevenidos
  + Nombres de archivo anonimizados
  + Almacenamiento aislado del servidor de aplicación principal
  + Funciones de ejecución deshabilitadas, errores no expuestos, tamaño limitado
```

Esta combinación de capas —idéntica en filosofía a la defensa en profundidad vista al cerrar cada bloque anterior de este temario (XSS, SQL Injection, Command Injection)— es lo que convierte una funcionalidad de carga de archivos, intrínsecamente arriesgada por naturaleza, en una funcionalidad razonablemente segura: ninguna capa aislada es perfecta, pero su combinación reduce drásticamente tanto la probabilidad de que una carga maliciosa tenga éxito como el impacto si, pese a todo, alguna lo consigue.

Al evaluar una aplicación durante una auditoría, esta misma lista de capas funciona como checklist directo: cada medida ausente es un hallazgo concreto y accionable que comunicar al equipo de desarrollo, con una justificación técnica clara de por qué importa y qué riesgo mitiga específicamente.
