---
icon: calculator
---

# Cálculo de severidad (CVSS)

## 📐 Qué es CVSS

**CVSS (Common Vulnerability Scoring System)** es un estándar para puntuar objetivamente la severidad de una vulnerabilidad, de 0.0 (nula) a 10.0 (crítica). La mayoría de plataformas de bug bounty (YesWeHack, Intigriti, Secur0...) usan una calculadora CVSS integrada para que rellenes un formulario de métricas y te calcule la puntuación automáticamente — así que no necesitas memorizar fórmulas, pero sí entender qué significa cada métrica para rellenarlas bien.

## 🧮 Las métricas base (versión 3.1 / 4.0)

### Explotabilidad (cómo de fácil es explotarlo)

| Métrica                                 | Qué mide                                              | Valores típicos                                |
| --------------------------------------- | ----------------------------------------------------- | ---------------------------------------------- |
| **AV — Attack Vector**                  | Desde dónde se puede atacar                           | Red (Network) / Adyacente / Local / Físico     |
| **AC — Attack Complexity**              | Cuántas condiciones especiales hacen falta            | Bajo / Alto                                    |
| **AT — Attack Requirements** (CVSS 4.0) | Condiciones adicionales del entorno objetivo          | Ninguno / Presente                             |
| **PR — Privileges Required**            | Qué privilegios necesita el atacante antes de empezar | Ninguno / Bajo / Alto                          |
| **UI — User Interaction**               | ¿Necesita que la víctima haga clic/interactúe?        | Ninguno / Pasivo / Activo (o Required en v3.1) |

### Impacto en el sistema vulnerable

| Métrica                 | Qué mide                                                   |
| ----------------------- | ---------------------------------------------------------- |
| **C — Confidentiality** | ¿Se exponen datos que no deberían verse?                   |
| **I — Integrity**       | ¿Se pueden modificar datos/comportamiento que no deberían? |
| **A — Availability**    | ¿Se afecta la disponibilidad del servicio?                 |

### Impacto en sistemas subsiguientes (CVSS 4.0)

Si el impacto se extiende más allá del sistema directamente vulnerable (por ejemplo, comprometer una cuenta de empleado te da acceso a otro sistema conectado), CVSS 4.0 separa esto en métricas "Subsequent System" (VC/VI/VA) del impacto en el "Vulnerable System" (SC/SI/SA).

## 🎯 Cómo pensar cada métrica con ejemplos reales

* **AV (Attack Vector)**: si basta con una petición HTTP desde internet → `Red`. Si hace falta estar en la misma red local → `Adyacente`. Si hace falta acceso físico al dispositivo → `Físico`.
* **PR (Privileges Required)**: ¿el atacante necesita estar autenticado como CUALQUIER usuario (bajo), como administrador (alto), o no necesita nada (ninguno)? Ojo: en un IDOR, si el atacante necesita su propia cuenta normal para explotarlo, eso es `PR: Bajo`, no `Ninguno`.
* **UI (User Interaction)**: ¿la víctima tiene que hacer algo (clicar un link, abrir un archivo) para que el ataque funcione? Si el atacante puede actuar sin que la víctima haga nada → `Ninguno`.
* **C/I/A del sistema vulnerable**: piensa en términos de "¿cuánto, y de quién?". Leer el email de un usuario es `C: Bajo`; leer/exportar la base de datos completa de usuarios es `C: Alto`.

## 🗣️ Cómo justificar tu puntuación en el reporte

No basta con pegar el número final. Argumenta brevemente vector por vector, como en el ejemplo real del manual:

> _"AV:N (alcanzable por HTTP), AC:L (trivial — una sola petición de login), AT:N, PR:N (explotar una cuenta ya existente no requiere ningún privilegio, solo su email), UI:N. Sistema vulnerable VC:H/VI:H (acceso completo de lectura/escritura a la identidad de la cuenta comprometida); VA:N."_

Esto le ahorra trabajo al triager y demuestra que entiendes por qué tu hallazgo merece esa severidad — no es un número que has "sentido".

## ⚖️ Consejos honestos sobre severidad

* **Sé conservador pero justo.** Pedir sistemáticamente Crítico para todo erosiona tu credibilidad con el programa.
* **Ten en cuenta el contexto del programa**, no solo el CVSS "de libro". Algunos programas tienen sus propias tablas de recompensa por severidad, a veces ligeramente distintas del CVSS puro.
* **Si el triager ajusta tu severidad a la baja con una explicación razonada, no lo tomes como un ataque personal** — es habitual y parte del proceso.
* **Documenta el "peor escenario realista"**, no el hipotético extremo improbable. Un CVSS creíble y bien argumentado se acepta mejor que uno inflado.
