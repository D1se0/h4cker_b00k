---
icon: trophy-star
---

# Intigriti — IDOR en API de favoritos

> 🔒 **CONFIDENCIAL — INFORMACIÓN REDACTADA** Este es un reporte real que envié, con el dominio real, los UUID de las cuentas de prueba y la IP ocultados con efecto "rotulador negro". Se comparte solo como referencia de **formato y metodología**, no como PoC explotable.

**Plataforma:** Intigriti **Programa:** \[Grupo de medios de comunicación — nombre redactado] **Severidad:** Media (4.2) **Estado:** Triage

***

## Título

IDOR en la API de favoritos de \[medio.ejemplo] permite a cualquier usuario autenticado leer, añadir y borrar los guardados de otro usuario

## Resumen

La función de "guardar artículo" (favoritos) del sitio está respaldada por un único recurso de API, `/api/_next-api/bookmarks/`, que recibe el `userId` de la cuenta como **campo controlado por el cliente** — en el body al escribir, en la query string al leer — en lugar de derivarlo del lado del servidor a partir de la sesión autenticada (el claim `sub` del JWT de sesión, o equivalente).

El backend nunca comprueba que el `userId` proporcionado por el cliente coincida con la sesión que está llamando. Resultado: **dos cuentas autenticadas cualesquiera pueden leer, añadir y borrar entre sí en sus listas de artículos guardados**, con solo conocer el UUID de la cuenta objetivo. Esto es un BOLA completo — no solo divulgación, sino lectura, escritura y borrado no autorizados sobre datos de otro usuario.

Reproducido de extremo a extremo, en vivo, con **dos cuentas de prueba desechables** (solo cuentas propias, sin tocar en ningún momento datos de un usuario real): la cuenta A escribió un artículo en la lista de favoritos de la cuenta B estando autenticada como A, y la cuenta B — sin hacer nada ella misma — lo vio aparecer en su propia lista momentos después, con el mismo timestamp `changedOn` exacto que devolvió la escritura.

Todos los datos de prueba se limpiaron inmediatamente tras cada reproducción; ambas cuentas quedaron con la lista vacía, tal y como estaban antes de empezar.

## Detalles técnicos

| Campo                   | Valor                                                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CWE                     | CWE-639 (Authorization Bypass Through User-Controlled Key)                                                                           |
| Endpoints               | `POST /api/_next-api/bookmarks/` (escritura/borrado) y `GET /api/_next-api/bookmarks/?userId=<uuid>` (lectura)                       |
| Autenticación requerida | Sí — dos cuentas distintas y autenticadas (el atacante solo necesita su propia sesión válida; no requiere interacción de la víctima) |
| Tipo de identificador   | UUIDv4 (`userId`)                                                                                                                    |

## Pasos de reproducción (resumen)

Dos cuentas de prueba desechables, creadas específicamente para este test:

* Cuenta A (atacante): `userId =` \[UUID redactado]
* Cuenta B (víctima): `userId =` \[UUID redactado]

**1 — Línea base**: confirmar que la lista de la cuenta B empieza vacía, autenticado como B.

**2 — El ataque**: autenticado como A, escribir en la lista de B:

```javascript
(async () => {
  const cookie = document.cookie.split('; ').find(c => c.startsWith('login-state='));
  const me = JSON.parse(decodeURIComponent(cookie.split('login-state=')[1]));
  const victimId = "<mark style='background-color:#000;color:#000;user-select:none'>[UUID de B redactado]</mark>";
  const r = await fetch('https://<mark style="background-color:#000;color:#000;user-select:none">[dominio-medio.ejemplo]</mark>/api/_next-api/bookmarks/', {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({shortId: 'ejemplo123', userId: victimId, bookmarked: true})
  });
  const body = await r.json();
  console.log('Atacante (yo):', me.userId, '| Víctima objetivo:', victimId, '| Status:', r.status, '| Respuesta:', body);
})();
```

Esta es la evidencia clave: la misma línea de consola muestra quién está autenticado realmente (`me.userId`, resuelto desde la cookie de sesión, no escrito a mano), qué ID de víctima se apuntó, y la aceptación 200 del servidor con el objeto persistido de vuelta.

**3 — Control**: confirmar, todavía como A, que la escritura NO aterrizó en la propia lista del atacante (descarta la explicación trivial de que el endpoint ignora `userId` y siempre escribe en la cuenta del que llama).

**4 — Confirmación**: autenticado de nuevo como B, ejecutar el mismo script de lectura del paso 1 — el `changedOn` es **idéntico byte a byte** al devuelto por la escritura de A en el paso 2. B nunca guardó nada; el artículo apareció en su lista puramente como efecto secundario de que A nombrara su `userId`.

**5 — Limpieza**: como B, revertir el `bookmarked` a `false`. Ambas cuentas terminan exactamente en el mismo estado vacío en el que empezaron.

## Reproducido varias veces, de forma consistente

| Ronda | Método                                                                                                                                    | Resultado                                                                                                                               |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | Consola del navegador, cuentas A/B (evidencia de este reporte)                                                                            | Ciclo completo lectura→escritura→control→lectura, timestamps `changedOn` coincidentes exactamente entre escritura y relectura           |
| 2     | Consola del navegador, mismas cuentas, sesión distinta el mismo día                                                                       | Mismo resultado: 200 en escritura cruzada, `[]` en control del atacante, relectura de la víctima con el mismo `changedOn`               |
| 3-5   | Consola del navegador, otro par de cuentas, 3 rondas independientes con distintos artículos, incluyendo ciclos completos de añadir+borrar | 200 consistente en cada escritura/borrado cruzado; la lista de la víctima se actualizó en todos los casos sin interacción de la víctima |

## Impacto

BOLA completo, no solo divulgación. Un atacante que conozca (u obtenga) el `userId` de otra cuenta puede, sin consentimiento y sin ninguna señal visible para la víctima:

* Leer su lista completa de artículos guardados (puede revelar hábitos de lectura/intereses).
* Añadir artículos arbitrarios a su lista.
* Borrar artículos que la víctima sí guardó realmente — una pérdida de datos real y persistente, no solo una fuga de privacidad.

El `userId` no está bien protegido como secreto: es accesible desde cualquier script que corra en la sesión autenticada del propio dueño de la cuenta (cookie no `HttpOnly` legible por JavaScript, y también expuesto en el `dataLayer` de analítica en cada carga de página autenticada). Esto significa que cualquier script de terceros que se ejecute en el navegador de un usuario logueado (publicidad, analítica, o un XSS no relacionado en otra propiedad del mismo grupo) podría recolectar ese `userId` y usarlo contra este endpoint.

No se requiere ninguna interacción de la víctima en ningún momento, y el ataque es trivialmente scriptable (como se ve en la PoC, una sola llamada `fetch()`).

**Nota sobre severidad**: el identificador es un UUIDv4, no enumerable ni adivinable, así que según la guía de severidad propia del programa esto se clasificaría como Bajo en principio. Como factor agravante: no es un IDOR de solo lectura — es lectura + escritura + borrado sobre datos de otra cuenta, y el UUID queda expuesto de forma pasiva en el lado del cliente en cada carga de página autenticada, en vez de algo que haya que forzar por fuerza bruta.

## Solución recomendada

El backend de `/api/_next-api/bookmarks/` debe derivar el `userId` propietario del recurso desde la sesión autenticada del lado del servidor (el claim `sub` del JWT de sesión, o equivalente), e ignorar o validar estrictamente cualquier `userId` recibido del cliente. Si un `userId` proporcionado por el cliente no coincide con el de la propia sesión, la petición debe rechazarse con `403 Forbidden`. Esto aplica tanto a la ruta GET (lectura) como a la POST (escritura/borrado) de este endpoint — ambas confían actualmente por igual en el valor proporcionado por el cliente.

Como medida adicional de refuerzo, considerar sacar el valor de `userId`/ID de cuenta de una cookie plana y legible por script, y del `dataLayer`, ya que — independientemente de este fallo concreto — funciona como identificador estable entre distintas propiedades del mismo grupo.

***

> 📌 **Por qué este reporte funcionó bien**: el script de consola que imprime "quién soy yo" + "qué pido" + "qué contesta el servidor" en una sola línea elimina cualquier ambigüedad sobre si la sesión activa era realmente la del atacante. Combinado con el timestamp `changedOn` idéntico entre la escritura de A y la lectura de B, la persistencia del efecto queda demostrada sin lugar a dudas — sin necesidad de tocar ninguna cuenta real.
