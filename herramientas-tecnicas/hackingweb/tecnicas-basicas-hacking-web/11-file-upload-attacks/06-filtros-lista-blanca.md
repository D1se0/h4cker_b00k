# Filtros de lista blanca

## Invirtiendo el enfoque: definir explícitamente qué se acepta

A diferencia de una lista negra, una lista blanca rechaza por defecto **todo**, salvo el conjunto explícito y reducido de extensiones que la aplicación realmente necesita aceptar (por ejemplo, únicamente `.jpg`, `.png`, `.pdf`):

```php
$extension = pathinfo($fileName, PATHINFO_EXTENSION);
$whitelist = array('jpg', 'jpeg', 'png', 'gif', 'pdf');

if (!in_array($extension, $whitelist)) {
    echo "File type not allowed";
    die();
}
```

## Por qué esta inversión ya es estructuralmente mejor

Una lista blanca no necesita anticipar cada variante peligrosa posible — solo necesita acertar con el conjunto, normalmente pequeño y bien conocido, de formatos que la funcionalidad concreta realmente requiere. Esto elimina el problema central de las listas negras: no hay "huecos" que un atacante pueda descubrir entre extensiones no contempladas, porque cualquier cosa fuera del conjunto explícito se rechaza por defecto.

## Por qué, aun así, no es una garantía completa por sí sola

Una lista blanca de **extensiones** resuelve el problema de "¿qué nombre tiene el archivo?", pero no resuelve por sí sola dos cuestiones relacionadas:

- **El nombre del archivo no garantiza su contenido real.** Nada impide, a nivel de nombre de archivo, que un archivo con extensión `.jpg` contenga en realidad un script ejecutable — el nombre es simplemente una etiqueta que el sistema operativo y las aplicaciones suelen (pero no están obligadas a) respetar.
- **La configuración del servidor puede ejecutar más de lo que el nombre sugiere.** Si el servidor web está configurado para interpretar como código cualquier archivo dentro de un directorio concreto, independientemente de su extensión declarada, una lista blanca de extensiones por sí sola no impide ese comportamiento.

Por esto, una lista blanca de extensión bien implementada se combina, en aplicaciones robustas, con una verificación adicional del **contenido real** del archivo — el tema que se desarrolla en el siguiente apartado — y con una configuración del servidor que impida la ejecución de código en el directorio donde se almacenan los archivos subidos, tratada en detalle en el apartado de prevención que cierra este bloque.

## La lección de diseño

Listas blancas frente a listas negras es, en esencia, el mismo debate de fondo que distingue **validación** de **sanitización**, visto ya en el bloque de XSS: definir explícitamente el formato esperado y rechazar cualquier desviación es sistemáticamente más robusto que intentar enumerar y bloquear cada variante de lo no deseado. Pero, como se ve aquí, incluso una lista blanca bien construida necesita combinarse con capas adicionales para constituir una defensa completa.
