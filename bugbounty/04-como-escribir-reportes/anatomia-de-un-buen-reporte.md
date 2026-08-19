# Anatomía de un buen reporte

## 🧱 Estructura estándar (funciona en casi cualquier plataforma)

1. **Título** — claro, específico, en el formato: `Tipo de vulnerabilidad en <componente> permite <impacto>`.
   - ❌ "Fallo de seguridad en la app"
   - ✅ "IDOR en API de favoritos de demorgen.be permite leer/modificar/borrar la lista de otro usuario"

2. **Resumen (Summary)** — 3 a 6 frases que un no-técnico casi podría entender: qué es, dónde está, por qué es grave. El triager decide en los primeros segundos si esto merece atención — gánatelo aquí.

3. **Detalles técnicos** — CWE, endpoint, tipo de autenticación requerida, entorno usado.

4. **Pasos de reproducción (Steps to Reproduce) / PoC** — el corazón del reporte. Deben ser:
   - **Completos**: sin dar nada por sabido.
   - **Numerados**: paso a paso, en orden.
   - **Reproducibles por un tercero**: cualquier persona del equipo de seguridad, sin conocer tu setup, debe poder seguirlos literalmente y llegar al mismo resultado.
   - **Con comandos exactos** (curl, scripts) que se puedan copiar y pegar.
   - **Con evidencia visual** en cada paso relevante (ver [Evidencias](evidencias-capturas-videos.md)).

5. **Impacto (Impact)** — qué puede hacer un atacante real con esto. Evita quedarte en la superficie ("obtengo un 200"); explica la consecuencia de negocio: fuga de datos personales, pérdida de datos, fraude económico, toma de cuentas, etc.

6. **Severidad / CVSS** — la puntuación y el razonamiento vector por vector (ver [Cálculo de severidad](calculo-cvss.md)).

7. **Recomendación de solución (Recommended Fix)** — no es obligatorio en todas las plataformas, pero suma muchísimo. Demuestra que entiendes el problema de raíz, no solo el síntoma.

8. **Checklist de reproducción** — un resumen en formato lista de verificación de lo que se ha probado, útil para el triager y para ti mismo como control de calidad antes de enviar.

## ✅ Reglas de oro para que el reporte se entienda a la primera

- **Escribe como si el lector no supiera nada del contexto.** No asumas que sabe qué es un CUPS, qué hace tu script, o por qué elegiste ese endpoint.
- **Un reporte, una vulnerabilidad.** Si encuentras algo relacionado pero distinto, ábrelo en un reporte aparte (puedes referenciarlo).
- **Incluye siempre un "control negativo".** Es decir, demuestra qué pasa SIN el fallo (por ejemplo: sin token → 401; token roto → 422) para probar que el servidor sí está validando algo, y que tu hallazgo no es "el endpoint simplemente no comprueba nada nunca".
- **No exageres el impacto, pero tampoco lo minimices.** Sé preciso y dejar que los hechos hablen.
- **Cierra el bucle de "qué NO hiciste y por qué".** Si te detuviste antes de tocar datos reales de un cliente, dilo explícitamente — genera confianza y demuestra profesionalidad (ver ejemplo en [YesWeHack — JWT hardcodeado](../06-ejemplos-reales/yeswehack-jwt-hardcodeado.md), sección de respuesta al "Need more info").

## 🧩 Plantilla genérica reutilizable

```markdown
# [Tipo de vulnerabilidad] en [componente] permite [impacto resumido]

## Resumen
(3-6 frases explicando qué es, dónde y por qué importa)

## Detalles técnicos
- CWE: 
- Endpoint/Componente afectado: 
- Autenticación requerida: 
- Entorno de pruebas: 

## Pasos de reproducción
1. ...
2. ...
3. ...
(con capturas/comandos en cada paso relevante)

## Impacto
(qué puede hacer un atacante real, en términos de negocio)

## Severidad (CVSS)
(vector completo + puntuación + breve justificación)

## Recomendación de solución
(causa raíz + fix sugerido)

## Checklist de reproducción
- [x] ...
- [x] ...
```
