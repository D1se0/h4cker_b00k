# Clasificación de ataques a la autenticación

## Organizando los ataques según el factor que explotan

Siguiendo la clasificación de factores de autenticación vista en el apartado anterior, los ataques a la autenticación se pueden agrupar de la misma forma — lo que ayuda a entender por qué cada tipo de ataque funciona y qué lo hace posible.

## Ataques contra autenticación basada en conocimiento

Es, con diferencia, la categoría más amplia y la que centra el resto de este bloque. Su debilidad estructural es que depende de información **estática** que puede:

- **Obtenerse**: mediante phishing, ingeniería social, o simplemente observando comportamientos de la aplicación que revelan información (como se verá en el apartado de enumeración de usuarios).
- **Adivinarse**: mediante fuerza bruta o ataques de diccionario, trabajados en profundidad en el bloque anterior.
- **Filtrarse**: en brechas de datos de terceros, alimentando ataques de *credential stuffing*.

## Ataques contra autenticación basada en posesión

Más resistente a ataques puramente remotos (phishing, adivinación), pero vulnerable a:

- **Robo o clonación física** del objeto de autenticación.
- **Ataques criptográficos** contra el algoritmo subyacente, si está mal implementado.

Un ejemplo conceptual: clonar una tarjeta NFC en un espacio público con suficiente proximidad física al objeto original es un vector de ataque real contra este tipo de autenticación, ajeno por completo a las técnicas de inyección o fuerza bruta trabajadas en otros bloques de este temario.

## Ataques contra autenticación basada en inherencia

El riesgo distintivo de esta categoría, ya mencionado en el apartado anterior, es la **irreversibilidad**: un rasgo biométrico filtrado no puede "cambiarse" como una contraseña. Un caso real ilustrativo: en 2019, una filtración en una empresa de cerraduras inteligentes biométricas expuso huellas dactilares y patrones faciales completos de usuarios registrados, junto con sus credenciales. A diferencia de una filtración de contraseñas (mitigable cambiándolas), los usuarios afectados no tenían forma de "revocar" sus propias huellas dactilares — una limitación estructural inherente a este factor de autenticación.

## Por qué este bloque se centra en conocimiento

De las tres categorías, la autenticación basada en conocimiento es la más extendida en aplicaciones web y la que ofrece la superficie de explotación más amplia y diversa desde una perspectiva de pentesting web — exactamente el terreno que se desarrolla en el resto de este bloque: enumeración de usuarios, fuerza bruta dirigida (tokens de reset, códigos 2FA), credenciales por defecto, mecanismos de restablecimiento de contraseña mal diseñados, y bypass de la lógica de autenticación mediante acceso directo o manipulación de parámetros.

## El hilo conductor de todo el bloque

Cada apartado siguiente desarrolla una vía distinta por la que la autenticación basada en conocimiento puede fallar — no porque la contraseña en sí sea débil (eso ya se cubrió en el bloque anterior), sino porque la **lógica que la rodea** —cómo se valida, cómo se restablece, cómo se protege frente a intentos repetidos, cómo se mantiene la sesión después— contiene fallos de diseño que un atacante puede explotar independientemente de lo robusta que sea la contraseña original.
