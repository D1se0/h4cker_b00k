# Qué es la autenticación

## Autenticación vs. autorización: una distinción que importa

Aunque a menudo se mencionan juntas, son conceptos distintos:

- **Autenticación**: confirmar que una entidad es quien dice ser ("¿quién eres?").
- **Autorización**: determinar qué puede hacer esa entidad, una vez identificada ("¿qué tienes permitido hacer?").

Este bloque se centra en la primera. La segunda —control de acceso roto, IDOR— se trata en detalle en el bloque de *Web Attacks*. Tener clara esta distinción evita confundir un hallazgo de "puedo entrar sin credenciales válidas" (autenticación) con uno de "entré legítimamente pero puedo hacer más de lo que debería" (autorización).

## Los tres factores de autenticación

| Factor | Se basa en | Ejemplos |
|---|---|---|
| **Conocimiento** | Algo que el usuario *sabe* | Contraseña, PIN, respuesta a pregunta de seguridad |
| **Posesión** | Algo que el usuario *tiene* | Token de seguridad, móvil con app de autenticación, tarjeta |
| **Inherencia** | Algo que el usuario *es* | Huella dactilar, reconocimiento facial, patrón de voz |

### Por qué cada factor tiene un perfil de riesgo distinto

**Conocimiento** es el más extendido y, precisamente por eso, el más atacado: la información puede obtenerse mediante phishing, fuerza bruta (bloque anterior), o filtraciones de datos — y es el foco principal de este bloque.

**Posesión** es más resistente a ataques remotos (un atacante no puede "adivinar" un token físico), pero introduce su propio riesgo: robo físico o clonación del objeto.

**Inherencia** ofrece comodidad, pero tiene una propiedad única y preocupante: **es irrevocable**. Si una contraseña se filtra, se cambia. Si una huella dactilar se filtra en una brecha de datos, no hay forma de "cambiarla" — la persona queda permanentemente expuesta para cualquier sistema que dependa de ese mismo rasgo biométrico. Esta es una de las razones por las que la autenticación basada exclusivamente en inherencia se considera, en ciertos contextos, más arriesgada a largo plazo que el conocimiento pese a su comodidad de uso.

## Autenticación de un solo factor vs. multifactor (MFA)

- **Un solo factor**: depende exclusivamente de un mecanismo (típicamente, solo contraseña). Si ese único factor se compromete, el atacante obtiene acceso completo.
- **MFA (Multi-Factor Authentication)**: combina dos o más factores de categorías distintas. Cuando son exactamente dos, se habla de **2FA**.

La fortaleza de MFA reside en que comprometer un único factor (por ejemplo, robar la contraseña vía phishing) no es suficiente — el atacante también necesitaría el segundo factor, normalmente mucho más difícil de obtener de forma remota.

> **Matiz importante**: dos factores del **mismo tipo** (contraseña + pregunta de seguridad, ambas de conocimiento) no constituyen verdadero MFA, aunque sean dos pasos — siguen compartiendo la misma debilidad estructural (ambas son "algo que se sabe", y por tanto vulnerables a las mismas técnicas de obtención). MFA real requiere combinar factores de **categorías distintas**.

## Por qué este bloque se centra en autenticación basada en conocimiento

De los tres factores, el basado en conocimiento es el más común en aplicaciones web y, por su propia naturaleza (información estática que puede memorizarse, transmitirse, adivinarse o filtrarse), el que ofrece la superficie de ataque más amplia y diversa. El resto de este bloque desarrolla, en profundidad, las distintas formas en que la autenticación basada en conocimiento —y, en menor medida, su combinación con un segundo factor de posesión (2FA)— puede implementarse de forma insegura y explotarse en consecuencia.
