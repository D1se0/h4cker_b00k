# Mentalidad y metodología general

## 🧭 El cambio de chip más importante

Cuando empiezas, tiendes a pensar "voy a buscar una vulnerabilidad guay tipo RCE o SQLi". La realidad del bug bounty en 2026 es otra: **la mayoría de reportes válidos y pagados vienen de fallos de lógica de negocio y de control de acceso** (IDOR/BOLA, credenciales hardcodeadas, autenticación rota, exposición de datos sensibles), no de exploits sofisticados.

> 🎯 La pregunta que te tiene que perseguir todo el rato es: **"¿qué pasaría si cambio este valor que no debería poder cambiar?"**

## 🔁 El bucle de trabajo (loop) que mejor me funciona

1. **Elegir un programa** con scope claro y, si eres nuevo, preferiblemente un VDP o un programa con buena reputación de respuesta rápida.
2. **Recon**: mapear todo lo que existe (subdominios, apps, endpoints, tecnologías). Ver [Reconocimiento](../03-metodologia-y-recon/reconocimiento.md).
3. **Entender el flujo normal de la aplicación como usuario legítimo.** Regístrate, navega, usa las funciones tal y como se supone que hay que usarlas. No puedes romper lo que no entiendes.
4. **Identificar "fronteras de confianza"**: cualquier punto donde el cliente (app/navegador) le dice al servidor "soy fulano" o "quiero el recurso X". Ahí es donde suelen vivir los IDOR/BOLA.
5. **Probar hipótesis pequeñas y controladas**, siempre con cuentas propias / datos inventados.
6. **Documentar en el momento**, no al final. Captura cada paso mientras lo haces, no confíes en tu memoria luego.
7. **Confirmar el impacto real** antes de reportar (ver más abajo "Impacto ≠ diferencia de código de estado").
8. **Reportar de forma clara y reproducible.**
9. **Responder rápido a las peticiones de info del triager.** La velocidad de respuesta influye mucho en la relación con el programa.

## ⚠️ "Impacto ≠ diferencia de código de estado"

Uno de los rechazos más comunes para principiantes es: *"Solo demuestras un 200 en vez de un 401, pero no demuestras impacto real."* Esto es MUY importante y aparece literalmente en uno de los ejemplos reales de este manual (ver [YesWeHack — JWT hardcodeado](../06-ejemplos-reales/yeswehack-jwt-hardcodeado.md)).

No basta con decir "obtengo una respuesta distinta". Hay que demostrar **qué puede hacer un atacante con eso**:
- ¿Puede leer datos que no son suyos?
- ¿Puede escribir/modificar datos de otro usuario?
- ¿Puede eliminar algo?
- ¿Puede evitar un control de seguridad (login, 2FA, rate limit)?

Si tu PoC solo muestra "antes daba 401 y ahora da 200", el triager tiene todo el derecho a pedirte más. Anticípate: añade siempre la prueba del **antes/después con datos reales de tus propias cuentas de prueba**, mostrando lectura, escritura o eliminación de un recurso.

## 🧱 Pensar en "capas" de un sistema

Cuando audites algo, ve capa por capa, no lo tires todo a la vez:

1. **Cliente (frontend/app)**: ¿qué información expone el código (JS bundles, APKs, IPAs)? ¿Qué valida y qué no?
2. **Transporte**: ¿usa HTTPS correctamente? ¿Hay endpoints internos expuestos por error?
3. **Autenticación**: ¿cómo identifica el sistema quién eres? ¿Tokens, cookies, JWT?
4. **Autorización**: una vez sabe quién eres, ¿comprueba de verdad que puedes hacer lo que pides?
5. **Lógica de negocio**: ¿hay pasos que se pueden saltar, repetir, o hacer en otro orden?
6. **Datos**: ¿qué se guarda, cómo se valida, cómo se sanea antes de mostrarlo?

## 🕐 Gestión del tiempo (y de la frustración)

- No vas a encontrar nada los primeros días/semanas. Es normal.
- Time-boxing: dedica bloques de tiempo definidos a un programa, no te obsesiones sin límite con uno solo.
- Lleva notas de lo que ya probaste (para no repetirte) y de ideas pendientes.
- Cuando encuentres algo, para y documenta ANTES de seguir buscando más — se te olvidan los detalles rápido.
