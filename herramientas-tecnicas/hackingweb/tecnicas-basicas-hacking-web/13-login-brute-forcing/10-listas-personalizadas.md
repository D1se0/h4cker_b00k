# Construyendo listas de palabras personalizadas

## Por qué las wordlists genéricas tienen un techo de efectividad

Listas como `rockyou.txt` o las colecciones de SecLists cubren un espectro amplio de contraseñas y nombres de usuario comunes, pero precisamente por su generalidad pueden ser ineficientes contra un objetivo concreto con convenciones propias de nomenclatura o patrones de contraseña específicos de su contexto. Una organización con una convención de nombres de usuario particular (por ejemplo, inicial del nombre + apellido), o un patrón de contraseñas corporativas reconocible (nombre de la empresa + año), difícilmente aparecerá representada de forma eficiente en una lista de propósito general.

Esto conecta directamente con lo trabajado en el apartado de *Ataques de diccionario* de este mismo bloque: cuanto más se adapta la wordlist al contexto real del objetivo, mayor es la probabilidad de éxito frente a una lista genérica de igual tamaño.

## Generando variantes de nombre de usuario a partir de nombre y apellido

Cuando se conoce el nombre completo de una persona pero no su nombre de usuario exacto en un sistema, existe un patrón reconocible de convenciones habituales que las organizaciones suelen seguir: nombre completo, inicial más apellido, nombre punto apellido, iniciales combinadas, y variantes similares.

Herramientas como **Username Anarchy** automatizan la generación sistemática de estas variantes a partir de un nombre y apellido, cubriendo en segundos decenas de combinaciones plausibles que llevaría mucho más tiempo enumerar a mano:

```bash
sudo apt install ruby -y
git clone https://github.com/urbanadventurer/username-anarchy.git
cd username-anarchy

./username-anarchy Nombre Apellido > candidatos_usuario.txt
```

El resultado incluye variantes como `nombreapellido`, `n.apellido`, `apellido.nombre`, iniciales combinadas, y otras combinaciones siguiendo convenciones corporativas habituales — exactamente el mismo principio de "generar variaciones sistemáticas a partir de un patrón base" visto en el apartado de ataques híbridos, aplicado aquí a nombres de usuario en lugar de a contraseñas.

## Por qué este enfoque es más eficiente que una lista genérica de nombres de usuario

Una lista genérica de millones de nombres de usuario reales (recopilados de filtraciones diversas) tiene baja probabilidad de contener exactamente la convención que una organización concreta usa internamente. Generar candidatos **a partir del patrón corporativo conocido** (si se ha identificado mediante reconocimiento previo, por ejemplo encontrando un correo corporativo con un formato reconocible) reduce drásticamente el espacio de búsqueda a variantes realmente plausibles, en lugar de depender del azar de que el nombre exacto aparezca en una lista masiva no orientada al objetivo.

## El límite ético de la personalización de wordlists

Llevar la personalización de una wordlist hasta el extremo de construir un perfil completo de una persona —su fecha de nacimiento, nombre de pareja, mascotas, intereses, extraídos de sus redes sociales— para generar candidatos de contraseña dirigidos contra ella específicamente, cruza del terreno de auditoría de seguridad de sistemas hacia el de **ingeniería social dirigida contra un individuo**. Aunque existen herramientas que automatizan ese proceso, ese nivel de perfilado personal queda fuera del alcance de este material: no se trata de una técnica que vaya a desarrollarse aquí en detalle, independientemente del contexto de auditoría.

Lo relevante a nivel conceptual, y que sí vale la pena retener: cuanta más información de contexto (no necesariamente personal de un individuo, sino organizacional — nombre de la empresa, productos, jerga del sector) se incorpore a una wordlist, mayor es su efectividad frente a una lista genérica — el mismo principio trabajado desde el apartado de fundamentos de este bloque, sin necesidad de cruzar hacia el perfilado de personas concretas.

## Cierre del bloque de Login Brute Forcing

Con esto se completa el recorrido de este bloque: desde los fundamentos matemáticos de la seguridad de contraseñas, pasando por los distintos tipos de ataque (diccionario, híbrido, spraying, credential stuffing), hasta las herramientas prácticas (Hydra, Medusa) para automatizar cualquiera de estos enfoques contra autenticación HTTP básica y formularios de login web. El siguiente bloque, *Broken Authentication*, retoma este terreno desde una perspectiva más amplia: no solo atacar la robustez de las contraseñas, sino identificar fallos estructurales en la propia lógica de autenticación y gestión de sesión de una aplicación.
