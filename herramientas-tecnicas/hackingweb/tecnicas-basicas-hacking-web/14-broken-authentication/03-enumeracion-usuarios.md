# Enumeración de usuarios

## Por qué un nombre de usuario "no sensible" puede serlo

La enumeración de usuarios ocurre cuando una aplicación responde de forma **distinguible** según si el nombre de usuario probado existe o no, en puntos como login, registro o restablecimiento de contraseña. Muchos equipos de desarrollo asumen que el nombre de usuario no es información sensible — pero si ese mismo nombre de usuario es el identificador principal requerido para autenticarse, conocerlo de antemano reduce el problema de "adivinar usuario y contraseña" a "adivinar solo la contraseña", exactamente la misma idea trabajada en el bloque de *Login Brute Forcing* respecto a credenciales por defecto.

Además, los usuarios suelen reutilizar el mismo nombre de usuario entre múltiples servicios (aplicaciones web, FTP, SSH, RDP) — confirmar que existe en un sistema puede orientar ataques contra otros sistemas relacionados.

## El caso ilustrativo: WordPress

Incluso aplicaciones ampliamente desplegadas como WordPress han presentado, por defecto, mensajes de error distinguibles entre usuario inexistente y contraseña incorrecta. Esta diferencia, aparentemente menor, es exactamente la señal que un atacante necesita para confirmar sistemáticamente qué nombres de usuario existen, sin necesitar conocer ninguna contraseña todavía.

## Cuándo la enumeración es un trade-off aceptado, y cuándo es una vulnerabilidad

No toda enumeración de usuarios es automáticamente un fallo de seguridad. Una aplicación de mensajería que permite buscar usuarios por nombre **necesita**, por diseño, exponer esa información — es parte del servicio que ofrece. La cuestión relevante es: ¿esa misma información, expuesta sin querer en un punto de **autenticación**, reduce la seguridad del mecanismo de login? Si es así, conviene evitarlo siempre que sea posible — por ejemplo, usando el correo electrónico (más difícil de enumerar sistemáticamente, y generalmente no expuesto en redes sociales con la misma facilidad que un nombre de usuario corto) en lugar de un nombre de usuario corto como identificador de login.

## Detectando la diferencia de respuesta

El primer paso es comparar manualmente, con un nombre de usuario claramente inexistente y uno conocido como válido, si la aplicación devuelve algo distinguible:

```
Usuario inexistente   → "Unknown user"
Usuario válido, contraseña incorrecta → "Invalid password"
```

Cualquier diferencia en el texto del mensaje, el código de estado HTTP, o incluso el tiempo de respuesta (tratado más abajo) es una señal explotable.

## Automatizando la enumeración con fuzzing

Una vez confirmada la diferencia, el proceso se automatiza exactamente con las técnicas vistas en el bloque de *Web Fuzzing*: probar sistemáticamente una wordlist de nombres de usuario candidatos, filtrando las respuestas según el patrón identificado.

```bash
ffuf -w wordlist_usuarios.txt \
     -u http://10.10.10.5/login.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=FUZZ&password=invalid" \
     -fr "Unknown user"
```

`-fr` filtra (excluye) las respuestas que contienen la cadena indicativa de "usuario inexistente" — lo que queda visible en la salida son, precisamente, los nombres de usuario que **sí** existen, confirmados por recibir una respuesta distinta.

Fuentes habituales de wordlists de nombres de usuario: colecciones genéricas como las de SecLists, o listas construidas a partir de reconocimiento previo del objetivo (perfiles corporativos en redes sociales, convenciones de nomenclatura identificadas) — la misma lógica de "cuanto más orientada al objetivo, más eficiente" trabajada en el bloque anterior.

## Enumeración mediante canales laterales (side-channel)

Cuando la respuesta visible es **idéntica** para usuario válido e inválido (la aplicación ha sido cuidadosa en igualar el mensaje de error), aún puede existir una diferencia indirecta: si el backend solo realiza una consulta a base de datos cuando el nombre de usuario existe, el **tiempo de respuesta** puede variar de forma medible entre ambos casos, incluso con un mensaje final idéntico.

Esto es conceptualmente el mismo principio que la inyección SQL ciega basada en tiempo, vista en el bloque de *SQL Injection Fundamentals*: cuando no hay diferencia visible en el contenido, el tiempo de respuesta se convierte en el canal de información explotable. Detectar y explotar este tipo de diferencia de forma fiable requiere un análisis estadístico más cuidadoso que una simple comparación de texto, ya que la latencia de red introduce ruido — un terreno de explotación más avanzado que queda fuera del alcance introductorio de este bloque.

## Mitigación

- **Mensajes de error genéricos e idénticos** en cualquier escenario de fallo de login (`"Usuario o contraseña incorrectos"`, sin distinguir cuál de los dos falló).
- **Tiempos de respuesta equiparados**: realizar siempre el mismo trabajo computacional (por ejemplo, calcular igualmente un hash de comparación) independientemente de si el usuario existe, para no filtrar la diferencia por canal lateral.
- **Limitar la exposición de nombres de usuario** en otras funcionalidades (registro, restablecimiento de contraseña) con el mismo cuidado aplicado al login — un atacante puede enumerar usuarios a través de cualquier punto de la aplicación que filtre esta información, no solo el formulario de login.

## Por qué este es siempre el primer paso de un ataque de autenticación más amplio

Confirmar qué nombres de usuario existen es, casi siempre, el paso previo a cualquier otro ataque de autenticación: fuerza bruta de contraseña dirigida (bloque anterior), explotación de un mecanismo de restablecimiento débil, o bypass de autenticación — todos ellos requieren, como mínimo, saber **a quién** atacar. El resto de este bloque asume, en sus distintos apartados, que este paso de reconocimiento ya se ha completado.
