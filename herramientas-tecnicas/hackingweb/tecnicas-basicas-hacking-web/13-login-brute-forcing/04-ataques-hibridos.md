# Ataques híbridos

## El origen del problema: políticas de cambio periódico de contraseña

Muchas organizaciones exigen cambiar la contraseña cada cierto tiempo, una medida pensada para mejorar la seguridad. En la práctica, sin usuarios bien formados, suele producir el efecto contrario: en lugar de generar una contraseña completamente nueva, las personas tienden a modificar mínimamente la anterior — añadir un número al final, incrementar un año, o anteponer un símbolo.

```
Verano2023  →  Verano2023!  →  Verano2024  →  Verano2024!
```

Este patrón predecible es exactamente lo que un **ataque híbrido** está diseñado para explotar.

## Cómo funciona un ataque híbrido

Combina la eficiencia de un ataque de diccionario con la capacidad de variación de la fuerza bruta: en lugar de probar la wordlist tal cual, cada palabra se transforma sistemáticamente añadiendo sufijos, prefijos, o sustituyendo caracteres según reglas predefinidas.

```
Palabra base: Verano2023
Variantes generadas automáticamente:
  Verano2023!
  Verano2023?
  Verano2024
  Verano2024!
  Verano2025
  ...
```

Este enfoque reduce drásticamente el espacio de búsqueda frente a una fuerza bruta pura sobre todos los caracteres posibles, mientras cubre exactamente el tipo de variación que un usuario real produciría al "actualizar" una contraseña existente para cumplir una política de cambio periódico.

## Por qué este enfoque es tan efectivo en la práctica

La fortaleza del ataque híbrido está en su adaptabilidad: no se limita al escenario de cambio periódico de contraseña — puede diseñarse para explotar **cualquier patrón observado o sospechado** dentro de una organización concreta. Si el reconocimiento previo (bloque de *Information Gathering*) revela, por ejemplo, que la organización usa el nombre de un proyecto interno o una convención de nomenclatura particular, esa información puede incorporarse directamente como base de las variantes a probar.

## Generando variantes con herramientas dedicadas

Herramientas como `hashcat` (con sus reglas de mutación) o scripts personalizados permiten aplicar transformaciones sistemáticas sobre una wordlist base: añadir años recientes, sustituir letras por números visualmente similares (`a`→`4`, `e`→`3`, `o`→`0` — el conocido *leetspeak*), o combinar palabras de una lista con sufijos numéricos comunes. El principio es siempre el mismo: partir de algo plausible (una palabra real) y aplicar las transformaciones más probables que un usuario real haría al adaptarla.

## La perspectiva defensiva

Entender por qué los ataques híbridos son tan efectivos es, en sí mismo, el argumento más sólido contra las políticas de cambio periódico de contraseña mal diseñadas — una de las razones por las que las directrices más recientes del NIST (mencionadas en el apartado de fundamentos de este bloque) se han alejado de exigir cambios periódicos obligatorios sin justificación concreta, priorizando en su lugar contraseñas largas y únicas desde el principio, combinadas con autenticación multifactor como capa adicional — tema que se retoma con más profundidad en el bloque de *Broken Authentication*.

## Cierre conceptual de los tipos de ataque

Con diccionario e híbridos cubiertos, junto a los tipos vistos en el apartado anterior (spraying, credential stuffing, fuerza bruta pura), se completa el panorama conceptual de qué estrategia elegir según el contexto. El resto de este bloque pasa a la parte práctica: cómo automatizar cualquiera de estos enfoques contra servicios reales usando **Hydra** y **Medusa**, las dos herramientas de referencia para este propósito.
