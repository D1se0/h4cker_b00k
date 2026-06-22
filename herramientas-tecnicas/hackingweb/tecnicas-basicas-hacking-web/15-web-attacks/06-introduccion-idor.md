# Introducción a IDOR

## Qué es

**IDOR (Insecure Direct Object Reference)** ocurre cuando una aplicación web expone una referencia directa a un objeto interno (un ID de base de datos, un nombre de archivo, un número de registro) **y no verifica en el servidor** que el usuario autenticado que hace la petición tenga realmente permiso sobre ese objeto concreto.

```
GET /download.php?file_id=123   → descarga el archivo 123 del usuario actual
GET /download.php?file_id=124   → ¿descarga el archivo 124 de OTRO usuario?
```

Si la respuesta a la segunda pregunta es "sí, y el servidor no impide nada", existe una vulnerabilidad IDOR.

## Por qué IDOR no es "solo exponer un ID"

El simple hecho de exponer un identificador numérico o predecible en una URL **no es por sí solo la vulnerabilidad** — es la ausencia de control de acceso en el servidor lo que la crea. Un identificador perfectamente visible pero protegido por una verificación server-side robusta ("¿el usuario autenticado es el propietario de `file_id=124`?") no es vulnerable. IDOR aparece cuando esa verificación no existe o es insuficiente.

Esta distinción importa al documentar hallazgos: el problema que hay que reportar y corregir es la **ausencia de control de acceso**, no la "predicibilidad del ID" en sí.

## Por qué es la vulnerabilidad más reportada en bug bounty

- Muy fácil de detectar: cambiar un número en una URL o en el cuerpo de una petición es trivial, sin herramientas especiales.
- Muy frecuente: implementar control de acceso completo en cada endpoint de una aplicación grande es complejo, y los desarrolladores a menudo confían en que "el frontend no expone esa funcionalidad a los usuarios sin permisos" — la misma lógica incompleta que hemos visto en cada bloque de este temario.
- Alto impacto demostrable: acceder a datos de otro usuario es un hallazgo concreto, fácilmente reproducible, con impacto de privacidad inmediato.

## El impacto según el tipo de objeto expuesto

| Tipo de IDOR | Impacto |
|---|---|
| Referencia a archivo/recurso | Acceso a datos privados de otro usuario (documentos, imágenes, datos personales) |
| Referencia a función/acción | Llamar funcionalidad reservada a otro rol (p.ej., funciones de admin) |
| Referencia modificable | Modificar o eliminar datos de otro usuario |

El tercer tipo — IDOR que permite modificar, no solo leer — es el de mayor gravedad, ya que no solo expone privacidad sino que permite alterar el estado de la aplicación en nombre de otro usuario.

## El rol del frontend en el problema

Muchas aplicaciones "protegen" las funciones administrativas simplemente ocultando los botones en la interfaz visual para usuarios sin ese rol — pero los endpoints de API que esas funciones invocan siguen siendo accesibles si se llaman directamente. Esto conecta directamente con el principio trabajado desde el bloque de *Introducción a Aplicaciones Web*: **el frontend no protege nada por sí mismo**. Todo control real debe existir en el servidor, verificando en cada petición que el usuario autenticado tiene realmente permiso sobre lo que está solicitando.

## Por qué incluso aplicaciones grandes lo tienen

Facebook, Instagram, Twitter — todas han tenido vulnerabilidades IDOR reportadas públicamente. No es una vulnerabilidad exclusiva de aplicaciones pequeñas o mal mantenidas. La razón es estructural: a medida que una aplicación crece en número de endpoints, funcionalidades y tipos de usuario, mantener una verificación de control de acceso consistente en **todos** los puntos de entrada se vuelve cada vez más complejo. Una sola omisión en un endpoint nuevo, una API interna que se asumió que no era accesible, o una función añadida con prisa sin pasar por la revisión de seguridad habitual — cualquiera de estos escenarios produce un IDOR real en producción.
