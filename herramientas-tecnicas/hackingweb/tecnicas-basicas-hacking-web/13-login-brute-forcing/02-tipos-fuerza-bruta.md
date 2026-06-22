# Tipos de ataques de fuerza bruta

## La matemática del espacio de búsqueda

El número de combinaciones posibles para una contraseña sigue una fórmula sencilla:

```
Combinaciones posibles = (Tamaño del conjunto de caracteres) ^ (Longitud de la contraseña)
```

| Escenario | Longitud | Conjunto de caracteres | Combinaciones |
|---|---|---|---|
| Corta y simple | 6 | minúsculas (a-z) | 26⁶ ≈ 309 millones |
| Más larga, simple | 8 | minúsculas (a-z) | 26⁸ ≈ 209 mil millones |
| Con complejidad | 8 | mayúsculas + minúsculas | 52⁸ ≈ 53,5 billones |
| Complejidad máxima | 12 | mayúsculas + minúsculas + números + símbolos | 94¹² ≈ 4,76 × 10²³ |

Un pequeño aumento en longitud o variedad de caracteres dispara exponencialmente el espacio de búsqueda — la razón fundamental por la que las recomendaciones de seguridad priorizan la longitud sobre la complejidad pura.

### El factor de la potencia de cómputo

| Hardware | Velocidad | Tiempo estimado (contraseña 8 caracteres, letras+dígitos) |
|---|---|---|
| Equipo básico | ~1 millón/segundo | ~6,9 años |
| Clúster de alto rendimiento | ~1 billón/segundo | Reducido drásticamente, pero contraseñas de 12+ caracteres siguen siendo inviables (~15.000 años incluso a esa velocidad) |

## Ejemplo práctico: fuerza bruta sobre un PIN numérico corto

Cuando el espacio de búsqueda es pequeño (por ejemplo, un PIN de 4 dígitos, con solo 10.000 combinaciones posibles), la fuerza bruta pura es completamente viable incluso con recursos modestos. Un script sencillo en Python que itera todas las combinaciones es suficiente:

```python
import requests

ip = "10.10.10.5"
port = 5000

for pin in range(10000):
    formatted_pin = f"{pin:04d}"  # 7 -> "0007"
    response = requests.get(f"http://{ip}:{port}/pin?pin={formatted_pin}")

    if response.ok and 'flag' in response.json():
        print(f"PIN correcto: {formatted_pin}")
        print(f"Flag: {response.json()['flag']}")
        break
```

Este caso ilustra perfectamente por qué la **longitud importa más que cualquier otra cosa**: un PIN de 4 dígitos numérico tiene solo 10.000 combinaciones — trivial de agotar en segundos. Extenderlo a 6 dígitos ya multiplica el espacio por 100; añadir letras lo dispara mucho más.

## Tipos de ataque, comparados

| Método | Cómo genera candidatos | Cuándo usarlo |
|---|---|---|
| **Fuerza bruta simple** | Todas las combinaciones de un conjunto de caracteres y longitud | Sin información previa, espacio de búsqueda pequeño (PINs, claves cortas) |
| **Ataque de diccionario** | Lista precompilada de palabras/contraseñas comunes | Se sospecha contraseña débil o predecible — ver siguiente apartado |
| **Ataque híbrido** | Diccionario + variaciones (sufijos, prefijos, sustituciones) | Se sospecha una variante de una palabra común — ver apartado dedicado |
| **Credential stuffing** | Credenciales filtradas en otra brecha, probadas tal cual | Se dispone de una filtración pública y se sospecha reutilización de contraseñas |
| **Password spraying** | Pocas contraseñas comunes contra muchos usuarios | Existen políticas de bloqueo por intentos fallidos — evita disparar el bloqueo en una sola cuenta |
| **Reverse brute force** | Una contraseña conocida contra muchos nombres de usuario | Se sospecha que una contraseña filtrada se reutiliza en múltiples cuentas |
| **Distribuido** | Reparte la carga entre varias máquinas | Objetivo con contraseña muy compleja, requiere paralelismo masivo |

## Por qué password spraying merece atención especial

A diferencia de la fuerza bruta tradicional (muchos intentos contra **un** usuario), el *password spraying* invierte el enfoque: pocas contraseñas comunes, probadas contra **muchos** usuarios. Esto es deliberado — la mayoría de políticas de bloqueo de cuentas cuentan los intentos fallidos **por usuario**, no de forma global. Un atacante que prueba `Password123!` contra 500 cuentas distintas, una vez cada una, nunca dispara el umbral de bloqueo de ninguna cuenta individual, pese a realizar 500 intentos en total — el mismo principio de "evadir el control sin romperlo directamente" que ha aparecido repetidamente en este temario al hablar de listas negras y WAFs.

## Conectando con el resto del bloque

Los siguientes apartados profundizan en ataques de diccionario e híbridos —las variantes más usadas en la práctica, por su mejor relación entre eficiencia y probabilidad de éxito— antes de pasar a las herramientas (Hydra, Medusa) que automatizan cualquiera de estos enfoques contra servicios reales.
