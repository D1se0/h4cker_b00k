# JavaScript Deobfuscation

JavaScript se ejecuta en el cliente, lo que significa que su código fuente es, por definición, accesible para cualquiera dispuesto a mirar. Para dificultar la lectura humana (sin afectar su funcionamiento), muchos desarrolladores —y bastantes más atacantes— recurren a la ofuscación. Este bloque enseña a localizar código JavaScript dentro de una página, entender cómo y por qué se ofusca, desofuscarlo con herramientas automatizadas, y analizar manualmente el resultado para entender su funcionalidad real, incluyendo la decodificación de las capas de codificación de texto (Base64, hex, ROT13) que suelen acompañar al código ofuscado.

## Contenido

1. [Localizando JavaScript en una página](01-localizando-javascript.md)
2. [Qué es la ofuscación de código](02-que-es-ofuscacion.md)
3. [Técnicas de ofuscación: minificación y packing](03-minificacion-packing.md)
4. [Ofuscación avanzada](04-ofuscacion-avanzada.md)
5. [Desofuscación: beautify y unpacking](05-desofuscacion.md)
6. [Análisis manual del código desofuscado](06-analisis-manual.md)
7. [Replicando peticiones HTTP descubiertas](07-replicando-peticiones-http.md)
8. [Decodificación: Base64, Hex y ROT13](08-decodificacion.md)

## Por qué este bloque importa

Esta habilidad aparece constantemente en pentesting real: malware que oculta su payload mediante JavaScript ofuscado, aplicaciones web que esconden funcionalidad no publicada en scripts minificados, o lógica de validación del lado del cliente que conviene entender antes de intentar evitarla. Saber desofuscar y leer JavaScript con soltura es una habilidad transversal que conecta directamente con análisis de malware, ingeniería inversa, y auditoría de aplicaciones web modernas.
