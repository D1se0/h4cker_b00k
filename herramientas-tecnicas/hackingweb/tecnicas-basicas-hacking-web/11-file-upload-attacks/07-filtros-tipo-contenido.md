# Filtros de tipo de contenido

## Más allá del nombre del archivo: verificar qué contiene realmente

Como se anticipó en el apartado anterior, validar únicamente la extensión declarada de un archivo deja una brecha: el nombre no garantiza el contenido. Las aplicaciones más cuidadosas añaden una segunda capa que examina, de una forma u otra, **qué es realmente** el archivo recibido, más allá de cómo se haya llamado.

Existen dos enfoques habituales, con fiabilidad muy distinta entre sí.

## Cabecera `Content-Type`: la verificación más débil

Cuando un navegador construye una petición de carga de archivo, incluye una cabecera `Content-Type` que normalmente deriva de la extensión seleccionada. Algunas aplicaciones backend confían en esa cabecera para decidir si el archivo es del tipo esperado:

```php
$type = $_FILES['uploadFile']['type'];

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
```

El problema de fondo: esa cabecera la genera el **cliente**, no el servidor — es, en esencia, una validación de frontend disfrazada de cabecera HTTP. Confiar en un valor que el propio emisor de la petición controla por completo no aporta ninguna garantía real sobre el contenido efectivo del archivo, exactamente el mismo principio de "nunca confiar en lo que llega del cliente sin verificación independiente" trabajado a lo largo de todo este temario.

## Verificación de tipo MIME por contenido: la opción más robusta

Un enfoque considerablemente más fiable consiste en que el servidor inspeccione directamente los **primeros bytes del archivo recibido**, comparándolos contra las firmas estándar conocidas para cada formato (la llamada "firma de archivo" o *bytes mágicos*) — por ejemplo, una imagen GIF auténtica siempre comienza con una secuencia de bytes reconocible específica de ese formato, independientemente de cómo se haya nombrado el archivo.

Esta verificación ya no depende de nada que el cliente declare voluntariamente (ni nombre de archivo, ni cabecera HTTP) — examina el contenido binario real, que es mucho más difícil de falsificar de forma completa sin comprometer también la validez del propio archivo como imagen funcional.

## Por qué incluso esto no es, por sí solo, una garantía absoluta

Verificar la firma inicial de un archivo confirma que **comienza** con la estructura esperada de ese formato — no garantiza que el resto del archivo esté libre de contenido adicional. Algunos formatos (como ciertos contenedores de imagen) permiten incrustar datos adicionales más allá de la estructura mínima requerida sin que eso invalide el archivo como imagen válida desde la perspectiva de un visor estándar. Esto es relevante porque conecta con técnicas de carga de archivos "polimórficos" (un archivo válido como imagen y, simultáneamente, válido como otro tipo de contenido en un contexto distinto) — un terreno avanzado de explotación que queda fuera del alcance conceptual de este bloque, pero que ilustra por qué ninguna validación aislada debería considerarse, por sí sola, suficiente.

## La capa que realmente cierra el problema

Verificar el contenido real reduce drásticamente la superficie de ataque frente a confiar en metadatos declarados por el cliente, pero la defensa estructuralmente completa —desarrollada con detalle en el apartado de prevención que cierra este bloque— combina esta verificación con medidas adicionales a nivel de **dónde y cómo se almacena y sirve** el archivo subido: independientemente de qué tan robusta sea la validación de entrada, si el servidor está configurado para no ejecutar nunca código en el directorio de archivos subidos, el impacto de cualquier validación que falle queda contenido.
