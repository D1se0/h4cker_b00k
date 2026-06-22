# Filtros de lista negra

## El enfoque: bloquear lo conocido como peligroso

La validación de extensión más común en servidores consiste en comparar la extensión del archivo recibido contra una lista de extensiones explícitamente prohibidas (`.php`, `.asp`, `.jsp`...), rechazando la carga si coincide.

```php
$extension = pathinfo($fileName, PATHINFO_EXTENSION);
$blacklist = array('php', 'php7', 'phps');

if (in_array($extension, $blacklist)) {
    echo "File type not allowed";
    die();
}
```

## Por qué este enfoque comparte la misma debilidad estructural vista en otros bloques

Exactamente el mismo argumento desarrollado en el bloque de *Command Injection* respecto a listas negras de caracteres: una lista negra solo cubre lo que sus autores **anticiparon explícitamente**. En el caso de extensiones de archivo, el problema se agrava porque:

- La mayoría de servidores web (Apache, IIS) pueden configurarse para interpretar como ejecutable **más de una extensión** asociada a un mismo lenguaje — una lista que solo cubre `.php` puede dejar fuera variantes igualmente funcionales que el motor del servidor también ejecuta.
- En sistemas que no distinguen mayúsculas de minúsculas en nombres de archivo (como es habitual en Windows), una comparación de lista negra sensible a mayúsculas puede evitarse trivialmente alterando la capitalización de la extensión.
- Listas negras desactualizadas o incompletas, mantenidas manualmente, tienden a quedarse atrás respecto a la superficie real de extensiones que un servidor concreto podría llegar a ejecutar.

## La conclusión de diseño, no la receta de bypass

El punto relevante para quien diseña o revisa una aplicación no es memorizar qué extensiones concretas "se les suelen olvidar" a los desarrolladores — es entender que **cualquier enfoque basado en enumerar lo prohibido hereda, por construcción, la posibilidad de dejar huecos**. Esta es la razón directa por la que el apartado de prevención de este bloque recomienda invertir el enfoque: en lugar de listar qué se rechaza, definir explícitamente y de forma restrictiva qué se acepta — el tema del siguiente apartado.
