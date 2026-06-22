# Fundamentos de la seguridad de contraseñas

## Qué es la fuerza bruta

Un ataque de fuerza bruta es un método de prueba sistemática: probar combinaciones de credenciales una a una hasta encontrar la correcta, en lugar de explotar un fallo lógico o de validación. Su éxito depende de tres factores:

- **Complejidad de la contraseña objetivo**: más longitud y variedad de caracteres multiplica exponencialmente el espacio de combinaciones a probar.
- **Capacidad de cómputo disponible**: más hilos, más peticiones por segundo, reducen el tiempo necesario.
- **Medidas de protección del objetivo**: bloqueo de cuentas, CAPTCHA, límites de tasa, pueden frustrar el ataque incluso con una contraseña débil.

## Anatomía de una contraseña fuerte (guía NIST)

| Propiedad | Por qué importa |
|---|---|
| **Longitud** | El factor más determinante — una contraseña de 6 caracteres en minúsculas tiene ~308 millones de combinaciones; una de 8, ~208 mil millones. Cada carácter adicional multiplica el espacio de búsqueda. |
| **Complejidad** | Combinar mayúsculas, minúsculas, números y símbolos amplía el conjunto de caracteres posibles por posición (26 → 52 → 62 → más de 90). |
| **Unicidad** | No reutilizar la misma contraseña entre cuentas — si una se filtra, todas las que la comparten quedan expuestas (la base del *credential stuffing*, visto en el siguiente apartado). |
| **Aleatoriedad** | Evitar palabras de diccionario o información personal predecible — la base de los ataques de diccionario. |

## Debilidades habituales que hacen viable la fuerza bruta

- Contraseñas cortas (menos de 8 caracteres).
- Palabras o frases comunes, vulnerables a ataques de diccionario.
- Información personal predecible (fechas, nombres de mascotas).
- Reutilización de contraseñas entre servicios.
- Patrones predecibles (`qwerty`, `123456`, sustituciones obvias como `p@ssw0rd`).

## El peligro de las credenciales por defecto

Muchos dispositivos y servicios se distribuyen con un usuario y contraseña predefinidos, ampliamente documentados públicamente. Algunos ejemplos clásicos, muy citados en listas de credenciales por defecto:

| Dispositivo | Usuario típico | Contraseña típica |
|---|---|---|
| Routers domésticos genéricos | `admin` | `admin` / `password` |
| Cámaras IP genéricas | `admin` | `1234` / `4321` |
| Puntos de acceso Ubiquiti | `ubnt` | `ubnt` |
| DVR/grabadores genéricos | `admin` | `12345` |

Estas tablas existen porque los fabricantes reutilizan las mismas credenciales en miles de unidades, y muchos usuarios nunca las cambian. Conocer esto reduce drásticamente el "espacio de búsqueda" en una auditoría: antes de lanzar cualquier fuerza bruta genérica, comprobar credenciales por defecto conocidas para la marca/modelo identificado (mediante fingerprinting, visto en el bloque de *Information Gathering*) es siempre el primer paso, de coste casi nulo.

Igual de relevante es el **nombre de usuario** por defecto (`admin`, `root`, `user`): conocerlo de antemano reduce el problema de "adivinar usuario y contraseña" a "adivinar solo la contraseña" — la mitad del trabajo ya está hecho. SecLists mantiene listas curadas de nombres de usuario comunes (`top-usernames-shortlist.txt`) precisamente para sistematizar esta comprobación.

## Por qué este conocimiento importa en una auditoría

Entender la seguridad de contraseñas desde la perspectiva defensiva es lo que permite, como pentester, decidir con criterio **qué tipo de ataque** tiene sentido en cada escenario:

- Política de contraseñas débil o ausente → mayor probabilidad de éxito con diccionario simple.
- Cuenta de administrador conocida en un dispositivo identificado → comprobar primero credenciales por defecto, antes de cualquier ataque sistemático.
- Indicios de reutilización de contraseñas (filtración pública conocida de la organización) → *credential stuffing* puede ser más eficiente que fuerza bruta pura.

El resto de este bloque desarrolla estas variantes con más detalle, antes de pasar a las herramientas prácticas (Hydra, Medusa) que automatizan su ejecución.
