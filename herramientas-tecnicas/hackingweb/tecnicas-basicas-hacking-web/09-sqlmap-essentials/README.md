# SQLMap Essentials

Tras entender manualmente cómo funciona la inyección SQL (bloque anterior), este bloque presenta **SQLMap**, la herramienta de automatización de referencia en la industria para detectar y explotar vulnerabilidades de inyección SQL. Se cubre su funcionamiento interno, cómo interpretar su salida, cómo construir ataques a partir de peticiones HTTP capturadas, cómo ajustar la detección para casos difíciles, la enumeración sistemática de bases de datos, y las técnicas para sortear protecciones como WAFs — siempre en el contexto de una auditoría autorizada.

## Contenido

1. [SQLMap: visión general y técnicas soportadas](01-vision-general-sqlmap.md)
2. [Primeros pasos: ejecución básica e interpretación de resultados](02-primeros-pasos.md)
3. [Entendiendo la salida de SQLMap](03-salida-sqlmap.md)
4. [Configurando el ataque: peticiones HTTP y autenticación](04-configurando-ataque.md)
5. [Diagnóstico de problemas en SQLMap](05-diagnostico-problemas.md)
6. [Ajustando la detección: nivel, riesgo y comparación de respuestas](06-ajustes-deteccion.md)
7. [Enumeración de bases de datos con SQLMap](07-enumeracion-sqlmap.md)
8. [Sorteando protecciones de aplicaciones web](08-bypass-protecciones.md)
9. [De SQLi a interacción con el sistema operativo](09-interaccion-sistema-operativo.md)

## Por qué este bloque importa

SQLMap automatiza en segundos lo que manualmente, como se vio en el bloque anterior, puede llevar mucho más tiempo — pero usarlo bien requiere entender qué está haciendo realmente por debajo. Sin esa base, SQLMap es una caja negra que falla de forma incomprensible ante cualquier obstáculo (WAF, tokens CSRF, respuestas inestables); con ella, se convierte en una herramienta que se puede diagnosticar, ajustar y dirigir con precisión quirúrgica.
