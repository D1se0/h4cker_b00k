# ¿Qué es el Bug Bounty?

## 🧠 La idea en una frase

Una empresa dice públicamente: *"si encuentras un fallo de seguridad en mis sistemas y me lo reportas de forma responsable, te lo agradezco (a veces con dinero, otras con puntos, reconocimiento o ambas cosas)"*. Eso es, en esencia, un programa de **Bug Bounty**.

En lugar de depender únicamente de auditorías internas o de una empresa de pentesting concreta, la organización abre (total o parcialmente) sus sistemas a una comunidad de investigadores de seguridad ("hunters") que buscan vulnerabilidades a cambio de una recompensa.

## 🔄 Cómo funciona el ciclo completo

1. **La empresa publica un programa** en una plataforma (YesWeHack, Intigriti, HackerOne, Secur0, Bugcrowd...) definiendo:
   - **Alcance (scope)**: qué dominios, apps o repositorios se pueden testear.
   - **Fuera de alcance (out of scope)**: qué NO se puede tocar.
   - **Reglas de compromiso**: qué tipo de pruebas están permitidas (por ejemplo, "no hagas fuerza bruta", "no uses escáneres automáticos agresivos", "no toques cuentas de usuarios reales").
   - **Recompensas**: tabla de bounties según severidad (CVSS) o política de puntos/reconocimiento.
   - **Safe Harbor**: compromiso legal de que, si sigues las reglas, no te van a demandar por investigar.

2. **El investigador (tú) busca vulnerabilidades** dentro de ese alcance, siguiendo siempre las reglas del programa.

3. **Se redacta y se envía un reporte** explicando: qué se ha encontrado, cómo reproducirlo paso a paso, y cuál es el impacto real.

4. **El equipo de seguridad de la empresa (o un triager de la plataforma) revisa el reporte**, intenta reproducirlo, y decide:
   - ✅ **Aceptado / Válido** → se corrige y normalmente se recompensa.
   - ❓ **Necesita más información** → te piden aclarar algo (¡es normal, no te lo tomes a mal!).
   - ❌ **No aplica / Duplicado / Fuera de alcance** → no se acepta, con explicación.

5. **Una vez corregido**, muchas plataformas permiten publicar el reporte (a veces con retraso, para no exponer la vulnerabilidad mientras sigue activa).

## 💶 ¿Y el dinero?

No todos los programas pagan. Hay tres grandes modelos:

| Modelo | Qué obtienes | Ejemplo típico |
|---|---|---|
| **Recompensa económica (bounty)** | Dinero por vulnerabilidad válida, según severidad | Programas privados/públicos con presupuesto |
| **VDP (Vulnerability Disclosure Program)** | Reconocimiento, "Hall of Fame", certificado, sin pago | Muchas administraciones públicas y ONGs |
| **Puntos / Reputación** | Puntos internos de la plataforma que suben tu ranking y desbloquean programas privados mejor pagados | Común en fases iniciales de todas las plataformas |

> 💡 **Tip importante**: no descartes los VDP sin recompensa económica al empezar. Son perfectos para aprender a reportar bien, sin la presión de "esto tiene que valer dinero", y muchas veces dan acceso a programas privados mejores.

## ⚖️ Legalidad: el "Safe Harbor"

Esto es clave y mucha gente lo pasa por alto: **solo estás autorizado a testear lo que el programa dice explícitamente que está en scope, y solo con las técnicas permitidas.** Salirte de ahí (por ejemplo, tocar cuentas de usuarios reales, hacer DoS, acceder a datos que no son tuyos "para comprobar") puede convertir una investigación legítima en un delito, aunque tu intención fuera buena.

Reglas de oro:

- 🔒 Lee el scope y las reglas **antes** de tocar nada.
- 🔒 Nunca accedas a datos de usuarios reales aunque "solo sea para confirmar el impacto". Se explica el impacto sin necesidad de robar el dato.
- 🔒 Si algo te da acceso a un panel de administración o a datos masivos, **para inmediatamente** y repórtalo con lo mínimo imprescindible como prueba.
- 🔒 Guarda siempre evidencia de que tus pruebas fueron mínimas y no destructivas.

## 🌍 Plataformas más conocidas

- **HackerOne**
- **Bugcrowd**
- **Intigriti**
- **YesWeHack**
- **Secur0** (más centrada en comunidad hispana)
- Programas propios gestionados directamente por la empresa (sin intermediario)

En este manual nos centramos en las tres que uso yo: **YesWeHack**, **Secur0** e **Intigriti**.
