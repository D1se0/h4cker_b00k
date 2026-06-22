# Ataques de diccionario

## Por qué funcionan: la predictibilidad humana

Un ataque de diccionario explota un hecho consistente sobre el comportamiento humano: la mayoría de personas prioriza contraseñas fáciles de recordar sobre contraseñas verdaderamente aleatorias, lo que las hace gravitar hacia palabras comunes, nombres, fechas y patrones predecibles. En lugar de probar todas las combinaciones posibles de caracteres (fuerza bruta pura), un ataque de diccionario prueba únicamente una lista precompilada de candidatos con alta probabilidad de coincidir.

## Por qué la calidad de la wordlist es el factor decisivo

Una lista genérica de contraseñas comunes (`rockyou.txt`, listas de SecLists) funciona razonablemente bien contra cuentas personales sin política de contraseñas estricta. Pero una lista **adaptada al objetivo concreto** —incorporando el nombre de la organización, jerga del sector, nombres de empleados identificados en reconocimiento previo— multiplica significativamente la probabilidad de éxito frente a una lista genérica, exactamente el mismo principio de "cuanto más específico el reconocimiento previo, mejor el resultado" que ha aparecido repetidamente en este temario.

## Fuerza bruta vs. diccionario: comparativa

| Aspecto | Diccionario | Fuerza bruta pura |
|---|---|---|
| Eficiencia | Mucho más rápido, espacio de búsqueda reducido | Puede ser extremadamente lento |
| Capacidad de orientación | Altamente adaptable al objetivo concreto | Sin capacidad de orientación inherente |
| Efectividad | Excelente contra contraseñas débiles/comunes | Funciona contra cualquier contraseña, dado tiempo suficiente |
| Limitación | Inútil contra contraseñas verdaderamente aleatorias | Inviable en la práctica para contraseñas largas y complejas |

## Filtrando una wordlist según una política de contraseñas conocida

Si se conoce la política de contraseñas de la organización objetivo (longitud mínima, requisitos de complejidad), tiene sentido **filtrar previamente** la wordlist para descartar candidatos que ni siquiera cumplirían esos requisitos — reduciendo drásticamente el tiempo de ataque sin perder cobertura real.

```bash
# Solo contraseñas de 8+ caracteres
grep -E '^.{8,}$' wordlist.txt > paso1.txt

# Que además contengan al menos una mayúscula
grep -E '[A-Z]' paso1.txt > paso2.txt

# Que además contengan al menos una minúscula
grep -E '[a-z]' paso2.txt > paso3.txt

# Que además contengan al menos un dígito
grep -E '[0-9]' paso3.txt > candidatos_finales.txt
```

Encadenando estos filtros con `grep` y expresiones regulares, una lista de 10.000 candidatos puede reducirse a un puñado de docenas que realmente cumplen la política — un ataque mucho más rápido y dirigido que probar la lista completa sin filtrar.

## Credential stuffing: cuando el "diccionario" son credenciales reales filtradas

Una variante especialmente efectiva del ataque de diccionario usa, en lugar de una lista genérica de contraseñas comunes, **credenciales reales filtradas** en brechas de seguridad previas de otros servicios. La lógica: dado que muchas personas reutilizan contraseñas entre cuentas, una combinación usuario/contraseña filtrada de un servicio A tiene una probabilidad razonable de funcionar también en un servicio B no relacionado.

Este vector es la razón de fondo detrás de una de las recomendaciones más repetidas de seguridad personal: **nunca reutilizar contraseñas entre servicios**. Desde la perspectiva de una organización, también es la razón por la que monitorizar bases de datos públicas de credenciales filtradas (servicios como Have I Been Pwned) es una práctica de seguridad proactiva recomendable: permite detectar si las credenciales de empleados ya circulan públicamente, antes de que alguien las use en un ataque de credential stuffing.

## Conectando con el siguiente apartado

Cuando un ataque de diccionario puro no encuentra coincidencia, pero hay indicios de que la contraseña real es una **variación** de algo predecible (por ejemplo, una organización con política de cambio periódico de contraseña, donde los usuarios tienden a incrementar un número o añadir un símbolo), la estrategia más eficiente no es pasar a fuerza bruta pura, sino a un **ataque híbrido** — el tema del siguiente apartado.
